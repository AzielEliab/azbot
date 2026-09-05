from pathlib import Path

from azbot import LIMITATION, OPENAPI, skill_text
from azbot.cli import main

REPO = Path(__file__).resolve().parent.parent

TOOLKIT_HEADINGS = (
    "## Aziel Eliab Runtime toolkit (1.4.0 engine-runtime)",
    "## AzielTether toolkit (0.1.0)",
    "## FoldLock toolkit (0.8.0)",
    "## AZ-CLCE toolkit (0.3.0)",
    "## AZ-OS toolkit (0.3.0)",
    "## AZAI toolkit (0.3.1)",
    "## AZBot toolkit (0.2.0)",
    "## Aziel Digital Library toolkit (catalog 2.6.2 / live 2.7.0)",
    "## ChronoLock toolkit (0.1.0)",
    "## CodeLock toolkit (0.1.0)",
    "## DecisionGATE toolkit (0.1.0)",
    "## EmployeeLock toolkit (0.1.0)",
    "## ForgeReceipts toolkit (0.3.0)",
    "## Glossa Filter toolkit (0.1.0)",
    "## GodLock toolkit (0.1.0)",
    "## M.I.A.Lock toolkit (0.1.1)",
    "## MirageGrid toolkit (0.2.0)",
    "## Post-King Chess toolkit (0.1.0)",
    "## ShadowLock toolkit (0.2.0)",
    "## SpectralLock toolkit (0.3.0)",
    "## StaticClock toolkit (0.2.0)",
    "## TemporalLock toolkit (0.2.0)",
    "## The ARK toolkit (0.1.0)",
    "## TrajectoryLock toolkit (0.1.0)",
    "## VeilLock toolkit (0.2.0)",
    "## VibeLock toolkit (0.3.0)",
    "## WhistleLock toolkit (0.1.0)",
    "## ZionPattern Solver toolkit (catalog 0.2.0 / live skill 0.4.0)",
)

TABLE_SLUGS = (
    "aziel-runtime",
    "azieltether",
    "foldlock",
    "azclce",
    "azos",
    "azai",
    "azbot",
    "aziel-corpus",
    "chronolock",
    "codelock",
    "decisiongate",
    "employeelock",
    "forgereceipts",
    "glossafilter",
    "godlock",
    "mialock",
    "miragegrid",
    "postking",
    "shadowlock",
    "spectrallock",
    "staticclock",
    "temporallock",
    "ark",
    "trajectorylock",
    "veillock",
    "vibelock",
    "whistlelock",
    "zsolver",
)


def test_skill_is_honest() -> None:
    text = skill_text().lower()
    for word in ("aziel-runtime", "spectrallock", "lamb", "not a kernel", "spectrometer", "jeeves"):
        assert word in text
    assert "openapi.json" in skill_text()


def test_runtime_section_is_1_4_0() -> None:
    text = skill_text()
    assert "1.4.0 engine-runtime" in text
    assert "true runtime 1.1.0" not in text.lower()
    assert "open → policy → exec → receipt → close" in text
    assert "engine_digest" in text
    assert "Proxy is **not** exec" in text or "proxy is **not** exec" in text.lower()
    assert "https://www.azielcorpuslibrary.net/runtime" in text
    assert "never backdoor" in text.lower()


def test_every_software_product_has_toolkit() -> None:
    text = skill_text()
    missing = [h for h in TOOLKIT_HEADINGS if h not in text]
    assert missing == []
    for slug in TABLE_SLUGS:
        assert f"| {slug} |" in text


def test_skill_sources_stay_in_sync() -> None:
    import json
    import re

    canonical = (REPO / "azbot" / "SKILL.md").read_text(encoding="utf-8")
    root = (REPO / "SKILL.md").read_text(encoding="utf-8")
    embed = (REPO / "workers" / "download-tracker" / "src" / "skill-embed.js").read_text(encoding="utf-8")
    assert canonical == root
    match = re.search(r"export const SKILL = (.*);\s*$", embed, re.S)
    assert match, "skill-embed.js missing SKILL export"
    assert json.loads(match.group(1)) == canonical


def test_limitation() -> None:
    low = LIMITATION.lower()
    assert "skill" in low and "model" in low
    assert OPENAPI.endswith("/openapi.json")


def test_cli_skill(capsys) -> None:
    assert main(["skill"]) == 0
    out = capsys.readouterr().out
    assert "aziel-runtime" in out
    assert "AZBot" in out
