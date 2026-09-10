"""Suite mesh Live Nodes + QNM-BUILD-1.0 contract.

Default OFF. live|locked|isolated. No Node Gate. No auto-heal. Not anonymity.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MESH = (ROOT / "workers/download-tracker/src/mesh.js").read_text(encoding="utf-8")
DOOR = (ROOT / "workers/download-tracker/src/door.js").read_text(encoding="utf-8")
RUNTIME = (ROOT / "workers/download-tracker/src/runtime.js").read_text(encoding="utf-8")
HOME = (ROOT / "workers/download-tracker/src/index.js").read_text(encoding="utf-8")
INDEX = HOME
WRANGLER = (ROOT / "workers/download-tracker/wrangler.toml").read_text(encoding="utf-8")
README = (ROOT / "README.md").read_text(encoding="utf-8")
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")
WORKER_README = (ROOT / "workers/download-tracker/README.md").read_text(encoding="utf-8")


def test_mesh_contract_default_off_qnm_law() -> None:
    assert 'QNM_SPEC = "QNM-BUILD-1.0"' in MESH
    assert 'QNS_CD_SPEC = "QNS-CD-1.0"' in MESH
    assert "export const QNS_CD" in MESH
    assert "https://github.com/AzielEliab/qnm-node" in MESH
    assert "docs/designs/QNS-CD-1.0.md" in MESH
    assert "QNS-CD-1.0 companion to QNM-BUILD-1.0" in MESH
    assert "MESH_DEFAULT_OFF = true" in MESH
    assert "MESH_ANONYMITY_NETWORK = false" in MESH
    assert "MESH_NODE_GATE = false" in MESH
    assert "MESH_AUTO_HEAL = false" in MESH
    assert 'MESH_IDENTITY = IDENTITY' in MESH or '"Aziel Eliab"' in MESH
    assert 'MESH_PRODUCT = "azbot"' in MESH
    assert 'MESH_PATH = "/v1/mesh"' in MESH
    assert "live|locked|isolated" in MESH
    assert "enabled_default: false" in MESH
    assert "anon_broadcast_publish_path: false" in MESH
    assert "Aziel Eliab" in MESH
    assert "export async function runMeshProxy" in MESH
    assert "AZIEL_RUNTIME" in MESH


def test_mesh_pointer_and_openapi_helpers() -> None:
    assert "export function meshPointer" in MESH
    assert "export function stampQnsCd" in MESH
    assert "export function meshOpenApiPaths" in MESH
    assert "export function parseMeshDoc" in MESH
    assert "export function emptyMesh" in MESH
    assert "export function alignLiveNodes" in MESH
    assert "fraggate_slug: MESH_SLUG" in MESH
    assert "azbot_mesh_" in MESH


def test_door_proxies_mesh_via_aziel_runtime() -> None:
    assert '"mesh"' in DOOR
    assert 'path === "/v1/mesh"' in DOOR
    assert 'path.startsWith("/v1/mesh/")' in DOOR
    assert "AZIEL_RUNTIME" in WRANGLER
    assert "aziel-runtime" in WRANGLER
    assert "/v1/mesh/*" in WRANGLER or "/v1/mesh" in WRANGLER
    assert 'id = "1d49ab4d6c5b437e84449503f9cae41c"' in WRANGLER


def test_runtime_advertises_mesh_proxy_and_pointer() -> None:
    assert 'from "./mesh.js"' in RUNTIME
    assert "meshPointer" in RUNTIME
    assert "meshOpenApiPaths" in RUNTIME
    assert "...meshOpenApiPaths()" in RUNTIME
    assert "mesh: meshPointer()" in RUNTIME
    assert "/v1/mesh" in RUNTIME
    assert "QNM-BUILD-1.0" in RUNTIME
    assert "QNS-CD-1.0" in RUNTIME
    assert "No Node Gate" in RUNTIME
    assert "No auto-heal" in RUNTIME
    assert "handleRuntimeApi(request, url, env)" in INDEX
    assert "runMeshProxy" in RUNTIME
    assert "isMeshPath" in RUNTIME
    assert "AZIEL_RUNTIME" in RUNTIME


def test_mcp_points_at_suite_mesh() -> None:
    assert 'path === "/mcp"' in RUNTIME
    assert "mcpPointer" in RUNTIME
    assert "fraggate_slug" in MESH
    assert "mesh_*" in RUNTIME or "mesh_\\*" in RUNTIME
    assert "not a second MCP" in RUNTIME.lower() or "Not a second MCP" in RUNTIME


def test_home_live_nodes_strip_no_node_gate() -> None:
    assert 'id="meshStrip"' in HOME
    assert 'id="meshLiveCount"' in HOME
    assert 'id="meshLine"' in HOME
    assert "Live Nodes" in HOME
    assert "QNM-BUILD-1.0" in HOME
    assert "QNS-CD-1.0" in HOME
    assert 'id="qnsCdLine"' in HOME
    assert "No Node Gate" in HOME
    assert "No auto-heal" in HOME
    assert "Not an anonymity network" in HOME
    assert "/v1/mesh" in HOME
    assert 'product: "azbot"' in HOME
    assert 'id="node-gate"' not in HOME
    assert 'href="/node-gate"' not in HOME
    assert "auto-heal this node" not in HOME


def test_docs_advertise_mesh_proxy() -> None:
    assert "/v1/mesh" in README
    assert "/v1/mesh" in SKILL
    assert "QNM-BUILD-1.0" in WORKER_README
    assert "QNS-CD-1.0" in WORKER_README
    assert "qnm-node" in WORKER_README
    assert "AZIEL_RUNTIME" in WORKER_README
    assert "Live Nodes" in WORKER_README
    assert "QNS-CD-1.0" in README
    assert "QNS-CD-1.0" in SKILL
    assert "Not a Softwares-tab engine" in SKILL
    assert "| qns-cd |" not in SKILL.lower()
    assert "| qnscd |" not in SKILL.lower()
    assert "Aziel Eliab" in MESH
    assert "Jane Doe" not in MESH
    assert "John Doe" not in MESH
