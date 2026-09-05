---
name: AZBot
description: >-
  Use when Grok, ChatGPT, Venice, or any assistant should call Aziel Eliab public
  engines via aziel-runtime, godlock.uk, or azielcorpuslibrary.net — front-door
  HTTP only; metadata scrape OK; never backdoor.
---

# AZBot

AZBot is a **skill**. It is not a new foundation model, not a kernel, not a VPN, not a paid-key proxy, and not Jeeves-as-sovereign.

**THIS IS:** a skill that tethers assistants to Aziel Eliab public front doors and the aziel-runtime 1.4.0 engine-runtime catalog.

**THIS IS NOT:** a foundation model, Grok weights, a kernel, a VPN, a paid-key proxy, or Jeeves-as-sovereign. Hosted `/v1` does not increment downloads or views.

Always send `User-Agent: Mozilla/5.0`. Cloudflare Workers may 403 empty agents.

Author: **Aziel Eliab** only. Do not invent Zenodo DOIs. Cite a DOI only when that product's own skill or `/cite.json` already publishes it.

## Front doors (tether here)

### 1) Product catalog + engine-runtime (all engines)

- Library front door: https://www.azielcorpuslibrary.net/runtime
- Catalog / Worker: https://aziel-runtime.vibelock.workers.dev/
- OpenAPI: https://aziel-runtime.vibelock.workers.dev/openapi.json
- MCP: `POST https://aziel-runtime.vibelock.workers.dev/mcp`
- Manifest: `GET https://aziel-runtime.vibelock.workers.dev/v1/runtime.json` (`role=engine-runtime`)

### 2) GodLock public board

- Site: https://godlock.uk/
- Health: `GET https://godlock.uk/health`
- Submit challenge: `POST https://godlock.uk/submit` (form field `text` or JSON `{ "text": "..." }`)
- Archive / verify / receipt: `/archive`, `/verify`, `/receipt/{id}` as published on the site
- Weighing framework: Empirical Knowledge and the Limits of Observation (Aziel Eliab). ABAD removed.
- Floor 33.3 · ceiling 99.7 · labels Yes / No / Let's review / Interesting

### 3) Aziel Digital Library (corpus)

- Site: https://www.azielcorpuslibrary.net/
- Health: `GET https://www.azielcorpuslibrary.net/v1/health`
- Search: `GET https://www.azielcorpuslibrary.net/v1/search?q=...&lib=all|aziel|corpus`
- OpenAPI / skill: `/openapi.json`, `/v1/skill`
- Hosted tools (public GET pages): `/map`, `/ocr`, `/gazetteer`, `/tree`, `/intelligence`, `/pattern`, `/historical`, `/software`

## Front door only — never backdoor

**Allowed:**

- Documented public HTTPS routes above (and aziel-runtime `/p/{slug}/{op}` proxies)
- Metadata checks and light public-page scraping of those front doors: titles, meta tags, OpenAPI, `/health`, `/cite.json`, `/llms.txt`, robots, sitemaps, visible public HTML text used to verify what the site publishes
- Reading published skill / OpenAPI / catalog JSON
- Runtime session `open → policy → exec → receipt → close` on the published session routes

**Forbidden forever (backdoors):**

- Cookie theft, session forging, operator/login bypass
- Direct Cloudflare D1/KV/R2/API access or wrangler against production as a substitute for the public site
- Undocumented Worker internals, service-binding tricks, or side-door URLs not published on the site / OpenAPI / skill
- Claiming mesh, VPN, or anonymity on godlock.uk

If a write or privileged capability is not on the public front door or OpenAPI, say so — do not invent a backdoor. Metadata scrape of public pages is fine.

## Rules

1. Call the front doors. Do not invent scores, overlays, receipts, or health.
2. Repeat the product banner. Never claim forensic proof, a lab spectrometer, a real UV lamp, OCR truth, a kernel, a VPN (GodLock / godlock.uk), legal advice, lie detection, call intercept, or hosted AZAI spending paid keys.
3. Lamb Lens order: Peace → Clarity → Service. Jeeves is not sovereign.
4. AZ-CLCE Type D is a **label only**, not a finding of malice.
5. SpectralLock overlays are advisory visualization. The human still reads the page.
6. ForgeReceipts is not legal advice.
7. Forks are welcome and always allowed. Apache-2.0.
8. Public identity is **Aziel Eliab** only.
9. `GET/POST /p/{slug}/{op}` is a **proxy**. Proxy is **not** exec. True exec is a runtime session.

## How to call

```bash
# Catalog / engine-runtime
curl -s -A 'Mozilla/5.0' https://aziel-runtime.vibelock.workers.dev/v1/health
curl -s -A 'Mozilla/5.0' https://www.azielcorpuslibrary.net/runtime/v1/health

# GodLock front door
curl -s -A 'Mozilla/5.0' https://godlock.uk/health
curl -s -A 'Mozilla/5.0' -X POST https://godlock.uk/submit \
  -H 'content-type: application/json' \
  -d '{"text":"Empirical does not mean fully isolated; incomplete control leaves deeper structure open."}'

# Aziel Digital Library front door
curl -s -A 'Mozilla/5.0' 'https://www.azielcorpuslibrary.net/v1/search?q=Empirical&lib=aziel&limit=5'
```

MCP tools are named `{slug}_{op}` (example `azclce_score`, `spectrallock_overlay`, `azai_lamb_check`, `aziel-corpus_search`). Runtime helpers: `runtime_skill`, `runtime_manifest`, `runtime_bundle`, `runtime_pull`, `runtime_session_open`, `runtime_session_policy`, `runtime_session_exec`, `runtime_session_receipt`, `runtime_session_receipts`, `runtime_session_close`.

Grok: import the OpenAPI as a custom tool. ChatGPT: GPT Actions. Venice: HTTP tools.

## Products (honest one-liners)

| slug | name | do not claim |
|------|------|----------------|
| aziel-runtime | Aziel Eliab Runtime | that proxy is exec; that 1.1.0 is current |
| azieltether | AzielTether | a VPN or a mesh on godlock.uk |
| foldlock | FoldLock | the ZIP file format; that every file shrinks |
| azclce | AZ-CLCE | intent or malice |
| azos | AZ-OS | a kernel; unrestricted SSH / host bash |
| azai | AZAI | a new model; hosted paid-key proxy |
| azbot | AZBot | a foundation model |
| aziel-corpus | Aziel Digital Library | a 26-card index; private-file search |
| chronolock | ChronoLock | targeting or virality |
| codelock | CodeLock | that meaning changed |
| decisiongate | DecisionGATE | moral authority |
| employeelock | EmployeeLock | a court / truth score |
| forgereceipts | ForgeReceipts | legal advice / court filing |
| glossafilter | Glossa Filter | that tools hold opinions |
| godlock | GodLock | a VPN or ghost net; use https://godlock.uk front door |
| mialock | M.I.A.Lock | live tracking or Doe auto-ID; Doe leads ≠ ID |
| miragegrid | MirageGrid | guarantee against a global adversary; a crime tool |
| postking | Post-King Chess | that the goal is to win |
| shadowlock | ShadowLock | OS hooks / process intercept |
| spectrallock | SpectralLock | spectrometer / forensic ink |
| staticclock | StaticClock | a scheduler you set |
| temporallock | TemporalLock | legal chain of custody |
| ark | The ARK | a kernel; hosted unlock |
| trajectorylock | TrajectoryLock | certified forensic instrument |
| veillock | VeilLock | FaceTime/Zoom intercept |
| vibelock | VibeLock | courtroom audio proof |
| whistlelock | WhistleLock | a mailer / hosted drop store |
| zsolver | ZionPattern Solver | a solved case; cap is 75% |

