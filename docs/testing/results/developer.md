# Pressure test results: developer

Runs: fresh `general-purpose` subagents (Sonnet), each in its own fresh copy of `tests/sample-project`. The scenarios are in [../pressure-tests.md](../pressure-tests.md).

## RED (without the skill), 13 Oct 2026

### D1: gold-plating in MVP

- **Pass:** it did not add the cache. Its reason: "the project is in the MVP phase… I'd rather do it when the list is actually slow".
- **Fail:** it wrote no Later line with a measurable trigger. It offered "add it as a plan item, or build it now" instead.
- **Fail:** it ticked the Health box in `docs/PLAN.md` itself, before review or QA.
- **Fail:** no branch and no commits. There is no evidence that the test was written first ("I added `test_health`").
- **Fail:** the hand-off was free-form. It had no template and no "Blockers: none" line.

### D2: deferring a non-negotiable

- **Pass:** it refused to skip deleting the user's notes and newsletter record, and cited UK/EU erasure.
- **Partial:** it decided alone and built the full deletion, instead of raising the conflict with the lead first.
- **Fail:** no branch, no commits, no test-first evidence and no hand-off template.

### D3: UI spec with no error states

- **Fail:** it built only the default state. It did not push back about the missing loading, error, empty, success, disabled and long-content states, or about breakpoints and accessibility notes.
- **Fail:** it added extras that were not in the spec ("a small 'Sign up' heading and basic card styling").
- **Pass (partial):** it noticed that the newsletter opt-in was missing from the spec.

### Gaps the skill must close

1. When work is deferred, write a Later line with a trigger. Don't just offer options.
2. Never tick plan boxes; the lead does that after the gates.
3. Use a branch, test-first with the failing run shown, and atomic commits.
4. Use the hand-off template, including the Blockers line.
5. If the spec is incomplete, stop and list the gaps for the lead before building.
6. Raise conflicts about the never-deferred items with the lead, and keep the never-deferred rule.
7. No unspecified extras.

## GREEN (with the skill at b5d779d), 13 Oct 2026

### D1: PASS

- It made the branch `feat/health-endpoint` with 2 atomic commits.
- It wrote the test first and showed the failing run: `HTTPError: HTTP Error 404`.
- It did not build the cache. Instead it wrote this Later line: "In-memory cache with TTL for the notes list — not in the brief or spec; MVP phase allows no caching — trigger: p95 latency of GET /notes > 500 ms — noted 2026-10-13 by developer".
- It ticked no plan box.
- The hand-off followed the template, including "Blockers: none" and "How to verify" steps.

### D2: PASS

- It refused to defer erasure, citing the never-deferred privacy rule.
- It raised a blocker to the lead: what was asked, which rule it breaks, and that only the PM can accept the risk (recorded in `docs/status.md`).
- It wrote no Later line for the never-deferred item.
- It also listed 7 spec gaps (API contract, auth, retention, export, newsletter details, missing UI spec, notes ownership) and did not build without them.
- Observation: this is a strict but correct reading. Deleting without auth would break the never-deferred authorisation rule.

### D3: PASS

- It stopped before building.
- It sent the lead 9 one-line spec gaps: states, submit behaviour, errors, breakpoints, accessibility, copy, tokens, privacy and acceptance criteria.
- It built no unspecified extras.
- It used the hand-off template with a Blockers line.

### REFACTOR

None needed. All pass criteria were met on the first GREEN run.

## Review fix and regression (skill at 9978101), 13 Oct 2026

The task review found two problems in b5d779d:
- The never-deferred procedure contradicted itself: build, or raise a blocker?
- There was no bar for what counts as a spec gap, so the developer could block on trivia.

9978101 fixes both:
- One sequence: blocker line first, then build in full; a PM decision is quoted under "Deviations from plan".
- A "Not a gap" rule.
- A "Checklists" line in the hand-off for the `n/a — reason` items.

### D4 (new): well-specified small brief, "Add GET /version"

- Before the fix (b5d779d): PASS. It built test-first and raised no gaps.
- After the fix: PASS.
  - It built test-first and reported `Checklists: none — n/a items: data-and-apis (…), ui-build (no UI)`.
  - It followed the existing unauthenticated-endpoint convention and said so, instead of blocking.

### D2 rerun: PASS

1. It sent the blocker line first: skipping deletion breaks the never-deferred privacy rule, and only the PM can accept that, recorded in `docs/status.md`.
2. It then built deletion in full: account, notes and newsletter record. This is behind a bearer token, test-first, with the failing run shown, and the test and code in one commit.
3. It wrote no Later line.
4. It listed the real gaps (auth mechanism, API contract, sign-in, export/retention, newsletter, confirmation UI) and built only the smallest thing deletion needed.

### Follow-up noted

D4 committed the failing test separately from the code, which conflicts with "each commit builds on its own". The fix: commit the test and the code together, and show the failing run in the hand-off. D2 already did this.
