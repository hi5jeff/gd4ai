"""从 CocoLoop hub 导入 skills：枚举 slug → 下载 zip → 读 SKILL.md + _meta.json
→ understand()（基于真实 SKILL.md，grounded）→ 一条 skill 组件。

用法（howai-api 容器内）:
    python -m app.ingest_cocoloop [--slugs a,b] [--limit N] [--dry-run] [--persist]
    留空 --slugs 时自动从 hub 首页/搜索页枚举可见 skill。
"""
import argparse
import concurrent.futures as cf
import io
import json
import re
import urllib.request
import zipfile

from . import ingest, ingest_repo as ir

HUB = "https://hub.cocoloop.cn"
DL = "https://dl.cocoloop.cn/bss/skills"


def _get(url, timeout=40):
    req = urllib.request.Request(url, headers={"User-Agent": "gd4ai-bot/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def fetch_slugs():
    """从 hub 首页 + 搜索页枚举可见 skill slug。"""
    slugs = set()
    for path in ("/", "/search"):
        try:
            html = _get(HUB + path).decode("utf-8", "ignore")
        except Exception:
            continue
        for m in re.findall(r"bss/skills/([A-Za-z0-9._-]+)", html):
            slugs.add(m[:-4] if m.lower().endswith(".zip") else m)
    return sorted(slugs)


def fetch_skill(slug):
    """下载 skill zip → 读 SKILL.md + _meta.json。带版本号失败则去版本重试。失败返回 None。"""
    tried = [slug]
    base = re.sub(r"-\d+(\.\d+)*$", "", slug)
    if base != slug:
        tried.append(base)
    for s in tried:
        try:
            data = _get(f"{DL}/{s}.zip")
            z = zipfile.ZipFile(io.BytesIO(data))
        except Exception:
            continue
        names = z.namelist()
        md_name = (next((n for n in names if n.lower().endswith("skill.md")), None)
                   or next((n for n in names if n.lower().endswith("readme.md")), None))
        skill_md = z.read(md_name).decode("utf-8", "ignore") if md_name else ""
        meta = {}
        if "_meta.json" in names:
            try:
                meta = json.loads(z.read("_meta.json"))
            except Exception:
                pass
        if len(skill_md) < 40 and not meta:
            continue
        # 标题优先级：_meta.displayName > SKILL.md 首个 #H1 > 去版本的 slug
        h1 = re.search(r"^#\s+(.+?)\s*$",
                       re.sub(r"^---.*?---\s*", "", skill_md, flags=re.S), re.M)
        name = (meta.get("displayName")
                or (h1.group(1) if h1 else "")
                or base.replace("-", " ")).strip()[:80]
        return {
            "slug": s,
            "name": name,
            "owner": meta.get("owner", ""),
            "skill_md": skill_md,
            "url": f"{DL}/{s}.zip",
        }
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slugs", default="", help="逗号分隔；留空则从 hub 枚举")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--persist", action="store_true")
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()

    slugs = [s.strip() for s in args.slugs.split(",") if s.strip()] or fetch_slugs()
    if args.limit:
        slugs = slugs[: args.limit]
    print(f"待处理 skill: {len(slugs)}", flush=True)

    from . import db
    if db.pool.closed:
        db.pool.open()
    existing, used = ir.load_state()

    def process(slug):
        sk = fetch_skill(slug)
        if not sk:
            return (slug, "下载/解析失败")
        desc0 = ir.norm_ws(sk["skill_md"])[:200] or sk["name"]
        doc, why = ir.make_component({
            "name": sk["name"], "description_zh": desc0, "url": sk["url"],
            "type": "skill", "kind": "tool", "scenarios": [],
            "ai_related": True, "keep": True,
        }, used, existing, source_text=sk["skill_md"])   # understand() 基于 SKILL.md
        return (slug, doc if doc else why)

    docs, skipped = [], {}
    with cf.ThreadPoolExecutor(args.workers) as ex:
        for slug, res in ex.map(process, slugs):
            if isinstance(res, dict):
                docs.append(res)
                print(f"  ✓ {res['name']} — {res['description_zh'][:44]}", flush=True)
            else:
                skipped[res] = skipped.get(res, 0) + 1
    print(f"产出 {len(docs)} 条，跳过 {skipped}", flush=True)

    if args.dry_run or not args.persist:
        print("(未落库)")
        return
    n = ingest.persist_docs(docs)
    print(f"✅ 落库 {n} 条（PG+Meili+向量）", flush=True)


if __name__ == "__main__":
    main()
