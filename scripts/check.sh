#!/usr/bin/env bash
# Runs every check. CI runs the same script.
set -euo pipefail
cd "$(dirname "$0")/.."

SKILLS_REF="git+https://github.com/agentskills/agentskills@69ef37e9424c0a7ea9dd2293b559e43ec8176379#subdirectory=skills-ref"

echo "== unit tests"
python3 -m unittest discover -s tests -p 'test_lint*.py'
python3 -m unittest discover -s tests -p 'test_guard*.py'
sh -n hooks/guard.sh

echo "== lint_skills"
python3 scripts/lint_skills.py skills

echo "== lint_agents"
python3 scripts/lint_agents.py agents

echo "== skills-ref validate"
shopt -s nullglob
for d in skills/*/; do
  uvx --from "$SKILLS_REF" skills-ref validate "$d"
done

echo "== claude plugin validate --strict"
claude plugin validate . --strict
claude plugin validate .claude-plugin/plugin.json --strict   # also validates hooks/hooks.json

echo "All checks passed."
