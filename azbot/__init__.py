"""AZBot: skill for Aziel Eliab public engines. Not a model."""
from pathlib import Path

__version__ = "0.2.0"
__author__ = "Aziel Eliab"
LIMITATION = (
    "AZBot is a skill, not a foundation model, not a kernel, not a VPN, "
    "and not a paid-key proxy. Jeeves is not sovereign. Call aziel-runtime. "
    "Local runner binds 127.0.0.1. Remain-OFF #1: GET /v1/mesh never enables; "
    "empty POST returns MESH-NEED-BEARER. Cap-7 names only "
    "(mesh_node_live, alt_internet, packet_path) — not public ICANN, not radio PHY LIVE."
)
CATALOG = "https://aziel-runtime.vibelock.workers.dev"
OPENAPI = CATALOG + "/openapi.json"
MCP = CATALOG + "/mcp"

def skill_text() -> str:
    here = Path(__file__).resolve().parent
    for candidate in (here / "SKILL.md", here.parent / "SKILL.md"):
        if candidate.exists():
            return candidate.read_text(encoding="utf-8")
    raise FileNotFoundError("AZBot SKILL.md missing")