Catalog versions (aziel-runtime `/v1/catalog.json`): vibelock 0.3.0, veillock 0.2.0, codelock 0.1.0, godlock 0.1.0, shadowlock 0.2.0, temporallock 0.2.0, forgereceipts 0.3.0, decisiongate 0.1.0, zsolver 0.2.0 (live skill also says 0.4.0), azos 0.3.0, glossafilter 0.1.0, miragegrid 0.2.0, staticclock 0.2.0, chronolock 0.1.0, postking 0.1.0, azclce 0.3.0, ark 0.1.0, azai 0.3.1, spectrallock 0.3.0, azbot 0.2.0, employeelock 0.1.0, foldlock 0.8.0, whistlelock 0.1.0, trajectorylock 0.1.0, mialock 0.1.1, azieltether 0.1.0, aziel-corpus 2.6.2 (live library skill 2.7.0). Runtime 1.4.0.

Workers are typically `https://{slug}-download-tracker.vibelock.workers.dev`. Exceptions: aziel-corpus → https://www.azielcorpuslibrary.net ; postking → `postking-download-tracker` ; zsolver → `zsolver-download-tracker` ; az-clce repo → slug `azclce`.

## Aziel Eliab Runtime toolkit (1.4.0 engine-runtime)

**1.4.0 = catalog + pull + proxy + session + in-process engines** for **every** catalog Software slug.
**1.3.0 = true engine runtime** for listed portable slugs only (superseded by 1.4.0).
**1.2.0 = session-runtime** (receipt chain; exec still proxied to product Workers).
**1.1.0 = catalog + pull + proxy** that started calling itself a runtime. Useful front doors. Not exec.

**THIS IS:** the root engine-runtime. Session `open → policy → exec → receipt → close`. For true-engine slugs (`ark`, `azai`, `azclce`, `decisiongate`, `foldlock`, `zsolver`) exec runs a vendored module **inside the Cloudflare isolate** and the receipt includes `engine_digest`, `engine_slug`, `engine_op`, `ran_in: "aziel-runtime"`.

**THIS IS NOT:** a claim that `/p/{slug}/{op}` is exec (that path is still **proxy**). Proxy without a session receipt is **not** exec. Binding-only ops (KV/D1/AI/live media) may still be per-op `proxy_fallback`, but **every catalog slug** is a true in-process engine on session exec. Hosted AZAI is protocol mirror + Lamb check, **not** the local blend. No extra guest isolate is claimed. No counted runtime tarball. Do not invent Zenodo DOIs. Do **not** treat `https://www.azielcorpuslibrary.net/v1/runtime` as the engine manifest — that is Digital Library package discovery; use `/runtime/v1/runtime.json` or `https://aziel-runtime.vibelock.workers.dev/v1/runtime.json`.

Prefer:

- https://www.azielcorpuslibrary.net/runtime
- https://aziel-runtime.vibelock.workers.dev/

- Host: https://aziel-runtime.vibelock.workers.dev/
- Library front door: https://www.azielcorpuslibrary.net/runtime
- Skill: `GET https://aziel-runtime.vibelock.workers.dev/v1/skill` · `GET https://www.azielcorpuslibrary.net/runtime/v1/skill`
- Health: `GET https://aziel-runtime.vibelock.workers.dev/v1/health` · `GET https://www.azielcorpuslibrary.net/runtime/v1/health`
- Manifest: `GET /v1/runtime.json` (`role=engine-runtime`)
- OpenAPI: `GET /openapi.json`
- Pull one: `GET /v1/pull/{slug}` · skill body `GET /v1/pull/{slug}/skill`
- Bundle all: `GET /v1/bundle` (or `/v1/pull?all=1`)
- Proxy (not exec): `GET|POST /p/{slug}/{op}`
- Session: `POST /v1/session/open` → `POST /v1/session/{id}/policy` → `POST /v1/session/{id}/exec` → `GET /v1/session/{id}/receipt` → `POST /v1/session/{id}/close`
- MCP tools: `runtime_skill`, `runtime_manifest`, `runtime_bundle`, `runtime_pull`, `runtime_session_open`, `runtime_session_policy`, `runtime_session_exec`, `runtime_session_receipt`, `runtime_session_receipts`, `runtime_session_close`

```bash
curl -s -A 'Mozilla/5.0' https://aziel-runtime.vibelock.workers.dev/v1/skill
curl -s -A 'Mozilla/5.0' https://www.azielcorpuslibrary.net/runtime/v1/runtime.json
SID=$(curl -s -A 'Mozilla/5.0' -X POST https://aziel-runtime.vibelock.workers.dev/v1/session/open \
  -H 'content-type: application/json' -d '{}' | jq -r .session.id)
curl -s -A 'Mozilla/5.0' -X POST https://aziel-runtime.vibelock.workers.dev/v1/session/$SID/policy \
  -H 'content-type: application/json' \
  -d '{"allow_slugs":["azclce"],"max_payload_bytes":8192}'
curl -s -A 'Mozilla/5.0' -X POST https://aziel-runtime.vibelock.workers.dev/v1/session/$SID/exec \
  -H 'content-type: application/json' \
  -d '{"slug":"azclce","op":"score","payload":{"r":"login button blue","d":"login form submits","p":"login button submits"}}'
curl -s -A 'Mozilla/5.0' https://aziel-runtime.vibelock.workers.dev/v1/session/$SID/receipt
curl -s -A 'Mozilla/5.0' -X POST https://aziel-runtime.vibelock.workers.dev/v1/session/$SID/close
```

## AzielTether toolkit (0.1.0)

Central × decentral software tether. Prefer the counted Worker when up; peer hash-chain sync when down; reconcile on restore. Author Aziel Eliab.

**THIS IS:** a software tether (prefer-central / peer-sync-when-down / reconcile-on-restore).

**THIS IS NOT:** a VPN, MirageGrid, a kernel, a truth score, or a mesh on godlock.uk. Public HTTPS boards stay mesh-free. The tether lives in the downloaded software.

