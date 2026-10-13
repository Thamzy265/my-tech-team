#!/usr/bin/env bash
# Runs every check. CI runs the same script.
set -euo pipefail
cd "$(dirname "$0")/.."

SKILLS_REF="git+https://github.com/agentskills/agentskills@69ef37e9424c0a7ea9dd2293b559e43ec8176379#subdirectory=skills-ref"

echo "== unit tests"
python3 -m unittest discover -s tests -p 'test_lint*.py'

echo "== lint_skills"
python3 scripts/lint_skills.py skills

echo "== skills-ref validate"
shopt -s nullglob
for d in skills/*/; do
  uvx --from "$SKILLS_REF" skills-ref validate "$d"
done

echo "== claude plugin validate --strict"
claude plugin validate . --strict

echo "All checks passed."
