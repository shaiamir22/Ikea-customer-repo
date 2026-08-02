# WhatsApp Shopping Agent — Open action items

Running list of action items for this project. Cross-project / relationship-level items live in the customer root's `context/open-action-items.md`. All items are owned by the PM unless noted; if a follow-up depends on someone else, note it inline.

## IKEA (client)

- [ ] Begin onboarding 1,500 employees to the agent on Sun 2026-08-02 (moved from Thu 30/7) (Avi & Efrat).
- [ ] Data-protection sign-off before real customer messages can be sent to an external AI provider.
- [ ] Decide whether +4-7s latency is acceptable in exchange for the ~87% per-message cost saving.
- [ ] Coordinate a conversation with the CISO before the fraud-detection workstream can start.
- [ ] Schedule the Netanya branch visit (3+ hours on-site).
- [ ] **Provide Meta's Israel utility/authentication per-message rate from the WABA invoice** — the dominant cost variable once service replies become billable on 2026-10-01. IKEA already holds this; escalate via David (OQ-12).

## Internal / Moveo

- [ ] Investigate the Gemini crash root cause; share findings with Shai, Efrat, Avi (Arnon's team).
- [ ] Implement a fallback LLM for Gemini outages (Arnon's team).
- [ ] Add the CEO to the agent's user list for a passive review (Arnon's team).
- [ ] Increase bandwidth to handle ~100 concurrent messages.
- [ ] Improve search quality for semantically complex queries (e.g. "ארונית קלה" → "כוורת").
- [ ] Keep driving latency down — the recurring top quality complaint.
- [ ] Test the delivery/assembly tracking link and report to Avi.
- [ ] Prepare the roadmap proposal: strategic goals, quick wins (delivery status), data collection strategy (Shai).
- [ ] Schedule the planning session with Avi and Efrat, post-sale (Shai).
- [ ] Set up a standing Wednesday brief — agree format and cadence with the team (Shai).
- [ ] Add Hebrew-language tests to Benjamin's PoC before it can be fully validated.
- [ ] Decide which improvements are retainer scope vs. a paid follow-up to pitch IKEA (Shai, with Arnon/David).
- [ ] Deliver the work plan for the Sunday 2026-08-02 review: what reaches definition of done, what it takes to hit the monthly cost target, what it takes to be crash-free at target load, and headcount plus timeline. Spreadsheet/Gantt of technical tasks broken to dev-days with estimates, sequencing, dependencies, and a one-or-two-developer recommendation (Shai — product; Tali & Niv — technical).
- [ ] Sit with Arnon to extract technical context before he goes on leave — the plan has to close before he leaves (Tali & Niv).
- [ ] Set up a standing Sunday one-hour rundown with Arnon: what gets done that week, technically, and by whom (Shai).
- [ ] Agree a single monthly cost target — ₪3-5k, ₪5-8k, and ~₪8k are all currently in play against a ~₪50k/mo projection (Shai, with Hai/David).
- [ ] Define the product-side latency target and the reasoning behind it; current average is 8-9s (Shai).
- [ ] Write the named on-call rota for the 1,500-employee release, including that normal working hours don't apply on release day (Shai, with Arnon).
- [ ] Set and communicate the two-tier release response policy — fast acknowledgement, fix within hours (Shai).
- [ ] Locate the eval set and confirm whether the lighter routed model passes quality checks (Niv / Arnon's team).
- [ ] Define concurrency by heuristic — messages per conversation, users per day, concurrent sessions — stating assumptions rather than waiting for exact numbers (Tali & Niv).
- [ ] Flag new client requests as out of scope when they arrive and price them, rather than letting them land in the retainer by default (Shai).
- [ ] Confirm which Gemini model the agent runs today and its token mix — blocks converting the price ladder into a per-message delta (Niv, OQ-13).
- [ ] Measure actual messages/user/day and the peak-hour curve from the live 1,500-employee release; replace the unmeasured ~80 msgs/user/day assumption under every volume tier (OQ-14).
- [ ] Add the Meta service-fee layer to the three-tier cost model — it is the larger of the two layers from 2026-10-01, and the model is now externally deadlined rather than internally scheduled (Tali & Niv).
- [ ] Scope reply-count consolidation and WhatsApp Flows as a cost lever — from 2026-10-01 the fee is per business-sent message, so message count matters more than token count. Cheap relative to a re-architecture.
- [ ] Re-open the decision on Benjamin's vendor-agnostic PoC against the Gemini retirement and price-rise evidence (Shai, with Hai/Arnon — OQ-11).
- [ ] Confirm with the BSP that Meta Business Agent token pricing (~$2/1M tokens, live since 2026-08-01) does not apply to a self-hosted Cloud API agent.
- [ ] Verify the Israel rate card and the Gemini price ladder against vendor primary sources before either reaches a slide — this session's egress policy blocked direct page fetches, so both are search-corroborated only (Shai).

_Source: ../context/meetings/2026-07-22-ikea-status-sync.md, context/meetings/2026-07-27-arnon-roadmap-conversation.md, context/comms/2026-07-27-benjamin-poc-handover.md, context/meetings/2026-07-28-internal-ikea-sync.md_