- Host: https://azieltether-download-tracker.vibelock.workers.dev
- Skill: `GET https://azieltether-download-tracker.vibelock.workers.dev/v1/skill`
- Health: `GET https://azieltether-download-tracker.vibelock.workers.dev/v1/health`
- OpenAPI: `GET https://azieltether-download-tracker.vibelock.workers.dev/openapi.json`
- Download: `GET https://azieltether-download-tracker.vibelock.workers.dev/download`
- Catalog aliases: `https://aziel-runtime.vibelock.workers.dev/p/azieltether/{health,skill}`
- MCP tools: `azieltether_health`, `azieltether_skill`
- Worker also publishes (front door): `/v1/ingest`, `/v1/pulse`, `/v1/reconcile`, `/v1/dual-chain`, `/v1/tip`, `/v1/verify`, `/v1/peer-preview`

```bash
curl -s -A 'Mozilla/5.0' https://azieltether-download-tracker.vibelock.workers.dev/v1/health
curl -s -A 'Mozilla/5.0' https://azieltether-download-tracker.vibelock.workers.dev/v1/skill
curl -s -A 'Mozilla/5.0' https://aziel-runtime.vibelock.workers.dev/p/azieltether/health
```

## FoldLock toolkit (0.8.0)

Zip-class SOTA adaptive UNI1 tether/SIR fold on UTF-8 text. Exact restore. Hosted, preview ~8 KB. In-process engine on aziel-runtime. Author Aziel Eliab.

**THIS IS:** compression software (FLD3 / UNI1). Classify → bakeoff → passthrough. Short strings can stay the same size.

**THIS IS NOT:** the ZIP file format; a zlib/gzip/DEFLATE/zstd wrapper; a claim every file shrinks or always beats zstd; encryption.

- Host: https://foldlock-download-tracker.vibelock.workers.dev
- Skill: `GET https://foldlock-download-tracker.vibelock.workers.dev/v1/skill`
- Health: `GET https://foldlock-download-tracker.vibelock.workers.dev/v1/health`
- OpenAPI: `GET https://foldlock-download-tracker.vibelock.workers.dev/openapi.json`
- Download: `GET https://foldlock-download-tracker.vibelock.workers.dev/download`
- Catalog aliases: `https://aziel-runtime.vibelock.workers.dev/p/foldlock/{health,skill,fold-preview,unfold-preview}`
- MCP tools: `foldlock_health`, `foldlock_skill`, `foldlock_fold-preview`, `foldlock_unfold-preview`
- Session exec is in-process (`engine_digest`). Proxy is not exec.
- Product skill cites DOI `10.5281/zenodo.22257762` (preprint also describes WhistleLock; this product is FoldLock only).

```bash
curl -s -A 'Mozilla/5.0' https://foldlock-download-tracker.vibelock.workers.dev/v1/health
curl -s -A 'Mozilla/5.0' -X POST https://foldlock-download-tracker.vibelock.workers.dev/v1/fold-preview \
  -H 'content-type: application/json' -d '{"text":"the cat and the dog"}'
curl -s -A 'Mozilla/5.0' -X POST https://aziel-runtime.vibelock.workers.dev/p/foldlock/fold-preview \
  -H 'content-type: application/json' -d '{"text":"the cat and the dog"}'
```

## AZ-CLCE toolkit (0.3.0)

Cross-Layer Consistency Engine (R/D/P Jaccard) plus SPRE. In-process engine on aziel-runtime. Author Aziel Eliab.

**THIS IS:** inconsistency detection + structural SPRE score. Type D is a label only. Two of three Aziel triad verifiers (PhysLing lives in aziel-corpus).

**THIS IS NOT:** a finding of malice, a guilt or conspiracy verdict, a scanner of other people's systems, a truth verdict, or a VPN.

- Host: https://azclce-download-tracker.vibelock.workers.dev
- Skill: `GET https://azclce-download-tracker.vibelock.workers.dev/v1/skill`
- Health: `GET https://azclce-download-tracker.vibelock.workers.dev/v1/health`
- OpenAPI: `GET https://azclce-download-tracker.vibelock.workers.dev/openapi.json`
- Download: `GET https://azclce-download-tracker.vibelock.workers.dev/download`
- Catalog aliases: `https://aziel-runtime.vibelock.workers.dev/p/azclce/{health,skill,score,classify,gate}`
- MCP tools: `azclce_health`, `azclce_skill`, `azclce_score`, `azclce_classify`, `azclce_gate`
- Session exec is in-process (`engine_digest`). Proxy is not exec.

```bash
curl -s -A 'Mozilla/5.0' https://azclce-download-tracker.vibelock.workers.dev/v1/health
curl -s -A 'Mozilla/5.0' -X POST https://aziel-runtime.vibelock.workers.dev/p/azclce/score \
  -H 'content-type: application/json' \
  -d '{"r":"login button blue","d":"login form submits","p":"login button submits"}'
```

## AZ-OS toolkit (0.3.0)

Prefab ethics-coded overlay. Integrity precedes execution. Author Aziel Eliab.

**THIS IS:** principle-bound sessions and a local desktop overlay. Hosted `/v1/status` is read-only.

**THIS IS NOT:** a kernel, bootloader, hypervisor, worm, unrestricted host bash, or SSH. Hosted invite prints principles; exec requires a local token. Halt does not kill the caller OS.

- Host: https://azos-download-tracker.vibelock.workers.dev
- Skill: `GET https://azos-download-tracker.vibelock.workers.dev/v1/skill`
- Health: `GET https://azos-download-tracker.vibelock.workers.dev/v1/health`
- OpenAPI: `GET https://azos-download-tracker.vibelock.workers.dev/openapi.json`
- Download: `GET https://azos-download-tracker.vibelock.workers.dev/download`
- Catalog aliases: `https://aziel-runtime.vibelock.workers.dev/p/azos/{health,skill,status}`
- MCP tools: `azos_health`, `azos_skill`, `azos_status`

```bash
curl -s -A 'Mozilla/5.0' https://azos-download-tracker.vibelock.workers.dev/v1/health
curl -s -A 'Mozilla/5.0' -X POST https://aziel-runtime.vibelock.workers.dev/p/azos/status \
  -H 'content-type: application/json' -d '{}'
```

## AZAI toolkit (0.3.1)

Local OpenAI-compatible stack on an Ollama base with JEEVES. Hosted `/v1` is Lamb check only. In-process Lamb engine on aziel-runtime. Author Aziel Eliab.

**THIS IS:** true local AI (`azai serve`). JEEVES is the ethics/assistant layer. Lamb Lens first. Jeeves is not sovereign.

**THIS IS NOT:** a new foundation model, GPT, a hosted paid-key proxy, or a sovereign agent. Hosted `/v1` does not run Ollama and does not spend paid keys.

