# AZBot Design for Node-Based Collaborative Forensic System

Zero-Trust AI × Human × Human Auditing Layer

**Author:** Aziel Eliab  
**Version:** Design 1.0 · October 2026  
**License:** Apache-2.0

Source PDF (same text): [AZBot-Node-Collaborative-Forensic-Design-1.0.pdf](AZBot-Node-Collaborative-Forensic-Design-1.0.pdf).

## 1. Purpose

AZBot is the local skill runner and AI interface that lets humans and AI collaborate inside the Aziel node mesh while preserving the existing zero-trust contract. It routes every request through FragGate, emits receipts into the shared lattice, and never becomes a second door or an unrestricted execution path.

It extends the current AZBot (v0.2.0) — a local skill catalog and OpenAPI/MCP client for aziel-runtime — so that it can participate in multi-party sessions on nodes without enabling public mesh radios or changing vault logic.

## 2. Position in the Platform

| Component | Role |
| --- | --- |
| AZ-OS | Ethics-gated session shell and closed-verb VFS on the node. |
| Aziel Runtime / FragGate | Single public door. Discovery, routing, refuse. |
| AZ Interface | Local control surface and pre-locked page cycles. |
| AZBot (this design) | Local AI handoff and skill runner that stays behind the gates. |

## 3. Node Role

On each node, AZBot runs locally (127.0.0.1). It does not open public ports. When a human or another node requests AI assistance inside a session:

- The request is presented to the local AZ-OS session.
- AZ-OS re-gates it (five ethics gates, ARC token if required, closed verb list).
- If the gate passes, AZBot packages the request as a FragGate call (slug + op + payload).
- The call returns a structured result + receipt.
- The receipt is appended to the session’s TemporalLock / ChainLock lattice.
- Other parties in the multi-party session can read the tip; they cannot rewrite it.

## 4. Constraints Preserved

This design adds node participation and multi-party receipt sharing. It does not rewrite the public contract.

| Remain-OFF item | Status |
| --- | --- |
| Mesh auto-enable / GET /v1/mesh | Still never enables |
| AZ-OS public exec / shell / lattice | Still refused |
| Vault destructive ops (ARK / EmbryoLock wipe, scorch, unlock) | Still local-only / FG-STUB |
| Deanonymize, invent_mark, backdate, public rollback | Still refused |
| FragGate single door | Unchanged |
| Local-first sessions | Unchanged |

## 5. Minimal Additions (No Feature Loss)

- Operator-gated mesh presence using existing MESH-NEED-BEARER and local qnm-node.
- Multi-party session object that shares receipt tips only.
- AZBot handoff that still travels through FragGate and produces a receipt.
- Existing tethers (AZRT-AZOS-TETHER, AzielTether under bearer, external anchors) used as specified.
- All currently live advisory Softwares remain live and unchanged.

## 6. Collaborative Flow

Human A (on Node 1) opens a session in AZ Interface → AZ-OS gates the request → AZBot (local) packages a FragGate call → Runtime routes to the appropriate Softwares engine → result + receipt returned → lattice updated → Human B (on Node 2) and the AI can read the verified tip. No node executes a refused verb. No public radio is auto-enabled.

Integrity precedes execution. The public identity is the work.

© 2026 Aziel Eliab · Apache-2.0
