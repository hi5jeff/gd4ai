import json
from psycopg_pool import ConnectionPool
from . import config

pool = ConnectionPool(config.PG_DSN, min_size=1, max_size=8, open=False)

SCHEMA = """
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE IF NOT EXISTS components (
    id TEXT PRIMARY KEY,
    type TEXT NOT NULL,
    name TEXT NOT NULL,
    doc JSONB NOT NULL,
    search_text TEXT NOT NULL,
    embedding vector(1024)
);
CREATE TABLE IF NOT EXISTS playbooks (
    id TEXT PRIMARY KEY,
    scenario TEXT NOT NULL,
    doc JSONB NOT NULL,
    search_text TEXT NOT NULL,
    embedding vector(1024)
);
-- 细粒度提示词表：可到千万级，独立于 components，用 HNSW 索引扛检索
CREATE TABLE IF NOT EXISTS prompts (
    id BIGSERIAL PRIMARY KEY,
    source_id TEXT NOT NULL,           -- 来源组件 id（关联 components 里的"提示词库"条目）
    ext_id TEXT,                       -- 源仓库内的原始 id，用于去重/更新
    title_zh TEXT NOT NULL,            -- LLM 生成的中文短标题
    summary_zh TEXT,                   -- 一句话说明能生成什么效果
    content TEXT NOT NULL,             -- 可直接复制的完整提示词原文
    scene_tags TEXT[] DEFAULT '{}',    -- 细分场景标签（香水广告/美妆/数码…）
    style_tags TEXT[] DEFAULT '{}',    -- 风格标签
    tools TEXT[] DEFAULT '{}',         -- 适用工具（midjourney/sd/即梦…）
    lang TEXT DEFAULT 'en',            -- content 语言
    quality REAL DEFAULT 0,            -- LLM 质量分 0-1
    search_text TEXT NOT NULL,         -- 用于向量化的检索文本
    embedding vector(1024),
    created_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE (source_id, ext_id)
);
CREATE INDEX IF NOT EXISTS prompts_hnsw ON prompts USING hnsw (embedding vector_cosine_ops);
CREATE INDEX IF NOT EXISTS prompts_scene ON prompts USING gin (scene_tags);

CREATE TABLE IF NOT EXISTS gap_log (
    id BIGSERIAL PRIMARY KEY,
    query TEXT NOT NULL,
    reason TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);
CREATE TABLE IF NOT EXISTS query_log (
    id BIGSERIAL PRIMARY KEY,
    query TEXT NOT NULL,
    intent TEXT,
    latency_ms INT,
    result_ids JSONB,
    created_at TIMESTAMPTZ DEFAULT now()
);
CREATE TABLE IF NOT EXISTS submissions (
    id BIGSERIAL PRIMARY KEY,
    url TEXT NOT NULL,
    note TEXT,
    status TEXT NOT NULL DEFAULT 'pending',  -- pending / imported / rejected / failed
    result TEXT,
    count INT DEFAULT 0,
    source TEXT DEFAULT 'user',
    created_at TIMESTAMPTZ DEFAULT now(),
    processed_at TIMESTAMPTZ
);
CREATE INDEX IF NOT EXISTS submissions_status ON submissions (status, created_at DESC);
"""


def init_schema():
    with pool.connection() as conn:
        conn.execute(SCHEMA)


def get_doc(table: str, item_id: str):
    assert table in ("components", "playbooks")
    with pool.connection() as conn:
        row = conn.execute(f"SELECT doc FROM {table} WHERE id = %s", (item_id,)).fetchone()
    return row[0] if row else None


def get_docs(table: str, ids: list[str]) -> dict:
    if not ids:
        return {}
    assert table in ("components", "playbooks")
    with pool.connection() as conn:
        rows = conn.execute(f"SELECT id, doc FROM {table} WHERE id = ANY(%s)", (ids,)).fetchall()
    return {r[0]: r[1] for r in rows}


def log_gap(query: str, reason: str):
    with pool.connection() as conn:
        conn.execute("INSERT INTO gap_log (query, reason) VALUES (%s, %s)", (query, reason))


def log_query(query: str, intent: str, latency_ms: int, result_ids: list[str]):
    with pool.connection() as conn:
        conn.execute(
            "INSERT INTO query_log (query, intent, latency_ms, result_ids) VALUES (%s, %s, %s, %s)",
            (query, intent, latency_ms, json.dumps(result_ids)),
        )


def add_submission(url: str, note: str = "", source: str = "user") -> dict:
    """登记一条用户提交的 URL。同一 URL 若已存在未处理记录则复用，不重复登记。"""
    with pool.connection() as conn:
        row = conn.execute(
            "SELECT id, status FROM submissions WHERE url = %s AND status = 'pending' LIMIT 1",
            (url,),
        ).fetchone()
        if row:
            return {"id": row[0], "status": row[1], "duplicate": True}
        row = conn.execute(
            "INSERT INTO submissions (url, note, source) VALUES (%s, %s, %s) RETURNING id",
            (url, note, source),
        ).fetchone()
        return {"id": row[0], "status": "pending", "duplicate": False}


def list_submissions(status: str | None = None, limit: int = 200) -> list[dict]:
    q = ("SELECT id, url, note, status, result, count, source, created_at, processed_at "
         "FROM submissions")
    params = []
    if status:
        q += " WHERE status = %s"
        params.append(status)
    q += " ORDER BY created_at DESC LIMIT %s"
    params.append(limit)
    cols = ["id", "url", "note", "status", "result", "count", "source",
            "created_at", "processed_at"]
    with pool.connection() as conn:
        rows = conn.execute(q, params).fetchall()
    out = []
    for r in rows:
        d = dict(zip(cols, r))
        for k in ("created_at", "processed_at"):
            d[k] = d[k].isoformat() if d[k] else None
        out.append(d)
    return out


def get_submission(sub_id: int) -> dict | None:
    with pool.connection() as conn:
        row = conn.execute("SELECT id, url, status FROM submissions WHERE id = %s",
                           (sub_id,)).fetchone()
    return {"id": row[0], "url": row[1], "status": row[2]} if row else None


def update_submission(sub_id: int, status: str, result: str = "", count: int = 0):
    with pool.connection() as conn:
        conn.execute(
            "UPDATE submissions SET status=%s, result=%s, count=%s, processed_at=now() "
            "WHERE id=%s",
            (status, result[:500], count, sub_id),
        )


def component_url_exists(url: str) -> str | None:
    """URL 是否已在组件库；命中则返回该组件名，否则 None。用于给重复提交清晰反馈。"""
    core = url.strip().lower().rstrip("/")
    for pre in ("https://", "http://", "www."):
        if core.startswith(pre):
            core = core[len(pre):]
    core = core.removesuffix(".git")
    if not core:
        return None
    with pool.connection() as conn:
        row = conn.execute(
            "SELECT name FROM components WHERE lower(doc->'source'->>'repo') LIKE %s "
            "OR lower(doc->'source'->>'url') LIKE %s LIMIT 1",
            (f"%{core}%", f"%{core}%"),
        ).fetchone()
    return row[0] if row else None


def submission_stats() -> dict:
    with pool.connection() as conn:
        rows = conn.execute(
            "SELECT status, count(*) FROM submissions GROUP BY status").fetchall()
    return {r[0]: r[1] for r in rows}
