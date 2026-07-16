"""提示词画廊解析器：把 awesome-*-prompts 这类 README 画廊拆成一条条提示词 JSON。

这类仓库（如 YouMind-OpenLab/awesome-gpt-image-2）由同一套 Action 生成，README 里每条提示词是：
    ### No. N: <标题>
    #### 📖 Description  <描述>
    #### 📝 Prompt
    ```
    <可复制的提示词正文>
    ```
本脚本抓 README → 按 `### No.` 拆块 → 取每块第一个代码块作为提示词正文 → 输出
[{"id","content","title"}] 到 stdout，供 app.import_prompts 走细粒度入库管线。

用法（容器内）:
    python -m app.extract_gallery <owner/repo 或 github URL> [--branch main] > /tmp/p.json
    python -m app.import_prompts <source_id> /tmp/p.json
"""
import argparse
import json
import re
import sys
import urllib.request


def fetch_raw(repo, path, branches=("main", "master")):
    for br in branches:
        url = f"https://raw.githubusercontent.com/{repo}/{br}/{path}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "gd4ai-bot/1.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                if r.status == 200:
                    return r.read().decode("utf-8", "ignore")
        except Exception:
            continue
    return ""


# 一条提示词块的标题行：### No. 12: xxx  /  ### 12. xxx  /  ### Prompt 12: xxx
HEADER = re.compile(r'^#{2,4}\s*(?:No\.?\s*)?(\d+)\s*[:：.、]\s*(.+?)\s*$', re.M)
FENCE = re.compile(r'```[a-zA-Z0-9_-]*\n(.*?)```', re.S)


def parse_gallery(md: str, repo_slug: str):
    """从 README markdown 抽取提示词块。返回 [{id, title, content}]。

    直接扫全文的 `### No. N:` 块——开头的示例代码块不在这种标题下，天然排除；
    Featured 与 All Prompts 里的重复条目按正文去重。"""
    body = md
    heads = list(HEADER.finditer(body))
    out, seen = [], set()
    for i, h in enumerate(heads):
        num = h.group(1)
        title = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', h.group(2)).strip()  # 去标题里的徽章图
        seg = body[h.end(): heads[i + 1].start() if i + 1 < len(heads) else len(body)]
        # 优先取 "Prompt" 小标题后的代码块；否则取本块第一个代码块
        pm = re.search(r'#+\s*.*Prompt\s*\n', seg)
        scope = seg[pm.end():] if pm else seg
        fence = FENCE.search(scope) or FENCE.search(seg)
        if not fence:
            continue
        content = fence.group(1).strip()
        if len(content) < 12:            # 太短的跳过（多半是占位）
            continue
        key = content[:120]
        if key in seen:                  # 同仓库内去重
            continue
        seen.add(key)
        out.append({"id": f"{repo_slug}-{num}", "title": title[:80], "content": content})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo", help="owner/repo 或 github URL")
    ap.add_argument("--branch", default="")
    ap.add_argument("--readme", default="README.md", help="要解析的 README 文件名")
    args = ap.parse_args()

    repo = args.repo.strip()
    m = re.search(r'github\.com/([^/]+/[^/#?]+)', repo)
    if m:
        repo = m.group(1)
    repo = repo.rstrip("/").removesuffix(".git")
    slug = repo.split("/")[-1].lower()

    branches = (args.branch,) if args.branch else ("main", "master")
    md = fetch_raw(repo, args.readme, branches)
    if not md:
        print(f"未取到 {repo}/{args.readme}", file=sys.stderr)
        sys.exit(1)

    items = parse_gallery(md, slug)
    print(f"[{repo}] 解析出 {len(items)} 条提示词", file=sys.stderr)
    print(json.dumps(items, ensure_ascii=False))


if __name__ == "__main__":
    main()
