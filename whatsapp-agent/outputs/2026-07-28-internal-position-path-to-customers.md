# IKEA — internal position: our path to end customers

**For:** David Mintz, Elad Kobi, Hai Morgenstern, Arnon Meltser
**From:** Shai Amir
**For the meeting:** Ikea sync internal, Tue 28/7, 10:00 — "what's been offered to the customer and what is the best approach for next steps"
**Read time:** 5 minutes

---

## 1. Where we are

The agent is live and good. 25,480 products in the live catalogue, 122K stock records across 5
branches, 24 dedicated tools, ~30% of queries answered on a fast path with no LLM call, ~25
automatic validation checks on every answer. Average response 9.3s. Cost per conversation is down
from **$0.03 to $0.01** — that reduction is ours, delivered under the retainer, and it is the
strongest evidence we have that the retainer produces value.

The broad employee release — **1,500 employees, moved from Thu 30/7 to Sun 2/8** — is the last
gate before anyone at IKEA starts asking the real question: when do actual customers get this.
December is when their CEO reviews the agent to decide on a public launch, with investment from
the American owners riding on it.

We are entering that conversation with three unresolved things: **five months unpaid**, a
**retainer whose scope nobody has written down**, and **one person writing code**.

On the last of those: Taly is staying on the team, and Arnon wants her taking technical tasks. That
is the redundancy answer, and it removes the risk we were most exposed to. It is a ramp rather than
a switch, so it does not change who is on call for 2/8 — but by the customer phase it should mean
Niv is no longer a single point of failure.

---

## 2. What was promised vs. where we are

This is the part we should walk in already aligned on, because IKEA can reconstruct it themselves.

| | |
|---|---|
| **Signed** | Fixed project **₪109,546 + VAT**, plus **₪10,000/mo + VAT** comprehensive support. Quote valid from 29.01.26. Anything outside the listed scope is priced separately — that clause is in the quote. |
| **Work plan promised** | 3 Feb – 13 Apr, 10 weeks. Weeks 5-6: internal employee launch. Weeks 9-10: *"peak loads of tens of thousands of concurrent users, gradual 10% rollout, then full launch."* |
| **Reality** | It is late July. The employee launch happens 2/8 — roughly 15 weeks past plan. A public launch was on paper for mid-April. |
| **SLA** | **There is no SLA, latency target, or concurrency number anywhere in the SOW or the quote.** I checked both documents end to end. |

Two things follow. First, the slip is not one-sided — the pilot was pushed by IKEA more than once,
and the sale period moved it again — but we should not walk in as though mid-April never happened.
Second, when Hai says "finish the project to the SLA / concurrent-session level committed in the
current agreement scope," **that level does not exist in writing**. We have to define it before we
can claim to have met it, and we should define it ourselves rather than let IKEA define it for us
in December.

---

## 3. What the ₪10k retainer covers — proposed definition of done

Right now it is undefined, which means every new request lands inside it by default. Proposed
boundary, to agree today:

**Inside the retainer:** routine maintenance; bug fixes; ongoing cost optimisation; monitoring of
model costs; keeping the catalogue/stock integration current.

**Outside the retainer — priced separately:**

| Item | Why it is outside |
|---|---|
| Benjamin's cost-optimisation re-architecture | New architecture, not maintenance. ~87% cheaper/message, any-language, vendor-agnostic. Built, 2,474 tests passing, off by default. |
| Load / stress testing | Expensive to run. Never been done. Needed for any capacity claim. |
| Automated QA & monitoring tooling | Niv reviewed **209 conversations by hand** recently. That does not survive 1,500 users, let alone customers. |
| Dedicated 24/7 support staffing | Two people, not a side duty. |
| Fraud detection | Separate workstream. Base is ready; gated on a CISO conversation. |
| Everything in §5 (customer readiness) | New capability, not upkeep. |

Selling these as discrete projects is also the honest answer to "how do we get paid" — each one has
a defensible standalone value story, which the arrears conversation currently lacks.

---

## 4. The five gates from employees to customers

The central reframe, and the thing I would like us to agree to say with one voice:

> **December is a decision gate, not a launch date.** What we bring their CEO is a *working
> customer pilot at one branch, plus data* — not a promise of national coverage. That is stronger
> evidence, and it is survivable with the team we actually have.

| Gate | When | What has to be true |
|---|---|---|
| **G0 — Employee release lands** | now → Sun 2/8 | Fallback model routing confirmed live (Gemini outages crashed the agent on 21/7 and stopped Efrat's testing). 24/7 support staffed in writing — two people. Taly is on the team and ramping onto technical work at Arnon's direction, but she is unavailable during launch week itself, so the 2/8 rota has to be named explicitly rather than assumed. Efrat's no-proactive-messaging rule enforced as a technical guard, not a promise. Onboarding QR/link updated; Avi's short video delivered for the internal publication after the sale ends 30/7. |
| **G1 — Retainer DoD + commercial reset** | this week | §3 agreed internally, then with IKEA. Delta list priced. Arrears conversation attached to it via Elad/Eldar. Postpone the Wednesday client meeting until we are aligned; no future-ideas deck there. |
| **G2 — Evidence from 1,500 employees** | Aug → Oct | This is Hai's "substantial sample", turned into a measurement plan: the larger survey (ratings + free text); conversation analytics out of DynamoDB (I need access via Arnon); an eval set built from real observed failures; latency and cost curves at real volume; a written quality bar with a pass mark. |
| **G3 — Customer-readiness gates** | Sep → Nov | The eight items in §5, each pass/fail. |
| **G4 — Staged customer launch** | Dec decision → Q1 | Netanya branch pilot (site visit already planned) with QR entry at the entrance, self-serve area and checkout → geographic widening → national. Bounds Meta cost, PII exposure and the concurrency ceiling at the same time. |

---

## 5. What is genuinely different about customers

Not a wish list — these are the things that break if we go from employees to consumers without
addressing them.

1. **Consent and entry point.** Employees are a known allowlist. Customers arrive cold. We need a
   QR/link entry, a privacy notice on first contact, IKEA's WABA with approved Meta template
   categories, and a written proactive-messaging policy. Note this cuts against push notifications
   — the 13/7 deck calls push the easiest follow-on project, and Efrat has already told us
   proactive messaging to non-users is forbidden. That constraint gets *stricter* for consumers.
2. **Privacy and security.** Consumer PII at scale: privacy notice, data-processing appendix,
   retention policy (today: 30-day cart, conversation logs in DynamoDB), and a ruling on whether
   any external AI provider may see customer messages. **Bundle the DPO/legal review with the CISO
   conversation we already need for fraud detection — one meeting, two unblocks.**
3. **Unit economics — two cost layers, only one modelled.** LLM/infra is $0.01/conversation. **Meta
   conversation fees on IKEA's WABA are unmodelled and land on IKEA.** We should produce the all-in
   number at three volume tiers before anyone commits publicly. Being the ones who raise this is
   worth more than being asked about it.
4. **Capacity.** The bottleneck is **AWS Lambda's 1000-concurrency limit** (~few-thousand concurrent
   chatters). Gemini/AWS reportedly support ~3,000 concurrent messages. **No load test has ever
   run.** We cannot state a capacity number until one does.
