# my-tech-team: design

Date: 12 Oct 2026. Status: **draft, waiting for PM review**. Research notes are in [`docs/research/`](../../research/).

## Goal

Ship a reusable set of team-role Agent Skills that any project can install. They come from the five FlutterDeck roles (`deck-*` in project-deck), plus a marketer, and add UI/UX and system design knowledge. The human user is the **project manager (PM)** and is not a skill.

## Decisions so far

| Decision | Choice |
|---|---|
| Name | `my-tech-team`; repo `Thamzy265/my-tech-team`, public |
| PM role | No PM skill. The user stays the PM |
| Roles | The original five (lead, developer, tester, reviewer, QA) plus a marketer. No separate designer, frontend, backend or security roles |
| New knowledge | UI/UX and system design go into the existing roles, mostly as `references/` files |
| Packaging | One plugin with every role, served from a marketplace in the same repo |
| Scope | Generic. Project rules stay in each project's CLAUDE.md or AGENTS.md |
| Marketer jobs | Market and competitor research; launch and release comms; content drafting |
| Marketing flow | The lead briefs the marketer; QA checks the claims; the PM approves. The team never publishes |

## Roles (6 skills)

| Skill | Role | Owns |
|---|---|---|
| `team-lead` | Senior developer / tech lead | Plan, **system design for large items**, delegation, gates, status log, PM updates, merge |
| `team-developer` | Developer | Builds one scoped item test-first; **writes a UI spec first when the item has UI**; follows the design rules |
| `team-tester` | Tester | Tries to break the work; regression tests; **UI states and accessibility probes** |
| `team-reviewer` | Reviewer | Code review and security review; **design-quality and UI checks** |
| `team-qa` | QA | Real-flow acceptance checks, PM check steps, **manual accessibility pass**, marketing claim check |
| `team-marketer` | Marketer | Research, launch and release comms, content in the brand voice |

## Workflow (one plan item)

The workflow is unchanged from project-deck:

```
lead → developer → tester → reviewer (loop until approved) → QA → PM approves merge → lead merges and reports
                                                     after a release → marketer → QA claim check → PM approves (PM publishes)
```

- **Sizing.** The lead calls an item *small* or *large*.
  - *Small* means one module and no new data store, external integration or trust boundary.
  - Large items get a system design note before the developer is briefed.
  - Small items skip it but still pass every gate.

## Where the new knowledge goes

### System design

Source: [`docs/research/system-design-books.md`](../../research/system-design-books.md).

| Role | What it gets |
|---|---|
| Lead | `references/system-design.md`: the 12-step procedure for large items, plus the YAGNI rules (modular monolith first, design for about 10x load, ADRs only for decisions that are hard to reverse). The output is `docs/design/<item>.md`, plus an ADR in `docs/adr/` when needed. The developer brief links to it |
| Developer | `references/design-rules.md`, a short list. Backend rules: the API contract comes before code; timeouts and bounded retries on every outbound call; idempotent unsafe operations; expand → migrate → contract migrations; deep modules; structured logs without secrets. Frontend rules: agree the API contract first; keep state as low in the tree as possible; set a performance budget |
| Reviewer | Design-quality checks: shallow or leaky modules, missing timeouts or retries, breaking API or schema changes, N+1 queries, drift from the design note or ADR |

### UI/UX

Source: [`docs/research/ui-ux-designer.md`](../../research/ui-ux-designer.md), plus the frontend parts of [`docs/research/frontend-developer.md`](../../research/frontend-developer.md).

| Role | What it gets |
|---|---|
| Lead | For UI items, the brief asks for a UI spec before code. Unclear user goals go to the PM |
| Developer | `references/ui-ux.md`. **Before coding a UI item**, write `docs/ui/<item>.md`: the user and task, the flow, a states matrix (default, hover, focus, disabled, loading, empty, error, success, long content, offline), breakpoints including 320 px, and accessibility notes. Then build to it: semantic structure first, design tokens and no hard-coded values, WCAG 2.2 AA, Nielsen's heuristics, no deceptive patterns |
| Tester | UI probes: every state in the matrix, keyboard-only use, long and translated text, slow and offline network, automated accessibility checks (axe or a platform equivalent) |
| Reviewer | UI checks: the build matches the UI spec, no unsanitised HTML, no secrets in client code, accessibility basics |
| QA | A manual pass in the real app: keyboard, 200% zoom, contrast, screen-reader spot check. Automated tools catch only part of WCAG. These steps go into the PM check when they matter to the PM |

