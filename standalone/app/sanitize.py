#!/usr/bin/env python3
"""AZbot Slingshot Prep — strip identifying embedded metadata from a COPY.

Does not upload. Does not rewrite content timestamps to fake origin.
Original file is never overwritten.
"""
from __future__ import annotations

import io
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff", ".bmp"}
MEDIA_EXT = {".mp4", ".mov", ".m4v", ".mkv", ".webm", ".mp3", ".wav", ".m4a", ".aac"}
OFFICE_EXT = {".docx", ".xlsx", ".pptx"}
PDF_EXT = {".pdf"}

OFFICE_META_NAMES = {
    "docProps/core.xml",
    "docProps/app.xml",
    "docProps/custom.xml",
}


def _out_path(src: Path, dest_dir: Path) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    return dest_dir / src.name


def sanitize_image(src: Path, dest: Path) -> str:
    from PIL import Image

    with Image.open(src) as im:
        clean = im.convert("RGB") if src.suffix.lower() in {".jpg", ".jpeg"} else im.copy()
        save_kw = {}
        if src.suffix.lower() in {".jpg", ".jpeg"}:
            save_kw.update(quality=95, optimize=True)
        clean.save(dest, **save_kw)
    return "image-reencoded-no-exif"


def sanitize_pdf(src: Path, dest: Path) -> str:
    from pypdf import PdfReader, PdfWriter

    reader = PdfReader(str(src))
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    # Empty document info; drop XMP if present by not copying metadata
    writer.add_metadata({})
    if getattr(reader, "metadata", None):
        pass
    with open(dest, "wb") as f:
        writer.write(f)
    return "pdf-info-cleared"


def sanitize_office(src: Path, dest: Path) -> str:
    with zipfile.ZipFile(src, "r") as zin, zipfile.ZipFile(
        dest, "w", compression=zipfile.ZIP_DEFLATED
    ) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            name = item.filename.replace("\\", "/")
            if name in OFFICE_META_NAMES:
                data = _blank_office_xml(name, data)
            # drop thumbnail junk that can carry device previews
            if name.startswith("docProps/thumbnail"):
                continue
            zout.writestr(item, data)
    return "office-core-props-blanked"


def _blank_office_xml(name: str, data: bytes) -> bytes:
    try:
        root = ET.fromstring(data)
    except ET.ParseError:
        return data
    # Wipe text in known identifying elements; keep structure so file stays valid
    wipe_local = {
        "creator",
        "lastModifiedBy",
        "company",
        "manager",
        "title",
        "subject",
        "description",
        "keywords",
        "category",
        "identifier",
        "revision",
        "version",
        "application",
        "appVersion",
        "template",
        "headingPairs",
        "titlesOfParts",
    }
    for el in root.iter():
        local = el.tag.split("}")[-1] if "}" in el.tag else el.tag
        if local in wipe_local:
            el.text = ""
            el.tail = None
            for child in list(el):
                el.remove(child)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def sanitize_media(src: Path, dest: Path) -> str:
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(src),
        "-map_metadata",
        "-1",
        "-c",
        "copy",
        str(dest),
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return "media-container-metadata-stripped"
    except (subprocess.CalledProcessError, FileNotFoundError):
        shutil.copy2(src, dest)
        return "media-copy-only-ffmpeg-unavailable"


def sanitize_generic(src: Path, dest: Path) -> str:
    shutil.copy2(src, dest)
    return "copied-no-known-metadata-handler"


def sanitize_file(src: Path, dest_dir: Path) -> dict:
    src = src.expanduser().resolve()
    if not src.is_file():
        raise FileNotFoundError(src)
    dest = _out_path(src, dest_dir)
    # never write onto the source
    if dest.resolve() == src:
        dest = dest_dir / f"clean-{src.name}"
    ext = src.suffix.lower()
    if ext in IMAGE_EXT:
        method = sanitize_image(src, dest)
    elif ext in PDF_EXT:
        method = sanitize_pdf(src, dest)
    elif ext in OFFICE_EXT:
        method = sanitize_office(src, dest)
    elif ext in MEDIA_EXT:
        method = sanitize_media(src, dest)
    else:
        method = sanitize_generic(src, dest)
    return {
        "source": str(src),
        "clean": str(dest),
        "method": method,
        "bytes": dest.stat().st_size,
    }


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: sanitize.py <file> [more files...] [--out DIR]")
        return 2
    dest_dir = Path("out")
    files = []
    args = argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--out" and i + 1 < len(args):
            dest_dir = Path(args[i + 1])
            i += 2
            continue
        files.append(Path(args[i]))
        i += 1
    for f in files:
        info = sanitize_file(f, dest_dir)
        print(f"{info['method']}\t{info['clean']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
