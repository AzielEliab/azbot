---
name: aziel-runtime
description: Call Aziel Eliab public engines through the aziel-runtime OpenAPI/MCP catalog. Use when scoring, overlay, health, or any catalog tool is needed.
---

# aziel-runtime

Call the live catalog. Do not invent scores, overlays, receipts, or health.

- Catalog: https://aziel-runtime.vibelock.workers.dev/
- OpenAPI: https://aziel-runtime.vibelock.workers.dev/openapi.json
- MCP: `POST https://aziel-runtime.vibelock.workers.dev/mcp`

Always send a normal User-Agent (for example `Mozilla/5.0`).

```bash
curl -s -A 'Mozilla/5.0' https://aziel-runtime.vibelock.workers.dev/v1/health
```

This skill is local instructions. It is not Grok weights and it does not proxy uploads.
