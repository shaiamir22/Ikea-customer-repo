# Conversation Analysis — what people ask, and how they react

_Date: 2026-07-29. Sample: 258 real production turns, 4 phones, 2026-05-16 → 05-18._

**This is a real analysis of real production conversations, not a plan.** It is also a small
and biased sample, and the bias matters enormously — see §2 before quoting any number.

---

## 1. Where the calls are actually stored

Four places, in increasing richness. Only the first two hold the conversation itself.

| # | Store | What it is | How to read it |
|---|---|---|---|
| 1 | **DynamoDB `IkeaWhatsAppChat-meta`** (eu-west-1) | The canonical transcript. One row per message: `PK=USER#<phone>`, `SK=MSG#<iso>#<wamid>`, with full `text`, direction, `options[]` shown, `pickedId` tapped, `cost`, `traceUri` | Query one person: `PK = USER#972…`, `SK begins_with MSG#`. Roster of everyone: query the `CONV#0`…`CONV#9` partitions |
| 2 | **S3 `ikea-debug-traces-meta`** | One JSON per *turn*, complete: model's `thinking_excerpt`, every tool call with args + result counts, validators fired, what was actually sent. Gated by `DEBUG_PHONES`, currently `*` = everyone | `python3 scripts/trace_read.py <wamid>` · list a day: `--phone 972… --date 2026-06-18 --list` |
| 3 | **DynamoDB `IkeaTrajectories-<env>`** | Structured per-turn digest of #2, written live by `TrajectoryConsumerFunction`. Partition `TURNS` | Query by `captured_at` |
| 4 | **S3 dashboard bucket `data.json`** | 1-min aggregate: last 50 messages per user + stats. What the dashboards render | Same-origin fetch from the CloudFront pages |

**The fastest way in, for a human:** the Live Trace tab on
`…cloudfront.net/agent-management.html` is a conversation browser over #4, and each turn
links to its trace in #2. For analysis at volume, go to #3 — it is already structured and
needs no scan.

**What this analysis used:** two corpora already extracted from #2 and committed in the
`ikea-agent` repo — `evals/results/trajectories.jsonl` (258 turns) and
`evals/results/mined_queries.jsonl` (123 turns, overlapping). Merged and deduped by
`message_id` = 258 distinct turns. No AWS credentials were needed, and none were available
in this session.

---

## 2. Read this before using any number below

**The four phones are testers running scripted QA, not customers shopping.** The evidence is
unambiguous: 46 of 258 turns (18%) are `שיחה חדשה` resets, and the same scenario is replayed
back-to-back — the kitchen script ("מטבח" → "מה ההבדל ביניהם" → "מה היתרונות ומה החסרונות")
runs **12 times** in one morning on one phone, with near-identical wording each time.

So: **no persona, frequency, or demand ranking in this document is generalisable.** What
*is* generalisable is the **failure mechanics** — when a tester and a customer type the same
Hebrew sentence, the pipeline behaves the same way. Treat this as a bug-and-behaviour study
with a genuine sample of the product's responses, not as market research.

Sample: 258 turns · 4 phones · 3 days · May 2026 · prompt v4.x era (the field is `None` in
these records, which is itself an instrumentation gap). The product has moved to v4.9.11
since. **Every failure below needs re-verification against today's index before it is acted
on.**

---

## 3. What people asked about

Topic mix across the 258 turns, by hand-coding the user text:

| Topic | Share | Examples |
|---|---|---|
| Kitchens (mostly warranty + "what's the difference") | ~30% | `מטבח חדש לבית`, `כמה שנות אחריות למטבחי מטוד?` |
| Dining / living-room tables | ~20% | `שולחן אוכל לסלון`, `שולחן נפתח - 6 סועדים` |
| Beds & bedroom | ~10% | `אני מחפש מיטה זוגית לחדר שינה`, `מסגרת מיטה מעץ, עם פתרונות אחסון` |
| Wardrobes & storage | ~10% | `ארון בגדים לחדר ילדם`, `קופסאות אחסון בתוך ארון בגדים` |
| Kids & baby | ~10% | `מגבת לילדים`, `סיר לילה`, `מגדל למידה`, `ריהוט מונטסורי` |
| Service / logistics | ~8% | `אני רוצה להגיע עם הרכב לקנות את השולחן, יהיה לי איפה לחנות?` |
| Small goods | ~5% | `יש בקבוקי שתיה?`, `סכו״ם לסלט` |
| Sofas, bathroom, other | rest | `אני מחפשת ספה`, `ארון עם כיור לחדר אמבטיה` |