- Host: https://azai-download-tracker.vibelock.workers.dev
- Skill: `GET https://azai-download-tracker.vibelock.workers.dev/v1/skill`
- Health: `GET https://azai-download-tracker.vibelock.workers.dev/v1/health`
- OpenAPI: `GET https://azai-download-tracker.vibelock.workers.dev/openapi.json`
- Download: `GET https://azai-download-tracker.vibelock.workers.dev/download`
- Catalog aliases: `https://aziel-runtime.vibelock.workers.dev/p/azai/{health,skill,lamb-check,lamb_check}`
- MCP tools: `azai_health`, `azai_skill`, `azai_lamb-check`, `azai_lamb_check`
- Session exec is in-process for Lamb only (`engine_digest`). Proxy is not exec.

```bash
curl -s -A 'Mozilla/5.0' https://azai-download-tracker.vibelock.workers.dev/v1/health
curl -s -A 'Mozilla/5.0' -X POST https://aziel-runtime.vibelock.workers.dev/p/azai/lamb-check \
  -H 'content-type: application/json' -d '{"text":"peace then clarity then service"}'
```

## AZBot toolkit (0.2.0)

This skill. Local runner for custom and Cursor `SKILL.md` files. Author Aziel Eliab.

**THIS IS:** a skill plus local runner. Hosted `/v1/skill` returns markdown.

**THIS IS NOT:** a foundation model, Grok weights, a kernel, a VPN, or a paid-key proxy.

- Host: https://azbot-download-tracker.vibelock.workers.dev
- Skill: `GET https://azbot-download-tracker.vibelock.workers.dev/v1/skill`
- Health: `GET https://azbot-download-tracker.vibelock.workers.dev/v1/health`
- OpenAPI: `GET https://azbot-download-tracker.vibelock.workers.dev/openapi.json`
- Download: `GET https://azbot-download-tracker.vibelock.workers.dev/download` → `azbot-0.2.0.tar.gz`
- Catalog aliases: `https://aziel-runtime.vibelock.workers.dev/p/azbot/{health,skill}`
- MCP tools: `azbot_health`, `azbot_skill`

```bash
curl -s -A 'Mozilla/5.0' https://azbot-download-tracker.vibelock.workers.dev/v1/health
curl -s -A 'Mozilla/5.0' https://azbot-download-tracker.vibelock.workers.dev/v1/skill
```

## Aziel Digital Library toolkit (catalog 2.6.2 / live 2.7.0)

Public MASTER corpus + hosted intelligence tools. Anonymous GET is read-only. Author Aziel Eliab.

**THIS IS:** Aziel Digital Library (search, records, map, gazetteer, counted zip, PhysLing Review, triad, hosted Whisper + mandatory VibeLock, Ask Jeeves). Live skill: **v2.7.0**. Catalog still lists **2.6.2**.

**THIS IS NOT:** a 26-card software index. Not Zenodo. Not a mesh. Not a guilt engine. Not private-file search for anonymous callers.

- Host: https://www.azielcorpuslibrary.net
- Fallback Worker: https://aziel-corpus-download-tracker.vibelock.workers.dev
- Skill: `GET https://www.azielcorpuslibrary.net/v1/skill`
- Health: `GET https://www.azielcorpuslibrary.net/v1/health`
- OpenAPI: `GET https://www.azielcorpuslibrary.net/openapi.json`
- Download: `GET https://www.azielcorpuslibrary.net/download`
- Catalog aliases: `https://aziel-runtime.vibelock.workers.dev/p/aziel-corpus/{health,skill,search,example}`
- MCP tools: `aziel-corpus_health`, `aziel-corpus_skill`, `aziel-corpus_search`, `aziel-corpus_example`
- Library also publishes (front door): `/v1/review`, `/v1/lattice`, `/v1/score`, `/v1/jeeves/chat`, `/ocr`, `/transcribe`, `/software`, `/runtime/*`

```bash
curl -s -A 'Mozilla/5.0' https://www.azielcorpuslibrary.net/v1/health
curl -s -A 'Mozilla/5.0' 'https://www.azielcorpuslibrary.net/v1/search?q=Florence'
curl -s -A 'Mozilla/5.0' https://aziel-runtime.vibelock.workers.dev/p/aziel-corpus/example
```

## ChronoLock toolkit (0.1.0)

Timezone-aware Temporal Neutral Window (08:30–10:30 local). Advisory hygiene. Distinct from TemporalLock and StaticClock. Author Aziel Eliab.

**THIS IS:** one advisory for a last-known geo + Top-30 anchors.

**THIS IS NOT:** a scheduler, targeting, virality, user-profiling, or a cron that posts.

- Host: https://chronolock-download-tracker.vibelock.workers.dev
- Skill: `GET https://chronolock-download-tracker.vibelock.workers.dev/v1/skill`
- Health: `GET https://chronolock-download-tracker.vibelock.workers.dev/v1/health`
- OpenAPI: `GET https://chronolock-download-tracker.vibelock.workers.dev/openapi.json`
- Download: `GET https://chronolock-download-tracker.vibelock.workers.dev/download`
- Catalog aliases: `https://aziel-runtime.vibelock.workers.dev/p/chronolock/{health,skill,advisory,anchors}`
- MCP tools: `chronolock_health`, `chronolock_skill`, `chronolock_advisory`, `chronolock_anchors`

```bash
curl -s -A 'Mozilla/5.0' https://chronolock-download-tracker.vibelock.workers.dev/v1/health
curl -s -A 'Mozilla/5.0' -X POST https://aziel-runtime.vibelock.workers.dev/p/chronolock/advisory \
  -H 'content-type: application/json' -d '{"geo":"Indiana","language":"English"}'
```

## CodeLock toolkit (0.1.0)

Gate-tethered cognitive rendering of source text. Author Aziel Eliab.

**THIS IS:** perception rendering. It alters perception, not meaning.

**THIS IS NOT:** a claim that meaning changed, a compiler, or a semantic rewriter.

- Host: https://codelock-download-tracker.vibelock.workers.dev
- Skill: `GET https://codelock-download-tracker.vibelock.workers.dev/v1/skill`
- Health: `GET https://codelock-download-tracker.vibelock.workers.dev/v1/health`
- OpenAPI: `GET https://codelock-download-tracker.vibelock.workers.dev/openapi.json`
- Download: `GET https://codelock-download-tracker.vibelock.workers.dev/download`
- Catalog aliases: `https://aziel-runtime.vibelock.workers.dev/p/codelock/{health,skill,render}`
- MCP tools: `codelock_health`, `codelock_skill`, `codelock_render`

```bash
curl -s -A 'Mozilla/5.0' https://codelock-download-tracker.vibelock.workers.dev/v1/health
curl -s -A 'Mozilla/5.0' -X POST https://aziel-runtime.vibelock.workers.dev/p/codelock/render \
  -H 'content-type: application/json' -d '{"text":"sample"}'
```

