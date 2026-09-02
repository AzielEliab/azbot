from __future__ import annotations

import argparse
import json
import urllib.request
from pathlib import Path

from azbot import CATALOG, LIMITATION, MCP, OPENAPI, __version__, skill_text
from azbot.skills_loader import (
    discover_skills,
    export_skill,
    get_skill,
    import_skill,
    skills_as_dicts,
)
from azbot.ui import serve


def _get(url: str) -> tuple[int, str]:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 AZBot-doctor"})
    try:
        with urllib.request.urlopen(req, timeout=20) as res:
            return res.status, res.read().decode("utf-8", "replace")
    except Exception as exc:  # noqa: BLE001
        return 0, str(exc)


def cmd_skill(args: argparse.Namespace) -> int:
    action = getattr(args, "skill_cmd", None)
    if action is None:
        print(skill_text())
        return 0
    if action == "run":
        skill = get_skill(args.name)
        print(skill.body)
        return 0
    if action == "import":
        imported = import_skill(Path(args.path))
        print(json.dumps({
            "ok": True,
            "name": imported.name,
            "slug": imported.slug,
            "path": str(imported.path),
            "description": imported.description,
        }, indent=2))
        return 0
    if action == "export":
        dest = Path(args.out) if getattr(args, "out", None) else None
        result = export_skill(args.name, dest=dest)
        if dest is None:
            print(result)
        else:
            print(result)
        return 0
    print("unknown skill action", file=__import__("sys").stderr)
    return 2


def cmd_skills(_: argparse.Namespace) -> int:
    rows = skills_as_dicts()
    if not rows:
        print("No SKILL.md files found.")
        return 0
    width = max(len(r["name"]) for r in rows)
    for row in rows:
        print(f"{row['name']:<{width}}  {row['description']}")
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
        "skills": len(discover_skills()),
    }, indent=2))
    return 0 if ok else 1


def cmd_ui(_: argparse.Namespace) -> int:
    serve()
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="azbot",
        description=(
            "AZBot skill runner. Not a model and not Grok weights. "
            "Prints skills, checks the catalog, or serves a local UI."
        ),
    )
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="cmd", required=True)

    skill_p = sub.add_parser("skill", help="Print catalog SKILL.md, or run/import/export a skill")
    skill_p.set_defaults(fn=cmd_skill)
    skill_sub = skill_p.add_subparsers(dest="skill_cmd")

    run_p = skill_sub.add_parser("run", help="Print a discovered skill body (local operator; not Grok weights)")
    run_p.add_argument("name")

    imp_p = skill_sub.add_parser("import", help="Copy a SKILL.md into skills/<slug>/")
    imp_p.add_argument("path")

    exp_p = skill_sub.add_parser("export", help="Write a skill as markdown")
    exp_p.add_argument("name")
    exp_p.add_argument("--out", help="Destination file (default: stdout)")

    sub.add_parser("skills", help="List discovered skills (name + description)").set_defaults(fn=cmd_skills)
    sub.add_parser("doctor", help="Ping aziel-runtime /v1/health").set_defaults(fn=cmd_doctor)
    sub.add_parser("ui", help="Loopback UI at 127.0.0.1:8870").set_defaults(fn=cmd_ui)
    args = p.parse_args(argv)
    return int(args.fn(args))


if __name__ == "__main__":
    raise SystemExit(main())
