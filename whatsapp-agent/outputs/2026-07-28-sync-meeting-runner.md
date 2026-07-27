# Ikea sync internal — meeting runner

**Tue 28.07.26, 10:00 · 30 minutes**
**Room:** David Mintz, Elad Kobi, Hai Morgenstern, Arnon Meltser
**Agenda as circulated:** what's been offered to the customer by Elad/Arnon, and what is the best
approach for next steps
**Deck:** `2026-07-28-path-to-customers-deck.html` · **Read-ahead:** `2026-07-28-internal-position-path-to-customers.md`

---

## The one thing to leave with

Everyone in this room says the same sentence to IKEA from Wednesday onwards:

> **December is a decision gate, not a launch date. What we bring the CEO is a working customer
> pilot at one branch, plus data.**

If that lands and nothing else does, the meeting worked. Everything below is in service of it.

---

## Timing

Twelve minutes of me, eighteen of them. Do not run the deck long — the decisions are the deliverable.

| Min | Slides | What I'm doing |
|---|---|---|
| 0–2 | 1–2 | Frame + where we are. Lead with the product being good and the cost win being ours. |
| 2–5 | 3–4 | Promised vs. real, then the reframe. **Slow down on slide 4.** |
| 5–9 | 5–6 | The five gates, then the eight customer differences. Point, don't read. |
| 9–12 | 7–8 | Retainer line and the two commercial models. Present both; give my view only if asked. |
| 12–14 | 9–10 | Unknowns, then read the five decisions out loud. |
| 14–28 | — | Discussion. Capture answers in the table below as they land. |
| 28–30 | 11 | Confirm the week and the Wednesday posture. |

---

## Opening line

> "We're four days from putting this in front of 1,500 employees and we've been unpaid for five
> months. I don't want to spend today on either of those separately — I want us to leave saying the
> same thing to IKEA about what happens *after* 2/8. I've got twelve minutes and five decisions."

---

## The five decisions — capture here

| # | Decision | My recommendation | Outcome | Owner |
|---|---|---|---|---|
| 1 | Retainer definition of done — agreed as drafted, or amended? | Agree as drafted. Inside: maintenance, bug fixes, cost optimisation, model-cost monitoring, catalogue/stock upkeep. Everything else priced. | | |
| 2 | Which commercial model do we open with? | Fixed-scope "Phase 2 — Go Public". You can't open an open-ended billing conversation with a client who hasn't paid in five months. | | |
| 3 | Who staffs 24/7 from Sun 02.08? | Two named people on a published rota. Taly is out that week, so this cannot be assumed. | | |
| 4 | CISO + DPO as one bundled session? | Yes — one meeting unblocks fraud detection *and* the customer phase. | | |
| 5 | Who owns the arrears conversation, before or after the scope reset? | Same conversation: scope first, arrears as the natural consequence. Elad/Eldar to run it. | | |

**Minimum viable outcome:** 1, 2 and 3 answered. 4 and 5 can be assigned rather than resolved.

---

## Likely pushback, and the answer

**Hai — "Finish the committed scope first, then propose improvements off a substantial sample."**
Agree with it, then supply the missing half: the committed scope has no SLA, latency or concurrency
figure in it, so "finished" is currently undefinable. G2 *is* his substantial sample, turned from a
hope into a measurement plan. I'm not proposing improvements ahead of it — I'm proposing we write
down the finish line before December so IKEA doesn't write it for us.

**Elad / Arnon — "We've already offered X to the customer."**
This is the actual agenda item, so ask it directly and early rather than defending against it: what
has been said out loud about a public launch, about capacity, and about what the retainer covers?
Anything already promised gets added to the G3 list rather than argued with. What I need is that
nothing *new* gets offered before the DoD exists.

**David — "Why postpone Wednesday?"**
Because walking into a client meeting with an unpaid invoice, an undefined retainer and a
future-ideas deck is how we end up giving away the eight G3 items for free. One week costs nothing;
the alternative sets the anchor for the whole customer phase.

**Anyone — "What capacity can we commit to?"**
There is no number, and we do not invent one. The known bottleneck is Lambda's 1000-concurrency
limit; no load test has ever run. The answer to IKEA is "after the load test," which is itself
priced work.

**Anyone — "Isn't a one-branch pilot a downgrade from what we promised?"**
It's a stronger artefact for a CEO review than a national rollout we can't evidence — and it bounds
Meta fees, PII exposure and the concurrency ceiling simultaneously. Netanya visit is already planned.

---

## Do not say in this room

- Any SLA, latency or concurrency commitment. None exists in the signed documents.
- Any capacity number ahead of the load test.
- Anything that implies proactive messaging to customers or employees who haven't written first —
  Efrat has ruled on it and we've committed to it in writing.
- In-chat payment. It contradicts IKEA's in-store model; stop offering it until they ask.

---

## Immediately after

1. Circulate the retainer DoD for sign-off the same day — while the agreement is fresh.
2. Send the delta list for pricing: re-architecture, load test, automated QA tooling, dedicated
   24/7 staffing, fraud detection, the eight G3 items.
3. Tell the client-facing thread that Wednesday is moving, before anyone confirms it.
4. Publish the 2/8 support rota to the team.
5. Ask Arnon for DynamoDB analytics access — G2 doesn't start without it.

---

_Grounded in: quote 29.01.26 · work plan (IKEA Smart Agent) · SOW · status & roadmap deck 13.07 ·
employee satisfaction survey, 30 of 104, 20.07 · Efrat Zigler Gagatsis 20.07 · internal prep 27.07 ·
Arnon roadmap conversation 27.07 · PoC handover and Hai's response 27.07 · status sync 22.07 ·
Trello "production (Scale)"._
