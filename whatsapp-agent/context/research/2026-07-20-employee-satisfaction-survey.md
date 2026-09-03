# Employee satisfaction survey — pilot results, 12–20 Jul 2026

- Source: Drive `סקר שביעות רצון — דוח תוצאות.pdf`, auto-generated from the pilot dashboard on 2026-07-20 09:58. Read 2026-09-03. Respondent names and phone numbers are in the PDF; not reproduced here beyond the IKEA stakeholders who answered.
- Already cited in the PRD (photo→SKU as OQ-12). This note holds the full picture.

## Numbers

| | |
|---|---|
| Surveys sent | 104 (waves on 12, 15, 16, 19, 20 Jul) |
| Responses | 30 — **29% response rate** |
| "Do you enjoy the agent experience?" | **27 / 30 yes** |
| "Does it help you?" | **24 / 30 yes** |
| "Should it be rolled out to more employees?" | **28 / 30 yes** |

Three questions, yes/no only. Two respondents answered no to everything; two more said "helps: no" but "enjoy: yes / roll out: yes". Among the yes-voters: Avi Yoktan, Moni Greentuch, Michal Ben Haim — three of the February discovery stakeholders answered, all positive.

## Free-text feedback (12 comments)

- **Photo → SKU recognition is weak** — five separate people: "doesn't always identify a photo and match the right SKU"; "still a mismatch between what I photograph and what it shows"; "must improve image recognition"; "tried several times to find a SKU from a photo, wrong answers"; "doesn't always identify products from a photo".
- **"Still far from usable for a customer.** Would be nice for AI-native customers, but for minority sectors…" — Eitan Miller.
- **Useful as a staff tool:** "excellent for finding SKUs for products at the tills"; "will help a lot in service — for trainees and veteran reps alike"; "for an IKEA employee, faster than going into the site to find products".
- **Feature ask:** show a **replacement SKU for discontinued kitchen products** — "more useful for items that left the range".
- **Roll out wider / keep developing:** "great but needs more development"; "roll it out to more employees to run it in and improve"; "can be distributed to the trainees".

## Reading it

- **Strong as an employee tool, not yet a customer product** — the respondents said so themselves. That is the same split the 07-28 room landed on (employee release now, one-branch customer pilot as the December gate). Use this as external evidence for the staging, not as a launch endorsement.
- **Photo → SKU is the single named defect.** The March spec deliberately scoped image input as "ask the user to describe it" (F22). Production went further and now under-delivers. Three options are already in the PRD (OQ-12): fix to a bar, hold at a reduced bar, or disable for customers.
- **Response rate 29%** with yes/no questions and no CSAT scale — good enough for a pulse, not for a December data pack. The spec's own metric was CSAT ≥ 4/5 (F11); no instrument for it exists yet.
- **Discontinued-item replacement** is a cheap, employee-sourced win that ties to PIA range data (SPR/ART) and to Moni's grey-indicator rule.

## Action items

- [ ] Decide photo→SKU for the customer pilot: fix / hold / disable — with estimates for all three (Shai, with Niv) — tracks PRD OQ-12
- [ ] Replace the yes/no pulse with a 1–5 CSAT question so the December pack has the metric the spec promised (Shai)
- [ ] Scope "replacement SKU for discontinued items" as a small retainer or quick-win item (Niv / Tali)
- [ ] Send the 30-day follow-up survey to the 1,500-employee cohort as the PRD plans; reuse the 12–20 Jul run as the baseline (Shai)
