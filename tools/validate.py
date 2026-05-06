#!/usr/bin/env python3
"""
Validate every bundle in this repo against the v1.1 schema.

Run: python3 tools/validate.py
Exit code: 0 = all good, 1 = at least one error.

Checks:
  1. Each bundle file matches schema/bundle.v1.1.schema.json
  2. Each _category.json matches schema/category.schema.json
  3. Bundle's `id` field matches its directory location
  4. Bundle's `category` field matches its parent dir
  5. rule_ids look syntactically valid (R001-R9999)
  6. demo_agent name ends in '-demo'
  7. Every bundle has a corresponding examples/<id>/ directory
  8. (TODO) Cedar policy templates compile with default parameters — needs ag-policy
  9. (TODO) rule_ids exist in BUILTIN_RULES — needs services repo
"""

import json
import re
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError:
    sys.exit("jsonschema not installed. Run: pip install jsonschema")

REPO = Path(__file__).resolve().parent.parent
BUNDLES_DIR = REPO / "bundles"
EXAMPLES_DIR = REPO / "examples"
SCHEMA_DIR = REPO / "schema"

errors: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)
    print(f"  ✗ {msg}")


def ok(msg: str) -> None:
    print(f"  ✓ {msg}")


def load_json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as e:
        err(f"{path.relative_to(REPO)}: invalid JSON — {e}")
        return None


def main() -> int:
    print(f"Validating bundles under {BUNDLES_DIR}\n")

    bundle_schema = load_json(SCHEMA_DIR / "bundle.v1.1.schema.json")
    category_schema = load_json(SCHEMA_DIR / "category.schema.json")
    if not bundle_schema or not category_schema:
        return 1

    bundle_validator = jsonschema.Draft7Validator(bundle_schema)
    category_validator = jsonschema.Draft7Validator(category_schema)

    # 1. Categories
    print("== _category.json files ==")
    for cat_file in sorted(BUNDLES_DIR.glob("*/_category.json")):
        rel = cat_file.relative_to(REPO)
        data = load_json(cat_file)
        if not data:
            continue
        violations = list(category_validator.iter_errors(data))
        if violations:
            for v in violations:
                err(f"{rel}: {v.message} (at {'/'.join(map(str, v.path))})")
        else:
            ok(str(rel))

    # 2. Bundles
    print("\n== bundle files ==")
    bundle_files = sorted(p for p in BUNDLES_DIR.rglob("*.json") if p.name != "_category.json")
    if not bundle_files:
        err("no bundle files found")
        return 1

    for bundle_file in bundle_files:
        rel = bundle_file.relative_to(REPO)
        data = load_json(bundle_file)
        if not data:
            continue

        violations = list(bundle_validator.iter_errors(data))
        for v in violations:
            err(f"{rel}: {v.message} (at {'/'.join(map(str, v.path))})")
        if violations:
            continue

        # 3+4. id matches location
        expected_id = f"{bundle_file.parent.name}/{bundle_file.stem}"
        if data["id"] != expected_id:
            err(f"{rel}: id={data['id']!r} but path implies {expected_id!r}")
        if data["category"] != bundle_file.parent.name:
            err(f"{rel}: category={data['category']!r} but path category={bundle_file.parent.name!r}")

        # 5. rule_ids syntactically valid
        for rid in data["rules"]["rule_ids"]:
            if not re.fullmatch(r"R\d{3,4}", rid):
                err(f"{rel}: malformed rule_id {rid!r}")

        # 6. demo agent naming
        for agent in data.get("demo_agents", []):
            if not agent["name"].endswith("-demo"):
                err(f"{rel}: demo_agent {agent['name']!r} must end in '-demo'")

        # 7. examples dir exists
        ex_dir = EXAMPLES_DIR / data["id"]
        if not ex_dir.is_dir():
            err(f"{rel}: missing required examples/{data['id']}/ directory")
        else:
            for required in ("README.md",):
                if not (ex_dir / required).is_file():
                    err(f"examples/{data['id']}/{required} missing")

        if not violations:
            ok(str(rel))

    # Summary
    print()
    if errors:
        print(f"FAIL — {len(errors)} error(s)")
        return 1
    print(f"OK — {len(bundle_files)} bundle(s) validated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
