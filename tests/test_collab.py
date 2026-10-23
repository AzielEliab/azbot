"""Design 1.0: Remain-OFF #1 and tip share without rewrite."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from azbot.cli import main
from azbot.collab import (
    LatticeMismatch,
    SessionStore,
    handoff,
    load_session,
    lock_report,
    mesh_get,
    mesh_post,
    open_session,
    probe_local_qnm,
    regate,
    rewrite,
    rollback,
)

ROOT = Path(__file__).resolve().parents[1]


def test_design_paper_landed() -> None:
    paper = ROOT / "docs/designs/AZBot-Node-Collaborative-Forensic-Design-1.0.md"
    pdf = ROOT / "docs/designs/AZBot-Node-Collaborative-Forensic-Design-1.0.pdf"
    text = paper.read_text(encoding="utf-8")
    assert "Aziel Eliab" in text
    assert "Apache-2.0" in text
    assert "Still never enables" in text
    assert "Still local-only / FG-STUB" in text
    assert "Still refused" in text
    assert pdf.read_bytes().startswith(b"%PDF")


def test_mesh_get_never_enables() -> None:
    status = mesh_get()
    assert status["enabled"] is False
    assert status["get_never_enables"] is True
    assert status["remain_off"] == 1
    assert status["qnm_override_applied_here"] is False
    assert status["cap7"] == "names-only"
    assert status["cap7_live"] is False
    assert status["radio_phy_live"] is False
    assert status["azchat_stamped_here"] is False
    assert status["bind"] == "127.0.0.1"
    assert "mesh_node_live" not in status
    assert "alt_internet" not in status
    assert "packet_path" not in status


def test_empty_post_needs_bearer_and_does_not_probe() -> None:
    called = {"n": 0}

    def opener(_url: str) -> bool:
        called["n"] += 1
        return True

    post = mesh_post({}, opener=opener)
    assert post["code"] == "MESH-NEED-BEARER"
    assert post["enabled"] is False
    assert post["radios"] == "off"
    assert called["n"] == 0
    assert "bearer" not in post


def test_bearer_without_loopback_qnm_stays_off() -> None:
    called = {"n": 0}

    def opener(_url: str) -> bool:
        called["n"] += 1
        return True

    off = mesh_post({"bearer": "op-token"}, qnm_url="https://example.invalid/mesh", opener=opener)
    assert off["code"] == "MESH-NEED-QNM-NODE"
    assert off["enabled"] is False
    assert called["n"] == 0
    assert probe_local_qnm("http://10.1.1.1:1", opener=opener) is False
    assert called["n"] == 0


def test_bearer_and_local_qnm_is_presence_not_radio() -> None:
    post = mesh_post({"bearer": "op-token"}, qnm_url="http://127.0.0.1:9/health", opener=lambda _url: True)
    assert post["code"] == "MESH-LOCAL-PRESENCE"
    assert post["enabled"] is False
    assert post["public_radios"] == "off"
    assert post["local_presence"] == "operator-gated"
    assert post["cap7_live"] is False
    assert post["radio_phy_live"] is False
    assert post["qnm_node"] == "127.0.0.1"
    assert "op-token" not in json.dumps(post)


def test_refused_verbs_do_not_call_transport() -> None:
    called = {"n": 0}

    def transport(_call: dict) -> dict:
        called["n"] += 1
        return {"ok": True, "code": "FG-OK", "receipt": {"sha256": "ab" * 32}}

    session = open_session(["human-a", "human-b"], session_id="refused")
    shell = handoff(session, "azos", "shell", {"cmd": "no"}, transport)
    wipe = handoff(session, "ark", "wipe", {}, transport)
    dean = handoff(session, "azclce", "deanonymize", {}, transport)
    back = handoff(session, "chainlock", "backdate", {}, transport)
    roll = handoff(session, "chainlock", "public-rollback", {}, transport)
    assert called["n"] == 0
    assert shell["code"] == "AZOS-REFUSED" and shell["executed"] is False
    assert wipe["code"] == "FG-STUB" and wipe["executed"] is False
    assert dean["code"] == "REFUSED"
    assert back["code"] == "REFUSED"
    assert roll["code"] == "ROLLBACK-REFUSED"
    assert regate("azos", "exec", {})["ok"] is False
    assert regate("azos", "lattice", {})["ok"] is False
    assert regate("embryolock", "scorch", {})["code"] == "FG-STUB"
    assert regate("azclce", "score", {})["ok"] is True
    assert rollback(session)["ok"] is False


def test_tip_share_has_no_rewrite(tmp_path: Path) -> None:
    session = open_session(["human-a", "human-b"], session_id="tip")

    def transport(call: dict) -> dict:
        assert set(call) == {"slug", "op", "payload"}
        digest = "cd" * 32
        return {
            "ok": True,
            "code": "FG-OK",
            "engine_digest": None,
            "receipt": {"sha256": digest, "slug": call["slug"], "op": call["op"]},
            "result": {"advisory": True},
        }

    done = handoff(session, "azclce", "score", {"d": "form", "p": "submits", "r": "button"}, transport)
    assert done["executed"] is True
    assert done["transport_called"] is True
    tip = done["tip"]
    assert len(tip) == 64
    forged = rewrite(session, 0, {"forged": True})
    assert forged["code"] == "TIP-NO-REWRITE"
    assert forged["tip"] == tip
    assert session.tip == tip
    assert session.verify()
    view = session.party_view()
    assert view["rewrite"] is False
    assert view["tip"] == tip
    assert all("payload" not in row for row in view["entries"])
    view["tip"] = "f" * 64
    view["entries"][0]["op"] = "shell"
    assert session.tip == tip
    assert session.entries[0]["receipt"]["op"] == "score"
    disk = session.to_disk()
    disk["entries"][0]["receipt"]["op"] = "shell"
    with pytest.raises(LatticeMismatch):
        load_session(disk)
    store = SessionStore(tmp_path)
    store.save(session)
    loaded = store.load()
    assert loaded is not None
    assert loaded.tip == tip
    assert loaded.verify()


def test_lock_report_is_local() -> None:
    report = lock_report()
    assert report["ok"] is True
    assert report["remain_off_1"] is True
    assert report["empty_post"] == "MESH-NEED-BEARER"
    assert report["tip_rewrite"] is False
    assert report["tip_unchanged"] is True
    assert report["refused_executed"] is False
    assert report["azchat_stamped_here"] is False
    assert report["radio_phy_live"] is False
    assert len(report["constraints"]) == 6


def test_cli_mesh_and_session(tmp_path: Path, capsys, monkeypatch) -> None:
    assert main(["mesh", "--json"]) == 0
    status = json.loads(capsys.readouterr().out)
    assert status["enabled"] is False
    assert status["get_never_enables"] is True

    assert main(["mesh", "post"]) == 0
    text = capsys.readouterr().out
    assert "MESH-NEED-BEARER" in text
    assert "Enabled: false" in text

    assert main(["session", "open", "--dir", str(tmp_path), "--party", "human-a"]) == 2
    assert main(["session", "open", "--dir", str(tmp_path), "--party", "human-a", "--party", "human-b"]) == 0
    assert main([
        "session", "handoff", "--dir", str(tmp_path),
        "--slug", "azclce", "--op", "score", "--payload", '{"r":"a","d":"b","p":"c"}',
    ]) == 0
    hand = capsys.readouterr().out
    assert "Executed: false" in hand
    assert "Engine not called." in hand
    assert main(["session", "tip", "--dir", str(tmp_path), "--json"]) == 0
    view = json.loads(capsys.readouterr().out)
    assert view["rewrite"] is False
    assert len(view["tip"]) == 64
    assert main(["session", "rewrite", "--dir", str(tmp_path)]) == 0
    refused = capsys.readouterr().out
    assert "TIP-NO-REWRITE" in refused
    assert view["tip"] in refused

    def boom(_call: dict) -> dict:
        return {"ok": True, "code": "FG-OK", "receipt": {"sha256": "ab" * 32}, "result": {"ok": True}}

    monkeypatch.setattr("azbot.cli.fraggate_transport", boom)
    assert main([
        "session", "handoff", "--dir", str(tmp_path), "--call",
        "--slug", "decisiongate", "--op", "check", "--payload", '{"proposal":"read the tip"}',
    ]) == 0
    called = capsys.readouterr().out
    assert "Executed: true" in called
    assert "FragGate" in called

    assert main([
        "session", "handoff", "--dir", str(tmp_path), "--call",
        "--slug", "azos", "--op", "exec", "--payload", "{}",
    ]) == 2
    blocked = capsys.readouterr().out
    assert "AZOS-REFUSED" in blocked
    assert "Executed: false" in blocked
