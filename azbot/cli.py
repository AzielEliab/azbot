"""Human CLI for AZBot. Machine output stays behind --json."""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path

from azbot import CATALOG, LIMITATION, MCP, OPENAPI, __version__, skill_text
from azbot.collab import (
    LatticeMismatch,
    SessionStore,
    fraggate_transport,
    handoff,
    lock_report,
    mesh_get,
    mesh_post,
    open_session,
    rewrite,
)
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
    print("  azbot doctor    Check the catalog and the local locks")
    print("  azbot mesh      Show the mesh gate (GET never enables)")
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
    catalog_ok = code == 200 and "ok" in body.lower()
    locks = lock_report()
    payload: dict[str, object] = {
        "ok": catalog_ok and bool(locks["ok"]),
        "catalog_health_status": code,
        "openapi": OPENAPI,
        "mcp": MCP,
        "limitation": LIMITATION,
        "version": __version__,
        "skills": len(discover_skills()),
        "locks": locks,
    }
    return payload, body


def _print_locks(locks: dict) -> None:
    print("Bind: 127.0.0.1")
    if locks.get("remain_off_1"):
        print("Remain-OFF #1: GET /v1/mesh never enables")
    else:
        print("Remain-OFF #1: failed")
    print(f"Empty POST: {locks.get('empty_post')}")
    if locks.get("tip_unchanged") and locks.get("tip_rewrite") is False:
        print("Tip share: read only")
    else:
        print("Tip share: rewrite check failed")
    print("Cap-7: names-only")
    tip = str(locks.get("tip") or "")
    if tip:
        print(f"Tip: {tip}")


def cmd_doctor(args: argparse.Namespace) -> int:
    payload, body = _doctor_report()
    ok = bool(payload["ok"])
    locks = payload["locks"]
    if _wants_json(args):
        _print_json(payload)
        return 0 if ok else 1
    status = int(payload["catalog_health_status"])  # type: ignore[arg-type]
    catalog_ok = status == 200 and "ok" in body.lower()
    if catalog_ok:
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
    if isinstance(locks, dict):
        _print_locks(locks)
    print()
    if ok:
        print("Next: azbot ui")
    elif not catalog_ok:
        print("Next: check the network, then run azbot doctor again.")
    else:
        print("Next: locks failed. Run azbot doctor --json.")
    return 0 if ok else 1


def _session_dir(args: argparse.Namespace) -> Path:
    raw = getattr(args, "dir", None)
    return Path(raw) if raw else Path.cwd() / ".azbot"


def cmd_mesh(args: argparse.Namespace) -> int:
    action = getattr(args, "mesh_cmd", None) or "get"
    if action == "post":
        payload = mesh_post({}, bearer=getattr(args, "bearer", "") or "")
    else:
        payload = mesh_get()
    if _wants_json(args):
        _print_json(payload)
        return 0 if payload.get("code") != "MESH-NEED-QNM-NODE" else 1
    if action == "post":
        print(f"Code: {payload['code']}")
        print(f"Enabled: {str(payload['enabled']).lower()}")
        print("Radios: off")
    else:
        print("Mesh: off")
        print("Remain-OFF #1: GET /v1/mesh never enables")
        print("Bind: 127.0.0.1")
        print("Cap-7: names-only")
    if payload.get("code") == "MESH-NEED-BEARER":
        print("Next: pass a bearer only with a local qnm-node. GET still never enables.")
    return 0


