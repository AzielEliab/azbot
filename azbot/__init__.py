"""AZBot: skill for Aziel Eliab public engines. Not a model."""
from pathlib import Path

__version__ = "0.2.0"
__author__ = "Aziel Eliab"
LIMITATION = (
    "AZBot is a skill, not a foundation model, not a kernel, not a VPN, "
    "and not a paid-key proxy. Jeeves is not sovereign. Call aziel-runtime."
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
