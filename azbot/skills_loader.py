"""Discover and manage Cursor-style SKILL.md files plus custom AZbot skills.

AZBot prints and stores skill markdown. It does not ship Grok model weights.
Execution is local operator instructions.
"""
from __future__ import annotations

import os
import re
import shutil
from dataclasses import dataclass
from pathlib import Path

FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*", re.DOTALL)
SLUG_RE = re.compile(r"[^a-z0-9]+")


@dataclass(frozen=True)
class Skill:
    name: str
    description: str
    path: Path
    body: str
    source: str

    @property
    def slug(self) -> str:
        return slugify(self.name)


def slugify(name: str) -> str:
    slug = SLUG_RE.sub("-", name.strip().lower()).strip("-")
    return slug or "skill"


def find_root(start: Path | None = None) -> Path:
    candidates: list[Path] = []
    if start is not None:
        candidates.append(Path(start).resolve())
    env_root = os.environ.get("AZBOT_ROOT")
    if env_root:
        candidates.append(Path(env_root).expanduser().resolve())
    candidates.append(Path.cwd().resolve())
    candidates.append(Path(__file__).resolve().parent.parent)
    seen: set[Path] = set()
    for base in candidates:
        for p in [base, *base.parents]:
            if p in seen:
                continue
            seen.add(p)
            if (p / "pyproject.toml").is_file() and (p / "azbot").is_dir():
                return p
            if (p / "standalone" / "skill" / "SKILL.md").is_file():
                return p
            if (p / "skills").is_dir() and (p / "azbot").is_dir():
                return p
    return Path.cwd().resolve()


def parse_skill_md(path: Path, source: str = "file") -> Skill | None:
    path = Path(path)
    if not path.is_file():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None
    meta = _parse_simple_yaml(match.group(1))
    name = str(meta.get("name") or "").strip()
    description = str(meta.get("description") or "").strip()
    if not name or not description:
        return None
    return Skill(name=name, description=description, path=path.resolve(), body=text, source=source)


def _parse_simple_yaml(block: str) -> dict[str, str]:
    data: dict[str, str] = {}
    current: str | None = None
    for raw in block.splitlines():
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if current and (raw.startswith(" ") or raw.startswith("\t")):
            extra = line.strip().strip('"').strip("'")
            if extra:
                data[current] = (data.get(current, "") + " " + extra).strip()
            continue
        if ":" not in line:
            current = None
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        if not key or key.startswith("-"):
            current = None
            continue
        value = value.strip()
        if value in {">", "|", ">-", "|-"}:
            data[key] = ""
            current = key
            continue
        if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
            value = value[1:-1]
        data[key] = value
        current = key
    return data


def _skill_files(root: Path) -> list[tuple[str, Path]]:
    found: list[tuple[str, Path]] = []
    skills_dir = root / "skills"
    if skills_dir.is_dir():
        direct = skills_dir / "SKILL.md"
        if direct.is_file():
            found.append(("skills", direct))
        for child in sorted(skills_dir.iterdir()):
            if not child.is_dir() or child.name == "cursor":
                continue
            md = child / "SKILL.md"
            if md.is_file():
                found.append(("skills", md))
    bundled = root / "standalone" / "skill" / "SKILL.md"
    if bundled.is_file():
        found.append(("bundled", bundled))
    extra = os.environ.get("AZBOT_SKILLS_DIR")
    if extra:
        extra_path = Path(extra).expanduser()
        if extra_path.is_file() and extra_path.name == "SKILL.md":
            found.append(("env", extra_path))
        elif extra_path.is_dir():
            for md in sorted(extra_path.rglob("SKILL.md")):
                found.append(("env", md))
    cursor_skills = root / ".cursor" / "skills"
    if cursor_skills.is_dir():
        for md in sorted(cursor_skills.rglob("SKILL.md")):
            found.append(("cursor", md))
    vendored = root / "skills" / "cursor"
    if vendored.is_dir():
        for md in sorted(vendored.rglob("SKILL.md")):
            found.append(("vendored-cursor", md))
    return found


def discover_skills(root: Path | None = None) -> list[Skill]:
    root = Path(root).resolve() if root is not None else find_root()
    out: list[Skill] = []
    seen_paths: set[Path] = set()
    seen_names: set[str] = set()
    for source, path in _skill_files(root):
        resolved = path.resolve()
        if resolved in seen_paths:
            continue
        skill = parse_skill_md(path, source=source)
        if skill is None:
            continue
        key = skill.name.strip().lower()
        if key in seen_names:
            continue
        seen_paths.add(resolved)
        seen_names.add(key)
        out.append(skill)
    return out


def get_skill(name: str, root: Path | None = None) -> Skill:
    needle = name.strip().lower()
    slug = slugify(name)
    for skill in discover_skills(root):
        if skill.name.strip().lower() == needle or skill.slug == slug:
            return skill
    raise KeyError(f"skill not found: {name}")


def import_skill(src: Path, root: Path | None = None) -> Skill:
    src = Path(src).expanduser().resolve()
    if src.name != "SKILL.md" and src.suffix.lower() not in {".md", ".markdown"}:
        # still allow any markdown file that has frontmatter
        pass
    skill = parse_skill_md(src, source="import")
    if skill is None:
        raise ValueError("SKILL.md needs YAML frontmatter with name and description")
    dest_root = Path(root).resolve() if root is not None else find_root()
    dest_dir = dest_root / "skills" / skill.slug
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / "SKILL.md"
    if src.resolve() != dest.resolve():
        shutil.copy2(src, dest)
    imported = parse_skill_md(dest, source="skills")
    if imported is None:
        raise ValueError("imported SKILL.md is missing name or description")
    return imported


def export_skill(name: str, dest: Path | None = None, root: Path | None = None) -> Path | str:
    skill = get_skill(name, root=root)
    if dest is None:
        return skill.body
    dest = Path(dest)
    if dest.suffix.lower() not in {".md", ".markdown"} and dest.is_dir():
        dest = dest / f"{skill.slug}.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(skill.body, encoding="utf-8")
    return dest


def skills_as_dicts(root: Path | None = None) -> list[dict[str, str]]:
    rows = []
    base = Path(root).resolve() if root is not None else find_root()
    for skill in discover_skills(root):
        try:
            rel = str(skill.path.relative_to(base))
        except ValueError:
            rel = str(skill.path)
        rows.append({
            "name": skill.name,
            "description": skill.description,
            "source": skill.source,
            "path": rel,
            "slug": skill.slug,
        })
    return rows
