#!/usr/bin/env python3
"""ARK envelope — encrypted body + encrypted metadata, phoenix re-seal on view.

Local vault format only. Does not hide who uploaded a file.
Does not execute anything when a third party opens the blob.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import secrets
import struct
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

MAGIC = b"ARK1"
SALT_LEN = 16
NONCE_LEN = 12
DEK_LEN = 32
SCRYPT_N = 2**14
SCRYPT_R = 8
SCRYPT_P = 1


def _b64(b: bytes) -> str:
    return base64.b64encode(b).decode("ascii")


def _ub64(s: str) -> bytes:
    return base64.b64decode(s.encode("ascii"))


def _kek(passphrase: str, salt: bytes) -> bytes:
    kdf = Scrypt(salt=salt, length=32, n=SCRYPT_N, r=SCRYPT_R, p=SCRYPT_P)
    return kdf.derive(passphrase.encode("utf-8"))


def _pack_bytes(header: dict, meta_ct: bytes, body_ct: bytes) -> bytes:
    raw_h = json.dumps(header, separators=(",", ":")).encode("utf-8")
    return MAGIC + struct.pack(">I", len(raw_h)) + raw_h + struct.pack(">I", len(meta_ct)) + meta_ct + struct.pack(">Q", len(body_ct)) + body_ct


def _unpack_bytes(blob: bytes) -> tuple[dict, bytes, bytes]:
    if blob[:4] != MAGIC:
        raise ValueError("not an ARK1 envelope")
    (hlen,) = struct.unpack(">I", blob[4:8])
    off = 8
    header = json.loads(blob[off : off + hlen].decode("utf-8"))
    off += hlen
    (mlen,) = struct.unpack(">I", blob[off : off + 4])
    off += 4
    meta_ct = blob[off : off + mlen]
    off += mlen
    (blen,) = struct.unpack(">Q", blob[off : off + 8])
    off += 8
    body_ct = blob[off : off + blen]
    return header, meta_ct, body_ct


def seal(src: Path, dest: Path, passphrase: str, extra_meta: dict | None = None) -> dict:
    src = src.expanduser().resolve()
    body = src.read_bytes()
    salt = secrets.token_bytes(SALT_LEN)
    dek = secrets.token_bytes(DEK_LEN)
    kek = _kek(passphrase, salt)
    wrap_n = secrets.token_bytes(NONCE_LEN)
    meta_n = secrets.token_bytes(NONCE_LEN)
    body_n = secrets.token_bytes(NONCE_LEN)
    wrapped = AESGCM(kek).encrypt(wrap_n, dek, b"ark-dek")
    meta = {
        "name": src.name,
        "bytes": len(body),
        "sha256": __import__("hashlib").sha256(body).hexdigest(),
        "sealed_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "gen": 0,
        "extra": extra_meta or {},
    }
    meta_ct = AESGCM(dek).encrypt(meta_n, json.dumps(meta).encode("utf-8"), b"ark-meta")
    body_ct = AESGCM(dek).encrypt(body_n, body, b"ark-body")
    header = {
        "v": 1,
        "gen": 0,
        "kdf": "scrypt",
        "n": SCRYPT_N,
        "r": SCRYPT_R,
        "p": SCRYPT_P,
        "salt": _b64(salt),
        "wrap_nonce": _b64(wrap_n),
        "wrapped_dek": _b64(wrapped),
        "nonce_meta": _b64(meta_n),
        "nonce_body": _b64(body_n),
    }
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(_pack_bytes(header, meta_ct, body_ct))
    return {"ark": str(dest), "gen": 0, "bytes": dest.stat().st_size, "name": src.name}


def _open_env(blob: bytes, passphrase: str) -> tuple[dict, dict, bytes, bytes]:
    header, meta_ct, body_ct = _unpack_bytes(blob)
    kek = _kek(passphrase, _ub64(header["salt"]))
    dek = AESGCM(kek).decrypt(_ub64(header["wrap_nonce"]), _ub64(header["wrapped_dek"]), b"ark-dek")
    meta = json.loads(AESGCM(dek).decrypt(_ub64(header["nonce_meta"]), meta_ct, b"ark-meta").decode("utf-8"))
    body = AESGCM(dek).decrypt(_ub64(header["nonce_body"]), body_ct, b"ark-body")
    return header, meta, body, dek


def inspect(src: Path, passphrase: str) -> dict:
    header, meta, body, _dek = _open_env(src.read_bytes(), passphrase)
    return {
        "header_gen": header.get("gen"),
        "meta": meta,
        "body_bytes": len(body),
        "body_sha256_ok": __import__("hashlib").sha256(body).hexdigest() == meta.get("sha256"),
    }


def phoenix(src: Path, passphrase: str, extract_to: Path | None = None) -> dict:
    """Authorized view: decrypt, optional extract, re-seal with gen+1, overwrite envelope."""
    src = src.expanduser().resolve()
    header, meta, body, _old_dek = _open_env(src.read_bytes(), passphrase)
    if extract_to is not None:
        extract_to.parent.mkdir(parents=True, exist_ok=True)
        extract_to.write_bytes(body)
    new_gen = int(header.get("gen", 0)) + 1
    meta["gen"] = new_gen
    meta["phoenix_utc"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    salt = secrets.token_bytes(SALT_LEN)
    dek = secrets.token_bytes(DEK_LEN)
    kek = _kek(passphrase, salt)
    wrap_n = secrets.token_bytes(NONCE_LEN)
    meta_n = secrets.token_bytes(NONCE_LEN)
    body_n = secrets.token_bytes(NONCE_LEN)
    wrapped = AESGCM(kek).encrypt(wrap_n, dek, b"ark-dek")
    meta_ct = AESGCM(dek).encrypt(meta_n, json.dumps(meta).encode("utf-8"), b"ark-meta")
    body_ct = AESGCM(dek).encrypt(body_n, body, b"ark-body")
    header = {
        "v": 1,
        "gen": new_gen,
        "kdf": "scrypt",
        "n": SCRYPT_N,
        "r": SCRYPT_R,
        "p": SCRYPT_P,
        "salt": _b64(salt),
        "wrap_nonce": _b64(wrap_n),
        "wrapped_dek": _b64(wrapped),
        "nonce_meta": _b64(meta_n),
        "nonce_body": _b64(body_n),
    }
    payload = _pack_bytes(header, meta_ct, body_ct)
    fd, tmp = tempfile.mkstemp(prefix=".ark-", dir=str(src.parent))
    os.close(fd)
    tmp_path = Path(tmp)
    try:
        tmp_path.write_bytes(payload)
        os.replace(tmp_path, src)
    finally:
        if tmp_path.exists():
            tmp_path.unlink(missing_ok=True)
    return {
        "ark": str(src),
        "gen": new_gen,
        "extracted": str(extract_to) if extract_to else None,
        "name": meta.get("name"),
    }


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="ark")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("seal")
    s.add_argument("src")
    s.add_argument("--out")
    s.add_argument("--pass", dest="pw", required=True)

    i = sub.add_parser("inspect")
    i.add_argument("src")
    i.add_argument("--pass", dest="pw", required=True)

    ph = sub.add_parser("phoenix")
    ph.add_argument("src")
    ph.add_argument("--pass", dest="pw", required=True)
    ph.add_argument("--extract")

    args = p.parse_args(argv[1:])
    if args.cmd == "seal":
        src = Path(args.src)
        dest = Path(args.out) if args.out else src.with_suffix(src.suffix + ".ark")
        print(json.dumps(seal(src, dest, args.pw), indent=2))
    elif args.cmd == "inspect":
        print(json.dumps(inspect(Path(args.src), args.pw), indent=2))
    elif args.cmd == "phoenix":
        ext = Path(args.extract) if args.extract else None
        print(json.dumps(phoenix(Path(args.src), args.pw, ext), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
