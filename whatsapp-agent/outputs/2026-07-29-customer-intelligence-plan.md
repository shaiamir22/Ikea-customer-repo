# Plan — Customer Intelligence, Personas, and a Product View Over the Project

_Date: 2026-07-29. Owner: Shai Amir. Status: proposal, not yet agreed._

**Companion:** `whatsapp-agent/context/research/2026-07-29-customer-data-inventory.md` —
the verified inventory of what data exists, with code citations. Read it first; this plan
assumes it.

---

## 1. What this is, in one paragraph

Extract everything we hold about the people using the IKEA WhatsApp agent, turn it into a
small number of behaviour-based personas, and stand up a product-level view of the project
that sits alongside the engineering views we already have. The aim is not a persona deck.
The aim is that the December review — and the August commercial meeting before it — is
argued with evidence about customers rather than charts about latency.

## 2. Why now

Four things converge:

1. **Volume arrives on 2026-08-02.** ~1,500 employees. Today's traffic is too thin to
   segment; in two weeks it will not be. Whatever we fail to instrument before then, we
   analyse without.
2. **December is a decision gate, not a launch** (decision, 2026-07-28). What gets decided
   is national rollout. A CEO deciding that wants evidence about customers and demand, and
   our entire observability estate is currently engineering-shaped.
3. **The August commercial meeting needs a story that isn't an apology.** The vehicle for
   recovering the ~₪140k gap is selling new scope. Demand evidence from real usage is the
   most credible input to that conversation we could bring.
4. **Two of these capabilities were already presented as delivered.** The Feb 2026
   requirements map put customer-intent detection (`מתעניין / מתלבט / קונה`) and a
   demand-and-trends dashboard in the **in-bot** bucket. Neither exists. That has a
   commercial edge — it argues this work sits inside committed scope rather than being new
   scope — and a risk edge, because it is an open claim heading into a CEO review. Handle
   it deliberately either way.

## 3. The honest starting position

We hold far more than a typical pilot, and much less than "customer data".

**Strong:** every message both directions with full text; which button was offered and
which was tapped; per-turn traces with the model's own reasoning, every tool call, and
every validator — for *everyone*, since `DEBUG_PHONES='*'`; a live per-turn trajectory
pipeline already deployed and already clustering; four kinds of feedback including a
comparable survey; and `rejected_items` / `search_intent_constraints` / `more_clicks` /
`active_goal`, which are the four richest intent signals in the system.

**Absent:** any purchase outcome, any demographics, any cross-channel identity, any visit
boundary.

**Three things that will bite if not said out loud:**

- **The pilot population is employees, not customers.** Employees know the catalogue and
  use internal vocabulary. Anything derived from pre-December traffic is an *employee*
  persona set unless a customer cohort is deliberately separated. This is the largest
  validity threat in the exercise and it must be on the front page of any deliverable.
- **A `שיחה חדשה` reset destroys the richest part of a person's record.** It wipes
  `conversation_context` — cart, goal, rejected items — with no archive. We are losing this
  now, and about to lose 100× more of it.
- **The existing clustering answers a different question.** `cluster_by_mechanism.py`
  clusters turns by failure mechanism (M1–M7). That is "how did the pipeline break", not
  "who was this person and what did they want". The customer axis is genuinely missing —
  but it is a *sibling* of the mechanism axis, and should be built as one.

## 4. Guardrails

These are what make the plan fundable rather than another cost line.

- **No new table scans.** `dashboard_aggregator.py` already scans the table once a minute,
  and its own docstring records that a `FilterExpression` does not reduce scan RCU. Ride
  `data.json` and the `IkeaTrajectories` table.
- **Deterministic before LLM.** Every feature that can be computed with code gets computed
  with code. LLM passes run on *samples*, never the corpus. We are mid-cost-crisis; an
  analytics job in the same spend class as the problem is not acceptable.
- **Extend the trajectory rail, don't build a second pipeline.** It already fans out
  per-turn, structured, off the hot path.
- **No eval runs** as a side effect of any step (standing repo rule).
- **Pseudonymise at extraction.** Phone → stable salted id, held in one mapping file
  outside the analysis corpus.
- **Nothing customer-identifying leaves the existing boundary.** Gemini via Vertex is
  inside it. Any external provider is OQ-2 territory and is out of bounds until signed off.

---

## Phase 0 — Instrument before the release (2026-07-29 → 08-02)

**Goal:** stop losing data, and add the customer axis to what the trajectory pipeline
already records. Analysis is explicitly *not* in this phase.

**The tension, stated plainly:** pushing to `main` deploys straight to production with no
staging gate, three days before a 1,500-person release, on a project that crashed on
2026-07-21. That is a real risk and I am not going to pretend it is free. My recommendation
is to land **only P0-1**, and only if Niv reviews it; if it does not clear review, accept
the data loss and ship it after the release stabilises. P0-2 and P0-3 wait until the week
of 08-04 regardless.

