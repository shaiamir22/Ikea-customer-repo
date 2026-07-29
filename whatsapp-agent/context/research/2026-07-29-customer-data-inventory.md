# Customer Data Inventory — what we actually hold

_Date: 2026-07-29. Author: Shai (with Claude). Scope: every store of customer-conversation
and customer-behaviour data across the IKEA WhatsApp agent, verified against code in
`m-AI-by-moveo/ikea-agent` rather than from memory or docs._

**Why this exists:** the persona / product-intelligence plan
(`whatsapp-agent/outputs/2026-07-29-customer-intelligence-plan.md`) needs a truthful
starting point. Several things that *look* available are not populated, and several things
that look like they need building already exist. This file is the reference; the plan is
the action.

**Verification note:** every claim below carries a code citation into `ikea-agent`. Claims
about production *volume* and *retention* are NOT verified — this session had no AWS
credentials (no `aws` CLI in the environment). Anything about row counts, date ranges, or
S3 lifecycle is flagged `[UNVERIFIED]` and is the first thing Phase 0 must confirm.

---

## Tier 1 — The conversation record (DynamoDB)

Table `IkeaWhatsAppChat-meta`, region `eu-west-1`. Single-table design; the SK prefix is the
row kind. Source: `worker-meta/infra/dynamo.py`.

| Row | Key | What it holds |
|---|---|---|
| Message | `USER#<phone>` / `MSG#<iso>#<wamid>` | Every message, both directions, full text |
| Session | `USER#<phone>` / `SESSION` | Durable per-person state (two separate attribute trees) |
| Feedback | `USER#<phone>` / `FEEDBACK#…` | Four distinct feedback kinds (below) |
| Conversation summary | `CONV#<0..9>` / `<phone digits>` | One small row per person — last message + `last_in_ts` |
| Survey roll-up | `CONFIG` / `SURVEY` | `responses[]` — every survey submission, one GetItem |
| Allowlist | `CONFIG` / `ALLOWLIST` | Permitted phones + `names` map — i.e. *who the pilot users are* |
| Live ticker | `LIVE` / `TICKER` | Realtime bump for the dashboard sidebar; no analytic value |
| Idempotency | `USER#<phone>` / `IDEMP#IN#<wamid>` | Dedup leases; no analytic value |

### Message rows — the core corpus

`dynamo.py:360-445`. Fields, and critically which are populated:

| Field | Direction | Populated? | Note |
|---|---|---|---|
| `text` | both | yes | Full message text, not truncated at rest |
| `createdAt`, `providerMessageId` | both | yes | |
| `contact_name` | IN | yes | WhatsApp contact name from the webhook |
| `pickedId` | IN | yes | The button/list id the user tapped — **explicit revealed preference** |
| `mediaUri` | IN | yes | S3 key of a sent image / voice note |
| `options[{id,title}]` | OUT | yes, capped 12 | The choices we *showed*. With `pickedId` this gives offered-vs-chosen |
| `cost{}` | OUT | yes | tokens, `gemini_cost_usd`, `prompt_version`, `is_test` |
| `traceUri` | OUT | first per turn | Pointer into the Tier 2 trace |
| `productSkus` | OUT | yes, capped 20 | SKUs surfaced in that message |
| `intent` | OUT | **partially — see caveat** | |
| `storeCode` | OUT | **yes but misnamed — see caveat** | |

**Caveat — `intent` is not customer intent.** It is set from
`agent_output.answer_intent` (`app.py:4794-4800`), which is an LLM-emitted *answer style*
(explain / compare / …), not a customer state. It is also absent on every non-agent turn,
and the input layer handles roughly 35% of turns deterministically at $0 LLM
(`agent-os/product/roadmap.md`, Phase 3). So this field covers ~65% of turns with the wrong
semantics. Do not build personas on it.

**Caveat — `storeCode` holds a store *name*.** `app.py:4800` assigns
`ctx.get("preferred_store")`, which is the Hebrew store name, into the field the docstring
describes as a code. Harmless today, but any join on store code must normalise via
`_STORE_NAME_TO_CODE`.

### Session rows — the richest per-person state

