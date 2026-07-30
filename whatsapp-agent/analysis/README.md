# Conversation analysis — how to re-run it

Regenerates the conversation-analysis report from live production data. Built for
the launch cohort: the first report was a hand-computed document over a 258-turn
May sample, which does not survive contact with 1,500 users. This is the pipeline
version — new window in, new report out, no numbers edited by hand.

```
conversation_report.py      extract → compute → render
report_template.html        the report, rendered from embedded metrics JSON
baseline-2026-05-may-sample.json   frozen May tester metrics, for --baseline
```

---

## Prerequisites

- **AWS read credentials** for `eu-west-1` (`dynamodb:Query` on
  `IkeaTrajectories-*`, and `dynamodb:GetItem` on `IkeaWhatsAppChat-meta` only if
  you use `--exclude-testers`). Nothing here writes.
- Python 3.9+, `boto3` (only for the DDB path — the `--input` path needs neither).

## The first launch run

```bash
cd whatsapp-agent/analysis

# Day 1 sanity check — numbers only, nothing written
python3 conversation_report.py --days 1 --exclude-testers --dry-run

# Week 1, with the May tester sample as the comparison point
python3 conversation_report.py --days 7 --exclude-testers \
  --baseline baseline-2026-05-may-sample.json \
  --label "launch week 1" \
  --out ../outputs/2026-08-09-conversation-report-launch-w1.html
```

Writes the HTML plus a sibling `.metrics.json`. **Keep the metrics file** — it
becomes the baseline for the next run, and the raw data behind it expires (below).

## Every option

| Flag | Default | Notes |
|---|---|---|
| `--days N` / `--since ISO` / `--until ISO` | `--days 7` | `--since` wins over `--days` |
| `--source ddb\|input` | `ddb` | `ddb` = Query on `IkeaTrajectories`, **never a Scan** |
| `--input f.jsonl …` | — | one or more JSONL files; deduped on `message_id` |
| `--exclude-testers` | off | `CONFIG/TESTERS` ∪ `TESTER_PHONES` env ∪ `--tester-phones` |
| `--baseline f.json` | — | renders directional deltas on the headline tiles |
| `--label "…"` | `last Nd` | appears in the report header |
| `--knowledge-threshold` | `0.40` | segment cut-point — **unvalidated, see below** |
| `--salt` | `$REPORT_SALT` | keep it **stable** to follow a cohort across runs |
| `--max-quotes` | `24` | pushback quotes shown, deduped by text |
| `--dry-run` | off | prints metrics to stdout, writes nothing |

## Cost and safety

- **No LLM.** Every figure is a counter or a regex. Re-running is free.
- **No Scans.** The trajectories table is queried on `partition="TURNS"` with a
  `captured_at` range. It does not touch the chat table the dashboard aggregator
  already scans once a minute.
- **Read-only.** No writes to DynamoDB, S3, or the agent.
- **Phones are pseudonymised** to a salted hash before they reach the report.
  Raw numbers never enter the HTML or the metrics JSON.

## Retention — this is a real constraint

Trajectory rows carry a **30-day TTL**, matching the
`s3://ikea-debug-traces-meta` lifecycle (`extract_trajectories.py:357`). After 30
days the window is gone from **both** the table and the trace bucket.

**Consequence:** if nobody runs this for five weeks, launch month is
unrecoverable. Either run it weekly, or archive the raw JSONL. The
`metrics.json` snapshots are the cheap insurance — they are small, they commit
cleanly, and they are all you need for trend lines.

## When the DDB window has expired

Extract from S3 traces using the agent repo's own extractor, then feed the JSONL
in. Do **not** reimplement trace→trajectory extraction — that logic must stay in
sync with `FLOW_NODES` in `agent-management.html` and lives in one place:

```bash
python3 <ikea-agent>/scripts/extract_trajectories.py --days 14 --output turns.jsonl
python3 conversation_report.py --source input --input turns.jsonl --since 2026-08-01
```

---

## Reading the output honestly

**The call-level zero-search rate is an upper bound.** `search_cap` blocks the
3rd+ search in a turn, and a blocked search reports zero rows without proving the
query would have failed. The defensible figure is the **turn-level** one: turns
where *every* search returned zero. The report states both and labels which is
which — keep it that way.

**Segments are behavioural, not demographic.** The agent stores no age, gender,
household, or home type. Six segments are assigned per user in a fixed precedence
order (`SEGMENT_ORDER`), so every user lands in exactly one; `frustrated` and
`blocked` are orthogonal flags that can co-occur with any segment. Same
disambiguation convention as `cluster_by_mechanism.py`'s `_MECHANISM_ORDER`.

**The segment cut-points are unvalidated.** They were written against a 4-user
tester sample. `--knowledge-threshold` is a flag precisely so it can be re-tuned
rather than quietly overfitted. First launch task: run with a few values, check
the segment sizes are sane, then fix the default and write down why.

**Employees are not customers.** Until a real customer cohort exists, every
segment here is an *employee* behaviour type. That caveat belongs on the front
page of anything shown to IKEA.

## What to watch in the first launch runs

The metrics that will actually tell you whether the product works at scale:

1. **Zero-result rate by segment.** If it climbs for exploratory segments and
   stays low for buyers, the product rewards knowing IKEA's vocabulary and
   punishes describing a need. That was the pattern in the May sample.
2. **Pushback rate.** The only signal carrying severity. Any rise is a
   regression, and the quotes tell you which one.
3. **Buyer rate.** 1.9% of turns grew a cart in May, from a single user. This is
   the first window where that number means anything.
4. **One-shot share.** Users who send ≤2 turns and never return — invisible in a
   tester sample, and the clearest abandonment signal at 1,500 users.
5. **Latency by outcome.** Deterministic/KB routes ran ~2× faster than the agent
   path. If that holds, moving traffic onto them cuts latency and spend together.

---

## Two launch risks found while building this

Both are in code comments nobody is likely to read at 3am:

**1 · The trajectories table writes to a single hot partition.**
`extract_trajectories.py:350` — *"PK: 'TURNS' (single hot partition — OK for low
volume; switch to a time-bucketed partition if traffic grows beyond ~50 RPS)"*.
A DynamoDB partition caps around 1,000 WCU/s. At 1,500 users this is probably
fine, but it is an untested assumption on launch day, and the failure mode is
silent: throttled writes mean **missing turns in the analytics**, not a visible
outage. Worth an alarm on `TrajectoryConsumerDlq` depth. Note the observability
pipeline degrading does not affect customers — but it does mean the December
evidence pack quietly loses data.

**2 · Trace retention is 30 days, and launch month is inside that window.**
See above. If the first analysis run slips past early September, launch week is
gone.

Neither is mine to fix — both belong to Niv/Arnon's side. Flagging, not filing.
