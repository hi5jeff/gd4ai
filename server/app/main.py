import json
import re
import threading
import time
import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Header
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from . import db, orchestrate, retrieval, config, ingest, ingest_repo


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.pool.open()
    db.init_schema()
    # 每次启动(即每次部署)清推荐缓存，避免旧编排/prompt 的陈旧结果赖在 Redis 里
    try:
        ingest.flush_reco_cache()
    except Exception:
        pass
    yield
    db.pool.close()


app = FastAPI(title="gd4.ai API", lifespan=lifespan)


class RecommendReq(BaseModel):
    query: str = Field(min_length=2, max_length=500)


@app.post("/api/recommend")
async def recommend(req: RecommendReq, lang: str = "zh"):
    return await run_in_threadpool(orchestrate.recommend, req.query, lang)


@app.get("/api/search")
async def search(q: str, type: str | None = None, limit: int = 10):
    hits = await run_in_threadpool(retrieval.hybrid, q, "components", min(limit, 30), type)
    docs = db.get_docs("components", [h["id"] for h in hits])
    return {"results": [orchestrate._component_card(docs[h["id"]]) for h in hits if h["id"] in docs]}


@app.get("/api/components/{item_id}")
async def component(item_id: str):
    doc = db.get_doc("components", item_id)
    if not doc:
        raise HTTPException(404)
    return doc


@app.get("/api/playbooks/{item_id}")
async def playbook(item_id: str):
    doc = db.get_doc("playbooks", item_id)
    if not doc:
        raise HTTPException(404)
    return doc


class SubmitReq(BaseModel):
    url: str = Field(min_length=5, max_length=500)
    note: str = Field(default="", max_length=500)


@app.post("/api/submit")
async def submit(req: SubmitReq):
    url = req.url.strip()
    if not (url.startswith("http://") or url.startswith("https://")):
        raise HTTPException(400, "请提交 http(s):// 开头的网址")
    res = await run_in_threadpool(db.add_submission, url, req.note.strip())
    return {"ok": True, **res}


def _require_admin(x_admin_token: str | None):
    if not config.ADMIN_TOKEN or x_admin_token != config.ADMIN_TOKEN:
        raise HTTPException(401, "无权限")


@app.get("/api/admin/submissions")
async def admin_list(status: str | None = None,
                     x_admin_token: str | None = Header(default=None)):
    _require_admin(x_admin_token)
    rows = await run_in_threadpool(db.list_submissions, status)
    stats = await run_in_threadpool(db.submission_stats)
    return {"stats": stats, "submissions": rows}


class ActionReq(BaseModel):
    action: str  # ingest / reject


def _do_ingest(sub_id: int, url: str):
    try:
        # dry_run=True 只是跳过写 YAML(容器内 /app/data 是只读挂载)，docs 照常产出；
        # 随后 persist_docs 直接落 PG+Meili+向量，才是真正入库。
        docs, _ = ingest_repo.ingest_any(url, dry_run=True, log=lambda *a: None)
        n = ingest.persist_docs(docs)
        if n:
            db.update_submission(sub_id, "imported", f"入库 {n} 条组件", n)
        else:
            dup = db.component_url_exists(url)
            if dup:
                db.update_submission(sub_id, "imported", f"已在库中：{dup}（无需重复）", 0)
            else:
                db.update_submission(sub_id, "failed", "未抽取到有效组件（可能不含AI相关内容/无法访问）", 0)
    except Exception as e:
        db.update_submission(sub_id, "failed", f"导入出错: {str(e)[:200]}", 0)


