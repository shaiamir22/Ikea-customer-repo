#!/usr/bin/env python3
"""Re-runnable conversation analysis for the IKEA WhatsApp agent.

Extracts production turns, computes the metrics, and regenerates the HTML
report. Built so the analysis can be re-run on any window — the launch cohort,
one week, one day — without hand-editing numbers into the page.

    # Launch cohort, last 7 days, from the live trajectories table
    python3 conversation_report.py --days 7 --exclude-testers

    # Compare against the frozen May baseline
    python3 conversation_report.py --days 7 --exclude-testers \
        --baseline baseline-2026-05-may-sample.json

    # Offline, from a JSONL produced by ikea-agent/scripts/extract_trajectories.py
    python3 conversation_report.py --input turns.jsonl

    # Numbers only, no HTML
    python3 conversation_report.py --days 7 --dry-run

Data sources
------------
`--source ddb` (default) queries `IkeaTrajectories-<env>`:
partition="TURNS", sort key `captured_at`. This is a **Query, not a Scan** —
it does not add scan RCU to the table the dashboard aggregator already scans
once a minute.

`--input` reads a JSONL of the same per-turn records. That is what
`ikea-agent/scripts/extract_trajectories.py` emits, and it is the escape hatch
when the DDB window has expired.

Retention: trajectory rows carry a **30-day TTL**, matching the
`s3://ikea-debug-traces-meta` lifecycle. Anything older than 30 days is gone
from both. Snapshot `metrics.json` for windows you want to keep — that is what
the baseline file is.

Cost: no LLM, no table scans, no writes. Read-only.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import statistics
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCHEMA = 2
_HERE = Path(__file__).resolve().parent

# ── Hebrew pushback patterns ────────────────────────────────────────────────
# The user telling us, unprompted, that we failed. These are self-labelled
# defects and the only signal in the system that carries severity.
# Validated on the May sample: recovered 12/12 with no false positives.
PUSHBACK_PATTERNS = [
    (r"לא קיבלתי", "did not receive"),
    (r"לא רואה", "cannot see"),
    (r"לא הראית", "you did not show"),
    (r"לא שלחת", "you did not send"),
    (r"אתה לא", "you are not"),
    (r"לא מציג", "not displaying"),
    (r"עדיין לא", "still not"),
    (r"ביקשתי", "I asked for"),
    (r"התכוונתי", "I meant"),
    (r"למה אתה", "why are you"),
    (r"למה לא", "why didn't you"),
    (r"אלו לא", "those are not"),
    (r"אלה לא", "these are not"),
    (r"זה לא מה", "that is not what"),
    (r"שאלתי", "I asked"),
]
_PUSHBACK_RE = re.compile("|".join(p for p, _ in PUSHBACK_PATTERNS))

# ── Topic buckets (keyword-coded, deterministic) ────────────────────────────
TOPIC_KEYWORDS = {
    "Kitchens": ["מטבח"],
    "Tables": ["שולחן"],
    "Beds": ["מיטה", "מיטות", "מזרן"],
    "Wardrobes & storage": ["ארון", "קופסא", "מדף", "כוורת"],
    "Kids & baby": ["ילד", "תינוק", "מגבת", "מגבות", "סיר", "צעצוע", "מונטסורי", "עריסה"],
    "Sofas & seating": ["ספה", "כורסא", "כסא", "כסאות"],
    "Bathroom": ["אמבטיה", "כיור", "מקלחת"],
    "Kitchenware & small goods": ["בקבוק", "סכו", "כפות", "סלט", "צלחת", "סיר בישול", "מגש"],
    "Lighting": ["מנורה", "תאורה", "נורה"],
    "Textiles": ["וילון", "שטיח", "כרית", "שמיכה"],
    "Warranty & service": ["אחריות", "חניה", "משלוח", "הרכבה", "החזר", "תיקון"],
}

# ── Segment assignment ──────────────────────────────────────────────────────
# ORDERED: first match wins, so every user lands in exactly one primary
# segment. Same disambiguation convention as cluster_by_mechanism's
# _MECHANISM_ORDER. Orthogonal flags (frustrated / blocked) are computed
# separately and can co-occur with any segment.
SEGMENT_ORDER = [
    "one_shot",
    "buyer",
    "curator",
    "knowledge_seeker",
    "explorer",
    "browser",
]
SEGMENT_LABELS = {
    "one_shot": ("One-shot", "Two turns or fewer — arrived, asked once, left."),
    "buyer": ("Buyer", "Added at least one item to the cart."),
    "curator": ("Curator", "Arrived with a basket of 3+ and managed it rather than building it."),
    "knowledge_seeker": ("Knowledge seeker", "Most of their intentful turns are warranty, service or store questions."),
    "explorer": ("Explorer", "Searched repeatedly, never added to cart."),
    "browser": ("Browser", "Engaged past the first turn without a clear shopping or service goal."),
}
KNOWLEDGE_ACTIONS = {"data_source"}
KNOWLEDGE_ROUTES = {"kb_lookup", "faq"}


# ═══════════════════════════ extraction ════════════════════════════════════

def load_from_ddb(since: str, until: str | None, table_name: str, region: str) -> list[dict]:
    """Query the trajectories table. Query on partition='TURNS', never a Scan."""
    import boto3  # lazy: mirrors the scripts/ CodeUri convention in ikea-agent
    from boto3.dynamodb.conditions import Key

    table = boto3.resource("dynamodb", region_name=region).Table(table_name)
    cond = Key("partition").eq("TURNS")
    cond = cond & (Key("captured_at").between(since, until) if until
                   else Key("captured_at").gte(since))

    items: list[dict] = []
    kwargs: dict = {"KeyConditionExpression": cond}
    pages = 0
    while True:
        resp = table.query(**kwargs)
        items.extend(_decimal_to_native(i) for i in (resp.get("Items") or []))
        pages += 1
        if "LastEvaluatedKey" not in resp:
            break
        kwargs["ExclusiveStartKey"] = resp["LastEvaluatedKey"]
    print(f"  loaded {len(items)} turns from {table_name} ({pages} page(s))", file=sys.stderr)
    return items


def load_from_jsonl(paths: list[str]) -> list[dict]:
    """Read one or more JSONL files, deduping on message_id/trace_id."""
    by_id: dict[str, dict] = {}
    for p in paths:
        n = 0
        for line in Path(p).read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            key = r.get("message_id") or r.get("trace_id") or f"_{len(by_id)}"
            # merge so a partial record in one file is completed by the other
            by_id[key] = {**r, **by_id.get(key, {})} if key in by_id else r
            n += 1
        print(f"  read {n} lines from {p}", file=sys.stderr)
    return list(by_id.values())


def _decimal_to_native(obj):
    from decimal import Decimal
    if isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    if isinstance(obj, dict):
        return {k: _decimal_to_native(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_decimal_to_native(v) for v in obj]
    return obj


def resolve_testers(explicit: list[str], region: str, chat_table: str) -> set[str]:
    """Tester phones: --tester-phones, then TESTER_PHONES env, then CONFIG/TESTERS."""
    out = {_digits(p) for p in explicit if _digits(p)}
    for p in (os.environ.get("TESTER_PHONES") or "").replace(";", ",").split(","):
        if _digits(p):
            out.add(_digits(p))
    try:
        import boto3
        t = boto3.resource("dynamodb", region_name=region).Table(chat_table)
        item = t.get_item(Key={"PK": "CONFIG", "SK": "TESTERS"}).get("Item") or {}
        for v in (item.get("phones") or item.get("names") or []):
            if _digits(str(v)):
                out.add(_digits(str(v)))
    except Exception as e:  # noqa: BLE001
        print(f"  note: could not read CONFIG/TESTERS ({e}) — using flags/env only",
              file=sys.stderr)
    return out


def _digits(s) -> str:
    return "".join(c for c in str(s or "") if c.isdigit())


def _canon_phone(s) -> str:
    """Canonical international digits, so USER#05… and USER#9725… collapse."""
    d = _digits(s)
    return "972" + d[1:] if d.startswith("0") else d


