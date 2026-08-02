# Cost & scale grounding — what the decks should say

_Date: 2026-08-02 · Owner: Shai · For: the C-level review (Arnon, David; then IKEA)_

_Companion: `../context/research/2026-08-02-ga-readiness-external-verification.md` (source verdicts and confidence). Decks in scope: `ikea-road-to-december`, `New three-slide deck`, `Work plan deck: retainer focus`._

---

## 0. The one-paragraph version

We have been optimizing the wrong cost line. The LLM bill everyone is reacting to — ₪48k/month at
national volume — is real but is a *national-rollout* problem that December does not trigger. The
cost that actually threatens December is **Meta's**: from **1 October 2026** every reply the agent
sends inside the 24-hour window stops being free and starts billing at Israel's utility rate, with
no volume discount. On plausible assumptions that fee is **10–25× our entire LLM cost** at pilot
volume. Sixteen days later, on 16 October, the Gemini 2.5 family reaches its earliest retirement
date and the successor tier costs 3–10× more per token. Both land inside the window where the plan
currently says "cost re-architecture lands." Neither is in any deck.

---

## 1. Fix the internal numbers first

Before adding anything external, three of our own figures don't survive contact with a calculator.
A CTO who divides one slide by another finds these in about ninety seconds.

### 1.1 The ₪0.10/message figure is wrong by 100×

`PROJECT-STATUS.md` R2 reads: *"Cost at ~₪0.10/message projects to ~₪50k/mo."* That is
arithmetically impossible — ₪0.10 × 48M messages is **₪4.8M/month**, not ₪50k.

The origin is a unit slip. Arnon's 2026-07-27 note says *"~0.1 **agorot** per message"* — that is
**₪0.001**, not ₪0.10. The PRD's own table uses ₪0.001/msg and reconciles correctly to ₪48k.

**Canonical figure: ~0.1 agorot (₪0.001) per message.** R2 has been corrected in this repo. The
"25× gap" framing carried in the prior chat summary inherits the same slip — the *ratio* ₪50k vs
₪2k is right, the per-message unit behind it was not.

### 1.2 "Per conversation" and "per message" are used interchangeably. They differ by ~37×

The decks lead with **$0.01 per conversation**. The cost model runs on **₪0.001 per message**.
At ≈₪3.7/$, $0.01/conversation = ₪0.037/conversation ⇒ **~37 messages per conversation**.

That may well be right, but it is nowhere stated. Right now a reader can divide the headline stat
by the model's unit and get a number that looks like a 37× error. **Every cost figure needs its
unit attached, and the messages-per-conversation ratio needs to appear once, explicitly.**

### 1.3 The volume model rests on an unmeasured assumption

Every tier in the PRD assumes **~80 messages per user per day**. That is very high for a shopping
agent, it is not measured, and it drives everything:

| Scenario | DAU | @80 msg/user/day | @20 | @8 |
|---|---:|---:|---:|---:|
| Employee release (live today) | 450 | 1.1M/mo | 0.3M/mo | 0.1M/mo |
| Netanya pilot (Dec) | 800 | 1.9M/mo | 0.5M/mo | 0.2M/mo |
| National (post-decision) | 20,000 | 48.0M/mo | 12.0M/mo | 4.8M/mo |

If real usage is 8–20 msgs/user/day, national volume is 4.8–12M/month and the LLM cost problem
shrinks by 4–10× on its own.

**The 1,500-employee release went live today.** Two weeks of traffic replaces this assumption with
a measured number. Do that before the cost model is presented as settled — it is the cheapest
credibility win available, and it is the same instrument that answers the peak-concurrency question
without needing anyone's industry benchmark.

---

## 2. The October cliff — the thing that isn't in any deck

### 2.1 What changes

From **1 October 2026**, Meta bills every business-sent reply inside the 24-hour customer service
window at the recipient country's utility/authentication rate. Today these are free. There is **no
volume discount** on service messages, and no exemption for AI vs human vs template. Inbound
customer messages remain free.

Our agent is almost purely inbound service replies. That is precisely the category moving from free
to paid — **seven weeks before the December pilot.**

### 2.2 What it costs

Billable volume = business-sent replies only, modelled at 50% of total message volume. The Israel
utility rate is **not yet confirmed** (see §4), so this is a sensitivity grid, not a forecast:

**Meta service-reply fees, ₪/month from 1 Oct 2026**

| Rate → | ₪0.02/reply | ₪0.05/reply | ₪0.10/reply |
|---|---:|---:|---:|
| **Netanya pilot** @80 msg/user/day | 19,200 | 48,000 | 96,000 |
| **Netanya pilot** @20 | 4,800 | 12,000 | 24,000 |
| **Netanya pilot** @8 | 1,920 | 4,800 | 9,600 |
| **National** @80 | 480,000 | 1,200,000 | 2,400,000 |
| **National** @20 | 120,000 | 300,000 | 600,000 |
| **National** @8 | 48,000 | 120,000 | 240,000 |

