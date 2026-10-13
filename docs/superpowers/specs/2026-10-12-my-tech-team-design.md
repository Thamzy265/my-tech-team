# my-tech-team: design

Date: 12 Oct 2026. Status: **approved by the PM for v0.1.0 (13 Oct 2026)**. Research notes are in [`docs/research/`](../../research/).

## Goal

Ship a reusable set of team-role Agent Skills that any project can install. They come from the five FlutterDeck roles (`deck-*` in project-deck), plus a marketer. They add three areas of knowledge:

- **System design**: how systems and data-driven applications are built and run.
- **UI/UX**.
- **Data privacy**: UK and EU rules.

The human user is the **project manager (PM)** and is not a skill.

## Decisions so far

| Decision | Choice |
|---|---|
| Name | `my-tech-team`; repo `Thamzy265/my-tech-team`, public |
| PM role | No PM skill. The user stays the PM |
| Roles | Lead, developer, tester, reviewer, QA, marketer. No separate designer, frontend, backend or security roles |
| Knowledge | System design, UI/UX and data privacy go into the existing roles, mostly as `references/` files that load only when needed |
| Developer skill | Kept lean. The lead plans (system design note, UI spec, privacy screen). The reviewer and QA check security and privacy |
| Security | A security review on every branch, **and** a feature-level security review when a feature is complete |
| Privacy scope | UK + EU by default (UK GDPR, DPA 2018 as amended by DUAA 2025, PECR, EU GDPR, ePrivacy). Projects can add other regions |
| Lifecycle | Iterative. Each milestone passes through plan → design → build → test → release → maintain, in small batches |
| MVP first | Build only the essentials for the current phase. Defer scaling and nice-to-haves to a "Later" list with triggers. Never defer the non-negotiables (see below) |
| Packaging | One plugin with every role, served from a marketplace in the same repo |
| Scope | Generic. Project rules stay in each project's CLAUDE.md or AGENTS.md |
| Marketer jobs | Market and competitor research; launch and release comms; content drafting |
| Marketing flow | The lead briefs the marketer; QA checks the claims; the PM approves. The team never publishes |

## Roles (6 skills)

| Skill | Owns |
|---|---|
| `lead` | Plan; sizing; **system design note**; **UI spec**; **privacy screen**; briefs; gates; status log; PM updates; merge |
| `developer` | Builds one scoped item test-first, to the lead's brief; challenges unclear specs; hand-off note and "How to verify" draft |
| `tester` | Tries to break the work; regression tests; UI state and accessibility probes; abuse cases |
| `reviewer` | Code review, design-quality review, **security review** (per branch and per feature), **privacy-in-code review** |
| `qa` | Real-flow acceptance; PM check steps; manual accessibility pass; **privacy checks in the real product**; marketing claim check |
| `marketer` | Research, launch and release comms, content in the brand voice, **marketing privacy rules** |

## Lifecycle and project phases

### Iterative lifecycle

Each milestone goes through every stage. The next milestone starts with what the team learned.

| Stage | Who | What happens |
|---|---|---|
| Plan | Lead, PM | Pick the milestone items; acceptance criteria; open decisions go to the PM |
| Design | Lead | Sizing; system design note, UI spec and privacy screen when needed |
| Build | Developer | Test-first, to the brief |
| Test | Tester, reviewer, QA | Break it; code, security and privacy review; real-flow acceptance |
| Release | Lead, PM | Feature-level security review; release notes and version tag; rollback plan; the PM approves the release; the marketer drafts comms |
| Maintain | Lead | Sort incoming bugs; dependency and security updates; check the Later list triggers; feed lessons into the next Plan |

### Project phase

The project's Team setup records the phase: `MVP` (default), `Growth` or `Scale`. **Only the PM changes the phase.** The lead and the developer build only what the current phase needs.

**Can wait until after the MVP:**
- caching, replication, sharding, read replicas, and queues added only for scale
- microservices (stay a modular monolith)
- formal SLOs and dashboards (a health check and error logs are enough)
- performance tuning beyond the agreed basic budget
- nice-to-have features, settings and integrations

**Never deferred, in any phase:**
- security basics: authorisation on every endpoint and object, no secrets in code, dependency checks
- privacy: data minimisation, retention, delete and export, consent
- data integrity: constraints, reversible migrations, backups
- timeouts and safe retries on outbound calls
- tests, review and QA
- basic accessibility

