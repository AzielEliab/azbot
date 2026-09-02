from azbot import LIMITATION, OPENAPI, skill_text
from azbot.cli import main


def test_skill_is_honest() -> None:
    text = skill_text().lower()
    for word in ("aziel-runtime", "spectrallock", "lamb", "not a kernel", "spectrometer", "jeeves"):
        assert word in text
    assert "openapi.json" in skill_text()


def test_limitation() -> None:
    low = LIMITATION.lower()
    assert "skill" in low and "model" in low
    assert OPENAPI.endswith("/openapi.json")


def test_cli_skill(capsys) -> None:
    assert main(["skill"]) == 0
    out = capsys.readouterr().out
    assert "aziel-runtime" in out
    assert "AZBot" in out
