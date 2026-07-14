"""通用 GitHub 仓库摄取器：LLM 勘探结构 → 分型处理 → AI相关严筛 → 去重入库。

一套逻辑吃任何结构的仓库，不为每个仓库手写解析器：
  ① 勘探(probe)：读根目录+README，LLM 判断结构类型 → 输出摄取方案
  ② 抽取(extract)：按类型切块 → LLM 逐块抽出结构化条目
  ③ 严筛：只留"可安装/可使用的 AI 相关工具/框架/skill/mcp"，论文/文章/教程跳过
  ④ 去重：按 repo/url 归一，跳过库里已有的
  ⑤ 落盘 data/components/ 供 validate + ingest

结构类型:
  single      根目录一个工具/mcp/skill → 1 条
  collection  子目录各含一个单元(如 skills/*) → 展开成 N 条
  json_lib    大 JSON 内容库(提示词等) → 走 import_prompts，本脚本只登记来源条目
  nav_list    markdown 导航/清单(AI-Compass/GitHubDaily) → 切块抽取里面每个资源

用法(容器内): python -m app.ingest_repo <owner/repo> [--dry-run] [--max-items N]
"""
import argparse
import concurrent.futures as cf
import json
import os
import pathlib
import re
import sys
import urllib.parse
import urllib.request

import yaml

from . import config, llm

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
DATA = pathlib.Path(config.DATA_DIR) / "components"

TYPES = ["mcp", "skill", "plugin", "role", "prompt", "workflow", "tool"]
SCENARIOS = ["web-dev", "ecommerce", "coding", "devtools", "data-analysis", "database",
             "automation", "scraping", "research", "agent", "rag", "llm-training",
             "llm-serving", "image-gen", "video-gen", "graphic-design", "game-dev",
             "office", "efficiency", "security", "finance", "nlp", "cv", "mcp-dev", "other"]
HOSTS = ["claude-code", "codex", "cursor", "windsurf", "any-mcp-client", "web", "desktop", "any"]


