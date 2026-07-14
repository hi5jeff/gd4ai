"""推荐编排：检索候选 → LLM 闭世界选择 → 校验 → 拼装方案包。核心约束：LLM 只能引用检索返回的 id。"""
import hashlib
import json
import time
import redis as redis_lib
from . import config, db, llm, retrieval

redis = redis_lib.from_url(config.REDIS_URL, decode_responses=True)

PROMPT = """你是 gd4.ai 的 AI 工具推荐编排器。用户需求："{query}"

候选组件（你只能从这里选，禁止编造任何库外内容）：
{candidates}

候选方案包（现成的组合方案，优先推荐匹配的）：
{playbooks}

规则：
1. selected 里的 id 必须来自候选组件列表；playbook_id 必须来自候选方案包列表或为 null
2. 只选真正相关的，宁少勿滥（通常 1-5 个）；组件描述与需求无关就不要选
3. 如果所有候选都与需求无关，返回 {{"no_match": true}}
4. intent_type: 用户要单个工具/提示词="single"，要完成一件完整的事="playbook"

输出严格 JSON（无 markdown 代码块）：
{{"intent_type": "single|playbook", "answer_zh": "给用户的一句话方案概述", "selected": [{{"id": "...", "reason_zh": "为什么需要它(一句话)"}}], "playbook_id": "匹配的方案包id或null", "no_match": false}}"""


def _cache_key(query: str) -> str:
    return "rec:" + hashlib.sha1(query.strip().lower().encode()).hexdigest()


def _component_card(doc: dict, reason: str = "") -> dict:
    q = doc.get("quality", {})
    return {
        "id": doc["id"], "type": doc["type"], "name": doc["name"],
        "description": doc["description_zh"], "reason": reason,
        "difficulty": doc["difficulty"], "host_tools": doc.get("host_tools", []),
        "install": doc.get("install", {}), "config_required": doc.get("config_required", []),
        "usage": doc.get("usage", {}),
        "stars": q.get("stars"), "last_commit": q.get("last_commit"),
        "verified": q.get("verified", False),
        "security_notes": q.get("security_notes_zh"),
        "source": doc.get("source", {}),
    }


def _no_result(query: str, reason: str, nearest: list[dict]) -> dict:
    db.log_gap(query, reason)
    return {
        "intent": "no_result",
        "answer": "库里暂时没有和这个需求精确匹配、经过验证的方案。我们已记录你的需求，会优先补充。" +
                  ("下面是最接近的内容（非精确匹配，仅供参考）：" if nearest else ""),
        "components": nearest, "playbook": None,
    }


def recommend(query: str) -> dict:
    t0 = time.time()
    query = query.strip()[:500]

    cached = redis.get(_cache_key(query))
    if cached:
        out = json.loads(cached)
        out["cached"] = True
        return out

    comp_hits = retrieval.hybrid(query, "components", limit=14)
    pb_hits = retrieval.hybrid(query, "playbooks", limit=3)

    if not comp_hits:
        return _no_result(query, "检索零命中", [])

    comp_docs = db.get_docs("components", [h["id"] for h in comp_hits])
    pb_docs = db.get_docs("playbooks", [h["id"] for h in pb_hits])

    cand_lines = [
        f'- id={d["id"]} 类型={d["type"]} 名称={d["name"]} 难度={d["difficulty"]} 说明={d["description_zh"][:80]}'
        for d in (comp_docs[h["id"]] for h in comp_hits if h["id"] in comp_docs)
    ]
    pb_lines = [
        f'- id={d["id"]} 标题={d["title_zh"]} 概述={d["summary_zh"][:80]}'
        for d in (pb_docs[h["id"]] for h in pb_hits if h["id"] in pb_docs)
    ] or ["(无)"]

    try:
        result = llm.chat_json(PROMPT.format(
            query=query, candidates="\n".join(cand_lines), playbooks="\n".join(pb_lines)))
    except RuntimeError:
        # LLM 挂了降级为纯检索结果
        nearest = [_component_card(comp_docs[h["id"]]) for h in comp_hits[:5] if h["id"] in comp_docs]
        return {"intent": "search_only", "answer": "AI 编排暂时不可用，以下是检索到的最相关内容：",
                "components": nearest, "playbook": None}

    # ---- 闭世界校验：剔除一切库外引用 ----
    valid_ids = set(comp_docs)
    selected = [s for s in result.get("selected", []) if s.get("id") in valid_ids]
    pb_id = result.get("playbook_id")
    if pb_id not in pb_docs:
        pb_id = None

    if result.get("no_match") or (not selected and not pb_id):
        nearest = [_component_card(comp_docs[h["id"]]) for h in comp_hits[:3] if h["id"] in comp_docs]
        return _no_result(query, "LLM判定候选不相关", nearest)

    playbook = None
    if pb_id:
        pb = pb_docs[pb_id]
        refs = [c["ref"] for c in pb["components"]]
        ref_docs = db.get_docs("components", refs)
        playbook = {
            "id": pb["id"], "title": pb["title_zh"], "summary": pb["summary_zh"],
            "steps": pb["steps"], "first_prompt": pb.get("first_prompt_zh"),
            "pitfalls": pb.get("pitfalls_zh", []),
            "components": [
                {**_component_card(ref_docs[c["ref"]]), "reason": c["role_zh"],
                 "optional": c.get("optional", False)}
                for c in pb["components"] if c["ref"] in ref_docs
            ],
        }

    out = {
        "intent": result.get("intent_type", "single"),
        "answer": result.get("answer_zh", ""),
        "components": [_component_card(comp_docs[s["id"]], s.get("reason_zh", "")) for s in selected],
        "playbook": playbook,
        "latency_ms": int((time.time() - t0) * 1000),
    }
    redis.setex(_cache_key(query), config.CACHE_TTL, json.dumps(out, ensure_ascii=False))
    db.log_query(query, out["intent"], out["latency_ms"],
                 [s["id"] for s in selected] + ([pb_id] if pb_id else []))
    return out
