# Customer Status — IKEA

_Customer-level dashboard for the Moveo ↔ IKEA relationship. This is the account view: health, commercial state, and what's moving across projects. It **links** to each project's `PROJECT-STATUS.md` rather than restating execution detail (which would drift). For the live cross-project rollup, run `pm-brief projects_root=<path to this customer repo>`._

_This file is also the **canonical marker that this folder is a customer root** — `pm-brief` keys off it to descend into the customer's projects. Don't rename it._

_Last updated: 2026-07-28_

---

## Account health

**Status:** active — live engagement, 1,500-employee release on Sun 2026-08-02, and a December review reframed internally as a **decision gate rather than a launch date** (one branch live with real customers plus data, not national coverage).
**Commercial:** fixed-price project running at a loss and ~5 months unpaid. Finishing is estimated at ~₪140k of further cost (worse case ~₪200k); the intent is to recover it by selling new scope at a second-half-of-August meeting, not by invoicing the overrun. No SLA, latency, or concurrency figure exists in the SOW or quote — the bar has to be authored before it can be claimed as met.
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

1. Run the commercial meeting with IKEA in the second half of August (Efrat abroad, Avi after her) — current state, new scope, and price. Not a status review and not a future-ideas deck. This is the vehicle for recovering the ~₪140k gap.
2. Agree the retainer definition of done internally, then put it to IKEA. While it stays undefined, every new client request lands inside it by default.
3. Secure payment from IKEA for ~5 months of outstanding work (via Elad/Eldar) — attached to the scope reset rather than run separately: scope first, arrears as the consequence.
4. Resolve the team single-point-of-failure risk. Tali is staying and taking technical tasks, which is the redundancy answer, but it is a ramp not a switch — confirm it turns into real cover before scaling further with IKEA.
5. Run the post-mortem on why a fixed-price project ran ~4 months past plan and is still unfinished.
6. Explore the fraud-detection workstream as a potential second project. The base is ready and it needs a coordinated CISO conversation; note a ~$250/month environment has been billing unused for ~3 months.
7. Join the daily 08:30 IKEA status sync (Shai, started 2026-07-22).
8. Grow the account toward the team's ambition of ~₪150k/month across ~3 people, which means more IKEA projects, not just more scope on this one.

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
- 2026-07-28: Internal sync — December reframed as a decision gate rather than a launch date; no SLA found committed anywhere in the SOW or quote, so we author the bar ourselves; ~₪140k (worse case ~₪200k) to finish, to be recovered by selling new scope at a second-half-of-August commercial meeting; post-mortem requested on the ~4-month slip. See `./context/meetings/2026-07-28-internal-ikea-sync-commercial.md` (commercial) and `whatsapp-agent/context/meetings/2026-07-28-internal-ikea-sync.md` (product).
