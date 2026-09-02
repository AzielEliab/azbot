#!/usr/bin/env python3
"""Local autonomous runner. Executes queued task files. Default is draft-only.

Task JSON:
{
  "action": "export.findings" | "x.post" | "x.reply" | "echo",
  "payload": {...},
  "publish": false
}

x.* only hits the network when publish=true AND AZBOT_PUBLISH=1 AND bearer is set.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from export_findings import bundle
from publish import post_x_tweet, reply_x


def run_task(path: Path, out_dir: Path) -> dict:
    spec = json.loads(path.read_text(encoding="utf-8"))
    action = spec.get("action")
    payload = spec.get("payload") or {}
    publish = bool(spec.get("publish"))
    if action == "echo":
        result = {"echo": payload}
    elif action == "export.findings":
        rows = payload.get("rows") or []
        points = payload.get("points")
        pts = [tuple(p) for p in points] if points else None
        result = bundle(payload.get("name") or path.stem, rows, out_dir, pts)
    elif action == "x.post":
        if not publish:
            result = {"status": "draft", "text": payload.get("text")}
        else:
            result = post_x_tweet(payload.get("text") or "")
    elif action == "x.reply":
        if not publish:
            result = {"status": "draft", "text": payload.get("text"), "in_reply_to": payload.get("in_reply_to")}
        else:
            result = reply_x(payload.get("text") or "", str(payload.get("in_reply_to")))
    else:
        raise RuntimeError(f"unknown action: {action}")
    spec["last_result"] = result
    spec["status"] = "ran"
    path.write_text(json.dumps(spec, indent=2) + "\n", encoding="utf-8")
    return {"task": str(path), "action": action, "result": result}


def main(argv: list[str]) -> int:
    root = Path(__file__).resolve().parent.parent
    queue = Path(argv[1]) if len(argv) > 1 else root / "queue"
    out = root / "out"
    if not queue.exists():
        print(json.dumps({"ok": True, "ran": 0, "note": "empty queue"}))
        return 0
    ran = []
    for path in sorted(queue.glob("*.json")):
        spec = json.loads(path.read_text(encoding="utf-8"))
        if spec.get("status") == "ran" and not spec.get("repeat"):
            continue
        ran.append(run_task(path, out))
    print(json.dumps({"ok": True, "ran": len(ran), "results": ran}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
