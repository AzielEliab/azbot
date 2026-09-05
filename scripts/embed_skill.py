#!/usr/bin/env python3
"""Copy azbot/SKILL.md to root + Worker embed. Author Aziel Eliab."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "azbot" / "SKILL.md"
ROOT_SKILL = ROOT / "SKILL.md"
EMBED = ROOT / "workers" / "download-tracker" / "src" / "skill-embed.js"


def main() -> int:
    text = SRC.read_text(encoding="utf-8")
    if not text.endswith("\n"):
        text += "\n"
    ROOT_SKILL.write_text(text, encoding="utf-8")
    EMBED.parent.mkdir(parents=True, exist_ok=True)
    EMBED.write_text(
        "/** Generated from azbot/SKILL.md — do not edit by hand. */\n"
        f"export const SKILL = {json.dumps(text)};\n",
        encoding="utf-8",
    )
    print(f"wrote {ROOT_SKILL}")
    print(f"wrote {EMBED}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
