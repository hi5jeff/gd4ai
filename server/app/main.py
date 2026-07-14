from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel, Field
from . import db, orchestrate, retrieval


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
