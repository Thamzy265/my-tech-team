# Research: security engineer

Checked 12 Oct 2026. This is the source material for the `team-security` skill. The role is defensive and advisory. The PM decides whether a risk is accepted.

## Top voices and standards

| Who / what | Signature idea | Source |
|---|---|---|
| OWASP Top 10:2025 | A01 Broken Access Control (now includes SSRF), A02 Security Misconfiguration, A03 Software Supply Chain Failures, A04 Cryptographic Failures, A05 Injection, A06 Insecure Design, A07 Authentication Failures, A08 Software or Data Integrity Failures, A09 Security Logging and Alerting Failures, A10 Mishandling of Exceptional Conditions | https://top10.owasp.org/2025 |
| OWASP ASVS 5.0.0 (May 2025) | About 350 requirements; levels L1, L2, L3 | https://asvs.dev |
| OWASP Top 10 for LLM Apps 2025 | Prompt injection, sensitive information disclosure, supply chain, poisoning, improper output handling, excessive agency, system prompt leakage, vector weaknesses, misinformation, unbounded consumption | https://genai.owasp.org/llm-top-10/ |
| OWASP Top 10 for Agentic Apps 2026 | ASI01 Agent Goal Hijack, and others | https://genai.owasp.org |
| Adam Shostack / Threat Modeling Manifesto | Four questions: What are we working on? What can go wrong? What are we going to do about it? Did we do a good job? Plus STRIDE | https://threatmodelingmanifesto.org/ |
| CWE Top 25 2025 | XSS, SQLi, CSRF, missing authorisation, OOB write, path traversal… | https://cwe.mitre.org/top25/archive/2025/2025_cwe_top25.html |
| NIST SSDF SP 800-218 | v1.1 is final (v1.2 is a draft) | https://csrc.nist.gov/Projects/ssdf/publications |
| CISA Secure by Design | Own customer security outcomes; remove whole classes of vulnerabilities; publish a vulnerability disclosure policy | https://www.cisa.gov/securebydesign |
| SLSA | Build levels L0–L3 (provenance) | https://slsa.dev |
| OpenSSF Scorecard | Automated repo checks (pinned dependencies, token permissions, branch protection) | https://github.com/ossf/scorecard |
| CVSS v4.0 | Base score alone is not risk; name the metric groups used (B/BT/BE/BTE) | https://www.first.org/cvss/v4-0/ |
| Tanya Janca, Troy Hunt, Bruce Schneier | Developer-friendly secure SDLC; breach realism; security as a process | https://shehackspurple.ca, https://www.troyhunt.com, https://www.schneier.com |

## Plan

- **Threat model** each new feature, trust-boundary change or new data flow: a data-flow diagram, STRIDE per element (plus the LLM/Agentic lists when AI is involved), ranked threats and mitigations.
- **Data classification:** public, internal, confidential, restricted.
- **ASVS level:** L1 for prototypes, L2 when there are accounts, PII or payments, L3 for high-value targets. The relevant requirements become acceptance criteria.
- **Abuse cases:** "As an attacker I…" stories next to the user stories.

## Verify

- **Review focus:** authorisation on every endpoint and object, input reaching sinks (SQL, shell, HTML, templates, deserialisation), SSRF, file upload, crypto, error paths that fail open, session and token handling.
- **Tools:** SAST (Semgrep/CodeQL), SCA/OSV on the lockfile, DAST on preview environments, secret scanning (gitleaks/trufflehog).
- **Supply chain:** committed lockfiles, Actions pinned to SHAs, least-privilege tokens, SBOM (CycloneDX/SPDX), Scorecard, typosquat checks on new packages.
- **Logging:** security events are logged; secrets and PII are not.
- **Incident readiness:** `security.txt` or a disclosure policy, a runbook, key-rotation steps.

## Severity and the merge gate

- CVSS v4.0, stating which label is used. Low 0.1–3.9, Medium 4.0–6.9, High 7.0–8.9, Critical 9.0–10. Adjust for reachability and CISA KEV listings.
- **Blocks the merge:** any Critical or High, a leaked secret, missing authorisation on a new endpoint, a reachable KEV-listed or Critical dependency, an unmitigated top threat.
- A Medium needs a task with a due date. Accepting a risk needs the PM's written sign-off.

## Checklist

1. The data-flow diagram and trust boundaries are current.
2. Data is classified, and PII and secret flows are identified.
3. An ASVS level is chosen and its requirements are mapped to tasks.
4. Abuse cases are written and have tests.
5. Authentication is correct, and authorisation is enforced server-side on every route and object.
6. Untrusted input is validated or encoded for each sink.
7. No SSRF, unsafe deserialisation or unrestricted upload.
8. Errors fail closed and do not leak internals.
9. Standard crypto libraries only; no hard-coded keys.
10. Secret scan is clean.
11. SCA shows no reachable High/Critical or KEV dependencies; versions are pinned.
12. CI uses SHA-pinned Actions and least-privilege tokens, and produces an SBOM.
13. Security events are logged without secrets, and alerts are defined.
14. LLM features use least-privilege tools, treat model output as untrusted, and keep a human approval step for destructive actions.
15. Security headers, CORS and other defaults are secure.

## Split with the reviewer

- **Reviewer:** correctness, readability, tests, performance. Flags security smells to the security engineer.
- **Security engineer:** threat model, ASVS requirements, authN/authZ, crypto, injection and SSRF, secrets, dependencies and supply chain, LLM risk, CVSS severity, and the security verdict.
- Either role can block a merge. Security has the final word on security severity. The PM decides on risk acceptance.

## Not verified

- The OWASP Top 10:2025 release status.
- The ASVS per-level percentages.
- The SSDF v1.2 changes.
- The SLSA v1.2 date.
- The Scorecard check details.
- The CVSS v4 bands (from memory; they match v3).
- The LLM and Agentic lists (from secondary sources).
