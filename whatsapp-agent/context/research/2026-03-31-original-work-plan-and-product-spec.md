# Original work plan (Feb 2026) and internal product spec (Mar 2026)

- Sources: Drive `תוכנית עבודה_ IKEA Smart Agent` (docx, Elad Kobi, 2026-02-03) and `IKEA_Agent_Product_Spec_EN` (docx, "Internal Document | March 2026 | Engineering Spec"). Read 2026-09-03.
- Why it matters now: these two documents are the closest thing to a promised bar that exists. The SOW and quote have no numbers; these do. They were written before the handover and are not referenced anywhere in this repo until now.

## The 10-week work plan (3 Feb → 13 Apr 2026)

Authored by Elad Kobi (signature block on the doc). Weekly structure:

- **Week 1 — foundations & API integrations.** Kickoff with success metrics; API access to stock, stores, products, orders; IKEA supplies a business WhatsApp number; KPI/cost dashboard; baseline error-rate and response-time measurement; load-bottleneck check "for thousands of users a day"; cost-tracking logs; PIA/catalogue integration; caching layer.
- **Week 2 — agent persona, self-service, analytics.** Data validation against core systems; brand-aligned persona; stock and exact location per store (aisle/bin); pickup-point directions; automated daily usage report; analytics dashboard; model-cost comparison tool; E2E tests.
- **Weeks 3–4** vision (photo → product). **Weeks 5–6** internal launch to IKEA employees. **Weeks 7–8** voice-to-text. **Weeks 9–10** scale to "tens of thousands of concurrent users", 10% gradual launch, then full launch.
- Detail for weeks 3–10 was to be delivered "after week 1 milestones complete". It never was, as far as the folder shows.

**Reading it against reality:** the plan had a full public launch by mid-April 2026. The employee release happened 2026-08-02 — the ~4-month slip the post-mortem is about. Week 1 alone assumed IKEA API access that was still being negotiated in June (e-commerce API declined) and a SORM stock feed that only arrived as an SFTP drop. Week 9–10's "tens of thousands concurrent" was written down without a load test ever being planned.

## The internal product spec — 23 features with metrics

Twenty-three features, each with description, value, success metrics, example. Feature list matches the client-facing April kickoff pack one-to-one. What the kickoff pack dropped were the **numbers**:

| Bar type | Spec figure | Where |
|---|---|---|
| Latency | **≤3 s** search, product details, stock, images; **≤2 s** navigation, service info, packaging, assembly; ≤4 s comparison; ≤5 s voice | F1, F3, F6, F9, F10, F13–F19 |
| Availability | **99.5% monthly uptime**; stock API 99.5% | F9, F19 |
| Search quality | Precision@3 ≥ 80%; ≥40% of searches lead to a product tap; ≤3 narrowing questions | F1, F2 |
| Data quality | 100% of products with price/description/image; <3% missing-data errors; stock lag ≤15 min; bin location for 100% of in-stock items, refreshed within 24 h | F3, F18, F19 |
| CSAT | ≥4/5 in an end-of-conversation survey | F11, F23 |
| Privacy | zero PII stored between conversations; logs deleted after 90 days | F12 |
| Dashboard | refreshed every 24 h, 100% of conversations logged (no PII), 99% uptime | F8 |

Other decisions embedded in the spec worth knowing:
- **Image input (F22) deliberately does not identify products** — the bot asks the user to describe what they see. Production later added photo-to-SKU anyway; it is now the top employee complaint (see the survey note).
- Five branches named: Netanya, Rishon LeZion, Kiryat Ata, Beer Sheva, Eshta'ol.
- Multilingual (F23): Hebrew, Arabic, French "in the first phase".
- Back-in-stock notification (F20), checkout guidance with instalment reminder over ₪1,000 (F21).

## Why this changes the "no bar exists" line

- Internally, a bar **did** exist: 3-second latency and 99.5% uptime, written in March. Production runs ~9.3 s average. The retainer deck (29 Jul) quietly reset the latency bar to p50 ≤ 9 s / p95 ≤ 15 s — a 3× relaxation of our own spec, never acknowledged as such.
- The spec is labelled internal, and the client-facing kickoff pack carries the features without the metrics. So the 07-28 statement "nothing is committed to IKEA in writing" still holds **unless this spec was shared**. That is the one fact to confirm before repeating the line in the August meeting.
- Either way, the spec is the natural seed for OQ-7 (the SLA we author ourselves): start from these numbers, decide which to keep, which to relax openly, and say why.

## Action items

- [ ] Confirm with Arnon/Tali whether `IKEA_Agent_Product_Spec_EN` was ever sent to IKEA — this decides whether "no bar was committed" is safe to say (Shai)
- [ ] Use the spec's metric table as the starting point for the authored SLA (OQ-7); mark each figure keep / relax / drop with a reason (Shai, with Tali & Niv)
- [ ] Feed the 10-week plan into the post-mortem as the baseline the slip is measured against (Shai)
