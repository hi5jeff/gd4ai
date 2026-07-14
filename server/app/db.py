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
