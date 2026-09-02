from __future__ import annotations

import argparse
import json
import urllib.request

from azbot import CATALOG, LIMITATION, MCP, OPENAPI, __version__, skill_text
from azbot.ui import serve


def _get(url: str) -> tuple[int, str]:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 AZBot-doctor"})
    try:
        with urllib.request.urlopen(req, timeout=20) as res:
            return res.status, res.read().decode("utf-8", "replace")
    except Exception as exc:  # noqa: BLE001
        return 0, str(exc)


def cmd_skill(_: argparse.Namespace) -> int:
    print(skill_text())
    return 0


def cmd_doctor(_: argparse.Namespace) -> int:
    code, body = _get(CATALOG + "/v1/health")
    ok = code == 200 and "ok" in body.lower()
    print(json.dumps({
        "ok": ok,
        "catalog_health_status": code,
        "openapi": OPENAPI,
        "mcp": MCP,
        "limitation": LIMITATION,
        "version": __version__,
    }, indent=2))
    return 0 if ok else 1


def cmd_ui(_: argparse.Namespace) -> int:
    serve()
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="azbot",
        description="AZBot skill. Not a model. Prints the skill, checks the catalog, or serves a local UI.",
    )
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("skill", help="Print SKILL.md").set_defaults(fn=cmd_skill)
    sub.add_parser("doctor", help="Ping aziel-runtime /v1/health").set_defaults(fn=cmd_doctor)
    sub.add_parser("ui", help="Loopback UI at 127.0.0.1:8870").set_defaults(fn=cmd_ui)
    args = p.parse_args(argv)
    return int(args.fn(args))


if __name__ == "__main__":
    raise SystemExit(main())
