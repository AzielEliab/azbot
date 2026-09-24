"""Human CLI and local-page contract. JSON shapes stay available via --json."""
from __future__ import annotations

import json
import threading
import urllib.request
from pathlib import Path

import pytest

from azbot import LIMITATION, __version__
from azbot.cli import main

REPO = Path(__file__).resolve().parent.parent


def test_bare_command_is_a_welcome(capsys) -> None:
    assert main([]) == 0
    out = capsys.readouterr().out
    assert "Next:" in out
    assert "azbot ui" in out
    assert "http://127.0.0.1:8870/" in out
    assert "Aziel Eliab" in out
    assert "the following arguments are required" not in out


def test_bare_json(capsys) -> None:
    assert main(["--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["ok"] is True
    assert data["version"] == __version__
    assert data["ui"] == "http://127.0.0.1:8870/"
    assert data["openapi"].endswith("/openapi.json")
    assert isinstance(data["skills"], int)


def test_help_reads_like_a_command_list(capsys) -> None:
    with pytest.raises(SystemExit) as exc:
        main(["--help"])
    assert exc.value.code == 0
    out = capsys.readouterr().out
    assert "azbot ui" in out
    assert "Examples:" in out
    assert "doctor --json" in out
    assert "Not a model" not in out
    assert "the following arguments are required" not in out


def test_unknown_command_has_a_next_step(capsys) -> None:
    with pytest.raises(SystemExit) as exc:
        main(["bogus"])
    assert exc.value.code == 2
    err = capsys.readouterr().err
    assert 'Unknown command "bogus".' in err
    assert "azbot --help" in err


def test_missing_skill_name_has_a_next_step(capsys) -> None:
    with pytest.raises(SystemExit) as exc:
        main(["skill", "run"])
    assert exc.value.code == 2
    err = capsys.readouterr().err
    assert "Missing skill name." in err
    assert "azbot skills" in err


def test_unknown_skill_has_a_next_step(capsys) -> None:
    assert main(["skill", "run", "no-such-skill-xyz"]) == 2
    err = capsys.readouterr().err
    assert "was not found" in err
    assert "azbot skills" in err


def test_skills_json_matches_list_shape(capsys) -> None:
    assert main(["skills", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert isinstance(data, list)
    names = {row["name"].strip().lower() for row in data}
    assert "azbot" in names
    assert {"name", "description", "source", "path", "slug"} <= set(data[0])


def test_doctor_json_keeps_the_report_shape(monkeypatch, capsys) -> None:
    monkeypatch.setattr("azbot.cli._get", lambda url: (200, '{"ok":true}'))
    assert main(["doctor", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert set(data) == {
        "ok",
        "catalog_health_status",
        "openapi",
        "mcp",
        "limitation",
        "version",
        "skills",
    }
    assert data["ok"] is True
    assert data["catalog_health_status"] == 200
    assert data["limitation"] == LIMITATION
    assert data["version"] == __version__


def test_doctor_human_is_plain(monkeypatch, capsys) -> None:
    monkeypatch.setattr("azbot.cli._get", lambda url: (0, "timed out"))
    assert main(["doctor"]) == 1
    out = capsys.readouterr().out
    assert "Catalog: no clear answer" in out
    assert "timed out" in out
    assert "azbot doctor" in out
    assert not out.lstrip().startswith("{")


def test_ui_prints_one_open_line(monkeypatch, capsys) -> None:
    class Dummy:
        def __init__(self, addr, handler):
            self.addr = addr

        def serve_forever(self):
            raise KeyboardInterrupt

        def server_close(self):
            return None

    monkeypatch.setattr("azbot.ui.ThreadingHTTPServer", Dummy)
    from azbot.ui import serve

    serve()
    lines = [line for line in capsys.readouterr().out.splitlines() if line.strip()]
    assert lines[0] == "Open http://127.0.0.1:8870/"


def test_home_html_and_json_accept() -> None:
    from http.server import ThreadingHTTPServer

    from azbot.ui import Handler

    httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    port = httpd.server_address[1]
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        html = urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=5).read().decode("utf-8")
        assert "Copy OpenAPI" in html
        assert "<details" in html
        assert "Advanced" in html
        assert 'name="viewport"' in html
        req = urllib.request.Request(
            f"http://127.0.0.1:{port}/",
            headers={"Accept": "application/json"},
        )
        payload = json.loads(urllib.request.urlopen(req, timeout=5).read().decode("utf-8"))
        assert payload["ok"] is True
        assert payload["version"] == __version__
        assert payload["openapi"].endswith("/openapi.json")
        skills = json.loads(
            urllib.request.urlopen(f"http://127.0.0.1:{port}/api/skills", timeout=5).read().decode("utf-8")
        )
        assert isinstance(skills, list)
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_pages_follow_the_design_standard() -> None:
    css = (REPO / "azbot" / "web" / "style.css").read_text(encoding="utf-8")
    html = (REPO / "azbot" / "web" / "index.html").read_text(encoding="utf-8")
    local = (REPO / "standalone" / "app" / "static" / "index.html").read_text(encoding="utf-8")
    readme = (REPO / "README.md").read_text(encoding="utf-8")
    for text in (css, local):
        assert "prefers-color-scheme" in text
        assert ":focus-visible" in text
        assert "#c9a227" in text
    assert "Service → Clarity → Peace." in html
    assert "Service → Clarity → Peace." in local
    assert "class=\"banner\"" not in html
    assert "Prep copies" in local
    assert "<details" in local
    assert readme.lstrip().startswith("# AZBot")
    assert "## Start" in readme
    assert "/v1/mesh" in readme
    assert "QNS-CD-1.0" in readme
    assert "What this is not" not in (REPO / "standalone" / "README.md").read_text(encoding="utf-8")
