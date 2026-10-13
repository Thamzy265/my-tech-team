# "How you can check it" (after every finished task)

Checked: 2026-10-12. Check the current source when a rule decides an outcome.

Whenever something is reported as done, give the PM numbered steps to check it themselves:

- **Before you start:** what must already be running or installed (e.g. "the app running locally from your IDE").
- **One action per step.** Each command goes in its own fenced `bash` block (no `$` prompt, no output inside the block), with paths the PM can copy as-is.
- **Expected result** after each step, in plain words, plus how to tell it failed ("if you see `401`, the token wasn't loaded; redo step 2").
- **Clean-up step** at the end (stop the server, delete temp folders).
- About how long it takes.

Rules:

- QA (or you) must have **run the exact steps** first and seen the expected results. Never hand over untested steps.
- Steps check behaviour the PM cares about (a page appears, a booking is saved, an email arrives), not internals.
- If a step needs something the PM doesn't have yet, say so up front instead of letting it fail halfway.
- QA writes them in `docs/qa/<milestone>.md` under a `PM check` heading, so they can be rerun later. The lead copies them from there into the PM update's "How you can check it", unchanged.
