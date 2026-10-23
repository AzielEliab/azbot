# AZBot

AZBot lists skill files on this computer and opens a local page with the catalog links an assistant can import.

**Author:** Aziel Eliab  
**Version:** 0.2.0  
**License:** [Apache-2.0](LICENSE)

## Start

1. Install the package:

```bash
pip install -e .
```

2. Open the local page:

```bash
azbot ui
```

3. In the browser, open http://127.0.0.1:8870/ and choose **Copy OpenAPI**.

The page stays on this computer (`127.0.0.1` only).

One-click install, when you want the counted tarball:

```bash
curl -fsSL https://azbot-download-tracker.vibelock.workers.dev/install.sh | bash
```

## Commands

```bash
azbot                 # welcome and next steps
azbot ui              # local page at http://127.0.0.1:8870/
azbot skills          # list skill files
azbot skill           # print the bundled skill
azbot skill run NAME  # print one skill
azbot doctor          # catalog check, in plain text
azbot doctor --json   # same check, for scripts
azbot --help
```

`azbot skills --json` prints the skill list as JSON. `azbot skill import PATH` copies a `SKILL.md` into `skills/<slug>/`. `azbot skill export NAME` writes markdown (`--out FILE` to save a file).

## Local shell

Slingshot Prep, ARK seal, and skill files also run from the standalone shell:

```bash
./standalone/launch.sh
```

Then open http://127.0.0.1:7747/. The first action on that page is **Prep copies**. Windows: `standalone\launch.bat`.

## Notes

Catalog: https://aziel-runtime.vibelock.workers.dev/  
OpenAPI: https://aziel-runtime.vibelock.workers.dev/openapi.json  
MCP: `POST https://aziel-runtime.vibelock.workers.dev/mcp`  
This Worker skill: https://azbot-download-tracker.vibelock.workers.dev/v1/skill  
This Worker OpenAPI: https://azbot-download-tracker.vibelock.workers.dev/openapi.json  

Send `User-Agent: Mozilla/5.0`.

Counted download: https://azbot-download-tracker.vibelock.workers.dev/  
Direct tarball: https://azbot-download-tracker.vibelock.workers.dev/download?asset=azbot-0.2.0.tar.gz  
GitHub: https://github.com/AzielEliab/azbot

Suite mesh on the download Worker is a proxy. `GET /v1/mesh` forwards to aziel-runtime via `AZIEL_RUNTIME`. QNM-BUILD-1.0 reports live, locked, and isolated. QNS-CD-1.0 is a cross-map to [qnm-node](https://github.com/AzielEliab/qnm-node) and the [aziel-runtime design](https://github.com/AzielEliab/aziel-runtime/blob/main/docs/designs/QNS-CD-1.0.md). Remain-OFF #1: `GET /v1/mesh` never enables; an empty POST returns `MESH-NEED-BEARER`. That GET is not cancelled by a QNM live OVERRIDE elsewhere. The mesh proxy has no Node Gate, does not auto-heal, and is not an anonymity network. Local qnsd stays on `127.0.0.1`. Cap-7 names (`mesh_node_live`, `alt_internet`, `packet_path`) are names only in this repo — not public ICANN, not radio PHY LIVE. This repo does not stamp azchat mesh.

Design 1.0 (local handoff, tip share, no rewrite): [docs/designs/AZBot-Node-Collaborative-Forensic-Design-1.0.md](docs/designs/AZBot-Node-Collaborative-Forensic-Design-1.0.md).

```bash
azbot mesh          # GET never enables
azbot mesh post     # empty POST → MESH-NEED-BEARER
azbot session open --party human-a --party human-b
azbot session handoff --slug azclce --op score --payload '{}'
azbot session tip
```

`azbot session handoff --call` posts one FragGate call. Without `--call` the package is recorded and the engine is not claimed.

AZBot is the skill and the local runner. The engines run on aziel-runtime. This package does not host those engines, and it is not an upload proxy. Network origin of a later post is still the channel you use. Hosted `/v1/skill` returns skill markdown. `/v1` does not increment downloads.

Skill files are read from `skills/`, `standalone/skill/SKILL.md`, `$AZBOT_SKILLS_DIR`, `./.cursor/skills/**/SKILL.md`, and `skills/cursor/`.

Cursor rules: [`standalone/cursor/INSTALL.md`](standalone/cursor/INSTALL.md).

Flutter sources for a local viewer of the same URLs: [`mobile/`](mobile/).

Clients that can import the OpenAPI or MCP links include ChatGPT, Grok, Venice, Claude, Cursor, Glama, Perplexity, Copilot, Gemini, Mistral, Meta AI, Apple Intelligence, Amazon Q, DuckAssist, You.com, and Cohere.

Service → Clarity → Peace.

Apache License 2.0. Copyright 2026 Aziel Eliab.
