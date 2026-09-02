---
name: AZBot
description: Use this when Grok, ChatGPT, Venice, or any assistant should call Aziel Eliab public engines via the aziel-runtime OpenAPI/MCP catalog.
---

# AZBot

AZBot is a **skill**. It is not a new foundation model, not a kernel, not a VPN, not a paid-key proxy, and not Jeeves-as-sovereign.

One catalog for every public Aziel Eliab engine:

- Catalog: https://aziel-runtime.vibelock.workers.dev/
- OpenAPI: https://aziel-runtime.vibelock.workers.dev/openapi.json
- MCP: `POST https://aziel-runtime.vibelock.workers.dev/mcp`

Always send a normal `User-Agent` (for example `Mozilla/5.0`). Cloudflare Workers may 403 empty agents.

## Rules

1. Call the catalog. Do not invent scores, overlays, receipts, or health.
2. Repeat the product banner. Never claim forensic proof, a lab spectrometer, a real UV lamp, OCR truth, a kernel, a VPN, legal advice, lie detection, call intercept, or hosted AZAI spending paid keys.
3. Lamb Lens order: Peace → Clarity → Service. Jeeves is not sovereign.
4. AZ-CLCE Type D is a **label only**, not a finding of malice.
5. SpectralLock overlays are advisory visualization. The human still reads the page.
6. ForgeReceipts is not legal advice.
7. Forks are welcome and always allowed. Apache-2.0.

## How to call

```bash
curl -s -A 'Mozilla/5.0' https://aziel-runtime.vibelock.workers.dev/v1/health
curl -s -A 'Mozilla/5.0' -X POST https://aziel-runtime.vibelock.workers.dev/p/azclce/score \
  -H 'content-type: application/json' \
  -d '{"r":"login button blue","d":"login form submits","p":"login button submits"}'
```

MCP tools are named `{slug}_{op}` (example `azclce_score`, `spectrallock_overlay`, `azai_lamb_check`).

Grok: import the OpenAPI as a custom tool. ChatGPT: GPT Actions. Venice: HTTP tools.

## Products (honest one-liners)

| slug | name | do not claim |
|------|------|----------------|
| vibelock | VibeLock | courtroom audio proof |
| veillock | VeilLock | FaceTime/Zoom intercept |
| codelock | CodeLock | that meaning changed |
| godlock | GodLock | a VPN or ghost net |
| shadowlock | ShadowLock | OS hooks / process intercept |
| temporallock | TemporalLock | legal chain of custody |
| forgereceipts | ForgeReceipts | legal advice / court filing |
| decisiongate | DecisionGATE | moral authority |
| zsolver | ZionPattern Solver | a solved case; cap is 75% |
| azos | AZ-OS | a kernel or remote shell |
| glossafilter | Glossa Filter | that tools hold opinions |
| miragegrid | MirageGrid | anonymity / VPN |
| staticclock | StaticClock | a scheduler you set |
| chronolock | ChronoLock | targeting or virality |
| postking | Post-King Chess | that the goal is to win |
| azclce | AZ-CLCE | intent or malice |
| ark | The ARK | a kernel; hosted unlock |
| azai | AZAI | a new model; hosted paid proxy |
| spectrallock | SpectralLock | spectrometer / forensic ink |


## Local (after one-click install)

```bash
curl -fsSL https://azbot-download-tracker.vibelock.workers.dev/install.sh | bash
azbot ui
```
