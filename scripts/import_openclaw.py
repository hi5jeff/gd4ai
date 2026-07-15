"""openclaw 插件导入: 175个插件名+URL → 批量LLM生成描述/分类 → 入 components 表。"""
import json, os, re, sys, urllib.request
from psycopg.types.json import Jsonb
sys.path.insert(0, "/app")
from app import db, retrieval, config, llm
db.pool.open()

# 读链接列表(name从URL slug推)
plugins = []
for line in open("/data/openclaw_plugins.txt"):
    url = line.strip()
    if not url: continue
    slug = url.rstrip("/").split("/")[-1]
    plugins.append({"slug": slug, "url": url})
print(f"读入 {len(plugins)} 个插件")

SCEN = ["communication","devtools","automation","search","coding","agent","media","llm-serving","other"]
PROMPT = """这些是 OpenClaw(开源AI agent框架)的插件,根据插件slug判断每个的用途,输出JSON数组。
插件列表:
{items}
对每个输出: {{"slug":"原样","name":"友好名称","description_zh":"一句话中文说明用途(30-60字)","type":"plugin|mcp","scenarios":["从这选1-2个: {scen}"],"keep":true/false(明显无意义的图标/占位则false)}}
只输出JSON数组,无markdown。"""

# 分批(每20个)过LLM
docs = []
used = set()
with db.pool.connection() as c:
    for (i,) in c.execute("SELECT id FROM components").fetchall(): used.add(i)

for i in range(0, len(plugins), 20):
    batch = plugins[i:i+20]
    items = "\n".join(f'{p["slug"]}' for p in batch)
    try:
        res = llm.chat_json(PROMPT.format(items=items, scen=SCEN), model=config.MODEL_BATCH, max_tokens=3000, retries=2)
    except Exception as e:
        print(f"批次{i}失败:{str(e)[:50]}"); continue
    if isinstance(res, dict): res = res.get("results") or []
    bymap = {p["slug"]: p for p in batch}
    for r in res:
        sl = r.get("slug")
        if sl not in bymap or not r.get("keep"): continue
        name = (r.get("name") or sl).strip()
        desc = (r.get("description_zh") or "").strip()
        if len(desc) < 8: continue
        cid, base, n = f"plugin-{re.sub(r'[^a-z0-9]+','-',sl.lower()).strip('-')}", None, 2
        base = cid
        while cid in used: cid = f"{base}-{n}"; n+=1
        used.add(cid)
        scen = [s for s in r.get("scenarios",[]) if s in SCEN][:2] or ["other"]
        docs.append({"id":cid,"type":r.get("type") if r.get("type") in ("plugin","mcp") else "plugin",
            "kind":"tool","name":name[:80],"description_zh":desc[:300],"host_tools":["any-mcp-client"],
            "scenarios":scen,"tags":["openclaw"],"difficulty":"intermediate",
            "install":{"method":"manual","notes_zh":f"详见 {bymap[sl]['url']}"},
            "quality":{"verified":False},"source":{"url":bymap[sl]["url"]}})
    print(f"  {i+len(batch)}/{len(plugins)} 处理, 累计 {len(docs)}", flush=True)

print(f"生成 {len(docs)} 条")
if "--dry-run" in sys.argv:
    for d in docs[:12]: print(f"  {d['name']}: {d['description_zh'][:40]}")
    sys.exit()
# 向量化入库
texts = [f"{d['name']} {d['description_zh']} {' '.join(d['tags'])}" for d in docs]
vecs = []
for i in range(0,len(texts),32): vecs.extend(retrieval.embed(texts[i:i+32]))
with db.pool.connection() as conn:
    for d,t,v in zip(docs,texts,vecs):
        vs="["+",".join(f"{x:.6f}" for x in v)+"]"
        conn.execute("INSERT INTO components (id,type,name,doc,search_text,embedding) VALUES (%s,%s,%s,%s,%s,%s::vector) ON CONFLICT (id) DO UPDATE SET doc=EXCLUDED.doc,search_text=EXCLUDED.search_text,embedding=EXCLUDED.embedding",
            (d["id"],d["type"],d["name"],Jsonb(d),t,vs))
idx=retrieval.meili.index("components")
task=idx.add_documents([{"id":d["id"],"type":d["type"],"name":d["name"],"description":d["description_zh"],"tags":d["tags"],"scenarios":d["scenarios"],"host_tools":d["host_tools"],"difficulty":d["difficulty"]} for d in docs],primary_key="id")
retrieval.meili.wait_for_task(task.task_uid)
print(f"✅ 入库 {len(docs)} 条 openclaw 插件")
