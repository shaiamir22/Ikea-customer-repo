# Release Plan — WhatsApp Shopping Agent, now → December decision gate

**Author:** Shai Amir, Moveo AI
**Date:** 2026-07-28
**For:** the Sunday 2026-08-02 work-plan review
**Companion to:** `../IKEA_WhatsApp_Shopping_Agent_PRD.md` (scope, jobs, objectives)

> **What this is.** The product-side release sequence and the timeline it implies. It answers the
> fourth heading the Sunday review asks for — **headcount and timeline** — and gives Tali and Niv the
> sequencing frame to hang dev-day estimates on. The estimates themselves are theirs; the ordering,
> the gates and the constraints are here.

---

## The frame

**December is a decision gate, not a launch date.** Five releases get us there. Each one is
independently useful and independently defensible if the next slips — which matters, because the
leave calendar (below) means at least one of them will come under pressure.

| Release | Window | Ships | Gate it clears |
|---|---|---|---|
| **R0** | now → **Sun 2026-08-02** | Employee release, hardened | 1,500 employees using it without improvisation |
| **R1** | Aug | Observability & evidence | We can state quality and cost without hand-counting |
| **R2** | Sep → Oct | Capacity & cost to the authored SLA | A bar we can put in writing to IKEA |
| **R3** | Sep → Nov | Customer readiness | The eight things that break for cold consumers |
| **R4** | late Nov → early Dec | Netanya branch live | Real customers, one branch, producing data |
| **—** | **Dec** | *Decision gate* | CEO reviews data pack; decides national rollout |
| **R5** | Q1 2027 | Staged widening | Only if December says yes |

---

## R0 — Employee release (Sun 2026-08-02) · **date-bound, cannot slip**

Moved from Thu 2026-07-30. 1,500 employees, up from the ~1,000 originally planned.

**Ships:** US-01 (fallback model routing), US-02 (named on-call rota + two-tier response policy),
US-03 (disclaimer, QR/link, internal video, proactive-messaging technical guard, CEO on the user list).

**Entry criteria — all must be true before Friday 2026-07-31:**

- [ ] Fallback routing live in production and verified by **fault injection**, not by waiting for the next Gemini outage
- [ ] Gemini crash root cause (2026-07-21) confirmed in writing, shared with Shai, Efrat, Avi
- [ ] Named on-call cover **per day**, circulated in writing
- [ ] Two-tier response policy communicated: acknowledge ≤15 min, fix may take hours
- [ ] Explicit statement that normal working hours do not apply on release day
- [ ] Onboarding QR/link updated and tested (Avi)
- [ ] Avi's internal-publication video ready — publishes after the sale ends 2026-07-30
- [ ] AI-error disclaimer live on first contact
- [ ] Proactive-messaging guard enforced technically, per Efrat's rule

**Two things to raise Sunday morning:**

1. **The collision.** The work-plan review and the employee release are the same day. Separate them or
   explicitly staff both. This is the single most avoidable risk in the plan.
2. **Tali is out from that same Sunday**, for two weeks. The rota cannot assume her.

**Exit criteria:** 72 hours post-release with no unhandled-exception outage >5 min, and an incident
log — even an empty one — written down.

---

## R1 — Observability & evidence (August)

The release that makes every later claim checkable. Without it, R2's cost target and R4's quality bar
are both assertions.

**Ships:** O5 instrumentation, J5 (one-tap bad-answer reporting), J15 (daily cost visibility),
conversation analytics out of DynamoDB, eval set v1 at 300 real cases, the 30-day employee survey.

**Why it comes first:** Niv reviewed **209 conversations by hand** to assess quality. That does not
survive 1,500 users. Every week R1 is late is a week of pilot traffic we cannot learn from — the
evidence window is the scarce resource here, not the engineering.

**Dependencies that are not engineering:**
- Conversation analytics access to DynamoDB — **Shai needs this via Arnon, this week**
- The eval set is currently **unlocated**. It blocks US-01's quality confirmation as well as O5. Finding it is on Niv / Arnon's team and it is the smallest task with the largest blast radius in this plan.

**Exit criteria:** a quality number, a cost-per-conversation number, and a p50/p95 latency number,
all produced without anyone reading a conversation by hand.

---

## R2 — Capacity & cost to the authored SLA (Sep → Oct)

The release that turns "the product isn't ready" into "the product meets this bar, here is the
evidence." This is what closes the gap with a client who believes we are already in the maintenance
phase.

**Ships:** O1 (cost model at three volume tiers **including Meta fees**), O2 (availability, error
budget, alerting), O3 (**the first load test ever run on this system**), O4 (continuous p50/p95).

**The cost reframe that changes this release's shape.** The ₪50k/month figure is the projection at
20,000 daily users — national scale. At December's actual scope it looks different:

| Scenario | Daily users | Projected | Verdict |
|---|---|---|---|
| Employee release | ~450 | ~₪1.1k/mo | Inside any target |
| Netanya pilot | ~400–800 | ~₪1–2k/mo | Inside any target |
| National | 20,000 | ~₪48k/mo | Needs ~85% reduction |

So **December is not gated on cost reduction** — it is gated on being able to *state* the cost
credibly at three tiers. The ~85% reduction national rollout needs is roughly what Benjamin's
re-architecture claims (~87%), which is why it belongs in the Phase 3 sale rather than in this
release. R2 delivers the model and the measurement, not the re-architecture.

