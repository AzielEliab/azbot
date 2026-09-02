# AZBot

**The skill Grok, ChatGPT, and Venice import** so they can call Aziel Eliab public engines.

**Author:** Aziel Eliab  
**Date:** 2026  
**License:** [Apache-2.0](LICENSE)  
**Version:** 0.1.0

> AZBot is a skill, not a model. Jeeves is not sovereign. Forks are welcome and always allowed.

## Quick start (three steps)

1. Copy this OpenAPI URL:  
   https://aziel-runtime.vibelock.workers.dev/openapi.json
2. Paste it into Grok custom tools, ChatGPT GPT Actions, or Venice HTTP tools.
3. Ask the assistant to run a tool (try `azclce_score` or `GET /v1/health`).

Local preview:

```bash
python -m venv .venv && source .venv/bin/activate && pip install -e ".[dev]"
azbot ui
```

Open http://127.0.0.1:8870 (loopback only). **Copy OpenAPI** / **Copy MCP**. Export is the skill markdown.

Counted download: [https://azbot-download-tracker.vibelock.workers.dev/](https://azbot-download-tracker.vibelock.workers.dev/)

Direct tarball: [azbot-0.1.0.tar.gz](https://azbot-download-tracker.vibelock.workers.dev/download?asset=azbot-0.1.0.tar.gz)

Live skill JSON: `GET https://azbot-download-tracker.vibelock.workers.dev/v1/skill`

## Honest scope

- Not a foundation model. Not a kernel. Not a VPN.
- Hosted `/v1/skill` returns this markdown. It does not run the other engines itself.
- The engines live on [aziel-runtime](https://aziel-runtime.vibelock.workers.dev/).
- Lamb Lens: Peace → Clarity → Service.

## CLI

```bash
azbot skill      # print SKILL.md
azbot doctor     # ping catalog /v1/health
azbot ui         # 127.0.0.1:8870
```

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
- Catalog: https://aziel-runtime.vibelock.workers.dev/

Isolated counter: Worker `azbot-download-tracker`, project `azbot`, KV `AZBOT_DOWNLOADS`. `/download` serves gzip (`private, no-store`). No 302 to GitHub.

## License

Apache License 2.0. Copyright 2026 Aziel Eliab.
