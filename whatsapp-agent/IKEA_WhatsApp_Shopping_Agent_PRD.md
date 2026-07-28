# PRD: WhatsApp Shopping Agent
**Product:** WhatsApp Shopping Agent
**Author:** Shai Amir, Moveo AI
**Date:** 2026-07-28
**Status:** Draft — for the Sunday 2026-08-02 work-plan review

> **How to read this.** This is the **product half** of the work plan due Sunday 2026-08-02. It defines
> what the initial product is, what bar it has to clear, and what is deliberately not in it. The
> **technical breakdown belongs to Tali and Niv, with Arnon** — every job (J-NN) and objective (O-N)
> below is written to be estimated in dev-days, sequenced, and given dependencies. Where a number is
> provisional it says so; do not treat a provisional figure as agreed.

---

## 1. Problem Statement

IKEA customers and employees need a fast, reliable way to search products, get recommendations, and navigate the store without waiting on staff or digging through the website — delivered as a WhatsApp agent, at a cost per message IKEA can sustain at scale.

Five months in, the agent is live and genuinely good: 25,480 products in the live catalogue, 122K stock
records across 5 branches, 24 dedicated tools, ~30% of queries answered on a fast path with no LLM
call, ~25 automatic validation checks on every answer, and cost per conversation already down from
$0.03 to $0.01. What it does not have is a **definition of done**. No SLA, latency target, or
concurrency figure appears anywhere in the SOW or the quote — so there is no bar to declare met, no
number to engineer against, and every new request lands inside the retainer by default.

The problem this PRD solves is therefore narrower than the product problem above, and it is the one
blocking December: **author the bar, scope the product that clears it, and make both estimable.**

---

## 2. Solution Overview

**IKEA Smart Agent v1** — the shopping assistant IKEA can put in front of real customers at one
branch, with the operational evidence to decide whether it goes national.

The central reframe, agreed in the 2026-07-28 internal sync and carried through this document:
**December is a decision gate, not a launch date.** What goes in front of IKEA's CEO is a working
single-branch customer pilot plus data — not a promise of national coverage. That is both stronger
evidence and survivable with the team we actually have.

Delivery is staged so that each stage is independently useful and independently defensible if the
next one slips.

**Phase 1 — Employee Release & Authored SLA (now → end Oct).** Land the 1,500-employee release on
Sun 2026-08-02 without improvisation, then harden the agent against a bar we write ourselves:
crash-free at a stated load, cost visible against a stated target, quality measured against an eval
set with a pass mark. Phase 1 turns "the product isn't ready" into "the product meets this, here is
the evidence."

**Phase 2 — Netanya Branch Customer Pilot (Sep → Dec).** Close the eight things that genuinely break
when you go from a known employee allowlist to cold consumers — consent and entry, privacy, human
escalation, post-purchase content coverage, language — and run one branch live with real customers
long enough to produce the December data pack.

The sequencing is deliberate: Phase 2 work starts before Phase 1 finishes, because the customer-side
gates have long lead times that are not engineering (CISO, DPO, Meta template approval, IKEA API
access). Those get started in August or they become the December blocker.

---

## 3. Phases

| Phase | Name | Primary Persona | Value Delivered | Status |
|---|---|---|---|---|
| 1 | Employee Release & Authored SLA | Efrat — IKEA employee | An agent 1,500 employees use daily without it falling over, measured against a bar we authored, producing the usage evidence December needs | **In scope** |
| 2 | Netanya Branch Customer Pilot | Noa — IKEA customer, Netanya | One branch live with real customers, plus the data that lets IKEA's CEO decide on national rollout | **In scope** |
| 3 | National Rollout & Commerce Surface | — | Geographic widening, post-purchase depth, commerce features | Pending December decision |

_Phase sequencing and delivery cadence are recommendations for discussion with engineering — final scope and timeline to be agreed jointly. Each user story (US-NN in §4) is itself an independently shippable delivery — there is no separate delivery numbering._