Two shapes of ask, and they behave very differently:

- **Knowledge questions** ("what's the difference", "how many years warranty") route to
  `data_source` / `kb_lookup` — 44 turns — and **generally work**. The warranty KB and the
  FAQ path are the most reliable part of the product.
- **Product-finding questions** route to `search` — 123 turns — and are where everything
  goes wrong.

---

## 4. How the bot responds

| Signal | Count | Share |
|---|---|---|
Turns that ran a search | 123 | 48% |
| …of those, **every** search returned zero | 25 | **20% of searching turns** |
| Bot asked a clarifying question | 89 | 34% |
| Validator **forced** `clarifying=true` | 54 | 21% |
| `search_cap` blocked a search | 71 | 28% |
| `blocked_repeat_query` fired | 57 | 22% |
| Retry storm (M7) | 33 | 13% |
| Validator rewrote the action (M5 drift) | 66 | 26% |
| Turns that grew the cart | **5** | **1.9%** |

**The core loop, and it is a trap.** The bot narrows instead of answering (34% clarifying,
half of it validator-forced). The user replies tersely — `5`, `3`, `מוכן`, `לבן`, `מתכת`.
Of the 74 terse agent turns, **16% returned zero results**, because the narrow reply arrives
without the original constraint attached. The user rephrases; `blocked_repeat_query` and
`search_cap` now block the retry (22% / 28%); the turn ends in a text-only apology. Then the
user resets and starts over.

`VAL:action_text_to_search` fired 93 times — the agent wanted to reply in text and the
validator converted it to a search. Combined with M5 drift at 26%, this confirms what
`CLAUDE.md` already says about `action_fix` rewriting ~80% of turns: **the LLM's chosen
action is close to meaningless; the validator chain is the real controller.**

---

## 5. How people react — the highest-value signal in the corpus

12 turns (4.7%) are the user explicitly telling us we failed. These are **self-labelled
defects**, and they are worth more than any satisfaction score because they say *what*
broke:

> `אתה לא מציג לי שום דבר` — "you're not showing me anything"
> `אלו לא קופסאות אחסון לבגדים לילדים` — "those aren't kids' clothes storage boxes"
> `מה למה נתת לי את האחריות של הכל, שאלתי על מטבחים` — "why did you give me the warranty for everything, I asked about kitchens"
> `ביקשתי ממתכת, למה אתה מציג גם את העץ?` — "I asked for metal, why are you showing wood too?"
> `למה לא הצגת אותו בפעם הראשונה?` — "why didn't you show it the first time?"
> `מ ההסגנון שביקשתי קודם?` — "what about the style I asked for earlier?"
> `לא שלחת תמונות` — "you didn't send photos"

Three of these — the metal/wood one, the "style I asked for earlier" one, and the
kitchen-warranty one — are users noticing **the bot dropped a constraint they had already
given**. That is M3 (cross-turn kwarg drop) and M4 (filter precedence collision) being
observed from the outside, by the customer, in plain Hebrew.

**This is cheap to instrument and nobody is doing it.** A regex over ~15 Hebrew pushback
patterns (`לא קיבלתי`, `לא הראית`, `אתה לא`, `ביקשתי`, `התכוונתי`, `למה לא`, `אלו לא`,
`שאלתי`…) recovered all 12 with no false positives in this sample. Run it over the message
table and you have a **continuous, zero-LLM, zero-scan quality metric grounded in what
customers actually complain about** — far better than the 👍/👎 rate, which is volunteered
and self-selected. I would build this before anything else in the persona plan.

### The image failure is the worst single experience in the sample

One user asked for a photo **eleven consecutive times** over four minutes, escalating:

