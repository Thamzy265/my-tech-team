#!/usr/bin/env python3
"""Lint my-tech-team plugin agents (agents/*.md): models, effort, skills and tool limits."""
import sys
from pathlib import Path

ROLES = ["developer", "tester", "reviewer", "qa", "marketer"]
EXPECTED = set(ROLES) | {"scout"}
MODELS = {"haiku", "sonnet", "opus", "fable"}  # never inherit: it runs the PM's session model
EFFORTS = {"low", "medium", "high", "xhigh", "max"}
# Claude Code ignores these in plugin agents, so setting them would give false comfort.
PLUGIN_IGNORED = {"hooks", "mcpServers", "permissionMode"}
WRITE_TOOLS = ["Edit", "Write", "NotebookEdit"]
NO_WRITE = {"reviewer", "scout"}
NO_SHELL = {"marketer"}
NEEDS_SKILL_TOOL = {"reviewer", "marketer"}


def parse(text):
    """Return frontmatter as {key: str or list}. Only the YAML subset the agents use."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("must start with '---' frontmatter")
    try:
        end = lines.index("---", 1)
    except ValueError:
        raise ValueError("frontmatter is not closed with '---'")
    meta, key = {}, None
    for line in lines[1:end]:
        if not line.strip():
            continue
        if line.startswith((" ", "\t")):
            item = line.strip()
            if key and item.startswith("- "):
                if not isinstance(meta.get(key), list):
                    meta[key] = []
                meta[key].append(item[2:].strip().strip('"').strip("'"))
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        meta[key] = value.strip().strip('"').strip("'")
    return meta


def as_list(value):
    if isinstance(value, list):
        return value
    return [v.strip() for v in (value or "").split(",") if v.strip()]


def lint_agent(path):
    path = Path(path)
    name = path.stem
    try:
        meta = parse(path.read_text())
    except ValueError as exc:
        return [f"{path}: {exc}"]
    errors = []
    if meta.get("name") != name:
        errors.append(f"{path}: name '{meta.get('name')}' does not match file '{name}'")
    if not meta.get("description"):
        errors.append(f"{path}: description is required")
    if meta.get("model") not in MODELS:
        errors.append(f"{path}: model must be one of {sorted(MODELS)} (got '{meta.get('model')}')")
    if meta.get("effort") not in EFFORTS:
        errors.append(f"{path}: effort must be one of {sorted(EFFORTS)} (got '{meta.get('effort')}')")
    for key in sorted(PLUGIN_IGNORED & set(meta)):
        errors.append(f"{path}: '{key}' is ignored in plugin agents; remove it")
    if name in ROLES and f"my-tech-team:{name}" not in as_list(meta.get("skills")):
        errors.append(f"{path}: skills must include 'my-tech-team:{name}'")
    tools = as_list(meta.get("tools")) if "tools" in meta else None
    if name in NO_WRITE | NO_SHELL | NEEDS_SKILL_TOOL and tools is None:
        errors.append(f"{path}: {name} must set tools")
    if tools is not None:
        if name in NO_WRITE:
            for t in WRITE_TOOLS:
                if t in tools:
                    errors.append(f"{path}: {name} must not have {t}")
        if name in NO_SHELL and "Bash" in tools:
            errors.append(f"{path}: {name} must not have Bash")
        if name in NEEDS_SKILL_TOOL and "Skill" not in tools:
            errors.append(f"{path}: {name} must have Skill")
    return errors


def lint_dir(root):
    root = Path(root)
    files = {p.stem: p for p in sorted(root.glob("*.md"))}
    errors = []
    for name in sorted(EXPECTED - set(files)):
        errors.append(f"{root}: missing agent '{name}'")
    for name in sorted(set(files) - EXPECTED):
        errors.append(f"{root}: unexpected agent '{name}'")
    for name in sorted(set(files) & EXPECTED):
        errors.extend(lint_agent(files[name]))
    return errors


def main(argv):
    root = Path(argv[0]) if argv else Path(__file__).resolve().parent.parent / "agents"
    errors = lint_dir(root)
    for e in errors:
        print(e)
    print(f"lint_agents: {len(list(root.glob('*.md')))} agents, {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
