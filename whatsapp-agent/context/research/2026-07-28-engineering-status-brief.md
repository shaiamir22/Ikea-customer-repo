# IKEA Israel WhatsApp Bot — engineering status (as of 2026-07-28)

Context for you (next session): this is a technical status brief on the IKEA Israel WhatsApp
bot built by Moveo. It was assembled from the live repo (`m-ai-by-moveo/ikea-agent`): git log,
the PM progress log (`docs/progress-log.jsonl`), `daily.md`, `agent-os/` specs and roadmap,
and the deploy template. Use it as the "engineering side" input; the user will pair it with
customer-facing info and a plan.

## 1. What the product is

Hebrew- **and now English**-language WhatsApp chatbot for IKEA Israel. Customers search
products, compare options, check per-store stock, get warranty/customer-service answers, get
in-store wayfinding, build a pickup list, and run narrowing flows for modular systems (PAX,
BESTÅ, METOD). Currently a pilot: most traffic is still internal (IKEA staff + Moveo testers),
with real customers being served alongside.

## 2. Live state

- Version line **v5.0**, system prompt **v4.11.8** (last bumped 2026-07-27), model
  **`gemini-3.5-flash`** served via **Vertex AI** (global endpoint) with **Workload Identity
  Federation** auth (no long-lived key on the active path) plus a cross-endpoint fallback to
  the Gemini Developer API on transient Vertex errors.
- Architecture unchanged (three layers): deterministic **input layer** ($0 LLM — greetings,
  SKU lookup, button taps, FAQ cache, KB classifier, numbered picks) → **agent layer** (single
  Gemini call, native tool-calling, **26 tools declared**, ≤6 tool rounds) → **output layer**
  (renderer + 11-stage safety formatter: voice, RTL, price/SKU/phone guards).
- Stack: Python 3.12 · AWS Lambda arm64 · DynamoDB · S3 · SQS FIFO · Meta WhatsApp Cloud API.
  Catalog ≈ 25.5k products (11.8k single articles + 13.7k pre-configured bundles), 122k stock
  rows across 5 stores, hybrid BM25 + vector (3,072-dim) search.
