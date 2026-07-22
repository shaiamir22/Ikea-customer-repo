# IKEA Customer Repo

Context repo for Moveo's IKEA engagement. Use this file to get oriented before
working on anything related to this account.

## Project

Moveo is building a WhatsApp personal shopping agent for IKEA. Kicked off end
of February 2026. The agent lets customers/employees:
- Search for products in-store or from home
- Get recommendations and compare products
- Navigate the store, find where items are located
- Build a "favorites" basket
- (Future/upsell) checkout, cross-sell, personalized re-engagement (e.g.
  "you bought a toddler bed a year ago, here's a bed for a 3-year-old")

Two user layers: IKEA employees (in-store, phase 1) and end customers
(future).

## Status (as of 2026-07-21)

- Product is not yet complete.
- Pilot with ~1,000 IKEA employees scheduled for end of July 2026 (IKEA
  wanted it live during their sale period but delayed it to end-of-month for
  reasons on their side).
- Latency: ~8s average (down from worse), but spikes to 25s still happen.
  One known cause: a bug that called the model 5x for a single reply.
- Quality: more stable than a month ago, but rare crashes/wrong answers
  persist. Current usage is mostly internal testers (10 users/day, 30-200
  msgs/day); real signal starts once ~1,000 employees are live.
- No stress/load testing done yet against API rate limits — not expected to
  be an issue at 1,000-2,000 users but needs revisiting as usage scales
  toward Sep/Oct.

## The cost crisis (top priority)

- Current cost: ~₪0.10/message (LLM inference cost, on Gemini).
- At a projected ~500k messages/mo, that's **~₪50k/mo**.
- Target: **~₪2k/mo** — a ~25x (two orders of magnitude) reduction.
- This is the single blocking issue before the product is viable to sell.

Levers being considered:
1. **Caching**
   - *Implicit*: shared session memory across users on the same serverless
     instance (same "Lambda"-style server handling many users at once) —
     free repeat answers within that shared context window.
   - *Explicit*: pre-defined answers for static/service questions (e.g.
     store hours, prices of fixed items) — doesn't work for
     product-recommendation questions that depend on conversation context.
2. **Model optimization**
   - Currently on Gemini (expensive, closed-source).
   - Cheaper closed-source models: 10x-100x cheaper per message, same
     pay-per-message model, but introduces dependence on shared rate
     limits/bandwidth (a prior outage on Claude was caused by this).
   - Open-source models (e.g. Llama) self-hosted on rented GPUs: fixed
     hourly cost (~$2/hr per GPU, ballpark $100-120/day for a small
     cluster) instead of per-message cost. Cost becomes independent of
     message volume — the main structural fix for scaling to 20k+
     users/day. Tradeoff: takes on infra ops, and needs a smaller model
     since a full large-model cluster is enormous overkill (a small
     8-GPU cluster of top-tier cards can run $500k+ upfront/committed
     spend — not what's needed here).
3. **Latency/cost are coupled**: some of the latency issues (e.g. the 5x
   model-call bug) are also cost issues — fixing one often fixes both.

## Team

- **Niv** — sole developer. Junior. Currently a single point of failure
  ("one-man show"). Needs a senior developer added alongside him for
  redundancy — non-negotiable before scaling further with IKEA.
- **Tali** — product-focused, has more dev experience than Niv but isn't
  doing hands-on code work. Open question: either she ramps up as real
  redundancy for Niv, or there's no reason to keep two product-only people
  on a team this size. Time-sensitive — she's reportedly being pursued for
  another role elsewhere.
- Arnon (Meltser) has been the de facto client-facing lead but has had ~zero
  bandwidth for this account; Shai is now taking over that role.

## Client / stakeholders

- **Shuki** — tech lead on IKEA's side. Cares most about product quality and
  answer accuracy/service, with secondary interest in the AI/tech itself.
- **Merchandising & logistics dept** — interested in pricing-related
  features.
- **Service dept** — interested in service quality / answer accuracy.
- **Sales/logistics** — interested in ROI: upsell/cross-sell numbers.
- IKEA has effectively unlimited budget appetite and ambition for this
  product long-term, but the immediate blocker is proving the current
  product works and is affordable before expanding scope.
- Real usage signal so far is mostly internal test conversations, not real
  customer-style questions. The upcoming employee pilot is meant to
  generate genuine usage patterns (real product questions: origin, specs,
  compatibility) to design around.

## Financials (sensitive — internal only)

- IKEA has not paid Moveo for ~5 months of work. Two people have been
  full-time on this for ~5 months at a loss.
- Securing payment (via Elad/Eldar) is an active, urgent workstream,
  separate from the technical work but a blocker for how much further
  free work continues.

## Shai's mandate

1. Define a formal work plan across the three active workstreams — cost,
   quality, latency — with owners and targets.
2. Fix the team single-point-of-failure risk (Tali's role, and/or hire a
   senior developer).
3. Join the daily 08:30 IKEA status sync (started 2026-07-22).
4. Support getting Moveo paid for outstanding work.
5. Longer-term: use this account to unlock upsell (cross-sell recs,
   personalization, checkout) once cost/quality/latency are under control.

## Meeting notes

See `docs/meetings/` for raw sync notes, newest first.
