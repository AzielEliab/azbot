# AZBot

**The skill OpenAPI- and MCP-capable assistants import** so they can call Aziel Eliab public engines. Locally it also runs custom skills and Cursor `SKILL.md` files.

Clients: ChatGPT (GPT Actions / OpenAI), Grok (xAI), Venice, Claude (Anthropic), Cursor (MCP), Glama (MCP), Perplexity, Microsoft Copilot / Bing, Google Gemini / Vertex, Mistral, Meta AI, Apple Intelligence surfaces, Amazon Q tooling, DuckAssist, You.com, Cohere, and other MCP/OpenAPI-capable assistants.

**Author:** Aziel Eliab  
**Date:** 2026  
**License:** [Apache-2.0](LICENSE)  
**Version:** 0.2.0

> AZBot is a skill, not a model. Not Grok weights. Jeeves is not sovereign. Forks are welcome and always allowed.


## One-click install

```bash
curl -fsSL https://azbot-download-tracker.vibelock.workers.dev/install.sh | bash
```

The script curls the **counted** tarball from this project's Worker
(`/download`, User-Agent `Mozilla/5.0`), extracts, makes a venv, and
`pip install -e .`. Then run `azbot ui`.

Or tap **Download** / **One-click install** on the Worker homepage
(a 6th-grader can tap it):
https://azbot-download-tracker.vibelock.workers.dev/

## Counted download (Cloudflare Worker)

**This is the counted download.** GitHub releases exist as a mirror.
The Worker serves the gzip itself (HTTP 200, no 302 to GitHub).

# → [https://azbot-download-tracker.vibelock.workers.dev/](https://azbot-download-tracker.vibelock.workers.dev/) ←

