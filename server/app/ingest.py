"""把 data/ 下的 YAML 入库：校验 → PG(含向量) → Meilisearch。用法: python -m app.ingest"""
import json
import pathlib
import jsonschema
import yaml
from psycopg.types.json import Jsonb
from . import config, db, retrieval

DATA = pathlib.Path(config.DATA_DIR)


def build_search_text(doc: dict) -> str:
    parts = [doc.get("name", ""), doc.get("description_zh", ""), doc.get("title_zh", ""),
             doc.get("summary_zh", ""), " ".join(doc.get("tags", [])),
             " ".join(doc.get("scenarios", [doc.get("scenario", "")]) if isinstance(doc.get("scenarios", doc.get("scenario")), list) else [doc.get("scenario", "")]),
             " ".join(doc.get("categories", []))]
    return " ".join(p for p in parts if p)


def load_validated(subdir: str, schema_name: str) -> list[dict]:
    schema = json.loads((DATA / "schema" / schema_name).read_text())
    docs = []
    for f in sorted((DATA / subdir).rglob("*.yaml")):
        doc = yaml.safe_load(f.read_text())
        jsonschema.validate(doc, schema)
        docs.append(doc)
    return docs


def upsert(table: str, docs: list[dict]):
    texts = [build_search_text(d) for d in docs]
    vecs = retrieval.embed(texts)
    with db.pool.connection() as conn:
        for doc, text, vec in zip(docs, texts, vecs):
            vec_str = "[" + ",".join(f"{x:.6f}" for x in vec) + "]"
            if table == "components":
                conn.execute(
                    "INSERT INTO components (id, type, name, doc, search_text, embedding) "
                    "VALUES (%s, %s, %s, %s, %s, %s::vector) "
                    "ON CONFLICT (id) DO UPDATE SET type=EXCLUDED.type, name=EXCLUDED.name, "
                    "doc=EXCLUDED.doc, search_text=EXCLUDED.search_text, embedding=EXCLUDED.embedding",
                    (doc["id"], doc["type"], doc["name"], Jsonb(doc), text, vec_str),
                )
            else:
                conn.execute(
                    "INSERT INTO playbooks (id, scenario, doc, search_text, embedding) "
                    "VALUES (%s, %s, %s, %s, %s::vector) "
                    "ON CONFLICT (id) DO UPDATE SET scenario=EXCLUDED.scenario, doc=EXCLUDED.doc, "
                    "search_text=EXCLUDED.search_text, embedding=EXCLUDED.embedding",
                    (doc["id"], doc["scenario"], Jsonb(doc), text, vec_str),
                )


def meili_index(index: str, docs: list[dict], filterables: list[str]):
    idx = retrieval.meili.index(index)
    flat = []
    for d in docs:
        flat.append({
            "id": d["id"],
            "type": d.get("type", "playbook"),
            "name": d.get("name") or d.get("title_zh", ""),
            "description": d.get("description_zh") or d.get("summary_zh", ""),
            "tags": d.get("tags", []),
            "scenarios": d.get("scenarios") or [d.get("scenario", "")],
            "host_tools": d.get("host_tools", []),
            "difficulty": d.get("difficulty") or d.get("audience", ""),
        })
    task = idx.add_documents(flat, primary_key="id")
    retrieval.meili.wait_for_task(task.task_uid)
    idx.update_settings({
        "searchableAttributes": ["name", "description", "tags", "scenarios"],
        "filterableAttributes": filterables,
    })


def main():
    db.pool.open()
    db.init_schema()
    comps = load_validated("components", "component.schema.json")
    pbs = load_validated("playbooks", "playbook.schema.json")
    upsert("components", comps)
    upsert("playbooks", pbs)
    meili_index("components", comps, ["type", "scenarios", "host_tools", "difficulty"])
    meili_index("playbooks", pbs, ["scenarios"])
    print(f"入库完成: 组件 {len(comps)}, 方案包 {len(pbs)}")


if __name__ == "__main__":
    main()
