# Data and APIs checklist

Checked: 2026-10-12. Check the current source when a rule decides an outcome.

Use this for data stores, APIs, migrations, integrations and background jobs. Work through every item. For an item that doesn't apply, write `n/a — <reason>`.

1. Write and agree the API contract (OpenAPI or the project's equivalent) **before** code, including the error shape and pagination. If the brief doesn't define them, raise a spec gap with the lead.
2. Follow the lead's design note. If you must deviate, record it in the hand-off under "Deviations from plan".
3. Database changes are expand → migrate → contract. Each step works with both the old and the new code, and is reversible.
4. The database enforces invariants (constraints, foreign keys, uniqueness).
5. Transactions are scoped to one aggregate. Commit local work before calling an external system.
6. Every outbound call has a timeout, and retries are bounded with backoff and jitter. Retry only idempotent operations.
7. Unsafe operations that clients may retry (payments, sign-up, sends) take an idempotency key.
8. No N+1 queries (assert the query count in a test), and indexes match the access paths.
9. Structured logs carry a request ID, route, status and duration. No secrets, tokens or personal data.
10. Config and secrets come from env or a secrets manager. Nothing sensitive is committed.
11. Authorisation is checked server-side on every object, and input is validated at the boundary.
12. MVP phase: no caching, sharding, replicas or queues for scale. Write a Later line with a trigger instead.

## Sources

`docs/research/backend-developer.md` (Checklist) and the design spec's "System design" developer row, in the my-tech-team repo.