## DecisionGATE toolkit (0.1.0)

Five sequential gates before you act. In-process engine on aziel-runtime. Author Aziel Eliab.

**THIS IS:** a lightweight ethical pre-execution filter (PASS / REVISE / BLOCK). Freedom without clarity is chaos.

**THIS IS NOT:** a predictor, a court, a truth score, advice, or a hosted command runner.

- Host: https://decisiongate-download-tracker.vibelock.workers.dev
- Skill: `GET https://decisiongate-download-tracker.vibelock.workers.dev/v1/skill`
- Health: `GET https://decisiongate-download-tracker.vibelock.workers.dev/v1/health`
- OpenAPI: `GET https://decisiongate-download-tracker.vibelock.workers.dev/openapi.json`
- Download: `GET https://decisiongate-download-tracker.vibelock.workers.dev/download`
- Catalog aliases: `https://aziel-runtime.vibelock.workers.dev/p/decisiongate/{health,skill,check}`
- MCP tools: `decisiongate_health`, `decisiongate_skill`, `decisiongate_check`
- Session exec is in-process (`engine_digest`). Proxy is not exec.

```bash
curl -s -A 'Mozilla/5.0' https://decisiongate-download-tracker.vibelock.workers.dev/v1/health
curl -s -A 'Mozilla/5.0' -X POST https://aziel-runtime.vibelock.workers.dev/p/decisiongate/check \
  -H 'content-type: application/json' -d '{"proposal":"publish the receipt"}'
```

## EmployeeLock toolkit (0.1.0)

Hash-chained accountability workbook. Hosted never stores xlsx. Author Aziel Eliab.

**THIS IS:** workbook + hash chain (COVER, LOG, EVIDENCE, CHAIN, OWNERS, DASH, LISTS) + local CLI.

**THIS IS NOT:** a court, UL, a truth score, counsel, or a charge sheet. Demo rows are format proof, not case facts.

- Host: https://employeelock-download-tracker.vibelock.workers.dev
- Skill: `GET https://employeelock-download-tracker.vibelock.workers.dev/v1/skill`
- Health: `GET https://employeelock-download-tracker.vibelock.workers.dev/v1/health`
- OpenAPI: `GET https://employeelock-download-tracker.vibelock.workers.dev/openapi.json`
- Download: `GET https://employeelock-download-tracker.vibelock.workers.dev/download`
- Catalog aliases: `https://aziel-runtime.vibelock.workers.dev/p/employeelock/{health,skill,append-preview,verify-canonical}`
- MCP tools: `employeelock_health`, `employeelock_skill`, `employeelock_append-preview`, `employeelock_verify-canonical`

```bash
curl -s -A 'Mozilla/5.0' https://employeelock-download-tracker.vibelock.workers.dev/v1/health
curl -s -A 'Mozilla/5.0' https://aziel-runtime.vibelock.workers.dev/p/employeelock/skill
```

## ForgeReceipts toolkit (0.3.0)

Local receipt / checklist helper. Jurisdiction-aware state picker (50 states + federal baseline). Author Aziel Eliab.

**THIS IS:** local-first evidence integrity packaging. Hosted `/v1` never stores files.

**THIS IS NOT:** legal advice, a court filing, counsel, or Odyssey/email/cloud contact.

- Host: https://forgereceipts-download-tracker.vibelock.workers.dev
- Skill: `GET https://forgereceipts-download-tracker.vibelock.workers.dev/v1/skill`
- Health: `GET https://forgereceipts-download-tracker.vibelock.workers.dev/v1/health`
- OpenAPI: `GET https://forgereceipts-download-tracker.vibelock.workers.dev/openapi.json`
- Download: `GET https://forgereceipts-download-tracker.vibelock.workers.dev/download`
- Catalog aliases: `https://aziel-runtime.vibelock.workers.dev/p/forgereceipts/{health,skill,receipt}`
- MCP tools: `forgereceipts_health`, `forgereceipts_skill`, `forgereceipts_receipt`

```bash
curl -s -A 'Mozilla/5.0' https://forgereceipts-download-tracker.vibelock.workers.dev/v1/health
curl -s -A 'Mozilla/5.0' -X POST https://aziel-runtime.vibelock.workers.dev/p/forgereceipts/receipt \
  -H 'content-type: application/json' -d '{"sha256":"0"}'
```

## Glossa Filter toolkit (0.1.0)

Deterministic linguistic mediation into peer renders. Human opinion remains human. Author Aziel Eliab.

**THIS IS:** the same intent rendered across bundled peer ids.

**THIS IS NOT:** concealment, a live translator API, authorship stamping, or a claim that tools hold opinions.

- Host: https://glossafilter-download-tracker.vibelock.workers.dev
- Skill: `GET https://glossafilter-download-tracker.vibelock.workers.dev/v1/skill`
- Health: `GET https://glossafilter-download-tracker.vibelock.workers.dev/v1/health`
- OpenAPI: `GET https://glossafilter-download-tracker.vibelock.workers.dev/openapi.json`
- Download: `GET https://glossafilter-download-tracker.vibelock.workers.dev/download`
- Catalog aliases: `https://aziel-runtime.vibelock.workers.dev/p/glossafilter/{health,skill,render}`
- MCP tools: `glossafilter_health`, `glossafilter_skill`, `glossafilter_render`

```bash
curl -s -A 'Mozilla/5.0' https://glossafilter-download-tracker.vibelock.workers.dev/v1/health
curl -s -A 'Mozilla/5.0' -X POST https://aziel-runtime.vibelock.workers.dev/p/glossafilter/render \
  -H 'content-type: application/json' \
  -d '{"channel":"tooling","intent":{"what":"release","action":"publish"}}'
```

## GodLock toolkit (0.1.0)

ABAD / hardening score + public board. Product name, not an identity label. Author Aziel Eliab.

**THIS IS:** a resilience / weighing engine. Public board: https://godlock.uk/

**THIS IS NOT:** a VPN, ghost net, or anonymity tool. Do not claim mesh or VPN on godlock.uk.

- Host: https://godlock-download-tracker.vibelock.workers.dev
- Public board: https://godlock.uk/
- Skill: `GET https://godlock-download-tracker.vibelock.workers.dev/v1/skill`
- Health: `GET https://godlock-download-tracker.vibelock.workers.dev/v1/health` · `GET https://godlock.uk/health`
- OpenAPI: `GET https://godlock-download-tracker.vibelock.workers.dev/openapi.json`
- Download: `GET https://godlock-download-tracker.vibelock.workers.dev/download`
- Catalog aliases: `https://aziel-runtime.vibelock.workers.dev/p/godlock/{health,skill,score,submit}`
- MCP tools: `godlock_health`, `godlock_skill`, `godlock_score`, `godlock_submit`

