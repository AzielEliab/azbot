#!/usr/bin/env python3
"""Local-only AZbot shell. Binds to 127.0.0.1. Does not upload."""
from __future__ import annotations

import json
import posixpath
import sys
import tempfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

APP_DIR = Path(__file__).resolve().parent
ROOT = APP_DIR.parent
REPO = ROOT.parent
STATIC = APP_DIR / "static"
OUT = ROOT / "out"
UPLOADS = ROOT / "work"

sys.path.insert(0, str(REPO))
sys.path.insert(0, str(APP_DIR))
from receipt import write_receipt  # noqa: E402
from sanitize import sanitize_file  # noqa: E402

try:
    from azbot.skills_loader import get_skill, import_skill, skills_as_dicts
except ImportError:  # pragma: no cover
    get_skill = None  # type: ignore[assignment]
    import_skill = None  # type: ignore[assignment]
    skills_as_dicts = None  # type: ignore[assignment]


class Handler(BaseHTTPRequestHandler):
    server_version = "AZbotLocal/0.2.0"

    def log_message(self, fmt: str, *args) -> None:
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    def _send(self, code: int, body: bytes, ctype: str, extra: dict[str, str] | None = None) -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        if extra:
            for k, v in extra.items():
                self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path in ("/", "/index.html"):
            data = (STATIC / "index.html").read_bytes()
            self._send(200, data, "text/html; charset=utf-8")
            return
        if path == "/health":
            self._send(200, b'{"ok":true,"bind":"127.0.0.1","version":"0.2.0"}', "application/json")
            return
        if path == "/api/skills":
            if skills_as_dicts is None:
                self._send(500, b'{"error":"skills loader missing"}', "application/json")
                return
            body = json.dumps(skills_as_dicts(REPO), indent=2).encode()
            self._send(200, body, "application/json; charset=utf-8")
            return
        if path.startswith("/api/skills/") and path.endswith("/export"):
            if get_skill is None:
                self._send(500, b'{"error":"skills loader missing"}', "application/json")
                return
            name = unquote(path[len("/api/skills/"):-len("/export")].strip("/"))
            try:
                skill = get_skill(name, root=REPO)
            except KeyError:
                self._send(404, b'{"error":"skill not found"}', "application/json")
                return
            extra = {"Content-Disposition": f'attachment; filename="{skill.slug}.md"'}
            self._send(200, skill.body.encode("utf-8"), "text/markdown; charset=utf-8", extra)
            return
        if path.startswith("/api/skills/") and path != "/api/skills/":
            if get_skill is None:
                self._send(500, b'{"error":"skills loader missing"}', "application/json")
                return
            name = unquote(path[len("/api/skills/"):].strip("/"))
            if name:
                try:
                    skill = get_skill(name, root=REPO)
                except KeyError:
                    self._send(404, b'{"error":"skill not found"}', "application/json")
                    return
                payload = {
                    "name": skill.name,
                    "description": skill.description,
                    "source": skill.source,
                    "body": skill.body,
                    "slug": skill.slug,
                }
                self._send(200, json.dumps(payload, indent=2).encode(), "application/json; charset=utf-8")
                return
        self._send(404, b"not found", "text/plain")

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        if path == "/api/skills/import":
            self._handle_skill_import()
            return
        if path not in ("/prep", "/ark/seal", "/ark/phoenix"):
            self._send(404, b"not found", "text/plain")
            return
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length)
        boundary = _boundary(self.headers.get("Content-Type", ""))
        if not boundary:
            self._send(400, b'{"error":"multipart required"}', "application/json")
            return
        files, fields = _parse_multipart(raw, boundary)
        UPLOADS.mkdir(parents=True, exist_ok=True)
        OUT.mkdir(parents=True, exist_ok=True)
        try:
            if path == "/prep":
                payload = _handle_prep(files)
            elif path == "/ark/seal":
                payload = _handle_ark_seal(files, fields)
            else:
                payload = _handle_ark_phoenix(files, fields)
        except Exception as exc:
            self._send(400, json.dumps({"ok": False, "error": str(exc)}).encode(), "application/json")
            return
        self._send(200, json.dumps({"ok": True, **payload}, indent=2).encode(), "application/json")

    def _handle_skill_import(self) -> None:
        if import_skill is None:
            self._send(500, b'{"error":"skills loader missing"}', "application/json")
            return
        length = int(self.headers.get("Content-Length", "0") or 0)
        if length <= 0 or length > 2 * 1024 * 1024:
            self._send(400, b'{"ok":false,"error":"file required"}', "application/json")
            return
        raw = self.rfile.read(length)
        files, _fields = _parse_multipart(raw, _boundary(self.headers.get("Content-Type", "")))
        if not files:
            self._send(400, b'{"ok":false,"error":"SKILL.md file required"}', "application/json")
            return
        name, blob = files[0]
        safe = posixpath.basename(name) or "SKILL.md"
        try:
            with tempfile.TemporaryDirectory() as tmp:
                incoming = Path(tmp) / safe
                incoming.write_bytes(blob)
                imported = import_skill(incoming, root=REPO)
            payload = {
                "ok": True,
                "name": imported.name,
                "description": imported.description,
                "slug": imported.slug,
                "path": str(imported.path),
            }
            self._send(200, json.dumps(payload, indent=2).encode(), "application/json")
        except Exception as exc:
            self._send(400, json.dumps({"ok": False, "error": str(exc)}).encode(), "application/json")


