#!/usr/bin/env python3
"""
Regenerate manifest.json from the current bundle tree.

Run: python3 tools/gen-manifest.py
Writes manifest.json at the repo root. CI runs this on every merge to main.
"""

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BUNDLES_DIR = REPO / "bundles"
EXAMPLES_DIR = REPO / "examples"
MANIFEST_PATH = REPO / "manifest.json"


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def next_manifest_version() -> str:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    counter = 1
    if MANIFEST_PATH.exists():
        try:
            existing = json.loads(MANIFEST_PATH.read_text())
            prev = existing.get("manifest_version", "")
            if prev.startswith(today):
                counter = int(prev.rsplit(".", 1)[1]) + 1
        except (json.JSONDecodeError, ValueError, IndexError):
            pass
    return f"{today}.{counter}"


def main() -> int:
    bundle_files = sorted(p for p in BUNDLES_DIR.rglob("*.json") if p.name != "_category.json")
    bundles = []
    for bf in bundle_files:
        try:
            data = json.loads(bf.read_text())
        except json.JSONDecodeError as e:
            print(f"skipping {bf}: {e}", file=sys.stderr)
            continue
        bundles.append({
            "id": data["id"],
            "version": data["version"],
            "status": data["status"],
            "category": data["category"],
            "path": str(bf.relative_to(REPO)),
            "sha256": sha256_of(bf),
            "has_example": (EXAMPLES_DIR / data["id"]).is_dir(),
        })

    manifest = {
        "schema_version": "1.1",
        "manifest_version": next_manifest_version(),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "bundles": bundles,
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"wrote manifest.json with {len(bundles)} bundle(s) - version {manifest['manifest_version']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