def pseudonymise(phone: str, salt: str) -> str:
    import hashlib
    return "U-" + hashlib.sha256((salt + _canon_phone(phone)).encode()).hexdigest()[:6]


# ═══════════════════════════ per-turn features ═════════════════════════════

def turn_features(t: dict) -> dict:
    """Deterministic per-turn features. No LLM, no inference."""
    ms = t.get("mechanism_signals") or {}
    il = t.get("input_layer") or {}
    route = (il.get("route") or "") if isinstance(il, dict) else ""
    text = t.get("user_text") or ""

    tags = {s.replace("VAL:", "") for s in (t.get("validator_tags") or [])}
    if not tags:
        tags = {v.get("name", "") for v in (t.get("validators") or [])
                if isinstance(v, dict) and v.get("fired")}

    search_calls = int(ms.get("search_count") or 0)
    zero_calls = int(ms.get("zero_result_searches") or 0)

    return {
        "phone": _canon_phone(t.get("user_phone") or t.get("phone") or ""),
        "at": t.get("captured_at") or "",
        "text": text,
        "words": len(text.split()),
        "action": t.get("action") or "",
        "route": route,
        "is_reset": route == "reset",
        "is_knowledge": (t.get("action") in KNOWLEDGE_ACTIONS) or (route in KNOWLEDGE_ROUTES),
        "is_clarifying": bool(t.get("is_clarifying_question")),
        "forced_clarifying": "forced_clarifying_true" in tags,
        "capped": bool({"blocked_search_cap", "search_cap"} & tags),
        "repeat_blocked": "blocked_repeat_query" in tags,
        "search_calls": search_calls,
        "zero_calls": zero_calls,
        "searched": search_calls > 0,
        "all_zero": bool(ms.get("all_searches_zero")),
        "m5": bool(ms.get("m5_validator_rewrite_drift")),
        "m7": bool(ms.get("m7_retry_storm")),
        "pushback": bool(_PUSHBACK_RE.search(text)),
        "thumbs_down": route == "feedback" and "negative" in str(il.get("reason", "")),
        "elapsed_ms": t.get("elapsed_ms"),
        "cart_before": _cart_size(t.get("session_before")),
        "cart_after": _cart_size(t.get("session_after")),
        "topics": [name for name, kws in TOPIC_KEYWORDS.items()
                   if any(k in text for k in kws)],
    }


