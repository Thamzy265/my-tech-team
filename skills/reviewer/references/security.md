# Security and privacy review checklist

Checked: 2026-10-12. Check the current source when a rule decides an outcome.

Use this for every branch review and every feature review. Work through every item. For an item that doesn't apply, write `n/a — <reason>`. This is not legal advice; privacy decisions with legal weight go to the PM.

## Severity

1. Score each security finding with **CVSS v4.0** and state the label you used: `CVSS-B` (base only), `CVSS-BT` (base + threat), `CVSS-BE` (base + environmental) or `CVSS-BTE`. Give the vector string when you can.
2. Bands: **Low** 0.1–3.9, **Medium** 4.0–6.9, **High** 7.0–8.9, **Critical** 9.0–10.0.
3. Adjust for reality, and say how:
   - **Reachability:** can an attacker reach the code (public route, signed-in user, admin only, not reachable)?
   - **CISA KEV:** a dependency CVE on the Known Exploited Vulnerabilities list is treated as at least High.
4. If you can't compute a CVSS score reliably (for example, no calculator or unclear metrics), say so. Give the qualitative band plus a one-line basis instead: reachability and the data exposed. Write it as `no CVSS score: band + basis`. Example: `High (no CVSS score: band + basis) — any signed-in customer, downloads other customers' invoices`.
5. Every finding gets a severity. "Looks risky" is not a severity.

## Blocks the merge

Any one of these makes the verdict **Block**:

- [ ] any Critical or High finding;
- [ ] a leaked secret (in code, config, history, logs or tests): also tell the lead it must be rotated, since removing it from the diff is not enough;
- [ ] missing authorisation on a new endpoint or object (including IDOR: an ID from the client used without an ownership check);
- [ ] a reachable Critical or KEV-listed dependency;
- [ ] personal data, secrets or tokens in logs, URLs, query strings or analytics;
- [ ] an unmitigated top threat from the design note.

Medium with a dated task in the plan (added by the lead: owner + due date) → approve with notes; Low → approve with notes, listed in the report. Only the PM can accept a known risk: open `docs/status.md` and confirm the decision is there with its date.

## Checklist (OWASP Top 10:2025)

- [ ] **A01 Broken access control:** authorisation is enforced server-side on every route and every object; no IDOR (try another user's ID); no SSRF (user-supplied URLs are allow-listed, internal addresses blocked).
- [ ] **A02 Security misconfiguration:** secure defaults; security headers and a CORS policy that isn't `*` with credentials; no debug mode, stack traces or test accounts in production config.
- [ ] **A03 Software supply chain:** lockfile committed and matching; new packages checked for typosquats, maintenance and licence; CI Actions pinned to commit SHAs; CI tokens least-privilege.
- [ ] **A04 Cryptographic failures:** TLS for all traffic; standard crypto libraries only, no home-made crypto; no hard-coded keys, salts or IVs.
- [ ] **A05 Injection:** every input reaching a sink (SQL, shell, HTML, templates, file paths, deserialisation) is parameterised or encoded for that sink.
- [ ] **A06 Insecure design:** every abuse case in the design note is handled and has a test.
- [ ] **A07 Authentication failures:** sessions and tokens expire, rotate on login and are invalidated on logout; passwords stored with a slow hash (argon2, bcrypt, scrypt), never plaintext or reversible; rate limits on login and reset.
- [ ] **A08 Software or data integrity:** updates, uploads (type, size, storage location) and deserialised data are verified before use.
- [ ] **A09 Logging and alerting:** security events (login, failed auth, permission denied, admin actions) are logged without secrets or personal data; alerts are defined for them.
- [ ] **A10 Exceptional conditions:** errors fail closed (deny on error), and error responses don't leak internals (stack traces, SQL, paths).

## AI and LLM features

Only when the product uses AI. Otherwise write `n/a — no AI features`.

- [ ] Model output is treated as untrusted input: encoded before display, validated before use in any sink.
- [ ] Tools the model can call have least privilege.
- [ ] Destructive actions (delete, send, pay, publish) need a human approval step.
- [ ] No secrets or other users' data in prompts or system prompts.
- [ ] Usage is limited (rate limits, token or cost caps per user).

## Privacy in code (UK + EU)

- [ ] No personal data, tokens or secrets in logs, URLs, query strings, analytics events or error reports.
- [ ] TLS in transit; encryption at rest for sensitive data.
- [ ] Authorisation is checked on every endpoint and object.
- [ ] Retention and deletion jobs exist, are tested, and cover backups and caches.
- [ ] Erasure also reaches processors (third parties holding the data).
- [ ] New third-party SDKs and pixels are justified and load only after consent.
- [ ] No secrets in the repo.
- [ ] APIs return only the data the caller needs.
- [ ] Test data is synthetic, never production personal data.
- [ ] Cloud regions and data transfers are deliberate choices, recorded in the design note.

Anything on the PM escalation list (breach or suspected breach, special category or children's data, new processors or transfers, DPIA) goes to the lead for the PM at once. A suspected breach is reported immediately.

## Sources

`docs/research/security-engineer.md` and `docs/research/data-privacy.md` ("Reviewer, in code"), in the my-tech-team repo.