Direct tarball (also counted):
[azbot-0.2.0.tar.gz](https://azbot-download-tracker.vibelock.workers.dev/download?asset=azbot-0.2.0.tar.gz)

- Compact count JSON (`{project, views, downloads, total}`): [https://azbot-download-tracker.vibelock.workers.dev/count](https://azbot-download-tracker.vibelock.workers.dev/count)
- Live stats JSON: [https://azbot-download-tracker.vibelock.workers.dev/stats](https://azbot-download-tracker.vibelock.workers.dev/stats)
- OpenAPI: [https://azbot-download-tracker.vibelock.workers.dev/openapi.json](https://azbot-download-tracker.vibelock.workers.dev/openapi.json)
- Skill: [https://azbot-download-tracker.vibelock.workers.dev/v1/skill](https://azbot-download-tracker.vibelock.workers.dev/v1/skill)
- Suite mesh proxy: [https://azbot-download-tracker.vibelock.workers.dev/v1/mesh](https://azbot-download-tracker.vibelock.workers.dev/v1/mesh) — default OFF; QNM live / locked / isolated
- One-click install: [https://azbot-download-tracker.vibelock.workers.dev/install.sh](https://azbot-download-tracker.vibelock.workers.dev/install.sh)
- GitHub: [https://github.com/AzielEliab/azbot](https://github.com/AzielEliab/azbot)

Isolated counter: Worker `azbot-download-tracker`, KV `AZBOT_DOWNLOADS`. Not mixed with any other product. `/v1` does not increment downloads.


## Quick start

```bash
./standalone/launch.sh
```

or

```bash
pip install -e .
azbot ui
```

Standalone UI: http://127.0.0.1:7747 (Slingshot Prep, ARK seal, Skills).  
Package UI: http://127.0.0.1:8870 (loopback only). **Copy OpenAPI** / **Copy MCP**. Skills panel: **Add skill** / **Export skill**.

Counted download: [https://azbot-download-tracker.vibelock.workers.dev/](https://azbot-download-tracker.vibelock.workers.dev/)

Direct tarball: [azbot-0.2.0.tar.gz](https://azbot-download-tracker.vibelock.workers.dev/download?asset=azbot-0.2.0.tar.gz)

Live skill JSON: `GET https://azbot-download-tracker.vibelock.workers.dev/v1/skill`

## Honest scope

- Not a foundation model. Not Grok weights. Not a kernel. Not a VPN.
- Not an upload proxy.
- Not an untraceable-origin system. Network origin of anything you later post is still your channel.
- Hosted `/v1/skill` returns skill markdown. It does not run the other engines itself.
- Suite mesh `/v1/mesh/*` PROXY to aziel-runtime via `AZIEL_RUNTIME`. Default OFF. QNM-BUILD-1.0 live|locked|isolated. QNS-CD-1.0 companion (cite/proxy only). No Node Gate. No auto-heal. Not anonymity. Catalog MCP `mesh_*` + FragGate `slug=mesh`.
- The engines live on [aziel-runtime](https://aziel-runtime.vibelock.workers.dev/).
- Lamb Lens: Peace → Clarity → Service.

## QNS-CD-1.0

Cross-map only. Not a new product. Not a Softwares-tab engine.

Companion to QNM-BUILD-1.0. Local qnsd: [qnm-node](https://github.com/AzielEliab/qnm-node). Runtime design: [QNS-CD-1.0](https://github.com/AzielEliab/aziel-runtime/blob/main/docs/designs/QNS-CD-1.0.md). This Worker cites/proxies suite mesh. Photon QNS1 vias stay on local qnsd (`127.0.0.1`). Restriction walks next via class. `GET /v1/mesh` never enables. No Node Gate. No local qnsd HTTP on this public Worker.

Author: Aziel Eliab.

## Skills (custom + Cursor)

AZBot discovers `SKILL.md` files with YAML frontmatter (`name` + `description`) from:

1. `skills/` — drop-in custom skills
2. `standalone/skill/SKILL.md` — bundled operator skill
3. `$AZBOT_SKILLS_DIR` if set
4. `./.cursor/skills/**/SKILL.md`
5. `skills/cursor/` — vendored Cursor skills

```bash
azbot skills              # list name + description
azbot skill               # print catalog SKILL.md
azbot skill run NAME      # print the skill body (local operator; not Grok weights)
azbot skill import PATH   # copy a SKILL.md into skills/<slug>/
azbot skill export NAME   # write markdown
azbot doctor              # ping catalog /v1/health
azbot ui                  # 127.0.0.1:8870
```

Cursor: copy `.cursor/rules` into a repo. See [`standalone/cursor/INSTALL.md`](standalone/cursor/INSTALL.md).

## iPhone & Android

Flutter sources: [`mobile/`](mobile/). Viewer for the OpenAPI/MCP URLs. Not a store IPA.

```bash
cd mobile
flutter create --org com.azieeliab --project-name azbot .
flutter pub get
flutter run
```

## Hosted

- OpenAPI: https://azbot-download-tracker.vibelock.workers.dev/openapi.json
- Health: `GET /v1/health`
- Skill: `GET /v1/skill` — does **not** increment downloads
- Suite mesh: `GET /v1/mesh` PROXY (default OFF). QNM-BUILD-1.0 live|locked|isolated. QNS-CD-1.0 companion. No Node Gate
- Catalog: https://aziel-runtime.vibelock.workers.dev/

Isolated counter: Worker `azbot-download-tracker`, project `azbot`, KV `AZBOT_DOWNLOADS`. `/download` serves gzip (`private, no-store`). No 302 to GitHub.

## Use with OpenAPI / MCP clients

Catalog OpenAPI: https://aziel-runtime.vibelock.workers.dev/openapi.json
Catalog MCP: `POST https://aziel-runtime.vibelock.workers.dev/mcp`
This Worker skill: https://azbot-download-tracker.vibelock.workers.dev/v1/skill
This Worker OpenAPI: https://azbot-download-tracker.vibelock.workers.dev/openapi.json
This Worker `/v1/fraggate/*` and `/v1/mesh/*` PROXY via AZIEL_RUNTIME. Suite mesh default OFF. QNM-BUILD-1.0 live|locked|isolated. QNS-CD-1.0 companion to QNM-BUILD-1.0. No Node Gate. No auto-heal. Not anonymity. Catalog MCP `mesh_*` + FragGate `slug=mesh`.

Import the catalog or Worker OpenAPI as a custom tool, GPT Action, or HTTP tool. Connect MCP at the catalog MCP URL. Always send `User-Agent: Mozilla/5.0`.

Known clients: ChatGPT (GPT Actions / OpenAI), Grok (xAI), Venice, Claude (Anthropic), Cursor (MCP), Glama (MCP), Perplexity, Microsoft Copilot / Bing, Google Gemini / Vertex, Mistral, Meta AI, Apple Intelligence surfaces, Amazon Q tooling, DuckAssist, You.com, Cohere, and other MCP/OpenAPI-capable assistants.

Practical import notes (same two doors; no per-crawler installer):

- OpenAPI: ChatGPT uses GPT Actions (no auth). Grok imports a custom tool. Venice uses HTTP tools. Other OpenAPI clients import the same JSON.
- MCP: Cursor and Glama connect to the catalog MCP URL. Other MCP clients use the same POST.

## Cite this

Aziel Eliab. AZBot. https://github.com/AzielEliab/azbot. https://azbot-download-tracker.vibelock.workers.dev. QNS-CD-1.0 companion to QNM-BUILD-1.0 (cross-map to qnm-node + aziel-runtime; not a new product).

- Catalog: https://aziel-runtime.vibelock.workers.dev/
- Worker homepage: https://azbot-download-tracker.vibelock.workers.dev/
- Counted download (gzip HTTP 200, no 302): https://azbot-download-tracker.vibelock.workers.dev/download
- GitHub: https://github.com/AzielEliab/azbot
- Citation JSON: https://azbot-download-tracker.vibelock.workers.dev/cite.json

## License

Apache License 2.0. Copyright 2026 Aziel Eliab.