`SESSION` carries two deliberately separate attribute trees, and the split matters:

**`conversation_context`** — wiped by a `שיחה חדשה` reset. Keys observed in the worker:
`cart`, `active_goal`, `proposed_goal`, `stashed_goal`, `user_preferences` (incl.
`preferred_store`, `preferred_store_code`), `language`, `last_search_query`,
`search_results`, `search_intent_constraints`, `shown_item_nos`, `rejected_items`,
`room_type`, `modular_topic`, `flow_state`, `pickup_list`, `bot_message_count`,
`history_summary`, `last_clarifying_question`, `more_clicks`, `cta_shown`,
`last_shown_products`, `detail_item_no`, `pagination_keep`, `suggestion_round_active`.

`rejected_items`, `search_intent_constraints`, `more_clicks` and `active_goal` are the four
highest-value persona signals in the whole system — they encode what a person *turned
down*, what they constrained on, how hard they dug, and what multi-item outcome they were
actually pursuing.

**`user_profile`** — survives a reset (`dynamo.py:913-960`, written at `app.py:6165-6180`):
`terms_accepted`, `onboarding_completed`, `user_name`, `preferred_store`,
`preferred_store_code`. This is the only durable, deliberately-declared per-person record we
have. It contains **no demographics** — no age, household, home type, or tenure.

**Important:** because a reset wipes `conversation_context`, cart and goal history are
*destroyed*, not archived. Anyone who says "start a new conversation" erases the richest
part of their own record. Phase 0 must fix this by snapshotting on reset.

### Feedback rows — four kinds, often conflated

`worker-meta/feedback.py`, `app.py:6340-6380`:

| SK | Trigger |
|---|---|
| `FEEDBACK#unsolicited#<msg_id>` | Free-text praise/complaint detected mid-conversation |
| `FEEDBACK#<reacted_msg_id>` | Emoji reaction on a bot message (👍 / 👎) |
| `FEEDBACK#explicit#<ts>` | Explicit prompted feedback |
| `FEEDBACK#survey#<ts>` | WhatsApp Flow survey: `q_enjoy`, `q_helpful`, `q_recommend`, `free_text` |

The survey is the only instrument with a **comparable scale across people** — everything
else is volunteered and therefore self-selected. Survey submissions are also mirrored into
`CONFIG/SURVEY.responses`, so the whole set is one GetItem (pilot scale only).

An idle-session prompt asks for feedback after ≥3 bot messages
(`scripts/session_monitor.py:33-35`), which is a known selection bias: feedback skews toward
conversations long enough to reach the threshold.

---

## Tier 2 — Per-turn traces (S3), the richest artifact we own

`s3://ikea-debug-traces-meta/2026/MM/DD/{phone}/wamid.*.json`. Gated by `DEBUG_PHONES`,
whose current prod value is `*` — **we are tracing everyone**.

One trace = one turn, complete: the model's `thinking_excerpt`, every tool call with args
+ SQL + `search_rationale` + `result_count` + latency, which validators fired,
`decisions[].search_outcome`, the actual `output_messages` sent, per-stage timings, and a
session before/after diff.

Read with `python3 scripts/trace_read.py <wamid>`. **The repo's standing rule applies to
this work too:** read the whole trace, never grep one field — a "0 products" result can be
a cap-block, a dedup-block, a cache hit, or a real recall failure, and reading a slice
produced wrong conclusions repeatedly on 2026-06-19 (`ikea-agent/CLAUDE.md`).

