# Strategy doc (12 Jul) and "M.ai × IKEA" status + roadmap deck (13 Jul 2026)

- Sources: Drive `אסטרטגיה-סוכן-חכם-איקאה.docx` (2026-07-12) and `מצגת-סוכן-איקאה-סטטוס-ומפת-דרכים-preview.pdf` (2026-07-13, 15 slides, Hebrew; text recovered from a reversed-RTL extract). Read 2026-09-03.
- Prepared a week before the handover, evidently for a client meeting. Repeated in the PRD's "system today" numbers, so the figures below are the ones already in circulation.

## System today — the numbers the deck put in front of IKEA

| Figure | Value |
|---|---|
| Products in the live catalogue | **25,480** (single items and complex systems) |
| Dedicated tools in the agent | **24** |
| Stock records, refreshing | **122K** across **5 branches**, updated every ~10 minutes |
| Average cost per conversation | **$0.03** |
| Queries answered on the fast path (no LLM call) | **~30%** |
| Average response time | **9.3 s** |
| Automatic QA checks per answer | **~25** (prices, SKUs, phone numbers, Hebrew) |
| Model | Gemini 3.5 |

Also claimed: nightly FAQ learning from repeated questions (human-approved, then answered instantly at no cost); automatic failover to a backup channel when the main AI provider drops; no message lost or handled twice; full conversation logging and a daily ops dashboard.

Capabilities slide: in-store navigation between departments in all five branches; real-time stock with aisle/shelf; smart cart kept 30 days with complementary suggestions; budget and room planning; modular-system planner handoff (pick up the planning code in chat, cart and pickup list from it); comparison of up to 3 products; customer-service FAQ from IKEA's own service data; smart search (free text, voice, photos, typo/slang tolerant); PII blocking and human handoff "when needed"; smart pickup list; feedback and CSAT surveys with automatic frustration detection; **WhatsApp Flow** forms; assembly PDF on demand.

## Near-term goals stated

1. **Cut cost by 10%** — context sent per turn is the main cost; better caching, wider free paths, context compression.
2. **Improve latency** (response times).
3. **Load readiness** — structured load tests *before* traffic grows; target "thousands of concurrent conversations" without latency damage; confirm model quotas aren't the bottleneck.
4. **Evaluate alternative models** — open-source/local for fixed cost and control, or a closed model with more generous quotas; structured quality comparison before any switch.

## Roadmap (strategy doc + deck), impact vs. effort

**Priority 1 — direct business value / data foundation**
- **Receipts, invoices and purchase history integration.** Answers post-purchase questions (history, invoice status, credits, cancellations, delivery-address changes) and takes load off the service centre. Very high impact, high effort: PII means a hardened security architecture; likely a multi-agent split with data-authority separation; integration with IKEA's support/ops systems. Presented with the caveat that IKEA's stated focus is the in-store sales experience.
- **Push notifications.** One-off campaigns (sale, new collection, holidays), agent-offered follow-ups (back-in-stock, price drop, open-cart reminder), personalised recommendations via Google Analytics × conversation analysis. High impact, low–medium effort: Meta approved templates + CRM connection + a frequency policy. **Framed as the "natural first follow-on project".**

**Priority 2 — customer experience**
- **Product simulation in the customer's room** — static image, no AR; medium–high impact, high effort; needs a POC.
- **Smart assembly assistant** (sequence-to-text over the official booklets, no live video) — medium–high impact, medium effort; needs a survey of how many customers actually get stuck.

**For strategic discussion, with caveats** (they collide with IKEA's bring-them-to-the-store model)
- Live in-store navigation (beacons / visual SLAM) — very high effort, medium impact since the store path is one-way and aisle/bin already exists.
- Virtual store tour from home (3D scans) — medium–high effort; "the world is going there".
- Full payment inside WhatsApp — very high effort (PCI, POS); unlikely to pass IKEA.

Strategy doc's opening instruction: *find out what IKEA actually cares about and where they see the future, including logistics, operations and internal store ops.*

## Closing slide — the ask that was never landed

- **Main goal: an agreed go-live date for the current project**, with **closed scope and predefined success metrics**, committed by both sides.
- Close the interim targets first: cost, response times, load.
- Jointly prioritise the roadmap and pick the first follow-on project.
- Named risks: IKEA's final approval of launch scope and customer messaging; data/system availability (CRM, analytics) for follow-ons; **defining success metrics and the approval process so no blockers appear mid-way.**

## Why it matters

- The July deck asked IKEA for exactly what the 07-28 room later said we lack: a go-live date, closed scope, success metrics. The ask was made; it was not closed. The August meeting is the second attempt and should say so.
- "$0.03 per conversation" and "9.3 s" are the client-facing baseline. Any later number (the retainer deck's $0.01, or a latency claim) will be compared to these.
- The roadmap is a Moveo wish-list ranked by us. The strategy doc itself says to first ask IKEA what they want. The IKEA-sourced asks (#29 receipts, #31 handoff) happen to match Priority 1 — lead with those.
