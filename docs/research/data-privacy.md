# Research: data privacy (UK + EU)

Checked 12 Oct 2026. **Not legal advice.** These are practical rules a software team can check. Anything legal goes to the PM or a qualified person. The default scope is UK and EU. A project can add other regions in its Team setup section.

## Where the rules stand

### UK GDPR + DPA 2018, amended by the Data (Use and Access) Act 2025 (DUAA)

- The ICO says every DUAA change to data protection law and PECR is now in force.
  - 20 Aug 2025: technical changes.
  - 5 Feb 2026: most of Part 5.
  - 19 Jun 2026: the duty to handle complaints.
  - Sources: https://ico.org.uk/about-the-ico/what-we-do/legislation-we-cover/data-use-and-access-act-2025/, https://www.gov.uk/guidance/data-use-and-access-act-2025-plans-for-commencement
- Changes that matter to a software team:
  - **Recognised legitimate interests:** a new lawful basis for a fixed list of purposes. It needs no balancing test, but the right to object still applies.
  - **Automated decisions:** solely automated significant decisions are allowed with safeguards (information, a way to contest, human review). They are still prohibited when they use special category data.
  - **Access requests (DSARs):** a "reasonable and proportionate" search is enough. The clock stops while you wait for clarification or ID.
  - **PECR fines:** the maximum rises to £17.5m or 4% of global turnover.
  - **Cookies:** new consent exceptions (see below).
  - **Complaints (from 19 Jun 2026):** have a complaints process, acknowledge within 30 days, and mention the right to complain in the privacy notice.

### EU GDPR + ePrivacy Directive

- No changes in force yet. The **Digital Omnibus** (proposed 19 Nov 2025) is still going through the legislative process. **Follow the current law.**
- The EU still requires consent for every non-essential cookie, analytics included.

### Other rules

- **ICO Children's code:** applies to services likely to be used by under-18s. It requires high-privacy defaults, geolocation and profiling off by default, no nudges, and a DPIA. https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/
- **EU AI Act:** check it only when the product has AI features (prohibited uses, transparency duties).

### International transfers

- EU → UK: adequacy renewed to 27 Dec 2031.
- EU → US: the Data Privacy Framework is valid. The General Court upheld it on 3 Sep 2025, and an appeal is pending.
- UK → US: the UK Extension ("data bridge"). Otherwise the IDTA or the UK Addendum, plus a transfer risk assessment.

### US (not in the default scope)

- CCPA/CPRA regulations took effect in 2026.
- About 20 state laws are in force. They require opt-outs, honouring Global Privacy Control, and often opt-in for sensitive data.

## Principles as engineering rules

- **Lawful basis:** record every personal data field and its purpose with a lawful basis.
- **Purpose limitation:** do not reuse data for a new purpose without a compatibility check.
- **Minimisation:** collect only fields that have a documented use; optional fields are optional in the UI.
- **Storage limitation:** set a retention period per data category, enforced by an automated deletion job that also covers backups and caches.
- **Accuracy:** users can edit their data, and corrections reach every copy.
- **Security:** TLS everywhere, encryption at rest for sensitive data, least-privilege access, audit logs, secrets outside the repo.
- **Privacy by design and default (Art 25):** the most private settings are the default; nothing is public by default.
- **Accountability:** keep the record of processing (Art 30), DPIAs, processor contracts (Art 28) and the breach log up to date.
- **Data subject rights the software must support:** access/export (respond within 1 month), erasure (including at processors), rectification, portability (machine-readable), objection, restriction, marketing opt-out.
- **Breaches:** notify the ICO within 72 hours of becoming aware, unless there is no likely risk. Tell the people affected if the risk is high.
- **DPIA triggers** (ICO list): large-scale profiling, special category data, children, location tracking, new technology or AI, automated significant decisions, combining datasets, invisible processing, denying a service based on data. https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/accountability-and-governance/data-protection-impact-assessments-dpias/

## Marketing rules

- **Email, SMS and DMs need consent**, or the **soft opt-in**: an existing customer, similar products, an opt-out offered at collection, and an opt-out in every message.
  - UK B2B emails to corporate addresses are exempt. EU rules vary by country.
- **UK cookies** (ICO guidance finalised 29 Apr 2026):
  - Consent exceptions: communication, strictly necessary, statistical purposes, appearance, emergency assistance.
  - The statistics exception covers first-party, aggregate usage figures only. It needs clear information, an easy way to object, and no tracking of individuals.
  - Advertising and tracking still need consent.
  - Source: https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/guidance-on-the-use-of-storage-and-access-technologies/
- **Everywhere:**
  - Nothing non-essential runs before the user chooses.
  - Reject is as easy as Accept.
  - No pre-ticked boxes.
  - Consent is easy to withdraw.
- **Privacy and security claims** ("GDPR compliant", "end-to-end encrypted", "we never sell your data") must be true and backed by evidence.
- **Research:**
  - A public profile is still personal data.
  - Scraping is high risk.
  - Prefer aggregated or anonymised data, and do not profile individuals.

## Checklists by role

### Lead, at planning

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

### Reviewer, in code

1. No personal data, tokens or secrets in logs, URLs, query strings, analytics events or error reports.
2. TLS in transit; encryption at rest for sensitive data.
3. Authorisation is checked on every endpoint and object.
4. Retention and deletion jobs exist, are tested, and cover backups and caches.
5. Erasure also reaches processors.
6. New third-party SDKs and pixels are justified and only load after consent.
7. No secrets in the repo.
8. APIs return only the data the caller needs.
9. Test data is synthetic, never production personal data.
10. Cloud regions and transfers are deliberate choices.

### QA, in the real product

1. Before any choice is made, the network panel shows no non-essential cookies or requests.
2. Reject is as easy as Accept, and rejecting really blocks trackers.
3. Withdrawing consent works.
4. Data export is complete and machine-readable.
5. Account deletion removes the data, including after a new sign-in and from emails.
6. Corrections are saved and shown.
7. Unsubscribe works on the first click.
8. The privacy notice matches what the app collects and which vendors it uses.
9. A route for privacy requests and complaints exists.
10. Children's defaults are in place where relevant.

### Marketer

1. Every contact has recorded consent or a soft opt-in, with source and date.
2. Every message has an opt-out, and opt-outs are processed quickly.
3. Suppression lists are respected.
4. No bought lists without evidence of consent.
5. Pixels, tags and ad tools only run after consent.
6. Analytics fits the UK statistics exception or has consent (always consent for EU users).
7. Every privacy or security claim has evidence, checked by QA.
8. No scraping or profiling of individuals.
9. Research and survey participants get a privacy notice.
10. Large-scale targeting or lookalike audiences go to the PM for a DPIA decision.

## Always escalate to the PM

- Any breach or suspected breach, **immediately**, because the 72-hour clock starts on awareness.
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
- Anything that depends on the unconfirmed details below.

## Not verified

- The exact commencement of each DUAA section.
- Whether final ICO guidance exists on recognised legitimate interests and automated decisions.
- The status of the Digital Omnibus, including its Art 88b.
- The EU AI omnibus.

Check legislation.gov.uk and ico.org.uk before relying on any of these.
