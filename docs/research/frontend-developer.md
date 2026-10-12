# Research: frontend developer

Checked 12 Oct 2026. This is the source material for the `team-frontend` skill, which must work for any UI stack: web (React, Vue, Svelte…) and mobile (Flutter…). Ideas are paraphrased.

## Top voices

| Who | Signature idea | Source |
|---|---|---|
| Google web.dev / Addy Osmani | Core Web Vitals at p75 of real users | https://web.dev/articles/vitals |
| Alex Russell | Budget for a median Android phone, not a developer laptop | https://infrequently.org/2025/11/performance-inequality-gap-2026/ |
| Kent C. Dodds | Testing Trophy: mostly integration tests that resemble real use | https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications |
| Testing Library | Query by role and label; test IDs as a last resort | https://testing-library.com/docs/queries/about/ |
| Heydon Pickering | Inclusive Components: semantic-first patterns | https://inclusive-components.design |
| Jeremy Keith | Progressive enhancement, resilient web design | https://resilientwebdesign.com |
| Jake Archibald | Offline-first, loading performance | https://jakearchibald.com |
| Dan Abramov | Keep state close to where it is used | https://overreacted.io |
| Sara Soueidan, Rachel Andrew, Josh W. Comeau | Practical accessibility; CSS layout; mental models for CSS | https://www.sarasoueidan.com, https://rachelandrew.co.uk, https://www.joshwcomeau.com |
| MDN | Web platform reference and Baseline | https://developer.mozilla.org |
| OWASP | XSS Prevention Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html |
| Flutter team | MVVM: views and view models; repositories as the single source of truth; stateless services | https://docs.flutter.dev/app-architecture/guide |

## How they plan

- **Component tree** from the design handoff, with every state per component. Design-system components are reused first.
- **State decisions:** local UI, shared, server cache or URL. Keep state as low in the tree as possible.
- **API contract:** confirm schemas, errors, pagination and auth. Generate types and mocks from the contract so the frontend can work in parallel with the backend.
- **Performance budget:** Russell's 2026 baseline is a Galaxy A24-class phone at 9/3 Mbps and 100 ms RTT, p75. A 3 s load allows about 2.0 MiB with 0.3 MiB JS (JS-light page) or about 1.2 MiB with 0.62 MiB JS (JS-heavy page).
- **Support matrix:** browsers (Baseline or browserslist), OS and device minimums, screen readers, viewports, locales.

## How they implement

- Semantic HTML first, ARIA only when nothing native fits (Flutter: `Semantics`).
- WCAG 2.2 AA, including 2.4.11, 2.5.7, 2.5.8 and 3.3.8.
- Test-first, Testing Trophy shape: types and lint, a few unit tests, mostly integration and component tests, a few E2E tests (Flutter: unit, widget, integration).
- Every async view has loading (no layout shift), empty, error with retry, offline and success states. Optimistic updates have a rollback.
- Progressive enhancement: core content works without JS, or when JS fails.
- i18n: no hard-coded strings, ICU plurals, locale formats, RTL through logical properties, room for longer text.

## What they keep watch on

- **Core Web Vitals (p75):** LCP ≤ 2.5 s good, > 4 s poor; INP ≤ 200 ms good, > 500 ms poor (INP replaced FID on 12 Mar 2024); CLS ≤ 0.1 good, > 0.25 poor.
- A per-route bundle budget enforced in CI; code splitting, image and font optimisation.
- Accessibility regressions: axe in CI plus manual keyboard and screen-reader passes.
- **Client security:**
  - Treat framework escape hatches (`dangerouslySetInnerHTML`, `v-html`, `{@html}`, `bypassSecurityTrust*`) as dangerous, and use DOMPurify when HTML is unavoidable.
  - Reject `javascript:` URLs.
  - Use CSP and Trusted Types as a second layer (Trusted Types reached Baseline in Feb 2026).
  - Never put secrets in client builds. Prefer httpOnly cookies over localStorage for tokens.
- Dependency cost and supply chain: package size, maintenance, licence, lockfile.

## Checklist

1. Read the design handoff and API contract, and raise gaps before coding.
2. Component tree with all states, mapped to tokens and components.
3. A state decision for each piece of state.
4. Types and mocks generated from the contract, never guessed.
5. Performance budget and support matrix agreed.
6. Failing tests from the acceptance criteria first.
7. Structure first, then style, then behaviour.
8. Loading, empty, error, offline and success states for each async view.
9. WCAG 2.2 AA met.
10. Strings externalised; layouts safe for RTL and longer text.
11. No unsanitised HTML sinks and no client secrets; the build works with CSP.
12. Every new dependency justified.
13. CI runs lint, types, tests, axe and the bundle-size check.
14. Self-review the diff, then hand off.

## Not verified

- Claims that Google lowered "good" INP to 150 ms are not confirmed by web.dev, so 200 ms is used.
- The Pickering, Soueidan, Keith, Archibald, Comeau, Andrew and Abramov URLs were not fetched.