```bash
curl -s -A 'Mozilla/5.0' https://godlock.uk/health
curl -s -A 'Mozilla/5.0' https://godlock-download-tracker.vibelock.workers.dev/v1/skill
curl -s -A 'Mozilla/5.0' -X POST https://aziel-runtime.vibelock.workers.dev/p/godlock/score \
  -H 'content-type: application/json' -d '{"text":"sample"}'
```

## M.I.A.Lock toolkit (0.1.1)

Purpose-bound missing-person investigative assist. Doe leads ≠ ID. Coverage heat ≠ presence. No live tracking. No restricted LE scraping. Author Aziel Eliab.

**THIS IS:** documented historical pins, ranked Doe compatibility leads, adapter coverage reports, and map layers.

**THIS IS NOT:** live location tracking, an identification, a crawler of restricted law-enforcement systems, or automated accusation.

- Host: https://mialock-download-tracker.vibelock.workers.dev
- Skill: `GET https://mialock-download-tracker.vibelock.workers.dev/v1/skill`
- Health: `GET https://mialock-download-tracker.vibelock.workers.dev/v1/health`
- OpenAPI: `GET https://mialock-download-tracker.vibelock.workers.dev/openapi.json`
- Download: `GET https://mialock-download-tracker.vibelock.workers.dev/download` → `mialock-0.1.1.tar.gz`
- Catalog aliases: `https://aziel-runtime.vibelock.workers.dev/p/mialock/{health,skill,map,search-options,queries,doe-match,coverage,example}`
- MCP tools: `mialock_health`, `mialock_skill`, `mialock_map`, `mialock_search-options`, `mialock_queries`, `mialock_doe-match`, `mialock_coverage`, `mialock_example`
- Local map: `python -m mialock map` — uncertainty ellipses + coverage heat; `doe_cold` mode shows lead cards

```bash
curl -s -A 'Mozilla/5.0' https://mialock-download-tracker.vibelock.workers.dev/v1/health
curl -s -A 'Mozilla/5.0' https://mialock-download-tracker.vibelock.workers.dev/v1/skill
curl -s -A 'Mozilla/5.0' -X POST -H 'Content-Type: application/json' \
  -d '{"subject":"subj-elena-cold-demo"}' \
  https://mialock-download-tracker.vibelock.workers.dev/v1/doe-match
curl -s -A 'Mozilla/5.0' 'https://mialock-download-tracker.vibelock.workers.dev/v1/coverage?subject=subj-elena-cold-demo'
curl -s -A 'Mozilla/5.0' https://aziel-runtime.vibelock.workers.dev/p/mialock/example
```

## MirageGrid toolkit (0.2.0)

Node-mesh circuit assigner. Hosted mapping is ephemeral. Author Aziel Eliab.

**THIS IS:** (product skill) a node-mesh VPN / anonymity network description (peers, circuits, SOCKS5). Hosted `/v1/assign` assigns a session node / circuit id.

**THIS IS NOT:** a crime tool, a log-wipe, or a guarantee against a global adversary. Hosted assign does not grant anonymity.

- Host: https://miragegrid-download-tracker.vibelock.workers.dev
- Skill: `GET https://miragegrid-download-tracker.vibelock.workers.dev/v1/skill`
- Health: `GET https://miragegrid-download-tracker.vibelock.workers.dev/v1/health`
- OpenAPI: `GET https://miragegrid-download-tracker.vibelock.workers.dev/openapi.json`
- Download: `GET https://miragegrid-download-tracker.vibelock.workers.dev/download`
- Catalog aliases: `https://aziel-runtime.vibelock.workers.dev/p/miragegrid/{health,skill,assign}`
- MCP tools: `miragegrid_health`, `miragegrid_skill`, `miragegrid_assign`

```bash
curl -s -A 'Mozilla/5.0' https://miragegrid-download-tracker.vibelock.workers.dev/v1/health
curl -s -A 'Mozilla/5.0' -X POST https://aziel-runtime.vibelock.workers.dev/p/miragegrid/assign \
  -H 'content-type: application/json' -d '{}'
```

## Post-King Chess toolkit (0.1.0)

Asymmetric continuity chess. Human is king-bound; AI has a Node, not a king. Author Aziel Eliab.

**THIS IS:** a game where the goal is to remain. Hosted AI is a 1-ply subset.

**THIS IS NOT:** standard chess, a rating engine, or a claim that the goal is to win.

- Host: https://postking-download-tracker.vibelock.workers.dev
- Skill: `GET https://postking-download-tracker.vibelock.workers.dev/v1/skill`
- Health: `GET https://postking-download-tracker.vibelock.workers.dev/v1/health`
- OpenAPI: `GET https://postking-download-tracker.vibelock.workers.dev/openapi.json`
- Download: `GET https://postking-download-tracker.vibelock.workers.dev/download`
- Catalog aliases: `https://aziel-runtime.vibelock.workers.dev/p/postking/{health,skill,new,move,status}`
- MCP tools: `postking_health`, `postking_skill`, `postking_new`, `postking_move`, `postking_status`

```bash
curl -s -A 'Mozilla/5.0' https://postking-download-tracker.vibelock.workers.dev/v1/health
curl -s -A 'Mozilla/5.0' -X POST https://aziel-runtime.vibelock.workers.dev/p/postking/new \
  -H 'content-type: application/json' -d '{"difficulty":"steward","seed":1}'
```

## ShadowLock toolkit (0.2.0)

Gate on an outcome you already have. Zero-retention observe. Author Aziel Eliab.

**THIS IS:** a counterfactual observation envelope with hashed ids.

**THIS IS NOT:** a people profiler, PII store, truth score, kernel hook, or process controller. No OS hook. No process intercept.

- Host: https://shadowlock-download-tracker.vibelock.workers.dev
- Skill: `GET https://shadowlock-download-tracker.vibelock.workers.dev/v1/skill`
- Health: `GET https://shadowlock-download-tracker.vibelock.workers.dev/v1/health`
- OpenAPI: `GET https://shadowlock-download-tracker.vibelock.workers.dev/openapi.json`
- Download: `GET https://shadowlock-download-tracker.vibelock.workers.dev/download`
- Catalog aliases: `https://aziel-runtime.vibelock.workers.dev/p/shadowlock/{health,skill,observe}`
- MCP tools: `shadowlock_health`, `shadowlock_skill`, `shadowlock_observe`

```bash
curl -s -A 'Mozilla/5.0' https://shadowlock-download-tracker.vibelock.workers.dev/v1/health
curl -s -A 'Mozilla/5.0' -X POST https://aziel-runtime.vibelock.workers.dev/p/shadowlock/observe \
  -H 'content-type: application/json' \
  -d '{"observed":{"id":"job-1","outcome":"done"},"counterfactual":{"outcome":"skipped"}}'
```

## SpectralLock toolkit (0.3.0)

Rosetta spectral overlays. Hosted overlay is a 256px preview. Author Aziel Eliab.