Set against our LLM/infra cost at ₪0.001/message:

| | LLM/infra | Meta fees @₪0.05 | Ratio |
|---|---:|---:|---:|
| Netanya pilot @20 msg/user/day | ₪480/mo | ₪12,000/mo | **25×** |
| National @20 msg/user/day | ₪12,000/mo | ₪300,000/mo | **25×** |

**Read the bottom line honestly: in every cell of that grid, the Meta fee exceeds the entire LLM
bill — usually by more than an order of magnitude.** The ₪48k figure that has driven months of
planning is roughly 4% of the real cost at national volume. Even the *pilot* — which the PRD
correctly shows is comfortably inside every cost target on LLM cost alone — moves outside every
target once Meta's fee lands.

### 2.3 Who pays it

Meta fees bill against **IKEA's WABA**, not ours. The PRD already flags this as unmodelled
(gate C3). Two consequences, and they point in opposite directions:

- **It is not our P&L.** This is not a ₪140k-style overrun. It does not worsen our commercial
  position directly.
- **It is our credibility.** If IKEA discovers in October that their WhatsApp bill went from ~zero
  to five or six figures a month and their agency didn't flag it, the December review is over
  before it starts. Surfacing it *now*, with a model and a mitigation, is the single strongest
  trust move available in August.

### 2.4 What reduces it

The fee is per business-sent message, so the lever is **message count, not token count** — a
different engineering problem from the one the team has been solving:

- **Consolidate replies.** Every "one moment…" / "here's what I found" / "anything else?" split into
  separate bubbles is now a separate charge. Fewer, denser messages.
- **WhatsApp Flows** to collect several inputs in one interaction instead of a back-and-forth.
- **Fast-path / FAQ deflection** already keeps ~30% of queries off the model — it now also keeps
  them off the *invoice*, which roughly doubles that track's value.
- **Click-to-WhatsApp entry** keeps its free 72-hour window — relevant if IKEA drives traffic from ads.

Note what this reprioritises: reply-count discipline was previously a UX nicety. From 1 October it
is the primary cost lever, and it is cheap to build compared to a re-architecture.

---

## 3. The second October event — Gemini

| Model | In $/1M | Out $/1M | vs 2.5 Flash | Status |
|---|---:|---:|---:|---|
| Gemini 2.5 Flash-Lite | 0.10 | 0.40 | 0.7× / 0.3× | Retires 2026-10-16 (earliest) |
| Gemini 2.5 Flash | 0.15 | 1.25 | — | Retires 2026-10-16 (earliest) |
| Gemini 3.5 Flash-Lite | 0.30 | 2.50 | 2.0× / 2.0× | Current gen |
| Gemini 3.5 Flash | 1.50 | 9.00 | **10× / 7.2×** | Current gen; cached input $0.15 |

The retirement date is the **earliest possible** shutdown, not a commitment; Google has said it will
confirm a final date once Gemini 3 is GA and give six months' notice. So the date is soft — **the
price direction is not.**

This kills the research report's central cost thesis. "Token prices are falling, so our unit cost
falls with them" is true for the market in general and **false for our migration path**, where the
forced move is 2–10× upward. Caching recovers input (cached input on 3.5 Flash = $0.15/1M, the same
as uncached 2.5 Flash) but does nothing for output, which is 7.2×.

**This makes Benjamin's PoC strategically central rather than optional.** It was parked on
2026-07-28 as out of base scope. Its two properties — vendor-agnostic via OpenRouter, ~87% cheaper
per message — are now exactly the hedge against a forced, inflationary migration on someone else's
timetable. The ~85% reduction the national tier needs and the ~87% the PoC delivers are the same
number; that is the bridge, and it is worth re-testing the "next stage" decision against this
evidence. Its two open business questions (data-protection sign-off, +4–7s latency) are unchanged
and both now sit on the critical path.

**Blocking unknown:** nothing in the repo records **which Gemini model we run today**. Until Niv
confirms it, none of the above converts into a per-message delta. One line in a config file.

---

## 4. What we still cannot answer, and who can

| Question | Owner | Why it blocks |
|---|---|---|
| Israel utility/auth per-message rate on Meta's rate card | **IKEA** (their WABA/BSP holds the invoice) | Turns §2.2's grid into one number. IKEA already has this. |
| Which Gemini model + current token mix | Niv | Turns §3's ladder into a per-message delta |
| Actual messages/user/day and peak-hour curve | Measure from the live employee release | Replaces the assumption under every volume tier |
| Does Meta Business Agent token pricing touch a self-hosted Cloud API agent? | BSP | Meta began billing its own agent platform 2026-08-01 at ~$2/1M tokens (~4–5¢/msg). Should not apply to us. Confirm, don't assume. |
| Real concurrency ceiling | Us (OQ-9) | No load test has ever run |

