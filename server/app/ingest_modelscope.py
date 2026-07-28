"""从 ModelScope MCP 广场导入（走官方内部 API，非爬网页）。

接口（抓包得到）:
    PUT https://www.modelscope.cn/api/v1/dolphin/mcpServers
    body {"PageSize":30,"PageNumber":1,"Query":"","Criterion":[]}
每条自带中文名/中文摘要/中文README/分类/调用量/Star/ServerConfig（可直接复制的 MCP 配置）。
因此无需再过 LLM 抽描述：中文字段直接用；ServerConfig 作为「怎么用」。

用法（容器内）:
    python -m app.ingest_modelscope --pages 5 --persist          # 前 5 页(每页30)
    python -m app.ingest_modelscope --min-calls 10000 --pages 20 --persist
"""
import argparse
import json
import urllib.request

from . import ingest, ingest_repo as ir

API = "https://www.modelscope.cn/api/v1/dolphin/mcpServers"
SITE = "https://www.modelscope.cn/mcp/servers/"


def fetch_page(page, size=30, query=""):
    body = json.dumps({"PageSize": size, "PageNumber": page,
                       "Query": query, "Criterion": []}).encode()
    req = urllib.request.Request(API, data=body, method="PUT", headers={
        "Content-Type": "application/json", "User-Agent": "Mozilla/5.0 (gd4ai-bot)"})
    with urllib.request.urlopen(req, timeout=40) as r:
        d = json.load(r)
    ms = (d.get("Data") or {}).get("McpServer") or {}
    return ms.get("McpServers") or [], ms.get("TotalCount") or 0


def to_doc(it, used, existing):
    """API 条目 → 组件 doc。中文字段齐全，无需 LLM 抽描述。"""
    path = it.get("Path") or ""
    name = (it.get("ChineseName") or it.get("Name") or path.split("/")[-1] or "").strip()
    desc = (it.get("AbstractCN") or it.get("TranslatedAbstract")
            or it.get("Abstract") or "").strip()
    if len(name) < 2 or len(desc) < 10:
        return None, "名称/描述不足"
    url = SITE + path if path else (it.get("FromSiteUrl") or "")
    doc, why = ir.make_component({
        "name": name, "description_zh": desc, "url": url,
        "type": "mcp", "kind": "tool",
        "scenarios": [], "ai_related": True, "keep": True,
    }, used, existing)
    if not doc:
        return None, why
    # 怎么用：官方给的 MCP 客户端配置，可直接复制
    cfg = it.get("ServerConfig") or it.get("StreamableHTTPServerConfig") or it.get("SSEServerConfig")
    if cfg:
        cfg_txt = cfg if isinstance(cfg, str) else json.dumps(cfg, ensure_ascii=False, indent=2)
        doc.setdefault("install", {})["notes_zh"] = (
            "在 MCP 客户端（Claude Desktop / Cursor 等）的配置文件中加入以下配置：")
        doc["install"]["command"] = cfg_txt[:1500]
    tags = [str(t)[:20] for t in (it.get("Category") or []) + (it.get("Tags") or [])][:6]
    if tags:
        doc["tags"] = tags
    q = doc.setdefault("quality", {})
    if it.get("Stars"):
        q["stars"] = it["Stars"]
    if it.get("CallVolume"):
        q["call_volume"] = it["CallVolume"]
    if it.get("FromSiteUrl"):
        doc["source"]["origin"] = it["FromSiteUrl"]
    return doc, "ok"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", type=int, default=5, help="抓多少页（每页 PageSize 条）")
    ap.add_argument("--size", type=int, default=30)
    ap.add_argument("--query", default="")
    ap.add_argument("--min-calls", type=int, default=0, help="调用量低于此值跳过（质量门槛）")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--persist", action="store_true")
    ap.add_argument("--chunk", type=int, default=60)
    args = ap.parse_args()

    from . import db
    if db.pool.closed:
        db.pool.open()
    existing, used = ir.load_state()

    buf, skipped = [], {}
    got = saved = 0
    for page in range(1, args.pages + 1):
        try:
            items, total = fetch_page(page, args.size, args.query)
        except Exception as e:
            print(f"  第{page}页失败: {str(e)[:80]}", flush=True)
            continue
        if page == 1:
            print(f"广场总量 {total}，本次抓 {args.pages} 页 × {args.size}", flush=True)
        if not items:
            break
        for it in items:
            if args.min_calls and (it.get("CallVolume") or 0) < args.min_calls:
                skipped["调用量不足"] = skipped.get("调用量不足", 0) + 1
                continue
            doc, why = to_doc(it, used, existing)
            if doc:
                buf.append(doc); got += 1
                if args.dry_run and got <= 12:
                    print(f"  ✓ {doc['name']} — {doc['description_zh'][:44]}", flush=True)
            else:
                skipped[why] = skipped.get(why, 0) + 1
        if args.persist and not args.dry_run and len(buf) >= args.chunk:
            saved += ingest.persist_docs(buf); buf = []
            print(f"  已落库 {saved}（第{page}页，产出 {got}，跳过 {skipped}）", flush=True)

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
