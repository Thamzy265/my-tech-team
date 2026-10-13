# UI build checklist

Checked: 2026-10-12. Check the current source when a rule decides an outcome.

Use this for screens and UI components. Work through every item. For an item that doesn't apply, write `n/a — <reason>` on the hand-off's "Checklists" line.

1. Read the UI spec. Every state in its states matrix must be built (default, hover, focus, disabled, loading, empty, error, success, long content, offline). If the matrix, breakpoints or accessibility notes are missing, stop and send the lead the list before building.
2. Structure first (semantic elements, or `Semantics` on Flutter), then style, then behaviour.
3. Use design tokens or theme values only, never hard-coded colours or sizes.
4. WCAG 2.2 AA:
   - contrast 4.5:1 for text and 3:1 for large text and UI elements;
   - visible focus that nothing covers;
   - targets at least 24×24 px;
   - labels on every input, with errors linked to their fields;
   - pasting allowed in login forms;
   - `prefers-reduced-motion` respected;
   - layout works at 320 px width.
5. Every async view has loading without layout shift, empty, error with a retry and a human message, and offline.
6. No unsanitised HTML (`innerHTML`, `dangerouslySetInnerHTML`, `v-html`, `{@html}`), and no `javascript:` URLs.
7. No secrets in client code: anything in the client bundle or app binary is public.
8. Store tokens in httpOnly cookies, not localStorage, where the platform allows it.
9. Strings are kept out of code, and the layout survives longer translated text.
10. Tests query by role or label (widget finders on Flutter); test IDs only as a last resort.
11. Justify every new dependency: size, maintenance, licence.
12. Third-party scripts and SDKs that track users load only after consent.
13. Performance: meet the brief's budget. The defaults are LCP ≤ 2.5 s, INP ≤ 200 ms and CLS ≤ 0.1 at p75 on a mid-range phone.

Build only what the spec shows. Headings, copy, icons or styling that aren't in the spec are spec gaps to raise, not extras to add.

## Sources

`docs/research/frontend-developer.md` (Checklist) and `docs/research/ui-ux-designer.md` (Handoff, Checklist), in the my-tech-team repo.