- Delivery model: **push to `main` deploys straight to production** (~90 s, no staging gate);
  staging is opt-in. Cadence is high — roughly **50 merged PRs in the last 7 days**
  (#946 → #995).
- Cost: ~**$200 (₪600) for ~16,000 messages ≈ 1.3 agorot/message** (~75 messages per dollar),
  measured 2026-07-05. Per-AI-conversation cost ~**$0.019** with ~**92% prompt-cache hit rate**
  (2026-07-12) — i.e. 1–2 orders of magnitude cheaper than human CS.

## 3. What shipped recently (last ~3.5 weeks)

**A. Search engine v2 — rebuilt and rolled to 100% of users (2026-07-05/06).** The single
biggest change of the period. Replaced many fragile filters (which blocked good results) with
one broad scan of the catalog plus an AI quality-check that verifies each result matches what
the customer asked. Measured: recall on documented failure cases **63% → ~90–100%**; precision
**~97–99%** on 121 real customer queries; per-search latency **6.5–14 s → ~2 s**; typical turn
now **2 model rounds instead of 3–6**. Rolled out via an overnight private canary (7 issues
caught and fixed same session), a 166-scenario live suite and a 121-query precision benchmark.
Also: honest "we don't carry that, here's the closest real thing" behaviour, and the bot now
holds its ground (correctly) when a customer insists the catalog is wrong.

**B. "More results" precision (2026-07-04, #771–773).** Page 2 of results was served with no
relevance judgement at all — a hand-coded filter list against an open-ended feature space, so
anything uncoded leaked (2-seat covers → 3-seat, "round rug" → rectangular, "regular oven" →
turbo). Now the existing async judge issues a second precision verdict that filters page 2,
with safe fallback. Verified on 40 real pagination events.

**C. Measurement infrastructure for search (2026-07-12, #858/#865).** Two permanent evals
built: a 25-case bake-off (today's full pipeline 16/22 vs raw BM25∪vector evidence pool
**25/25** — proving the right answer is always in the pool and the loss happens in the
gates/filters), and a **67-case golden set** mined from two weeks of real failures (engine v2:
**94% recall vs 70%** for v1). This produced the agreed next lever — "Variant B" (see §4).

**D. Reliability and infrastructure (2026-07-12).**
- **Warm-server pool** enabled after a 12-minute live safety check: 18/18 real requests
  (including 3 concurrent) landed on a warm container — milliseconds instead of ~4 s.
- **60-second-wall recovery** (completion-aware idempotency) had its first real save: a
  customer's voice message that timed out got answered ~100 s later instead of silently
  vanishing.
- Root-caused a real 104-second customer wait (a stuck S3 download — 1 event in 1,843 over two
  weeks); all large downloads now time-boxed (~8 s then retry).
- **Self-inflicted incident, handled well:** a warmup improvement deployed that morning caused
  ~4,300 self-invocations in minutes; caught by our own post-deploy check in ~4 minutes, killed
  immediately, then fixed structurally with three independent guards plus a template-level off
  switch. Same day: found two product/stock feeds that had been frozen since Friday (alarms had
  fired but weren't read) — reported and restored — and fixed the weekly image-index refresh
  that had been failing silently.

**E. Vision / conversational context (2026-07-12, #866–#869).** Real field case: a customer
photographed a vase, the image turn timed out, and the follow-up "what is this product?" was
answered confidently about an unrelated item from the cart. Fixes: images are stored in history
with their recognition result (`[image — recognized: KÄLLARHALS vase]`) instead of `[image]`;
the deterministic photo path now persists the inbound message at all; a low-confidence photo is
attached to the customer's next question. Also: a semantic FAQ match now yields to the AI when
the customer has fresh product context (a "I want the battery" message was being hijacked by a
canned service answer), and the bot no longer shows unrelated "complementary items" when the
requested type isn't in that product's official list.

**F. In-store navigation (2026-07-05, #775).** New `store_navigation` tool over the 5 real store
directory maps. A store map is a numbered one-way route, not a coordinate grid, so routing is
computed in code from relative order in each store's real sequence (which differs per store) and
the model only phrases the ready answer. HE + EN, defaults to the customer's preferred store.
Verified with 24 tests, 5 live scenarios and a production smoke test.

**G. English support wave (2026-07-22/23, #946–#959, #973).** English chats got an end-to-end
localization pass, mostly root-cause work: display language is now resolved *before* the
deterministic shortcuts (that late resolution was the root of dozens of hard-coded Hebrew
strings leaking into English chats — store picker, cart, pickup list, survey, buttons);
**Material** and **product type** now come from IKEA's PIA feed in official English (99.9% and
100% coverage respectively — no machine translation; the type was leaking Hebrew on 75% of
bundle cards); all 31 planner/configurator button names translated within WhatsApp's 20-char
limit; units converted (kg, cm, l); the **pickup checklist Flow** published as a separate
English Flow so the Hebrew one was untouched (zero risk to existing users); English onboarding
Flow served to English users; `i want <SKU>` shows a card instead of silently adding to cart.

**H. Planner-CTA discipline (2026-07-23→27, #962–#982).** A long, honest iteration: the space
planner was appearing proactively, and a bogus planner recommendation could even delete product
cards. One experiment (gating on a structured `planner_intent` field) was **reverted** (#980)
before landing on the current policy — the planner appears **only when the customer explicitly
asks**, enforced both by instruction and by a deterministic ask-gate at the output door
(prompt v4.11.8, after a wide production test showed instruction-only leaked 18/24).

**I. Stock freshness and restock ETA (2026-07-27, #983–#988).** The quantity feed is now parsed
by column header with a schema-change alarm (it had been positional); out-of-stock cards show a
restock ETA taken from the feed's Planned Arrival Date, worded like the website and handed to the
agent as a phrase; the restock FAQ defers to the AI when a specific product (including a bare
SKU) is in focus.

**J. Resilience hardening (2026-07-28, #989–#991).** A corrupted local copy of the product DB
now self-heals inside search, product detail, stock check and product lookup (previously only in
one fallback path), plus more ephemeral disk. Also #974: the search filter timeout raised 5 s → 20 s.

**K. Dashboards / observability (ongoing).** Analytics accuracy overhaul: real customers vs
internal workers tagged and shown side-by-side, synthetic load-test numbers excluded, blank
daily-activity chart fixed, cost-per-message and per-conversation metrics added, WhatsApp
broadcast by segment (#796–#798). Live-trace ops dashboard rebuilt to read a per-conversation
summary row instead of scanning the whole message table — **~10× cheaper (~$45/mo → ~$3–5/mo)**,
list refresh ~3 s — plus a new quality monitor (failure rate, empty searches, >10 s answers,
drop-offs). Recent smaller ones: image lightbox and recognition labels in the conversation view
(#863/#866), open-on-first-unread scroll anchoring (#992), and a trace-cache poisoning fix
(#994) where clicking a message mid-turn permanently froze that turn's product cards on
"SKU only" for the life of the browser tab (reproduced and proven with Playwright).

## 4. What's next / in flight

The team doesn't use GitHub issues or long-lived PRs (both are empty right now), so near-term
plans live in specs and in the leads' heads. What is demonstrably in flight:

1. **Hierarchical (routed) knowledge retrieval — the main open workstream.** Spec started
   2026-07-16, owner Niv. Origin: a real bug on 2026-07-15 where the bot confabulated "no such
   service" about mattress exchange — a genuine IKEA-IL policy page that had been in the sitemap
   since 2022 but was never scraped, because page *recognition* (1,443 pages) was never wired to
   MD *creation* (the scraper used a hardcoded ~50-page list). Design: the prompt holds a stable
   menu of **26 categories** (not filenames); the model routes a question to a category; a
   retrieval tool searches **only within that category** (a hard wall, so a returns question can
   never ground on a bedroom-inspiration page) with a confidence gate and an honest fallback.
   New pages under an existing category become answerable with no prompt edit. Status: the code
   has landed — `knowledge` tool, KB index, 26-category prompt menu, a governor capping 3 distinct
   categories per turn, 8 test files — but it is **dormant behind `KB_RETRIEVAL_ENABLED=0` in
   production**. Remaining: enable on staging (branch `enable-kb-staging` exists), then a
   golden-set eval + canary + explicit approval before the production flip, then a daily
   scrape+index rebuild cadence with a new-category reconcile alert. Reach: ~1,383 kept pages
   across 26 categories, versus ~50 hand-listed files today.
2. **Search "Variant B"** — the pre-agreed next lever from the bake-off: feed the full candidate
   pool into the existing curation/judge stage, since the evidence shows the loss is in the gates,
   not the data. Also noted from the golden set: attribute filters (folding/outdoor) are silently
   dropped in v2 rather than blocking.
3. **Referent / focus tracking** — the bot can lose which product the customer is referring to
   across turns. Flagged as its own open workstream on the roadmap; not yet started.
4. **Tone workstream** — under customer pushback the bot over-agrees in tone (facts stay
   correct). Known, queued, predates the new search engine.
5. **Dead-code cleanup** — the old search machinery is now unused; cleanup was deliberately
   deferred until engine v2 had a few quiet days in production. That window has passed.
6. **Auth cleanup** — the dormant long-lived Google service-account key is still retained as a
   fallback; decommissioning waits on a soak plus pinning a fixed IAM role name.
7. **Blocked on IKEA / external, not on us:** cart-to-checkout deep links (needs IKEA
   e-commerce API access), human handoff to a live agent (needs CRM/helpdesk integration),
   proactive messaging such as restock and sale alerts (needs consent + scheduling). A
   daily-cost budget alarm and broader cross-session personalization are also still open but
   are ours to do.
8. **Latency program is parked, deliberately.** It ran 2026-06-03→10 (baseline AI-turn p50
   14.6 s / p90 27.6 s) and delivered the guards, cold-start and deterministic-route wins. The
   remaining big lever ("slim compose", ~−2.8 s) was merged dormant, tried, and **reverted on
   quality grounds**. Note that search engine v2 subsequently cut turns from 3–6 model rounds
   to ~2, which is a latency win from the quality side.

## 5. How to read this / confidence

- Solid: everything in §2 and §3 is from merged code, the deploy template, and the team's own
  dated progress log.
- Weaker: §4 is *inferred* from in-flight artifacts (specs, a staging-enable branch, dormant
  flags, "open" notes in the logs). There is **no dated near-term plan document in the repo**,
  so treat "upcoming days" as "what is demonstrably queued", not as a committed schedule. Worth
  confirming with Niv/Arnon.
- Several tracking documents are stale relative to the code (the roadmap was last updated
  2026-06-22; the KB spec's own tracker says stage S0 while stages S1–S4 have clearly landed;
  the repo's CLAUDE.md still names an older prompt version). The code is the source of truth.
- Engineering style visible in the log and worth knowing: fixes are pushed to the root cause
  rather than patched in the prompt; changes are verified against real production traffic and
  traces rather than declared fixed; incidents and reverts are written down honestly, including
  self-inflicted ones.
