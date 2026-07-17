"""从 CocoLoop hub 导入 skills（详情页驱动）：
遍历 /skills/<id> 详情页 → 取中文显示名 + 下载按钮链接 + 作者 → 下载 zip 读 SKILL.md
→ understand()（grounded）→ 一条 skill 组件。source 用详情页 URL；安装说明用 CocoLoop 统一方式。

用法（howai-api 容器内）:
    python -m app.ingest_cocoloop --enumerate --max-id 7700 --persist [--workers 5]
    python -m app.ingest_cocoloop --ids 1430,100 --dry-run     # 指定 ID 试跑
"""
import argparse
import concurrent.futures as cf
import io
import re
import urllib.request
import zipfile

from . import ingest, ingest_repo as ir

HUB = "https://hub.cocoloop.cn"

INSTALL_NOTE = ("CocoLoop / OpenClaw 生态 skill。安装：把 skill 包放入你的 Agent"
                "（Claude Code 等）的 skills 目录，或用 CocoLoop 客户端一键安装。"
                "下载：{dl}")


def _get(url, timeout=40):
    req = urllib.request.Request(url, headers={"User-Agent": "gd4ai-bot/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def parse_detail(sid, html):
    """从详情页 HTML 抽取 {id, name, author, dl_url, source_url}；非 skill 页返回 None。"""
    dl = re.search(r'href="(https://dl\.cocoloop\.cn/bss/skills/[^"]+\.zip)"', html)
    if not dl:
        return None
    name = ""
    tm = re.search(r"<title>([^<]*)</title>", html)
    if tm:
        t = tm.group(1)
        if " - " in t:
            t = t.split(" - ", 1)[1]
        name = t.split("|")[0].strip()
    if not name:                       # 兜底：JSON name 字段
        nm = re.search(r'"name":"([^"]{3,60})"', html)
        name = nm.group(1) if nm else f"skill {sid}"
    am = re.search(r'"(?:owner|author|creator)":"([^"]{2,40})"', html)
    return {"id": sid, "name": name[:80],
            "author": (am.group(1) if am else ""),
            "dl_url": dl.group(1), "source_url": f"{HUB}/skills/{sid}"}


def enumerate_details(max_id, workers=8):
    """遍历 /skills/<id> 收集详情记录（ID 稀疏，404/非skill页跳过）。"""
    def one(i):
        try:
            html = _get(f"{HUB}/skills/{i}", timeout=20).decode("utf-8", "ignore")
        except Exception:
            return None
        return parse_detail(i, html)
    out = []
    with cf.ThreadPoolExecutor(workers) as ex:
        for i, rec in zip(range(1, max_id + 1), ex.map(one, range(1, max_id + 1))):
            if rec:
                out.append(rec)
            if i % 500 == 0:
                print(f"  枚举 {i}/{max_id}，已得 {len(out)} 个 skill", flush=True)
    return out


def fetch_md(dl_url):
    """下载 skill zip → SKILL.md（无则 README.md）。"""
    try:
        z = zipfile.ZipFile(io.BytesIO(_get(dl_url)))
    except Exception:
        return ""
    names = z.namelist()
    n = (next((n for n in names if n.lower().endswith("skill.md")), None)
         or next((n for n in names if n.lower().endswith("readme.md")), None))
    return z.read(n).decode("utf-8", "ignore") if n else ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids", default="", help="逗号分隔的详情页 ID；试跑用")
    ap.add_argument("--enumerate", action="store_true")
    ap.add_argument("--max-id", type=int, default=7700)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--persist", action="store_true")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--chunk", type=int, default=40)
    args = ap.parse_args()

    from . import db
    if db.pool.closed:
        db.pool.open()
    existing, used = ir.load_state()

    if args.ids.strip():
        recs = []
        for sid in [x.strip() for x in args.ids.split(",") if x.strip()]:
            try:
                r = parse_detail(sid, _get(f"{HUB}/skills/{sid}").decode("utf-8", "ignore"))
                if r:
                    recs.append(r)
            except Exception:
                pass
    else:
        print(f"枚举 /skills/1..{args.max_id} …", flush=True)
        recs = enumerate_details(args.max_id, max(args.workers, 8))
    # 断点续跑：详情页 URL 已在库则跳过
    fresh = [r for r in recs if r["source_url"].lower() not in existing]
    if args.limit:
        fresh = fresh[: args.limit]
    print(f"枚举得 {len(recs)}，去掉已在库后待处理 {len(fresh)}", flush=True)

    def process(rec):
        md = fetch_md(rec["dl_url"])
        if len(md) < 40:
            return (rec, "SKILL.md太薄")
        doc, why = ir.make_component({
            "name": rec["name"], "description_zh": ir.norm_ws(md)[:200] or rec["name"],
            "url": rec["source_url"], "type": "skill", "kind": "tool",
            "scenarios": [], "ai_related": True, "keep": True,
        }, used, existing, source_text=md)   # understand() 基于 SKILL.md 出描述/第一步
        if doc:
            doc.setdefault("install", {})["notes_zh"] = INSTALL_NOTE.format(dl=rec["dl_url"])
            if rec["author"]:
                doc.setdefault("quality", {})["author"] = rec["author"]
            return (rec, doc)
        return (rec, why)

    buf, skipped = [], {}
    got = saved = 0
    with cf.ThreadPoolExecutor(args.workers) as ex:
        for rec, res in ex.map(process, fresh):
            if isinstance(res, dict):
                buf.append(res); got += 1
                if args.dry_run:
                    print(f"  ✓ {res['name']} — {res['description_zh'][:46]}", flush=True)
            else:
                skipped[res] = skipped.get(res, 0) + 1
            if args.persist and not args.dry_run and len(buf) >= args.chunk:
                saved += ingest.persist_docs(buf); buf = []
                print(f"  已落库 {saved}（产出 {got}，跳过 {skipped}）", flush=True)
    print(f"产出 {got} 条，跳过 {skipped}", flush=True)
    if args.dry_run or not args.persist:
        print("(未落库)")
        return
    if buf:
        saved += ingest.persist_docs(buf)
    ingest.flush_reco_cache()
    print(f"✅ 落库 {saved} 条（增量，PG+Meili+向量）", flush=True)


if __name__ == "__main__":
    main()
