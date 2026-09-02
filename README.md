# AZBot

**The skill Grok, ChatGPT, and Venice import** so they can call Aziel Eliab public engines. Locally it also runs custom skills and Cursor `SKILL.md` files.

**Author:** Aziel Eliab  
**Date:** 2026  
**License:** [Apache-2.0](LICENSE)  
**Version:** 0.2.0

> AZBot is a skill, not a model. Not Grok weights. Jeeves is not sovereign. Forks are welcome and always allowed.

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
- The engines live on [aziel-runtime](https://aziel-runtime.vibelock.workers.dev/).
- Lamb Lens: Peace → Clarity → Service.

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
- Catalog: https://aziel-runtime.vibelock.workers.dev/

Isolated counter: Worker `azbot-download-tracker`, project `azbot`, KV `AZBOT_DOWNLOADS`. `/download` serves gzip (`private, no-store`). No 302 to GitHub.

## License

Apache License 2.0. Copyright 2026 Aziel Eliab.
