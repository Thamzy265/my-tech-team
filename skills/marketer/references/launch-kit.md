# Launch kit

Checked: 2026-10-12. Check the current source when a rule decides an outcome.

Templates for launch, release and content drafts. Describe only what the QA evidence shows as PASS. Write in the brand voice from `docs/marketing/voice.md`.

## Draft layout (`docs/marketing/launches/<version>.md`)

```markdown
# <Product> <version> — launch draft

Status: DRAFT — not approved, not published. Date: <YYYY-MM-DD>
Evidence: docs/qa/<milestone>.md, <release notes or CHANGELOG path>

## Release notes
## Announcement
### Short
### Medium
### Long
## Claims
## Not included
- <feature> — <not in QA evidence | FAIL | NOT RUN> (docs/qa/<milestone>.md#<row>)
## Requested, not used
- "<claim>" — <why> — <evidence that would allow it>
## Privacy items for the PM
- <none | item — rule — what the PM must decide>
```

## 1. Release notes

```markdown
## <version> — <YYYY-MM-DD>

### New
- <what the user can now do, in user terms> (evidence: docs/qa/<milestone>.md#<row>)

### Improved
- <what works better for the user, and how you know>

### Fixed
- <what was broken, from the user's side, now fixed>

### Known issues
- <what still doesn't work, and the workaround if there is one>
```

- Write for users, not developers: "You can export an invoice as a PDF", not "Added `/invoices/{id}/pdf`".
- Leave out a heading that has no items, except "Known issues": write "None known." there.
- Copy known issues from FAIL and "Not observed" rows in the QA evidence. Don't hide them.

## 2. Announcement post

Each version has five parts, in this order:

1. **Hook:** one sentence on the user's problem or the outcome.
2. **What is new:** the shipped features, from the release notes.
3. **Who it is for.**
4. **How to try it:** install, update or sign-up step.
5. **Link:** release notes, download or docs.

| Version | Length | Use |
|---|---|---|
| Short | up to 280 characters, one link | social posts |
| Medium | 80–150 words | newsletters, community posts |
| Long | 300–600 words, with headings | blog post |

- No hashtag lists, no invented quotes or testimonials, no numbers without a source.
- Every factual sentence has a row in the claims table.

## 3. README or landing checklist

- [ ] One-line value statement: what it does and for whom.
- [ ] Who it is for (and, if useful, who it isn't for).
- [ ] Install.
- [ ] Quick start in 3 steps, each one a command or one action.
- [ ] A screenshot of the real, current product, with alt text.
- [ ] Support: where to ask for help or report a bug.
- [ ] Licence.

README text also follows ASD-STE100 (short sentences, one instruction per sentence, active voice).

## 4. Claims table

Put it under `## Claims` in every launch and content draft (research has none). One row per factual claim. QA fills the "QA verdict" column as `<verified|reword|remove> — docs/qa/<file>.md#claim-check` and keeps its full evidence in `docs/qa/`.

```markdown
| Claim | Source/evidence | QA verdict |
|---|---|---|
| "Export any invoice as a PDF" | docs/qa/M4.md#1 | |
| "Used by 40 accounting firms" | <none yet — need the customer list date and count> | |
| "Works on iOS and Android" | docs/qa/M4.md#6 (iOS only) | |
```

- A factual claim is anything a reader could check: features, platforms, speed, numbers, prices, integrations, privacy, security, comparisons, awards.
- Quote the claim exactly as written in the draft.
- Evidence is a QA evidence row, a design note, ADR or audit, or a public source URL with the date you checked it. "The PM said so" is not evidence.
- Privacy and security claims and superlatives ("best", "#1", "leading") need written evidence; QA will mark them `remove` without it. Leave them out unless you have it.
- After QA marks a row `reword` or `remove`, change the draft to match and keep the row with the new wording, before you report. Send the changed rows back to QA.