| # | Change | Why | Size |
|---|---|---|---|
| **P0-1** | On `שיחה חדשה` reset, write a snapshot row (`USER#<phone>` / `CTXSNAP#<ts>`) with the `conversation_context` being discarded, before the `REMOVE` | The only genuinely urgent item. Right now this data is destroyed; volume is about to 100× | Small — one put before an existing remove |
| **P0-2** | Add a `customer_signals` block to the trajectory record produced by `extract_trajectories.py` / the trajectory consumer: goal type, entry mode (text/image/voice/button), rejected-item count, refinement count, cart-add flag, service-vs-shopping flag, language | Puts the customer axis on the rail that already exists, at ~zero marginal cost | Medium, additive, no hot-path change |
| **P0-3** | Backfill `is_test` labelling as far back as possible from `CONFIG/TESTERS` ∪ `TESTER_PHONES` | Pre-2026-07-03 rows are unlabelled; tester traffic must be excludable from personas | Small, offline script |

**Also in this window, and free:** get AWS read credentials to whoever does the analysis,
and establish the four unverified numbers (distinct phones with ≥1 inbound, total MSG rows,
earliest reliable `createdAt`, trace retention depth including the known 05-18→05-29 hole).
Nothing downstream can be sized without these.

**Exit:** reset snapshots live or consciously deferred; corpus depth known; credentials in
hand.

---

## Phase 1 — Build the corpus (week of 2026-08-04, ~4 days)

**Goal:** one analysis-ready dataset, offline, deterministic, zero LLM.

1. **Extract.** Traces via the concurrency pattern already in
   `extract_trajectories.py` (16 parallel S3 downloads, ~300 traces in 15–20s); DDB rows
   via targeted per-person queries off the `CONV#` roster, not a scan. Pseudonymise on
   write.
2. **Reconstruct visits.** No visit boundary exists, so define one: an idle gap (start with
   30 min, tune against the distribution) or an explicit reset. Every downstream metric
   depends on this choice — write it down and keep it fixed.
3. **Build a per-person feature table.** Deterministic only:
   - *Goal shape* — `active_goal.type` (room / list / custom), modular-config flag,
     single-item lookup vs multi-item plan
   - *Decisiveness* — turns to first cart add, `rejected_items` count, search-refinement
     count, `more_clicks`
   - *Entry mode* — text / image / voice / button-tap mix
   - *Service vs shopping* — `data_source` + FAQ-cache-dominant vs search-dominant
   - *Depth* — `bot_message_count`, visit length, visits per person
   - *Outcome proxies* — cart add, pickup list generated, and the abandonment point when
     neither happened
   - *Context* — language, preferred store, employee-vs-customer flag, tester flag
   - *Experience received* — turns hitting an M1–M7 mechanism, p50/p90 latency, error hits.
     This lets us ask which personas got the worst product, which is the bridge between the
     two axes.
4. **Mine demand deterministically.** Reuse the FAQ-miner pattern (cluster → human
   approve → publish) over: zero-result searches, `rejected_items`, and the existing
   `CACHE_MISS` corpus. This produces a ranked "what people wanted that we could not
   serve" list — the direct input to the August scope conversation.

**Deliverable:** feature table + a written data-quality note (coverage, holes, biases).

---

## Phase 2 — Personas (week of 2026-08-11, ~4 days)

**Goal:** 4–6 behaviour-based personas, defensible, ready for the August commercial meeting.

**Method — behaviour clustering, not demographics.** We have no demographics, so personas
are built from the feature table: cluster on the axes above, then characterise each cluster
by reading a *sample* of real conversations from it. LLM summarisation applies to the
sample only (tens of conversations), never the corpus. Every persona claim traces to a
cluster statistic or a quoted conversation — a persona that cannot be traced gets cut.

**Each persona states:** size (% of people, % of turns); what they are trying to do; entry
mode and language; where they succeed; **where the product fails them specifically**, tied
to M1–M7 where it applies; the one change that would help them most; and the evidence
behind each claim.

**Then the part that makes it product management rather than decoration** — map personas
onto decisions already on the table:

- Does the delivery/assembly integration (named top strategic feature, 2026-07-22) serve a
  large persona, or a loud one?
- Search quality on semantically complex queries was excluded from December scope
  (2026-07-28). Which personas does that exclusion hurt, and how many are they?
- The ₪3–5k / ₪5–8k / ~₪8k cost-target spread (OQ-8) implies different message volumes per
  person. Which personas are we willing to serve less well?
- Which personas would even notice the +4–7s latency of Benjamin's ~87%-cheaper PoC (OQ-1)?
  This turns a stalled judgement call into a measurable one.

**Flagship analysis — settle the journey-vs-shortcut tension.** The Feb requirements map
records a live disagreement inside IKEA: does the agent shortcutting the store journey
suppress browsing and impulse purchase, or do customers want shortcuts with basket-building
happening at the end anyway? We can answer this empirically — compare basket size and
breadth between shortcut-style and browse-style visits. It is the single highest-value
analysis available from what we hold, and it is a question IKEA already knows it has.

