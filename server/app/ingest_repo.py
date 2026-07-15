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


# ---------------- 网页抓取 ----------------
FIRECRAWL_KEY = os.environ.get("FIRECRAWL_API_KEY", "")


def fetch_firecrawl(url):
    """用 firecrawl 云 API 抓取,返回干净 Markdown(能渲染JS、正文更全)。失败返回 None。"""
    if not FIRECRAWL_KEY:
        return None
    body = json.dumps({"url": url, "formats": ["markdown"], "onlyMainContent": True}).encode()
    req = urllib.request.Request("https://api.firecrawl.dev/v2/scrape", data=body,
        headers={"Authorization": f"Bearer {FIRECRAWL_KEY}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            d = json.load(r)
        md = (d.get("data") or {}).get("markdown", "")
        return md if md and len(md) > 100 else None
    except Exception as e:
        print(f"  firecrawl失败({str(e)[:50]}),降级原生抓取", file=sys.stderr)
        return None


def fetch_web(url):
    """抓取网页正文。优先 firecrawl(干净markdown/能渲染JS),失败降级原生 HTML 清洗。"""
    md = fetch_firecrawl(url)
    if md:
        return md
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; gd4ai-bot/1.0)"})
    with urllib.request.urlopen(req, timeout=40) as r:
        html = r.read().decode("utf-8", "ignore")
    html = re.sub(r"<(script|style|noscript)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    html = re.sub(r'<a\s[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>',
                  lambda m: f" {re.sub(r'<[^>]+>', '', m.group(2))} ({m.group(1)}) ", html, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"&[a-z]+;", " ", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n", text)
    return text.strip()


def chunk_text(text, target=3500):
    """把纯文本按长度切块。超长单行强制按字符硬切(防某行过长成一个巨块被LLM漏掉)。"""
    lines = []
    for ln in text.split("\n"):
        while len(ln) > target:
            lines.append(ln[:target])
            ln = ln[target:]
        lines.append(ln)
    chunks, buf = [], ""
    for ln in lines:
        if len(buf) + len(ln) > target and buf:
            chunks.append(buf)
            buf = ln
        else:
            buf += "\n" + ln
    if buf.strip():
        chunks.append(buf)
    return [c for c in chunks if len(c.strip()) > 80]


def ingest_web(url, dry_run=False, max_items=0, min_stars=0, min_year=0,
               existing=None, used_ids=None, log=print):
    """摄取一个网页/网站：抓正文 → 切块 → LLM 抽取条目 → 严筛去重。"""
    if existing is None or used_ids is None:
        existing, used_ids = load_state()
    text = fetch_web(url)
    if len(text) < 200:
        log(f"[{url}] 网页内容过少({len(text)}字)，跳过")
        return [], {"structure": "web_empty"}
    chunks = chunk_text(text)
    log(f"[{url}] 抓取 {len(text)} 字 → {len(chunks)} 块，并发抽取…")
    raw_items = []
    with cf.ThreadPoolExecutor(4) as ex:
        for items in ex.map(extract_chunk, chunks):
            raw_items.extend(items)
    stats, cand = {}, []
    for it in raw_items:
        doc, why = make_component(it, used_ids, existing, default_repo=url)
        stats[why] = stats.get(why, 0) + 1
        if doc:
            cand.append(doc)
    log(f"[{url}] 初筛 {dict(sorted(stats.items(), key=lambda x:-x[1]))} → 候选 {len(cand)}")
    if min_stars or min_year:
        def check(doc):
            u = (doc.get("source") or {}).get("repo", "")
            if "github.com" not in u:
                return doc
            stars, pushed = enrich_github(u)
            if stars is not None and stars < min_stars:
                return None
            if min_year and pushed and pushed[:4].isdigit() and int(pushed[:4]) < min_year:
                return None
            if stars is not None:
                doc["quality"]["stars"] = stars
            if pushed:
                doc["quality"]["last_commit"] = pushed
            return doc
        with cf.ThreadPoolExecutor(8) as ex:
            cand = [d for d in ex.map(check, cand) if d]
        log(f"[{url}] star/年过滤 → 存活 {len(cand)}")
    docs = cand[:max_items] if max_items else cand
    if not dry_run:
        for d in docs:
            out = DATA / d["type"] / f"{d['id']}.yaml"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(yaml.dump(d, allow_unicode=True, sort_keys=False, width=120))
    return docs, {"structure": "web"}


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

抽取其中每一个**对用户有价值的条目**，并判断它属于哪一类(kind)：
- tool: 能安装/使用的工具、框架、mcp、skill、插件（有代码仓库或产品）
- knowledge: 有价值的技巧/经验/方法论/指南/教程（如"vibe coding指南""prompt技巧"）——不是工具但是干货
- resource: 导航站/合集/目录/精选清单（本身是一个可查阅的资源入口）

只丢弃（keep=false）：纯新闻、时效性资讯、榜单快讯、公众号/社交媒体关注链接、纯广告、无实质内容的条目。

对每一项输出:
- name: 名称
- description_zh: 一句话中文说明它是什么/能干什么(40-80字)
- url: 官网或GitHub链接(从文档里找,没有就null)
- kind: tool | knowledge | resource
- type: {types} 之一(knowledge/resource 拿不准填 tool，kind 才是关键)
- scenarios: 1-3个,从 {scenarios} 选
- keep: 是否值得收录(true/false)
- ai_related: 是否与AI/大模型/AI开发/AI应用相关(true/false)

只输出严格 JSON 数组(无markdown),没有合格项输出 []:
[{{"name":"...","description_zh":"...","url":"...","kind":"tool","type":"...","scenarios":[...],"keep":true,"ai_related":true}}]"""


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


def enrich_github(url):
    """给 GitHub url 补 stars/最近提交。返回 (stars, pushed_date) 或 (None, None)。"""
    m = re.match(r"https?://github\.com/([^/]+/[^/#?]+)", url or "")
    if not m:
        return None, None
    repo = m.group(1).rstrip("/").removesuffix(".git")
    try:
        info = gh_json(f"/repos/{repo}")
        return info.get("stargazers_count"), (info.get("pushed_at") or "")[:10]
    except Exception:
        return None, None


def make_component(item, used_ids, existing, default_repo=None,
                   min_stars=0, min_year=0):
    if not item.get("ai_related", True):
        return None, "非AI相关"
    # keep=false 才丢弃(新闻/榜单/社交链接)。旧字段 is_tool 兼容: is_tool=false 但没给keep则丢
    if item.get("keep") is False or (item.get("is_tool") is False and "keep" not in item):
        return None, "无价值(新闻/榜单/社交)"
    kind = item.get("kind") if item.get("kind") in ("tool", "knowledge", "resource") else "tool"
    typ = item.get("type") if item.get("type") in TYPES else "tool"
    name = str(item.get("name", "")).strip()
    desc = str(item.get("description_zh", "")).strip()
    if len(name) < 2 or len(desc) < 10:
        return None, "名称/描述不足"
    url = (item.get("url") or default_repo or "").strip()
    if url and url.lower().rstrip("/") in existing:
        return None, "已存在"
    scen = [s for s in item.get("scenarios", []) if s in SCENARIOS][:3] or ["other"]

    # GitHub 项目：补 star/最近提交，过滤太冷门或多年不更新的
    stars, pushed = (None, None)
    if (min_stars or min_year) and "github.com" in url:
        stars, pushed = enrich_github(url)
        if stars is not None and stars < min_stars:
            return None, f"star不足({stars})"
        if min_year and pushed and pushed[:4].isdigit() and int(pushed[:4]) < min_year:
            return None, f"多年未更新({pushed})"

    base = f"{typ}-{slugify(name)}"
    cid, n = base, 2
    while cid in used_ids:
        cid, n = f"{base}-{n}", n + 1
    used_ids.add(cid)
    if url:
        existing.add(url.lower().rstrip("/"))

    quality = {"verified": False}
    if stars is not None:
        quality["stars"] = stars
    if pushed:
        quality["last_commit"] = pushed
    doc = {
        "id": cid, "type": typ, "kind": kind, "name": name[:80], "description_zh": desc[:300],
        "host_tools": ["any"], "scenarios": scen, "tags": [], "difficulty": "intermediate",
        "install": {"method": "manual", "notes_zh": "详见来源链接"},
        "quality": quality,
        "source": {"repo" if "github.com" in url else "url": url} if url else {"url": default_repo or ""},
    }
    return doc, "ok"


SUBUNIT_PROMPT = """这是 GitHub 仓库 {repo} 里的一个子项目「{name}」(路径 {path})。
它的 README/说明:
---
{readme}
---
判断并输出JSON: {{"name":"友好名称","description_zh":"一句话中文说明这个子项目能干什么(40-80字)","type":"{types}其一","scenarios":["从{scen}选1-3个"],"keep":true/false(是否是有价值的可用应用/工具,占位/空目录=false)}}
只输出JSON,无markdown。"""


def norm_ws(s):
    """压平多余空白，便于喂给 LLM。"""
    return re.sub(r"[ \t]+", " ", re.sub(r"\n\s*\n+", "\n", s or "")).strip()


def _find_app_dirs(repo, base, depth=4):
    """递归找叶子应用目录：含 README/代码文件、且不再有有意义子目录的目录。返回 [(name,path)]。"""
    out = []
    try:
        items = gh_json(f"/repos/{repo}/contents/{urllib.parse.quote(base)}") if base else gh_json(f"/repos/{repo}/contents/")
    except Exception:
        return out
    subdirs = [i for i in items if i["type"] == "dir" and not i["name"].startswith(".")
               and i["name"] not in ("docs", "assets", "images", "__pycache__")]
    files = [i for i in items if i["type"] == "file"]
    has_readme = any(f["name"].lower().startswith("readme") for f in files)
    has_code = any(f["name"].endswith((".py", ".ts", ".js", ".ipynb")) for f in files)
    # 叶子：有README/代码 且 子目录很少 → 它本身是个 app
    if base and (has_readme or has_code) and len(subdirs) <= 1:
        out.append((base.split("/")[-1], base))
        return out
    # 还有子目录且没到深度上限 → 继续下钻
    if subdirs and depth > 0:
        for sd in subdirs:
            out.extend(_find_app_dirs(repo, sd["path"], depth - 1))
    elif base and (has_readme or has_code):
        # 到底了但本目录有内容 → 也算一个 app
        out.append((base.split("/")[-1], base))
    return out


def _make_subunit(repo, name, path, meta, used_ids, existing, log):
    """读子项目 README → LLM 生成描述 → 组件。"""
    readme = ""
    for rn in ("README.md", "readme.md", "SKILL.md"):
        readme = gh_raw(repo, f"{path}/{rn}")
        if readme:
            break
    url = f"https://github.com/{repo}/tree/main/{path}"
    if url.lower() in existing:
        return None
    try:
        r = llm.chat_json(SUBUNIT_PROMPT.format(
            repo=repo, name=name, path=path, readme=norm_ws(readme)[:2500] or name,
            types=TYPES, scen=SCENARIOS), model=config.MODEL_BATCH, max_tokens=1200, retries=2)
    except Exception:
        return None
    if not r.get("keep") or len((r.get("description_zh") or "")) < 10:
        return None
    doc, why = make_component({
        "name": r.get("name") or name, "description_zh": r["description_zh"],
        "url": url, "kind": "tool",
        "type": r.get("type") if r.get("type") in TYPES else "tool",
        "scenarios": r.get("scenarios", []), "ai_related": True, "keep": True,
    }, used_ids, existing)
    if doc:
        doc["quality"]["stars"] = meta.get("stargazers_count")
    return doc


# ---------------- 核心：摄取单个仓库 ----------------
def load_state():
    """加载全库已有 repo/url 和 id，供去重。批量模式下多仓库共享同一份并累加。"""
    existing = existing_repos()
    used_ids = set()
    for f in DATA.rglob("*.yaml"):
        used_ids.add(yaml.safe_load(f.read_text())["id"])
    return existing, used_ids


def ingest_one(repo, dry_run=False, max_items=0, min_stars=0, min_year=0,
               existing=None, used_ids=None, log=print):
    """摄取一个仓库，返回产出的 doc 列表。existing/used_ids 传入则跨仓库共享去重。"""
    if existing is None or used_ids is None:
        existing, used_ids = load_state()

    meta = gh_json(f"/repos/{repo}")
    tree = gh_json(f"/repos/{repo}/contents/")
    readme = gh_raw(repo, "README.md")
    plan = probe(repo, meta, tree, readme)
    structure = plan.get("structure")
    log(f"[{repo}] 结构={structure} 依据={plan.get('reason')}")
    docs = []

    if structure == "nav_list":
        nav_files = plan.get("nav_files") or [
            t["name"] for t in tree if t["name"].endswith(".md")
            and t["name"].lower() != "readme.md"][:20]
        all_chunks = []
        for nf in nav_files:
            all_chunks.extend(chunk_markdown(gh_raw(repo, nf)))
        log(f"[{repo}] {len(nav_files)} 文件 → {len(all_chunks)} 块，并发抽取…")
        raw_items = []
        with cf.ThreadPoolExecutor(4) as ex:
            for items in ex.map(extract_chunk, all_chunks):
                raw_items.extend(items)
        stats, cand = {}, []
        for it in raw_items:
            doc, why = make_component(it, used_ids, existing)
            stats[why] = stats.get(why, 0) + 1
            if doc:
                cand.append(doc)
        log(f"[{repo}] 初筛 {dict(sorted(stats.items(), key=lambda x:-x[1]))} → 候选 {len(cand)}")
        if min_stars or min_year:
            def check(doc):
                url = (doc.get("source") or {}).get("repo", "")
                if "github.com" not in url:
                    return doc
                stars, pushed = enrich_github(url)
                if stars is not None and stars < min_stars:
                    return None
                if min_year and pushed and pushed[:4].isdigit() and int(pushed[:4]) < min_year:
                    return None
                if stars is not None:
                    doc["quality"]["stars"] = stars
                if pushed:
                    doc["quality"]["last_commit"] = pushed
                return doc
            with cf.ThreadPoolExecutor(8) as ex:
                cand = [d for d in ex.map(check, cand) if d]
            log(f"[{repo}] star≥{min_stars}/年≥{min_year} → 存活 {len(cand)}")
        docs = cand[:max_items] if max_items else cand

    elif structure in ("single", "json_lib"):
        doc, why = make_component({
            "name": meta["name"], "description_zh": (meta.get("description") or meta["name"])[:200],
            "url": meta["html_url"], "type": "tool", "scenarios": ["other"], "ai_related": True,
        }, used_ids, existing)
        if doc:
            doc["quality"]["stars"] = meta.get("stargazers_count")
            doc["quality"]["last_commit"] = (meta.get("pushed_at") or "")[:10]
            docs.append(doc)
        log(f"[{repo}] {structure}: {'收录1条' if doc else why}")

    elif structure == "collection":
        cdir = plan.get("collection_dir")
        # 递归找所有叶子 app 目录(支持多级 monorepo)
        app_dirs = _find_app_dirs(repo, cdir or "")
        if max_items:
            app_dirs = app_dirs[:max_items]
        log(f"[{repo}] collection: 发现 {len(app_dirs)} 个子项目,读README+LLM生成描述…")
        with cf.ThreadPoolExecutor(4) as ex:
            results = list(ex.map(
                lambda np: _make_subunit(repo, np[0], np[1], meta, used_ids, existing, log),
                app_dirs))
        docs = [d for d in results if d]
        log(f"[{repo}] 展开 {len(docs)} 条子项目")
        # 仓库本体也作为 1 条合集入口
        d0, _ = make_component({
            "name": meta["name"], "description_zh": (meta.get("description") or meta["name"])[:200],
            "url": meta["html_url"], "kind": "resource", "type": "plugin",
            "scenarios": ["coding"], "ai_related": True, "keep": True,
        }, used_ids, existing)
        if d0:
            d0["quality"]["stars"] = meta.get("stargazers_count")
            d0["quality"]["last_commit"] = (meta.get("pushed_at") or "")[:10]
            docs.append(d0)

    # nav_list 仓库本体也登记
    if plan.get("self_worth") and structure == "nav_list":
        d2, _ = make_component({
            "name": meta["name"], "description_zh": (meta.get("description") or meta["name"])[:200],
            "url": meta["html_url"], "type": "tool", "scenarios": ["research"], "ai_related": True,
        }, used_ids, existing)
        if d2:
            d2["quality"]["stars"] = meta.get("stargazers_count")
            docs.append(d2)

    if not dry_run:
        for d in docs:
            out = DATA / d["type"] / f"{d['id']}.yaml"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(yaml.dump(d, allow_unicode=True, sort_keys=False, width=120))
    return docs, plan


def ingest_any(target, dry_run=False, max_items=0, min_stars=0, min_year=0,
               existing=None, used_ids=None, log=print):
    """统一入口：自动识别 owner/repo、github URL、普通网页 URL，路由到对应摄取器。"""
    t = target.strip()
    is_url = t.startswith("http://") or t.startswith("https://")
    if is_url and "github.com/" in t:
        m = re.search(r"github\.com/([^/]+/[^/#?]+)", t)
        t = m.group(1).rstrip("/").removesuffix(".git") if m else t
        is_url = False
    if is_url:
        return ingest_web(t, dry_run, max_items, min_stars, min_year, existing, used_ids, log)
    return ingest_one(t, dry_run, max_items, min_stars, min_year, existing, used_ids, log)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo", help="owner/repo 或 http(s):// 网址")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--persist", action="store_true",
                    help="直接落库(PG+Meili+向量)，而非只写 YAML")
    ap.add_argument("--max-items", type=int, default=0)
    ap.add_argument("--min-stars", type=int, default=0)
    ap.add_argument("--min-year", type=int, default=0)
    args = ap.parse_args()
    # --persist 时用 dry_run=True 跳过写 YAML(可能只读)，docs 照常产出后直接落库
    docs, _ = ingest_any(args.repo, args.dry_run or args.persist,
                         args.max_items, args.min_stars, args.min_year)
    print(f"\n共产出 {len(docs)} 条新组件")
    for d in docs[:15]:
        print(f"  [{d['type']}] {d['name']} — {d['description_zh'][:50]}")
    if args.dry_run and not args.persist:
        print("(dry-run，未落盘)")
    elif args.persist:
        from . import ingest
        n = ingest.persist_docs(docs)
        print(f"✅ 已落库 {n} 条(PG+Meili+向量)")
    else:
        print(f"✅ 已写 YAML {len(docs)} 条(需再跑 app.ingest 才入库)")


if __name__ == "__main__":
    main()
