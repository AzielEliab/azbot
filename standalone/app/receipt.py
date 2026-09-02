#!/usr/bin/env python3
"""Write a SHA-256 receipt next to a file. Narrative-free."""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_receipt(path: Path) -> Path:
    path = path.expanduser().resolve()
    digest = sha256_file(path)
    rec = {
        "file": path.name,
        "sha256": digest,
        "bytes": path.stat().st_size,
        "recorded_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "note": "hash of this copy only",
    }
    out = path.with_suffix(path.suffix + ".receipt.json")
    out.write_text(json.dumps(rec, indent=2) + "\n", encoding="utf-8")
    return out


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: receipt.py <file> [more files...]")
        return 2
    for raw in argv[1:]:
        p = write_receipt(Path(raw))
        print(p)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
