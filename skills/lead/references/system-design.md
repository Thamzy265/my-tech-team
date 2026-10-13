# System design for large items

Checked: 2026-10-12. Check the current source when a rule decides an outcome.

Use this for every **large** item before the developer brief. Write the result to `docs/design/<item>.md` with the template below. Write an ADR in `docs/adr/` for each decision that is hard to reverse. Sources: DDIA 2nd ed., Fundamentals of Software Architecture 2nd ed., the Google SRE books, Release It!, A Philosophy of Software Design, Building Evolutionary Architectures, DDD, Software Architecture: The Hard Parts.

## System design procedure for the lead

Run this before a significant feature. For small items, steps 1, 6, 8 and 11 are enough.

1. Clarify requirements, scope and non-goals, both functional and non-functional. (Xu; Fundamentals of SA)
2. Pick the top 3 architecture characteristics and a target for each. (Fundamentals of SA)
3. Make a back-of-envelope estimate: users, QPS, data growth, read/write ratio. Skip it when the numbers are trivially small. (Xu; DDIA)
4. Model the domain: bounded contexts, the domain's language, and where the feature lives. (Khononov; Evans)
5. Design the data: model, storage, consistency and transaction needs, and a schema-change plan. (DDIA)
6. Draft two alternatives and compare their trade-offs. (Ousterhout; Hard Parts)
7. Define module and API boundaries as deep modules, with versioning and backward compatibility. (Ousterhout; Newman)
8. Plan for failure: timeouts, bounded retries with jitter, idempotency, and circuit breakers where they are justified. (Nygard; Vitillo)
9. Define SLIs/SLOs and observability. (SRE books)
10. List trust boundaries and where untrusted data enters, plus abuse cases. The reviewer checks against this list in the security review.
11. Plan the rollout: expand-contract migrations, feature flags, small batches, a rollback path. (Evolutionary Architectures; DORA)
12. Write an ADR and add fitness functions or tests that protect the chosen characteristics. (Fundamentals of SA; Evolutionary Architectures)

## What to skip on small projects (YAGNI)

- Microservices, sagas, event sourcing, CQRS: start with a modular monolith.
- Formal SLOs and error budgets: one uptime and latency target is enough.
- Full tactical DDD: keep only bounded contexts and the domain's language.
- Sharding, multi-region, custom caches: wait until the numbers or real metrics justify them.
- Circuit breakers: optional. Timeouts and bounded retries are still mandatory.
- ADRs: only for decisions that are hard to reverse.

Rule of thumb: design for about 10x current load, not 1000x.

## Rules for the lead

- Follow the project phase. Anything the phase doesn't need becomes a Later line with a measurable trigger, listed in the design note and added to the plan's Later section.
- Never defer the never-deferred items (authorisation, secrets, privacy, data integrity, timeouts and retries, tests and review, basic accessibility). Design them in now.
- Leave every PM decision open in the note, with options and a recommendation.
- Spend real design effort only on decisions that are expensive to undo. Those get an ADR.

## Design note template (`docs/design/<item>.md`)

Fill every heading. Write `n/a — <reason>` where a heading doesn't apply.

```markdown
# <Item> — design note

Date: <YYYY-MM-DD> — Size: large — <why> — Phase: <MVP | Growth | Scale> — Status: draft, waiting for PM

## Context
<The problem, who it is for, what exists today. Links to the plan item.>

## Requirements and non-goals
- Functional: <...>
- Non-functional: <...>
- Non-goals: <what this item will not do>

## Top 3 qualities
| Quality | Target | How we check it |
|---|---|---|
| <e.g. data integrity> | <e.g. no double charge per booking> | <test or measurement> |

## Estimate
<users, requests per second, data growth, read/write ratio — or "trivially small: <numbers>">

## Data
<model, storage, constraints, consistency and transactions, schema-change plan (expand → migrate → contract)>

## Options
### A: <name>
<how it works; benefits; costs and risks; effort>
### B: <name>
<how it works; benefits; costs and risks; effort>

## Decision
<A or B and why; what we give up. ADR link if hard to reverse. "Waiting for PM" if the PM must choose.>

## Failure plan
<every outbound call: timeout, bounded retries with jitter, idempotency key; what the user sees on failure>

## Observability
<health check, error logs without personal data, the one or two numbers to watch>

## Trust boundaries and abuse cases
- Boundaries: <where untrusted data enters: requests, webhooks, uploads, third-party responses>
- Abuse cases: "As an attacker I <action> so that <gain>" — mitigation: <...>

## Privacy
<from references/privacy.md, or "n/a — no personal data">

## Rollout and rollback
<migration order, feature flag, small batches; how to roll back and how to confirm it worked>

## Later lines
- <what> — <why> — trigger: <measurable condition> — noted <date> by lead
```

## ADR template (`docs/adr/<NNNN>-<title>.md`)

Michael Nygard's format. One decision per ADR. Number them in order; never edit an accepted ADR. Write a new one that supersedes it.

```markdown
# <NNNN>. <Title>

Date: <YYYY-MM-DD>

## Status
<Proposed | Accepted | Superseded by <NNNN>>

## Context
<The forces at play: the problem, the constraints, the options considered.>

## Decision
<What we will do, in active voice: "We will ...".>

## Consequences
<What becomes easier, what becomes harder, and what we give up.>
```
