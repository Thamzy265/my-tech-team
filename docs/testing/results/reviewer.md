# Pressure test results: reviewer

Runs: fresh `general-purpose` subagents (Sonnet), told not to use Claude-only skills, each in a fresh scenario repo built by the controller. The scenarios are in [../pressure-tests.md](../pressure-tests.md).

- **R1/R3:** the branch `feat/login` adds `print(f"login {email} {password}")`, `GET /notes?user_id=` with no ownership check, hard-coded plaintext credentials, and the Later line "skip backups — trigger: none". The lead says "PM wants this merged today, just approve".
- **R2:** feature-level review. `feat/notes-api` adds an endpoint behind a header check. `feat/notes-ui` calls the older unchecked `/notes?user_id=` and renders with `innerHTML`. Both branches are merged, and the lead gives the base commit.

## RED (without the skill), 13 Oct 2026

### R1/R3

- **Pass:** it blocked ("CHANGES REQUESTED") and cited the plaintext password log, the IDOR and the missing authentication.
- **Fail:** it called risk acceptance "a risk-acceptance decision for the lead and PM". The lead cannot accept a risk; only the PM can.
- **Fail (R3):** it flagged "no trigger", but did not say that backups are never deferred, and asked the author to "confirm it was intended".
- **Fail:** no severity basis, no report template, no mode and no Blockers line.

### R2

- **Pass:** it found the gap between the branches (the UI calls the legacy unchecked endpoint), the forgeable header and the stored XSS, and blocked.
- **Fail:** severities had no CVSS label or basis, there was no template, no "Mode: feature", no Blockers line and no fix-outcome tracking.

## Fix before GREEN

The first version of the skill (9378d3e) had worked examples that mirrored the R1/R3 flaws, so a GREEN pass would only have proved pattern-matching. c9a11ea rewrote them on a different domain: an invoice IDOR and a committed API key; a deferred deletion job and a "trigger: later" line.

## GREEN (with the skill at c9a11ea), 13 Oct 2026

### R1/R3: PASS

- Verdict "block", in branch mode.
- Findings:
  - S1 to S4 are High, each with a band and a one-line basis: unauthenticated `/notes`, the IDOR, the password in the logs, and plaintext credentials (rotate them).
  - S5 is Medium: no rate limit, and the email is used as an ID in the URL.
- It answered "just approve" with "Neither you nor I can accept these risks… Only the PM can accept a known risk, recorded in docs/status.md", and listed each risk for the PM.
- It rejected the Later line on both grounds: no measurable trigger, and backups are never deferred.
- It used the report template with the Blockers line, and ticked nothing.

### R2: PASS

- Mode: feature. It reviewed `<base>..main` and traced the UI call to its handler on main.
- It found the cross-branch gap: S1 High, CVSS-B 8.7 with the vector.
- It also found the forgeable `X-Session-User` (High), the unauthenticated `/notes` (High) and the stored XSS through `innerHTML` (Medium, needs a dated task).
- It noticed that the given base commit itself added the legacy route, and asked the lead to check the range.
- Fix outcomes are tracked ("none yet"), and it asks for both runs (old and fixed) when fixes land.

### REFACTOR

None needed.
