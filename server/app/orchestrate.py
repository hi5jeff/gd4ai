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

**answer 和 reason 字段必须用「用户提问所用的语言」回答**（用户用中文问就用中文答，用英文问就用英文答，用日文问就用日文答，以此类推）。界面语言仅作参考，以用户实际提问语言为准。

输出严格 JSON（无 markdown 代码块）：
{{"intent_type": "single|playbook", "answer": "一句话方案概述", "selected": [{{"id": "...", "reason": "为什么需要它(一句话)"}}], "playbook_id": "匹配的方案包id或null", "no_match": false}}"""

NO_RESULT = {
    "zh": "库里暂时没有和这个需求精确匹配、经过验证的方案。我们已记录你的需求，会优先补充。",
    "en": "We don't have a verified solution for this exact need yet. Your request has been logged and will be prioritized for curation.",
}
NEAR_MATCH = {
    "zh": "下面是最接近的内容（非精确匹配，仅供参考）：",
    "en": "Here are the closest matches (not exact, for reference):",
}
FALLBACK = {
    "zh": "AI 编排暂时不可用，以下是检索到的最相关内容：",
    "en": "AI orchestration is temporarily unavailable. Here are the closest matches from our library:",
}


def _cache_key(query: str, lang: str) -> str:
    return "rec:" + hashlib.sha1(f"{query}|{lang}".strip().lower().encode()).hexdigest()


def _component_card(doc: dict, reason: str = "", reason_en: str = "") -> dict:
    q = doc.get("quality", {})
    i = doc.get("install", {})
    u = doc.get("usage", {})
    return {
        "id": doc["id"], "type": doc["type"],
        "name": doc["name"], "name_en": doc.get("name_en"),
        "description": doc["description_zh"], "description_en": doc.get("description_en"),
        "reason": reason, "reason_en": reason_en,
        "difficulty": doc["difficulty"], "host_tools": doc.get("host_tools", []),
        "install": i, "config_required": doc.get("config_required", []),
        "usage": doc.get("usage", {}),
        "stars": q.get("stars"), "last_commit": q.get("last_commit"),
        "verified": q.get("verified", False),
        "security_notes": q.get("security_notes_zh"),
        "security_notes_en": q.get("security_notes_en"),
        "source": doc.get("source", {}),
    }


def _prompt_card(p: dict) -> dict:
    return {
        "id": f"prompt-{p['id']}", "type": "prompt-item",
        "title_zh": p["title_zh"], "summary_zh": p.get("summary_zh", ""),
        "content": p["content"], "scene_tags": p.get("scene_tags", []),
        "style_tags": p.get("style_tags", []), "source_id": p.get("source_id"),
        "score": round(p.get("score", 0), 3),
    }


PROMPTS_ANSWER = {
    "zh": "为你从提示词库里找到这些最匹配的，可直接复制使用：",
    "en": "Here are the best-matching prompts from our library, ready to copy:",
}


def _prompts_answer(query: str, prompts: list[dict], lang: str, t0: float) -> dict:
    out = {
        "intent": "prompts",
        "answer": PROMPTS_ANSWER.get(lang, PROMPTS_ANSWER["zh"]),
        "answer_en": PROMPTS_ANSWER["en"],
        "components": [], "playbook": None,
        "prompts": [_prompt_card(p) for p in prompts],
        "latency_ms": int((time.time() - t0) * 1000),
    }
    db.log_query(query, "prompts", out["latency_ms"], [p["id"] for p in out["prompts"]])
    return out


def _no_result(query: str, reason: str, nearest: list[dict], lang: str) -> dict:
    db.log_gap(query, reason)
    msg = NO_RESULT.get(lang, NO_RESULT["zh"])
    if nearest:
        msg += NEAR_MATCH.get(lang, NEAR_MATCH["zh"])
    return {"intent": "no_result", "answer": msg, "answer_en": NO_RESULT["en"] + (NEAR_MATCH["en"] if nearest else ""),
            "components": nearest, "playbook": None}


def recommend(query: str, lang: str = "zh") -> dict:
    t0 = time.time()
    query = query.strip()[:500]

    cached = redis.get(_cache_key(query, lang))
    if cached:
        out = json.loads(cached)
        out["cached"] = True
        return out

    comp_hits = retrieval.hybrid(query, "components", limit=14)
    pb_hits = retrieval.hybrid(query, "playbooks", limit=3)
    # 细粒度提示词检索：命中高分说明用户要的是"具体提示词"而非"提示词来源"
    prompt_hits = retrieval.search_prompts(query, limit=6, min_quality=0.55)
    strong_prompts = [p for p in prompt_hits if p["score"] >= 0.6]

    if not comp_hits and not strong_prompts:
        return _no_result(query, "检索零命中", [], lang)

    # 只命中提示词、没命中组件 → 直接返回具体提示词（不必走组件编排）
    if strong_prompts and not comp_hits:
        return _prompts_answer(query, strong_prompts, lang, t0)

    comp_docs = db.get_docs("components", [h["id"] for h in comp_hits])
    pb_docs = db.get_docs("playbooks", [h["id"] for h in pb_hits])

    cand_lines = [
        f'- id={d["id"]} 类型={d["type"]} 名称={d["name"]} 难度={d["difficulty"]} 说明={d["description_zh"][:80]}'
        for d in (comp_docs[h["id"]] for h in comp_hits if h["id"] in comp_docs)
    ]
    pb_lines = [
        f'- id={d["id"]} 标题={d["title_zh"]} 概述={d.get("summary_zh","")[:80]}'
        for d in (pb_docs[h["id"]] for h in pb_hits if h["id"] in pb_docs)
    ] or ["(无)"]

    lang_name = "中文" if lang == "zh" else "English"
    try:
        result = llm.chat_json(PROMPT.format(
            query=query, candidates="\n".join(cand_lines), playbooks="\n".join(pb_lines),
            lang_name=lang_name))
    except RuntimeError:
        nearest = [_component_card(comp_docs[h["id"]]) for h in comp_hits[:5] if h["id"] in comp_docs]
        return {"intent": "search_only", "answer": FALLBACK.get(lang, FALLBACK["zh"]),
                "answer_en": FALLBACK["en"], "components": nearest, "playbook": None}

    # ---- 闭世界校验：剔除一切库外引用 ----
    valid_ids = set(comp_docs)
    selected = [s for s in result.get("selected", []) if s.get("id") in valid_ids]
    pb_id = result.get("playbook_id")
    if pb_id not in pb_docs:
        pb_id = None

    if result.get("no_match") or (not selected and not pb_id):
        nearest = [_component_card(comp_docs[h["id"]]) for h in comp_hits[:3] if h["id"] in comp_docs]
        return _no_result(query, "LLM判定候选不相关", nearest, lang)

    playbook = None
    if pb_id:
        pb = pb_docs[pb_id]
        refs = [c["ref"] for c in pb["components"]]
        ref_docs = db.get_docs("components", refs)
        playbook = {
            "id": pb["id"],
            "title": pb["title_zh"], "title_en": pb.get("title_en"),
            "summary": pb.get("summary_zh", ""), "summary_en": pb.get("summary_en"),
            "steps": pb["steps"],
            "first_prompt": pb.get("first_prompt_zh"),
            "first_prompt_en": pb.get("first_prompt_en"),
            "pitfalls": pb.get("pitfalls_zh", []),
            "pitfalls_en": pb.get("pitfalls_en", []),
            "components": [
                {**_component_card(ref_docs[c["ref"]], c["role_zh"], c.get("role_en", "")),
                 "optional": c.get("optional", False)}
                for c in pb["components"] if c["ref"] in ref_docs
            ],
        }

    out = {
        "intent": result.get("intent_type", "single"),
        "answer": result.get("answer", ""),
        "answer_en": result.get("answer", ""),  # LLM outputs in requested lang
        "components": [_component_card(comp_docs[s["id"]], s.get("reason", "")) for s in selected],
        "playbook": playbook,
        "prompts": [_prompt_card(p) for p in strong_prompts],
        "latency_ms": int((time.time() - t0) * 1000),
    }
    redis.setex(_cache_key(query, lang), config.CACHE_TTL, json.dumps(out, ensure_ascii=False))
    db.log_query(query, out["intent"], out["latency_ms"],
                 [s["id"] for s in selected] + ([pb_id] if pb_id else []))
    return out