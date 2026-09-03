# Project Status — WhatsApp Shopping Agent

_This file is the PM's single source of truth for what's happening right now. `brief` reads it at the start of every session. Use `refresh-status` to keep it in sync with recent context._

_Last updated: 2026-09-03 (Drive archive ingested; execution state still as of 2026-07-28 — run `refresh-status` after the August catch-up)_

---

## Phase

**Now:** Build / pre-launch — stabilizing ahead of the 1,500-employee release on Sun 2026-08-02, and producing a costed work plan for review the same day.
**Next:** Employee release live and stable — 1,500 IKEA employees using the agent daily with a named on-call rota, generating the usage data that feeds the December decision.
**Gate:** An approved work plan (Sun 2026-08-02) that says what "done" is, what it costs to hit the monthly cost target, what it costs to be crash-free at target load, and who is needed. December is a **decision gate, not a launch**: the goal is one branch live with real customers plus data, not national coverage. Note the earlier framing — "finish to the SLA committed in the agreement scope" — turned out to be unactionable: no SLA, latency, or concurrency figure exists in the SOW or quote, so the bar has to be authored before it can be met.

---

## To advance

**Critical (gates the employee pilot)**
- Cost per message. At the loads we committed to support this projects to ~₪50k/month, which makes the product unsellable. Three targets are in play and none is settled: ₪3-5k/mo (what the client is said to be willing to pay), ₪5-8k/mo (Shai's working range), ~₪8k/mo (what the January presentation promised). Resolve to one figure before costing the plan.
- The Sunday 2026-08-02 work plan — product content from Shai, technical breakdown from Tali and Niv with Arnon. Must close before Arnon goes on leave; he holds most of the technical context.
- Fallback model routing so the agent survives Gemini API outages — the agent crashed repeatedly on 2026-07-21 and halted Efrat's testing. (Niv / Arnon's team)
- Confirm the Gemini crash root cause and share findings with Shai, Efrat, Avi.
- Named on-call rota for the 1,500-employee release, in writing, plus a two-tier response policy: acknowledge fast, fix within hours. Normal working hours don't apply on release day.
- Bandwidth: define the loads we actually stand behind. Target is 20,000 *daily* users; the concurrent number is unknown and to be derived by heuristic rather than waited for.

**Not critical right now**
- Latency. 8-9s average today, and the room's read on 2026-07-28 is that this is near the floor of the current implementation — going materially lower means a rewrite (three months minimum). Do not fund it as its own line item; it improves as a by-product of the cost work. A product-side target number is still owed.
- Benjamin's LLM-sandwich PoC (~87% cheaper per message, any-language support, vendor-agnostic via OpenRouter, +4-7s latency). Fully built and behind an off-by-default switch, 2,474 tests passing on `origin/staging-llm-sandwich-py312`. Confirmed on 2026-07-28 as **out of base scope** — a follow-on programme, not part of finishing the current product. Whether he is needed, and for how long, should fall out of the Sunday work plan. Two business decisions pend regardless: (1) data-protection sign-off to send real customer messages to an external AI provider, (2) whether +4-7s latency is acceptable for the ~87% saving. Hebrew-language testing is the remaining validation gap.
- Search-quality improvements for semantically complex queries (e.g. "ארונית קלה" should match "כוורת"). Explicitly **excluded from the December single-branch scope** as of 2026-07-28 — improve incrementally rather than letting it gate the release.
- Delivery/assembly status integration — top strategic feature, automates a high-volume service query and reduces call center load. Test the tracking link and report to Avi.
- Fraud detection — base is ready; needs a coordinated conversation with IKEA's CISO before the project can start. Potential separate paid workstream.
- Phase 3 vision: link agent interactions to in-store purchases for full customer-journey data; restaurant food menus, allergy info, mobile ordering.

---

## What's next

_Concrete calendar-able actions. 3-5 max. Not goals, not outcomes._

1. Deliver the work plan for the Sunday 2026-08-02 review — DoD, cost target, crash-free-at-load, headcount and timeline, as a task breakdown with dev-day estimates.
2. Write and circulate the named on-call rota for the 1,500-employee release on Sun 2026-08-02.
3. Book the standing Sunday one-hour rundown with Arnon — weekly technical plan and owners.
4. Book the commercial meeting with IKEA for the second half of August (scope and price).
5. Arrange the Netanya branch visit (3+ hours, on-site).

---

## What's open

_Full register of open questions and risks. Each item tagged with owner and phase._