5. **Quality bar.** Customers don't tolerate what employees tolerate, and they screenshot failures.
   Photo→SKU recognition is the known weak point — five separate survey respondents named it, and
   one wrote that the agent is *"still far from usable for a customer."* Needs the eval set with a
   pass mark, plus automated QA replacing manual conversation review.
6. **Escalation.** A human hand-off into IKEA's contact centre **with conversation context**. This
   was raised by their marketing side in June and deferred. Without it, a customer launch moves
   load *onto* the call centre instead of relieving it — which contradicts the entire business case
   we are selling.
7. **Content coverage.** Customers ask about order status, delivery, assembly, returns, credits.
   That is the delivery/assembly integration (already their top priority) plus the post-purchase
   data they declined in June. Without it the agent deflects the highest-volume customer intents.
8. **Language.** Hebrew is primary and is the one language Benjamin's PoC has **not** been tested
   in. Arabic and French were requested and are not built. Customer traffic includes Arabic speakers.

---

## 6. Two commercial models — pick one to open with

| | Fixed-scope "Phase 2 — Go Public" | T&M partnership |
|---|---|---|
| **Shape** | One priced project, closed scope, defined success metrics, gated on the December review | Bill time and materials for the dynamic work |
| **For** | Cleanest to invoice against given five months unpaid. Keeps the ₪10k retainer strictly maintenance. Forces IKEA to define what "public launch" means. | No renegotiation per feature. Matches how the work actually behaves. Was the direction the 22/7 refinement session leaned toward. |
| **Against** | Scope negotiation takes time we may not have before December. | Weakest leverage on the arrears — open-ended billing to a client who hasn't paid is a hard sell internally. Needs a monthly cap. |

Either way: **retainer DoD in writing, and the §5 items are paid scope, not retainer.** That part
should not be negotiable regardless of which model we open with.

---

## 7. What nobody knows yet

Stating these openly is the point — none of them should be answered with a guess in front of IKEA.

- What SLA the agreement commits to. **Nothing.** It has to be written before it can be met.
- Whose WABA the customer phase runs on, and who pays Meta fees at customer volume.
- Whether IKEA will open order/delivery APIs, having declined the receipts integration in June.
- What the CISO/DPO will permit on external AI providers and on data retention.
- The real concurrency ceiling and the real cost per conversation at customer volume — both
  untested.
- How quickly Taly's technical ramp turns into real redundancy. She is staying and Arnon wants her
  on technical tasks, so *whether* we get a second pair of hands is settled. What is still open is
  whether she is genuinely covering for Niv by the customer phase, or still ramping — and that is
  a scheduling question we can answer ourselves rather than an unknown to live with.
- Whether IKEA wants a service channel or a commerce surface. In-chat payment contradicts their
  in-store model; we should stop offering it until they say otherwise.

Two decisions are already open on **their** side and have been for a while: data-protection
sign-off to send real customer messages to an external AI provider, and whether +4-7s latency is
acceptable in exchange for the ~87% cost saving.

---

## 8. Decisions I need from this meeting

1. **Retainer DoD** (§3) — agreed as written, or amended?
2. **Which commercial model do we open with** (§6) — fixed-scope Phase 2, or T&M with a cap?
3. **Who staffs 24/7 support from Sun 2/8?** Niv alone is not a plan, and Taly is out that specific
   week. Related, and worth settling in the same breath: what is the ramp plan for Taly's technical
   tasks, who mentors it, and what does she own by the customer phase?
4. **Do we book the CISO + DPO conversation as one bundled session** covering fraud detection and
   customer-phase privacy together?
5. **Who owns the arrears conversation with IKEA, and does it go before or after the scope reset?**
   My view: same conversation, scope first, arrears as the natural consequence.

---

_Sources: quote `Ikea - הצעת מחיר` (29.01.26); `תוכנית עבודה_ IKEA Smart Agent`; SOW; status &
roadmap deck 13/7; employee satisfaction survey (30 of 104 responses, 20/7); Efrat Zigler Gagatsis
email 20/7; internal prep meeting Niv/Taly/Shai 27/7; Arnon roadmap conversation 27/7; Benjamin PoC
handover + Hai's response 27/7; IKEA daily status sync 22/7; idea refinement session 22/7; Trello
IKEA board, card "production (Scale)"._
