#!/usr/bin/env python3
"""Lint my-tech-team plugin agents (agents/*.md): models, effort, skills and tool limits."""
import re
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


def unquote(item):
    item = item.strip()
    if len(item) >= 2 and item[0] == item[-1] and item[0] in "\"'":
        item = item[1:-1]
    return item.strip()


def split_items(value):
    """Split 'a, b' or '[a, b]' into items; commas inside parentheses stay put."""
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        value = value[1:-1]
    items, depth, cur = [], 0, ""
    for ch in value:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == "," and depth == 0:
            items.append(cur)
            cur = ""
        else:
            cur += ch
    items.append(cur)
    return [unquote(i) for i in items if i.strip()]


def parse(text):
    """Return frontmatter as {key: str or list}. Only the YAML subset the agents use.

    Lines that are not 'key: value', indented, or '- item' raise ValueError so the
    linter fails loudly instead of passing on a misread file."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("must start with '---' frontmatter")
    try:
        end = lines.index("---", 1)
    except ValueError:
        raise ValueError("frontmatter is not closed with '---'")
    meta, key = {}, None
    for n, raw in enumerate(lines[1:end], start=2):
        line = re.sub(r"(^|\s)#.*$", "", raw).rstrip()
        if not line.strip():
            continue
        item = line.strip()
        if item.startswith("- ") or item == "-":
            if key is None:
                raise ValueError(f"cannot parse line {n}: {raw!r}")
            if not isinstance(meta.get(key), list):
                meta[key] = []
            meta[key].append(unquote(item[1:]))
        elif line.startswith((" ", "\t")):
            continue
        else:
            name, sep, value = line.partition(":")
            if not sep or not re.fullmatch(r"[A-Za-z][\w-]*", name.strip()):
                raise ValueError(f"cannot parse line {n}: {raw!r}")
            key = name.strip()
            value = value.strip()
            if value.startswith("[") and value.endswith("]"):
                meta[key] = split_items(value)
            elif key in ("tools", "skills"):
                meta[key] = split_items(value) if value else ""
            else:
                meta[key] = unquote(value)
    return meta


def as_list(value):
    if isinstance(value, list):
        return value
    return split_items(value or "")


def base_name(tool):
    return tool.split("(", 1)[0].strip()


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
    tools = [base_name(t) for t in as_list(meta.get("tools"))] if "tools" in meta else None
    if name in NO_WRITE | NO_SHELL | NEEDS_SKILL_TOOL and tools is None:
        errors.append(f"{path}: {name} must set tools")
    if name == "qa" and "tools" in meta:
        errors.append(f"{path}: qa must not set tools (it would drop the browser and simulator tools)")
    if name == "scout" and "skills" in meta:
        errors.append(f"{path}: scout must not set skills")
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