def _boundary(ctype: str) -> bytes | None:
    if "boundary=" not in ctype:
        return None
    return ctype.split("boundary=", 1)[1].strip().encode()


def _parse_multipart(raw: bytes, boundary: bytes | None) -> tuple[list[tuple[str, bytes]], dict[str, str]]:
    files: list[tuple[str, bytes]] = []
    fields: dict[str, str] = {}
    if not boundary:
        return files, fields
    parts = raw.split(b"--" + boundary)
    for part in parts:
        if not part or part in (b"--", b"--\r\n"):
            continue
        if b"\r\n\r\n" not in part:
            continue
        header, body = part.split(b"\r\n\r\n", 1)
        if body.endswith(b"\r\n"):
            body = body[:-2]
        header_s = header.decode("utf-8", "replace")
        filename = None
        field = None
        for line in header_s.split("\r\n"):
            if "filename=" in line:
                filename = line.split("filename=", 1)[1].strip().strip('"')
            if "name=" in line and "filename=" not in line:
                field = line.split("name=", 1)[1].strip().strip('"').split(";")[0].strip().strip('"')
            if "name=" in line and "filename=" in line:
                field = None
        if filename is not None:
            files.append((filename or "file.bin", body))
        elif field:
            fields[field] = body.decode("utf-8", "replace")
    return files, fields


def _handle_prep(files: list[tuple[str, bytes]]) -> dict:
    results = []
    for name, blob in files:
        safe = posixpath.basename(name) or "file.bin"
        incoming = UPLOADS / safe
        incoming.write_bytes(blob)
        info = sanitize_file(incoming, OUT)
        rec = write_receipt(Path(info["clean"]))
        results.append(
            {
                "original_name": safe,
                "clean": info["clean"],
                "method": info["method"],
                "bytes": info["bytes"],
                "receipt": str(rec),
            }
        )
    return {"results": results}


def _handle_ark_seal(files: list[tuple[str, bytes]], fields: dict[str, str]) -> dict:
    from ark import seal

    pw = fields.get("pass") or fields.get("pw") or ""
    if not pw:
        raise ValueError("pass required")
    results = []
    for name, blob in files:
        safe = posixpath.basename(name) or "file.bin"
        incoming = UPLOADS / safe
        incoming.write_bytes(blob)
        dest = OUT / (safe + ".ark")
        results.append(seal(incoming, dest, pw))
    return {"results": results}


def _handle_ark_phoenix(files: list[tuple[str, bytes]], fields: dict[str, str]) -> dict:
    from ark import phoenix

    pw = fields.get("pass") or fields.get("pw") or ""
    if not pw:
        raise ValueError("pass required")
    results = []
    for name, blob in files:
        safe = posixpath.basename(name) or "file.bin"
        incoming = UPLOADS / safe
        incoming.write_bytes(blob)
        dest = OUT / safe
        dest.write_bytes(incoming.read_bytes())
        extract = OUT / (safe + ".extracted")
        results.append(phoenix(dest, pw, extract))
    return {"results": results}


def main() -> None:
    host, port = "127.0.0.1", 7747
    httpd = ThreadingHTTPServer((host, port), Handler)
    print(f"AZbot local shell  http://{host}:{port}")
    print("Slingshot Prep is local-only. This process does not upload.")
    print("Not Grok weights. Not an upload proxy. Not untraceable origin.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstop")


if __name__ == "__main__":
    main()
