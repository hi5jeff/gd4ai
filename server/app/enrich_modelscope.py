"""补全 ModelScope Skills 的「怎么用」：用 API 的 ReadMeContent 做 grounding 跑 understand()。

导入时为省成本只用了 API 的中文描述（准确但没有安装/上手步骤）。本脚本按 skill 路径
回查 API 拿完整 README → understand() → 更新 install/usage → 重新向量化增量入库。

用法（容器内）:
    python -m app.enrich_modelscope [--limit N] [--workers 4] [--chunk 40]
"""
import argparse
import concurrent.futures as cf
import json
import urllib.parse
import urllib.request

from . import db, ingest, ingest_repo as ir

README_API = "https://www.modelscope.cn/api/v1/rm/fc?Type=translate-readme"


def fetch_readme(url):
    """按详情页 URL(.../skills/<owner>/<name>) 取中文 README。失败返回空串。"""
    path = urllib.parse.urlparse(url).path
    parts = [p for p in path.split("/") if p]
    if len(parts) < 3 or parts[0] != "skills":
        return ""
    owner, name = parts[1], parts[2]
    body = json.dumps({"type": "skill", "owner": owner, "name": name,
                       "preferLanguage": "zh_CN"}).encode()
    req = urllib.request.Request(README_API, data=body, method="POST", headers={
        "Content-Type": "application/json", "User-Agent": "Mozilla/5.0 (gd4ai-bot)"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.load(r)
    except Exception:
        return ""
    return d.get("content") or ""


THIN = ("doc->'source'->>'url' LIKE '%modelscope.cn/skills%' "
        "AND (doc->'install'->>'notes_zh' = '详见来源链接' OR doc->'usage' IS NULL)")


def work(row):
    cid, doc = row
    url = (doc.get("source") or {}).get("url", "")
    md = fetch_readme(url)
    if len(md) < 150:
        return (cid, "无README")
    u = ir.understand(doc.get("name", ""), doc.get("type", "skill"), url, md)
    if not u:
        return (cid, "LLM空")
    ir.apply_understanding(doc, u)
    return (cid, doc)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--chunk", type=int, default=40)
    args = ap.parse_args()

    if db.pool.closed:
        db.pool.open()
    with db.pool.connection() as conn:
        q = f"SELECT id, doc FROM components WHERE {THIN} ORDER BY id"
        if args.limit:
            q += f" LIMIT {args.limit}"
        rows = conn.execute(q).fetchall()
    print(f"待补全 {len(rows)} 条", flush=True)

    buf, stats = [], {}
    done = saved = 0
    with cf.ThreadPoolExecutor(args.workers) as ex:
        for cid, res in ex.map(work, rows):
            done += 1
            if isinstance(res, dict):
                buf.append(res)
            else:
                stats[res] = stats.get(res, 0) + 1
            if len(buf) >= args.chunk:
                saved += ingest.persist_docs(buf); buf = []
                print(f"  已落库 {saved}（进度 {done}/{len(rows)}，跳过 {stats}）", flush=True)
    if buf:
        saved += ingest.persist_docs(buf)
    ingest.flush_reco_cache()
    print(f"✅ 补全 {saved} 条，跳过 {stats}", flush=True)


if __name__ == "__main__":
    main()
