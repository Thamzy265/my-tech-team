# Slides for large items

Checked: 2026-10-12. Check the current source when a rule decides an outcome.

## When to make a deck

- Every **large** item, and every new milestone plan.
- **Before** briefing the developer. The PM must approve the deck before work starts.
- Always, even when the PM asks for "just a chat summary". The deck is the record the PM approves. Give the chat summary as well, after the deck path.

## Make it

1. Write the design note, UI spec and privacy section first. The deck summarises them; it doesn't replace them.
2. Copy the template: `assets/deck-template.html` in this skill → `docs/slides/<item>.html` (use the slides folder from Team setup if it differs). `<item>` is a short kebab-case name, e.g. `booking-deposits`.
3. Replace every `[bracketed]` text, including `<title>`. Search the file for `[` before you finish: none may remain.
4. Keep the file self-contained: no external scripts, fonts, images or trackers.
5. If a slide truly doesn't apply, delete it and say why on the Scope slide's small print.

## Slide order

The template has 9 slides: a title slide, then these 8, in this order.

1. The problem and who it is for.
2. Scope for this phase and what is deferred (the Later lines, with triggers).
3. Two design options and the recommendation.
4. Data and privacy (fields, purpose, retention; lawful basis and DPIA screening under "Needs PM").
5. Security (trust boundaries, abuse cases, mitigations).
6. Risks.
7. The plan and how the PM will check it.
8. Decisions needed from the PM, each with options and your recommendation.

## Writing rules

- Plain language. Say what it means for users, not how the code works.
- About 6 bullets per slide at most. Evidence and sources go in small print (`class="small"`).
- Never fill in a PM decision. Lawful basis, risk acceptance and scope choices stay on the Decisions slide as questions.

## Show it and wait

1. Give the PM the path (`docs/slides/<item>.html`) and say how to open it: in any browser; arrow keys move between slides; print saves a PDF.
2. *On Claude Code:* open it in the browser pane, or send it as a rendered file.
3. Ask for approval and the decisions on slide 8. Record the PM's answer, dated, in the status log.
4. **Don't brief the developer until the PM approves.** If the PM changes something, update the deck, the design note and the spec, and ask again.
