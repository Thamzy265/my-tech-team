# Research: UI/UX designer

Checked 12 Oct 2026. This is the source material for the `team-designer` skill. Ideas are paraphrased.

## Top voices

| Who | Signature idea | Source |
|---|---|---|
| Jakob Nielsen / NN/g | 10 usability heuristics, heuristic evaluation | https://www.nngroup.com/articles/ten-usability-heuristics/ |
| Don Norman | Affordances, signifiers, feedback, the gulfs of execution and evaluation | https://jnd.org |
| Steve Krug | "Don't make me think": self-evident UI, cheap DIY usability tests | https://sensible.com |
| Adam Wathan & Steve Schoger | *Refactoring UI*: start from the feature, not the layout; design in grayscale first; constrained scales | https://www.refactoringui.com |
| Brad Frost | Atomic Design: atoms → molecules → organisms → templates → pages | https://atomicdesign.bradfrost.com |
| Jared Spool | Design is the rendering of intent | https://articles.centercentre.com/ |
| Luke Wroblewski | Mobile first, form design | https://www.lukew.com |
| Erika Hall | *Just Enough Research*: research to reduce risk, not as a ritual | https://abookapart.com/products/just-enough-research |
| Harry Brignull | Deceptive patterns catalogue | https://deceptive.design |
| W3C WAI | WCAG 2.2 is the current Recommendation; WCAG 3.0 is still a draft | https://www.w3.org/TR/WCAG22/ |
| W3C Design Tokens CG | Format Module 2025.10, the first stable version | https://www.w3.org/community/reports/design-tokens/CG-FINAL-format-20251028/ |
| Google / Apple | Material 3, Human Interface Guidelines | https://m3.material.io, https://developer.apple.com/design/human-interface-guidelines |

## How they plan

1. **Frame the problem:** user, job, outcome, constraints, success metric, riskiest assumptions. Do just enough research: existing data, competitors, support tickets.
2. **Task flows:** the happy path plus branches (auth, errors, permissions, cancel, undo).
3. **Wireframes:** low fidelity, grayscale, the core feature first.
4. **High fidelity:** constrained scales for spacing, type, colour, radius and elevation, following platform conventions.
5. **Design system:** reuse first. A new component gets its variants and states defined. Token names are semantic (`color.text.danger`, not `red-600`).

## Handoff

- Spec per screen and component: layout, tokens (no hard-coded values), content rules, interactions.
- **States matrix:** default, hover, focus-visible, active, disabled, loading, empty, error, success, partial data, long content, offline, permission denied.
- Breakpoints, including 320 CSS px reflow (WCAG 1.4.10).
- Accessibility notes: headings, landmarks, focus order, accessible names, alt text, error association, `prefers-reduced-motion`.
- Tokens as DTCG JSON, with light and dark themes.
- **Design review of the built UI** at every breakpoint and state: keyboard-only use, 200% and 400% zoom, contrast. Issues are ranked Blocker, Major or Minor.

## What they keep watch on

- Nielsen's 10 heuristics.
- **WCAG 2.2 AA.** The most common failures (WebAIM Million 2026, secondary reports) are low-contrast text (~84% of home pages), missing alt text, missing form labels, empty links and empty buttons.
- **Often missed in 2.2:** 2.4.11 Focus Not Obscured, 2.5.7 Dragging Movements, 2.5.8 Target Size (24×24 CSS px), 3.3.8 Accessible Authentication (allow paste and password managers), 3.3.7 Redundant Entry.
- **Core:** contrast of 4.5:1 for text and 3:1 for large text and UI elements; focus visible; reflow; text resize.
- **Metrics:** task success, time on task, error rate, SUS, funnel drop-off.
- **Deceptive patterns to avoid:** confirmshaming, roach motel, sneak into basket, hidden costs, trick questions, forced continuity, nagging, privacy-invasive defaults.

## Checklist

1. Problem, user, task and success metric are written down.
2. Assumptions and open questions are logged for the PM.
3. Flows cover the happy path, errors, cancel/undo and auth edges.
4. Existing components and tokens are reused, and any new one is justified.
5. The hierarchy works in grayscale before visual polish.
6. A states matrix exists for every screen.
7. Breakpoints are specified, including 320 px reflow.
8. Contrast passes (4.5:1 text, 3:1 UI and large text).
9. Targets are ≥ 24×24 px (44–48 px on touch platforms).
10. Focus order, visible focus and keyboard paths are defined, and nothing covers the focused element.
11. Every input has a label, errors link to fields and explain the fix, and there is no redundant entry.
12. Copy is plain language, CTAs are verbs, and errors explain how to recover.
13. No deceptive patterns, and destructive actions have a confirmation or undo.
14. The handoff includes tokens, component specs and accessibility notes.
15. The built UI is reviewed against the spec, with ranked issues.

## Working without Figma (as an AI agent)

- Flows: Mermaid flowcharts or state diagrams.
- Wireframes: Markdown/ASCII for low fidelity; static HTML/CSS prototypes styled only from token CSS variables, with all states shown side by side.
- Tokens: DTCG `tokens.json`, converted to CSS variables.
- Review: run the UI in a headless browser and screenshot every breakpoint and state; run axe-core or Lighthouse; then do a manual keyboard pass. Automated tools catch only part of WCAG.
- Contrast: compute it from the token values with a script.

## Not verified

- NN/g, HIG, Material, Refactoring UI, Krug, Norman and LukeW content came from general knowledge, not fetched pages.
- The WebAIM 2026 figures came from secondary reports.
- 44–48 px touch targets are platform guidance, not a WCAG AA requirement.
