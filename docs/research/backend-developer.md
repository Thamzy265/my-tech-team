# Research: backend developer

Checked 12 Oct 2026. This is the source material for the `team-backend` skill. Ideas are paraphrased.

## Top voices

| Who | Signature idea | Source |
|---|---|---|
| Google SRE | Four golden signals; SLIs, SLOs, error budgets and an error-budget policy | https://sre.google/sre-book/monitoring-distributed-systems/, https://sre.google/workbook/implementing-slos/ |
| Michael Nygard | *Release It!* stability patterns (timeouts, circuit breaker, bulkheads); ADRs | https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions |
| Martin Fowler / Danilo Sato | Parallel change: expand → migrate → contract | https://martinfowler.com/bliki/ParallelChange.html |
| Ham Vocke | Practical test pyramid; consumer-driven contract tests | https://martinfowler.com/articles/practical-test-pyramid.html |
| Kent Beck | TDD: red, green, refactor | *Test-Driven Development by Example* |
| Kleppmann & Riccomini | *DDIA* 2nd ed.: replication, transactions, consistency, evolvable encodings | https://martin.kleppmann.com/2026/03/24/designing-data-intensive-applications-2e.html |
| Sam Newman / Eric Evans | Bounded contexts, information hiding, aggregates as consistency boundaries | https://samnewman.io, https://www.domainlanguage.com/ddd/ |
| Charity Majors / Honeycomb | Wide, structured, high-cardinality events | https://www.honeycomb.io/blog/why-observability-2-0-gamechanger |
| Tom Wilkie / Brendan Gregg | RED (services) and USE (resources) methods | https://grafana.com/blog/2018/08/02/the-red-method-how-to-instrument-your-services/, https://www.brendangregg.com/usemethod.html |
| Stripe / Brandur Leach | Idempotency keys: replay the first response, reject a reused key with different parameters, atomic phases | https://docs.stripe.com/api/idempotent_requests, https://brandur.org/idempotency-keys |
| Google AIP / Microsoft | API design rules: resources, standard methods, errors, pagination, long-running operations | https://google.aip.dev/general, https://github.com/microsoft/api-guidelines |
| Twelve-Factor App | Config in env, stateless processes, disposability, logs as streams | https://12factor.net/ |
| OpenAPI | OAS 3.2.0 (Sept 2025), backward compatible with 3.1 | https://www.openapis.org/ |
| Chris Richardson | Transactional outbox, saga | https://microservices.io/patterns/data/transactional-outbox.html |

## How they plan

- **Contract first:** an OpenAPI document agreed with the frontend before code, covering errors, pagination and versioning. A mock from the contract unblocks the frontend.
- **Domain and data model:** aggregates, transaction boundaries and isolation level; an outbox for events.
- **Migrations:** an expand → migrate → contract plan that says which steps can be reversed.
- **ADRs** for decisions that are hard to reverse.
- **Rough capacity estimates** that turn into SLO targets.

## How they implement

- Test-first, pyramid shape: unit tests for domain logic, integration tests against a real database and real HTTP, a provider contract test against the OpenAPI document, minimal E2E.
- Backward-compatible migrations: add nullable columns, dual-write, backfill, switch reads, and drop the old column in a later deploy.
- Idempotency keys on unsafe POSTs.
- A timeout on every outbound call; bounded retries with backoff and jitter, only for idempotent operations; graceful shutdown.
- One wide structured log event per request, with request and trace IDs, and no secrets or PII.
- Config and secrets from env or a secrets manager. Feature flags separate deploy from release.

## What they keep watch on

- RED per endpoint and USE per resource (connection pools, queues); SLO burn.
- N+1 and slow queries: EXPLAIN plans, index coverage, bounded pools.
- Data integrity: database constraints, uniqueness, an audit of each backfill.
- Backward compatibility: no removed or renamed fields and no new required fields without a deprecation window. Diff the OpenAPI document in CI.
- Object-level authorisation on every resource (OWASP API1, BOLA), input validation, rate limits.

## Checklist

1. OpenAPI contract agreed with the frontend, with examples and an error model.
2. An ADR for each significant decision.
3. Data model plus an expand/contract migration plan with a rollback.
4. Failing tests written first; the pyramid respected.
5. Provider contract tests pass.
6. Migrations work with both the old and the new code (N-1).
7. Unsafe POSTs are idempotent.
8. Every outbound call has a timeout and bounded, jittered retries.
9. The database enforces invariants; transactions are scoped to aggregates.
10. No N+1 queries (query count asserted in tests); indexes match access paths.
11. Structured logs carry request IDs and no secrets or PII.
12. RED metrics emitted; an SLO target set.
13. Config and secrets come from env or a vault.
14. Object-level authorisation, validated input, rate limits.
15. Risky changes are behind a flag, with a removal task.

## Not verified

The Beck, Evans, Newman, Richardson and OWASP API entries, OpenTelemetry and the N+1 guidance came from general knowledge, not fetched pages.
