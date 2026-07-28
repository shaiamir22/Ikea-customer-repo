# Arnon — how he sees the project continuing (2026-07-27)

Conversation with Arnon on the shape of the work going forward. He splits it into three buckets: improvements inside the existing retainer, possible paid scope to pin down with the client, and the team's longer-term ambition. Fraud detection sits slightly apart — largely ready, but gated on client approval.

## 1. Retainer scope (improvements included in current work)

- **Cost reduction** — still the headline item.
- **Bandwidth** — the agent must handle ~100 concurrent messages.
- **Model routing away from Gemini** — configuration approved for the existing flow.
- **Search quality** — currently limited on semantically complex queries. Example: "ארונית קלה" should surface "כוורת". Need to raise the odds of finding the right product when the phrasing isn't literal.
- **Latency, latency, latency** — and quality generally. Repeated for emphasis.

## 2. Possible paid scope (to pin down with the client)

Framed as growing the team on the back of paid work:

- Additional products.
- Requests and "dreams" from the client.
- Low-hanging fruit.
- Prioritize by development difficulty against business importance (X-Y).

## 3. The ambition

- ~₪150k/month across roughly 3 people — which means growing the number of projects with IKEA.

## Fraud detection

The base is ready. To start the project, we need a coordinated conversation with IKEA's CISO first. Treated as a real near-term possibility rather than a hypothetical, but it needs client approval before anything begins.

## Other

- **Netanya branch** — a visit can be scheduled. Worth doing, 3 hours minimum.
- **Standing Wednesday brief** — set one up; agree the format and whether the character of the meeting varies week to week with the team.

## What I need out of this

Shai's own read on what the conversation has to produce — written up after the fact, and the input he took into the 2026-07-28 internal sync.

- **An ordered product work plan that descends to technical detail.** Product content is Shai's; the technical breakdown belongs to Tali and Niv.
- **A definition of the initial product** — what it is and what it contains, so there is something to call done.
- **Cost reduction with a real target.** Currently ~0.1 agorot per message, which at the loads we committed to support comes out around ₪50,000/month — not sensible, and nobody will pay it. Needs to come down to ₪5,000–8,000. Benjamin may be needed for this, so the planning has to decide whether to involve him, how many people the project needs, and whether this is base scope or an extension.
- **Bandwidth defined to the smallest detail** — exactly which loads we intend to stand behind: how many messages, how many users, and so on.
- **Model routing with an orderly fallback**, plus the conclusions the specialists owe us: does the new lighter model pass our quality checks, and where is the eval set?
- **Search quality is deferred.** It can be fixed gradually, but it is not part of the initial product we want to support for the December customer release, even at a single branch.
- **A latency target per message**, and the route to reaching it.
- **Everything else split off separately** — anything that is a plan for later, saleable, or a commercial extension.

Fraud detection fell between the chairs and is worth returning to in the business conversations. The ~₪150k/month ambition is a team goal rather than a project one.

## Action items

- [ ] Pin down with the client which items are retainer vs. paid scope
- [ ] Prioritize the paid-scope candidates by difficulty vs. importance
- [ ] Arrange the coordinated CISO conversation before starting fraud detection
- [ ] Schedule the Netanya branch visit (3+ hours)
- [ ] Set up the standing Wednesday brief and agree its format with the team
- [ ] Decide whether Benjamin's cost work is base scope or a separate extension, and how many people the project needs
- [ ] Get the eval set located and confirm whether the lighter routed model passes quality checks
