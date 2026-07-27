# Project Status — WhatsApp Shopping Agent

_This file is the PM's single source of truth for what's happening right now. `brief` reads it at the start of every session. Use `refresh-status` to keep it in sync with recent context._

_Last updated: 2026-07-27_

---

## Phase

**Now:** Build / pre-launch — stabilizing ahead of the ~1,000-employee pilot.
**Next:** Employee pilot live and stable — ~1,000 IKEA employees using the agent daily with 24/7 support, generating real usage data.
**Gate:** A stable agent (no crashes during Gemini outages) plus a cost trajectory IKEA can sustain. Hai's guidance: finish the project to the SLA / concurrent-session level committed in the current agreement scope first, then propose cost and latency improvements based on feedback from a substantial user sample.

---

## To advance

**Critical (gates the employee pilot)**
- Fallback model routing so the agent survives Gemini API outages — the agent crashed repeatedly on 2026-07-21 and halted Efrat's testing. (Niv / Arnon's team)
- Confirm the Gemini crash root cause and share findings with Shai, Efrat, Avi.
- Bandwidth: agent must handle ~100 concurrent messages.
- Latency — repeated as the top quality complaint. ~8s average with spikes to 25s; one known cause was a bug issuing 5 model calls per message.
- Team redundancy: Niv is the sole developer and a single point of failure. Confirm Tali's role or add a senior dev. (Shai)

**Not critical right now**
- Benjamin's LLM-sandwich PoC (~87% cheaper per message, any-language support, vendor-agnostic via OpenRouter, +4-7s latency). Fully built and behind an off-by-default switch, 2,474 tests passing on `origin/staging-llm-sandwich-py312`. Per Hai, hold for the next stage rather than shipping into the pilot — but two business decisions are pending regardless: (1) data-protection sign-off to send real customer messages to an external AI provider, (2) whether +4-7s latency is acceptable for the ~87% saving. Hebrew-language testing is the remaining validation gap.
- Search-quality improvements for semantically complex queries (e.g. "ארונית קלה" should match "כוורת").
- Delivery/assembly status integration — top strategic feature, automates a high-volume service query and reduces call center load. Test the tracking link and report to Avi.
- Fraud detection — base is ready; needs a coordinated conversation with IKEA's CISO before the project can start. Potential separate paid workstream.
- Phase 3 vision: link agent interactions to in-store purchases for full customer-journey data; restaurant food menus, allergy info, mobile ordering.

---

## What's next

_Concrete calendar-able actions. 3-5 max. Not goals, not outcomes._

1. Prepare the roadmap proposal for the next planning meeting — big-picture strategic goals, quick wins (delivery status), and data collection strategy.
2. Schedule the planning session with Avi and Efrat (post-sale).
3. Set up a standing Wednesday brief — agree format and cadence with the team.
4. Decide with Arnon/David which improvements are retainer scope vs. a paid follow-up to pitch IKEA.
5. Arrange the Netanya branch visit (3+ hours, on-site).

---

## What's open

_Full register of open questions and risks. Each item tagged with owner and phase._

| # | Item | Owner | Phase |
|---|---|---|---|
| OQ-1 | Is +4-7s latency acceptable in exchange for the ~87% per-message cost saving? | Client | 2 |
| OQ-2 | Data-protection sign-off to send real customer messages to an external AI provider (OpenRouter) | Client | 2 |
| OQ-3 | Which improvements fall under the existing retainer vs. a new paid scope? | Us | 1 |
| OQ-4 | Does Tali become real engineering redundancy for Niv, or step back? | Us | 1 |
| OQ-5 | Can the fraud-detection workstream start? Needs a coordinated conversation with IKEA's CISO. | Client | 3 |
| OQ-6 | What is the committed SLA / concurrent-session level in the current agreement scope? | Us | 1 |
| R1 | Niv is the sole developer — illness or departure stalls the project outright. | Us | 1 |
| R2 | Cost at ~₪0.10/message projects to ~₪50k/mo against a ~₪2k/mo target; unresolved, this makes the product unsellable at scale. | Us | 1 |
| R3 | Gemini API instability crashes the agent; no fallback model in production yet. | Us | 1 |
| R4 | A shaky pilot creates negative internal perception at IKEA ahead of the December CEO review, which gates the public launch and investment from the American owners. | Us | 1 |
| R5 | Hebrew-language testing is not yet done on the PoC — Hebrew is the primary customer language. | Us | 2 |

---

## Stakeholders

| Name | Role | Company | Last contact | Status |
|---|---|---|---|---|
| Shuki | Tech lead | IKEA | 2026-07-22 | Active |
| Avi | Employee onboarding | IKEA | 2026-07-22 | Active |
| Efrat | Employee tester | IKEA | 2026-07-22 | Active — blocked by crashes |
| Arnon Meltser | Prior account lead | Moveo | 2026-07-27 | Active |
| Niv | Developer | Moveo | 2026-07-22 | Active |
| Tali | Product | Moveo | 2026-07-21 | Role under review |
| Benjamin | Engineer (PoC) | Moveo | 2026-07-27 | Handed over PoC |
| Hai Morgenstern | Leadership | Moveo | 2026-07-27 | Active |

---

## Monday item

not configured

_Verify this reflects the current stage before any C-level or PM sync._

---

## Recent decisions

_Decisions made in the last 30 days that are not yet obvious from the spec._

- 2026-07-27: Per Hai — finalize the project to the committed SLA / concurrent-session scope first; propose cost and latency improvements at the next stage, based on feedback from a substantial user sample rather than shipping them into the pilot.
- 2026-07-22: Delivery/assembly status integration named the top strategic feature priority. Agent scope stays on shopping assistance, not design tools.
- 2026-07-22: Employee pilot (~1,000 users) set for ~Aug 1 with an AI-error disclaimer and 24/7 support for the first 1-2 months; CEO reviews performance in December to decide on a public launch.
- 2026-07-21: Shai took over the account from Arnon as client-facing lead.
