#!/usr/bin/env python3
"""校验 data/ 下所有组件和方案包 YAML：schema 合法 + 引用完整。入库前必须全绿。"""
import json, sys, pathlib
import yaml, jsonschema

ROOT = pathlib.Path(__file__).parent.parent / "data"

def load_all(subdir, schema_file):
    schema = json.loads((ROOT / "schema" / schema_file).read_text())
    items, errors = {}, []
    for f in sorted((ROOT / subdir).rglob("*.yaml")):
        try:
            doc = yaml.safe_load(f.read_text())
            jsonschema.validate(doc, schema)
            if doc["id"] in items:
                errors.append(f"{f.name}: id 重复 {doc['id']}")
            items[doc["id"]] = doc
        except Exception as e:
            errors.append(f"{f.name}: {str(e).splitlines()[0][:160]}")
    return items, errors

def main():
    comps, e1 = load_all("components", "component.schema.json")
    pbs, e2 = load_all("playbooks", "playbook.schema.json")
    errors = e1 + e2

    # 引用完整性：relations 和 playbook.components.ref 必须指向存在的组件 id
    for c in comps.values():
        rel = c.get("relations", {})
        for kind in ("works_with", "alternatives", "requires"):
            for ref in rel.get(kind, []):
                if ref not in comps:
                    errors.append(f"组件 {c['id']}: relations.{kind} 引用不存在的 id '{ref}'")
    for p in pbs.values():
        for comp in p["components"]:
            if comp["ref"] not in comps:
                errors.append(f"方案 {p['id']}: 引用不存在的组件 '{comp['ref']}'")

    print(f"组件 {len(comps)} 个, 方案包 {len(pbs)} 个")
    if errors:
        print("\n".join("❌ " + e for e in errors))
        sys.exit(1)
    print("✅ 全部校验通过")

if __name__ == "__main__":
    main()