def _cart_size(sess) -> int:
    if not isinstance(sess, dict):
        return 0
    c = sess.get("cart")
    if isinstance(c, list):
        return len(c)
    if isinstance(c, dict):
        return len(c.get("items") or [])
    return 0


# ═══════════════════════════ aggregation ═══════════════════════════════════

def _pct(n, d):
    return round(100.0 * n / d, 1) if d else 0.0


def _pctile(vals, q):
    if not vals:
        return None
    s = sorted(vals)
    return s[min(len(s) - 1, int(q * len(s)))]


def build_metrics(turns: list[dict], *, salt: str, window: dict,
                  excluded_testers: int, max_quotes: int,
                  knowledge_threshold: float = 0.40) -> dict:
    F = [turn_features(t) for t in turns]
    F = [f for f in F if f["at"]]
    F.sort(key=lambda f: f["at"])
    n = len(F)
    if not n:
        raise SystemExit("no turns in window — nothing to report")

    by_user: dict[str, list[dict]] = defaultdict(list)
    for f in F:
        by_user[f["phone"]].append(f)

    # ---- headline counters
    searching = [f for f in F if f["searched"]]
    all_zero = [f for f in F if f["all_zero"]]
    cart_grew = [f for f in F if f["cart_after"] > f["cart_before"]]
    total_calls = sum(f["search_calls"] for f in F)
    zero_calls = sum(f["zero_calls"] for f in F)
    terse = [f for f in F if 0 < f["words"] <= 3 and f["route"] == "agent"]
    lat = [f["elapsed_ms"] for f in F if f["elapsed_ms"]]

    # ---- latency by action group
    lat_by_action = []
    for act, group in Counter(f["action"] for f in F if f["action"]).most_common(6):
        vals = [f["elapsed_ms"] for f in F if f["action"] == act and f["elapsed_ms"]]
        if len(vals) >= 5:
            lat_by_action.append({"label": act, "n": len(vals),
                                  "p50_s": round(_pctile(vals, .5) / 1000, 1),
                                  "p90_s": round(_pctile(vals, .9) / 1000, 1)})
    lat_by_action.sort(key=lambda d: d["p50_s"])

    # ---- segmentation
    segments, user_rows = _segment(by_user, knowledge_threshold)

    # ---- pushback quotes (deduped, pseudonymised, capped)
    quotes, seen = [], set()
    for f in sorted((f for f in F if f["pushback"]), key=lambda f: f["at"], reverse=True):
        key = f["text"].strip()[:60]
        if key in seen:
            continue
        seen.add(key)
        quotes.append({"text": f["text"][:180], "user": pseudonymise(f["phone"], salt),
                       "at": f["at"][:16], "action": f["action"] or f["route"],
                       "all_zero": f["all_zero"]})
        if len(quotes) >= max_quotes:
            break

    # ---- zero-result query clusters (what people wanted and could not get)
    zq = Counter(f["text"].strip()[:70] for f in all_zero if f["text"].strip())

    return {
        "schema": SCHEMA,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "window": window,
        "provenance": {
            "turns": n, "users": len(by_user),
            "days": len({f["at"][:10] for f in F}),
            "first": F[0]["at"][:16], "last": F[-1]["at"][:16],
            "excluded_tester_turns": excluded_testers,
        },
        "headline": {
            "turns": n,
            "users": len(by_user),
            "turns_per_user": round(n / len(by_user), 1),
            "search_calls": total_calls,
            "zero_calls": zero_calls,
            "zero_call_rate": _pct(zero_calls, total_calls),
            "searching_turns": len(searching),
            "all_zero_turns": len(all_zero),
            "all_zero_rate_of_searching": _pct(len(all_zero), len(searching)),
            "cart_growth_turns": len(cart_grew),
            "cart_growth_rate": _pct(len(cart_grew), n),
            "buyers": sum(1 for u in user_rows if u["cart_adds"] > 0),
            "buyer_rate": _pct(sum(1 for u in user_rows if u["cart_adds"] > 0), len(by_user)),
            "latency_p50_s": round(_pctile(lat, .5) / 1000, 1) if lat else None,
            "latency_p90_s": round(_pctile(lat, .9) / 1000, 1) if lat else None,
            "latency_max_s": round(max(lat) / 1000, 1) if lat else None,
            "pushback_turns": sum(1 for f in F if f["pushback"]),
            "pushback_rate": _pct(sum(1 for f in F if f["pushback"]), n),
            "pushback_users": len({f["phone"] for f in F if f["pushback"]}),
            "reset_turns": sum(1 for f in F if f["is_reset"]),
            "reset_rate": _pct(sum(1 for f in F if f["is_reset"]), n),
        },
        "funnel": [
            {"label": "Turns", "n": n, "pct": 100.0},
            {"label": "Ran ≥1 search", "n": len(searching), "pct": _pct(len(searching), n)},
            {"label": "Every search returned zero", "n": len(all_zero),
             "pct": _pct(len(all_zero), n), "tone": "crit"},
            {"label": "Grew the cart", "n": len(cart_grew), "pct": _pct(len(cart_grew), n)},
        ],
        "narrowing": [
            {"label": "Clarifying question asked", "n": sum(1 for f in F if f["is_clarifying"]),
             "pct": _pct(sum(1 for f in F if f["is_clarifying"]), n)},
            {"label": "…validator-forced", "n": sum(1 for f in F if f["forced_clarifying"]),
             "pct": _pct(sum(1 for f in F if f["forced_clarifying"]), n), "tone": "s2"},
            {"label": "search_cap blocked a search", "n": sum(1 for f in F if f["capped"]),
             "pct": _pct(sum(1 for f in F if f["capped"]), n), "tone": "warn"},
            {"label": "blocked_repeat_query", "n": sum(1 for f in F if f["repeat_blocked"]),
             "pct": _pct(sum(1 for f in F if f["repeat_blocked"]), n), "tone": "warn"},
            {"label": "Validator rewrote action (M5)", "n": sum(1 for f in F if f["m5"]),
             "pct": _pct(sum(1 for f in F if f["m5"]), n), "tone": "s2"},
            {"label": "Retry storm (M7)", "n": sum(1 for f in F if f["m7"]),
             "pct": _pct(sum(1 for f in F if f["m7"]), n), "tone": "crit"},
        ],
        "terse": {"n": len(terse),
                  "all_zero": sum(1 for f in terse if f["all_zero"]),
                  "rate": _pct(sum(1 for f in terse if f["all_zero"]), len(terse))},
        "latency_by_action": lat_by_action,
        "topics": [{"label": k, "n": v} for k, v in
                   Counter(t for f in F for t in f["topics"]).most_common()],
        "actions": [{"label": k or "(none)", "n": v} for k, v in
                    Counter(f["action"] or f["route"] for f in F).most_common(12)],
        "segments": segments,
        "quotes": quotes,
        "zero_queries": [{"text": k, "n": v} for k, v in zq.most_common(15)],
    }


