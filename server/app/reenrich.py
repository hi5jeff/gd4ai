"""重新「读懂」已入库的薄组件：抓真实源 → LLM 理解怎么用/对谁有帮助 → 更新 install/usage/描述
→ 重新向量化入库 + 更新 Meili + 清推荐缓存。

原则：grounded。抓不到源、或源内容太少 → 跳过，绝不凭空编使用方法。

用法（在 howai-api 容器内，能连内网 PG/embedding/mdbox）:
    python -m app.reenrich [--limit N] [--workers 4]
"""
import argparse
import concurrent.futures as cf
import re

from . import db, ingest, ingest_repo


def fetch_source(src: dict) -> str:
    """按组件的 source 抓原始资料：github→README，普通url→网页正文。"""
    src = src or {}
    repo = (src.get("repo") or "").strip()
    url = (src.get("url") or "").strip()
    if repo and "github.com" in repo:
        m = re.search(r'github\.com/([^/]+/[^/#?]+?)(?:/tree/[^/]+/(.+))?/?$', repo)
        if not m:
            return ""
        owner_repo = m.group(1).removesuffix(".git")
        path = m.group(2)
        for rn in ("README.md", "readme.md", "SKILL.md", "README.rst"):
            p = f"{path}/{rn}" if path else rn
            t = ingest_repo.gh_raw(owner_repo, p)
            if t:
                return t
        return ""
    target = url or repo
    if target.startswith("http"):
        try:
            return ingest_repo.fetch_web(target)
        except Exception:
            return ""
    return ""


def reenrich_one(row):
    """(id, doc) → 更新后的 doc；抓不到源/LLM空 → (id, 原因字符串)。"""
    cid, doc = row
    src = doc.get("source") or {}
    text = fetch_source(src)
    if not text or len(text) < 120:
        return (cid, "无源")
    u = ingest_repo.understand(
        doc.get("name", ""), doc.get("type", "tool"),
        src.get("repo") or src.get("url") or "", text)
    if not u:
        return (cid, "LLM空")
    ingest_repo.apply_understanding(doc, u)
    return (cid, doc)


THIN = ("(doc->'install'->>'notes_zh' = '详见来源链接' OR doc->'usage' IS NULL) "
        "AND (coalesce(doc->'source'->>'repo','') <> '' "
        "     OR coalesce(doc->'source'->>'url','') <> '')")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()

    db.pool.open()
    db.init_schema()
    with db.pool.connection() as conn:
        q = f"SELECT id, doc FROM components WHERE {THIN} ORDER BY id"
        if args.limit:
            q += f" LIMIT {args.limit}"
        rows = conn.execute(q).fetchall()
    print(f"待重理解的薄组件: {len(rows)}")

    updated, stats = [], {"无源": 0, "LLM空": 0}
    done = 0
    with cf.ThreadPoolExecutor(args.workers) as ex:
        for cid, res in ex.map(reenrich_one, rows):
            done += 1
            if isinstance(res, dict):
                updated.append(res)
            else:
                stats[res] = stats.get(res, 0) + 1
            if done % 25 == 0:
                print(f"  进度 {done}/{len(rows)}，已理解 {len(updated)}，跳过 {dict(stats)}")

    print(f"理解完成：更新 {len(updated)}，跳过 {dict(stats)}")
    if not updated:
        print("无可更新")
        return
    # 重新向量化（新描述更丰富→检索也更准）+ 落 PG + Meili + 清缓存
    ingest.upsert("components", updated)
    ingest.meili_index("components", updated,
                       ["type", "scenarios", "host_tools", "difficulty"])
    ingest.flush_reco_cache()
    print(f"✅ 已重入库 {len(updated)} 条（PG+向量+Meili），推荐缓存已清")


if __name__ == "__main__":
    main()