`[UNVERIFIED]` How far back traces go, and whether an S3 lifecycle rule expires them.
Tracing was dead 05-18→05-29 (fixed in #195), so there is a known hole. Check
`docs/aws-storage-audit.html` and the bucket lifecycle before assuming depth.

---

## Tier 3 — Derived layers that already exist (do not rebuild)

This is the part most likely to be missed. A live per-turn analytics pipeline is already
deployed:

**Live trajectory pipeline** — `template-meta.yaml:2187-2320`:
`new trace → SQS TrajectoryConsumerQueue → TrajectoryConsumerFunction → PutItem into
IkeaTrajectories-<env> (partition "TURNS") → async-invoke ClusterSummaryRefresher`. The
refresher also runs on a short EventBridge schedule as a safety net. Each trajectory row
carries `trajectory_nodes`, per-round `tool_calls`, `validators`, `session_before/after`,
and precomputed `mechanism_signals` (`scripts/extract_trajectories.py`).

**This is the rail to extend.** It already fans out per-turn, structured, off the hot path,
with no table scans. Adding a customer axis to it costs far less than building a new
pipeline.

**Existing clustering is on the wrong axis for our purpose.**
`scripts/cluster_by_mechanism.py:44` clusters turns by *failure mechanism*:
`M2a_taxonomy_gap`, `M2b_ranker_collapse`, `M1_zero_result_cascade`,
`M3_cross_turn_kwarg_drop`, `M4_filter_precedence_collision`, `M6_spr_metadata_gap`,
`M5_validator_rewrite_drift`, `M7_retry_storm`. Secondary axis is top user-text bigrams.
Output: `s3://ikea-search-db/cluster_summary.json`.

That is an engineering-diagnostic view: *how did the pipeline break*. It answers nothing
about *who the person was or what they wanted*. The customer axis is the gap — and it is a
sibling of this, not a replacement.

**Other derived artifacts already in place:**

| Artifact | Producer | Contents |
|---|---|---|
| `data.json` (gz) on the dashboard bucket | `scripts/dashboard_aggregator.py`, 1-min schedule | `messages[]` capped 50/user, `feedback[]`, `user_count`, `stats` per 24h/7d/30d/all (messages_in/out, users, errors, avg_latency_s) |
| `cluster_summary.json` | `cluster_summary_refresher.py` | Mechanism clusters, 14d lookback |
| `latency_summary.json` | `scripts/latency_summary.py` | Latency distribution |
| `/ops.html` cost view | `ops_aggregator` (PR #748) | Per-turn cost, stamped with `prompt_version` + `is_test` |
| FAQ-miss corpus + nightly miner | `log_cache_miss` → `nightly-analyzer/` DBSCAN | Unanswered-question clusters → human-gated review queue |

The FAQ miner is the closest thing we already have to demand mining — it clusters what
people asked that we could not answer, and a human promotes candidates. Its output is a
real signal for personas, and its architecture (mine → cluster → human-approve → publish)
is the pattern the persona work should copy rather than invent.

**Cost note on the aggregator:** it does ONE full paginated table scan per run and its own
docstring records why — a `FilterExpression` does not reduce scan RCU. Any new "just scan
the table" job doubles that cost. Ride `data.json` and the Trajectories table instead.

---

## Tier 4 — The front-ends (what stakeholders already look at)

| Surface | Source file | Reads |
|---|---|---|
| `…cloudfront.net/agent-management.html` | `ikea-agent/docs/agent-management.html` (7,283 lines) | `data.json`, `cluster_summary.json`, `latency_summary.json`, `evals/results/*`. Tabs: **overview, flow, journeys, livetrace, latency, evals, config**. Can also send WhatsApp messages directly via `graph.facebook.com` (admin reply) |
| `…cloudfront.net/` (root) | `ikea-agent/admin-dashboard/dashboard.html` (9,415 lines) | Same cache; also drives the daily SES analytics email |
| `/ops.html` | `ikea-agent/scripts/ops_dashboard.html` | Cost observability |

Both CloudFront URLs were unreachable from this session — the environment's network policy
denied the host at the proxy (`connect_rejected`, 403 to CONNECT). Everything above is read
from the source that generates those pages, which is equivalent for planning purposes but
means **the live tab contents were not visually confirmed**.

The tab list is itself the finding: six of the seven tabs are engineering views. There is a
`journeys` tab and a `livetrace` conversation browser, but no view answering "who uses this,
what for, and how well does it serve each group".

---

## What we do NOT have

Stating these plainly, because a persona deck that implies otherwise is worse than none.

1. **No purchase outcome.** Nothing links a conversation to a transaction. Cart adds are
   the deepest funnel step we can observe. Linking interactions to in-store purchases is
   listed as a Phase 3 vision item in `PROJECT-STATUS.md`, not something we hold.
2. **No demographics at all.** No age, gender, household size, home type, tenure, or
   income. Preferred store is a weak geographic proxy; language is a weak segmentation
   signal; `user_name` is self-declared.
3. **The pilot population is IKEA employees, not customers.** Access is allowlist-gated,
   and the ~1,500-person release on 2026-08-02 is an *employee* release. Employees know the
   catalogue, use internal vocabulary, and shop differently. **Anything derived from
   pre-December traffic is an employee persona set unless a customer cohort is separated
   out.** This is the single largest validity threat to the whole exercise.
4. **No visit boundary.** A `שיחה חדשה` reset is the only explicit boundary, and it
   destroys context rather than archiving it. Otherwise a person's messages are one
   undifferentiated stream.
5. **No cross-channel identity.** No join to call centre, ikea.co.il, or IKEA Family. The
   phone number is the only key, and it is PII.
6. **Test traffic is mixed in** and only partially marked — `cost.is_test` exists from
   2026-07-03 (CONFIG/TESTERS ∪ `TESTER_PHONES`), so earlier rows are unlabelled. Tester
   conversations must be excluded from personas and currently cannot be, before that date.

---

## Constraints any extraction plan must respect

- **Cost.** The project's central problem is ~₪0.10/message projecting to ~₪50k/mo against
  a ₪2–8k/mo target (`PROJECT-STATUS.md`, R2 / OQ-8). An analytics job that runs LLM passes
  over the whole corpus is the same class of spend we are trying to cut. Every phase below
  needs a costed envelope, and cheap-deterministic must come before LLM.
- **No new table scans.** See the aggregator note above.
- **Evals never run without explicit permission** (`ikea-agent/CLAUDE.md`). A persona
  workstream must not trip an eval run as a side effect.
- **`scripts/` CodeUri landmine.** Any new Lambda under `scripts/` must not
  `import boto3` at module top — CI installs only `worker-meta/requirements.txt` and a
  top-level import breaks pytest collection. Use a lazy getter.
- **Push to `main` deploys to production.** No staging gate. Instrumentation lands in prod
  by default.
- **Privacy.** The primary key is a phone number. `terms_accepted` is a hard gate
  (`app.py:6051-6055`), but whether that ToU text covers behavioural analysis and profiling
  is a question for IKEA, not an assumption for us. Separately, OQ-2 already flags that
  sending real customer messages to an *external* AI provider needs data-protection
  sign-off; Gemini via Vertex is inside the existing boundary, anything else is not.

---

## Lineage finding: intent + trends were presented as already-in-bot

`Ikea-Presentation-Shuki/src/pages/RequirementsMap.tsx` (committed 2026-02-24) lists the
requirements presented to IKEA in an `inBot` bucket — capabilities stated as covered.
Two of them are:

- **#5** `זיהוי כוונת לקוח (מתעניין / מתלבט / קונה)` — detect customer intent:
  browsing / deliberating / buying
- **#8** `דשבורד – זיהוי ביקושים ומגמות` — dashboard: demand and trend identification

Neither exists as described. The `intent` field is answer-style on ~65% of turns (above);
the dashboards report messages, latency, cost, and failure mechanisms, not demand or
trends. Both were presented as in-scope, and both remain open.

The same file records a live product tension that this data can actually settle
(`tensions[0]`): whether the agent short-cutting the store journey suppresses browsing and
impulse purchase, versus customers wanting shortcuts with basket-building happening at the
end anyway. That is an empirical question about behaviour, and it is the highest-value
single analysis available from what we hold.

---

## First actions before anything is built

1. Get AWS read credentials for the analyst doing this work — nothing here can be sized
   without them.
2. Establish the four `[UNVERIFIED]` numbers: distinct phones with ≥1 inbound; total MSG
   rows; earliest reliable `createdAt`; trace retention depth and the 05-18→05-29 hole.
3. Confirm which phones are testers vs real pilot users (`CONFIG/ALLOWLIST.names`,
   `CONFIG/TESTERS`, `TESTER_PHONES`), and how many pre-2026-07-03 rows are unlabelled.
4. Put the ToU / analytics-consent question to IKEA in writing before profiling begins.
