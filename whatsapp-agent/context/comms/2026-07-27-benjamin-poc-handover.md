# Benjamin's PoC handover + Hai's response (2026-07-27)

Email thread: Benjamin → Shai, David, Niv, Taly, Hai. Reply from Hai Morgenstern.

## Benjamin — proof-of-concept handover

Hands over the PoC he's been building for the IKEA WhatsApp bot. Three things it does:

1. Makes the bot **~87% cheaper per message**.
2. Lets customers chat in **any language**, not just Hebrew.
3. **Modularity** — moves off a design locked to a single AI vendor. Via OpenRouter, routing to the cheapest/best model and switching freely.

Quality is on par with today's bot. The trade-off is replies **~4-7s slower**.

### Write-ups

- Plain-language summary (what it does, results, what's next): https://claude.ai/code/artifact/14ebb321-434b-427e-b8ad-d8fe51ad0b38
- Technical playbook (architecture, local tester, rebuild steps, safety): https://claude.ai/code/artifact/8e45dd7d-60ca-4312-97a5-7f44f767daec

### Code

Two branches, fully independent of the current code, both level with main as of 2026-07-27 (nothing ahead or behind):

- `origin/staging-llm-sandwich-py312` — current version on Python 3.12 (latest platform), re-validated: **2,474 tests pass**.
- `origin/staging-llm-sandwich` — stable previously-tested version on Python 3.9, kept as a guaranteed fallback.

### Testing status

Manually tested in French and English across several conversation types using a local fake-WhatsApp interface; works well. **Gap: Hebrew tests are still missing** — Hebrew is the primary customer language, so this is needed before full validation.

To try it: the technical playbook has a 3-line command to launch the local fake-WhatsApp tester — chat with the bot and watch cost, latency and language live. No production access needed.

### Safety

The whole thing sits behind a switch that is **OFF by default**, so production is completely unaffected. Nothing ships until we decide to.

Two decisions pending before any real-customer test, both business/compliance rather than code:
1. Data-protection sign-off to send real customer messages to the external AI provider.
2. Whether the +4-7s latency is acceptable for the ~87% saving.

## Hai Morgenstern — response

Recommends the main narrative and focus should be: **finalize this project first** — at the level of SLA / concurrent sessions committed to in the current agreement scope. Then propose these improvements (mainly cost, later latency) plus general use-case/flow improvements — but only after feedback from a substantial sample of users in the next stage.

TL;DR: yes to more fixes, both engineering and logic/algo — but at the next stage, driven by feedback from a significant sample (number of users, diverse uses). Flagged to David to factor this into preparation for the follow-up project with IKEA.

## Implications

- The PoC is **not** going into the Aug 1 pilot. It's staged and safe, waiting on the next phase.
- Hebrew testing is the open validation gap on the PoC itself.
- The two pending decisions (data protection, latency-vs-cost) are client-side and unresolved.
- Need clarity on what SLA / concurrent-session level the current agreement actually commits to — that's the definition of "finalized" Hai is pointing at.
