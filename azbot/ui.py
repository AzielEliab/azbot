"""Local AZBot UI. Bind 127.0.0.1 only."""
from __future__ import annotations

import json
import posixpath
import tempfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib.resources import files
from pathlib import Path
from urllib.parse import unquote, urlparse

from azbot import LIMITATION, __version__, skill_text
from azbot.skills_loader import get_skill, import_skill, skills_as_dicts

LOOPBACK = frozenset({"127.0.0.1", "localhost", "::1"})
WEB = files("azbot") / "web"


class Handler(BaseHTTPRequestHandler):
    server_version = f"AZBot/{__version__}"

    def log_message(self, fmt: str, *args: object) -> None:
        return

    def _send(self, status: int, body: bytes, content_type: str, extra: dict[str, str] | None = None) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        if extra:
            for k, v in extra.items():
                self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path in {"/", "/index.html"}:
            self._send(200, (WEB / "index.html").read_bytes(), "text/html; charset=utf-8")
            return
        if path == "/style.css":
            self._send(200, (WEB / "style.css").read_bytes(), "text/css; charset=utf-8")
            return
        if path == "/app.js":
            self._send(200, (WEB / "app.js").read_bytes(), "application/javascript; charset=utf-8")
            return
        if path == "/api/skill":
            body = skill_text().encode("utf-8")
            self._send(200, body, "text/markdown; charset=utf-8")
            return
        if path == "/api/skills":
            body = json.dumps(skills_as_dicts(), indent=2).encode("utf-8")
            self._send(200, body, "application/json; charset=utf-8")
            return
        if path.startswith("/api/skills/") and path.endswith("/export"):
            name = unquote(path[len("/api/skills/"):-len("/export")].strip("/"))
            try:
                skill = get_skill(name)
            except KeyError:
                self._send(404, json.dumps({"error": "skill not found"}).encode(), "application/json; charset=utf-8")
                return
            filename = f"{skill.slug}.md"
            extra = {"Content-Disposition": f'attachment; filename="{filename}"'}
            self._send(200, skill.body.encode("utf-8"), "text/markdown; charset=utf-8", extra)
            return
        if path.startswith("/api/skills/") and path != "/api/skills/":
            name = unquote(path[len("/api/skills/"):].strip("/"))
            if name:
                try:
                    skill = get_skill(name)
                except KeyError:
                    self._send(404, json.dumps({"error": "skill not found"}).encode(), "application/json; charset=utf-8")
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
        self._send(404, LIMITATION.encode(), "text/plain; charset=utf-8")

    def do_POST(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path != "/api/skills/import":
            self._send(404, LIMITATION.encode(), "text/plain; charset=utf-8")
            return
        length = int(self.headers.get("Content-Length", "0") or 0)
        if length <= 0 or length > 2 * 1024 * 1024:
            self._send(400, json.dumps({"ok": False, "error": "file required"}).encode(), "application/json; charset=utf-8")
            return
        raw = self.rfile.read(length)
        files, _fields = _parse_multipart(raw, _boundary(self.headers.get("Content-Type", "")))
        if not files:
            self._send(400, json.dumps({"ok": False, "error": "SKILL.md file required"}).encode(), "application/json; charset=utf-8")
            return
        name, blob = files[0]
        safe = posixpath.basename(name) or "SKILL.md"
        try:
            with tempfile.TemporaryDirectory() as tmp:
                incoming = Path(tmp) / safe
                incoming.write_bytes(blob)
                imported = import_skill(incoming)
            payload = {
                "ok": True,
                "name": imported.name,
                "description": imported.description,
                "slug": imported.slug,
                "path": str(imported.path),
            }
            self._send(200, json.dumps(payload, indent=2).encode(), "application/json; charset=utf-8")
        except Exception as exc:  # noqa: BLE001
            self._send(400, json.dumps({"ok": False, "error": str(exc)}).encode(), "application/json; charset=utf-8")


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
        if filename is not None:
            files.append((filename or "SKILL.md", body))
        elif field:
            fields[field] = body.decode("utf-8", "replace")
    return files, fields


def serve(host: str = "127.0.0.1", port: int = 8870) -> None:
    if host not in LOOPBACK:
        raise ValueError("AZBot UI binds loopback only (127.0.0.1)")
    httpd = ThreadingHTTPServer((host, port), Handler)
    print(f"AZBot UI http://{host}:{port} (loopback only)")
    print(LIMITATION)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
    finally:
        httpd.server_close()
