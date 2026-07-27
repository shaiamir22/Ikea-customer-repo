# Customer Status — IKEA

_Customer-level dashboard for the Moveo ↔ IKEA relationship. This is the account view: health, commercial state, and what's moving across projects. It **links** to each project's `PROJECT-STATUS.md` rather than restating execution detail (which would drift). For the live cross-project rollup, run `pm-brief projects_root=<path to this customer repo>`._

_This file is also the **canonical marker that this folder is a customer root** — `pm-brief` keys off it to descend into the customer's projects. Don't rename it._

_Last updated: 2026-07-22_

---

## Account health

**Status:** active — live engagement accelerating toward the Aug 1 employee pilot and a Dec public-launch decision.
**Commercial:** 5 months of work delivered, unpaid to date; pushing to secure payment while development continues ahead of the Aug 1 employee rollout and December public-launch decision.
**Relationship owners:** Shai Amir owns execution and the client relationship (took over 2026-07-21). Arnon Meltser was the prior de facto client-facing lead (near-zero bandwidth, handed off to Shai). Exec sponsor on IKEA's side not yet named — the CEO is expected to do a passive review ahead of the December decision.

---

## Projects

| Project | Stage | Detail | Monday |
|---|---|---|---|
| [whatsapp-agent](whatsapp-agent/PROJECT-STATUS.md) | Build / pre-launch | WhatsApp personal shopping agent for IKEA employees (phase 1) and, later, customers — search, recommendations, in-store navigation, favorites basket. | not configured |

_Each project's own `PROJECT-STATUS.md` is the source of truth for its execution status._

---

## Cross-project next steps

_Things that belong to the relationship, not to a single project (project-specific next steps live in each project's `PROJECT-STATUS.md`)._

1. Secure payment from IKEA for ~5 months of outstanding work (via Elad/Eldar) — separate workstream from the technical work, but a blocker for how much further free work continues.
2. Resolve the team single-point-of-failure risk: confirm Tali's role (ramp up as real engineering redundancy, or step back) and/or hire a senior developer alongside Niv — non-negotiable before scaling further with IKEA.
3. Join the daily 08:30 IKEA status sync (Shai, started 2026-07-22).
4. Pin down with IKEA which improvements fall under the existing retainer vs. a new paid scope — and prioritize the paid candidates by development difficulty against business importance.
5. Explore the fraud-detection workstream as a potential second project. The base is ready; it needs a coordinated conversation with IKEA's CISO before anything starts.
6. Grow the account toward the team's ambition of ~₪150k/month across ~3 people, which means more IKEA projects, not just more scope on this one.

---

## Customer state pointers

- **monday_item_url:** not configured
- **gdrive_folder_id:** not configured
- **shared Monday board:** not configured
- **github_repo:** https://github.com/shaiamir22/ikea-customer-repo

---

## Recent customer-level events

- 2026-07-21: Onboarding sync — Arnon handed the account to Shai. Cost crisis (~₪50k/mo → ~₪2k/mo target), quality/latency status, team risk, and unpaid invoices covered. See `./context/meetings/2026-07-21-ikea-sync-onboarding.md`.
- 2026-07-27: Arnon laid out how he sees the engagement continuing — retainer improvements, possible paid scope, the ~₪150k/mo ambition, and fraud detection as a client-gated second workstream. Separately, Benjamin handed over a PoC (~87% cheaper per message, any-language, vendor-agnostic) and Hai directed that it wait for the next stage rather than ship into the pilot. See `whatsapp-agent/context/`.
- 2026-07-22: IKEA daily status sync — fallback-model fix needed for Gemini-outage crashes, Aug 1 employee rollout confirmed, Dec CEO review gates public launch, delivery/assembly integration flagged as top feature priority. See `./context/meetings/2026-07-22-ikea-status-sync.md`.