@app.post("/api/admin/submissions/{sub_id}/action")
async def admin_action(sub_id: int, req: ActionReq,
                       x_admin_token: str | None = Header(default=None)):
    _require_admin(x_admin_token)
    sub = await run_in_threadpool(db.get_submission, sub_id)
    if not sub:
        raise HTTPException(404, "记录不存在")
    if req.action == "reject":
        await run_in_threadpool(db.update_submission, sub_id, "rejected", "已拒绝", 0)
        return {"ok": True, "status": "rejected"}
    if req.action == "ingest":
        # 导入前先判重：URL 已在库则直接跳过，不浪费 LLM
        dup = await run_in_threadpool(db.component_url_exists, sub["url"])
        if dup:
            await run_in_threadpool(db.update_submission, sub_id, "imported",
                                    f"已在库中：{dup}（跳过，未重复导入）", 0)
            return {"ok": True, "status": "imported", "duplicate": True}
        # 异步：立刻标记「导入中」并返回，后台线程过 LLM 真入库，完成后自动改状态
        await run_in_threadpool(db.update_submission, sub_id, "importing", "导入中…", 0)
        threading.Thread(target=_do_ingest, args=(sub_id, sub["url"]), daemon=True).start()
        return {"ok": True, "status": "importing"}
    raise HTTPException(400, "action 须为 ingest 或 reject")


def _stats_overview():
    """库存概览：总数 + 按类型分组 + 提示词数。Redis 缓存 1 小时，每小时最多查一次库。"""
    key = "stats:overview"
    try:
        cached = orchestrate.redis.get(key)
        if cached:
            return json.loads(cached)
    except Exception:
        pass
    with db.pool.connection() as conn:
        rows = conn.execute(
            "SELECT doc->>'type', count(*) FROM components GROUP BY 1").fetchall()
        prompts = conn.execute("SELECT count(*) FROM prompts").fetchone()[0]
    by_type = {r[0]: r[1] for r in rows if r[0]}
    out = {"total": sum(by_type.values()), "by_type": by_type,
           "prompts": prompts, "updated_at": int(time.time())}
    try:
        orchestrate.redis.setex(key, 3600, json.dumps(out))
    except Exception:
        pass
    return out


@app.get("/api/stats")
async def stats():
    return await run_in_threadpool(_stats_overview)


# ---- OpenAI 兼容 API：带 key 即可像调 OpenAI 一样调 gd4.ai 推荐 ----
API_MODEL = "gd4-recommend"


class ChatMessage(BaseModel):
    role: str = "user"
    content: object = ""


class ChatReq(BaseModel):
    model: str = API_MODEL
    messages: list[ChatMessage] = []
    stream: bool = False


def _check_api_key(authorization: str | None):
    if not config.API_KEYS:
        raise HTTPException(503, "API 未启用")
    key = (authorization or "").removeprefix("Bearer ").strip()
    if key not in config.API_KEYS:
        raise HTTPException(401, "无效的 API key")


def _last_user_query(messages):
    for m in reversed(messages):
        if m.role == "user":
            c = m.content
            if isinstance(c, list):   # 兼容 OpenAI 多模态 content 数组
                c = " ".join(p.get("text", "") for p in c if isinstance(p, dict))
            return str(c or "").strip()
    return ""