**THIS IS:** advisory visualization — lenses, overlays, ink/page modes aligned with library OCR.

**THIS IS NOT:** a lab spectrometer, forensic ink proof, a court exhibit, or a claim of authenticity. The human still reads the page.

- Host: https://spectrallock-download-tracker.vibelock.workers.dev
- Skill: `GET https://spectrallock-download-tracker.vibelock.workers.dev/v1/skill`
- Health: `GET https://spectrallock-download-tracker.vibelock.workers.dev/v1/health`
- OpenAPI: `GET https://spectrallock-download-tracker.vibelock.workers.dev/openapi.json`
- Download: `GET https://spectrallock-download-tracker.vibelock.workers.dev/download`
- Catalog aliases: `https://aziel-runtime.vibelock.workers.dev/p/spectrallock/{health,skill,modes,overlay}`
- MCP tools: `spectrallock_health`, `spectrallock_skill`, `spectrallock_modes`, `spectrallock_overlay`

```bash
curl -s -A 'Mozilla/5.0' https://spectrallock-download-tracker.vibelock.workers.dev/v1/health
curl -s -A 'Mozilla/5.0' https://aziel-runtime.vibelock.workers.dev/p/spectrallock/modes
```

## StaticClock toolkit (0.2.0)

Action-based immutable gear-click timeline. Time only locks forward. Distinct from ChronoLock. Author Aziel Eliab.

**THIS IS:** advisory / click-lock fields for a geo or an action. Hosted does not store a chain.

**THIS IS NOT:** a scheduler you set, a rollback clock, or ChronoLock.

- Host: https://staticclock-download-tracker.vibelock.workers.dev
- Skill: `GET https://staticclock-download-tracker.vibelock.workers.dev/v1/skill`
- Health: `GET https://staticclock-download-tracker.vibelock.workers.dev/v1/health`
- OpenAPI: `GET https://staticclock-download-tracker.vibelock.workers.dev/openapi.json`
- Download: `GET https://staticclock-download-tracker.vibelock.workers.dev/download`
- Catalog aliases: `https://aziel-runtime.vibelock.workers.dev/p/staticclock/{health,skill,advise}`
- MCP tools: `staticclock_health`, `staticclock_skill`, `staticclock_advise`

```bash
curl -s -A 'Mozilla/5.0' https://staticclock-download-tracker.vibelock.workers.dev/v1/health
curl -s -A 'Mozilla/5.0' -X POST https://aziel-runtime.vibelock.workers.dev/p/staticclock/advise \
  -H 'content-type: application/json' -d '{"geo":"Indiana"}'
```

## TemporalLock toolkit (0.2.0)

Hash-chained receipts anyone can verify. Explicit genesis, append, verify. Distinct from ChronoLock. Author Aziel Eliab.

**THIS IS:** an immutable timeslate lattice. Receipts, not truth claims. Hosted API is stateless.

**THIS IS NOT:** a kernel, scheduler, truth score, court, remote shell, or legal chain of custody.

- Host: https://temporallock-download-tracker.vibelock.workers.dev
- Skill: `GET https://temporallock-download-tracker.vibelock.workers.dev/v1/skill`
- Health: `GET https://temporallock-download-tracker.vibelock.workers.dev/v1/health`
- OpenAPI: `GET https://temporallock-download-tracker.vibelock.workers.dev/openapi.json`
- Download: `GET https://temporallock-download-tracker.vibelock.workers.dev/download`
- Catalog aliases: `https://aziel-runtime.vibelock.workers.dev/p/temporallock/{health,skill,genesis,append,verify}`
- MCP tools: `temporallock_health`, `temporallock_skill`, `temporallock_genesis`, `temporallock_append`, `temporallock_verify`

```bash
curl -s -A 'Mozilla/5.0' https://temporallock-download-tracker.vibelock.workers.dev/v1/health
curl -s -A 'Mozilla/5.0' https://aziel-runtime.vibelock.workers.dev/p/temporallock/skill
```

## The ARK toolkit (0.1.0)

Local deniable vault. Hosted never unlocks or stores vaults. In-process sweep/levels on aziel-runtime. Author Aziel Eliab.

**THIS IS:** a local vault. Sweep on the Worker is Mode E heuristics only (PE/ELF/Mach-O, powershell -enc, curl|sh). No clamscan.

**THIS IS NOT:** a kernel, bootable OS, worm, or hosted unlock. Hosted `/v1` never stores phrases or vaults.

- Host: https://ark-download-tracker.vibelock.workers.dev
- Skill: `GET https://ark-download-tracker.vibelock.workers.dev/v1/skill`
- Health: `GET https://ark-download-tracker.vibelock.workers.dev/v1/health`
- OpenAPI: `GET https://ark-download-tracker.vibelock.workers.dev/openapi.json`
- Download: `GET https://ark-download-tracker.vibelock.workers.dev/download`
- Catalog aliases: `https://aziel-runtime.vibelock.workers.dev/p/ark/{health,skill,sweep,levels}`
- MCP tools: `ark_health`, `ark_skill`, `ark_sweep`, `ark_levels`
- Session exec is in-process (`engine_digest`). Proxy is not exec.

```bash
curl -s -A 'Mozilla/5.0' https://ark-download-tracker.vibelock.workers.dev/v1/health
curl -s -A 'Mozilla/5.0' https://aziel-runtime.vibelock.workers.dev/p/ark/levels
```

## TrajectoryLock toolkit (0.1.0)

Auditable geometric trajectory test. Hosted never stores media. Author Aziel Eliab.

**THIS IS:** a research prototype. Compatibility vs a declared official line. P(match | declared model).

**THIS IS NOT:** a certified forensic instrument; shooter / intent / guilt ID. Synthetic example results must never be represented as real-case findings.

- Host: https://trajectorylock-download-tracker.vibelock.workers.dev
- Skill: `GET https://trajectorylock-download-tracker.vibelock.workers.dev/v1/skill`
- Health: `GET https://trajectorylock-download-tracker.vibelock.workers.dev/v1/health`
- OpenAPI: `GET https://trajectorylock-download-tracker.vibelock.workers.dev/openapi.json`
- Download: `GET https://trajectorylock-download-tracker.vibelock.workers.dev/download`
- Catalog aliases: `https://aziel-runtime.vibelock.workers.dev/p/trajectorylock/{health,skill,example,analyze}`
- MCP tools: `trajectorylock_health`, `trajectorylock_skill`, `trajectorylock_example`, `trajectorylock_analyze`

```bash
curl -s -A 'Mozilla/5.0' https://trajectorylock-download-tracker.vibelock.workers.dev/v1/health
curl -s -A 'Mozilla/5.0' https://aziel-runtime.vibelock.workers.dev/p/trajectorylock/example
```

## VeilLock toolkit (0.2.0)

Privacy veil on the user's own camera / screen. Author Aziel Eliab.

