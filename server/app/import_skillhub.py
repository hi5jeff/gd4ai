"""skillhub.cn 分页 API 导入：翻页拉 JSON → 按 downloads 质量门槛筛 → 字段直接映射入 components。

skillhub 是结构化 skill 数据库(7.7万条),字段规整、自带中文描述,几乎不用 LLM。
质量优先：只收 downloads >= 门槛的，不无脑全搬。

用法(容器内):
    python -m app.import_skillhub [--min-downloads 100] [--max-pages 60] [--page-size 100] [--dry-run]
"""
import argparse
import re
import sys
import time
import urllib.request

from psycopg.types.json import Jsonb
from . import db, retrieval

API = "https://api.skillhub.cn/api/skills"

CAT_TO_SCENARIOS = {
    "ai-agent": ["agent"], "coding": ["coding"], "productivity": ["efficiency"],
    "writing": ["writing"], "data": ["data-analysis"], "design": ["graphic-design"],
    "devops": ["devtools"], "research": ["research"], "marketing": ["marketing"],
}


def fetch_page(page, ps):
    url = f"{API}?page={page}&pageSize={ps}"
    for _ in range(3):
        try:
            with urllib.request.urlopen(url, timeout=25) as r:
                import json
                return json.load(r)["data"]["skills"]
        except Exception:
            time.sleep(2)
    return []


def slugify(s):
    s = re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")
    return s[:40] or "skill"


def to_doc(s, used_ids):
    name = (s.get("name") or "").strip()
    desc = (s.get("description_zh") or s.get("description") or "").strip()
    if len(name) < 2 or len(desc) < 10:
        return None
    cid, base, n = f"skill-{slugify(s.get('slug') or name)}", f"skill-{slugify(s.get('slug') or name)}", 2
    while cid in used_ids:
        cid = f"{base}-{n}"; n += 1
    used_ids.add(cid)
    cat = s.get("category") or ""
    scen = CAT_TO_SCENARIOS.get(cat, ["other"])
    tags = [str(t)[:20] for t in (s.get("tags") or [])][:6]
    home = s.get("homepage") or s.get("upstream_url") or ""
    return {
        "id": cid, "type": "skill", "kind": "tool", "name": name[:80],
        "description_zh": desc[:300],
        "host_tools": ["claude-code"], "scenarios": scen, "tags": tags,
        "difficulty": "beginner",
        "install": {"method": "manual", "notes_zh": f"详见 {home}" if home else "详见 skillhub.cn"},
        "config_required": (["API Key"] if (s.get("labels") or {}).get("requires_api_key") == "true" else []),
        "quality": {
            "verified": bool(s.get("verified")),
            "downloads": s.get("downloads", 0),
            "stars": s.get("stars", 0),
        },
        "source": {"url": home or f"https://skillhub.cn/skills/{s.get('slug','')}"},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--top", type=int, default=0, help="按score排序只取前N个(A方案:头部精华)")
    ap.add_argument("--min-downloads", type=int, default=100, help="下载量门槛")
    ap.add_argument("--max-pages", type=int, default=60)
    ap.add_argument("--page-size", type=int, default=100)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    db.pool.open()
    db.init_schema()
    used_ids = set()
    with db.pool.connection() as c:
        for (i,) in c.execute("SELECT id FROM components").fetchall():
            used_ids.add(i)

    kept, scanned = [], 0
    # --top 模式: 拉全部候选(API按score降序),取合格的前N个
    if args.top:
        all_skills = []
        for p in range(1, args.max_pages + 1):
            skills = fetch_page(p, args.page_size)
            if not skills:
                break
            all_skills.extend(skills)
            if len(all_skills) >= args.top * 2:  # 多拉一些防去重后不够
                break
        # 已按score排序,顺序取合格的
        for s in all_skills:
            doc = to_doc(s, used_ids)
            if doc:
                kept.append(doc)
            if len(kept) >= args.top:
                break
        scanned = len(all_skills)
        print(f"按score取前{args.top}: 拉{scanned}条 → 合格{len(kept)}条")
    else:
        for p in range(1, args.max_pages + 1):
            skills = fetch_page(p, args.page_size)
            if not skills:
                break
            scanned += len(skills)
            for s in skills:
                if s.get("downloads", 0) < args.min_downloads:
                    continue
                doc = to_doc(s, used_ids)
                if doc:
                    kept.append(doc)
            if p % 10 == 0:
                print(f"  扫描 {scanned} 条, 过质量线 {len(kept)}", flush=True)
    print(f"扫描 {scanned} 条 → downloads≥{args.min_downloads} 且合格 {len(kept)} 条")

    if args.dry_run:
        for d in kept[:15]:
            print(f"  [{d['quality']['downloads']}下载] {d['name']} — {d['description_zh'][:40]}")
        print("(dry-run,未入库)")
        return
    if not kept:
        print("无合格数据")
        return

    # 向量化 + 入库(直接进 components 表 + Meili)
    texts = [f"{d['name']} {d['description_zh']} {' '.join(d['tags'])}" for d in kept]
    vecs = []
    for i in range(0, len(texts), 32):
        vecs.extend(retrieval.embed(texts[i:i+32]))
        if (i // 32) % 10 == 0:
            print(f"  向量化 {min(i+32,len(texts))}/{len(texts)}", flush=True)
    with db.pool.connection() as conn:
        for d, text, vec in zip(kept, texts, vecs):
            vec_str = "[" + ",".join(f"{x:.6f}" for x in vec) + "]"
            conn.execute(
                "INSERT INTO components (id, type, name, doc, search_text, embedding) "
                "VALUES (%s,%s,%s,%s,%s,%s::vector) ON CONFLICT (id) DO UPDATE SET "
                "doc=EXCLUDED.doc, search_text=EXCLUDED.search_text, embedding=EXCLUDED.embedding",
                (d["id"], "skill", d["name"], Jsonb(d), text, vec_str))
    # 同步 Meili
    idx = retrieval.meili.index("components")
    flat = [{"id": d["id"], "type": "skill", "name": d["name"],
             "description": d["description_zh"], "tags": d["tags"],
             "scenarios": d["scenarios"], "host_tools": d["host_tools"],
             "difficulty": d["difficulty"]} for d in kept]
    task = idx.add_documents(flat, primary_key="id")
    retrieval.meili.wait_for_task(task.task_uid)
    print(f"✅ 入库 {len(kept)} 条 skill 到 components 表")


if __name__ == "__main__":
    main()
