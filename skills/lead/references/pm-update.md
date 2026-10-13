# PM update format

Checked: 2026-10-12. Check the current source when a rule decides an outcome.

Use this for **every** status update, progress report or "where are we?" answer. Fill every line, in this order. Write "none" when a line is empty; never leave a line out. After sending it, add a dated entry to the status log.

## Rules

Plain language. No code except the copy-paste commands in "How you can check it". "How you can check it" does not count towards the word limit: copy QA's steps in full. Keep everything else under about 300 words in total: at most three bullets per section, one line each, with evidence in brackets, not sentences. Put the detail (findings, security notes, evidence) in the status log or `docs/qa/` and link to it.

Health: **on track** means nothing is blocked and no open findings are older than one work loop. **At risk** means open findings or a dependency is late, but there's a plan. **Blocked** means waiting on the PM or something outside the team. "Needs you" lists only what is needed now; later needs go under "Next up".

- "Done" means every gate passed (developer, tester, reviewer, QA), the PM approved the merge, it is merged to main and the plan box is ticked. Anything else is "In progress", with the gates still open.
- "How you can check it" is copied from QA's `PM check` section in `docs/qa/<milestone>.md` and follows `check-steps.md` (in this folder), for every item under "Done". If nothing is done, write "none".
- A gate marked `n/a — <reason>` is named in "In progress" or "Done", with the reason.
- The blockers table always has all six rows.

## Format

```markdown
**Status:** <milestone> — <one-line health: on track / blocked / at risk>

**Done since last update**

- <outcome, in user terms> (<evidence: tests passing, review result, demo>)

**How you can check it**

1. <step, with commands in their own `bash` blocks> → expect <result>

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