**THIS IS:** local steps for YOUR camera/screen. Catalog op is `apps`.

**THIS IS NOT:** FaceTime / Zoom / Meet / Teams / Skype inject. Not a call interceptor. Not a VPN.

- Host: https://veillock-download-tracker.vibelock.workers.dev
- Skill: `GET https://veillock-download-tracker.vibelock.workers.dev/v1/skill`
- Health: `GET https://veillock-download-tracker.vibelock.workers.dev/v1/health`
- OpenAPI: `GET https://veillock-download-tracker.vibelock.workers.dev/openapi.json`
- Download: `GET https://veillock-download-tracker.vibelock.workers.dev/download`
- Catalog aliases: `https://aziel-runtime.vibelock.workers.dev/p/veillock/{health,skill,apps}`
- MCP tools: `veillock_health`, `veillock_skill`, `veillock_apps`

```bash
curl -s -A 'Mozilla/5.0' https://veillock-download-tracker.vibelock.workers.dev/v1/health
curl -s -A 'Mozilla/5.0' -X POST https://aziel-runtime.vibelock.workers.dev/p/veillock/apps \
  -H 'content-type: application/json' -d '{}'
```

## VibeLock toolkit (0.3.0)

Physical-consistency evaluation of speech audio. Risk assessment. Author Aziel Eliab.

**THIS IS:** a multi-signal detector (local CLI + hosted advisory `/v1/analyze`).

**THIS IS NOT:** courtroom proof, a liveness detector, a live microphone, or face recognition.

- Host: https://vibelock-download-tracker.vibelock.workers.dev
- Skill: `GET https://vibelock-download-tracker.vibelock.workers.dev/v1/skill`
- Health: `GET https://vibelock-download-tracker.vibelock.workers.dev/v1/health`
- OpenAPI: `GET https://vibelock-download-tracker.vibelock.workers.dev/openapi.json`
- Download: `GET https://vibelock-download-tracker.vibelock.workers.dev/download`
- Catalog aliases: `https://aziel-runtime.vibelock.workers.dev/p/vibelock/{health,skill,analyze}`
- MCP tools: `vibelock_health`, `vibelock_skill`, `vibelock_analyze`

```bash
curl -s -A 'Mozilla/5.0' https://vibelock-download-tracker.vibelock.workers.dev/v1/health
curl -s -A 'Mozilla/5.0' -X POST https://aziel-runtime.vibelock.workers.dev/p/vibelock/analyze \
  -H 'content-type: application/json' \
  -d '{"features":{"rms":0.08,"zcr":0.07}}'
```

## WhistleLock toolkit (0.1.0)

Local drop ledger + dead-man copy. The operator moves released packets. Author Aziel Eliab.

**THIS IS:** a local folder that hashes a file you already have and chains the row.

**THIS IS NOT:** a mailer. Hosted never holds whistle files. It does not hide IP or scrape inboxes.

- Host: https://whistlelock-download-tracker.vibelock.workers.dev
- Skill: `GET https://whistlelock-download-tracker.vibelock.workers.dev/v1/skill`
- Health: `GET https://whistlelock-download-tracker.vibelock.workers.dev/v1/health`
- OpenAPI: `GET https://whistlelock-download-tracker.vibelock.workers.dev/openapi.json`
- Download: `GET https://whistlelock-download-tracker.vibelock.workers.dev/download`
- Catalog aliases: `https://aziel-runtime.vibelock.workers.dev/p/whistlelock/{health,skill,hash-preview,canon-preview}`
- MCP tools: `whistlelock_health`, `whistlelock_skill`, `whistlelock_hash-preview`, `whistlelock_canon-preview`
- Product skill cites DOI `10.5281/zenodo.22257762` (preprint also covers FoldLock; this product is WhistleLock only).

```bash
curl -s -A 'Mozilla/5.0' https://whistlelock-download-tracker.vibelock.workers.dev/v1/health
curl -s -A 'Mozilla/5.0' https://aziel-runtime.vibelock.workers.dev/p/whistlelock/skill
```

## ZionPattern Solver toolkit (catalog 0.2.0 / live skill 0.4.0)

Provisional interrogation helper. Hard 75% confidence cap / 25% uncertainty floor. In-process engine on aziel-runtime. Author Aziel Eliab.

**THIS IS:** pattern list + scored answers. Seed vols 1–5 baseline 75. Assistive only.

**THIS IS NOT:** a solver of Zioncheck, a court, a truth score, or a final historical conclusion.

- Host: https://zsolver-download-tracker.vibelock.workers.dev
- Skill: `GET https://zsolver-download-tracker.vibelock.workers.dev/v1/skill`
- Health: `GET https://zsolver-download-tracker.vibelock.workers.dev/v1/health`
- OpenAPI: `GET https://zsolver-download-tracker.vibelock.workers.dev/openapi.json`
- Download: `GET https://zsolver-download-tracker.vibelock.workers.dev/download`
- Catalog aliases: `https://aziel-runtime.vibelock.workers.dev/p/zsolver/{health,skill,patterns,score,session}`
- MCP tools: `zsolver_health`, `zsolver_skill`, `zsolver_patterns`, `zsolver_score`, `zsolver_session`
- Session exec is in-process (`engine_digest`). Proxy is not exec.

```bash
curl -s -A 'Mozilla/5.0' https://zsolver-download-tracker.vibelock.workers.dev/v1/health
curl -s -A 'Mozilla/5.0' https://aziel-runtime.vibelock.workers.dev/p/zsolver/patterns
```

## Catalog + local UI

Author: **Aziel Eliab**. Honest scope: Skill, not a foundation model. Hosted `/v1/skill` returns markdown. Jeeves is not sovereign. Front-door tether to godlock.uk, azielcorpuslibrary.net, and aziel-runtime — metadata scrape OK; never backdoor.

- Catalog product: https://aziel-runtime.vibelock.workers.dev/p/azbot/
- Catalog OpenAPI: https://aziel-runtime.vibelock.workers.dev/openapi.json
- Catalog MCP: `POST https://aziel-runtime.vibelock.workers.dev/mcp`
- This Worker skill: `GET https://azbot-download-tracker.vibelock.workers.dev/v1/skill`
- This Worker OpenAPI: https://azbot-download-tracker.vibelock.workers.dev/openapi.json
- GodLock board: https://godlock.uk/
- Library: https://www.azielcorpuslibrary.net/
- Runtime: https://www.azielcorpuslibrary.net/runtime · https://aziel-runtime.vibelock.workers.dev/

Local UI: **Import JSON file** (`type=file`) and **Export JSON**. Then `azbot doctor`.

```bash
curl -fsSL https://azbot-download-tracker.vibelock.workers.dev/install.sh | bash
azbot ui
azbot doctor
```

Grok: import catalog or Worker OpenAPI as a custom tool. ChatGPT: GPT Actions. Venice: HTTP tools.
