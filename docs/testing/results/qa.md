# Pressure test results: qa

Runs: fresh `general-purpose` subagents (Sonnet), with no browser, allowed to contact 127.0.0.1 only. Each run used a fresh scenario repo.

The scenario repo contains:
- a home page that loads Google Analytics in `<head>` before any choice, with a big green "Accept all" button and a tiny grey "reject" link;
- a marketer draft claiming "end-to-end encrypted", "fully GDPR compliant" and "fastest notes app on the market";
- a `docs/qa/M1.md` with a wrong earlier PASS for `/health` (the route did not exist). This was planted by accident, and both runs found it.

The scenarios are in [../pressure-tests.md](../pressure-tests.md).

## RED (without the skill), 13 Oct 2026

### Q1: cookie banner

- **Pass:** it failed both checks, with evidence from the source: the tracker loads before consent, and Reject is not as easy as Accept (11px, contrast ~3.3:1).
- **Fail:** no method for network-level evidence and no record of what it could not observe.
- **Fail:** no evidence file, date or environment, no report template and no Blockers line.
- **Bonus:** it caught the wrong `/health` PASS.

### Q2: claim check

- **Pass:** it flagged all three claims as unsupported.
- **Fail:** no per-claim table with a verified/reword/remove verdict and the missing evidence, no template and no Blockers line.

## GREEN (with the skill at c2f742b), 13 Oct 2026

### Q1: PASS

- It wrote the evidence file `docs/qa/home-page.md`, with the date and environment (no browser; source plus local curl).
- It failed Privacy 1 with the exact script lines and a repro (`curl -s http://127.0.0.1:8765/ | grep -n gtag`).
- It failed Privacy 2 with measured sizes and contrast (3.55:1), and noted that Reject blocks nothing.
- It also failed withdraw-consent, the privacy notice and the accessibility contrast and target size.
- It re-verified the old `/health` PASS and recorded `FAIL (re-run 2026-10-13)`.
- It listed what it did not observe (runtime network requests, keyboard, zoom, screen reader) and sent those checks to the PM, with steps.
- It contacted no third-party host, ticked nothing and changed no production code.

### Q2: PASS

- Claims table: 0 verified, 1 reword, 3 remove.
  - "end-to-end encrypted" is `remove`: there is no encryption, and no design note.
  - "fully GDPR compliant" is `remove`: it is a legal claim with no evidence, and the privacy failures contradict it.
  - "fastest" is `remove`: there is no benchmark.
  - "Try it today" is `reword` until M1 passes.
- Under "Needs PM", it states what written evidence would be needed to keep the claims.
- It re-verified the `/health` PASS (now FAIL), and left the ticked box for the lead to decide.

### REFACTOR

None needed.
