# Client-facing kickoff pack (Apr 2026) and progress decks (30 Apr, 3 Jun)

- Sources: Drive `Kickoffs/ikea_kickoff (1).docx` ("official kickoff document, April 2026"); `Kickoffs/ikea-kickoff-30.04.26.html` (two-week summary); `Slides/ikea-progress-03-06-26.html` ("the road we travelled"). Read 2026-09-03. Two sibling HTML decks (`ikea-kickoff.html` 19.4, `ikea-status-29-07-26.html`) are JavaScript bundles and could not be read.
- Why grouped: together they are the written record of what IKEA was **shown and told** between the discovery round and the handover.

## Kickoff pack (April) — what IKEA was told

Framed as "the bot is in active production with a small user group; this is the formal kickoff for wider rollout and expectation-setting."

- **Live features (13):** natural-language search, guided narrowing (max 3 questions), full product details, purchase tips, intent detection, comparison, cross-sell, internal insights dashboard, 24/7 availability with hours messaging, tone & style, privacy (no PII between conversations), service info (delivery 5–10 days, returns, assembly), real-time stock by branch (five branches).
- **Planned (10):** voice input, in-store navigation, package info, assembly videos, Toolbox images, bin location, back-in-stock alerts, checkout/instalment guidance, image input, Arabic/French.
- Contradiction inside the doc: the full status table marks **all 23** as "in development / future", while the prose calls 13 of them live. Reads like a template that was never reconciled.
- **Known gaps admitted to the client:** conversation "jumps" between topics; clarifying questions feel redundant; inconsistent result formats; the bot forgets earlier details in long conversations; irrelevant results on multi-criteria queries; service info not always right by region; 15-minute stock lag not explained; **confident answers on edge cases where it lacks data**.
- **Test asks to IKEA** (8 questions) and an explicit **out-of-test list**: back-in-stock (F20), voice (F10), multilingual (F23), and UI design ("WhatsApp owns the interface").
- **Feedback mechanics:** 👍/👎 on every reply; free-text prompt after 👎; **weekly feedback summary to IKEA**.
- **Fix process with SLAs — this is a written commitment to IKEA:**

| Stage | Owner | SLA |
|---|---|---|
| Intake and categorise (UX / accuracy / coverage) | automatic | immediate |
| Analyse, find recurring patterns (≥2 cases) | PM + QA | ≤48 h |
| Prioritise (bug / UX / missing content) | PM | weekly |
| Fix (prompt, logic, data) | Engineering | ≤5 days |
| Verify | QA | ≤2 days |
| Report back in the weekly summary | PM | weekly |

  By severity: **critical bug (bot not answering / wrong info) — 24 h**; UX improvement — 5 business days; missing content — 10 business days.
- **New-feature process:** request in a fixed format (need, audience, ideal conversation, success criterion) → assessment within **7 business days** (approve / reasoned reject / alternative) → spec + target date, **formal IKEA sign-off before development** → staged rollout → 30-day results report.
- Closing line: "we are here as partners, not vendors." Footer: "for internal use and the official kickoff."

## Two-week summary (30 Apr)

- Five new features: **SPR support (PAX, METOD, BESTÅ)** with parts, prices and stock per component; **smart pickup list** sorted by aisle with an interactive checklist; **sales-advisor persona** (proactive recommendations, comparisons, lifestyle fit); **visual stock indicator per branch** (traffic-light on every product card); **modular-configuration advice** (assembly rules).
- Measured improvements: catalogue search coverage up "from 83%" (new figure was a live counter, not captured); search quality upgrade; extra knowledge files (guides, catalogues).
- Next steps listed: search relevance, system-prompt refinement from real conversations, design inspiration from the site based on collected items, **location-based pickup list / in-store navigation**, careers-page redirect for job questions.
- Headline metrics (messages sent, active users, feedback meetings) were live counters — not recoverable from the file.

## "The road we travelled" (3 Jun) — the DoD framing IKEA already saw

Four-act deck: starting point → today → project-end target → beyond.

- **Starting point, admitted:** no transparency into decisions; context-less answers; taxonomy gaps; customer journeys not handled end-to-end; PIA series data unused; **"showing results" with no results**; SPR changes not updatable.
- **Today:** error taxonomy (critical vs. low); automatic detection of critical errors (e.g. results not shown, performance drop); observability; full PIA alignment; state graph with metadata. "The new ability to detect errors also exposes new things to fix — that is the point."
- **Project-end target, as stated to IKEA:** *one agreed and verified picture of what the agent can do, and in which customer journeys.* Two deliverables: an **approved list of customer stories/journeys**, and a **definition of done on two axes: critical errors + customer journeys.**
- **Beyond project end:** a live system in "SaaS mode" — continuous error management with clear priorities, staying aligned to IKEA's environment (PIA, Itinerary), adding/changing/removing journeys as needed. Loop: detect → improve → verify → release.

## Why this matters

- **A DoD was proposed to IKEA in June.** The 07-28 room said no definition of done exists. More precisely: the *shape* of one was presented (journeys + critical errors) and the **approved journey list was never produced**. Finishing that list is the shortest path to a DoD IKEA has already nodded at.
- **Written process SLAs exist** (24 h critical fix, weekly report, 7-day feature assessment). They are about responsiveness, not system latency or uptime, so the "no SLA in the SOW/quote" line is still true — but "we never committed anything in writing" is not. Whether this pack was handed over as-is is the thing to confirm.
- The **weekly feedback summary** and the **formal-sign-off-before-build** rule are exactly the two mechanisms that would have stopped scope creep. Both lapsed. Reinstating them costs nothing and is defensible as "back to the kickoff agreement".
- The April gap list is a ready-made regression checklist; several items (long-conversation memory, multi-criteria search, confident wrong answers) are still live complaints in the July survey.

## Action items

- [ ] Confirm whether the April kickoff pack (with the 24 h / 5-day / 10-day fix SLAs and the 7-day feature-assessment promise) was delivered to IKEA (Shai, with Arnon/Tali)
- [ ] Produce the approved customer-journey list promised in the 3 Jun deck — this is the DoD artefact IKEA has already seen the frame for (Shai, with Tali)
- [ ] Reinstate the weekly written feedback summary and the sign-off-before-build rule, citing the kickoff pack as the source (Shai)
- [ ] Open `ikea-status-29-07-26.html` in a browser and capture what was shown to IKEA on 29 Jul; it is the latest client-facing status and unreadable as text (Shai)
