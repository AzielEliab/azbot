"""Local multi-party forensic session for AZBot Design 1.0.

Binds 127.0.0.1. Packages a FragGate call. Appends an immutable tip.
Does not enable public mesh radios and does not host vault wipe.

Author: Aziel Eliab. Apache-2.0.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import urllib.error
import urllib.request
import uuid
from pathlib import Path
from typing import Callable
from urllib.parse import urlparse

DESIGN = "AZBot-Node-Collaborative-Forensic-Design-1.0"
AUTHOR = "Aziel Eliab"
BIND = "127.0.0.1"
FRAGGATE_CALL = "https://aziel-runtime.vibelock.workers.dev/v1/fraggate/call"
GENESIS = "0" * 64
REMAIN_OFF_1 = "GET /v1/mesh never enables; empty POST returns MESH-NEED-BEARER."
CAP7 = "names-only"
CAP7_NAMES = ("mesh_node_live", "alt_internet", "packet_path")
LOOPBACK = frozenset({"127.0.0.1", "localhost", "::1"})

AZOS_PUBLIC = frozenset({"exec", "shell", "lattice"})
VAULT_SLUGS = frozenset({"ark", "embryolock"})
VAULT_OPS = frozenset({"wipe", "scorch", "unlock"})
ALWAYS_REFUSED = frozenset({
    "deanonymize",
    "invent_mark",
    "backdate",
    "rollback",
    "public_rollback",
    "shell",
})

CONSTRAINTS = (
    {"item": "Mesh auto-enable / GET /v1/mesh", "status": "Still never enables"},
    {"item": "AZ-OS public exec / shell / lattice", "status": "Still refused"},
    {"item": "Vault destructive ops (ARK / EmbryoLock wipe, scorch, unlock)", "status": "Still local-only / FG-STUB"},
    {"item": "Deanonymize, invent_mark, backdate, public rollback", "status": "Still refused"},
    {"item": "FragGate single door", "status": "Unchanged"},
    {"item": "Local-first sessions", "status": "Unchanged"},
)

_PARTY = re.compile(r"^[a-z0-9][a-z0-9._-]{0,79}$")
Transport = Callable[[dict], dict]


def _canon(obj: object) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def sha256_canon(obj: object) -> str:
    return hashlib.sha256(_canon(obj)).hexdigest()


def _norm_token(value: object) -> str:
    return str(value or "").strip().lower().replace(" ", "_").replace("-", "_")


def _party(label: object) -> str:
    text = str(label or "").strip().lower().replace(" ", "-")
    if not _PARTY.match(text):
        raise ValueError("Party label must be 1–80 characters: a-z, 0-9, dot, underscore, hyphen.")
    return text


class LatticeMismatch(ValueError):
    """On-disk chain does not recompute. Not repaired."""


def mesh_get() -> dict:
    """Status read. Never enables radios. QNM live OVERRIDE is not applied here."""
    return {
        "ok": True,
        "code": "MESH-OK",
        "enabled": False,
        "radios": "off",
        "default_off": True,
        "remain_off": 1,
        "get_never_enables": True,
        "qnm_override_applied_here": False,
        "bind": BIND,
        "cap7": CAP7,
        "cap7_names": list(CAP7_NAMES),
        "cap7_live": False,
        "cap7_values_stamped_here": False,
        "radio_phy_live": False,
        "radio_phy_claimed_here": False,
        "azchat_stamped_here": False,
        "node_gate": False,
        "auto_heal": False,
        "anonymity_network": False,
        "author": AUTHOR,
        "design": DESIGN,
        "note": "Remain-OFF #1. " + REMAIN_OFF_1 + " Cap-7 names only. Not public ICANN. Not radio PHY LIVE.",
    }


def _loopback_qnm(url: str) -> bool:
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    return parsed.scheme in {"http", "https"} and host in LOOPBACK


def probe_local_qnm(url: str | None = None, opener: Callable[[str], bool] | None = None) -> bool:
    """True only when a loopback qnm-node URL answers. Unset URL does not call the network."""
    target = (url if url is not None else os.environ.get("AZBOT_QNM_NODE", "")).strip()
    if not target or not _loopback_qnm(target):
        return False
    fetch = opener or _probe_fetch
    try:
        return bool(fetch(target))
    except Exception:
        return False


def _probe_fetch(url: str) -> bool:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=2) as res:
            return 200 <= int(res.status) < 500
    except urllib.error.HTTPError as exc:
        return 200 <= int(exc.code) < 500


def mesh_post(body: dict | None = None, bearer: str = "", qnm_url: str | None = None, opener: Callable[[str], bool] | None = None) -> dict:
    """Empty POST refuses. Bearer plus local qnm-node records presence and leaves public radios off."""
    payload = body if isinstance(body, dict) else {}
    token = str(bearer or payload.get("bearer") or payload.get("token") or "").strip()
    base = mesh_get()
    base["ok"] = False
    base["enabled"] = False
    base["radios"] = "off"
    if not token:
        base["code"] = "MESH-NEED-BEARER"
        base["message"] = "Empty POST does not enable. Operator bearer required. Remain-OFF #1."
        return base
    if not probe_local_qnm(qnm_url, opener=opener):
        base["code"] = "MESH-NEED-QNM-NODE"
        base["local_presence"] = "off"
        base["message"] = "Operator bearer is set. Local qnm-node on 127.0.0.1 was not found. Public radios stay off."
        return base
    base["ok"] = True
    base["code"] = "MESH-LOCAL-PRESENCE"
    base["enabled"] = False
    base["public_radios"] = "off"
    base["local_presence"] = "operator-gated"
    base["qnm_node"] = BIND
    base["message"] = "Local presence only. GET /v1/mesh still never enables. Cap-7 stays names-only. Radio PHY is not claimed."
    return base


def regate(slug: str, op: str, payload: dict | None = None, arc_token: str = "") -> dict:
    """Closed-verb re-gate. Five ethics gates stay on AZ-OS. This is not a second door."""
    slug_n = _norm_token(slug).replace("_", "-")
    if slug_n == "az-os":
        slug_n = "azos"
    op_n = _norm_token(op)
    body = payload if isinstance(payload, dict) else {}
    refused = {
        "ok": False,
        "executed": False,
        "slug": slug_n,
        "op": op_n,
        "ethics_gates_hosted_here": False,
        "door": "fraggate",
    }
    if op_n in ALWAYS_REFUSED or (slug_n == "azos" and op_n in AZOS_PUBLIC):
        refused["code"] = "AZOS-REFUSED" if slug_n == "azos" and op_n in AZOS_PUBLIC else "REFUSED"
        if op_n in {"rollback", "public_rollback"}:
            refused["code"] = "ROLLBACK-REFUSED"
        return refused
    if slug_n in VAULT_SLUGS and op_n in VAULT_OPS:
        refused["code"] = "FG-STUB"
        refused["scope"] = "local-only"
        return refused
    if body.get("arc_required") and not str(arc_token or "").strip():
        refused["code"] = "AZOS-NEED-ARC"
        return refused
    return {
        "ok": True,
        "executed": False,
        "code": "AZOS-REGATE-PASS",
        "slug": slug_n,
        "op": op_n,
        "ethics_gates_hosted_here": False,
        "azos_regate": "closed-verb",
        "door": "fraggate",
        "note": "Closed-verb pass. Five ethics gates stay on AZ-OS. Next hop is one FragGate call.",
    }


def package_call(slug: str, op: str, payload: dict | None = None) -> dict:
    gate = regate(slug, op, payload)
    return {"slug": gate["slug"], "op": gate["op"], "payload": payload if isinstance(payload, dict) else {}}


class Session:
    def __init__(self, parties: list[str], session_id: str | None = None) -> None:
        labels = [_party(p) for p in parties]
        if len(labels) < 2:
            raise ValueError("A collaborative session needs at least two parties.")
        if len(set(labels)) != len(labels):
            raise ValueError("Party labels must be unique.")
        self.session_id = session_id or uuid.uuid4().hex
        self.parties = labels
        self.bind = BIND
        self.entries: list[dict] = []
        self.tip = ""

    def append(self, receipt: dict) -> str:
        prev = self.tip or GENESIS
        stored = json.loads(json.dumps(receipt, sort_keys=True))
        body = {"index": len(self.entries), "prev": prev, "receipt": stored}
        tip = sha256_canon(body)
        self.entries.append({"index": body["index"], "prev": prev, "tip": tip, "receipt": stored})
        self.tip = tip
        return tip

    def verify(self) -> bool:
        prev = GENESIS
        for i, entry in enumerate(self.entries):
            body = {"index": i, "prev": prev, "receipt": entry["receipt"]}
            if entry["index"] != i or entry["prev"] != prev or entry["tip"] != sha256_canon(body):
                return False
            prev = entry["tip"]
        if self.entries:
            return self.tip == self.entries[-1]["tip"]
        return self.tip == ""

    def party_view(self) -> dict:
        """Tip share. No payload. No write handle."""
        return {
            "session_id": self.session_id,
            "bind": self.bind,
            "parties": list(self.parties),
            "tip": self.tip,
            "index": (len(self.entries) - 1) if self.entries else None,
            "rewrite": False,
            "entries": [
                {
                    "index": e["index"],
                    "prev": e["prev"],
                    "tip": e["tip"],
                    "slug": e["receipt"].get("slug"),
                    "op": e["receipt"].get("op"),
                    "code": e["receipt"].get("code"),
                    "executed": e["receipt"].get("executed"),
                    "upstream_sha256": e["receipt"].get("upstream_sha256") or "",
                }
                for e in self.entries
            ],
        }

    def to_disk(self) -> dict:
        return json.loads(json.dumps({
            "session_id": self.session_id,
            "parties": list(self.parties),
            "bind": self.bind,
            "tip": self.tip,
            "entries": self.entries,
            "design": DESIGN,
            "author": AUTHOR,
        }))


def rewrite(session: Session, index: int = 0, receipt: dict | None = None) -> dict:
    before = session.tip
    length = len(session.entries)
    return {
        "ok": False,
        "code": "TIP-NO-REWRITE",
        "executed": False,
        "tip": session.tip,
        "tip_unchanged": session.tip == before and len(session.entries) == length,
        "index": index,
        "ignored": True,
    }


def rollback(session: Session) -> dict:
    before = session.tip
    length = len(session.entries)
    return {
        "ok": False,
        "code": "ROLLBACK-REFUSED",
        "executed": False,
        "tip": session.tip,
        "tip_unchanged": session.tip == before and len(session.entries) == length,
    }


def _receipt_from(gate: dict, remote: dict | None, kind: str) -> dict:
    remote = remote or {}
    upstream = remote.get("receipt") if isinstance(remote.get("receipt"), dict) else {}
    upstream_sha = upstream.get("sha256") if isinstance(upstream.get("sha256"), str) else ""
    if len(upstream_sha) != 64:
        upstream_sha = ""
    executed = bool(
        kind == "fraggate"
        and remote.get("ok") is True
        and upstream_sha
        and remote.get("fixture") is not True
    )
    return {
        "kind": kind,
        "door": "fraggate",
        "slug": gate.get("slug"),
        "op": gate.get("op"),
        "code": gate.get("code") if kind == "refusal" else (remote.get("code") or gate.get("code")),
        "executed": executed,
        "upstream_sha256": upstream_sha,
        "fixture": bool(remote.get("fixture")),
        "ran_in": remote.get("ran_in") if executed else None,
        "proxy_is_not_exec": not bool(remote.get("engine_digest")),
        "invented": False,
        "lattice": ["temporallock", "chainlock"],
    }


def handoff(session: Session, slug: str, op: str, payload: dict | None = None, transport: Transport | None = None, arc_token: str = "") -> dict:
    """Package slug+op+payload, pass the closed-verb gate, append one tip. Refused verbs do not call transport."""
    gate = regate(slug, op, payload, arc_token=arc_token)
    call = package_call(slug, op, payload)
    if not gate["ok"]:
        receipt = _receipt_from(gate, None, "refusal")
        tip = session.append(receipt)
        return {
            "ok": False,
            "executed": False,
            "code": gate["code"],
            "tip": tip,
            "transport_called": False,
            "call": call,
            "party_view": session.party_view(),
        }
    if transport is None:
        remote = {"ok": False, "code": "FG-DRY-RUN", "fixture": True}
        called = False
    else:
        called = True
        try:
            remote = transport(call)
        except Exception as exc:
            remote = {"ok": False, "code": "FG-UNREACHABLE", "detail": type(exc).__name__}
        if not isinstance(remote, dict):
            remote = {"ok": False, "code": "FG-NON-OBJECT"}
    receipt = _receipt_from(gate, remote, "fraggate")
    if remote.get("code"):
        receipt["code"] = remote["code"]
    tip = session.append(receipt)
    return {
        "ok": bool(remote.get("ok")) and receipt["executed"],
        "executed": receipt["executed"],
        "code": receipt["code"],
        "tip": tip,
        "transport_called": called,
        "call": call,
        "result": remote.get("result"),
        "party_view": session.party_view(),
    }


def fraggate_transport(call: dict, url: str = FRAGGATE_CALL, timeout: float = 20) -> dict:
    """POST one FragGate call. A missing receipt is not exec and is not invented."""
    req = urllib.request.Request(
        url,
        data=_canon(call),
        headers={"User-Agent": "Mozilla/5.0", "Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as res:
            raw = res.read(2 * 1024 * 1024)
            parsed = json.loads(raw.decode("utf-8", "replace"))
    except Exception as exc:
        return {"ok": False, "code": "FG-UNREACHABLE", "detail": type(exc).__name__}
    if not isinstance(parsed, dict):
        return {"ok": False, "code": "FG-NON-OBJECT"}
    receipt = parsed.get("receipt") if isinstance(parsed.get("receipt"), dict) else None
    engine = parsed.get("engine_digest") or (receipt or {}).get("engine_digest")
    ok = parsed.get("ok") is True and parsed.get("isError") is not True
    return {
        "ok": ok,
        "code": parsed.get("code") or ("FG-OK" if ok else "FG-REFUSED"),
        "result": parsed.get("result", parsed),
        "receipt": receipt,
        "ran_in": parsed.get("ran_in"),
        "engine_digest": engine or None,
    }


def open_session(parties: list[str], session_id: str | None = None) -> Session:
    return Session(parties, session_id=session_id)


def load_session(doc: dict) -> Session:
    session = Session(list(doc.get("parties") or []), session_id=str(doc.get("session_id") or "") or None)
    session.entries = list(doc.get("entries") or [])
    session.tip = str(doc.get("tip") or "")
    if not session.verify():
        raise LatticeMismatch("TIP-NO-REWRITE")
    return session


class SessionStore:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.path = root / "session.json"

    def save(self, session: Session) -> None:
        if not session.verify():
            raise LatticeMismatch("TIP-NO-REWRITE")
        self.root.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(session.to_disk(), indent=2) + "\n", encoding="utf-8")

    def load(self) -> Session | None:
        if not self.path.is_file():
            return None
        return load_session(json.loads(self.path.read_text(encoding="utf-8")))


def doctor_transport(call: dict) -> dict:
    """Local lattice fixture. Does not claim a Softwares engine ran."""
    digest = sha256_canon({"op": call["op"], "payload": call["payload"], "slug": call["slug"]})
    return {
        "ok": True,
        "code": "FG-FIXTURE",
        "fixture": True,
        "result": {"advisory": True, "slug": call["slug"], "op": call["op"]},
        "receipt": {"sha256": digest, "slug": call["slug"], "op": call["op"], "note": "doctor fixture"},
        "ran_in": None,
    }


def lock_report() -> dict:
    """Remain-OFF #1 and tip-share-no-rewrite. No network."""
    status = mesh_get()
    empty = mesh_post({})
    called = {"n": 0}

    def counting(call: dict) -> dict:
        called["n"] += 1
        return doctor_transport(call)

    session = open_session(["human-a", "human-b"], session_id="doctor")
    done = handoff(session, "azclce", "score", {"d": "form", "p": "submits", "r": "button"}, counting)
    tip = done["tip"]
    forged = rewrite(session, 0, {"forged": True})
    refused = handoff(session, "azos", "shell", {"cmd": "no"}, counting)
    rolled = rollback(session)
    view = session.party_view()
    remain = status["enabled"] is False and status["get_never_enables"] is True and status["qnm_override_applied_here"] is False
    ok = (
        remain
        and empty["code"] == "MESH-NEED-BEARER"
        and empty["enabled"] is False
        and forged["ok"] is False
        and forged["tip"] == tip
        and forged["tip_unchanged"] is True
        and refused["executed"] is False
        and refused["transport_called"] is False
        and called["n"] == 1
        and rolled["ok"] is False
        and session.verify()
        and view["rewrite"] is False
        and all("payload" not in row for row in view["entries"])
    )
    return {
        "ok": ok,
        "bind": BIND,
        "remain_off_1": remain,
        "empty_post": empty["code"],
        "empty_post_enables": empty["enabled"],
        "tip": tip,
        "tip_rewrite": forged["ok"],
        "tip_unchanged": forged["tip"] == tip,
        "refused_code": refused["code"],
        "refused_executed": refused["executed"],
        "rollback": rolled["code"],
        "cap7": CAP7,
        "cap7_live": False,
        "radio_phy_live": False,
        "azchat_stamped_here": False,
        "design": DESIGN,
        "constraints": list(CONSTRAINTS),
    }
