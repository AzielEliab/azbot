---
name: AZBot
description: Use when calling AZBot hosted /v1 or installing the local package. Author Aziel Eliab.
---

# AZBot

A skill for Grok, ChatGPT, and Venice. Not a model. Jeeves is not sovereign. Author: **Aziel Eliab**.

**THIS IS:** a skill plus local runner for custom and Cursor SKILL.md files.

**THIS IS NOT:** a foundation model, Grok weights, a kernel, a VPN, or a paid-key proxy. Hosted `/v1` does not increment downloads or views.

Always send `User-Agent: Mozilla/5.0`. Cloudflare Workers may 403 an empty agent.

## Call these URLs

- Worker OpenAPI: https://azbot-download-tracker.vibelock.workers.dev/openapi.json
- Catalog OpenAPI: https://aziel-runtime.vibelock.workers.dev/openapi.json
- MCP: `POST https://aziel-runtime.vibelock.workers.dev/mcp`
- Live skill (this markdown): `GET https://azbot-download-tracker.vibelock.workers.dev/v1/skill`

Ops (do **not** increment downloads or views):

- `GET /v1/health` — liveness
- `GET /v1/skill` — this file
- Product POSTs listed in OpenAPI

Grok: import OpenAPI as a custom tool. ChatGPT: GPT Actions. Venice: HTTP tools.

## Example

```bash
curl -s -A 'Mozilla/5.0' https://azbot-download-tracker.vibelock.workers.dev/v1/health
curl -s -A 'Mozilla/5.0' https://azbot-download-tracker.vibelock.workers.dev/v1/skill
```

## Local (after one-click install)

```bash
curl -fsSL https://azbot-download-tracker.vibelock.workers.dev/install.sh | bash
azbot ui
azbot doctor
```

Then open http://127.0.0.1:8870 (loopback only).

Counted download (gzip HTTP 200, no 302): https://azbot-download-tracker.vibelock.workers.dev/download?asset=azbot-0.2.0.tar.gz
GitHub: https://github.com/AzielEliab/azbot
