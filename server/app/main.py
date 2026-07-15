from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Header
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel, Field
from . import db, orchestrate, retrieval, config, ingest, ingest_repo


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.pool.open()
    db.init_schema()
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
            db.update_submission(sub_id, "failed", "未抽取到有效组件（可能不含AI相关内容）", 0)
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
        # 同步执行(过 LLM，可能数十秒)；导入结果写回记录
        await run_in_threadpool(_do_ingest, sub_id, sub["url"])
        result = await run_in_threadpool(db.get_submission, sub_id)
        return {"ok": True, "status": result["status"]}
    raise HTTPException(400, "action 须为 ingest 或 reject")


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
