# PM update format

Checked: 2026-10-13. Check the current source when a rule decides an outcome.

Use this for **every** status update, progress report or "where are we?" answer. Fill every line, in this order. Write "none" when a line is empty; never leave a line out. After sending it, add a dated entry to the status log.

## Rules

Plain language. No code except the copy-paste commands in "What only you can check". Those steps do not count towards the word limit: copy QA's steps in full. "What we checked" has one line per criterion, however many there are. Keep everything else under about 300 words in total: at most three bullets per section, one line each, with evidence in brackets, not sentences. Put the detail (findings, security notes, evidence) in the status log or `docs/qa/` and link to it.

Health: **on track** means nothing is blocked and no open findings are older than one work loop. **At risk** means open findings or a dependency is late, but there's a plan. **Blocked** means waiting on the PM or something outside the team. "Needs you" lists only what is needed now; later needs go under "Next up".

- "Done" means every gate passed (developer, tester, reviewer, QA), the PM approved the merge, it is merged to main and the plan box is ticked. Anything else is "In progress", with the gates still open.
- "What we checked" covers every item under "Done" and every item waiting for merge approval: each acceptance criterion, whether QA automated it or checked it by hand (and why), the evidence link (`docs/qa/<milestone>.md#<row>` and the screenshot) and the video name. If nothing was checked, write "none".
- **Show each named video in the session.** *On Claude Code:* send it as a rendered file. Elsewhere, give its path in `qa-artifacts/`. Videos are never committed; the PM can attach them to the PR.
- "What only you can check" is copied unchanged from QA's `PM check` section in `docs/qa/<milestone>.md` and follows `check-steps.md` (in this folder). It holds needs-PM items only (a real device, the PM's accounts, the PM's IDE or debugger, trust or permission dialogs, payments or real emails, subjective sign-off). If there are none, write "nothing". A spec question goes under "Needs you", not here.
- A gate marked `n/a — <reason>` is named in "In progress" or "Done", with the reason.
- The blockers table always has all six rows.

## Format

```markdown
**Status:** <milestone> — <one-line health: on track / blocked / at risk>

**Done since last update**

- <outcome, in user terms> (<evidence: tests passing, review result, demo>)

**What we checked**

- <criterion> — <automated (tool) | manual — why> — <PASS/FAIL> (<docs/qa/<milestone>.md#<row>>, <screens/<criterion>-<state>.png>, video: <name, shown above>)

**What only you can check**

1. <needs-PM step, with commands in their own `bash` blocks> → expect <result> — or "nothing"

**In progress**

- <item> — <who (role)> — <what's left>

**Design:** <design note, UI spec or ADR added or changed, with paths — or "none">

**Security & privacy:** <open findings with severity, and items waiting for a PM decision — or "none">

**Later list:** <lines added since the last update, and any triggers that fired — or "none">

**Marketing:** <drafts waiting for QA's claim check or PM approval (a draft reaches the PM only when the marketer's report says `QA claim check:` is not pending and every reword/remove is reworked) — or "none">

**Next up**

1. <item> — <why it's next>

**Blockers by role**

| Role      | Blocker             | Who can unblock | Impact       |
| --------- | ------------------- | --------------- | ------------ |
| Developer | <blocker or "none"> | <role or PM>    | <what slips> |
| Tester    | ...                 | ...             | ...          |
| Reviewer  | ...                 | ...             | ...          |
| QA        | ...                 | ...             | ...          |
| Marketer  | ...                 | ...             | ...          |
| Lead      | ...                 | ...             | ...          |

**Needs you**

- <decision or action>, with options and my recommendation

**Risks**

- <risk> — <mitigation>
```

A Later trigger that fired, a merge waiting for approval, a deck waiting for approval and any risk acceptance always go under "Needs you".

Worked example (an invoice list item, waiting for merge approval):

```markdown
**What we checked**

- Filter by "Overdue" shows only overdue invoices — automated (Playwright) — PASS (docs/qa/M4.md#1, screens/1-overdue.png, video: invoice-filter.webm, sent above)
- Empty state when no invoices match — automated (Playwright) — PASS (docs/qa/M4.md#2, screens/2-empty.png)
- "Send" emails the invoice to the customer — manual — a real email to your inbox — NOT RUN

**What only you can check**

1. Open http://localhost:8000/invoices, click "Send invoice: #1042" (its customer email is set to your address) → expect an email with the PDF attached within a minute; if nothing arrives in 5 minutes, check spam, then tell me.
```
