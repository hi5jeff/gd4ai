"""批量摄取多个 GitHub 仓库：受控并发（默认同时 2 个仓库），跨仓库共享去重。

一条命令喂一串仓库，不用为每个仓库单独起脚本。并发受控是因为 mdbox 网关和
GitHub API 都有限流，同时跑太多会互相挤爆。

用法(容器内):
    python -m app.ingest_batch repos.txt [--dry-run] [--min-stars N] [--min-year Y] [--concurrency 2]
repos.txt: 每行一个 owner/repo（# 开头为注释）
也可直接传逗号分隔: python -m app.ingest_batch "owner/a,owner/b"
"""
import argparse
import concurrent.futures as cf
import sys
import threading

from . import ingest_repo

_lock = threading.Lock()   # 保护共享去重集合


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repos", help="repos.txt 路径 或 逗号分隔的 owner/repo 列表")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--max-items", type=int, default=0)
    ap.add_argument("--min-stars", type=int, default=0)
    ap.add_argument("--min-year", type=int, default=0)
    ap.add_argument("--concurrency", type=int, default=2)
    args = ap.parse_args()

    # 解析仓库列表：优先当文件读，读不到就当逗号分隔的列表
    import os
    if os.path.isfile(args.repos):
        with open(args.repos) as f:
            repos = [ln.strip() for ln in f if ln.strip() and not ln.startswith("#")]
    else:
        repos = [r.strip() for r in args.repos.split(",") if r.strip()]

    print(f"批量摄取 {len(repos)} 个仓库，并发 {args.concurrency}\n")

    existing, used_ids = ingest_repo.load_state()

    def worker(repo):
        # 共享 existing/used_ids，加锁保证跨仓库去重一致
        try:
            with _lock:
                snap_e, snap_u = set(existing), set(used_ids)
            docs, plan = ingest_repo.ingest_any(
                repo, args.dry_run, args.max_items, args.min_stars, args.min_year,
                existing=snap_e, used_ids=snap_u,
                log=lambda m: print(m, flush=True))
            with _lock:
                for d in docs:
                    used_ids.add(d["id"])
                    src = d.get("source", {})
                    for x in (src.get("repo"), src.get("url")):
                        if x:
                            existing.add(x.lower().rstrip("/"))
            return repo, len(docs), plan.get("structure")
        except Exception as e:
            print(f"[{repo}] ❌ 失败: {str(e)[:100]}", flush=True)
            return repo, 0, "error"

    results = []
    with cf.ThreadPoolExecutor(args.concurrency) as ex:
        for r in ex.map(worker, repos):
            results.append(r)

    print("\n===== 批量摄取汇总 =====")
    total = 0
    for repo, n, struct in results:
        total += n
        print(f"  {repo}: {struct} → {n} 条")
    print(f"合计新增 {total} 条{'（dry-run未落盘）' if args.dry_run else ''}")


if __name__ == "__main__":
    main()
