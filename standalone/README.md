# AZbot Local 0.2.0

Local operator shell. Binds to 127.0.0.1 only.

## Run

Linux / macOS:

    chmod +x launch.sh
    ./launch.sh

Windows:

    launch.bat

Requires Python 3. Pillow and pypdf for image/PDF prep. ffmpeg optional for media container tags. cryptography for ARK seal.

## What this is

- Slingshot Prep: copy a file, strip identifying embedded metadata, write a SHA-256 receipt.
- ARK1: encrypt body + metadata. Phoenix re-seals gen+1 on authorized local view.
- Skills panel: list, Add skill, Export skill. Discovers custom `skills/` and Cursor `SKILL.md` files.
- Local web UI at http://127.0.0.1:7747
- CLI from repo root: `azbot skills` / `azbot skill run NAME`

## What this is not

- Not Grok model weights. In-session AZbot on grok.com has full Grok tools. This download is the local hygiene shell plus a skill runner.
- Not an upload proxy.
- Not an untraceable-origin system. Network origin of anything you later post is still your channel.

## Identity lock

Public identity on this package is Aziel Eliab. No operator legal name, home, or county in this tree.
