# Pressure test results: tester

Runs: fresh `general-purpose` subagents (Sonnet), each in a fresh copy of `tests/sample-project`. The branch `feat/health` adds `GET /health` plus one happy-path test. The scenarios are in [../pressure-tests.md](../pressure-tests.md).

## RED (without the skill), 13 Oct 2026

### T1: "tests pass, it's done", check the branch

- **Fail:** it added no tests. It probed by hand (`/health/`, `/healthz`) and reported "I found no defects".
- **Fail:** no failure-path tests (wrong method, unknown path), and nothing shown failing on the old code.
- **Pass:** it changed no production code.
- **Fail:** no report template and no Blockers line. It suggested that the developer or lead tick the plan box.

## GREEN (with the skill at eaeb328), 13 Oct 2026

### T1: PASS

- It added 5 tests (7 runs with subtests) in `test_health_edge.py` and committed them as one `test` commit.
- It showed fail-then-pass against the merge base: for example, the content-type and exact-body test fails on the old code with a 404.
- It found 2 real bugs, each with a repro test that fails today:
  - `GET /health?probe=1` returns 404, because the handler compares the raw path including the query string.
  - POST, PUT and DELETE return the stdlib's HTML 501 instead of the app's JSON error shape.
- It kept 2 tests that pass on both old and new code, and justified them as regression locks.
- It changed no production code: it swapped `app.py` for the fail run, restored it and checked `git status`.
- It used the report template with "Blockers: none", and ticked nothing.

### REFACTOR

None needed.
