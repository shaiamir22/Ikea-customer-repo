# SOW + price quote — what was actually signed up to (Jan 2026)

- Source: Drive `IKEA Whatsapp Agent - SOW` (Google Doc, 2026-01-21) and `Ikea - הצעת מחיר` (Google Doc, quote dated 29.01.26, last edited 2026-04-16). Read 2026-09-03.
- Relationship-level because the commercial terms govern every IKEA workstream, not just the agent.
- Caveat: these are the Drive copies. Whether the signed version differs (dates filled in, any redlines) is not verifiable from here.

## Commercial terms (quote)

- **Fixed price: ₪109,546 + VAT** for the five-phase project. Phases: (a) infrastructure/architecture, (b) WhatsApp Cloud API integration, (c) AI agent core — LangGraph, model routing, Hebrew prompts, "9 dedicated tools", (d) analytics & self-learning, (e) testing, hardening, launch.
- **Support retainer: ₪10,000 + VAT per month** — described as "comprehensive support: model-cost monitoring, adopting new technologies into the client's systems, maintenance and upgrades etc." No definition of done, hours, or response times attached.
- **Out-of-scope clause, verbatim in spirit:** all scope is based on the pre-agreed assumptions; *any client request not included in the listed scope is priced separately as agreed between the parties.* This is the contractual hook for the scope reset — it already exists, it just hasn't been used.
- **Payment:** 50% advance on signature; invoices at the start of each phase, due within 7 days. Late payment beyond 7 days accrues interest (Bank Leumi overdraft rate + 5%) **and the company may suspend services until the debt is settled.** Relevant to ~5 months unpaid; a lever to hold, not to pull casually.
- **Termination:** either side, 30 days' written notice before end of half-year; final settlement for services rendered.
- **Ways of working promised:** a shared Monday board (opened on the client's account); a **weekly Thursday sprint-planning meeting** with the client's contacts; contacts named by the client with authority to reprioritise and change budget.
- **IP:** deliverables vest in the client after full payment; Moveo keeps background know-how; open-source and third-party components under their own licences. Moveo may name IKEA as a client in marketing and add "Created by Moveo".
- **Liability:** AS-IS, capped at 12 months' fees. Client is solely responsible for legal compliance (privacy law, consumer law, accessibility).
- Quote valid 15 days from 29.01.26.

## Technical scope (SOW, English)

- Goal: WhatsApp sales/support assistant for IKEA Israel — customers and employees, Hebrew + English, product discovery, stock by branch, technical details, self-serve aisle/bin, store hours and navigation links.
- **Data source: web scraping of ikea.com/il** — "no direct API access is available". (Superseded within weeks: PIA was connected by 2026-02-18; SORM stock feed came later via SFTP.)
- Architecture as scoped: Twilio WhatsApp → API Gateway → ingest Lambda → SQS FIFO → worker Lambda (LangGraph + **Claude**) → DynamoDB → Twilio. (Production ended up on Meta Cloud API and Gemini.)
- **Milestone 1 — internal demo, 20 business days:** Twilio sandbox, Hebrew multi-turn agent, scraping MVP, basic stock check, guardrails.
- **Milestone 2 — production launch, 28 business days:** dimensions/assembly PDFs, nearest-store + Waze, rich WhatsApp UI (lists/buttons), LangSmith observability.
- Cost strategies listed: response caching, model cascading (Haiku/4o-mini for routine, Sonnet for complex), context summarisation, 30-minute scrape cache, token budgeting.

## What this settles, and what it doesn't

- **Confirms the 2026-07-28 finding:** no SLA, latency, uptime, or concurrency figure anywhere in either document. The only time-bound commitments are delivery durations (48 business days total ≈ 10 weeks) and payment terms.
- **Contract value vs. cost to finish:** the whole fixed project was ₪109.5k. The ~₪140k (worse case ₪200k) still needed to finish exceeds the original contract value. That framing belongs in the post-mortem, not in front of IKEA.
- **The retainer was never defined** beyond one sentence. The 07-28 decision to write the retainer DoD is filling a gap the quote left open, not renegotiating something agreed.
- **Two promised rituals lapsed:** the Monday board ("not configured" in this repo) and the Thursday sprint meeting. The daily 08:30 sync replaced the latter informally.

## Action items

- [ ] Use the quote's "requests outside listed scope are priced separately" clause as the opening frame for the August commercial meeting — it is already agreed language, not a new ask (Shai)
- [ ] Confirm the signed copy matches this Drive version — dates, any redlines, whether the 50% advance and phase invoices were actually issued (Shai, via Elad/Eldar)
- [ ] Decide internally whether the late-payment / suspension clause is ever to be referenced with IKEA, or held in reserve (David, Elad Kobi)
