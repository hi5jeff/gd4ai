#!/usr/bin/env python3
"""批量翻译 data/ 下所有组件和方案包的中文字段 → 英文。约束：只改 en 字段，不碰中文原文。"""
import concurrent.futures as cf
import json
import os
import pathlib
import sys
import urllib.request

import yaml

ROOT = pathlib.Path(__file__).parent.parent / "data"
MDBOX_KEY = os.environ["MDBOX_API_KEY"]
MDBOX_URL = os.environ.get("MDBOX_BASE_URL", "https://api.mdbox.ai")

def llm_json(prompt):
    body = json.dumps({"model": "deepseek-v4-flash", "messages": [{"role": "user", "content": prompt}],
                       "max_tokens": 3000, "temperature": 0.1}).encode()
    req = urllib.request.Request(f"{MDBOX_URL}/v1/chat/completions", data=body,
        headers={"Authorization": f"Bearer {MDBOX_KEY}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        content = json.load(r)["choices"][0]["message"]["content"].strip()
    if content.startswith("```"):
        content = content.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return json.loads(content)


def translate_component(fpath):
    doc = yaml.safe_load(fpath.read_text())
    # 跳过已有英文的
    if doc.get("description_en") and len(doc["description_en"]) > 10:
        return doc["id"], "skip"

    i = doc.get("install", {}) or {}
    u = doc.get("usage", {})
    q = doc.get("quality", {}) or {}

    prompt = f"""Translate these Chinese fields to English (natural, idiomatic). Output strict JSON, no markdown.
{{
  "name_en": "{doc.get('name','')}",
  "description_en": "{doc.get('description_zh','')}",
  "notes_en": "{i.get('notes_zh','') or ''}",
  "first_prompt_en": "{u.get('first_prompt_zh','') or ''}",
  "verify_en": "{u.get('verify_zh','') or ''}",
  "security_notes_en": "{q.get('security_notes_zh','') or ''}",
  "maintenance_note_en": "{q.get('maintenance_note_zh','') or ''}"
}}
Keep empty strings as empty strings. Keep technical terms (npx, MCP, API, repo names, code) unchanged."""
    try:
        tr = llm_json(prompt)
    except Exception as e:
        return doc["id"], f"LLM:{str(e)[:60]}"

    # 只写回非空值
    if tr.get("name_en"):
        doc["name_en"] = tr["name_en"]
    if tr.get("description_en"):
        doc["description_en"] = tr["description_en"]
    if tr.get("notes_en"):
        (doc.setdefault("install", {}) or doc["install"])["notes_en"] = tr["notes_en"]
    if tr.get("first_prompt_en"):
        (doc.setdefault("usage", {}) or doc["usage"])["first_prompt_en"] = tr["first_prompt_en"]
    if tr.get("verify_en"):
        (doc.setdefault("usage", {}) or doc["usage"])["verify_en"] = tr["verify_en"]
    if tr.get("security_notes_en"):
        (doc.setdefault("quality", {}) or doc["quality"])["security_notes_en"] = tr["security_notes_en"]
    if tr.get("maintenance_note_en"):
        (doc.setdefault("quality", {}) or doc["quality"])["maintenance_note_en"] = tr["maintenance_note_en"]

    fpath.write_text(yaml.dump(doc, allow_unicode=True, sort_keys=False, width=120))
    return doc["id"], "done"


def translate_playbook(fpath):
    doc = yaml.safe_load(fpath.read_text())
    if doc.get("title_en") and doc.get("summary_en"):
        return doc["id"], "skip"

    prompt = f"""Translate these Chinese fields to English. Output strict JSON, no markdown.
{{
  "title_en": "{doc.get('title_zh','')}",
  "summary_en": "{doc.get('summary_zh','')}",
  "first_prompt_en": "{doc.get('first_prompt_zh','') or ''}",
  "steps": {json.dumps([{"title_zh": s.get("title_zh",""), "detail_zh": s.get("detail_zh","")} for s in doc.get("steps", [])])},
  "components": {json.dumps([{"role_zh": c.get("role_zh","")} for c in doc.get("components", [])])},
  "pitfalls": {json.dumps(doc.get("pitfalls_zh", []) or [])}
}}
Output: {{"title_en":"...","summary_en":"...","first_prompt_en":"...",
  "steps":[{{"title_en":"...","detail_en":"..."}},...],
  "components":[{{"role_en":"..."}},...],
  "pitfalls":["..."]}}
Keep empty strings empty. Keep technical terms unchanged."""
    try:
        tr = llm_json(prompt)
    except Exception as e:
        return doc["id"], f"LLM:{str(e)[:60]}"

    if tr.get("title_en"):
        doc["title_en"] = tr["title_en"]
    if tr.get("summary_en"):
        doc["summary_en"] = tr["summary_en"]
    if tr.get("first_prompt_en"):
        doc["first_prompt_en"] = tr["first_prompt_en"]
    for i, s in enumerate(tr.get("steps", []) or []):
        if i < len(doc["steps"]):
            if s.get("title_en"):
                doc["steps"][i]["title_en"] = s["title_en"]
            if s.get("detail_en"):
                doc["steps"][i]["detail_en"] = s["detail_en"]
    for i, c in enumerate(tr.get("components", []) or []):
        if i < len(doc["components"]) and c.get("role_en"):
            doc["components"][i]["role_en"] = c["role_en"]
    for i, p in enumerate(tr.get("pitfalls", []) or []):
        if i < len(doc.get("pitfalls_zh", []) or []) and p:
            doc.setdefault("pitfalls_en", [None] * len(doc["pitfalls_zh"]))[i] = p
    if doc.get("pitfalls_en"):
        doc["pitfalls_en"] = [p for p in doc["pitfalls_en"] if p]

    fpath.write_text(yaml.dump(doc, allow_unicode=True, sort_keys=False, width=120))
    return doc["id"], "done"


def main():
    comps = sorted((ROOT / "components").rglob("*.yaml"))
    pbs = sorted((ROOT / "playbooks").rglob("*.yaml"))
    print(f"组件 {len(comps)} | 方案包 {len(pbs)}")

    stats = {}
    with cf.ThreadPoolExecutor(8) as ex:
        futs = [(ex.submit(translate_component, f), f.stem) for f in comps]
        futs += [(ex.submit(translate_playbook, f), f.stem) for f in pbs]
        for i, (fut, stem) in enumerate(futs, 1):
            _, why = fut.result()
            stats[why] = stats.get(why, 0) + 1
            if i % 20 == 0:
                print(f"  进度 {i}/{len(futs)}")

    print(f"\n完成:")
    for k, v in sorted(stats.items()):
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()