| # | Item | Owner | Phase |
|---|---|---|---|
| OQ-1 | Is +4-7s latency acceptable in exchange for the ~87% per-message cost saving? | Client | 2 |
| OQ-2 | Data-protection sign-off to send real customer messages to an external AI provider (OpenRouter) | Client | 2 |
| OQ-3 | Which improvements fall under the existing retainer vs. a new paid scope? | Us | 1 |
| OQ-4 | ~~Does Tali become real engineering redundancy for Niv, or step back?~~ **Answered 2026-07-28:** Tali is staying and taking technical tasks at Arnon's direction. Open remainder is how fast the ramp turns into real cover — a scheduling question, tracked under R1. | Us | 1 |
| OQ-5 | Can the fraud-detection workstream start? Needs a coordinated conversation with IKEA's CISO. | Client | 3 |
| OQ-6 | ~~What is the committed SLA / concurrent-session level in the current agreement scope?~~ **Answered 2026-07-28: nothing is committed in writing** — no SLA, latency, or concurrency figure appears in the SOW or the quote. Superseded by OQ-7. | Us | 1 |
| OQ-7 | What SLA do *we* commit to, given none exists in the agreement? Needs a latency target, a concurrency figure, and a quality bar with a pass mark — authored by us before IKEA authors it for us in December. | Us | 1 |
| OQ-8 | Which single monthly cost target do we hold ourselves to? ₪3-5k, ₪5-8k, and ~₪8k are all currently in play against a ~₪50k/mo projection. | Us | 1 |
| OQ-9 | What is the real concurrency ceiling? No load test has ever run, and there is currently no capacity on the team to run one. | Us | 1 |
| OQ-11 | Does Benjamin's vendor-agnostic PoC get re-opened? Parked 2026-07-28 as out of base scope; on the 08-02 evidence it is the hedge against both the Gemini 2.5 retirement and the successor tier's 2-10× price rise. The ~85% reduction national needs and the ~87% the PoC delivers are the same number. | Us (Hai/Arnon) | 1 |
| OQ-12 | What is Meta's Israel utility/authentication per-message rate? The dominant cost variable from 2026-10-01 and the input that turns the sensitivity grid into one number. **IKEA already holds this** on their WABA invoice — needs escalating, not researching. | Client | 1 |
| OQ-13 | Which Gemini model does the agent run today, and what is its token mix? Not recorded anywhere in the repo; without it the price ladder cannot be turned into a per-message delta. | Us (Niv) | 1 |
| OQ-14 | What is the measured messages-per-user-per-day and peak-hour curve? Every volume tier assumes ~80 msgs/user/day, which is unmeasured and high. The 1,500-employee release went live 2026-08-02 — two weeks of traffic replaces the assumption. | Us | 1 |
| OQ-15 | Was any of the pre-handover paper formally given to IKEA — the March spec (≤3 s latency, 99.5% uptime), the April kickoff pack (24 h critical-fix SLA, 7-day feature assessment), the 3 Jun DoD deck? If yes, "nothing is committed in writing" is wrong in the direction that hurts us. Sources in `context/research/2026-03-31-original-work-plan-and-product-spec.md` and `context/comms/2026-04-15-kickoff-pack-and-progress-decks.md`. | Us (Arnon/Tali) | 1 |
| OQ-16 | Where is the approved customer-journey list? The 3 Jun deck told IKEA the project ends with an agreed list of journeys plus a critical-error DoD. The list was never produced. It is the shortest route to a DoD IKEA has already seen the frame for. | Us | 1 |
| OQ-17 | Do we state the latency bar change? Our own March spec said ≤3 s and the Feb client email said 1–2 s; the 29 Jul retainer deck commits p50 ≤ 9 s / p95 ≤ 15 s. Right call, but a 3× relaxation of our own number that no document acknowledges. | Us | 1 |
| OQ-18 | Did the retainer deck's Aug W1–W4 backlog close (alarms to IaC, failover fault-injection + 07-21 RCA, on-call rota, SFTP→S3 cutover, latency alarm, three-tier cost model)? Not recorded here. | Us (Niv/Tali) | 1 |
| OQ-10 | How is the ~₪140k (worse case ~₪200k) cost of finishing this fixed-price project funded? Intent is new paid scope sold in August, not an overrun invoice. | Us | 1 |
| R1 | Niv is the sole developer today. Tali is staying and ramping onto technical work, which is the redundancy answer, but it is a ramp not a switch. Compounded by leave: Tali out two weeks from 2026-08-02, Niv out in September, Arnon out shortly — the plan must close before Arnon leaves, since he holds most of the technical context. | Us | 1 |
| R2 | Cost at **~0.1 agorot (₪0.001)/message** projects to ~₪48-50k/mo **at national volume** against a ~₪2k/mo target; unresolved, this makes the product unsellable at national scale. _Corrected 2026-08-02: previously written as "₪0.10/message", a 100× unit slip — ₪0.10 × 48M msgs would be ₪4.8M/mo. Source figure is Arnon's "~0.1 agorot per message" (2026-07-27); the PRD volume table was already correct. Note per O1 that pilot volumes sit inside target on this layer._ | Us | 1 |
| R6 | **Meta stops charging nothing for service replies on 2026-10-01.** Every business-sent reply inside the 24h window becomes billable at Israel's utility rate, no volume discount — the agent is almost entirely this message class. On plausible assumptions the Meta fee is 10-25× the entire LLM bill at pilot volume, and it bills to IKEA's WABA, not ours. Unmodelled in every deck; lands seven weeks before the December pilot. | Us | 1 |
| R7 | **Gemini 2.5 family reaches earliest retirement 2026-10-16**, and the successor tier costs 2-10× more per token (3.5 Flash is 10× input / 7.2× output vs 2.5 Flash). The "token deflation" assumption underpinning the cost plan is false for our migration path. Date is soft (Google promises 6 months' notice at Gemini 3 GA); price direction is not. | Us | 1 |
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
| Tali | Product, ramping onto technical | Moveo | 2026-07-27 | Active — staying, taking technical tasks; out two weeks from 2026-08-02 |
| Benjamin | Engineer (PoC) | Moveo | 2026-07-27 | Handed over PoC |
| Hai Morgenstern | Leadership | Moveo | 2026-07-27 | Active |
| Avi Bar | VP Range | IKEA | 2026-02-17 (discovery) | Dormant since discovery — owns PIA/SORM knowledge; concern about the agent shortcutting the store path is unresolved |
| Michal | VP Marketing | IKEA | 2026-06-16 | Active in June (cart-visualisation ask); tone & style owner |
| Moni Greentuch | Range / website | IKEA | 2026-02-26 | Author of the stock-indicator rules; survey respondent |

---

## Monday item

not configured

_Verify this reflects the current stage before any C-level or PM sync._

---

## Recent decisions

_Decisions made in the last 30 days that are not yet obvious from the spec._

- 2026-09-03 (recorded, not new): the Drive archive shows three pre-handover decisions this file did not know about — (a) the Feb 2026 plan targeted **full public launch by 13 Apr 2026**, the baseline for the ~4-month slip; (b) the March spec set **≤3 s latency and 99.5% uptime** internally, and the 29 Jul retainer deck reset latency to p50 ≤ 9 s without acknowledging the change; (c) on 3 Jun IKEA was shown a DoD frame of **approved customer journeys + critical-error taxonomy**, and the June marketing asks (#29 receipts, #30 cart visualisation, #31 handoff context) were all parked. The e-commerce API was **declined once in June**. Details in `context/` (files dated 2026-02-17 through 2026-07-29).
- 2026-07-28: December is a **decision gate, not a launch date**. The target is one branch (Netanya) live with real customers plus data, so the December review decides national rollout. Scope deliberately narrowed to be achievable with the team we have.
- 2026-07-28: **No SLA is committed in writing** — none appears in the SOW or the quote. We author the bar ourselves rather than let IKEA define it in December. This supersedes the 07-27 guidance below, which assumed a committed level existed.
- 2026-07-28: **Latency deprioritised as a standalone workstream.** At 8-9s it is near the floor of the current implementation; it improves as a by-product of the cost work, and going materially lower means a rewrite.
- 2026-07-28: **Benjamin's re-architecture is out of base scope** — a follow-on programme. Whether he is needed falls out of the Sunday work plan.
- 2026-07-28: **Work plan due Sunday 2026-08-02**, reviewed and approved with the team: DoD, cost target, crash-free-at-load, headcount and timeline.
- 2026-07-28: **New client requests get named as new scope and priced** rather than absorbed into the retainer by default.
- 2026-07-27: Per Hai — finalize the project to the committed SLA / concurrent-session scope first; propose cost and latency improvements at the next stage, based on feedback from a substantial user sample rather than shipping them into the pilot. _(Superseded 2026-07-28: no such committed scope exists.)_
- 2026-07-22: Delivery/assembly status integration named the top strategic feature priority. Agent scope stays on shopping assistance, not design tools.
- 2026-07-22: Employee pilot (~1,000 users) set for ~Aug 1 with an AI-error disclaimer and 24/7 support for the first 1-2 months; CEO reviews performance in December to decide on a public launch.
- 2026-07-21: Shai took over the account from Arnon as client-facing lead.