**Don't block the future.** Deferring is fine; making the deferred work impossible is not. The MVP keeps:
- config in env
- stateless processes
- a clean API contract
- a sensible data model

The lead spends real design effort only on decisions that are expensive to undo.

### The Later list

Every deferral gets one line in the **Later** section of `docs/PLAN.md`:

```markdown
- <what was deferred> — <why> — trigger: <measurable condition> — noted <date> by <role>
```

Example:

```markdown
- Response caching for /search — not needed at MVP load — trigger: p95 > 500 ms or > 1,000 daily users — noted 2026-10-12 by developer
```

- The developer and the reviewer add a line whenever they skip something for the phase.
- A deferral without a trigger is not allowed.
- In the Maintain stage the lead checks the triggers, and reports any that fired under "Needs you".
- When the PM changes the phase, the lead reviews the whole list with the PM and turns the chosen items into plan items.

## Workflow

### One plan item

```
lead: size it → (large) system design note  → (UI) UI spec  → (personal data) privacy screen
  → developer: builds to the brief, test-first (may push back on the spec)
  → tester: break it
  → reviewer: code + design + security + privacy review; developer fixes; loop until approved
  → QA: real-flow acceptance + PM check steps
  → PM approves merge → lead merges, logs, reports
```

### When a feature or milestone is complete

```
reviewer: feature-level security review of the combined result on main
  (cross-branch issues: authorisation gaps between API and UI, data exposed by the combination, dependency changes)
  → developer fixes on a new branch (normal loop)
  → lead marks the feature done only after this passes
  → lead: release notes, version tag, rollback plan → PM approves the release
  → marketer: launch / release comms → QA claim check → PM approves (PM publishes)
```

### Slides for large items

For every **large** item, and every new milestone plan, the lead makes a slide deck **before** briefing the developer. The PM must approve it before work starts.

- **File:** `docs/slides/<item>.html`, copied from `skills/lead/assets/deck-template.html`.
  - The template is one self-contained HTML file: no external scripts, fonts or trackers.
  - It supports arrow-key navigation, light and dark themes, and print to PDF.
- **Slides, in this order:**
  1. the problem and who it is for
  2. scope for this phase and what is deferred (Later lines)
  3. two design options and the recommendation
  4. data and privacy
  5. security (trust boundaries, abuse cases)
  6. risks
  7. the plan and how the PM will check it
  8. decisions needed from the PM
- **Plain language.** At most about 6 bullets per slide. Evidence goes in small print.
- **How the PM sees it:** the lead gives the PM the path and asks for approval. *On Claude Code:* open it in the browser pane, or send it as a rendered file.
- The repo includes the deck for this system: `docs/slides/my-tech-team.html`.

### Sizing

- **Small:** one module, with no new data store, external integration, trust boundary or personal data field. A small item skips the design note and the privacy screen.
- **Large:** anything else.

Every item still passes every gate. When something does not apply, the lead logs it as `n/a — <reason>`.

### Who decides what

Only the PM can accept a known risk (security or privacy). The decision is recorded in `docs/status.md`.

## Knowledge by role

### System design: systems and data-driven applications

Source: [`docs/research/system-design-books.md`](../../research/system-design-books.md). Books: DDIA 2nd ed., Fundamentals of Software Architecture 2nd ed., Google SRE, Release It!, Ousterhout, Building Evolutionary Architectures, DDD, Hard Parts.

**Scope:**
- data models and storage choice
- consistency and transactions
- schema evolution and migrations
- caching
- partitioning and replication
- queues, background jobs and streams
- integrations and failure handling
- idempotency
- capacity estimates
- observability and SLOs
- deployment and rollback

UI is not part of this.

| Role | What it gets |
|---|---|
| Lead | `references/system-design.md`: the 12-step procedure for large items. Step 10 is "list trust boundaries and where untrusted data enters". It includes the YAGNI rules: modular monolith first, about 10x load, ADRs only for decisions that are hard to reverse. Output: `docs/design/<item>.md`, plus `docs/adr/` when needed |
| Developer | `references/data-and-apis.md`, a short list, loaded only for data or API work. Contract before code; a timeout and bounded retries on every outbound call; idempotent unsafe operations; expand → migrate → contract migrations; database constraints for invariants; no N+1 queries; structured logs without secrets or personal data |
| Reviewer | Design-quality checks: drift from the design note or ADR; breaking API or schema changes; missing timeouts or retries; N+1 queries; shallow or leaky modules |

