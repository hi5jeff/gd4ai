#!/usr/bin/env python3
"""半自动采集管线：GitHub topic 高星扫描 → deepseek-v4-flash 抽取 → schema 校验 → 落盘 data/components/

防幻觉硬约束：
1. 安装命令必须逐字出现在 README 原文中（空白归一后子串匹配），否则降级 method=manual 丢弃命令
2. type/scenarios/host_tools/difficulty 全部从受控枚举选择，越界即丢弃该条
3. 已收录仓库（含手工策展 36 条）自动跳过，不覆盖人工数据
"""
import concurrent.futures as cf
import json
import os
import pathlib
import re
import sys
import time
import urllib.request

import jsonschema
import yaml

ROOT = pathlib.Path(__file__).parent.parent
DATA = ROOT / "data" / "components"
SCHEMA = json.loads((ROOT / "data" / "schema" / "component.schema.json").read_text())

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
MDBOX_KEY = os.environ["MDBOX_API_KEY"]
MDBOX_URL = os.environ.get("MDBOX_BASE_URL", "https://api.mdbox.ai")

# (topic, 星数下限, 最多收录数)
SOURCES = [
    ("mcp-server", 300, 120),
    ("claude-code", 200, 60),
]

TYPES = ["mcp", "skill", "plugin", "role", "prompt", "workflow", "tool"]
SCENARIOS = ["web-dev", "ecommerce", "web-testing", "scraping", "automation", "data-analysis",
             "database", "devtools", "coding", "mcp-dev", "planning", "research", "open-source",
             "image-gen", "video-gen", "portrait", "graphic-design", "ui-design", "branding",
             "interior-design", "3d-design", "game-dev", "game-animation", "pixel-art",
             "office", "writing", "marketing", "token-saving", "efficiency", "security",
             "finance", "communication", "search", "memory", "monitoring", "media", "other"]
HOSTS = ["claude-code", "codex", "cursor", "windsurf", "any-mcp-client", "web", "desktop", "any"]

PROMPT = """你是数据抽取器。根据 GitHub 仓库信息生成组件条目，输出严格 JSON（无 markdown）。

仓库: {full_name} | ⭐{stars} | topics: {topics}
官方描述: {desc}
README 节选:
---
{readme}
---

字段要求:
- is_component: 这是不是一个用户可以安装/使用的组件或工具? awesome列表/教程/文章/纯资料集合 = false
- type: 只能选 {types}（mcp server=mcp; Claude Code的skill=skill; 子代理/persona或其合集=role; 命令/模板/插件合集=plugin; 提示词库=prompt; 独立软件/网站=tool）
- name: 简短名称(保留英文原名)
- description_zh: 60-120字中文说明，讲清"是什么+能干什么+适合谁"
- scenarios: 1-4个，只能选 {scenarios}
- host_tools: 1-3个，只能选 {hosts}
- tags: 3-6个中文或英文短标签
- difficulty: beginner|intermediate|advanced（零配置可用=beginner，要API key/配置=intermediate，要编译/复杂环境=advanced）
- install_command: 从README里【逐字复制】一条最主要的安装命令（优先 claude mcp add / npx / uvx / pip / npm 单行命令）；README里没有明确命令就填 null，禁止自己编写
- install_notes_zh: 一句话安装要点(可含前置条件)
- config_required: 需要用户准备的东西列表(API key等)，没有则 []
- first_prompt_zh: 装好后用户可以说的第一句话(中文，一句)

输出: {{"is_component": bool, "type": "...", "name": "...", "description_zh": "...", "scenarios": [...], "host_tools": [...], "tags": [...], "difficulty": "...", "install_command": "...|null", "install_notes_zh": "...", "config_required": [...], "first_prompt_zh": "..."}}"""


def http_json(url, headers=None, data=None, timeout=60):
    req = urllib.request.Request(url, data=data, headers=headers or {})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def gh(path):
    return http_json(f"https://api.github.com{path}",
                     {"Authorization": f"Bearer {GITHUB_TOKEN}", "Accept": "application/vnd.github+json"})


