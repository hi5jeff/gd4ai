#!/usr/bin/env python3
"""用 GitHub API 补全组件的 stars / last_commit（写回 YAML）。无 token 限 60 次/时。"""
import json, os, pathlib, re, urllib.request
import yaml

ROOT = pathlib.Path(__file__).parent.parent / "data" / "components"
TOKEN = os.environ.get("GITHUB_TOKEN", "")

def gh(repo):
    req = urllib.request.Request(f"https://api.github.com/repos/{repo}",
        headers={"Authorization": f"Bearer {TOKEN}"} if TOKEN else {})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)

cache = {}
for f in sorted(ROOT.rglob("*.yaml")):
    doc = yaml.safe_load(f.read_text())
    repo_url = (doc.get("source") or {}).get("repo", "")
    m = re.match(r"https://github\.com/([^/]+/[^/]+)", repo_url)
    if not m:
        continue
    repo = m.group(1)
    try:
        info = cache.get(repo) or gh(repo)
        cache[repo] = info
        q = doc.setdefault("quality", {})
        q["stars"] = info["stargazers_count"]
        q["last_commit"] = info["pushed_at"][:10]
        f.write_text(yaml.dump(doc, allow_unicode=True, sort_keys=False, width=120))
        print(f"{doc['id']}: ⭐{q['stars']} 最近提交 {q['last_commit']}")
    except Exception as e:
        print(f"{doc['id']}: FAIL {e}")
