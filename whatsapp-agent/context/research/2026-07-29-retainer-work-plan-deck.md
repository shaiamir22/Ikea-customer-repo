# "Work plan deck: retainer focus" — Niv & Taly, 29 Jul 2026 (edited to 3 Aug)

- Source: Drive `Slides/Work plan deck: retainer focus` (Google Slides, 19 slides, English) plus an identical "Copy of". Read 2026-09-03. Referenced by `../../outputs/2026-08-02-cost-and-scale-grounding.md` but never digested.
- This is the technical half of the 08-02 work plan: what the ₪10k/month retainer covers, the bar it holds, a 60-day backlog, and what sits outside it.

## Framing

"The standing tech plan for a live production agent — and the growth tracks priced outside it." Retainer scope = maintenance & operations: monitoring, QA & bugs, maintenance, optimisation & scale at the margin. Headline facts: 1,500 staff served, 25,480 products, 122K stock records / 5 branches, **25 tools** in production.

Tags per line: LIVE (running today), ON-GOING (recurring monthly), OPEN (ours, not started), IKEA (waiting on client), plus IN FLIGHT.

## Six retainer tracks

| # | Track | Goal | Live today | Open / blocked |
|---|---|---|---|---|
| 01 | Reliability & availability (20%) | ≥99.5% availability, no outage >5 min, owned error budget | 26 CloudWatch alarms + SNS; DB self-heal, 4 GB headroom; **cross-endpoint Gemini failover in production**; keep-warm, fan-out breaker | Alarms into infrastructure-as-code; **named on-call rota with two-tier escalation** ("an org decision, not an engineering one") |
| 02 | Monitoring & cost watch (15%) | Drift caught on a dashboard before it is an incident or invoice | Cost reconciled to invoice; ops dashboard | **Cost model at three volume tiers incl. Meta fees** — OPEN (the 08-02 grounding says close this first; 1 Oct deadline) |
| 03 | QA & defect triage (25%) | Defects from real traffic, fixed at cause | Failure-cluster pipeline (every trace auto-classified); one-tap bad-answer reporting | Weekly cluster triage; golden-set regression before each release. Hand-sampled review stays until an automated eval exists — **the eval build is an upsell** |
| 04 | Maintenance & upkeep (15%) | Nothing degrades quietly | — | Index rebuilds, FAQ mining, quarterly dependency/credential/model-version reviews |
| 05 | Data & feed accuracy (10%) | Stock, price, restock answers correct | Header-based stock parse; schema-drift and stale-feed alarms | **SFTP → S3 cutover in flight**; **restock-date coverage ~14%** and out-of-stock verification widening — tagged IKEA |
| 06 | Quality watch & content (15%) | Answer quality holds and improves at the margin | — | Hebrew robustness (abbreviations, typos, slang); KB corrections across **26 categories, ~1,383 pages**; daily sampled review; fast-path/FAQ tuning to keep ~30% off the model |

Latency is explicitly **"a no-regression constraint, not an improvement goal — ~9.3 s against a 9 s p50 bar."**

## 60-day backlog (one-off tasks, dated)

| Track | Task | Output | Target |
|---|---|---|---|
| 01 | 26 alarms into infrastructure-as-code | alarms survive a stack recreate | Aug W1 |
| 03 | Start weekly cluster triage + regression ritual | weekly fix batch | Aug W1 |
| 01 | Fault-inject the Gemini failover; write up the 07-21 root cause | verified failover report | Aug W2 |
| 01 | Publish the on-call rota and two-tier escalation policy | runbook, named owners | Aug W2 |
| 02 | Alarm p50/p95 latency against 9 s / 15 s | latency alarm + panel | Aug W2 |
| 05 | Complete SFTP → S3 feed cutover, retire old path | feed on S3 | Aug W2 |
| 02 | Rebuild cost model at three tiers incl. Meta fees | cost sheet off the dashboard | Aug W3 |
| 04 | Schedule monthly search/KB index rebuild | automated job + log | Aug W3 |
| 03 | One-tap bad-answer reporting into the triage queue | feedback in production | Aug W4 |
| 06 | Hebrew robustness fix batch one, from top failure clusters | measured cluster drop | Sep W1 |

Cadence: daily alarm/cost/latency read; weekly cluster review + fix batch + feed health; **monthly index rebuild and a written report to IKEA** (availability, cost, latency, top clusters); quarterly dependency/model review and upsell re-cut. "Escalation path and response-time commitments — to confirm with IKEA."

## The service bar the deck proposes

| Dimension | Bar | Evidence |
|---|---|---|
| Availability | 99.5% monthly, no outage >5 min | alarm history |
| Latency | **p50 ≤ 9 s, p95 ≤ 15 s, no regression** | continuous measurement |
| Cost | **~$0.01 per conversation at current volume** | dashboard, invoice-reconciled |
| Failover | automatic, within one request | fault injection |
| Data freshness | stock feeds current, drift alarmed within the hour | feed alarms |
| Reporting | one written monthly report against every line | monthly pack |

"Task-success percentage is deliberately absent — it needs the automated eval, which is an upsell track."

## Outside the retainer — upsells

- **Blocked on IKEA CRM — human handoff with conversation context.** No live transfer today; the agent can only give the CS number. Needs a trigger, a context package, and transport into the contact centre. Next move: confirm which CRM/helpdesk.
- **Blocked on e-commerce API — order & delivery status.** Does not exist; post-purchase questions have no data source. "IKEA's own top-priority job for the agent." **Access was declined once in June.** Next move: a decision on API access or an interim data path.
- **Enabler, ours — cost re-architecture for national volume.** Fewer and cheaper model calls per turn; projected **~85% reduction**. Next move: scope against a national cost target. (This is Benjamin's PoC territory, see `../comms/2026-07-27-benjamin-poc-handover.md`.)
- **Optional tracks:** Arabic/French; photo-to-SKU and voice optimisation; additional user journeys. "Pick the two that matter most before December."
- Pricing slide for upsells: **TBD**.

## Reading it against the rest of the record

- **The latency bar was relaxed 3× without saying so.** The March spec said ≤3 s; the Feb client email said 1–2 s; this deck sets p50 ≤ 9 s as the commitment. Defensible (latency is near the floor of the current design) but it must be stated as a change, with the rewrite as the priced alternative.
- **Cost: $0.03 → $0.01** is the strongest retainer-value story we have, and it is LLM + infrastructure only. Meta's per-message fees from 1 Oct sit outside it (see the 08-02 grounding).
- **Two of four upsells are blocked on IKEA**, and one of them (order status) is what IKEA says it wants most. The August meeting has to convert "blocked" into a named owner and date on IKEA's side, or the item is not sellable.
- **Restock-date coverage at 14%** is a data-quality fact IKEA has not been told in those terms. It caps how honest a "back in stock on…" answer can be.
- The on-call rota is still OPEN here and in `PROJECT-STATUS.md`; the deck itself says it is an org decision. It needs David or Hai to sign the names.
- The Aug W1–W4 targets have passed. Whether they closed is not recorded in this repo.

## Action items

- [ ] Reconcile the Aug W1–W4 backlog against what actually shipped; update `PROJECT-STATUS.md` (Shai, with Niv & Tali)
- [ ] Put the latency-bar change (3 s spec → 9 s p50) in writing as a decision with reasons, before IKEA notices it (Shai)
- [ ] Price the four upsell tracks — the deck's pricing slide says TBD and the August meeting needs numbers (Shai, with Arnon/David)
- [ ] Get IKEA to name the owner and decision date for e-commerce API access and the CRM/helpdesk choice (Shai, via Efrat)
