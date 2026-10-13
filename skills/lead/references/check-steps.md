# "What only you can check" (after every finished task)

Checked: 2026-10-13. Check the current source when a rule decides an outcome.

Write steps only for the needs-PM list (real device, the PM's accounts, the PM's IDE or debugger, trust or permission dialogs, payments or real emails, subjective sign-off). Everything else is automated by QA and shown as evidence under "What we checked". If nothing is on the list, write "nothing".

For the items that are on the list, give the PM numbered steps to check them. This is the same format QA uses:

- **Before you start:** what must already be installed or running, and about how long the check takes.
- **One action per step.** Each command in its own fenced `bash` block: no `$` prompt, no output inside the block, paths the PM can copy as-is.
- **Expected result** after each step, in plain words, plus how to tell it failed and what to do ("if you see `401`, redo step 2").
- **Clean-up step** at the end (stop servers, delete temp folders).

Rules:

- QA (or you) must have **run the exact steps** first and seen the expected results. Never hand over untested steps.
- Steps check behaviour the PM cares about (a page appears, a booking is saved, an email arrives), not internals.
- If a step needs something the PM doesn't have yet, say so up front instead of letting it fail halfway.
- QA writes them in `docs/qa/<milestone>.md` under a `PM check` heading, so they can be rerun later. The lead copies them from there into the PM update's "What only you can check", unchanged.
- A step a tool could run (a focus ring, an alert's role, a layout at 320 px) goes back to QA to automate. A question about what the product should do is a decision for "Needs you", not a step.