**Deliverables:** persona set (Hebrew for IKEA, English internal); the demand-gap ranking
from Phase 1.4; the journey-vs-shortcut finding. All carrying the employee-population
caveat prominently.

---

## Phase 3 — The product view over the project (from 2026-08-18, continuing)

**Goal:** a standing product-axis view, so this does not decay into a one-off deck.

1. **A product axis beside the mechanism axis.** Publish
   `s3://…/customer_summary.json` from the trajectory table — same pattern as
   `cluster_summary.json`, same refresher shape, clustered on customer signals instead of
   failure mechanisms. Surface it as one new tab in `agent-management.html`, which is
   currently six engineering tabs and a journeys view. This is what requirement #8
   (demand and trends) actually asked for.
2. **Customer-intent labelling, done properly.** Requirement #5 wanted
   browsing / deliberating / buying. Today's `intent` field is answer-*style* on ~65% of
   turns, which is the wrong semantics. Derive the real thing from behaviour in the
   trajectory record (deterministic rules first, measured against a hand-labelled sample
   before any LLM classifier is considered).
3. **A monthly product review** in `whatsapp-agent/outputs/`: persona mix shift, demand
   gaps opened and closed, which personas received the worst product that month, and what
   the next month's priority is as a consequence. One page.
4. **The December evidence pack.** Working backwards from the decision gate: usage by
   persona, demand we could not serve, quality by persona, cost per persona, and a
   defensible recommendation on national rollout. Built incrementally from the monthly
   reviews, not written in December.

---

## Cost envelope

Deliberately small, because the project's core problem is cost.

| Phase | Effort | Runtime cost |
|---|---|---|
| 0 | ~1 dev-day | ~0 — snapshot puts + additive fields |
| 1 | ~4 analyst-days | S3 GETs + targeted queries; no new scans; no LLM |
| 2 | ~4 analyst-days | LLM on samples only — tens of conversations, not the corpus |
| 3 | ~2 dev-days to stand up, ~0.5 day/month | One more small refresher on the existing rail |

Roughly **10 days of work, front-loaded**, with negligible added run-rate. Deliberately no
new infrastructure, no re-architecture, and no dependency on Benjamin's PoC.

## Explicitly out of scope

Purchase linking (Phase 3 vision, needs IKEA systems we do not have); demographic personas
(no data, and inventing them would be fabrication); anything requiring an external AI
provider (OQ-2 unresolved); any eval run; any re-architecture; and any change to the agent's
customer-facing behaviour — this workstream observes, it does not touch the product.

## Decisions needed

| # | Decision | Who |
|---|---|---|
| D-1 | Does P0-1 (reset snapshot) ship before 08-02, or wait until after the release? | Shai + Niv |
| D-2 | Who does the analysis? It is ~8 analyst-days in a team with a single developer, Tali out two weeks from 08-02, Niv out in September | Shai |
| D-3 | Is this named as in-scope work (leaning on the Feb requirements-map lineage) or as new priced scope at the August meeting? | Shai + Hai |
| D-4 | Do we tell IKEA that requirements #5 and #8 were presented as in-bot and are open — and if so, before or at the August meeting? | Shai + Hai |
| D-5 | Does the ToU users accept cover behavioural analysis and profiling? Needs a written answer from IKEA before profiling begins | Shai → IKEA |
| D-6 | Is a customer cohort (Netanya, per the December single-branch scope) separated early enough to build *customer* personas rather than only employee ones? | Shai + Avi/Shuki |

## Risks

| # | Risk | Mitigation |
|---|---|---|
| PR-1 | Employee personas get read as customer personas — the worst outcome, because it makes a confident wrong case at the December gate | Caveat on the front page of every deliverable; separate a customer cohort as early as D-6 allows |
| PR-2 | Phase 0 destabilises the 08-02 release | Recommend P0-1 only, gated on Niv's review; defer the rest |
| PR-3 | Reads as an analytics project competing with the cost and stability work | Held to ~10 days, no new run-rate, and every persona mapped to a decision already on the table |
| PR-4 | Volume stays too thin to cluster meaningfully | Phase 2 is gated on the Phase 1 data-quality note; if it is thin, publish the demand-gap ranking (which works at any volume) and defer personas |
| PR-5 | D-5 comes back negative and profiling cannot proceed | Ask now, in Phase 0, not after 8 days of work |
| PR-6 | Sole-developer bottleneck (R1) swallows even 1 dev-day | Phase 1 and 2 need no developer time — only read credentials |

## What good looks like

By the August commercial meeting: a ranked demand-gap list and a first persona cut, giving
the scope conversation an evidence base instead of a cost apology.

By December: the rollout recommendation is argued on who uses this, what they need, and what
we could not serve — with latency and cost as supporting detail rather than the whole story.