### Phase 2 detail — Netanya Branch Customer Pilot

Phase 2 is scoped by a single question: **what actually breaks when the user is a cold consumer
instead of a known employee?** These are not wish-list items; each one is a thing that fails without
work.

| # | Gate | What has to be true | Lead time driver |
|---|---|---|---|
| C1 | Consent & entry point | QR/link entry at the Netanya entrance, self-serve area and checkout. Privacy notice on first contact. IKEA's WABA with approved Meta template categories. Written proactive-messaging policy, enforced as a technical guard. | Meta template approval |
| C2 | Privacy & security | Privacy notice, data-processing appendix, retention policy (today: 30-day cart, conversation logs in DynamoDB), and a ruling on whether any external AI provider may see customer messages. **Bundle the DPO/legal review with the CISO conversation already needed for fraud detection — one meeting, two unblocks.** | Client-side (CISO/DPO) |
| C3 | Unit economics, both layers | LLM/infra is modelled at $0.01/conversation. **Meta conversation fees on IKEA's WABA are unmodelled and land on IKEA.** Produce the all-in number at three volume tiers before anyone commits publicly. | None — do it now |
| C4 | Capacity | A load test result, not a guess. See O3. | Test capability gap (§7 R6) |
| C5 | Quality bar | Eval set with a pass mark, plus automated QA replacing manual conversation review. See O5. | Needs pilot traffic first |
| C6 | Human escalation | Hand-off into IKEA's contact centre **with conversation context**. Raised by IKEA marketing in June and deferred. Without it, a customer launch moves load *onto* the call centre instead of relieving it — which contradicts the business case we are selling. | IKEA contact-centre integration |
| C7 | Content coverage | Customers ask about order status, delivery, assembly, returns, credits. That is the delivery/assembly integration (already IKEA's top priority) plus the post-purchase data they declined in June. | IKEA API access |
| C8 | Language | Hebrew is primary. Arabic and French were requested and are not built; customer traffic at Netanya includes Arabic speakers. Arabic/French are **out of v1** (§5) — this gate is Hebrew robustness only. | None |

**Phase 2 jobs to be done** — estimable alongside Phase 1's:

- **J6 — Cold start.** When I'm standing in the Netanya store, I want to scan a QR and start chatting without installing anything, so I can get help immediately. _(C1)_
- **J7 — Informed consent.** When I first message the agent, I want to know I'm talking to AI and what happens to my data, so I can decide whether to continue. _(C1, C2)_
- **J8 — Escape hatch.** When the agent can't help me, I want a hand-off to a human with my conversation attached, so I don't have to repeat myself. _(C6)_
- **J9 — Post-purchase.** When I ask about an order I already placed, I want its delivery and assembly status, so I don't have to call the service centre. _(C7)_
- **J10 — My own Hebrew.** When I write in Hebrew the way I actually speak — abbreviations, typos, colloquial product names — I want to be understood. _(C8)_

---

## 4. Phase 1 — Employee Release & Authored SLA

### Problem We're Solving

Two gaps close here, and they compound each other.

**Operationally:** the 1,500-employee release on Sun 2026-08-02 is the last gate before IKEA starts
asking when real customers get this. The previous releases ran on improvisation and it showed — the
agent crashed repeatedly on 2026-07-21 during Gemini instability and halted Efrat's testing outright.
A shaky release creates negative internal perception at IKEA ahead of the December CEO review, which
gates both the public launch and investment from the American owners.

**Definitionally:** the client believes the project is already in its SLA / bug-fix phase. The room's
read of the product's actual state is different. That gap has to be closed deliberately rather than
left to surface on its own — and it cannot be closed until there is a bar to close it against. Phase 1
authors that bar and then meets it.

Who benefits immediately: 1,500 IKEA employees get a tool that answers faster than walking to a
terminal, and Moveo gets the usage evidence that makes the December conversation about data instead
of promises.

### Who We're Solving This For

**Persona 1: Efrat — Employee tester / shop-floor employee, IKEA**
Works the floor. Gets asked about stock, location and delivery status constantly, and today the
answer means walking to a terminal or calling someone. She has been testing the agent and hit
repeated crashes on 2026-07-21 that stopped her work entirely. She will forgive a slow answer; she
will not forgive an agent that is down when a customer is standing in front of her. Her tolerance for
a wrong answer is higher than a customer's — she can sanity-check it — but she has no patience for
having to check every answer. She has also set a hard rule: **no proactive messaging to non-users.**

**Persona 2: Niv — Developer / on-call, Moveo**
The sole developer today, junior, and until Tali's ramp lands he is the single point of failure. He
recently reviewed **209 conversations by hand** to assess quality. That does not survive 1,500 users,
let alone customers. He needs the agent to fail over on its own at 21:00 rather than page him, and he
needs quality and cost to be observable without manual sampling. Every operator job below (J11–J15)
exists because Niv currently does it manually or cannot do it at all.

_Secondary: **Avi** (employee onboarding — owns the QR/link and the internal publication video) and
**Shuki** (IKEA tech lead — cares most about answer accuracy and service quality)._

### How We Measure Success

Phase 1 targets. Where a figure is provisional it is marked; provisional figures need a decision
before the plan can be costed against them.

| Metric | Target |
|---|---|
| Employee adoption | ≥600 of 1,500 employees send ≥1 message in the first 30 days; ≥250 weekly actives by end Sep |
| Availability | ≥99.5% monthly; **zero** unhandled-exception outages lasting >5 min |
| Model-provider failover | Automatic, within one request, no user-visible failure — verified by fault injection, not by waiting for an outage |
| Latency | p50 ≤9s, p95 ≤15s — a **no-regression constraint**, not an improvement goal (see O4) |
| Cost per conversation | Held at or below today's $0.01, with a published model at three volume tiers (see O1) |
| Quality | ≥90% task success on catalogue & stock intents, ≥85% overall, on a 300-case eval set built from real observed failures |
| Manual QA effort | Zero hand-reviewed conversations required to state a quality number |
| Time to acknowledge an incident on release day | ≤15 min, per the two-tier policy |

---

### Epics & User Stories

Jobs are written from the user's side. **J-NN** are functional jobs; **O-N** are engineering
objectives that cut across them. Both need dev-day estimates — the objectives are where most of the
risk sits, and they are the four headings the Sunday review asks for.

---

#### Epic 1: The release lands without improvisation

Everything that must be true by Sun 2026-08-02. This epic is date-bound and cannot slip.

**US-01 / J11 — Survive a provider outage**
When the primary model provider fails, the agent fails over automatically so users never see a crash.

Acceptance Criteria:
- Fallback model routing live in production, configured for the existing flow (config already approved per Arnon, 2026-07-27)
- Failover triggers within one request on primary-provider error; the user sees a normal answer, not an error or a hang
- Verified by deliberate fault injection against the primary provider, not by waiting for the next outage
- Gemini crash root cause from 2026-07-21 confirmed in writing and shared with Shai, Efrat and Avi
- The lighter routed model is confirmed to pass quality checks against the eval set — **blocked on locating the eval set** (Niv / Arnon's team)

**US-02 / J12 — Someone is actually on call**
When something breaks at 21:00 on release day, a named person is on call and the response policy is written down.

Acceptance Criteria:
- Named on-call cover **per day**, in writing, circulated before Fri 2026-07-31
- Explicit statement that normal working hours do not apply on release day
- Two-tier response policy in force: acknowledge ≤15 min ("received, we're on it"), fix allowed to take hours
- Rota accounts for Tali being unavailable during launch week (out two weeks from 2026-08-02)
- **Note the collision:** the work-plan review and the employee release currently land on the same day. Separate them or explicitly staff both.

**US-03 — Release hygiene**
Employees arrive to a release that behaves like one.

Acceptance Criteria:
- AI-error disclaimer shown on first contact
- Onboarding QR/link updated and verified (Avi)
- Avi's short internal-publication video delivered, scheduled after the sale ends 2026-07-30
- Efrat's no-proactive-messaging rule enforced as a **technical guard**, not a promise
- CEO added to the agent's user list for passive review

---

#### Epic 2: The employee jobs the agent is for

The functional core. Mostly built — the estimate here is the delta to reach the Phase 1 quality bar,
not a rebuild.

**US-04 / J1 — Stock at my branch**
When a customer asks me about a product on the shop floor, I can check whether it's in stock at my branch, so I answer without leaving them to find a terminal.

Acceptance Criteria:
- Stock answered per-branch across all 5 branches from the 122K-record stock integration
- Answer states branch and quantity band, and says plainly when stock is unknown rather than guessing
- Meets the ≥90% catalogue-and-stock pass mark on the eval set

**US-05 / J2 — Where is it**
When I'm asked where an item is, I get the aisle and bin location, so I direct the customer precisely.

Acceptance Criteria:
- Aisle/bin returned for in-stock self-serve items at the queried branch
- Distinguishes showroom, self-serve and warehouse-only items
- Says so explicitly when location data is unavailable

**US-06 / J3 — Describe, don't name**
When a customer describes what they need rather than naming it, the agent surfaces plausible products, so I can offer options.

Acceptance Criteria:
- Returns a ranked shortlist with enough detail to choose between options
- **Scoped deliberately:** semantically complex query handling (e.g. "ארונית קלה" → "כוורת") is **excluded** from the December bar per the 2026-07-28 decision. Improve incrementally; do not let it gate the release. It is excluded from the eval-set pass mark accordingly.

**US-07 / J4 — Delivery and assembly status**
When a customer asks about their delivery or assembly booking, I get the current status, so I don't hand them to the call centre.

Acceptance Criteria:
- Delivery/assembly status returned for a valid order reference
- Tracking link tested end to end and reported to Avi
- IKEA's **top strategic feature priority** — automates a high-volume service query and reduces call-centre load. Carries into Phase 2 as C7.

**US-08 / J5 — Report a bad answer**
When the agent gets it wrong, I say so in one tap, so the failure becomes an eval case instead of a shrug.

Acceptance Criteria:
- One-tap negative feedback on any agent turn
- Captured with full conversation context and queued into the eval-set pipeline (feeds O5)
- Volume and top failure categories visible without manual review

---

#### Epic 3: Objectives — the four headings the Sunday review asks for

These are not user stories, and they are where the estimate actually lives. Each needs dev-days,
sequencing, dependencies, and a one-or-two-developer call.

**O1 — Cost: hit a monthly target that is stated together with a load**

The single most important correction in this document: **a cost target is meaningless without the
load it is measured at.** The ~₪50k/month figure everyone is reacting to is the projection at
**20,000 daily users** — the national target, not the December scope.

Product-side model, assumptions stated for engineering to validate or replace:

| Scenario | Daily users | Msgs/user/day | Msgs/month | @ ~₪0.001/msg | Verdict |
|---|---|---|---|---|---|
| Employee release (Aug) | ~450 (30% of 1,500 DAU) | ~80 | ~1.1M | **~₪1.1k/mo** | Comfortably inside any target |
| Netanya pilot (Dec) | ~400–800 ramping | ~80 | ~1–1.9M | **~₪1–2k/mo** | Comfortably inside any target |
| National (post-decision) | 20,000 | ~80 | ~48M | **~₪48k/mo** | **Unsellable — needs ~85% reduction** |

Two conclusions follow, and both should be put to the room on Sunday:

1. **December is not gated on cost.** At single-branch volumes the agent is already affordable. The
   ₪50k problem is a *national-rollout* problem, which is precisely the thing December *decides*.
2. **The ~85% reduction that national rollout needs is almost exactly what Benjamin's
   re-architecture claims (~87%).** The room ruled it out of base scope on 2026-07-28, and for
   December that is right. But the arithmetic says national rollout is not reachable without
   something of that magnitude — so it should be sold as the **Phase 3 enabler**, not shelved.

Acceptance Criteria:
- One monthly cost target agreed, replacing the three competing figures (₪3–5k / ₪5–8k / ~₪8k). **Provisional: ₪5–8k/mo at national load**, pending Hai/David sign-off — see OQ-8
- All-in cost published at three volume tiers, **including Meta conversation fees**, which are currently unmodelled and land on IKEA (C3)
- Per-message cost observable per day against target, without manual calculation (J15)
- Cost work must not breach the O4 latency bar

**O2 — Reliability: crash-free at target load**

Acceptance Criteria:
- ≥99.5% monthly availability; zero unhandled-exception outages >5 min
- Automatic model-provider failover verified by fault injection (US-01)
- Error budget defined, with a written rule for what happens when it is spent
- Alerting that pages the named on-call person rather than relying on a user reporting it

**O3 — Capacity: a number backed by a test, not a heuristic**

**No load test has ever run.** Until one does, we cannot state a capacity number — and the team
currently has no capacity to run one (§7 R6). The room's instruction was to state assumptions and
proceed rather than wait.

Product-side heuristic for engineering to check, replace, or reject:

- Target **20,000 daily users** — explicitly daily, not concurrent
- ~10,000 people/day visit IKEA's site; assume a low-thousands share reach the bot
- A conversation runs 10–150 messages; assume ~80 as the working mean
- Peak hour ≈ 15% of daily traffic → ~3,000 users in the peak hour
- Active conversation ≈ 10 min → **~500 concurrent sessions**
- ~3,000 users × 80 msgs ÷ 3,600s → **~67 msg/s at peak**
- At a 9s response time → **~600 in-flight invocations**

Against the known bottleneck — **AWS Lambda's 1000-concurrency limit** — that lands inside the
ceiling but without comfortable headroom, and the estimate is sensitive to the messages-per-conversation
assumption. Gemini/AWS reportedly support ~3,000 concurrent messages. The difference between 10k and
20k daily users was called a factor of two, not an order of magnitude, and not worth stalling over.

Acceptance Criteria:
- Concurrency defined by heuristic with assumptions written down — messages per conversation, users per day, concurrent sessions (Tali & Niv)
- A load test run at least once, establishing the real ceiling
- A stated capacity number we are willing to put in writing to IKEA
- Lambda concurrency headroom confirmed or a mitigation costed

**O4 — Latency: hold the line**

Current average 8–9s (9.3s measured). The room's read on 2026-07-28: this is near the floor of the
current implementation, and going materially lower means a rewrite estimated at three months minimum.

**Provisional target: p50 ≤9s, p95 ≤15s**, framed as a **no-regression constraint on the cost work**
rather than an improvement goal — pending confirmation, see OQ-11. Reasoning, which is owed alongside
the number: latency is not the top complaint that cost is, it improves as a by-product of cost work,
and funding it as its own line item buys a rewrite we cannot afford before December.

One useful consequence: Benjamin's +4–7s on a 9.3s base lands at 13–16s, which **straddles the p95
bar**. Setting this target therefore partially answers OQ-1 rather than leaving it open indefinitely.

Acceptance Criteria:
- p50 and p95 measured continuously at real volume, not sampled by hand
- No cost optimisation ships that breaches the p95 bar
- Known 5-model-calls-per-message bug confirmed fixed or confirmed already resolved — it helps both latency and cost

**O5 — Quality: a bar with a pass mark, measured automatically**

Acceptance Criteria:
- Eval set located (currently unlocated — blocks US-01) and rebuilt to **300 cases drawn from real observed failures**, including the J5 feedback queue
- Pass mark: **≥90% on catalogue & stock intents, ≥85% overall**
- Runs automatically per release. **Zero** hand-reviewed conversations required to state a quality number
- Conversation analytics available out of DynamoDB — *Shai needs access via Arnon*
- Larger employee survey (ratings + free text) run at the 30-day mark
- Photo→SKU is a known weak point — five separate survey respondents named it, one writing the agent is *"still far from usable for a customer."* **Decision required (OQ-12):** fix to bar, hold at a reduced bar, or disable the entry point for the customer pilot. Estimate all three.

---

## 5. Out of Scope / Future Phases

Explicitly excluded from v1. Each of these is a real thing someone has asked for — listing them here
is what stops them landing inside the retainer by default, per the 2026-07-28 rule: **when a new
request arrives, say plainly that it is new scope and price it.**

- **Benjamin's LLM-sandwich re-architecture** — ~87% cheaper/message, any-language, vendor-agnostic via OpenRouter, +4–7s latency. Built and behind an off-by-default switch, 2,474 tests passing on `origin/staging-llm-sandwich-py312`. Out of base scope per 2026-07-28; **recommended as the Phase 3 national-rollout enabler** on the O1 arithmetic. Hebrew testing is the remaining validation gap.
- **Search quality on semantically complex queries** — improve incrementally, do not let it gate December.
- **Photo→SKU recognition** — pending the OQ-12 decision.
- **Fraud detection** — base is ready, gated on a coordinated CISO conversation. Separate paid workstream. Note a ~$250/month environment has been billing unused for ~3 months.
- **Arabic and French** — requested, not built. Hebrew robustness only in v1.
- **National rollout** — what December decides, not what December ships.
- **In-chat payment / checkout** — contradicts IKEA's in-store model. Stop offering it until they say otherwise.
- **Push and proactive messaging** — the 13/7 deck calls push the easiest follow-on, but Efrat has already forbidden proactive messaging to non-users, and the constraint gets *stricter* for consumers.
- **Restaurant food menus, allergy info, mobile ordering** — Phase 3 vision.
- **Linking agent interactions to in-store purchases** for full customer-journey data — Phase 3 vision.
- **Design tools** — strategic focus stays on shopping assistance, confirmed 2026-07-22.
- **Load/stress testing, automated QA tooling, dedicated 24/7 support staffing** — named as outside the retainer and priced separately, even though O2/O3/O5 depend on them. This is a commercial boundary, not a technical one: the work is in scope for the *product*, and out of scope for the *₪10k retainer*.

---

## 6. Open Questions

| # | Question | Owner | Due |
|---|---|---|---|
| OQ-1 | Is +4-7s latency acceptable in exchange for the ~87% per-message cost saving? Partially answered by the O4 p95 bar — 13–16s straddles it. | Client | Aug (commercial mtg) |
| OQ-2 | Data-protection sign-off to send real customer messages to an external AI provider (OpenRouter) | Client | Bundle with CISO — Aug |
| OQ-3 | Which improvements fall under the existing retainer vs. a new paid scope? | Us | Before Aug client mtg |
| OQ-5 | Can the fraud-detection workstream start? Needs a coordinated conversation with IKEA's CISO. | Client | Aug |
| OQ-7 | What SLA do *we* commit to, given none exists in the agreement? §4 O1–O5 is the proposed answer — confirm or amend it on Sunday. | Us | **2026-08-02** |
| OQ-8 | Which single monthly cost target do we hold ourselves to? ₪3-5k, ₪5-8k, and ~₪8k are all in play. **Provisional: ₪5–8k at national load.** Note per O1 that December is not gated on this. | Us (Hai/David) | **2026-08-02** |
| OQ-9 | What is the real concurrency ceiling? No load test has ever run, and there is no capacity on the team to run one. | Us | Sep |
| OQ-10 | How is the ~₪140k (worse case ~₪200k) cost of finishing this fixed-price project funded? Intent is new paid scope sold in August, not an overrun invoice. | Us | Aug |
| OQ-11 | Confirm the latency target as a no-regression constraint (p50 ≤9s / p95 ≤15s) rather than an improvement goal. **Provisional pending Sunday.** | Us | **2026-08-02** |
| OQ-12 | Photo→SKU: fix to bar, hold at a reduced bar, or disable for the customer pilot? Five survey respondents named it as the weak point. | Us | Sep |
| OQ-13 | Whose WABA does the customer phase run on, and who pays Meta conversation fees at customer volume? Currently unmodelled and landing on IKEA. | Client | Sep |
| OQ-14 | Will IKEA open order/delivery APIs, having declined the receipts integration in June? C7 and J9 depend on it. | Client | Sep |
| OQ-15 | Does IKEA want a service channel or a commerce surface? Shapes Phase 3 entirely. | Client | Dec |

_OQ-4 and OQ-6 were answered on 2026-07-28 and are retired: Tali is staying and taking technical tasks (remainder tracked under R1); and nothing is committed in writing on SLA (superseded by OQ-7)._

---

## 7. Risks

| # | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R1 | Niv is the sole developer. Tali is ramping onto technical work, but it is a ramp not a switch. Compounded by leave: Tali out two weeks from 2026-08-02, Niv out in September, Arnon out shortly. | High | High | **The plan must close before Arnon leaves** — he holds most of the technical context. Sit with him this week (Tali & Niv). Standing Sunday one-hour technical rundown. Two-developer recommendation in the work plan. |
| R2 | Cost projects to ~₪50k/mo at national load against a ₪5–8k target, making the product unsellable at scale. | High | High | Per O1, decouple December from national: single-branch volumes are already affordable. Sell the re-architecture as the Phase 3 enabler rather than absorbing it. |
| R3 | Gemini API instability crashes the agent; no fallback model in production yet. | High | High | US-01, before 2026-08-02. Fault-injection verified. Root cause confirmed in writing. |
| R4 | A shaky pilot creates negative internal perception at IKEA ahead of the December CEO review, which gates the public launch and investment from the American owners. | Medium | High | Epic 1 in full. Named rota, two-tier response policy, disclaimer, technical guard on proactive messaging. |
| R5 | Hebrew testing is not yet done on Benjamin's PoC — Hebrew is the primary customer language. | High | Medium | Out of base scope, so this is a Phase 3 gate rather than a December one. Add Hebrew tests before the PoC can be validated at all. |
| R6 | **No load-testing capability on the team.** The room's answer for the employee release was to observe it live. That does not extend to customers, and O3/C4 depend on it. | High | High | Named as a missing skill, not resolved. Either buy the capability or accept a stated-assumption capacity number and say so in writing to IKEA. |
| R7 | **Date collision:** the work-plan review and the 1,500-employee release both land on Sun 2026-08-02. | Certain | Medium | Separate them, or explicitly staff both. Raise Sunday morning. |
| R8 | The client believes the project is already in its SLA / bug-fix phase; the room's read differs. Left alone, this surfaces on its own terms in December. | High | High | Close it deliberately at the second-half-of-August commercial meeting, with the §4 bar as the artefact that makes the conversation concrete. |
| R9 | Long-lead Phase 2 gates (CISO, DPO, Meta template approval, IKEA order APIs) are client-side and start slow. | High | High | Start them in August, not September. Bundle DPO with the CISO conversation — one meeting, two unblocks. |

---

## Revision History

- 2026-07-28: Filled from the 2026-07-27 Arnon roadmap conversation, the 2026-07-28 internal sync (product and commercial halves), the internal position paper, and the Benjamin PoC handover. Authored the SLA bar (O1–O5) that the agreement never specified; scoped v1 to a single-branch December decision gate; separated the cost target from the load it is measured at. Product half of the Sunday 2026-08-02 work plan — technical breakdown owed by Tali and Niv with Arnon.
- 2026-07-27: Initial draft created.
