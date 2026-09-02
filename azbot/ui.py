"""Local AZBot UI. Bind 127.0.0.1 only."""
from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib.resources import files
from urllib.parse import urlparse

from azbot import LIMITATION, skill_text

LOOPBACK = frozenset({"127.0.0.1", "localhost", "::1"})
WEB = files("azbot") / "web"


class Handler(BaseHTTPRequestHandler):
    server_version = "AZBot/0.1.0"

    def log_message(self, fmt: str, *args: object) -> None:
        return

    def _send(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
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
        self._send(404, LIMITATION.encode(), "text/plain; charset=utf-8")


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