---

## 5. Changes to make to each deck

### `ikea-road-to-december` (the big one, for Arnon & David)

This deck is in good shape and its structure survives — the changes are additive plus one
correction.

1. **Add a slide between "The Gap" and "The Path": _The October cliff_.** Two dated events, the
   sensitivity grid, the mitigation list. This is the strongest slide in the deck because it is the
   one thing leadership cannot already know.
2. **Track 02 goal changes.** "Cost model at three volume tiers, including Meta conversation fees
   (Aug W3)" is now the deck's highest-value line, not a routine gap. Re-date it as pre-October and
   say explicitly that the Meta layer is the larger of the two.
3. **Retire the ₪0.10/message figure** wherever it appears. Canonical: ~0.1 agorot (₪0.001)/message.
4. **State the messages-per-conversation ratio once** so $0.01/conversation and ₪0.001/message
   reconcile on the page.
5. **Label the ~80 msgs/user/day assumption as an assumption**, with a date for replacing it from
   live employee data. Volunteering this is more credible than being caught on it.
6. **"Cost re-architecture (~85% target)"** — connect it explicitly to the Gemini migration, so it
   reads as a hedge against a dated external risk rather than an optimisation we'd like funded.
7. **The "what we need from you" slide gains one item for David:** escalate the Israel rate card to
   IKEA. It is the cheapest unblock on the list and only IKEA can do it.

### `New three-slide deck` (Taly's, for IKEA C-level — high-level trust-building)

The 2026-07-29 sync concluded this audience needs an overview, not detail. Keep that. Two edits:

- Slide 1 says **"~$0.01 per conversation, current volume."** Add the three words *"LLM and
  infrastructure only"*. Without them it reads as all-in, and it isn't — and it is about to be very
  much not.
- Slide 2's "COST & LATENCY — flat under growth" is now a promise we can't make without knowing
  Meta's rate. Soften to hold *our* layer flat, and name the platform layer as a separate item being
  modelled. One clause, and it protects us in December.

### `Work plan deck: retainer focus`

- Track 02's "Cost model at three volume tiers, including Meta conversation fees" is listed as OPEN.
  It should be the first thing closed — it now has a hard external deadline of 1 October.
- Consider whether reply-count optimisation belongs in Track 04 (Optimization & Scale) as a named
  item. It is new work, it is cheap, and it has the best cost-per-effort ratio of anything on the list.

### The GA-readiness research PDF and infographic

**Do not put either in front of IKEA in their current form.** Roughly a third of the report is not
usable as sourced fact, and the infographic's §7 Q&A describes capabilities we have not built
(circuit-breaker at 3.5s, on-prem NER PII layer, 1.5% block kill-switch, DPIA "finalized for DPO
sign-off") in the present tense. Against our own status — no live handoff, no automated eval, no
task-success metric, privacy sign-off outstanding — that is claiming capability we don't have.
Full verdict list in the verification file.

What is worth salvaging: the Meta platform mechanics (throughput tiers, quality rating, messaging
limits), Amendment 13 obligations, and the RAND finding that ~77–80% of AI project failures are
organisational rather than technical — which is the best external support we have for the "four of
eight gaps are blocked on IKEA" argument.

---

## 6. The story for the room

Five beats. The order matters — the credibility is built before the ask.

1. **We run a healthy production system.** 1,500 staff, 25 tools, 26 alarms, cost reconciled to
   invoice, every trace classified. Our own data, all verifiable.
2. **We found our own error before you did.** The ₪0.10/message figure was a unit slip; the real
   number is 100× smaller. Correcting it publicly is what buys the right to be believed on the next
   three beats.
3. **The cost problem is real but mis-located.** Our LLM cost at pilot volume is ~₪500–2,000/month —
   inside every target. The ₪48k number is a national-volume projection, and national volume is
   what December *decides*, not what December *does*.
4. **The actual threat is external and dated.** 1 October, Meta starts charging for the replies that
   are free today. 16 October, our model tier reaches its earliest retirement and its successor
   costs more. Both land inside the plan's cost-work window. Here is the sensitivity grid; here is
   the one number we need from IKEA to close it.
5. **The ask.** Confirm the Israel rate card, decide the four critical-path items, and re-open the
   vendor-agnostic re-architecture — not as a cost optimisation, as insurance against a migration
   we do not control the timing of.

The strongest thing about this version is that beats 2 and 4 are both things we volunteered. An
adversarial review is looking for what you're hiding; the fastest way through it is to have already
said it.
