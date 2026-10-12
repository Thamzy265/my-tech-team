# my-tech-team: design

Date: 12 Oct 2026. Status: **draft, waiting for PM review**. Research notes are in [`docs/research/`](../../research/).

## Goal

Ship a reusable set of team-role Agent Skills that any project can install. They come from the five FlutterDeck roles (`deck-*` in project-deck), widened from a dev team into a tech team. The human user is the **project manager (PM)** and is not a skill.

## Decisions so far

| Decision | Choice |
|---|---|
| Name | `my-tech-team`; repo `Thamzy265/my-tech-team`, public |
| PM role | No PM skill. The user stays the PM |
| Packaging | One plugin with every role, served from a marketplace in the same repo |
| Scope | Generic. Project rules stay in each project's CLAUDE.md or AGENTS.md |
| Marketer jobs | Market and competitor research; launch and release comms; content drafting |
| Marketing flow | The lead briefs the marketer; claims are checked; the PM approves. The team never publishes |
| New roles (12 Oct) | UI/UX designer, frontend developer, backend developer, security engineer |

## Roles (9 skills)

| Skill | Role | Owns | Main sources |
|---|---|---|---|
| `team-lead` | Senior developer / tech lead | Plan, system design, delegation, gates, status log, PM updates, merge | Fundamentals of SA, DDIA, Hard Parts, SRE, DORA |
| `team-designer` | UI/UX designer | Problem framing, flows, wireframes, states matrix, tokens, accessibility notes, design review of the built UI | NN/g heuristics, Krug, Refactoring UI, Atomic Design, WCAG 2.2, DTCG tokens |
| `team-frontend` | Frontend developer | Client UI on any stack (web or mobile), client state, async states, performance budget, client security | web.dev CWV, Russell, Testing Trophy, Inclusive Components, Flutter architecture guide |
| `team-backend` | Backend developer | APIs (contract first), data and migrations, stability, observability | DDIA, Release It!, SRE, Stripe idempotency, Google AIP, Twelve-Factor, Parallel Change |
| `team-tester` | Tester | Tries to break the work; regression tests; abuse-case tests | Existing `deck-tester` |
| `team-reviewer` | Code reviewer | Correctness, design quality, tests, performance; flags security concerns to security | Existing `deck-reviewer`, Ousterhout |
| `team-security` | Security engineer | Threat model, security requirements, security review, supply chain and secrets, severity, security verdict | OWASP Top 10:2025, ASVS 5.0, LLM/Agentic Top 10, Shostack, CWE Top 25, SSDF, SLSA, CVSS v4 |
| `team-qa` | QA | Real-flow acceptance checks, PM check steps, marketing claim check | Existing `deck-qa` |
| `team-marketer` | Marketer | Research, launch and release comms, content in the brand voice | Anthropic marketing plugin (prior art) |

`deck-developer` is split into `team-frontend` and `team-backend`. Both keep its shared rules: TDD, atomic Conventional Commits, no pushing or merging, the hand-off note, a "How to verify" draft and blocker reports. Work that is neither frontend nor backend (CLIs, daemons, libraries, infra scripts) goes to `team-backend`. See open question Q1.

## Workflow (one plan item)

```
Lead: pick item → size it → (large) system design note + ADRs
  → Security: threat model + security requirements      (if data / trust boundaries change)
  → Designer: flows, states matrix, tokens, spec         (if there is UI)
  → Backend + Frontend: agree API contract first, then build on separate branches
  → Tester: break it, add regression and abuse-case tests
  → Reviewer (code) + Security (security review), in parallel; developer fixes; loop until both approve
  → Designer: design review of the built UI              (if there is UI)
  → QA: real-flow acceptance + PM check steps
  → PM approves merge → Lead merges, ticks plan, reports
  → Marketer: launch / release comms → QA claim check → PM approves (PM publishes)
```

- **Sizing:** the lead calls an item *small* (one module, no new data or trust boundary) or *large*.
  - Small items skip the design note, the threat model and ADRs. They still pass every gate.
  - If a role does not apply, the lead writes it as `n/a — <reason>` in the log.
- **Either gate can block.** The reviewer blocks on correctness. Security blocks on security. The designer blocks on Blocker-rated UI issues. QA blocks on failed acceptance.
- **Only the PM can accept a risk**, and the acceptance is recorded in `docs/status.md`.