def _segment(by_user: dict[str, list[dict]],
             knowledge_threshold: float = 0.40) -> tuple[list[dict], list[dict]]:
    """Assign each user one primary segment (ordered, first match wins) plus
    orthogonal flags, then aggregate per segment.

    `knowledge_threshold` is deliberately a parameter, not a constant: these
    cut-points were written against a 4-user tester sample and are UNVALIDATED.
    Re-tune them once launch volume exists — see the README.
    """
    rows = []
    for phone, fs in by_user.items():
        turns = len(fs)
        adds = sum(1 for f in fs if f["cart_after"] > f["cart_before"])
        peak_cart = max([f["cart_after"] for f in fs] + [0])
        knowledge = sum(1 for f in fs if f["is_knowledge"])
        searching = sum(1 for f in fs if f["searched"])
        all_zero = sum(1 for f in fs if f["all_zero"])
        lat = [f["elapsed_ms"] for f in fs if f["elapsed_ms"]]
        # Resets carry no topical intent, so they must not dilute the ratios —
        # a user who resets 36 times is not "less of a knowledge seeker" for it.
        intentful = max(1, turns - sum(1 for f in fs if f["is_reset"]))

        if turns <= 2:
            seg = "one_shot"
        elif adds > 0:
            seg = "buyer"
        elif peak_cart >= 3:
            seg = "curator"
        elif knowledge >= knowledge_threshold * intentful:
            seg = "knowledge_seeker"
        elif searching >= 3:
            seg = "explorer"
        else:
            seg = "browser"

        rows.append({
            "user": phone, "segment": seg, "turns": turns, "cart_adds": adds,
            "peak_cart": peak_cart, "knowledge": knowledge, "searching": searching,
            "all_zero": all_zero,
            "zero_rate": _pct(all_zero, searching),
            "resets": sum(1 for f in fs if f["is_reset"]),
            "clarifying": sum(1 for f in fs if f["is_clarifying"]),
            "storms": sum(1 for f in fs if f["m7"]),
            "pushback": sum(1 for f in fs if f["pushback"]),
            "thumbs_down": sum(1 for f in fs if f["thumbs_down"]),
            "words": round(statistics.mean([f["words"] for f in fs]), 1),
            "p50_s": round(_pctile(lat, .5) / 1000, 1) if lat else None,
            "frustrated": any(f["pushback"] or f["thumbs_down"] for f in fs),
            "blocked": all_zero >= max(1, 0.5 * searching) and searching > 0,
        })

    out = []
    total_users = len(rows)
    for seg in SEGMENT_ORDER:
        members = [r for r in rows if r["segment"] == seg]
        if not members:
            continue
        name, desc = SEGMENT_LABELS[seg]
        turns = sum(r["turns"] for r in members)
        searching = sum(r["searching"] for r in members)
        p50s = [r["p50_s"] for r in members if r["p50_s"] is not None]
        out.append({
            "key": seg, "name": name, "desc": desc,
            "users": len(members), "user_pct": _pct(len(members), total_users),
            "turns": turns, "turn_pct": _pct(turns, sum(r["turns"] for r in rows)),
            "median_turns": round(statistics.median([r["turns"] for r in members]), 1),
            "cart_adds": sum(r["cart_adds"] for r in members),
            "zero_rate": _pct(sum(r["all_zero"] for r in members), searching),
            "pushback_users": sum(1 for r in members if r["pushback"] > 0),
            "frustrated_pct": _pct(sum(1 for r in members if r["frustrated"]), len(members)),
            "blocked_pct": _pct(sum(1 for r in members if r["blocked"]), len(members)),
            "resets_per_user": round(sum(r["resets"] for r in members) / len(members), 1),
            "median_p50_s": round(statistics.median(p50s), 1) if p50s else None,
        })
    return out, rows


