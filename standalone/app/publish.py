#!/usr/bin/env python3
"""Official-API publish adapters. Tokens from env only. Never stores passwords.

AZBOT_PUBLISH=1 required to hit the network.
AZBOT_X_BEARER = user-context bearer for X API v2.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


def _require_publish() -> None:
    if os.environ.get("AZBOT_PUBLISH") != "1":
        raise RuntimeError("publish gated: set AZBOT_PUBLISH=1 to allow network post")


def post_x_tweet(text: str) -> dict:
    _require_publish()
    token = os.environ.get("AZBOT_X_BEARER", "").strip()
    if not token:
        raise RuntimeError("AZBOT_X_BEARER missing")
    if len(text) > 25000:
        raise RuntimeError("text too long")
    req = urllib.request.Request(
        "https://api.x.com/2/tweets",
        data=json.dumps({"text": text}).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "AZbotLocal/1.3",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        raise RuntimeError(f"X API {e.code}: {body[:500]}") from e


def reply_x(text: str, in_reply_to: str) -> dict:
    _require_publish()
    token = os.environ.get("AZBOT_X_BEARER", "").strip()
    if not token:
        raise RuntimeError("AZBOT_X_BEARER missing")
    payload = {"text": text, "reply": {"in_reply_to_tweet_id": str(in_reply_to)}}
    req = urllib.request.Request(
        "https://api.x.com/2/tweets",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "AZbotLocal/1.3",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        raise RuntimeError(f"X API {e.code}: {body[:500]}") from e


def draft_only(action: str, payload: dict, queue_dir: Path) -> Path:
    queue_dir.mkdir(parents=True, exist_ok=True)
    n = len(list(queue_dir.glob("*.json"))) + 1
    path = queue_dir / f"{n:04d}-{action}.json"
    rec = {"action": action, "payload": payload, "status": "draft"}
    path.write_text(json.dumps(rec, indent=2) + "\n", encoding="utf-8")
    return path


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: publish.py draft-x TEXT | post-x TEXT | reply-x ID TEXT")
        return 2
    cmd = argv[1]
    root = Path(__file__).resolve().parent.parent
    queue = root / "queue"
    if cmd == "draft-x":
        text = " ".join(argv[2:])
        print(draft_only("x.post", {"text": text}, queue))
        return 0
    if cmd == "post-x":
        text = " ".join(argv[2:])
        print(json.dumps(post_x_tweet(text), indent=2))
        return 0
    if cmd == "reply-x":
        print(json.dumps(reply_x(" ".join(argv[3:]), argv[2]), indent=2))
        return 0
    print("unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
