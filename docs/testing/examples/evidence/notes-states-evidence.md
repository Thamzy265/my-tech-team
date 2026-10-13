# QA — notes-states

Date: 2026-10-13 — Environment: macOS 27.0.1, Playwright 1.63.0 headless Chromium (chromium-1243), Node 22.12.0, commit e9664a6, page opened as file://.../static/states.html (static page, no server needed; app.py does not serve it)

The lead's request has no plan item, so the criteria below are taken from the lead's message ("three states: empty, with notes, error") plus the skill's accessibility pass.

Run: `npx playwright test --config qa-artifacts/qa.config.ts` (QA-only config, git-ignored: video on, 1280x720, output to qa-artifacts/notes-states). Spec: `e2e/notes-states.spec.ts`. 1 test, passed. Data: synthetic ("Buy milk", "Call Sam"); no personal data on screen.

| # | Criterion | Automated / manual | Tool and command | Result | Evidence |
|---|---|---|---|---|---|
| 1 | Empty state shows "No notes yet. Write your first note." and hides list and error | automated | Playwright — command above | PASS | screens/1-empty.png; video: qa-artifacts/notes-states-flow.webm |
| 2 | "With notes" shows the list (Buy milk, Call Sam) and hides the empty state | automated | Playwright — same run | PASS | screens/2-with-notes.png |
| 3 | Error state shows "Could not load notes." with a "Try again" button, as role=alert, and hides the list | automated | Playwright — same run, `getByRole('alert')` | PASS | screens/3-error.png; alert absent from the accessibility tree while hidden, present after clicking Error |
| 4 | Keyboard: Tab order Empty, With notes, Error, Try again; Shift+Tab goes back; Enter and Space switch state; focus always visible; no trap | automated | Playwright — same run, `keyboard.press` | PASS | screens/4-focus-empty.png, 4-focus-with-notes.png, 4-focus-error.png, 4-focus-try-again.png; focused outline style/width asserted not none/0 (blue browser default ring) |
| 5 | Accessibility tree: every control has a name; sections are named regions; error is an alert | automated | Playwright — `toMatchAriaSnapshot` | PASS | tree: h1 "My notes"; buttons "Empty", "With notes", "Error"; alert "Error state" containing "Try again" |
| 6 | Contrast 4.5:1 and target size at least 24x24 px | automated | Playwright — computed colours from rendered styles | PASS | h1 and body text rgb(0,0,0) on rgb(255,255,255) = 21:1; buttons rgb(0,0,0) on rgb(239,239,239) = 18.3:1; all buttons at least 24x24 px |
| 7 | 320 px width: all three states fit, no sideways scroll | automated | Playwright — `setViewportSize 320x640`, scrollWidth - clientWidth = 0 | PASS | screens/5-320-empty.png, 5-320-with-notes.png, 5-320-error.png |
| 8 | 200% zoom (640 CSS px viewport, error state) fits | automated | Playwright — viewport 640x360 as the 200% equivalent of 1280 | PASS | screens/6-zoom200-error.png |
| 9 | "Try again" does something | automated | Playwright — click, observe | FAIL / SPEC GAP — nothing happens: the error stays visible, no retry, no state change | see Spec gaps; not a defect until the lead confirms what it should do |

## Findings

- Minor: the buttons Empty / With notes / Error give no sign of which state is selected (no `aria-pressed`, no highlight). A screen reader user hears the content change only for the error alert; the empty and list changes are silent. Not a WCAG failure by itself.
- Minor: the state switcher buttons are a demo control and are always on the page; confirm they are meant to ship.
- Spec gap: what should "Try again" do (reload notes from `GET /notes`, then show empty or list)? Currently a dead button.
- Spec gap: the page is static and never calls `GET /notes`; the three states are only toggled by hand. Confirm this is a state demo, not the real notes page.

## Accessibility

Keyboard: pass. 200% zoom and 320 px: pass. Contrast: pass. Screen reader: live screen reader not observed (accessibility tree checked, role=alert confirmed). Result: pass, with the Minor items above.

## Privacy

n/a — no personal data, cookies, tracking or third-party requests (single local static file, no scripts loading from outside; source read).

## Not observed
- Live screen reader (VoiceOver etc.): accessibility tree only. A person with a screen reader or the PM can check.
- Other browsers (Firefox, WebKit) and real touch devices: only Chromium tested.
- The page served over HTTP by the app: app.py has no route for /static/states.html, so it was opened via file://.
- Real 200% browser zoom: approximated with a 640 CSS px viewport.

## PM check

PM check: nothing — every criterion was checked by QA (see the table above). The "Try again" behaviour is a spec question for the lead, not a PM step.
