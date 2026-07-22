# IKEA Sync — 2026-07-21 (Shai onboarding)

- Recording: https://fathom.video/share/no5sKPaKxQvnnt2aop2Ro7xZik4Bdpht
- Attendees: Shai Amir, Arnon Meltser

## Purpose

Onboard Shai as the new owner of the IKEA account and hand off context from
Arnon, who has been running it solo with no real bandwidth.

## Key points

- Project kicked off end of Feb 2026 (~5 months in).
- Product: WhatsApp personal shopping agent — search, recommendations,
  in-store navigation, favorites basket; future upsell (checkout,
  cross/upsell, personalization).
- Pilot: ~1,000 IKEA employees, originally meant to launch during IKEA's
  sale period, pushed to end of July for reasons on IKEA's side.
- Cost: ~₪0.10/message → ~₪50k/mo at projected ~500k msgs/mo. Target ~₪2k/mo
  (~25x reduction). This is the top blocker to calling the project "done."
- Quality: much improved vs. a month ago; rare crashes/wrong answers remain.
- Latency: ~8s average, spikes to 25s. One known cause: a bug causing 5
  model calls per message — fixing it helps both latency and cost.
- No real stress testing yet; not expected to be a problem at ~1,000-2,000
  users, needs revisiting as usage grows toward Sep/Oct.
- Cost reduction levers discussed: implicit caching (shared session memory
  across users on the same serverless instance), explicit caching
  (pre-defined answers for static/service questions only), cheaper
  closed-source models (10x-100x), or self-hosted open-source models on
  rented GPUs (fixed hourly cost, decouples cost from message volume —
  ballpark ~$100-120/day for a right-sized small-model cluster).
- Team is currently a "one-man show" (Niv, junior dev) — a major risk.
  Tali (product-focused, more senior as a dev than Niv but not writing
  code) needs a decision: ramp up as real engineering redundancy, or the
  team doesn't need two product people. She may also be recruited
  elsewhere, so this is time-sensitive.
- Client stakeholders have different priorities: Shuki (tech lead) cares
  most about quality/service, secondarily about the AI/tech itself;
  merchandising/logistics cares about pricing features; sales cares about
  upsell ROI. IKEA has large budget/ambition long-term but the immediate
  ask is proving the current product works and is affordable.
- IKEA has not paid Moveo for ~5 months of work — two people full-time at a
  loss. Getting paid (via Elad/Eldar) is an active, separate workstream.
- Daily IKEA status sync at 08:30 — Shai to join starting 2026-07-22, Arnon
  will introduce him.

## Action items

- [ ] Define IKEA work plan: cost, quality, latency targets + owners (Shai)
- [ ] Resolve team structure: confirm/change Tali's role; add a senior dev
      for redundancy against Niv being a single point of failure (Shai)
- [ ] Join IKEA daily status call, 2026-07-22 08:30 — Arnon to introduce
      Shai (Shai)
- [ ] Push to secure payment for outstanding ~5 months of work, with
      Elad/Eldar (Shai, ongoing)
