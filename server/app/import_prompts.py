"""细粒度提示词导入管线：源 JSON → 批量过 LLM(质量分+中文标题+场景标签) → 向量化 → prompts 表。

设计要点：
- 批量过 LLM（每批 BATCH 条一次调用），不逐条，省时省钱
- 多进程/多线程并发调 LLM 与向量化
- 质量分低于阈值直接丢弃；(source_id, ext_id) 唯一约束天然去重
- content 原文一字不改，只加工元数据

用法（在 howai-api 容器内跑，能连内网 PG/embedding/mdbox）:
    python -m app.import_prompts <source_id> <本地json路径> [--limit N] [--min-quality 0.55]
源 JSON 格式: [{"id":..., "content":"..."}]（YouMind 提示词库格式）
"""
import argparse
import concurrent.futures as cf
import json
import sys

from psycopg.types.json import Jsonb
from . import config, db, llm, retrieval

BATCH = 8           # 每次给 LLM 多少条（批太大→网关504）
EMBED_BATCH = 32
WORKERS = 4         # 并发批数（太高易触发网关限流/超时）
CONTENT_CLIP = 500  # 每条 content 送进 LLM 的最大字符

PROMPT = """你在为 AI 绘图提示词库做数据加工。下面是 {n} 条图片生成提示词（英文原文），逐条分析。

对每一条，输出：
- id: 原样返回输入的 id
- keep: 是否值得收录（true/false）。垃圾、残缺、纯乱码、明显重复模板 → false
- quality: 质量分 0-1（提示词是否完整、具体、可复现出好效果）
- title_zh: 中文短标题（10字内，概括生成什么，如"香水广告主图""国风美妆海报"）
- summary_zh: 一句话说明能生成什么效果的图（20字内）
- scene_tags: 1-3个细分场景中文标签（如 香水广告/化妆品/数码产品/食品/服装/珠宝/人像/风景）
- style_tags: 1-2个风格标签（如 写实/3D/扁平/国风/赛博朋克/极简）

只输出严格 JSON 数组，无 markdown：
[{{"id":..., "keep":true, "quality":0.8, "title_zh":"...", "summary_zh":"...", "scene_tags":[...], "style_tags":[...]}}]

提示词列表：
{items}"""


def process_batch(batch: list[dict]) -> list[dict]:
    """一批 [{id, content}] → LLM 加工后的元数据列表。失败返回 []。"""
    items_txt = "\n".join(
        f'[id={it["id"]}] {it["content"][:CONTENT_CLIP]}' for it in batch
    )
    try:
        result = llm.chat_json(
            PROMPT.format(n=len(batch), items=items_txt),
            model=config.MODEL_BATCH, max_tokens=3000, retries=3,
        )
    except Exception as e:
        print(f"  批次失败: {str(e)[:80]}", file=sys.stderr)
        return []
    # LLM 可能返回 {"results":[...]} 或直接数组
    if isinstance(result, dict):
        result = result.get("results") or result.get("data") or []
    by_id = {str(it["id"]): it for it in batch}
    out = []
    for r in result:
        rid = str(r.get("id"))
        if rid not in by_id or not r.get("keep"):
            continue
        content = by_id[rid]["content"]
        out.append({
            "ext_id": rid,
            "content": content,
            "title_zh": (r.get("title_zh") or "")[:60] or "未命名提示词",
            "summary_zh": (r.get("summary_zh") or "")[:120],
            "scene_tags": [str(t)[:20] for t in (r.get("scene_tags") or [])][:3],
            "style_tags": [str(t)[:20] for t in (r.get("style_tags") or [])][:2],
            "quality": float(r.get("quality") or 0),
        })
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source_id")
    ap.add_argument("json_path")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--min-quality", type=float, default=0.55)
    args = ap.parse_args()

    raw = json.loads(open(args.json_path).read())
    if args.limit:
        raw = raw[: args.limit]
    raw = [it for it in raw if it.get("content")]
    print(f"源 {args.source_id}: 读入 {len(raw)} 条")

    db.pool.open()
    db.init_schema()

    batches = [raw[i : i + BATCH] for i in range(0, len(raw), BATCH)]
    enriched = []
    with cf.ThreadPoolExecutor(WORKERS) as ex:
        for i, res in enumerate(ex.map(process_batch, batches), 1):
            enriched.extend(res)
            if i % 20 == 0:
                print(f"  LLM 加工 {i}/{len(batches)} 批, 累计保留 {len(enriched)}")

    kept = [e for e in enriched if e["quality"] >= args.min_quality]
    print(f"LLM 加工完: 保留 {len(enriched)}，过质量线({args.min_quality}) {len(kept)}")
    if not kept:
        print("无合格数据，退出")
        return

    # 向量化：检索文本 = 中文标题+摘要+标签+英文content片段（双语可检索）
    def emb_text(e):
        return " ".join([e["title_zh"], e["summary_zh"], " ".join(e["scene_tags"]),
                         " ".join(e["style_tags"]), e["content"][:200]])
    texts = [emb_text(e) for e in kept]
    vecs = []
    for i in range(0, len(texts), EMBED_BATCH):
        vecs.extend(retrieval.embed(texts[i : i + EMBED_BATCH]))
        if (i // EMBED_BATCH) % 10 == 0:
            print(f"  向量化 {min(i+EMBED_BATCH,len(texts))}/{len(texts)}")

    # 批量入库（去重 upsert）
    inserted = 0
    with db.pool.connection() as conn:
        with conn.cursor() as cur:
            for e, text, vec in zip(kept, texts, vecs):
                vec_str = "[" + ",".join(f"{x:.6f}" for x in vec) + "]"
                cur.execute(
                    "INSERT INTO prompts (source_id, ext_id, title_zh, summary_zh, content, "
                    "scene_tags, style_tags, quality, search_text, embedding) "
                    "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s::vector) "
                    "ON CONFLICT (source_id, ext_id) DO UPDATE SET title_zh=EXCLUDED.title_zh, "
                    "summary_zh=EXCLUDED.summary_zh, scene_tags=EXCLUDED.scene_tags, "
                    "quality=EXCLUDED.quality, embedding=EXCLUDED.embedding",
                    (args.source_id, e["ext_id"], e["title_zh"], e["summary_zh"], e["content"],
                     e["scene_tags"], e["style_tags"], e["quality"], text, vec_str),
                )
                inserted += 1
    print(f"✅ 入库 {inserted} 条到 prompts 表 (source={args.source_id})")
    with db.pool.connection() as conn:
        total = conn.execute("SELECT count(*) FROM prompts").fetchone()[0]
    print(f"   prompts 表现有总量: {total}")


if __name__ == "__main__":
    main()