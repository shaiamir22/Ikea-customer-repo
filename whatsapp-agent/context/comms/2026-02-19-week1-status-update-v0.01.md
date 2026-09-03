# Week-1 client status email + "version 0.01" architecture note (18–19 Feb 2026)

- Source: Drive `Communication` (Google Doc, Hebrew, draft with "[your name]" placeholder). Read 2026-09-03. Outbound status update to IKEA after the first working week; unclear whether it was sent verbatim.

## What was reported as done (week 1)

- **PIA connected**; full integration with IKEA's Meta business account.
- **Catalogue coverage 100%** — 11,461 products pulled from PIA (up from 2,900).
- Discovery round held with Avi Yoktan, Avi Bar, Michal (see `../meetings/2026-02-17-discovery-round-avi-yoktan-avi-bar-michal.md`). Flagged to the client that the round surfaced conflicting requirements needing a decision — explicitly the path-vs-shortcut question.

## Gaps raised with the client

- **SORM connection** for real-time stock, prices and physical locations — email sent to Efrat to book a meeting with **Shir**.
- **Tone & persona** — waiting on the "messages" page.
- **Range updates not in PIA** — waiting on a document of supplementary range changes and guidance, so the agent can be a single source of truth.

## "Version 0.01" — the architecture reset

Reported as a new system trial on **Gemini Flash-Lite 2.5**:
- Prompt caching, claimed 50–90% token-cost saving.
- **Classifier → executor → responder** structure, running searches in code; response time quoted at **1–2 seconds**.
- BM25 search, tuned for Hebrew and Scandinavian product names.
- "Zero hallucinations" via hard data retrieval; fact-checking and circuit-breaker mechanisms.
- Product images in chat; deep links to product pages.
- **Stated trade-off:** less conversational flexibility and shallower reasoning than a freer LLM design — "we will keep tuning the balance."

## Week-2 plan as promised

- Wider internal distribution to employees (with Efrat) for first feedback.
- Focus use cases: purchase assistance, stock and location, FAQ, assembly explanations.
- Tune the analytics dashboard: success metrics, volumes, costs.

## Why it matters

- The 1–2 s latency claim in this email is the origin of the client's latency expectation. Production is ~9.3 s. If this email was sent, the client has a written number from us — worth knowing before the August meeting.
- The three "waiting on IKEA" items (SORM, tone page, range updates) are the same shape as today's blockers (CRM, e-commerce API). The dependency pattern is six months old.