def gh_readme(full_name):
    req = urllib.request.Request(f"https://api.github.com/repos/{full_name}/readme",
        headers={"Authorization": f"Bearer {GITHUB_TOKEN}", "Accept": "application/vnd.github.raw"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read().decode("utf-8", "ignore")
    except Exception:
        return ""


def llm(prompt):
    body = json.dumps({"model": "deepseek-v4-flash", "messages": [{"role": "user", "content": prompt}],
                       "max_tokens": 3000, "temperature": 0.1}).encode()
    resp = http_json(f"{MDBOX_URL}/v1/chat/completions", data=body, timeout=120,
                     headers={"Authorization": f"Bearer {MDBOX_KEY}", "Content-Type": "application/json"})
    content = resp["choices"][0]["message"]["content"].strip()
    if content.startswith("```"):
        content = content.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return json.loads(content)


def norm_ws(s):
    return re.sub(r"\s+", " ", s or "").strip()


def existing_repos_and_ids():
    repos, ids = set(), set()
    for f in DATA.rglob("*.yaml"):
        doc = yaml.safe_load(f.read_text())
        ids.add(doc["id"])
        repo = (doc.get("source") or {}).get("repo", "")
        if repo:
            repos.add(repo.lower().rstrip("/"))
    return repos, ids


def search_candidates():
    seen_repos, _ = existing_repos_and_ids()
    out, seen_names = [], set()
    for topic, min_stars, max_take in SOURCES:
        taken = 0
        for page in (1, 2):
            res = gh(f"/search/repositories?q=topic:{topic}+stars:>={min_stars}&sort=stars&order=desc&per_page=100&page={page}")
            for r in res.get("items", []):
                fn = r["full_name"]
                low = r["html_url"].lower().rstrip("/")
                if fn in seen_names or low in seen_repos:
                    continue
                if re.search(r"awesome|curated|-list$", r["name"], re.I):
                    continue
                seen_names.add(fn)
                out.append({"full_name": fn, "stars": r["stargazers_count"],
                            "desc": (r.get("description") or "")[:300],
                            "topics": r.get("topics", [])[:8],
                            "html_url": r["html_url"], "pushed": r["pushed_at"][:10]})
                taken += 1
                if taken >= max_take:
                    break
            if taken >= max_take:
                break
        print(f"topic:{topic} 候选 {taken} 个")
    return out


def slugify(name):
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return s[:40] or "item"


def process(cand, used_ids):
    readme = gh_readme(cand["full_name"])
    if len(readme) < 200:
        return None, "README太短"
    try:
        ex = llm(PROMPT.format(types=TYPES, scenarios=SCENARIOS, hosts=HOSTS,
                               readme=norm_ws(readme)[:3500], **cand))
    except Exception as e:
        return None, f"LLM失败:{str(e)[:60]}"

    if not ex.get("is_component"):
        return None, "非组件(列表/教程)"
    if ex.get("type") not in TYPES:
        return None, f"type越界:{ex.get('type')}"
    scen = [s for s in ex.get("scenarios", []) if s in SCENARIOS][:4]
    hosts = [h for h in ex.get("host_tools", []) if h in HOSTS][:3]
    if not scen or not hosts or ex.get("difficulty") not in ("beginner", "intermediate", "advanced"):
        return None, "枚举字段不合法"
    if not (ex.get("description_zh") or "").strip() or len(ex["description_zh"]) < 10:
        return None, "描述缺失"

    # 防幻觉：命令必须逐字出现在 README（空白归一）
    cmd = ex.get("install_command")
    method = "manual"
    if cmd and norm_ws(cmd) in norm_ws(readme):
        c = cmd.strip()
        method = ("claude-mcp-add" if c.startswith("claude mcp add") else
                  "npx" if c.startswith("npx") else "uvx" if c.startswith("uvx") else
                  "pip" if c.startswith(("pip ", "pip3 ")) else
                  "npm" if c.startswith("npm") else "git-clone" if c.startswith("git clone") else "manual")
        if method == "manual":
            cmd = None
    else:
        cmd = None

    base = f"{ex['type']}-{slugify(cand['full_name'].split('/')[-1])}"
    cid, n = base, 2
    while cid in used_ids:
        cid, n = f"{base}-{n}", n + 1

    doc = {
        "id": cid, "type": ex["type"], "name": str(ex.get("name") or cand["full_name"])[:80],
        "description_zh": ex["description_zh"][:300],
        "host_tools": hosts, "scenarios": scen,
        "tags": [str(t)[:20] for t in ex.get("tags", [])][:6],
        "difficulty": ex["difficulty"],
        "install": {k: v for k, v in {
            "method": method, "command": cmd,
            "notes_zh": (ex.get("install_notes_zh") or "").strip()[:200] or None}.items() if v},
        "config_required": [str(c)[:60] for c in ex.get("config_required", [])][:5],
        "quality": {"stars": cand["stars"], "last_commit": cand["pushed"], "verified": False},
        "source": {"repo": cand["html_url"]},
    }
    fp = (ex.get("first_prompt_zh") or "").strip()
    if fp:
        doc["usage"] = {"first_prompt_zh": fp[:300]}
    try:
        jsonschema.validate(doc, SCHEMA)
    except Exception as e:
        return None, f"schema:{str(e).splitlines()[0][:60]}"
    return doc, "ok"


def main():
    cands = search_candidates()
    print(f"待处理 {len(cands)} 个（去重后）")
    _, used_ids = existing_repos_and_ids()
    stats, written = {}, 0
    lock_ids = set(used_ids)

    with cf.ThreadPoolExecutor(8) as ex:
        futs = {ex.submit(process, c, lock_ids): c for c in cands}
        for i, fut in enumerate(cf.as_completed(futs), 1):
            doc, why = fut.result()
            stats[why if not doc else "ok"] = stats.get(why if not doc else "ok", 0) + 1
            if doc:
                lock_ids.add(doc["id"])
                out = DATA / doc["type"] / f"{doc['id']}.yaml"
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_text(yaml.dump(doc, allow_unicode=True, sort_keys=False, width=120))
                written += 1
            if i % 20 == 0:
                print(f"进度 {i}/{len(cands)} 已落盘 {written}")

    print(f"\n完成: 新增 {written} 条")
    for k, v in sorted(stats.items(), key=lambda x: -x[1]):
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
