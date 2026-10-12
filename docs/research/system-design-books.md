# Research: system design and architecture books

Checked 12 Oct 2026. Ideas are paraphrased. Items marked *(not checked)* are recalled, not confirmed against a source.

## Shortlist

| # | Book | Author(s) | Edition / year | Best for | Roles |
|---|---|---|---|---|---|
| 1 | Designing Data-Intensive Applications | Martin Kleppmann, Chris Riccomini | 2nd ed., O'Reilly, 2026 | Data models, storage, replication, consistency, streams | Lead, Backend |
| 2 | Fundamentals of Software Architecture | Mark Richards, Neal Ford | 2nd ed., O'Reilly, 2025 | Architecture characteristics, styles, ADRs, governance | Lead |
| 3 | Site Reliability Engineering + The SRE Workbook | Beyer et al. (Google) | 2016 / 2018 | SLOs, error budgets, monitoring, incidents | Lead, Backend, QA |
| 4 | Release It! | Michael Nygard | 2nd ed., 2018 | Stability patterns for production | Backend, Security |
| 5 | A Philosophy of Software Design | John Ousterhout | 2nd ed., 2021 | Managing complexity in modules and APIs | Frontend, Backend, Reviewer |
| 6 | Building Evolutionary Architectures | Ford, Parsons, Kua, Sadalage | 2nd ed., O'Reilly, 2022 | Fitness functions, incremental change | Lead, Tester |
| 7 | Learning Domain-Driven Design | Vlad Khononov | O'Reilly, 2021 (Evans' *Domain-Driven Design*, 2003, *not checked*) | Bounded contexts, subdomains | Lead, Backend |
| 8 | Accelerate + DORA metrics | Forsgren, Humble, Kim (2018, *not checked*); dora.dev | DORA now has five metrics (rework rate added 2024) | Delivery performance | Lead, QA |
| 9 | Understanding Distributed Systems | Roberto Vitillo | 2nd ed., 2022 | Practical distributed systems | Backend |
| 10 | System Design Interview Vol. 1 & 2 | Alex Xu (Vol. 2 with Sahn Lam) | 2020 *(not checked)* / 2022 | Back-of-envelope estimates, worked designs | Lead, Backend |
| 11 | Building Microservices | Sam Newman | 2nd ed., O'Reilly, 2021 | Service boundaries, migrating off a monolith | Lead, Backend |
| 12 | Software Architecture: The Hard Parts | Ford, Richards, Sadalage, Dehghani | O'Reilly, 2021 | Trade-off analysis, distributed data, sagas | Lead |

Also useful: *Team Topologies* (Skelton & Pais, 2nd ed., 2025) for how the team is structured, and *Designing Distributed Systems* (Brendan Burns, 2nd ed., 2024).

## Ideas to turn into skill rules

- **DDIA:** state reliability, scalability and maintainability needs; describe load with numbers; use p95/p99 percentiles, not averages; pick the consistency model on purpose; make retries safe (idempotency); plan schema changes that stay backward and forward compatible.
- **Fundamentals of SA:** choose the top 3 architecture characteristics and design from them; write an ADR (context, decision, consequences) for each decision that is hard to reverse; default to a modular monolith.
- **SRE:** set SLIs/SLOs per user journey; use an error budget to decide between features and reliability; alert on symptoms or SLO burn rate, not causes; watch the four golden signals (latency, traffic, errors, saturation); write blameless postmortems.
- **Release It!:** a timeout on every outbound call; circuit breakers and bulkheads; retries with backoff and jitter; fail fast; treat every integration point as a failure source.
- **Ousterhout:** deep modules (simple interface, lots of functionality); information hiding; define errors out of existence; design it twice; comments explain *why*.
- **Evolutionary Architectures:** automated fitness functions (dependency rules, performance budgets); expand-contract migrations for schemas and APIs.
- **DDD:** bounded contexts and a context map; the domain's language in code; put most effort into the core subdomain; an anti-corruption layer in front of external systems.
- **DORA:** small batches, trunk-based work, measure lead time, deploy frequency, change fail rate, recovery time and rework rate.
- **Vitillo:** assume the network is unreliable; idempotency keys; caches with explicit invalidation and TTLs.
- **Alex Xu:** clarify scope first; estimate QPS, storage and bandwidth; high-level design first, then dig into the bottlenecks.
- **Newman:** split by business capability and keep each service's data private; strangler fig migration; avoid a distributed monolith.
- **Hard Parts:** every architecture choice is a trade-off, so write down what you give up.

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
10. Hand trust boundaries to the security engineer for threat modelling.
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

## Sources

- https://martin.kleppmann.com/2026/03/24/designing-data-intensive-applications-2e.html
- https://www.oreilly.com/library/view/-/9781098175504
- https://nealford.com/books/
- https://sre.google/books/
- https://www.oreilly.com/library/view/release-it-2nd/9781680504552/
- https://nealford.com/books/bea2e.html
- https://www.oreilly.com/library/view/building-microservices/9781492034018
- https://www.oreilly.com/library/view/software-architecture-the/9781492086888/
- https://itrevolution.com/book/team-topologies/
- https://dora.dev/guides/dora-metrics/history/
- https://oreilly.com/library/view/designing-distributed-systems/9781098156343