# ═══════════════════════════ render ════════════════════════════════════════

def render(metrics: dict, baseline: dict | None, template: Path, out: Path) -> None:
    html = template.read_text(encoding="utf-8")
    payload = {"metrics": metrics, "baseline": baseline}
    blob = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
    if "__METRICS_JSON__" not in html:
        raise SystemExit(f"template {template} has no __METRICS_JSON__ placeholder")
    out.write_text(html.replace('"__METRICS_JSON__"', blob), encoding="utf-8")
    print(f"  wrote {out}", file=sys.stderr)


# ═══════════════════════════ cli ═══════════════════════════════════════════

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    src = ap.add_argument_group("source")
    src.add_argument("--source", choices=["ddb", "input"], default="ddb")
    src.add_argument("--input", nargs="+", help="JSONL file(s) of per-turn records")
    src.add_argument("--table", default=os.environ.get("TRAJECTORIES_TABLE_NAME", "IkeaTrajectories-prod"))
    src.add_argument("--chat-table", default="IkeaWhatsAppChat-meta")
    src.add_argument("--region", default=os.environ.get("AWS_REGION", "eu-west-1"))

    win = ap.add_argument_group("window")
    win.add_argument("--days", type=int, default=7, help="lookback in days (default 7)")
    win.add_argument("--since", help="ISO start, overrides --days")
    win.add_argument("--until", help="ISO end")

    ap.add_argument("--exclude-testers", action="store_true",
                    help="drop CONFIG/TESTERS + TESTER_PHONES + --tester-phones")
    ap.add_argument("--tester-phones", nargs="*", default=[])
    ap.add_argument("--baseline", help="metrics.json to compare against")
    ap.add_argument("--label", default="", help="human label for this run, e.g. 'launch week 1'")
    ap.add_argument("--salt", default=os.environ.get("REPORT_SALT", "ikea-2026"),
                    help="pseudonymisation salt — keep it stable to track a cohort over time")
    ap.add_argument("--max-quotes", type=int, default=24)
    ap.add_argument("--knowledge-threshold", type=float, default=0.40,
                    help="share of a user's intentful turns that must be service/KB "
                         "questions to call them a knowledge seeker (default 0.40, UNVALIDATED)")
    ap.add_argument("--out", default=str(_HERE.parent / "outputs" / "conversation-report-latest.html"))
    ap.add_argument("--metrics-out", default="")
    ap.add_argument("--dry-run", action="store_true", help="print metrics, write nothing")
    a = ap.parse_args()

    since = a.since or (datetime.now(timezone.utc) - timedelta(days=a.days)).isoformat()
    window = {"since": since, "until": a.until, "label": a.label or f"last {a.days}d"}

    print(f"→ window {since[:16]} … {(a.until or 'now')[:16]}", file=sys.stderr)
    if a.input:
        turns = load_from_jsonl(a.input)
        before = len(turns)
        turns = [t for t in turns
                 if (t.get("captured_at") or "") >= since
                 and (not a.until or (t.get("captured_at") or "") <= a.until)]
        # Never silently fall back to the unfiltered set — a mistyped --since
        # that quietly returns everything is how a report ends up describing a
        # different window than its own header claims.
        print(f"  {len(turns)}/{before} turns inside the window", file=sys.stderr)
        if not turns:
            raise SystemExit(
                f"window {since[:16]} … {a.until or 'now'} matched 0 of {before} turns. "
                "Widen --days/--since, or check the file's captured_at range.")
    else:
        turns = load_from_ddb(since, a.until, a.table, a.region)

    excluded = 0
    if a.exclude_testers:
        testers = resolve_testers(a.tester_phones, a.region, a.chat_table)
        if testers:
            before = len(turns)
            turns = [t for t in turns
                     if _canon_phone(t.get("user_phone") or t.get("phone") or "") not in
                     {_canon_phone(p) for p in testers}]
            excluded = before - len(turns)
            print(f"  excluded {excluded} tester turns ({len(testers)} phone(s))", file=sys.stderr)
        else:
            print("  --exclude-testers set but no tester phones resolved", file=sys.stderr)

    metrics = build_metrics(turns, salt=a.salt, window=window,
                            excluded_testers=excluded, max_quotes=a.max_quotes,
                            knowledge_threshold=a.knowledge_threshold)

    h = metrics["headline"]
    print(f"\n{metrics['provenance']['turns']} turns · {h['users']} users · "
          f"{metrics['provenance']['days']} day(s)", file=sys.stderr)
    print(f"  search calls {h['search_calls']} · {h['zero_call_rate']}% zero", file=sys.stderr)
    print(f"  all-zero turns {h['all_zero_turns']} "
          f"({h['all_zero_rate_of_searching']}% of searching)", file=sys.stderr)
    print(f"  cart-growth {h['cart_growth_rate']}% of turns · "
          f"{h['buyer_rate']}% of users bought", file=sys.stderr)
    print(f"  pushback {h['pushback_turns']} turns ({h['pushback_rate']}%) "
          f"from {h['pushback_users']} users", file=sys.stderr)
    print(f"  latency p50 {h['latency_p50_s']}s / p90 {h['latency_p90_s']}s", file=sys.stderr)
    for s in metrics["segments"]:
        print(f"  {s['name']:<18} {s['users']:>5} users ({s['user_pct']:>4}%) "
              f"zero-rate {s['zero_rate']:>4}%  frustrated {s['frustrated_pct']:>4}%",
              file=sys.stderr)

    if a.dry_run:
        print(json.dumps(metrics, ensure_ascii=False, indent=2))
        return 0

    mpath = Path(a.metrics_out) if a.metrics_out else Path(a.out).with_suffix(".metrics.json")
    mpath.parent.mkdir(parents=True, exist_ok=True)
    mpath.write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  wrote {mpath}", file=sys.stderr)

    baseline = json.loads(Path(a.baseline).read_text(encoding="utf-8")) if a.baseline else None
    render(metrics, baseline, _HERE / "report_template.html", Path(a.out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
