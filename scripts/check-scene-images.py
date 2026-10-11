#!/usr/bin/env python3
"""Validate scene image assignments; standard library only, no paid services."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / "data" / "scene-images.json").read_text(encoding="utf-8"))
seen_ids, seen_pages, seen_files, seen_hashes = set(), set(), set(), {}
errors = []
for item in data["images"]:
    ident, page, filename = (item[k] for k in ("id", "page", "file"))
    for key, value, seen in (("id", ident, seen_ids), ("page", page, seen_pages), ("file", filename, seen_files)):
        if value in seen:
            errors.append(f"duplicate {key}: {value}")
        seen.add(value)
    path = ROOT / filename
    if item.get("status") == "published":
        if not path.is_file():
            errors.append(f"published image missing: {filename}")
        else:
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if digest in seen_hashes:
                errors.append(f"identical image content: {filename} and {seen_hashes[digest]}")
            seen_hashes[digest] = filename
print(f"Checked {len(data['images'])} image assignments: {len(errors)} error(s)")
for error in errors:
    print("ERROR:", error)
raise SystemExit(bool(errors))
