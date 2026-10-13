# Marketing privacy (UK + EU)

Checked: 2026-10-12. Check the current source when a rule decides an outcome.

**Not legal advice.** These are practical rules a marketer can check. Whether something is lawful, which lawful basis applies, and any public privacy or compliance claim go to the PM through the lead.

Scope: UK GDPR, DPA 2018 as amended by the Data (Use and Access) Act 2025, PECR; EU GDPR and the ePrivacy Directive. A project's Team setup can add other regions.

## Marketer checklist

Work through every item. Write `n/a — <reason>` for items that don't apply.

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

You check and flag; you don't build. Adding a pixel, tag, script, form or analytics tool is a product change: send it to the lead as a privacy item for the PM.

## Cookies and tracking: UK vs EU

- **UK** (ICO guidance on storage and access technologies, finalised 29 Apr 2026):
  - No consent needed for: communication, strictly necessary, statistical purposes, appearance, emergency assistance.
  - The **statistics exception** covers first-party, aggregate usage figures only. It needs clear information, an easy way to object, and no tracking of individuals.
  - Advertising, retargeting and cross-site tracking still need consent.
- **EU:** consent for every non-essential cookie or similar technology, analytics included. No statistics exception.
- **Both:**
  - Nothing non-essential runs before the user chooses.
  - Reject is as easy as Accept.
  - No pre-ticked boxes.
  - Consent is easy to withdraw.
- An ad or retargeting pixel (for example a LinkedIn Insight Tag or a TikTok pixel) is never covered by an exception. It needs prior consent in the UK and the EU, and the PM decides whether to use it at all.
- Source: https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/guidance-on-the-use-of-storage-and-access-technologies/

## Email, SMS and DMs: consent or soft opt-in

Marketing messages need consent, or the **soft opt-in**. The soft opt-in applies only if **all** of these hold:

1. You got the contact details from a customer, during a sale or negotiation for a sale.
2. The message is about your own similar products or services.
3. The person was given a simple way to opt out when you collected the details.
4. Every message has a simple way to opt out.

- UK B2B emails to corporate addresses are exempt from the consent rule (the opt-out still applies). Sole traders and some partnerships count as individuals. EU rules vary by country.
- Record the basis, source and date for each contact. No record means no message.

## Research

- A public profile is still personal data.
- Scraping is high risk. Don't do it; send any request to scrape to the PM through the lead.
- Prefer aggregated or anonymised data. Don't profile individuals.

## Always escalate to the PM (through the lead)

- Any breach or suspected breach, **immediately**, because the 72-hour clock starts on awareness.
- Processing that triggers a DPIA or is high risk (including large-scale targeting or lookalike audiences).
- Special category, children's, criminal-offence or biometric data.
- AI or automated decisions with significant effects.
- Choosing a lawful basis, especially (recognised) legitimate interests.
- New international transfers, new processors or new contracts (including new ad, email or analytics vendors).
- Access requests, erasure disputes and complaints.
- Any contact with a regulator.
- Public privacy or security claims.
- Scraping.
- Selling or sharing data.
- Anything that depends on rules not yet confirmed (the exact commencement of each DUAA section, the EU Digital Omnibus).

Check legislation.gov.uk and ico.org.uk before relying on any rule that decides an outcome.