def _render_markdown(r, lang):
    zh = lang == "zh"
    out = [r.get("answer", "")]

    def comp(c):
        s = [f"### {c.get('name','')}  ·  {c.get('type','')}"]
        if c.get("reason"):
            s.append(f"> {c['reason']}")
        if c.get("description"):
            s.append(c["description"])
        inst = c.get("install") or {}
        if inst.get("notes_zh"):
            s.append(("**用法：**" if zh else "**How to use:** ") + inst["notes_zh"])
        if inst.get("command"):
            s.append("```\n" + inst["command"] + "\n```")
        u = c.get("usage") or {}
        if u.get("first_prompt_zh"):
            s.append(("**第一步：**" if zh else "**First step:**") + "\n```\n" + u["first_prompt_zh"] + "\n```")
        if c.get("config_required"):
            s.append(("**需要准备：**" if zh else "**Prerequisites:** ") + ", ".join(c["config_required"]))
        link = (c.get("source") or {}).get("repo") or (c.get("source") or {}).get("url")
        if link:
            s.append(("来源：" if zh else "Source: ") + link)
        return "\n".join(s)

    pb = r.get("playbook")
    if pb:
        out.append(("\n## 方案：" if zh else "\n## Plan: ") + pb.get("title", ""))
        if pb.get("summary"):
            out.append(pb["summary"])
        if pb.get("components"):
            out.append("\n## 需要的组件" if zh else "\n## Components")
            out += [comp(c) for c in pb["components"]]
        if pb.get("steps"):
            out.append("\n## 操作步骤" if zh else "\n## Steps")
            for i, st in enumerate(pb["steps"], 1):
                out.append(f"{i}. **{st.get('title_zh','')}** — {st.get('detail_zh','')}")
        if pb.get("first_prompt"):
            out.append(("\n## 起手提示词\n" if zh else "\n## First prompt\n") + "```\n" + pb["first_prompt"] + "\n```")
    comps = r.get("components") or []
    if comps and not pb:
        out.append("\n## 推荐组件" if zh else "\n## Recommended")
        out += [comp(c) for c in comps]
    prompts = r.get("prompts") or []
    if prompts:
        out.append("\n## 提示词" if zh else "\n## Prompts")
        for p in prompts:
            out.append(f"### {p.get('title_zh','')}")
            if p.get("summary_zh"):
                out.append(p["summary_zh"])
            if p.get("content"):
                out.append("```\n" + p["content"] + "\n```")
    return "\n\n".join(x for x in out if x)


def _sse(cid, created, model, content):
    def chunk(delta, finish=None):
        obj = {"id": cid, "object": "chat.completion.chunk", "created": created, "model": model,
               "choices": [{"index": 0, "delta": delta, "finish_reason": finish}]}
        return f"data: {json.dumps(obj, ensure_ascii=False)}\n\n"
    yield chunk({"role": "assistant"})
    for i in range(0, len(content), 64):
        yield chunk({"content": content[i:i + 64]})
    yield chunk({}, "stop")
    yield "data: [DONE]\n\n"


@app.get("/v1/models")
async def list_models(authorization: str | None = Header(default=None)):
    _check_api_key(authorization)
    return {"object": "list", "data": [
        {"id": API_MODEL, "object": "model", "created": 0, "owned_by": "gd4.ai"}]}


@app.post("/v1/chat/completions")
async def chat_completions(req: ChatReq, authorization: str | None = Header(default=None)):
    _check_api_key(authorization)
    query = _last_user_query(req.messages)
    if len(query) < 2:
        raise HTTPException(400, "messages 中缺少有效的 user 内容")
    lang = "zh" if re.search(r"[一-鿿]", query) else "en"
    result = await run_in_threadpool(orchestrate.recommend, query, lang)
    content = _render_markdown(result, lang)
    cid = "chatcmpl-" + uuid.uuid4().hex[:24]
    created = int(time.time())
    if req.stream:
        return StreamingResponse(_sse(cid, created, req.model, content),
                                 media_type="text/event-stream")
    pt, ct = len(query), len(content)
    return {
        "id": cid, "object": "chat.completion", "created": created, "model": req.model,
        "choices": [{"index": 0, "message": {"role": "assistant", "content": content},
                     "finish_reason": "stop"}],
        "usage": {"prompt_tokens": pt, "completion_tokens": ct, "total_tokens": pt + ct},
    }


@app.get("/api/health")
async def health():
    status = {}
    try:
        with db.pool.connection() as conn:
            status["pg_components"] = conn.execute("SELECT count(*) FROM components").fetchone()[0]
    except Exception as e:
        status["pg_error"] = str(e)[:100]
    try:
        status["meili"] = retrieval.meili.health()["status"]
    except Exception as e:
        status["meili_error"] = str(e)[:100]
    try:
        status["redis"] = orchestrate.redis.ping()
    except Exception as e:
        status["redis_error"] = str(e)[:100]
    try:
        status["embedding_dim"] = len(retrieval.embed(["ping"])[0])
    except Exception as e:
        status["embedding_error"] = str(e)[:100]
    ok = all(k in status for k in ("pg_components", "meili", "redis", "embedding_dim"))
    return {"ok": ok, **status}