def cmd_session(args: argparse.Namespace) -> int:
    action = getattr(args, "session_cmd", None)
    as_json = _wants_json(args)
    if action not in {"open", "handoff", "tip", "rewrite"}:
        if as_json:
            _print_json({"ok": False, "error": "missing session action"})
        else:
            print("Missing session action.\nTry: azbot session --help", file=sys.stderr)
        return 2
    store = SessionStore(_session_dir(args))
    if action == "open":
        parties = list(getattr(args, "party", None) or [])
        try:
            session = open_session(parties)
        except ValueError as exc:
            if as_json:
                _print_json({"ok": False, "error": str(exc)})
            else:
                print(f"{exc}\nTry: azbot session open --party human-a --party human-b", file=sys.stderr)
            return 2
        store.save(session)
        view = session.party_view()
        if as_json:
            _print_json({"ok": True, **view, "path": str(store.path)})
        else:
            print(f"Session: {session.session_id}")
            print(f"Parties: {', '.join(session.parties)}")
            print(f"Saved: {store.path}")
            print("Next: azbot session handoff --slug SLUG --op OP")
        return 0
    try:
        session = store.load()
    except (OSError, json.JSONDecodeError, LatticeMismatch) as exc:
        if as_json:
            _print_json({"ok": False, "code": "TIP-NO-REWRITE", "error": str(exc)})
        else:
            print("Session file does not verify.\nRefusing to rewrite it.", file=sys.stderr)
        return 2
    if session is None:
        if as_json:
            _print_json({"ok": False, "error": "no session"})
        else:
            print("No session on this machine.\nTry: azbot session open --party human-a --party human-b", file=sys.stderr)
        return 2
    if action == "tip":
        view = session.party_view()
        if as_json:
            _print_json(view)
        else:
            print(f"Tip: {view['tip'] or '(none)'}")
            print("Rewrite: refused")
            print(f"Parties: {', '.join(view['parties'])}")
        return 0
    if action == "rewrite":
        result = rewrite(session, 0, {"forged": True})
        if as_json:
            _print_json(result)
        else:
            print(f"Code: {result['code']}")
            print(f"Tip: {result['tip']}")
            print("Tip unchanged.")
        return 0
    try:
        payload = json.loads(getattr(args, "payload", None) or "{}")
    except json.JSONDecodeError:
        if as_json:
            _print_json({"ok": False, "error": "payload must be JSON"})
        else:
            print("Payload must be a JSON object.\nTry: --payload '{}'", file=sys.stderr)
        return 2
    if not isinstance(payload, dict):
        if as_json:
            _print_json({"ok": False, "error": "payload must be a JSON object"})
        else:
            print("Payload must be a JSON object.\nTry: --payload '{}'", file=sys.stderr)
        return 2
    transport = fraggate_transport if getattr(args, "call", False) else None
    result = handoff(session, args.slug, args.op, payload, transport)
    store.save(session)
    if as_json:
        _print_json({
            "ok": result["ok"],
            "executed": result["executed"],
            "code": result["code"],
            "tip": result["tip"],
            "transport_called": result["transport_called"],
            "call": result["call"],
            "party_view": result["party_view"],
        })
    else:
        print(f"Code: {result['code']}")
        print(f"Executed: {str(result['executed']).lower()}")
        print(f"Tip: {result['tip']}")
        if result["transport_called"]:
            print("Door: FragGate")
        else:
            print("Door: packaged locally. Engine not called.")
        print("Rewrite: refused")
    if result["code"] in {"AZOS-REFUSED", "REFUSED", "FG-STUB", "ROLLBACK-REFUSED", "AZOS-NEED-ARC"}:
        return 2
    if getattr(args, "call", False) and not result["executed"]:
        return 1
    return 0


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
  azbot mesh
  azbot mesh post
  azbot session open --party human-a --party human-b

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
        help="Check the catalog and the local locks",
        description="Check catalog /v1/health, Remain-OFF #1, and tip-share-no-rewrite.",
    ).set_defaults(fn=cmd_doctor)

    mesh_p = sub.add_parser(
        "mesh",
        parents=[json_flag],
        help="Show the local mesh gate",
        description="GET never enables. Empty POST returns MESH-NEED-BEARER.",
    )
    mesh_p.set_defaults(fn=cmd_mesh, mesh_cmd="get")
    mesh_sub = mesh_p.add_subparsers(dest="mesh_cmd", metavar="<action>")
    mesh_sub.add_parser("get", parents=[json_flag], help="Read mesh status. Does not enable.").set_defaults(fn=cmd_mesh)
    mesh_post_p = mesh_sub.add_parser("post", parents=[json_flag], help="Empty POST unless --bearer is set.")
    mesh_post_p.add_argument("--bearer", default="", help="Operator bearer. Not written to disk.")
    mesh_post_p.set_defaults(fn=cmd_mesh)

    session_p = sub.add_parser(
        "session",
        parents=[json_flag],
        help="Multi-party session. Parties read the tip.",
        description="Local session on 127.0.0.1. Handoff packages a FragGate call. The tip is not rewritten.",
    )
    session_p.set_defaults(fn=cmd_session)
    session_sub = session_p.add_subparsers(dest="session_cmd", metavar="<action>")
    open_p = session_sub.add_parser("open", parents=[json_flag], help="Open a session for two or more parties")
    open_p.add_argument("--dir", help="Session directory (default: .azbot in the current directory)")
    open_p.add_argument("--party", action="append", default=[], help="Party label. Repeat for each party.")
    hand_p = session_sub.add_parser("handoff", parents=[json_flag], help="Package slug + op + payload")
    hand_p.add_argument("--slug", required=True)
    hand_p.add_argument("--op", required=True)
    hand_p.add_argument("--payload", default="{}", help="JSON object")
    hand_p.add_argument("--call", action="store_true", help="POST the package to FragGate")
    hand_p.add_argument("--dir", help="Session directory (default: .azbot in the current directory)")
    tip_p = session_sub.add_parser("tip", parents=[json_flag], help="Print the tip. No payload.")
    tip_p.add_argument("--dir", help="Session directory (default: .azbot in the current directory)")
    rewrite_p = session_sub.add_parser("rewrite", parents=[json_flag], help="Show that rewrite is refused")
    rewrite_p.add_argument("--dir", help="Session directory (default: .azbot in the current directory)")
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
