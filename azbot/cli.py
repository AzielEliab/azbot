"""Human CLI for AZBot. Machine output stays behind --json."""
from __future__ import annotations

import argparse
import json
import re
import sys
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

UI_URL = "http://127.0.0.1:8870/"


def _get(url: str) -> tuple[int, str]:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 AZBot-doctor"})
    try:
        with urllib.request.urlopen(req, timeout=20) as res:
            return res.status, res.read().decode("utf-8", "replace")
    except Exception as exc:  # noqa: BLE001
        return 0, str(exc)


def _plain_error(prog: str, message: str) -> str:
    bad = re.search(r"invalid choice: '([^']+)'", message)
    if bad:
        name = bad.group(1)
        if prog == "azbot":
            return f'Unknown command "{name}".\nTry: azbot ui   or   azbot --help'
        if prog.startswith("azbot skill"):
            return f'Unknown skill action "{name}".\nTry: azbot skill --help'
        return f'Unknown command "{name}".\nTry: azbot --help'
    if message.startswith("unrecognized arguments"):
        extra = message.split(":", 1)[-1].strip()
        return f"Unknown option {extra}.\nTry: {prog} --help"
    required = re.search(r"the following arguments are required: (.+)", message)
    if required:
        fields = required.group(1)
        if "name" in fields and prog.endswith(" run"):
            return "Missing skill name.\nTry: azbot skills"
        if "name" in fields and prog.endswith(" export"):
            return "Missing skill name.\nTry: azbot skills"
        if "path" in fields:
            return "Missing path to a SKILL.md file.\nTry: azbot skill import PATH"
        return f"Missing {fields}.\nTry: {prog} --help"
    return f"{message}\nTry: azbot --help"


class HumanParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        self.exit(2, _plain_error(self.prog, message) + "\n")


def _wants_json(args: argparse.Namespace) -> bool:
    return bool(getattr(args, "json", False))


def _skill_payload(skill) -> dict[str, str]:
    return {
        "name": skill.name,
        "description": skill.description,
        "source": skill.source,
        "body": skill.body,
        "slug": skill.slug,
    }


def _print_json(payload: object) -> None:
    print(json.dumps(payload, indent=2))


def cmd_welcome(args: argparse.Namespace) -> int:
    count = len(discover_skills())
    if _wants_json(args):
        _print_json({
            "ok": True,
            "name": "azbot",
            "version": __version__,
            "author": "Aziel Eliab",
            "skills": count,
            "ui": UI_URL,
            "openapi": OPENAPI,
            "mcp": MCP,
        })
        return 0
    print("AZBot lists skill files on this computer and opens a local page for the catalog links.")
    print()
    print(f"Skills found: {count}")
    print()
    print("Next:")
    print(f"  azbot ui        Open {UI_URL}")
    print("  azbot skills    List skill files")
    print("  azbot doctor    Check the catalog")
    print("  azbot --help    Show commands")
    print()
    print("Author: Aziel Eliab")
    return 0


def cmd_skill(args: argparse.Namespace) -> int:
    action = getattr(args, "skill_cmd", None)
    as_json = _wants_json(args)
    if action is None:
        text = skill_text()
        if as_json:
            _print_json({"ok": True, "format": "markdown", "body": text})
        else:
            print(text)
        return 0
    if action == "run":
        try:
            skill = get_skill(args.name)
        except KeyError:
            if as_json:
                _print_json({"error": "skill not found"})
            else:
                print(f'Skill "{args.name}" was not found.\nTry: azbot skills', file=sys.stderr)
            return 2
        if as_json:
            _print_json(_skill_payload(skill))
        else:
            print(skill.body)
        return 0
    if action == "import":
        path = Path(args.path)
        if not path.is_file():
            if as_json:
                _print_json({"ok": False, "error": "file required"})
            else:
                print(f"No file at {args.path}.\nTry: azbot skill import PATH", file=sys.stderr)
            return 2
        try:
            imported = import_skill(path)
        except (OSError, ValueError) as exc:
            if as_json:
                _print_json({"ok": False, "error": str(exc)})
            else:
                print(f"{exc}\nTry: azbot skill import PATH", file=sys.stderr)
            return 2
        if as_json:
            _print_json({
                "ok": True,
                "name": imported.name,
                "slug": imported.slug,
                "path": str(imported.path),
                "description": imported.description,
            })
        else:
            print(f"Added skill {imported.name}.")
            print(f"Saved to {imported.path}.")
            print("Next: azbot skills")
        return 0
    if action == "export":
        dest = Path(args.out) if getattr(args, "out", None) else None
        try:
            result = export_skill(args.name, dest=dest)
        except KeyError:
            if as_json:
                _print_json({"error": "skill not found"})
            else:
                print(f'Skill "{args.name}" was not found.\nTry: azbot skills', file=sys.stderr)
            return 2
        if as_json:
            if dest is None:
                skill = get_skill(args.name)
                _print_json(_skill_payload(skill))
            else:
                _print_json({"ok": True, "path": str(result), "name": args.name})
        else:
            print(result)
        return 0
    print(f'Unknown skill action "{action}".\nTry: azbot skill --help', file=sys.stderr)
    return 2


