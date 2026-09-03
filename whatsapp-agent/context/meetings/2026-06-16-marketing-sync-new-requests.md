# Marketing sync — three new requests, all parked (16 Jun 2026)

- Source: Drive `תוספות ורעיונות שיווק לתיעדוף` (Google Doc, "requirements map and new ideas — marketing meeting 16.06.26"). Read 2026-09-03. Written by the Moveo side for management prioritisation.
- IKEA attendees implied by attribution: Efrat (marketing), Michal (marketing), Shai (IKEA marketing — not Shai Amir).

## Requests

| # | Request | Source | Product / tech implication | Decision recorded |
|---|---|---|---|---|
| 29 | **Sync with store purchase/receipt systems** — user enters a receipt/purchase id and gets assembly instructions and key purchase info in WhatsApp | Efrat | Needs CRM/POS integration; strong post-purchase value | Not proceeding for now |
| 30 | **Generative visualisation of the cart** — an AI-rendered room containing everything in the user's cart | Michal | Needs a visual generative model; high marketing/sales potential, heavy and slow in WhatsApp | Not proceeding for now |
| 31 | **Hand over conversation context to customer service** when escalating to a human, so the customer does not repeat themselves | Shai (IKEA marketing) | Needs bot ↔ contact-centre integration; key to a smooth experience | Not proceeding for now |

## Tension points flagged for management

1. **Escalation frustration** — Shai (IKEA) named the core pain: customers handed to a human start from zero. Costs dev time but is the lever for load reduction and retention. Decision needed on whether it joins the next core version.
2. **Wow vs. weight** — Michal's cart visualisation is a marketing effect that could lift conversion but risks long WhatsApp latency. Decision: separate POC or wait.
3. **Post-purchase value** — Efrat's receipt link turns the agent from a pre-purchase tool into a post-purchase companion; a conceptual shift that needs IKEA to open sensitive APIs.

## Why it matters now

- All three reappear in the July strategy doc and the retainer deck's upsell list (#29 → "order & delivery status / receipts", #31 → "human handoff with context"). Both are now recorded as **blocked on IKEA access** — and the e-commerce API request was declined once, also in June.
- These are the concrete, IKEA-sourced items to price for the August commercial meeting. They were asked for by marketing, not invented by us.
- Note the name collision: there is a Shai on IKEA's marketing side. Attribution in notes must say which Shai.

## Action items

- [ ] Carry #29 and #31 into the August scope-and-price list as IKEA-originated asks, each with its access dependency named (Shai Amir)
- [ ] Ask Efrat who owns the e-commerce/CRM API decision after the June decline, so the dependency has a name (Shai Amir)
