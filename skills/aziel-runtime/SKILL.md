---
name: aziel-runtime
description: Call Aziel Eliab public engines through the aziel-runtime 1.4.0 engine-runtime (catalog + pull + proxy + session + in-process engines). Use when scoring, overlay, health, session exec, or any catalog tool is needed.
---

# aziel-runtime

Call the live engine-runtime. Do not invent scores, overlays, receipts, or health.

**1.4.0** = catalog + pull + proxy + session + in-process engines for listed slugs.
**1.2.0** = session/receipt (exec still proxied).
**1.1.0** = catalog + pull + proxy. Useful front doors. Not exec.

True exec: `open → policy → exec → receipt → close`.
True-engine slugs: `ark`, `azai`, `azclce`, `decisiongate`, `foldlock`, `zsolver` (receipt includes `engine_digest`). Other slugs are `proxy_fallback`. `GET/POST /p/{slug}/{op}` is a proxy. Proxy is not exec.

- Library front door: https://www.azielcorpuslibrary.net/runtime
- Catalog: https://aziel-runtime.vibelock.workers.dev/
- OpenAPI: https://aziel-runtime.vibelock.workers.dev/openapi.json
- MCP: `POST https://aziel-runtime.vibelock.workers.dev/mcp`
- Manifest: `GET https://aziel-runtime.vibelock.workers.dev/v1/runtime.json`

Always send a normal User-Agent (for example `Mozilla/5.0`).

```bash
curl -s -A 'Mozilla/5.0' https://aziel-runtime.vibelock.workers.dev/v1/health
curl -s -A 'Mozilla/5.0' https://www.azielcorpuslibrary.net/runtime/v1/runtime.json
```

This skill is local instructions. It is not Grok weights and it does not proxy uploads.
Author: Aziel Eliab only. Do not invent Zenodo DOIs.
