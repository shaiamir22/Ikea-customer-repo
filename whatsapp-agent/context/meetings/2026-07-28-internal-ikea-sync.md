# Internal IKEA sync — 2026-07-28 (product plan to December)

- Attendees: Shai Amir, Arnon Meltser, Hai Morgenstern, David Mintz, Elad Kobi
- Source: Hebrew recording — transcript plus auto-summary. The auto-summary attributes nearly every line to a single speaker and is unreliable on attribution; points below are recorded as room decisions unless the transcript names someone unambiguously.
- Paper taken into the room: `../../outputs/2026-07-28-internal-position-path-to-customers.md`
- Commercial half of this meeting: `../../../context/meetings/2026-07-28-internal-ikea-sync-commercial.md`

## Purpose

Turn "the product isn't ready" into a costed, dated plan the account lead can run with — what the initial product is, what it must hit on cost, latency and load, and who is needed to get there.

## Key points

- **Scope for December is one branch, not the country.** The target is a single branch (Netanya) live with real end customers under a tighter SLA, deliberately narrowed so it is achievable with the team we actually have. National rollout is what December *decides*, not what December ships.
- **The SLA has to be authored, not looked up.** No latency, accuracy, or concurrency figure exists anywhere in the agreement, so defining the bar is now a product task rather than a lookup. Meanwhile the client believes the project is already in its SLA / bug-fix phase — a gap that has to be closed deliberately.
- **Load target: 20,000 daily users** — explicitly *daily*, not concurrent. The concurrent number is unknown and is to be derived by heuristic rather than waited for: roughly 10,000 people a day visit IKEA's site, assume a low-thousands share reach the bot, and a conversation runs 10–150 messages. Engineering was told to state its assumptions and proceed; the difference between 10k and 20k was called a factor of two, not an order of magnitude, and not worth stalling over.
- **Latency is near the floor of the current implementation.** 8–9s average today. Room consensus was *not* to fund latency work as its own line item — it improves as a by-product of the cost work, and going materially below the current floor would mean rewriting the implementation (estimated at three months minimum). A product-side target number is still owed, with the reasoning behind it.
- **Cost is the actual blocker, not latency.** At the loads we committed to support, the current per-message price projects to roughly **₪50k/month**, which nobody will pay — the room's framing was that the product is simply not sellable until this comes down. Three different targets were named and none was settled:
  - ₪3,000–5,000/month — stated as what the client is willing to pay
  - ₪5,000–8,000/month — Shai's working range
  - ~₪8,000/month — stated as what the January presentation actually promised

  This needs to resolve to one figure before the work plan can be costed against it.
- **Benjamin's re-architecture is out of base scope.** Framed as a follow-on programme, not part of finishing the current product. About 60% cost reduction is already banked since project start; his plan is quoted as a further ~80% on top. Whether he is needed, and for how long, should fall out of the Sunday work plan rather than being decided ahead of it.
- **New requests must be named as out of scope when they arrive.** Data arrived from Shuki and Nathan for a feature that then entered development with no scope decision attached. The rule agreed: stop, say plainly that this is new scope, and price it — do not let it land inside the retainer by default.
- **The 1,500-employee release needs a formal rota, not goodwill.** Named on-call cover per day, written down; an explicit statement that normal working hours do not apply on release day; and a two-tier response policy — acknowledge fast ("received, we're on it"), with the actual fix allowed to take hours. Previous releases ran on improvisation and it showed.
- **Note the collision on Sunday 2026-08-02:** the work-plan review and the employee release currently land on the same day. Worth separating or explicitly staffing both.
- **Vacations bound the whole plan.** Tali is out for two weeks from Sunday, Niv is out in September, and Arnon is out shortly — **the plan has to close before Arnon leaves**, since he holds most of the technical context. Otherwise a month is lost.
- **Search quality is explicitly excluded** from the December single-branch scope. The semantically-complex-query problem ("ארונית קלה" should surface "כוורת") gets improved incrementally rather than gating the release.
- **Testing capacity is a known gap.** There is currently no way to load-test even the 1,500-employee release; the room's answer was to observe it live. Flagged as a missing skill on the team rather than resolved.

## Next steps

- **Shai:** own the product half of the work plan — what the initial product is, the cost target, the load definition, and the latency target — and bring it to Sunday's review.
- **Tali & Niv, with Arnon:** break the plan down technically. Sit with Arnon before he leaves and extract what he holds; the technical estimates are theirs to produce, not Shai's.
- **Leadership:** decide the single monthly cost target so the plan can be costed against a real number.
- **All:** review and approve the plan together on Sunday.

## Action items

- [ ] Deliver the work plan for Sunday 2026-08-02 review, covering four headings: what reaches definition of done; what it takes to hit the monthly cost target; what it takes to be crash-free at target load; and the headcount plus timeline. Format: a spreadsheet/Gantt of technical tasks broken to dev-days with estimates, sequencing, dependencies, and a recommendation on one developer or two. (Shai — product content; Tali & Niv — technical breakdown)
- [ ] Sit with Arnon to extract technical context before he goes on leave (Tali & Niv)
- [ ] Set up a standing Sunday one-hour rundown with Arnon — what gets done that week, technically, and by whom (Shai)
- [ ] Agree a single monthly cost target and replace the three competing figures (Shai, with Hai/David)
- [ ] Define the product-side latency target and the reasoning behind it (Shai)
- [ ] Write the named on-call rota for the 1,500-employee release, including that normal working hours don't apply on release day (Shai, with Arnon)
- [ ] Set the two-tier response policy for the release — fast acknowledgement, fix within hours — and communicate it to the team (Shai)
- [ ] Locate the eval set and confirm whether the lighter routed model passes quality checks (Niv / Arnon's team)
- [ ] Define concurrency by heuristic — messages per conversation, users per day, concurrent sessions — and state the assumptions rather than waiting for exact numbers (Tali & Niv)
