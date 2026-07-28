"""从 ModelScope MCP 广场 / Skills 导入（纯 JS 站，需无头浏览器渲染）。

流程：webread 渲染列表页 → 收集 /mcp/servers/<owner>/<name> 详情链接 →
逐个渲染详情页取正文 → understand()（grounded）→ 一条 mcp 组件。

用法（howai-api 容器内需装 webread；否则在宿主跑 --dump 产出 JSON 再导）:
    python -m app.ingest_modelscope --dump-list > /tmp/urls.txt      # 仅列出详情URL
    python -m app.ingest_modelscope --from-json /tmp/pages.json --persist
"""
import argparse
import json
import re
import subprocess

from . import ingest, ingest_repo as ir

BASE = "https://www.modelscope.cn"
LIST_PAGES = ("/mcp", "/skills")


def render(url, timeout=90, html=False):
    """用 webread 渲染页面，返回可读文本（或 DOM）。失败返回空串。"""
    cmd = ["webread", url] + (["--html"] if html else [])
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=timeout, text=True)
        return r.stdout or ""
    except Exception:
        return ""


def list_detail_urls(list_paths=LIST_PAGES):
    """渲染列表页，抽取 MCP 详情链接（去重、保序）。"""
    seen, out = set(), []
    for p in list_paths:
        dom = render(BASE + p, html=True)
        for m in re.findall(r'/mcp/servers/([A-Za-z0-9@._-]+/[A-Za-z0-9@._-]+)', dom):
            u = f"{BASE}/mcp/servers/{m}"
            if u not in seen:
                seen.add(u)
                out.append(u)
    return out


NOISE = re.compile(r'^(Home|Models|Datasets|Studios|Docs|Community|Skills|MCP|Civision|'
                   r'login / register|Server Detail|Tool Testing|Discussions|'
                   r'Deployable|Original|Translated|Hosted)$', re.I)


def parse_detail(url, text):
    """从渲染文本里取 {name, body}。name 用页首标题，body 去掉导航噪音。"""
    lines = [l.strip() for l in text.splitlines()]
    name = ""
    m = re.match(r'^#\s+(.+?)\s*·', lines[0]) if lines else None
    if m:
        name = m.group(1).strip()
    if not name:
        name = url.rstrip("/").split("/")[-1]
    body = "\n".join(l for l in lines if l and not NOISE.match(l) and not l.startswith("<http"))
    return {"name": name[:80], "body": body, "url": url}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dump-list", action="store_true", help="只输出详情 URL 列表")
    ap.add_argument("--from-json", default="", help="外部渲染好的 [{url,name,body}] JSON")
    ap.add_argument("--urls", default="", help="逗号分隔的详情 URL")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--persist", action="store_true")
    ap.add_argument("--chunk", type=int, default=20)
    args = ap.parse_args()

    if args.dump_list:
        for u in list_detail_urls():
            print(u)
        return

    from . import db
    if db.pool.closed:
        db.pool.open()
    existing, used = ir.load_state()

    # 取页面数据：外部 JSON 优先（宿主渲染好），否则容器内自己渲染
    if args.from_json:
        pages = json.load(open(args.from_json))
    else:
        urls = [u.strip() for u in args.urls.split(",") if u.strip()] or list_detail_urls()
        urls = [u for u in urls if u.lower() not in existing]
        if args.limit:
            urls = urls[: args.limit]
        pages = [parse_detail(u, render(u)) for u in urls]

    pages = [p for p in pages if p.get("url", "").lower() not in existing]
    if args.limit:
        pages = pages[: args.limit]
    print(f"待处理 {len(pages)} 条", flush=True)

    buf, skipped = [], {}
    got = saved = 0
    for p in pages:
        body = p.get("body") or ""
        if len(body) < 120:
            skipped["正文太少"] = skipped.get("正文太少", 0) + 1
            continue
        doc, why = ir.make_component({
            "name": p.get("name") or p["url"].split("/")[-1],
            "description_zh": ir.norm_ws(body)[:200],
            "url": p["url"], "type": "mcp", "kind": "tool",
            "scenarios": [], "ai_related": True, "keep": True,
        }, used, existing, source_text=body)
        if doc:
            buf.append(doc); got += 1
            if args.dry_run:
                print(f"  ✓ {doc['name']} — {doc['description_zh'][:46]}", flush=True)
        else:
            skipped[why] = skipped.get(why, 0) + 1
        if args.persist and not args.dry_run and len(buf) >= args.chunk:
            saved += ingest.persist_docs(buf); buf = []
            print(f"  已落库 {saved}（产出 {got}）", flush=True)

    print(f"产出 {got}，跳过 {skipped}", flush=True)
    if args.dry_run or not args.persist:
        print("(未落库)")
        return
    if buf:
        saved += ingest.persist_docs(buf)
    ingest.flush_reco_cache()
    print(f"✅ 落库 {saved} 条", flush=True)


if __name__ == "__main__":
    main()