**Biggest risk in the whole plan sits here:** R6 — there is **no load-testing capability on the team**.
The room's answer for the employee release was to observe it live. That does not extend to customers.
Either buy the capability in August or accept a stated-assumption capacity number and tell IKEA
plainly that is what it is.

**Also here:** Niv is out in September. R2 is the release that collides with it.

**Exit criteria:** a capacity number and a cost-per-conversation number we are willing to put in
writing to IKEA.

---

## R3 — Customer readiness (Sep → Nov) · **starts in August**

The eight gates from PRD §3. R3 is listed after R2 but **its client-side items must start in August**
— they are the long poles, and none of them are engineering.

**Start in August (long lead, client-side):**
- **C2 / OQ-2** — CISO + DPO conversation. **Bundle these into one session** covering fraud detection and customer-phase privacy together: one meeting, two unblocks.
- **C1 / OQ-13** — IKEA's WABA, Meta template category approval, and who pays Meta conversation fees
- **C7 / OQ-14** — IKEA order/delivery API access. They declined the receipts integration in June; if the answer is no again, J9 and C7 are dead and R4's scope shrinks accordingly.
- **C6** — contact-centre escalation integration. Raised by IKEA marketing in June, deferred. Without it, a customer launch moves load *onto* the call centre instead of relieving it, which contradicts the business case being sold.

**Engineering (Sep → Nov):** J6 (QR cold start), J7 (consent + AI disclosure on first contact),
J8 (escalation with conversation context), J9 (post-purchase status), J10 (Hebrew robustness).

**Exit criteria:** every gate C1–C8 pass/fail, with the fails explicitly accepted or the scope cut to
match.

---

## R4 — Netanya branch live (late Nov → early Dec)

One branch. Real customers. QR entry at the entrance, the self-serve area and checkout.

Deliberately narrow: it bounds Meta cost, PII exposure and the concurrency ceiling all at once, and
it is survivable with the team we actually have.

**Prerequisite:** the Netanya site visit (3+ hours, on-site) — currently unscheduled and needed well
before this release to place entry points sensibly.

**Exit criteria:** two weeks of real customer traffic and a December data pack — adoption, quality
against the pass mark, cost per conversation at real volume, latency curves, escalation rate, and the
failures we did not fix, stated plainly.

---

## December — the decision gate

Not a release. IKEA's CEO reviews the data pack and decides on national rollout; investment from the
American owners rides on it.

What we bring: **a working customer pilot at one branch, plus data.** Not a promise of national
coverage. Stronger evidence, and honest about what is still unproven.

---

## R5 — Staged widening (Q1 2027) · only if December says yes

Geographic widening → national. This is where Benjamin's re-architecture becomes necessary rather
than optional (the ~85% cost reduction), where Arabic and French get built, and where the commerce-vs-service
question (OQ-15) has to be answered.

---

## What bounds the timeline

**Leave is the binding constraint, not scope.**

| Who | Out | Hits |
|---|---|---|
| **Arnon** | shortly | **The plan must close before he leaves** — he holds most of the technical context |
| **Tali** | two weeks from Sun 2026-08-02 | R0 launch week and the start of R1 |
| **Niv** | September | R2 — capacity and cost, the heaviest engineering in the plan |

Plus: Efrat is travelling abroad and Avi follows her, which is why the commercial meeting sits in the
**second half of August**.

**The immovable one:** sit with Arnon this week and extract what he holds. Everything else in this
plan can slip by a week. That cannot — if it does, a month is lost.

---

## Headcount recommendation

**Two developers, from September.** The product-side reading, for engineering to confirm or reject
with real estimates:

- R0 and R1 are achievable with one developer, because R0 is mostly configuration and policy and R1 is instrumentation.
- **R2 and R3 overlap by design** — R3's client-side gates have to run in parallel with R2's engineering or they become the December blocker. One developer cannot run both, and September is exactly when Niv is out.
- R6 (no load-testing capability) is a *skills* gap on top of the headcount gap. A second developer who can run a load test solves two problems at once; a second developer who cannot solves one.

**With one developer:** R3 and R4 slip past December, and the decision gate arrives with employee data
instead of customer data — which is a materially weaker case in front of the CEO.

This is a recommendation from the product side. **The dev-day estimates, sequencing within each
release, and the final one-or-two-developer call belong to Tali and Niv with Arnon.**

---

## What engineering owes back for Sunday

Per the 2026-07-28 action item — a spreadsheet or Gantt of technical tasks broken to dev-days:

1. **Dev-day estimate per job (J1–J15) and per objective (O1–O5).** The PRD is structured so each one is estimable on its own.
2. **Sequencing and dependencies** within and across R0–R4.
3. **Validate, replace or reject the O3 concurrency heuristic.** State your assumptions; do not wait for exact numbers.
4. **A one-or-two-developer call** with the reasoning.
5. **Two specific unblocks:** locate the eval set, and confirm whether the lighter routed model passes quality checks.

---

_Sources: `../context/meetings/2026-07-28-internal-ikea-sync.md`; `../../context/meetings/2026-07-28-internal-ikea-sync-commercial.md`; `../context/meetings/2026-07-27-arnon-roadmap-conversation.md`; `../context/comms/2026-07-27-benjamin-poc-handover.md`; `../../context/meetings/2026-07-22-ikea-status-sync.md`; `../../context/meetings/2026-07-21-ikea-sync-onboarding.md`; `2026-07-28-internal-position-path-to-customers.md`._
