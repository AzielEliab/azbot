# AZBot download tracker

Isolated counter Worker `azbot-download-tracker`, project `azbot`, KV `AZBOT_DOWNLOADS`.

GET `/` increments views and serves the homepage (download buttons + suite Live Nodes strip).
GET `/download` increments downloads and serves the gzip (HTTP 200, no 302).
GET `/count` returns `{project, views, downloads, total}`.
GET `/v1/skill` returns skill markdown. Does not increment.
GET `/v1/fraggate/list`, GET `/v1/fraggate/describe`, POST `/v1/fraggate/call` PROXY to aziel-runtime via the `AZIEL_RUNTIME` service binding. Not local ops.
`/v1/mesh/*` PROXY to aziel-runtime suite mesh (`AZIEL_RUNTIME`). Default OFF. QNM-BUILD-1.0 live|locked|isolated. No Node Gate. No auto-heal. Not anonymity. Human UI Live Nodes strip polls `GET /v1/mesh`.
GET `/mcp` returns dual-surface MCP pointer (catalog MCP + FragGate `slug=mesh`). Not a second MCP. Does not increment.

## QNS-CD-1.0

Cross-map only. Not a new product. Not a Softwares-tab engine.

Companion to QNM-BUILD-1.0. Local qnsd lives in [qnm-node](https://github.com/AzielEliab/qnm-node). Design: [QNS-CD-1.0](https://github.com/AzielEliab/aziel-runtime/blob/main/docs/designs/QNS-CD-1.0.md). This Worker cites/proxies suite mesh. Photon QNS1 vias stay on local qnsd (`127.0.0.1`). Restriction walks next via class. `GET /v1/mesh` never enables. No Node Gate. No local qnsd HTTP on this public Worker.

Author: Aziel Eliab. Apache-2.0.