## System design (in `team-lead`)

The 12-step procedure in [`docs/research/system-design-books.md`](../../research/system-design-books.md) becomes the lead's procedure for large items. It lives in a `references/system-design.md` file. The output is `docs/design/<item>.md`, plus an ADR in `docs/adr/` for each decision that is hard to reverse.

YAGNI rules are part of the skill:
- Default to a modular monolith.
- Design for about 10x current load.
- Timeouts and bounded retries are always required; circuit breakers are optional.

The backend and frontend skills point to the matching steps (data, failure planning, contracts) and do not repeat them.

## Generic project contract

Each project adds a short **Team setup** section to CLAUDE.md or AGENTS.md. Skills read it and use these defaults when it is missing:

| Setting | Default |
|---|---|
| Plan and acceptance criteria | `docs/PLAN.md` |
| Status log | `docs/status.md` |
| QA evidence and PM check steps | `docs/qa/<milestone>.md` |
| Design notes and ADRs | `docs/design/`, `docs/adr/` |
| Threat models | `docs/security/threat-model.md` |
| UI specs and tokens | `docs/ui/` |
| Marketing and brand voice | `docs/marketing/`, `docs/marketing/voice.md` |
| Check command | Ask the PM on first run, then record it |
| Project-specific rules for review, test and security | Listed in the project file |

## Shared rules (all roles)

- **Blockers:** report them immediately and in every hand-off, giving *what, who can unblock, what is needed, impact*. Write "Blockers: none" when there are none.
  - Each PM update has a blockers table covering every role.
  - Roles that were not active since the last update are grouped on one line: "Designer, Marketer: not active".
- **Never** push, merge, publish, post or email. Those actions go through the lead or the PM.
- **Tool-neutral wording**, with short "On Claude Code: …" notes for subagents, the `code-review`/`security-review` skills, ReportFindings and superpowers TDD.
- **Language:** PR text and the README use ASD-STE100 Simplified Technical English. Marketing copy uses the brand voice. PM updates use plain language.

## Lead updates

- The PM update format stays (status, done, how you can check it, in progress, next up, blockers by role, needs you, risks).
- New lines: **Design** (if any design or ADR changed) and **Marketing** (drafts waiting for approval).
- The "How you can check it" rules stay the same, and move to `references/check-steps.md`.

## Repository layout

```
.claude-plugin/marketplace.json   marketplace "my-tech-team", one plugin, source "./"
.claude-plugin/plugin.json        name, version, description, author, repository, license MIT
skills/team-<role>/SKILL.md       9 skills; long material in references/
docs/research/                    research notes (sources for the skills)
docs/superpowers/specs/           this design
README.md                         ASD-STE100: install for Claude Code; copy into .agents/skills for others
CHANGELOG.md, LICENSE (MIT)
```

- Frontmatter uses only the open-spec fields (`name`, `description`, `license`, `metadata`).
- Each SKILL.md stays under 500 lines. Checklists and long procedures go in `references/`.
- If `source: "./"` fails `claude plugin validate --strict`, the plugin moves to `plugins/my-tech-team/`.

## Testing

- `skills-ref validate` on every skill, and `claude plugin validate . --strict` on the repo, both in CI.
- **Pressure tests (writing-skills):**
  - Give a fresh agent each skill and a small sample project, and fix the gaps it reports.
  - Scenarios include:
    - the lead is tempted to skip a gate to go faster
    - the security engineer is asked to "just approve" a High finding
    - the marketer is asked to overstate a feature
    - the designer gets a UI with no error states
- An end-to-end dry run of one small and one large item on a sample repo.

## Out of scope (v1)

- A PM skill. Claude Code `agents/*.md` subagent definitions, which may come in a later version.
- Separate DevOps/SRE, data or mobile roles. Their concerns sit with the backend, frontend and security roles for now.

## Open questions for the PM

- **Q1.** Should a generic `team-developer` stay for work that is neither frontend nor backend (for example project-deck's daemon), or should `team-backend` cover it? *Recommendation: `team-backend` covers it, to keep the list short.*
- **Q2.** Keep the `team-` prefix on skill names? *Recommendation: yes, because copied skills have no namespace.*
- **Q3.** Should QA do the marketing claim check? *Recommendation: yes, because QA holds the evidence.*
- **Q4.** Do the Team setup defaults in the table above look right?
