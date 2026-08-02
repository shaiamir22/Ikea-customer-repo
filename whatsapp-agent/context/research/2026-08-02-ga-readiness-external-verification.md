# External verification pass — GA readiness research claims

_Date: 2026-08-02 · Owner: Shai · Input: `Enterprise_WhatsApp_Chatbot_GA_Proposal.pdf` + `ga_readiness_infographic.html` (deep-research output, external benchmarks previously unverified)_

## Why this file exists

The GA-readiness research report was produced in a run where web tools were unavailable, so its
external benchmarks went in unverified. This pass checks them before anything reaches Arnon,
David, or IKEA's C-level.

## Method and its ceiling — read this before quoting anything below

Verification was done with **web search only**. Direct page fetches are blocked by this
environment's egress policy (403 on CONNECT for every external host tried, including
`developers.facebook.com`, `ai.google.dev`, `twilio.com`). So every finding below is
**corroborated across search results, not read off the primary page.**

That is good enough to *kill a wrong number* and good enough to *raise a flag*. It is **not**
good enough to put a rate in a contract or a slide footnote reading "Source: Meta". Items marked
**PRIMARY-SOURCE REQUIRED** must be confirmed by opening the vendor's own page before leadership
sees them.

Confidence labels: **High** = multiple independent sources agree · **Medium** = corroborated but
thin or aggregator-only · **Low** = single source, or figure varies materially between sources.

---

## 1. The two findings that were not in the research at all

These matter more than anything the report got right or wrong, because both are **time-bound and
land before December**.

### 1.1 Meta resumes charging for service messages on 2026-10-01 — **High**

Today, when a customer messages the agent first, every reply the business sends inside the
24-hour customer-service window is **free**. From **1 October 2026** that ends: every
business-sent reply inside the window is billed per message at the recipient country's
utility/authentication rate. Utility templates sent inside the window become chargeable on the
same date.

Two details that make it worse than it first sounds:

- **No volume discount.** Utility and authentication *templates* get volume tiers that reduce the
  rate as monthly volume grows. Service messages explicitly do not — the rate stays flat at any
  volume.
- **No exemption for who sends it.** AI reply, human agent reply, or template — from 1 October
  there is no free way to respond inside an open conversation.

Unchanged: inbound customer messages are never billed, and the 72-hour entry-point window from
Click-to-WhatsApp ads keeps its free start.

**Why this is the single most important number in the project:** the IKEA agent is almost entirely
inbound service replies. That is the exact category moving from free to paid, seven weeks before
the December pilot. See the cost model in
`../../outputs/2026-08-02-cost-and-scale-grounding.md` — at pilot volumes the Meta fee is
plausibly **10–25× the entire LLM bill** the team has spent months optimizing.