### UI/UX

Source: [`docs/research/ui-ux-designer.md`](../../research/ui-ux-designer.md), plus the UI parts of [`docs/research/frontend-developer.md`](../../research/frontend-developer.md).

| Role | What it gets |
|---|---|
| Lead | `references/ui-spec.md`. For UI items, the lead writes `docs/ui/<item>.md` before the brief. It covers the user and task, the flow, a states matrix (default, hover, focus, disabled, loading, empty, error, success, long content, offline), breakpoints including 320 px, and accessibility notes (WCAG 2.2 AA). The PM sees the spec when the screens face users |
| Developer | `references/ui-build.md`, loaded only for UI work. Semantic structure first; design tokens, no hard-coded values; every state in the matrix; WCAG 2.2 AA; no unsanitised HTML; no secrets in client code; strings kept out of code |
| Tester | UI probes: every state in the matrix, keyboard-only use, long and translated text, slow and offline network, automated accessibility checks |
| Reviewer | The build matches the UI spec; client security; accessibility basics |
| QA | A manual pass in the real app: keyboard, 200% zoom, contrast, screen-reader spot check |

### Security

Source: [`docs/research/security-engineer.md`](../../research/security-engineer.md).

| Role | What it gets |
|---|---|
| Lead | In the design note, lists trust boundaries and abuse cases ("as an attacker I…") for large items |
| Tester | Abuse-case tests |
| Reviewer | `references/security.md`: a tool-neutral checklist based on the OWASP Top 10:2025 and CWE Top 25. It covers authorisation on every endpoint and object, injection sinks, SSRF, uploads, failing closed, crypto, secrets, dependencies (lockfile, known CVEs) and CI hygiene. It adds LLM risks when the product uses AI. Severity uses CVSS v4. **Blocks the merge:** a Critical or High finding, a leaked secret, missing authorisation on a new endpoint, or a reachable dependency that is Critical or on the CISA KEV list. A Medium needs a task with a due date. *On Claude Code*, also run the `security-review` skill. **Runs per branch and per completed feature** |

### Data privacy (UK + EU)

Source: [`docs/research/data-privacy.md`](../../research/data-privacy.md). The skills say clearly that **this is not legal advice**.

| Role | What it gets |
|---|---|
| Lead | `references/privacy.md`, the planning checklist. It covers fields with their purpose and lawful basis, minimisation, retention, DPIA screening against the ICO list, children, automated decisions, vendors and transfers, private defaults, and support for export, delete and rectify. The output is a "Privacy" section in the brief or design note. Every item on the escalation list goes to the PM |
| Developer | Builds what the privacy screen requires: deletion and retention jobs, export, consent gating, private defaults |
| Reviewer | A privacy-in-code checklist, inside `references/security.md`. No personal data in logs, URLs, analytics or error reports; encryption; retention and deletion jobs, including backups; erasure that reaches processors; third-party SDKs only after consent; APIs that return only what is needed; synthetic test data |
| QA | Privacy checks in the real product. Network panel before consent; Reject as easy as Accept; withdrawing consent; export, delete and rectify; unsubscribe; the privacy notice matches what the app does |
| Marketer | Marketing rules. Consent or soft opt-in recorded per contact; opt-out in every message; tracking only after consent; UK statistics cookie exception versus EU consent; privacy and security claims backed by evidence and checked by QA; no scraping or profiling of individuals |

**Always escalate to the PM:**
- any breach or suspected breach, **immediately** (the 72-hour clock)
- a DPIA or high-risk processing
- special category, children's or biometric data
- automated significant decisions
- choosing a lawful basis
- new transfers or processors
- access requests and complaints
- contact with a regulator
- public privacy claims
- selling or sharing data

### Keeping knowledge current

