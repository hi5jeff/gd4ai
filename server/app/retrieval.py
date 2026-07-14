import httpx
import meilisearch
from . import config, db

meili = meilisearch.Client(config.MEILI_URL, config.MEILI_KEY)


def embed(texts: list[str]) -> list[list[float]]:
    out = []
    for i in range(0, len(texts), 8):
        resp = httpx.post(f"{config.EMBED_URL}/embed", json={"inputs": texts[i : i + 8]}, timeout=60)
        resp.raise_for_status()
        out.extend(resp.json())
    return out


def keyword_search(index: str, q: str, limit: int = 20, type_filter: str | None = None) -> list[dict]:
    opts = {"limit": limit}
    if type_filter:
        opts["filter"] = f"type = {type_filter}"
    try:
        return meili.index(index).search(q, opts)["hits"]
    except Exception:
        return []


def vector_search(table: str, vec: list[float], limit: int = 20) -> list[tuple[str, float]]:
    assert table in ("components", "playbooks")
    vec_str = "[" + ",".join(f"{x:.6f}" for x in vec) + "]"
    with db.pool.connection() as conn:
        rows = conn.execute(
            f"SELECT id, 1 - (embedding <=> %s::vector) AS score FROM {table} "
            f"ORDER BY embedding <=> %s::vector LIMIT %s",
            (vec_str, vec_str, limit),
        ).fetchall()
    return [(r[0], float(r[1])) for r in rows]


def hybrid(q: str, table: str = "components", limit: int = 12, type_filter: str | None = None) -> list[dict]:
    """关键词(Meili) + 向量(pgvector) RRF 融合。返回 [{id, rrf, kw_rank, vec_score}]"""
    kw_hits = keyword_search(table, q, 20, type_filter)
    vec_hits = vector_search(table, embed([q])[0], 20)

    scores: dict[str, dict] = {}
    for rank, h in enumerate(kw_hits):
        s = scores.setdefault(h["id"], {"id": h["id"], "rrf": 0.0, "kw_rank": None, "vec_score": None})
        s["rrf"] += 1 / (60 + rank)
        s["kw_rank"] = rank
    for rank, (cid, score) in enumerate(vec_hits):
        s = scores.setdefault(cid, {"id": cid, "rrf": 0.0, "kw_rank": None, "vec_score": None})
        s["rrf"] += 1 / (60 + rank)
        s["vec_score"] = score
    ranked = sorted(scores.values(), key=lambda x: -x["rrf"])[:limit]
    return ranked