def gh_json(path):
    req = urllib.request.Request(f"https://api.github.com{path}",
        headers={"Authorization": f"Bearer {GITHUB_TOKEN}", "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def gh_raw(owner_repo, path):
    req = urllib.request.Request(
        f"https://api.github.com/repos/{owner_repo}/contents/{urllib.parse.quote(path)}",
        headers={"Authorization": f"Bearer {GITHUB_TOKEN}", "Accept": "application/vnd.github.raw"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read().decode("utf-8", "ignore")
    except Exception:
        return ""


# ---------------- ① 勘探 ----------------
PROBE_PROMPT = """你在为一个"AI工具生态推荐系统"判断一个 GitHub 仓库该怎么导入。

仓库: {repo} (⭐{stars})
官方描述: {desc}
根目录内容:
{tree}
README 节选:
{readme}

判断这个仓库的结构类型，输出严格 JSON(无markdown):
{{
  "structure": "single|collection|json_lib|nav_list",
  "reason": "一句话依据",
  "collection_dir": "若为collection,子单元所在目录名,否则null",
  "nav_files": ["若为nav_list,需要解析的markdown文件路径列表,否则[]"],
  "self_worth": true/false
}}

structure 判据:
- single: 整个仓库就是一个工具/mcp/skill/框架本体(有单一的安装入口)
- collection: 有个目录下面每个子目录/文件是一个独立可用单元(如 skills/xxx/SKILL.md)
- json_lib: 主要内容是大型 JSON/数据文件(如成千上万条提示词)
- nav_list: 主要内容是 markdown 里的"资源链接清单/导航"(列了很多别的项目的链接)

self_worth: 这个仓库本体值不值得作为1条工具收录(nav_list通常true——它本身是个有用的导航)。"""


def probe(owner_repo, meta, tree, readme):
    prompt = PROBE_PROMPT.format(
        repo=owner_repo, stars=meta.get("stargazers_count", 0),
        desc=(meta.get("description") or "")[:200],
        tree="\n".join(f"  {t['type']} {t['name']}" for t in tree[:50]),
        readme=readme[:2000])
    return llm.chat_json(prompt, model=config.MODEL_BATCH, max_tokens=1500, retries=2)


# ---------------- ② 抽取(nav_list/单块) ----------------
EXTRACT_PROMPT = """你在从一段 AI 资源导航文档里抽取"可安装/可使用的工具"。下面是文档片段：

---
{chunk}
---

抽取其中每一个**具体的工具/框架/项目/skill/mcp**（有名字、能用的东西）。
严格排除：论文、博客文章、新闻、榜单、教程、纯概念介绍、公众号/社交媒体链接。

对每个合格项输出:
- name: 名称
- description_zh: 一句话中文说明它能干什么(40-80字)
- url: 它的官网或GitHub链接(从文档里找,没有就null)
- type: {types} 之一(拿不准填 tool)
- scenarios: 1-3个,从 {scenarios} 选
- ai_related: 是否与AI/大模型/AI开发相关(true/false)

只输出严格 JSON 数组(无markdown),没有合格项输出 []:
[{{"name":"...","description_zh":"...","url":"...","type":"...","scenarios":[...],"ai_related":true}}]"""


def extract_chunk(chunk):
    try:
        result = llm.chat_json(
            EXTRACT_PROMPT.format(chunk=chunk[:4000], types=TYPES, scenarios=SCENARIOS),
            model=config.MODEL_BATCH, max_tokens=3500, retries=2)
    except Exception as e:
        print(f"  抽取失败: {str(e)[:60]}", file=sys.stderr)
        return []
    if isinstance(result, dict):
        result = result.get("results") or result.get("items") or []
    return result if isinstance(result, list) else []


def chunk_markdown(md, target=3000):
    """按 ## / ### 标题切块，尽量每块 ~target 字符。"""
    # 去掉 HTML 徽章头
    md = re.sub(r"<p align.*?</p>", "", md, flags=re.S)
    parts = re.split(r"(?=^#{2,3}\s)", md, flags=re.M)
    chunks, buf = [], ""
    for p in parts:
        if len(buf) + len(p) > target and buf:
            chunks.append(buf)
            buf = p
        else:
            buf += p
    if buf.strip():
        chunks.append(buf)
    return [c for c in chunks if len(c.strip()) > 100]


# ---------------- 工具函数 ----------------
def slugify(s):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s[:40] or "item"


def existing_repos():
    repos = set()
    for f in DATA.rglob("*.yaml"):
        d = yaml.safe_load(f.read_text())
        r = (d.get("source") or {}).get("repo", "")
        u = (d.get("source") or {}).get("url", "")
        for x in (r, u):
            if x:
                repos.add(x.lower().rstrip("/"))
    return repos


def make_component(item, used_ids, existing, default_repo=None):
    if not item.get("ai_related", True):
        return None, "非AI相关"
    typ = item.get("type") if item.get("type") in TYPES else "tool"
    name = str(item.get("name", "")).strip()
    desc = str(item.get("description_zh", "")).strip()
    if len(name) < 2 or len(desc) < 10:
        return None, "名称/描述不足"
    url = (item.get("url") or default_repo or "").strip()
    if url and url.lower().rstrip("/") in existing:
        return None, "已存在"
    scen = [s for s in item.get("scenarios", []) if s in SCENARIOS][:3] or ["other"]

    base = f"{typ}-{slugify(name)}"
    cid, n = base, 2
    while cid in used_ids:
        cid, n = f"{base}-{n}", n + 1
    used_ids.add(cid)
    if url:
        existing.add(url.lower().rstrip("/"))

    doc = {
        "id": cid, "type": typ, "name": name[:80], "description_zh": desc[:300],
        "host_tools": ["any"], "scenarios": scen, "tags": [], "difficulty": "intermediate",
        "install": {"method": "manual", "notes_zh": "详见来源链接"},
        "quality": {"verified": False},
        "source": {"repo" if "github.com" in url else "url": url} if url else {"url": default_repo or ""},
    }
    return doc, "ok"


# ---------------- 主流程 ----------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo", help="owner/repo")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--max-items", type=int, default=0)
    args = ap.parse_args()

    meta = gh_json(f"/repos/{args.repo}")
    tree = gh_json(f"/repos/{args.repo}/contents/")
    readme = gh_raw(args.repo, "README.md")

    plan = probe(args.repo, meta, tree, readme)
    print(f"[勘探] 结构={plan.get('structure')} 依据={plan.get('reason')}")

    existing = existing_repos()
    used_ids = set()
    for f in DATA.rglob("*.yaml"):
        used_ids.add(yaml.safe_load(f.read_text())["id"])

    structure = plan.get("structure")
    docs = []

    if structure == "nav_list":
        nav_files = plan.get("nav_files") or []
        if not nav_files:
            nav_files = [t["name"] for t in tree if t["name"].endswith(".md")
                         and t["name"].lower() != "readme.md"][:20]
        # 收集所有块
        all_chunks = []
        for nf in nav_files:
            md = gh_raw(args.repo, nf)
            all_chunks.extend(chunk_markdown(md))
        print(f"[抽取] {len(nav_files)} 个文件 → {len(all_chunks)} 块，并发抽取…")
        raw_items = []
        with cf.ThreadPoolExecutor(4) as ex:
            for i, items in enumerate(ex.map(extract_chunk, all_chunks), 1):
                raw_items.extend(items)
                if i % 10 == 0:
                    print(f"  {i}/{len(all_chunks)} 块, 累计 {len(raw_items)} 条原始项")
        print(f"[抽取] 原始 {len(raw_items)} 条 → 严筛+去重…")
        stats = {}
        for it in raw_items:
            doc, why = make_component(it, used_ids, existing)
            stats[why] = stats.get(why, 0) + 1
            if doc:
                docs.append(doc)
            if args.max_items and len(docs) >= args.max_items:
                break
        print(f"[严筛] {dict(sorted(stats.items(), key=lambda x:-x[1]))}")

    elif structure == "single":
        # 整仓库当 1 条：让 LLM 用 README 抽字段
        doc, why = make_component({
            "name": meta["name"], "description_zh": (meta.get("description") or "")[:200],
            "url": meta["html_url"], "type": "tool", "scenarios": ["other"], "ai_related": True,
        }, used_ids, existing)
        if doc:
            docs.append(doc)
        print(f"[single] {'收录1条' if doc else why}")

    elif structure == "collection":
        cdir = plan.get("collection_dir")
        subs = gh_json(f"/repos/{args.repo}/contents/{urllib.parse.quote(cdir)}") if cdir else []
        print(f"[collection] {cdir}/ 下 {len(subs)} 个单元")
        for s in subs:
            if s["type"] != "dir":
                continue
            doc, why = make_component({
                "name": s["name"], "description_zh": f"来自 {args.repo} 的 {s['name']} 单元",
                "url": s["html_url"], "type": "skill", "scenarios": ["coding"], "ai_related": True,
            }, used_ids, existing)
            if doc:
                docs.append(doc)
            if args.max_items and len(docs) >= args.max_items:
                break

    elif structure == "json_lib":
        print("[json_lib] 该类型走专用 import_prompts 管线，本脚本仅登记来源。")
        doc, why = make_component({
            "name": meta["name"], "description_zh": (meta.get("description") or "")[:200],
            "url": meta["html_url"], "type": "tool", "scenarios": ["other"], "ai_related": True,
        }, used_ids, existing)
        if doc:
            docs.append(doc)

    # nav_list 仓库本体也值得登记
    if plan.get("self_worth") and structure == "nav_list":
        d2, _ = make_component({
            "name": meta["name"], "description_zh": (meta.get("description") or meta["name"])[:200],
            "url": meta["html_url"], "type": "tool", "scenarios": ["research"], "ai_related": True,
        }, used_ids, existing)
        if d2:
            docs.append(d2)

    print(f"\n共产出 {len(docs)} 条新组件")
    if args.dry_run:
        for d in docs[:15]:
            print(f"  [{d['type']}] {d['name']} — {d['description_zh'][:50]}")
        print("(dry-run，未落盘)")
        return
    for d in docs:
        out = DATA / d["type"] / f"{d['id']}.yaml"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(yaml.dump(d, allow_unicode=True, sort_keys=False, width=120))
    print(f"✅ 已落盘 {len(docs)} 条到 data/components/（跑 validate + ingest 生效）")


if __name__ == "__main__":
    main()
