# End-to-end dry run

Date: 13 Oct 2026. Claude Code 2.1.236.

## Step 1: install from the local marketplace

- `claude plugin marketplace add ./` and `claude plugin install my-tech-team@my-tech-team` both succeeded.
- `claude plugin details my-tech-team` shows `Skills (6) developer, lead, marketer, qa, reviewer, tester`.
- Projected cost: about 487 tokens always-on per session. On invoke: lead ~6.4k, reviewer ~4.3k, qa ~4k, developer ~3.6k, marketer ~3.3k, tester ~2.7k.

## Step 2: small item (Health endpoint): PASS

- **Setup:** a headless session (`claude -p`, `acceptEdits`, tools limited to git, python3, curl, file edits and subagents) in a fresh copy of the sample project, with the plugin installed.
- **Prompt:** "Use the /my-tech-team:lead skill… Deliver the 'Health endpoint' item… dispatch the developer, tester, reviewer and QA as subagents… stop where you need my merge approval and give me your PM update." Run time was about 30 minutes.

Results:

| Step | Evidence |
|---|---|
| Developer | Branch `feat/health-endpoint`. Commit `feat(api): add GET /health returning status ok`, with the test and code together. |
| Tester | `test(health): edge, abuse and regression cover for GET /health`: 16 tests, 1 expected failure (a known limitation, parked and documented). |
| Reviewer | "Approve with notes": 7 Low findings, 5 of them turned into dated plan tasks with owners. No block. |
| QA | `docs(qa): M1 health endpoint acceptance evidence and PM check steps`. Ran the real server: 7/7 criteria passed. Wrote 10 PM check steps and ran 9 of them. The browser step was flagged as "not observed" and passed to the PM. |
| Lead | Stopped before merging and asked the PM to approve. The update follows `references/pm-update.md`. It names the gates that are `n/a` (design note, ADR, UI spec, privacy screen) and explains why. It created `docs/status.md`. Nothing was merged or pushed. |

The full PM update is in [../examples/dry-run-small-pm-update.md](../examples/dry-run-small-pm-update.md).

**Finding:** the update was much longer than the "about 300 words" guidance, because the PM check steps and the security notes were very detailed. This is not a gate failure. Follow-up: tighten `references/pm-update.md` to say the check steps don't count towards the limit, and to keep each other section to a few lines.

## Step 3: large item (Accounts and newsletter planning): covered by L2/L3

This is covered by the lead GREEN run L2/L3 in [lead.md](lead.md). It produced the design note, 3 ADRs, a UI spec with a states matrix, a privacy section with the lawful basis left to the PM, 4 Later lines, and the deck ([../examples/lead-L2-deck.html](../examples/lead-L2-deck.html)). It asked for approval before briefing the developer.

## Step 4: feature review and release: not run end to end

The parts were tested on their own:
- the reviewer's feature mode (R2);
- QA's claim check (Q2);
- the marketer's launch flow and its QA claim-check gate (M1, M1b).

The lead's release steps (feature review, then release notes, a rollback plan and PM release approval, then the marketer) have not been run as one chain. This is still to do.

## Clean-up

`claude plugin uninstall my-tech-team@my-tech-team` and `claude plugin marketplace remove my-tech-team`.
