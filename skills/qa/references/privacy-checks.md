# Privacy checks in the real product

Checked: 2026-10-12. Check the current source when a rule decides an outcome.

**Not legal advice.** These are behaviour checks a QA agent can run and record. Whether something is lawful, which basis applies, and any public compliance claim go to the PM through the lead.

Run every item for every change that touches personal data, cookies, tracking, consent, accounts, email or the privacy notice. Record each as `PASS`, `FAIL` or `n/a — <reason>` in `docs/qa/<milestone>.md`, with the date, the environment and masked evidence. Use a fresh browser profile or private window for each consent check, so earlier choices don't hide a problem.

**Evidence sources, best first:** the browser network panel and storage view; the served page source and local requests (`curl -s`, `curl -sI` against local hosts only); the code and config. Never contact third-party hosts unless the project's rules allow it. Write down what you could not observe.

**Checks that need access to processors or third-party systems** (a processor's dashboard, a mail provider's list, an analytics account) are recorded under "Not observed" in the evidence file, with who can check them (usually the PM). Never mark them PASS from the app's side alone.

## UK vs EU: analytics cookies

- **EU (GDPR + ePrivacy):** every non-essential cookie or similar technology needs consent first, **analytics included**.
- **UK (PECR as amended by DUAA; ICO guidance of 29 Apr 2026):** a statistics exception allows **first-party, aggregate** usage analytics without consent, only with clear information, an easy way to object, and no tracking of individuals. Third-party analytics that track individuals, advertising and tracking still need consent.
- **Both:** nothing non-essential runs before the user chooses; Reject is as easy as Accept; no pre-ticked boxes; consent is easy to withdraw.
- If the project serves both UK and EU users (the default), apply the EU rule: analytics waits for consent.

## The 10 checks

1. **Before any choice, nothing non-essential runs.**
   How to check: open the browser dev tools Network tab, clear it, reload, and make no choice on the banner. Expect no requests to analytics or ad domains, and no non-essential cookies under Application → Cookies (or Storage → Cookies). Without a browser: in the served page source, look for analytics or ad scripts in `<head>` or anywhere that loads before the consent check, and for `Set-Cookie` headers on the first response. Quote the line.

2. **Reject is as easy as Accept, and rejecting really blocks trackers.**
   How to check: compare the two options on the first layer: same layer, same number of clicks, similar size, weight and contrast (measure the colours; a faded link next to a bold button fails). Then reject in a fresh profile, clear the Network tab, browse three pages, and expect no analytics or ad requests and no new non-essential cookies.

3. **Withdrawing consent works.**
   How to check: accept, then find the way to change the choice (footer link or settings) and record how many clicks it takes. Withdraw, clear the Network tab, browse, and expect trackers to stop and their cookies to be removed or no longer set. Withdrawing should be as easy as giving consent.

4. **Data export is complete and machine-readable.**
   How to check: create a test account with known synthetic data in every field the privacy section lists. Request the export. Expect a machine-readable file (JSON or CSV) that contains every listed field and item, and no other user's data.

5. **Account deletion removes the data, including after a new sign-in and from emails.**
   How to check: delete the test account. Sign in again with the same details and expect no old data. Check the admin or database view for the record; record the listed processors under "Not observed", with who can check them. Trigger an email that would have gone to the account (newsletter, reminder) and expect none. Note any data the privacy section says is kept, and for how long.

6. **Corrections are saved and shown.**
   How to check: change a profile field, reload, sign out and in, and expect the new value everywhere it appears (profile page, emails, export).

7. **Unsubscribe works on the first click.**
   How to check: subscribe a test address, open the unsubscribe link from a real sent message in a local mail catcher (an external test inbox only if the project's rules allow it), and expect one click, no sign-in and no extra form. Trigger the next send and expect nothing to arrive. Also check the signup form: a marketing consent checkbox must start unticked.

8. **The privacy notice matches what the app collects and which vendors it uses.**
   How to check: list every field the forms collect and every third-party host seen in the Network tab or the page source. Compare with the privacy notice. Every field and vendor must be named, with its purpose. Anything missing is a FAIL.

9. **A route for privacy requests and complaints exists.**
   How to check: from the app or the privacy notice, find how to make a privacy request (access, deletion, correction) and how to complain. Expect a working contact route and, for the UK, a mention of the right to complain. Send nothing to a real address; record the route only.

10. **Children's defaults are in place where relevant.**
    How to check: only if the project says under-18s are likely users (otherwise `n/a — <reason>`). Create a new account and expect the most private settings by default: profile not public, geolocation off, profiling and personalised ads off, and no nudges to turn them on.

## Recording a failure

One line per failure in the evidence file and the bug: the check number, what you saw (request URL with any personal data masked, cookie name, script line, size or contrast numbers), what was expected, and steps to reproduce. Report it to the lead; the developer fixes it.