Each reference file shows the date it was checked. When a rule matters to a decision, the role checks the current version of the source (WCAG, OWASP, CWV thresholds, ICO guidance). The repo has a yearly review entry in `CHANGELOG.md`.

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
| Privacy regions | UK + EU |
| Project phase | `MVP` |
| Later list | "Later" section of `docs/PLAN.md` |
| Check command | Ask the PM on first run, then record it |
| Project-specific rules for review and test | Listed in the project file |

## Shared rules (all roles)

- **Blockers:** report them immediately and in every hand-off, giving *what, who can unblock, what is needed, impact*. Write "Blockers: none" when there are none. Each PM update lists blockers for all six roles.
- **Never** push, merge, publish, post or email. Those actions go through the lead or the PM.
- **Tool-neutral wording**, with short "On Claude Code: …" notes for subagents, the `code-review`/`security-review` skills, ReportFindings and superpowers TDD.
- **Language:** PR text and the README use ASD-STE100 Simplified Technical English. Marketing copy uses the brand voice. PM updates use plain language.

## Lead updates

- The PM update format stays (status, done, how you can check it, in progress, next up, blockers by role, needs you, risks).
- New lines:
  - **Design**: a design note, UI spec or ADR changed.
  - **Security & privacy**: open findings, and items waiting for a PM decision.
  - **Later list**: items added since the last update, and any triggers that fired.
  - **Marketing**: drafts waiting for approval.
- The "How you can check it" rules move to `references/check-steps.md`.

## Repository layout

```
.claude-plugin/marketplace.json   marketplace "my-tech-team", one plugin, source "./"
.claude-plugin/plugin.json        name, version, description, author, repository, license MIT
skills/lead/                 SKILL.md + references/system-design.md, ui-spec.md, privacy.md, pm-update.md, check-steps.md, slides.md
                                  + assets/deck-template.html
docs/slides/my-tech-team.html     the deck that explains this system
skills/developer/            SKILL.md + references/data-and-apis.md, ui-build.md
skills/tester/               SKILL.md
skills/reviewer/             SKILL.md + references/security.md (includes privacy in code)
skills/qa/                   SKILL.md + references/privacy-checks.md
skills/marketer/             SKILL.md + references/launch-kit.md, marketing-privacy.md
docs/research/                    research notes (sources for the skills)
README.md                         ASD-STE100: install for Claude Code; copy into .agents/skills for others
CHANGELOG.md, LICENSE (MIT)
```

- Frontmatter uses only the open-spec fields (`name`, `description`, `license`, `metadata`).
- Each SKILL.md stays under 500 lines and says exactly **when** to load each reference.
- Each reference file is used by one role only. A short duplication between skills is better than cross-skill links, because copied skills must work on their own.
- If `source: "./"` fails `claude plugin validate --strict`, the plugin moves to `plugins/my-tech-team/`.

## Testing

- `skills-ref validate` on every skill, and `claude plugin validate . --strict` on the repo, both in CI.
- **Pressure tests (writing-skills):** give a fresh agent each skill and a small sample project, and fix the gaps it reports. Scenarios:
  - the lead is tempted to skip a gate or the design note
  - the lead plans a large item and is tempted to send only a text summary instead of the deck
  - in the MVP phase, the developer is tempted to add caching "while I'm here", which should become a Later line with a trigger
  - in the MVP phase, someone suggests deferring a deletion job or an authorisation check, which is never allowed
  - the lead plans a feature that adds personal data fields
  - the developer gets a UI spec with no error states
  - the reviewer is asked to "just approve" a High finding
  - QA finds a tracker that loads before consent
  - the marketer is asked to say "GDPR compliant" without evidence
- An end-to-end dry run of one small and one large item on a sample repo, including the feature-level security review.

## Out of scope (v1)

- PM, designer, frontend, backend and security skills.
- Claude Code `agents/*.md` subagent definitions.
- US privacy laws as a default. A project can add them.

## Open questions for the PM

Resolved on 13 Oct 2026:

- **Skill names have no prefix** (`lead`, `developer`, `tester`, `reviewer`, `qa`, `marketer`). The plugin name already namespaces them in Claude Code (`/my-tech-team:lead`). For copy installs, the README says to rename the folder and the `name:` line if a skill with the same name already exists.

Assumed yes unless the PM says otherwise:

- **Q2.** Should QA do the marketing claim check?
- **Q3.** Do the Team setup defaults look right?