> `תראה לי תמונה שלו` → `לא רואה תמונה` → `יש אותו בלבן?` → `תראה לי אותו בלבן` →
> `תראה לי תמונה` → `עדיין לא הראית לי תמונה` → `עדיין לא קיבלתי תמונה` →
> `לא קיבלתי תמונה` → `תשלח לי תמונה` → `אני רוצה תמונה שלו בלבן` → `תמונות!` → `תמונה`

Only 3 of those 11 turns routed to `show_images`; the rest went to `show_search_results`.
A second phone hit the same wall (`תראה לי תמונה של המיטה` → `לא שלחת תמונות`), and a third
asked for pictures because it couldn't identify the products by name
(`תראה לי תמונות, אני לא מכיר את המוצרים האלה`).

This does not appear on the open-issues list in `PROJECT-STATUS.md`. For a furniture product
on WhatsApp, "I cannot get you a picture" is close to a total failure, and the escalation
pattern (`תמונות!`) is exactly what will produce bad internal word-of-mouth at 1,500 users.
**Verify whether this still reproduces before Aug 2.**

---

## 6. Zero-result clusters — with an honest caveat about each

`CLAUDE.md` warns that a zero can be a cap-block, a dedup-block, a cache hit, or a real
recall failure. I checked: on the failing turns below, `session_before.shown_item_nos` was
**empty** and the cart was **empty**, so dedup is ruled out. But `search_cap` /
`search_cat_cap` fired 3–5× per turn, so **the 3rd and later searches in each turn report
zero without proving the query would return zero.** Only the first two searches per turn are
clean evidence. I've marked accordingly.

| Cluster | Attempts | Clean evidence | Status |
|---|---|---|---|
| **Kids' towels** — `מגבת לילדים`, `מגבות לילדים`, `מגבות אמבטיה לילדים`, `מגבות לתינוקות` | 8, across 2 phones and 4 resets | `מגבת לילדים` and `מגבת` (both with `room=חדר ילדים`) genuinely returned 0 | Solid. The bare `מגבות` zero is cap-contaminated — do not cite it |
| **Potty training** — `סיר לילה`, `סיר לילדים`, `סיר גמילה`, `פתרונות לגמילת ילדים`, `מה יכול לסייע לילד להיגמל מחיטולים?` | 6, across 3 phones | **See below — this one is a possible regression** | Needs replay |
| **Style search** — `בסגנון כפרי` (rustic), `בסגנון מודרני` | 4 | All-zero + retry storm | Solid |
| **Numeric dimensions** — `שולחן שכשהוא סגור הוא קוטר 130` | 1 | All-zero + storm | Matches open bug **M15** (auto-widen numeric constraints on empty result) |
| **Bathroom vanity** — `ארון עם כיור לחדר אמבטיה` | 3 | All-zero + storm | Solid, and it is a core IKEA category |
| **Hebrew-transliterated series** — `מסדרת אנגסון`, `מסדרת סקוב וסטוק`, `ANGSHUMLA` | 4 | Zero | `מסדרת מאלמ` (MALM) *worked* — so coverage is partial |
| **Bath toys** — `צעצועים לרחצה`, `סט צעצועים לאמבטיה` | 2 | Zero | Solid |

### The potty case may be a regression, and it is worth 20 minutes

- **05-16, phone …9278:** `search(query="סיר לילה")` → **2 results**, SKUs `00591583` /
  `40591581`, `product_type_he = "סיר לילדים"`, series `LILLA` and `LOCKIG`. The products
  exist in the catalogue. Note this succeeded *despite* `shown_item_nos` already holding 6
  items.
- **05-18, phone …1983:** the **identical string** `search(query="סיר לילה")` → **0**, on a
  freshly reset session with empty dedup state. So did `סיר לילדים` — which is the exact
  `product_type_he` value the 05-16 call returned.

Same query, same index, two days apart, results → nothing. Both were among the first two
searches of their turn, so neither is cap-contaminated. I am **not** asserting a regression
from a two-point sample — but this is precisely the shape of one, and it is cheap to settle:
replay those two strings against today's index (`scripts/debug_trace.py --text "סיר לילה"`)
and compare. If it still returns zero while the SKUs are live, something between 05-16 and
05-18 broke a class of queries and may still be broken.

