#!/usr/bin/env python3
"""Lint my-tech-team skills for rules the generic validators do not check."""
import re
import sys
from pathlib import Path

ALLOWED_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_LINES = 500
MAX_DESCRIPTION = 1024
# Leftovers from the FlutterDeck originals. The skills must stay generic.
BANNED = [
    re.compile(r"\bdeck-(lead|developer|tester|reviewer|qa)\b", re.I),
    re.compile(r"flutterdeck", re.I),
    re.compile(r"\bpnpm\b", re.I),
    re.compile(r"\bzod\b", re.I),
]
TEXT_SUFFIXES = {".md", ".html", ".py", ".sh", ".json", ".txt"}
BLOCK_SCALAR_RE = re.compile(r"^[>|][+-]?\d*$")
FILE_REF_RE = re.compile(r"(?<![\w/:.-])((?:references|assets|scripts)/[A-Za-z0-9._/-]+\.[a-z]+)")


def parse_frontmatter(text):
    """Return (top-level keys -> raw value, body). Only the YAML subset the skills use."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("SKILL.md must start with '---' frontmatter")
    try:
        end = lines.index("---", 1)
    except ValueError:
        raise ValueError("frontmatter is not closed with '---'")
    meta = {}
    for line in lines[1:end]:
        if not line.strip() or line.startswith((" ", "\t")):
            continue  # nested values (e.g. under metadata:)
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip().strip('"').strip("'")
    return meta, "\n".join(lines[end + 1:])


def lint_skill(skill_dir):
    skill_dir = Path(skill_dir)
    path = skill_dir / "SKILL.md"
    errors = []
    text = path.read_text()
    try:
        meta, body = parse_frontmatter(text)
    except ValueError as exc:
        return [f"{path}: {exc}"]

    name = meta.get("name", "")
    if not NAME_RE.match(name) or len(name) > 64:
        errors.append(f"{path}: invalid name '{name}'")
    if name != skill_dir.name:
        errors.append(f"{path}: name '{name}' does not match folder '{skill_dir.name}'")
    for key in sorted(set(meta) - ALLOWED_KEYS):
        errors.append(f"{path}: non-spec frontmatter key '{key}'")
    description = meta.get("description", "")
    if BLOCK_SCALAR_RE.match(description):
        errors.append(f"{path}: description must be a single line (block scalars '>' and '|' are not supported)")
    elif not 1 <= len(description) <= MAX_DESCRIPTION:
        errors.append(f"{path}: description must be 1-{MAX_DESCRIPTION} characters (got {len(description)})")
    line_count = len(text.splitlines())
    if line_count > MAX_LINES:
        errors.append(f"{path}: {line_count} lines; keep SKILL.md under {MAX_LINES}")
    for ref in sorted(set(FILE_REF_RE.findall(body))):
        if not (skill_dir / ref).is_file():
            errors.append(f"{path}: missing file {ref}")
    for md in sorted(f for f in skill_dir.rglob("*") if f.is_file() and f.suffix in TEXT_SUFFIXES):
        content = md.read_text()
        for pattern in BANNED:
            m = pattern.search(content)
            if m:
                errors.append(f"{md}: project-specific term '{m.group(0)}'")
    return errors


def main(argv):
    root = Path(argv[0]) if argv else Path(__file__).resolve().parent.parent / "skills"
    errors = []
    for skill_md in sorted(root.glob("*/SKILL.md")):
        errors.extend(lint_skill(skill_md.parent))
    for e in errors:
        print(e)
    print(f"lint_skills: {len(list(root.glob('*/SKILL.md')))} skills, {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