def cmd_skills(args: argparse.Namespace) -> int:
    rows = skills_as_dicts()
    if _wants_json(args):
        _print_json(rows)
        return 0
    if not rows:
        print("No skill files found.")
        print("Next: azbot skill import PATH")
        return 0
    width = max(len(r["name"]) for r in rows)
    for row in rows:
        print(f"{row['name']:<{width}}  {row['description']}")
    print()
    print("Next: azbot skill run NAME")
    return 0


def _doctor_report() -> tuple[dict[str, object], str]:
    code, body = _get(CATALOG + "/v1/health")
    ok = code == 200 and "ok" in body.lower()
    payload: dict[str, object] = {
        "ok": ok,
        "catalog_health_status": code,
        "openapi": OPENAPI,
        "mcp": MCP,
        "limitation": LIMITATION,
        "version": __version__,
        "skills": len(discover_skills()),
    }
    return payload, body


def cmd_doctor(args: argparse.Namespace) -> int:
    payload, body = _doctor_report()
    ok = bool(payload["ok"])
    if _wants_json(args):
        _print_json(payload)
        return 0 if ok else 1
    status = int(payload["catalog_health_status"])  # type: ignore[arg-type]
    if ok:
        print("Catalog: answered")
        print(f"Health: HTTP {status}")
    else:
        print("Catalog: no clear answer")
        if status:
            print(f"Health: HTTP {status}")
        else:
            print("Health: the catalog did not answer")
            reason = body.splitlines()[0].strip() if body else ""
            if reason:
                print(f"Reason: {reason}")
    print(f"Skills on this machine: {payload['skills']}")
    print(f"OpenAPI: {payload['openapi']}")
    print(f"MCP: {payload['mcp']}")
    print()
    if ok:
        print("Next: azbot ui")
    else:
        print("Next: check the network, then run azbot doctor again.")
    return 0 if ok else 1


def cmd_ui(_: argparse.Namespace) -> int:
    serve()
    return 0


def _build_parser() -> HumanParser:
    json_flag = argparse.ArgumentParser(add_help=False)
    json_flag.add_argument("--json", action="store_true", help="Print JSON for scripts")

    p = HumanParser(
        prog="azbot",
        parents=[json_flag],
        usage="%(prog)s [--json] <command> [<args>]",
        description="List skill files on this computer and open the local catalog page.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""Examples:
  azbot
  azbot ui
  azbot skills
  azbot doctor
  azbot doctor --json

More:
  azbot skill run NAME
  azbot skill import PATH
  azbot skill export NAME --out FILE

The local page is {UI_URL}
Author: Aziel Eliab
""",
    )
    p.add_argument("--version", action="version", version=f"azbot {__version__}")
    sub = p.add_subparsers(dest="cmd", metavar="<command>")

    skill_p = sub.add_parser(
        "skill",
        parents=[json_flag],
        help="Print the bundled skill, or run, import, or export one",
        description="Print the bundled skill, or run, import, or export one skill file.",
    )
    skill_p.set_defaults(fn=cmd_skill)
    skill_sub = skill_p.add_subparsers(dest="skill_cmd", metavar="<action>")

    run_p = skill_sub.add_parser(
        "run",
        parents=[json_flag],
        help="Print one skill file",
        description="Print one skill file from this computer.",
    )
    run_p.add_argument("name", help="Skill name")

    imp_p = skill_sub.add_parser(
        "import",
        parents=[json_flag],
        help="Copy a SKILL.md into skills/<slug>/",
        description="Copy a SKILL.md into skills/<slug>/.",
    )
    imp_p.add_argument("path", help="Path to a SKILL.md file")

    exp_p = skill_sub.add_parser(
        "export",
        parents=[json_flag],
        help="Write a skill as markdown",
        description="Write a skill as markdown. Prints the file when --out is omitted.",
    )
    exp_p.add_argument("name", help="Skill name")
    exp_p.add_argument("--out", help="Destination file (default: print the skill)")

    sub.add_parser(
        "skills",
        parents=[json_flag],
        help="List skill files on this computer",
        description="List skill files on this computer (name and description).",
    ).set_defaults(fn=cmd_skills)
    sub.add_parser(
        "doctor",
        parents=[json_flag],
        help="Check whether the catalog answers",
        description="Check whether the aziel-runtime catalog answers /v1/health.",
    ).set_defaults(fn=cmd_doctor)
    sub.add_parser(
        "ui",
        parents=[json_flag],
        help="Open the local page at 127.0.0.1:8870",
        description=f"Serve the local page. Open {UI_URL}",
    ).set_defaults(fn=cmd_ui)
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    if getattr(args, "cmd", None) is None:
        return cmd_welcome(args)
    return int(args.fn(args))


if __name__ == "__main__":
    raise SystemExit(main())
