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
2. 选出所有真正相关的组件（通常 2-6 个），无关的不选；相关的宁全勿漏
3. **凡是专为用户所述任务打造的对口组件（名称/说明与需求高度吻合，如"网站UI设计"对应的UI/UX设计skill），必须选入，且排在前面；不要因为已经选了通用工具就把它省略**
4. 组playbook工作流时，也要把上述对口的专用组件一并选进 selected，不能只给通用件（如只给"设计师+Figma+图像生成"却漏掉专门的UI设计skill）
5. 如果所有候选都与需求无关，返回 {{"no_match": true}}
6. intent_type: 用户要单个工具/提示词="single"，要完成一件完整的事="playbook"

**所有面向用户的文本字段（answer / reason / name / desc）必须用「用户提问所用的语言」输出**（中文问→中文，英文问→英文，日文问→日文，任意语言同理）。库里数据是中文的，你负责翻译成用户语言。界面语言仅供参考，以实际提问语言为准。
- name: 组件的名称（专有名词/产品名保留原文，其余按用户语言）
- desc: 用一句话把该组件的作用讲清楚，用用户语言

输出严格 JSON（无 markdown 代码块）：
{{"intent_type": "single|playbook", "answer": "一句话方案概述", "selected": [{{"id": "...", "name": "...", "desc": "...", "reason": "为什么需要它(一句话)"}}], "playbook_id": "匹配的方案包id或null", "no_match": false}}"""

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


def _component_card(doc: dict, reason: str = "", name: str = "", desc: str = "") -> dict:
    """展示卡片。name/desc 若由 LLM 按用户语言给出则覆盖库里中文原文（数据只存单语）。"""
    q = doc.get("quality", {})
    return {
        "id": doc["id"], "type": doc["type"], "kind": doc.get("kind", "tool"),
        "name": name or doc["name"],
        "description": desc or doc["description_zh"],
        "reason": reason,
        "difficulty": doc["difficulty"], "host_tools": doc.get("host_tools", []),
        "install": doc.get("install", {}), "config_required": doc.get("config_required", []),
        "usage": doc.get("usage", {}),
        "stars": q.get("stars"), "last_commit": q.get("last_commit"),
        "verified": q.get("verified", False),
        "security_notes": q.get("security_notes_zh"),
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
    return {"intent": "no_result", "answer": msg, "components": nearest, "playbook": None}


def recommend(query: str, lang: str = "zh") -> dict:
    t0 = time.time()
    query = query.strip()[:500]

    cached = redis.get(_cache_key(query, lang))
    if cached:
        out = json.loads(cached)
        out["cached"] = True
        return out

    comp_hits = retrieval.hybrid(query, "components", limit=18)
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
                "components": nearest, "playbook": None}

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
            "title": pb["title_zh"],
            "summary": pb.get("summary_zh", ""),
            "steps": pb["steps"],
            "first_prompt": pb.get("first_prompt_zh"),
            "pitfalls": pb.get("pitfalls_zh", []),
            "components": [
                {**_component_card(ref_docs[c["ref"]], c["role_zh"]),
                 "optional": c.get("optional", False)}
                for c in pb["components"] if c["ref"] in ref_docs
            ],
        }

    out = {
        "intent": result.get("intent_type", "single"),
        "answer": result.get("answer", ""),  # LLM 已按用户语言输出
        "components": [_component_card(comp_docs[s["id"]], s.get("reason", ""),
                                       s.get("name", ""), s.get("desc", ""))
                       for s in selected],
        "playbook": playbook,
        "prompts": [_prompt_card(p) for p in strong_prompts],
        "latency_ms": int((time.time() - t0) * 1000),
    }
    redis.setex(_cache_key(query, lang), config.CACHE_TTL, json.dumps(out, ensure_ascii=False))
    db.log_query(query, out["intent"], out["latency_ms"],
                 [s["id"] for s in selected] + ([pb_id] if pb_id else []))
    return out