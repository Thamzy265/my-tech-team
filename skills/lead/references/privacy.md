# Privacy screen at planning (UK + EU)

Checked: 2026-10-12. Check the current source when a rule decides an outcome.

**Not legal advice.** These are practical checks a software team can do. Anything with legal weight, including the choice of lawful basis, goes to the PM (and a qualified person if the PM decides). The default scope is UK GDPR, DPA 2018 as amended by the Data (Use and Access) Act 2025, PECR, EU GDPR and ePrivacy. A project can add regions in its Team setup.

Use this for every item that adds, changes, shares or deletes personal data. The output is a **Privacy** section in the design note (or the brief, for a small item), using the template at the end. Every item on the "Always escalate" list goes to the PM.

## Lead, at planning

Work through all 11. Write `n/a — <reason>` for any that don't apply.

1. List each personal data field with its purpose and lawful basis.
2. Remove the fields nobody needs.
3. Set a retention period for each category.
4. Screen for a DPIA against the ICO list.
5. Check whether children are likely users.
6. Check for automated decisions or profiling with significant effects.
7. List new vendors and SDKs, with their contracts and transfer mechanisms.
8. Check for special category data.
9. Set private defaults.
10. Plan export, delete and rectify.
11. Note the updates needed to the record of processing and the privacy notice.

For item 1, you list the fields and purposes. **The PM decides the lawful basis.** Write "PM decides" with the likely options; never pick one yourself.

## DPIA triggers (ICO list)

Screen against each. If any applies, the DPIA decision goes to the PM. Write the result in the Privacy section: "DPIA screening: <triggers hit, or none> — <PM decision needed | not needed because ...>".

- Large-scale profiling.
- Special category data.
- Children.
- Location tracking.
- New technology or AI.
- Automated significant decisions.
- Combining datasets.
- Invisible processing.
- Denying a service based on data.

Source: https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/accountability-and-governance/data-protection-impact-assessments-dpias/

## Rules the plan must include

- **Minimisation:** collect only fields that have a documented use; optional fields are optional in the UI.
- **Retention:** a period per data category, enforced by an automated deletion job that also covers backups and caches.
- **Rights the software must support:** access/export (respond within 1 month), erasure (including at processors), rectification, portability (machine-readable), objection, restriction, marketing opt-out.
- **Private by default:** the most private settings are the default; nothing is public by default.
- **Purpose limitation:** don't reuse data for a new purpose without a compatibility check.

## If the item sends marketing email or SMS, or sets cookies

- **Email, SMS and DMs need consent**, or the **soft opt-in**: an existing customer, similar products, an opt-out offered at collection, and an opt-out in every message. UK B2B emails to corporate addresses are exempt; EU rules vary by country.
- Record consent per contact: what they agreed to, the source and the date. A newsletter sign-up is its own unticked choice, never bundled with sign-up or terms.
- **Cookies:** nothing non-essential runs before the user chooses. Reject is as easy as Accept. No pre-ticked boxes. Consent is easy to withdraw. The EU needs consent for every non-essential cookie, analytics included. The UK statistics exception covers first-party, aggregate usage figures only, with clear information and an easy way to object; advertising and tracking still need consent.

## Always escalate to the PM

- **Any breach or suspected breach, immediately — 72-hour clock.** The clock to notify the ICO starts on awareness.
- Processing that triggers a DPIA or is high risk.
- Special category, children's, criminal-offence or biometric data.
- AI or automated decisions with significant effects.
- Choosing a lawful basis, especially (recognised) legitimate interests.
- New international transfers, new processors or new contracts.
- Access requests, erasure disputes and complaints.
- Any contact with a regulator.
- Public privacy or security claims.
- Scraping.
- Selling or sharing data.
- Anything that depends on unconfirmed details: the exact commencement of each DUAA section, final ICO guidance on recognised legitimate interests and automated decisions, and the status of the EU Digital Omnibus. Check legislation.gov.uk and ico.org.uk first.

## Privacy section template

```markdown
## Privacy

Not legal advice. Items marked "PM decides" need the PM's decision before the developer starts.

| Field | Purpose | Lawful basis (PM decides) | Retention | Shared with | Notes |
|---|---|---|---|---|---|
| <field> | <why we need it> | PM decides — options: <e.g. contract, consent> | <period, and the deletion job> | <processor and region, or none> | <optional? private default? export/delete/rectify> |

- Fields removed: <fields we don't need, or none>
- DPIA screening: <triggers hit, or none> — <PM decision needed | not needed because ...>
- Children likely: <yes/no — why>
- Automated decisions or profiling: <none | what>
- Special category data: <none | what>
- New vendors / SDKs / transfers: <none | vendor — contract — transfer mechanism>
- Private defaults: <...>
- Export, delete, rectify: <how each works, including backups and processors>
- Marketing consent: <n/a | how consent or soft opt-in is collected and recorded; opt-out in every message>
- Record of processing and privacy notice updates: <...>
- Escalated to PM: <list, or none>
```