Note also that `מחפש מגבת לילדים` is the *example query in `CLAUDE.md`'s own debug_trace
snippet* — this failure was known and being actively tested in May. Confirm whether
PR #116-118 (kids `room_type` filter) closed it or not.

---

## 7. Demand signals worth naming

Two things users asked for repeatedly, unprompted, that the product does not do:

**Customisation / personal fit** — five distinct asks in the sample:
> `ואם אני רוצה לבחור צבע מסוים לרגליים וצבע אחר למשטח אפשר?` — different colour for legs vs top?
> `יש לי אפשרות לשחק עם הצבעים ולעשות עיצוב אישי?` — can I play with colours, do a personal design?
> `יש אפשרות לשולחן בעיצוב אישי?` · `ספה מותאמת אישית` · `אני רוצה משהו שיתאים לסלון שלי בדיוק`

**"What goes with what" / completing a set** — `איפה הכסאות?` (where are the chairs?),
`זה מגיע רק שולחן או יחד עם הכסאות במחיר הזה?` (is that the table alone or with chairs at
that price?), `איפה הקופסאות?`. Users assume the agent understands a *set*, not an item.
The goal engine exists for this; it is not reaching them.

Both are consistent with the "delivery/assembly + completeness" direction already named as
the top strategic feature, and both are stronger evidence than a feature request in a
meeting.

---

## 8. What actually works (so the picture is balanced)

- **Deterministic paths are flawless.** All 5 SKU lookups resolved. Button taps resolved.
  `kb_lookup` for warranty answered 9 times. These cost $0 in LLM and never failed.
- **The one genuinely successful shopping session** is phone …9278 on 05-16: kids' table →
  MAMMUT → chairs → cart, then LOCKIG → cart, then BUSUNGE wardrobe → cart. Three cart adds
  in ~5 minutes. It worked because the products were findable by series name and the user
  accepted what was shown.
- **`show_comparison` worked** both times it was invoked — including
  `מה ההבדל בין המיטות מאלמ שהצגת לי?`
- **Recovery from a pivot worked**: `לא, אני רוצה ארון בגדים` mid-flow was handled cleanly.

The pattern: **the product is reliable when the user knows the series name or the SKU, and
unreliable when they describe what they want in their own words.** That is the single
sentence summary of this sample, and it is a search-quality statement — which matters,
because search quality on semantically complex queries was explicitly excluded from the
December scope on 2026-07-28. This sample is the argument for revisiting that call.

---

## 9. What I'd do with this

Ordered by value-per-day-of-work:

1. **Ship the Hebrew pushback detector** (~half a day, no LLM, no scan). A continuous
   quality metric grounded in customer complaints. Also backfillable over all history.
2. **Re-verify the image failure before Aug 2.** Highest-severity user-visible defect in
   the sample and absent from the open-issues list.
3. **Replay the 7 zero-result clusters against today's index** (~2 hours). Settles the
   potty regression question and tells us which gaps are still live.
4. **Fix the typo'd reset.** `יחה חדשה` (dropped first letter) and `שיחה חדשהֿ` (stray
   diacritic) both missed the reset pattern and burned a full LLM turn. Trivially cheap,
   and 18% of turns are resets.
5. **Instrument `prompt_version` into the trajectory record** — it is `None` throughout this
   sample, so no finding here can be tied to a prompt version.
6. **Re-run this analysis on the first week of the 1,500-employee traffic**, where the topic
   mix will finally mean something.

---

## Method + reproducibility

```bash
cd <ikea-agent>
# the two corpora used, both already in the repo:
wc -l evals/results/trajectories.jsonl evals/results/mined_queries.jsonl
# merge on message_id, then the aggregates in §4-6 are plain Counters over
# mechanism_signals / validator_tags / tool_calls[].result_count
```

Every quantitative claim above comes from those two files. Every quote is verbatim user
text. Nothing here is modelled, inferred, or LLM-summarised — and nothing here is a
substitute for the same analysis run over a real customer cohort.
