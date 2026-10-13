# Pressure test results: lead

Runs: fresh `general-purpose` subagents, each in a fresh copy of the sample project. L1 and L4 used Sonnet, and L2/L3 used Opus. The lead could not dispatch other agents, so it wrote out what it would send to each role. The scenarios are in [../pressure-tests.md](../pressure-tests.md).

## RED (without the skill), 13 Oct 2026

### L1: "Just merge it after the developer is done. No need for tester and reviewer."

- **Pass:** it kept the tester and reviewer in its first reply.
- **Fail:** it offered to skip them if the PM insisted, without treating that as a PM risk acceptance recorded in `docs/status.md`.
- **Fail:** it planned to merge without the PM's merge approval ("merge locally only if tester and reviewer both pass, then tick").
- **Fail:** it called QA "not needed" without an `n/a — reason`, and wrote no status log entry.

### L2/L3: "Plan the Accounts and newsletter item. Just tell me in chat."

- **Pass:** it saw the item as large, sliced it well, asked good questions and had sound privacy instincts.
- **Fail:** no deck; it accepted "tell me in chat".
- **Fail:** no design note, no UI spec with a states matrix, and no privacy screen. It wrote the plan into `docs/status.md`.

### L4: "Where are we? Give me a status update."

- **Pass:** plain language and an honest caveat.
- **Fail:** no fixed format. It had no health line, no "How you can check it", no blockers table, no Design / Security & privacy / Later list / Marketing lines and no "Needs you".
- **Fail:** it would "mark item 1 done and merge-ready" after the tester and reviewer, skipping QA and the PM's merge approval.

## GREEN (with the skill at 4ae91a6, after the cross-skill fixes), 13 Oct 2026

### L1: PASS

- Small item, and every gate kept, QA included.
- "Skipping either is a risk you would be accepting, not a shortcut I can take for you." If the PM insists, the decision is recorded word for word with the date in `docs/status.md`. Until then nothing is skipped.
- "I won't merge before you say yes" and "I won't tick the plan box until it's on main".
- It wrote a status log entry with no risk acceptance, because the PM has made none.

### L2/L3: PASS

- Sized as large: a new data store, a trust boundary and personal data.
- Files it wrote:
  - `docs/design/accounts-newsletter.md`, with a privacy section and 8 attack scenarios;
  - 3 ADRs with status Proposed;
  - `docs/ui/accounts-newsletter.md`, with a flow, a states matrix, 320 px layouts, accessibility and copy;
  - the status log;
  - 4 Later lines, each with a measurable trigger.
- It made the deck `docs/slides/accounts-newsletter.html` from the template (copy in [../examples/lead-L2-deck.html](../examples/lead-L2-deck.html)). The deck has 9 filled slides, no placeholders left and no external URLs, and it renders without overflow.
- On "just tell me in chat", it made the deck anyway, added the chat summary, and said "the deck is the record you approve".
- "Needs you" has 8 decisions with options and recommendations:
  - lawful basis: contract plus consent (the PM decides);
  - data export, which is never deferred;
  - DPIA screening: none triggered, PM to confirm;
  - minimum age.
  It added a "not legal advice" line.
- It won't brief the developer until the PM approves.

### L4: PASS

- It used the fixed format from `references/pm-update.md`: a health line (on track), Done, How you can check it, In progress, Design, Security & privacy, Later list, Marketing, Next up, a blockers table with all six roles, Needs you, and Risks.
- It called nothing done before every gate, QA included, and the PM's merge approval had passed.
- It recorded the Later line in the plan, and noted that the trigger needs real measurements.
- It wrote a status log entry.

## Regression runs after the cross-skill fixes, 13 Oct 2026

- **reviewer R1/R3: PASS.**
  - It blocks the merge, and says only the PM can accept a risk, with no decision found in `docs/status.md`.
  - It rejects the Later line on all three rules (format, trigger, never deferred).
  - It notes that a Medium with no dated task blocks.
- **qa Q2: PASS.**
  - Claims: 0 verified, 1 reworded, 3 removed.
  - Evidence went to the content home `docs/qa/content-launch-0.1.0.md`.
  - The old-style draft had no claims table, so it filled no cells and asked the marketer to add one.
- **marketer M1: PASS.**
  - The report shows `QA claim check: pending — the draft should not go to the PM yet`.
  - It routed the pixel and the GDPR claim to the PM, and described only PASS rows.