Sources: [hello-charles](https://www.hello-charles.com/blog/whatsapp-service-message-pricing-what-changes-in-2026) ·
[ycloud](https://www.ycloud.com/blog/whatsapp-service-messages-24-hour-window-pricing) ·
[chakrahq](https://chakrahq.com/article/whatsapp-api-pricing-update-service-messages-october-2026/) ·
[tesseraai](https://tesseraai.cloud/en/blog/whatsapp-service-message-charges-2026/) ·
[quali-d](https://quali-d.com/blog/whatsapp-api-service-message-pricing-2026)

> **PRIMARY-SOURCE REQUIRED** — confirm the date, the category treatment, and the Israel rate on
> Meta's own pricing page before this goes in a deck.

### 1.2 Gemini token prices rise on the migration path — **High** on prices, **Medium** on dates

The research's entire cost-optimism thesis is macro token deflation ("mid-tier rates have fallen
to $0.14/1M input"). For the Gemini family this project actually runs on, the near-term
direction is **the opposite**.

| Model | Input $/1M | Output $/1M | vs 2.5 Flash | Status |
|---|---|---|---|---|
| Gemini 2.5 Flash-Lite | 0.10 | 0.40 | 0.7× / 0.3× | Retires 2026-10-16 (earliest) |
| Gemini 2.5 Flash | 0.15 | 1.25 | 1.0× / 1.0× | Retires 2026-10-16 (earliest) |
| Gemini 3.5 Flash-Lite | 0.30 | 2.50 | 2.0× / 2.0× | Current gen |
| Gemini 3.5 Flash | 1.50 | 9.00 | **10.0× / 7.2×** | Current gen; cached input $0.15 |

Retirement of Gemini 2.5 Pro, 2.5 Flash and 2.5 Flash-Lite is dated **2026-10-16**, but that is
the *earliest possible* shutdown, not a commitment — Google says it will confirm a final date once
Gemini 3 reaches GA and give at least six months' notice. Treat the date as soft and the price
direction as hard.

Caching softens input but not output: cached input on 3.5 Flash is $0.15/1M — a 90% discount, and
exactly what *uncached* input cost on 2.5 Flash. Output has no cache equivalent and is 7.2×.

Sources: [Gemini deprecations](https://ai.google.dev/gemini-api/docs/deprecations) ·
[Vertex AI release notes](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/release-notes) ·
[gcpstudyhub](https://gcpstudyhub.com/blog/google-is-retiring-gemini-2-5-on-agent-platform-what-you-need-to-know-and-do-before-october-2026) ·
[OpenRouter 3.5 Flash](https://openrouter.ai/google/gemini-3.5-flash) ·
[OpenRouter 2.5 Flash-Lite](https://openrouter.ai/google/gemini-2.5-flash-lite) ·
[pricepertoken](https://pricepertoken.com/pricing-page/model/google-gemini-2.5-flash) ·
[cloudzero](https://www.cloudzero.com/blog/gemini-pricing/)

> **PRIMARY-SOURCE REQUIRED** — and **confirm which Gemini model the agent runs today**. The whole
> table is only actionable once we know our starting point; nothing in the repo states it.

### 1.3 Adjacent, probably not ours — Meta Business Agent token billing — **Medium**

Meta began billing its **own** Business Agent platform per token on **2026-08-01** at ~$2.00/1M
tokens, reported as ~4–5¢ per message at 20–25k tokens/message.

This is Meta's hosted agent product. IKEA's agent is self-built on Cloud API with our own LLM, so
this pricing should **not** apply to us — but that needs confirming, not assuming, and it is a
useful competitive anchor: Meta itself prices AI-handled messages at roughly 4–5¢. Our LLM cost
per message is ~0.1 agorot (≈0.03¢).

Sources: [enterprisedna](https://enterprisedna.co/resources/news/meta-business-agent-billing-august-1-token-pricing-2026/) ·
[techtimes](https://www.techtimes.com/articles/320787/20260716/meta-business-agent-billing-starts-aug-1-free-test-window-ends-days.htm) ·
[chatmaxima](https://chatmaxima.com/blog/meta-business-agent-platform-explainer-2026/)

---

## 2. Claims from the report — verdicts

### Confirmed

| Claim as written | Verdict | Confidence | Note |
|---|---|---|---|
| Meta Cloud API default throughput 80 msg/sec per business number | **Confirmed, and incomplete** | High | 80 mps is the default; **auto-upgrade to 1,000 mps** exists for numbers with medium+ quality rating. Throughput counts inbound *and* outbound. Over-limit returns error 130429 (report said generic HTTP 429). The report presented 80 mps as a hard ceiling — it is a starting tier. |
| Messaging tiers 1k / 10k / 100k / unlimited unique recipients per 24h | **Confirmed, and incomplete** | High | Unverified accounts start at **250**/day before business verification; the report omits this rung. Upgrade needs healthy (Green/Yellow) quality + ≥50% of current limit used in a single day within 7 days. Meta reviews every 6 hours. |
| Quality rating drives tier; sustained low rating demotes | **Confirmed** | High | Green/Yellow/Red. Computed from block rate, report rate, unhealthy template usage, volume-vs-tier over trailing 24h. 7 days at Low ⇒ one-tier demotion. |
| Gartner: ≥30% of GenAI projects abandoned after PoC by end-2025 | **Confirmed** | High | Press release 2024-07-29. Report's "30% to 50%" overstates it — Gartner's number is "at least 30%"; the 50% comes from a separate Gartner article on project failure. Don't present as a single range. |
| RAND: >80% of AI projects fail | **Confirmed, with a caveat that helps us** | High | RAND RRA2680-1, from 65 practitioner interviews. The useful finding for our deck: **~77–80% of failures are strategic/organisational, only ~23% technical.** That directly supports the "four of eight gaps are blocked on IKEA, not on engineering" argument. |
| Israel Amendment 13 in force; PPA AI guidance requires bot disclosure, explicit opt-in, DPIA, DPO | **Confirmed, dates corrected** | High | In force **2025-08-14** (report said "August 2025" — fine). Draft AI guidance is **Feb 2025 draft, May 2025 revision** — the report's "Published April 2025" is wrong. Substance (disclosure, no pre-checked consent, DPIA, DPO, scraping limits, data-subject rights) holds. |
| Prompt caching gives ~90% discount on cached input | **Confirmed for Gemini** | High | Gemini 2.5+ = 90% discount on cached input; Gemini 2.0 = 75%. Explicit caching adds **$1.00 per 1M tokens per hour storage**; implicit caching has no storage cost. Report cited Anthropic's numbers and thresholds — wrong vendor for this project. |
| Leroy Merlin Brazil: R$111M WhatsApp GMV, cart abandonment to 0.5% | **Confirmed as reported by vendor** | Medium | Corroborated, but it is a **Blip marketing case study**, not audited disclosure. Also carries an 80% AHT reduction. Fine as directional colour, not as a target. |

### Refuted, misattributed, or not safe to use

| Claim as written | Problem | Confidence |
|---|---|---|
| "Token deflation — mid-tier rates at $0.14/1M input" as *our* cost trajectory | True of some vendors' mid-tier models; **false for our Gemini migration path**, where the successor tier is 3–10× more expensive. Using it as our forward assumption is the most dangerous line in the report. | High |
| Prompt-caching thresholds "1,024 / 2,048 / 4,096 tokens for Claude Sonnet/Opus/Haiku" | Anthropic-specific. We run Gemini. Irrelevant, and quoting it signals we don't know our own stack. | High |
| "68% net system cost reduction from caching" | Traceable to a single Spring AI + Anthropic blog post. Not a benchmark, not our vendor, not our workload. Drop it. | High |
| Report's §1 adoption curve (24% M1 → 34% M3 cart recovery → 55–65% M6 containment) | Sourced to content-marketing blogs (`chati.ai`, `inappstory`, `lime-technologies`), not primary research. The specific 24%/34%/55–65% ladder should not be presented as benchmark data. | High |
| "Peak hour = 15–25% of daily volume", "10AM–2PM = +20% engagement" | Sourced to `chatarchitect` / `trengo` blogs. Directionally ordinary, but not a citable benchmark. **We don't need it** — we have 1,500 staff live and can measure our own peak curve within two weeks. | High |
| "Meta template approval: <24h median, 48–72h worst case" | Aggregator-sourced only; no Meta SLA found. Also **largely irrelevant to us** — templates are for business-initiated messaging; our agent is inbound-driven. | Medium |
| "$5M–$20M for full enterprise GenAI deployment" (Gartner) | Order-of-magnitude away from this project (₪109k fixed + ₪10k/mo). Quoting it invites the question "so why is ours 1/500th the price?" Leave it out. | Medium |
| "30% of build capital reserved for post-GA tuning" | Traces to a vendor blog (`quickchat.ai`), presented in the report as an "established enterprise benchmark". It isn't. The *practice* is sound and we should budget for tuning — just don't cite a number we can't stand behind. | High |
| IDC/Lenovo "4 of 33 pilots graduated"; S&P "42% abandoned in 2025, up from 17%" | Both reached only via an intermediary blog (`landauai.com`), not the issuing houses. Do not use until traced. | Low |
| Infographic: "Meta Cloud API Ceiling — **80 ms/sec**" | Unit error; should be msg/sec. Also stated as a ceiling when it is an upgradable default. | High |
| Infographic: "0.5% Cart Abandonment — *Channel Efficiency Baseline*" | Relabels one Brazilian retailer's vendor-reported result as an industry baseline. | High |
| Infographic: "Peak Concentraion" | Typo. | High |
| Infographic: caching chart captioned "68% Net Reduction" over bars showing 90% | The chart and its caption disagree. | High |
| Infographic §7 Q&A: circuit-breaker at 3.5s, NER PII layer, 1.5% block kill-switch, confidence <0.70 flagging, 24h queue retention | **These describe systems we have not built.** Written as present-tense capability ("The architecture incorporates…", "have been finalized for legal DPO sign-off"). Against our own status — no live handoff, no automated eval, no task-success metric, privacy sign-off outstanding — putting these in front of IKEA would be claiming capability we don't have. Cut or rewrite every one as a proposal. | High |

---

## 3. What still cannot be verified from here

| Gap | Why it matters | How to close |
|---|---|---|
| **Meta's Israel per-message rate card** (utility/auth rate, the one service replies will bill at) | The dominant cost variable from 1 Oct. One aggregator suggested ₪0.15–0.30/message generally, likely marketing-weighted; utility typically runs 80–95% below marketing. Range is too wide to plan on. | Open Meta's pricing page on an unrestricted network, or ask IKEA's BSP/WABA admin for the actual invoice rate — **IKEA already holds this data.** |
| Which Gemini model the agent runs today, and its current token mix | Without it the price ladder can't be turned into a per-message delta | Niv — one line in the config |
| Whether Meta Business Agent token pricing touches a self-hosted Cloud API agent | Changes the fee model if yes | Confirm with BSP |
| Actual messages per user per day | Every volume tier in the PRD rests on ~80/user/day, which is unmeasured and high | **Measure it from the employee release that went live today.** Two weeks of data replaces the assumption. |
| Real concurrency ceiling (OQ-9) | No load test has ever run | Unchanged from PROJECT-STATUS; external benchmarks are no substitute |

---

## 4. What this pass changes

1. The cost conversation is **not primarily an LLM-cost conversation**. From 1 October the platform
   fee plausibly dominates the LLM bill by an order of magnitude. See the grounding memo.
2. **October 2026 is a double cliff** — Meta service fees start 1 Oct, Gemini 2.5 retires 16 Oct
   (earliest) — landing exactly where the plan schedules "cost re-architecture lands, Oct–Nov."
3. **Benjamin's vendor-agnostic PoC changes status.** Parked 2026-07-28 as out of base scope, it is
   now the hedge against both Gemini deprecation and Gemini price inflation. That decision deserves
   re-examination on this evidence — see OQ-11 in PROJECT-STATUS.
4. Roughly a third of the research report is **not usable as sourced fact**. The internal
   first-party data is the stronger evidence, as the earlier run concluded — this pass reinforces
   that, and narrows the external set to a handful of platform facts that are genuinely load-bearing.
