All four gates have passed. Here is the PM update — the merge is yours to approve, and I have not merged.

---

**Status:** M1 — on track, waiting on you. The health endpoint is finished and accepted by QA; nothing is merged until you say so.

**Done since last update**

- Nothing is on main yet, so nothing is "done" by our definition. The work below is complete and sitting on the branch `feat/health-endpoint`, with every gate passed.

**How you can check it**

(Copied from QA's `PM check` section, `docs/qa/m1.md#pm-check`. QA ran steps 1–6 and 8–10 verbatim and saw each result; step 7 is the one they could not run and would like you to eyeball. You need a Mac or Linux machine with Python 3.12, **two Terminal windows**, and about 5 minutes. Nothing to install. Replace `<project folder>` with the folder holding this project.)

1. Open Terminal and go to the project folder:
```bash
cd <project folder>
```
→ expect the prompt to come back with no message. `No such file or directory` means the path is wrong.

2. Get the right version of the code:
```bash
git switch feat/health-endpoint
```
→ expect `Switched to branch 'feat/health-endpoint'` or `Already on 'feat/health-endpoint'`. Both are fine. If you see `error: Your local changes would be overwritten`, stop and tell me — don't force anything.

3. Check Python:
```bash
python3 --version
```
→ expect `Python 3.12.3` (any `3.12.x` is fine). Anything lower, or `command not found`, stop and tell me.

4. Run the automated tests:
```bash
python3 -m unittest -v
```
→ this prints **several hundred lines**, including alarming-looking web addresses like `/<script>alert(1)</script>` and `/../../etc/passwd`. That is normal — those are deliberate attack-style requests our tester fires at the service to prove it shrugs them off. Ignore all of it and read only the **last two lines**, which must say:
```
Ran 16 tests in 3.263s
OK (expected failures=1)
```
The seconds will differ on your machine. `expected failures=1` is not a problem — it is one known limitation we have deliberately written a test for and parked (see "Security & privacy" below). If the last line says `FAILED`, send me the last 20 lines.

5. Start the service:
```bash
python3 app.py
```
→ expect **nothing to happen and your prompt not to come back**. That silence means it worked. Leave this window alone and open a **second Terminal window**. (`Address already in use` means something else has the port — tell me.)

6. In the **second** window, go to the project folder and ask the service if it is healthy:
```bash
cd <project folder>
```
```bash
curl -s -i http://127.0.0.1:8765/health
```
→ expect, give or take the date and Python version:
```
HTTP/1.0 200 OK
Server: BaseHTTP/0.6 Python/3.12.3
Date: Tue, 13 Oct 2026 08:53:09 GMT
Content-Type: application/json
Content-Length: 16

{"status": "ok"}
```
The three things that matter: first line says **200 OK**, the type is **application/json**, and the last line is exactly **`{"status": "ok"}`**. `Failed to connect` means the service in the first window isn't running — redo step 5.

7. See the same thing in a web browser — open http://127.0.0.1:8765/health
→ expect a near-blank page showing `{"status": "ok"}` and nothing else. No logo, no design: this is a page for machines, not people, so plain text is the correct result. **This is the one step QA could not run** (no browser in their environment); they reproduced it with a request carrying a real Chrome's exact headers and got the same 200 and the same body. Please eyeball it for us.

8. Check it behaves on a page that doesn't exist:
```bash
curl -s -i http://127.0.0.1:8765/nope
```
→ expect first line `HTTP/1.0 404 Not Found`, last line `{"error": "not found"}`. A 404 here is the **correct, passing** result — it proves the service answers tidily instead of crashing.

9. Check the notes list still works:
```bash
curl -s http://127.0.0.1:8765/notes
```
→ expect exactly `[]`. This confirms the new health feature didn't disturb what was already there.

10. Stop the service: go back to the **first** window and press **Ctrl+C**
→ expect a **red multi-line error block** ending in `KeyboardInterrupt`, then your prompt. **This is normal, not a bug** — it is Python's way of saying "I was interrupted", which is exactly what Ctrl+C does. Nothing was installed and the service creates no files, so there is nothing to tidy up.

**In progress**

- **Health endpoint** — lead — waiting on your merge approval, and nothing else. Developer pass · tester pass (16 tests, green) · reviewer approve with notes · QA accept. Design note, ADR, UI spec and privacy screen are all `n/a — small item, no UI, no personal data`; the gates themselves were not reduced.

**Design:** none — this was a small item (one module, no new data store, integration, trust boundary or personal data), so no design note, UI spec, ADR or deck was needed.

**Security & privacy:** 7 open findings, all Low, none blocking. Five now have dated owners and due dates in `docs/PLAN.md`. Nothing needs a decision from you. In plain terms: (a) the server handles one request at a time, so a client that opens a connection and never finishes its request can mute the health check until it goes away — this is loopback-only and already true on main, but **it must be re-scored as serious before this service is ever exposed beyond this machine**; (b) `/health?t=1` returns "not found" and `HEAD /health` is refused — invisible when you check by hand, but many uptime monitors and load balancers probe exactly those two ways, so both need fixing *before* we wire this to a monitor; (c) the server tells callers its exact Python version. Privacy: QA verified for real that this endpoint reads, writes and returns no personal data, and that nothing personal lands in the log — a cookie and a browser identity sent in got the identical 16-byte answer back. The access log does record the caller's address, which is personal data under UK/EU rules, but while we bind to this machine only it can never be anything but `127.0.0.1`. That stops being true the day the address changes.

**Later list:** none — no deferrals were made. The reviewer's position, which I accepted: dated plan tasks are the stronger instrument here, so these went into the plan with owners and dates rather than onto the Later list.

**Marketing:** none — no marketer dispatched, no launch comms in scope for this item.

**Next up**

1. **Merge the health endpoint**, once you approve — a local `git merge --no-ff` (there is no remote and I will not push). Then I tick the M1 box.
2. **The five review follow-ups** in `docs/PLAN.md` — the slow-client fix and the query-string routing fix are due 2026-10-20; ordering is your call.
3. **Accounts and newsletter** (the other M1 item) — this one is large: new personal data, sign-in, account deletion and newsletter consent. It needs a design note, a UI spec, a privacy section and a deck for your approval before anyone writes code, and it carries the open question of the lawful basis for the newsletter. I'll bring you options and a recommendation; I won't choose it.

**Blockers by role**

| Role | Blocker | Who can unblock | Impact |
| --- | --- | --- | --- |
| Developer | none | — | — |
| Tester | none | — | — |
| Reviewer | none | — | — |
| QA | Couldn't run the browser check (step 7) — no browser in their environment; reproduced with a real Chrome header set instead | PM, in about a minute | Browser rendering stays inferred, not observed. Low — the endpoint is machine-facing and the command-line check covers the contract |
| Marketer | none | — | — |
| Lead | Merge approval is yours and I can't proceed without it | PM | The branch stays unmerged and the M1 box stays unticked |

**Needs you**

- **Approve the merge of `feat/health-endpoint` into main.** All four gates passed: tester 16 tests green, reviewer "approve with notes" with no blocks, QA accept with 7/7 criteria passing, and the check steps above verified. My recommendation: approve. The alternative is to hold it until the slow-client and HEAD fixes land, which I don't recommend — the endpoint meets its acceptance criterion today, the open findings are all Low, and two of them already existed on main before this work started.
- Optional, one minute: run step 7 in a browser so we can mark that observed rather than inferred.

**Risks**

- The slow-client weakness is harmless while we bind to this machine only, and serious the moment we don't — mitigated by the dated plan task and by the explicit instruction in it to re-score the severity before any change of bind address.
- `HEAD` and query-string probes don't return 200, so wiring this to a monitor before those fixes would produce false alarms — mitigated by the two dated plan tasks, both due before any monitoring work.

---

Everything is recorded: `docs/status.md` (created — CLAUDE.md named it but the file didn't exist), `docs/qa/m1.md` for the QA evidence, and the five follow-ups in `docs/PLAN.md`. The branch is unmerged and nothing was pushed. I'll stop here until you approve.