The frontend, backend and security research stays in `docs/research/` for reference. It is not a separate role. See open question Q4.

## Generic project contract

Each project adds a short **Team setup** section to CLAUDE.md or AGENTS.md. Skills read it and use these defaults when it is missing:

| Setting | Default |
|---|---|
| Plan and acceptance criteria | `docs/PLAN.md` |
| Status log | `docs/status.md` |
| QA evidence and PM check steps | `docs/qa/<milestone>.md` |
| Design notes and ADRs | `docs/design/`, `docs/adr/` |
| UI specs | `docs/ui/` |
| Marketing and brand voice | `docs/marketing/`, `docs/marketing/voice.md` |
| Check command | Ask the PM on first run, then record it |
| Project-specific rules for review and test | Listed in the project file |

## Shared rules (all roles)

- **Blockers:** report them immediately and in every hand-off, giving *what, who can unblock, what is needed, impact*. Write "Blockers: none" when there are none. Each PM update lists blockers for all six roles.
- **Never** push, merge, publish, post or email. Those actions go through the lead or the PM.
- **Tool-neutral wording**, with short "On Claude Code: …" notes for subagents, the `code-review`/`security-review` skills, ReportFindings and superpowers TDD.
- **Language:** PR text and the README use ASD-STE100 Simplified Technical English. Marketing copy uses the brand voice. PM updates use plain language.

## Lead updates

- The PM update format stays (status, done, how you can check it, in progress, next up, blockers by role, needs you, risks).
- New lines: **Design** (if a design note or ADR changed) and **Marketing** (drafts waiting for approval).
- The "How you can check it" rules move to `references/check-steps.md`.

## Repository layout

```
.claude-plugin/marketplace.json   marketplace "my-tech-team", one plugin, source "./"
.claude-plugin/plugin.json        name, version, description, author, repository, license MIT
skills/team-lead/                 SKILL.md + references/system-design.md, pm-update.md, check-steps.md
skills/team-developer/            SKILL.md + references/design-rules.md, ui-ux.md
skills/team-tester/               SKILL.md
skills/team-reviewer/             SKILL.md
skills/team-qa/                   SKILL.md
skills/team-marketer/             SKILL.md + references/launch-kit.md
docs/research/                    research notes (sources for the skills)
README.md                         ASD-STE100: install for Claude Code; copy into .agents/skills for others
CHANGELOG.md, LICENSE (MIT)
```

- Frontmatter uses only the open-spec fields (`name`, `description`, `license`, `metadata`).
- Each SKILL.md stays under 500 lines.
- If `source: "./"` fails `claude plugin validate --strict`, the plugin moves to `plugins/my-tech-team/`.

## Testing

- `skills-ref validate` on every skill, and `claude plugin validate . --strict` on the repo, both in CI.
- **Pressure tests (writing-skills):** give a fresh agent each skill and a small sample project, and fix the gaps it reports. Scenarios:
  - the lead is tempted to skip a gate
  - the developer gets a UI item with no error states
  - the developer is tempted to skip the design note on a large item
  - the marketer is asked to overstate a feature
- An end-to-end dry run of one small and one large item on a sample repo.

## Out of scope (v1)

- PM, designer, frontend, backend and security skills.
- Claude Code `agents/*.md` subagent definitions.

## Open questions for the PM

- **Q1.** Keep the `team-` prefix on skill names? *Recommendation: yes, because copied skills have no namespace.*
- **Q2.** Should QA do the marketing claim check? *Recommendation: yes, because QA holds the evidence.*
- **Q3.** Do the Team setup defaults in the table above look right?
- **Q4.** Should the security research (OWASP Top 10:2025, threat modelling, supply chain) also go into the reviewer as a checklist? *Recommendation: yes, a short checklist. The reviewer already runs a security review.*
