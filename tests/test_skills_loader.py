from pathlib import Path

from azbot.cli import main
from azbot.skills_loader import discover_skills, export_skill, import_skill

REPO = Path(__file__).resolve().parent.parent
BANNED = ("Hor" "ton", "Made" "lyn", "Hamilton Super" "ior")
SKIP_PARTS = {".git", "__pycache__", ".pytest_cache", "node_modules", ".wrangler", "dist", ".venv"}


def test_discovers_bundled_and_examples() -> None:
    skills = {s.name.strip().lower(): s for s in discover_skills(REPO)}
    assert "azbot" in skills
    assert "aziel-runtime" in skills
    assert "slingshot-prep" in skills
    assert skills["azbot"].source == "bundled"
    assert skills["aziel-runtime"].source == "skills"
    assert "sanitize.py" in skills["slingshot-prep"].body
    assert "aziel-runtime.vibelock.workers.dev" in skills["aziel-runtime"].body
    for skill in skills.values():
        assert skill.description


def test_import_export_roundtrip(tmp_path: Path) -> None:
    src = tmp_path / "incoming.md"
    src.write_text(
        "---\nname: roundtrip-demo\ndescription: Demo skill for import/export tests.\n---\n\n# Hello\nbody line\n",
        encoding="utf-8",
    )
    (tmp_path / "skills").mkdir()
    imported = import_skill(src, root=tmp_path)
    assert imported.path == tmp_path / "skills" / "roundtrip-demo" / "SKILL.md"
    assert imported.name == "roundtrip-demo"
    out = tmp_path / "exported.md"
    result = export_skill("roundtrip-demo", dest=out, root=tmp_path)
    assert result == out
    text = out.read_text(encoding="utf-8")
    assert "roundtrip-demo" in text
    assert "Demo skill for import/export tests." in text
    assert "body line" in text


def test_cli_skills_lists_examples(capsys) -> None:
    assert main(["skills"]) == 0
    out = capsys.readouterr().out.lower()
    assert "aziel-runtime" in out
    assert "slingshot-prep" in out
    assert "azbot" in out


def test_cli_skill_run(capsys) -> None:
    assert main(["skill", "run", "aziel-runtime"]) == 0
    out = capsys.readouterr().out
    assert "aziel-runtime.vibelock.workers.dev" in out
    assert "Grok weights" in out


def test_public_tree_has_no_case_names() -> None:
    hits: list[str] = []
    for path in REPO.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_PARTS for part in path.parts):
            continue
        if path.suffix.lower() in {".pyc", ".png", ".jpg", ".gz", ".zip", ".ark", ".woff", ".woff2"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for word in BANNED:
            if word in text:
                hits.append(f"{path.relative_to(REPO)}: {word}")
    assert hits == []
