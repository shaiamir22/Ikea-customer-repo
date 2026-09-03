# Discovery round with IKEA stakeholders — 16–17 Feb 2026

- Source: Drive `Summary Meetings` (Google Doc, three meeting summaries, Hebrew). Read 2026-09-03. Written by the Moveo side at the time.
- Moveo attendees: Arnon Meltser, Or Baruchim. IKEA attendees vary per meeting.
- Why it matters: this is where the requirement list came from, and where the two unresolved product tensions (path vs. shortcut; website vs. WhatsApp) were first stated. Neither has been resolved since.

## 1. Avi Yoktan — store experience (16 Feb, 15:30–17:00)

Attendees: Arnon, Or; Avi Yoktan, Efrat, Nitzanta (IKEA).

- Classic in-store questions the agent should absorb: where do I get a cart / yellow bags / toilets / a specific department.
- Restaurant and food info (Wednesday buffet, free coffee before 9) — for customers *and* employees.
- Better website-to-store handover; "did you know" content (e.g. KALMAR is a Swedish town).
- **Free spare parts from Sweden** — an existing but unknown service; surface it via the bot.
- Everything already on the site — accessibility, hours, stock — should be reachable from the bot.
- The two reasons customers stop staff in-store: **wayfinding** and **item details** (spec, price, availability).

## 2. Avi Bar — VP Range (סמנכ"ל מגוון) (17 Feb)

Attendees: Arnon, Or; Avi Bar, Moni, Efrat (IKEA).

- **Systems of record:** all product data and decisions come from **PIA**. Product structure is **SPR** (a solution) containing several **ART** (items), each item sellable on its own. Each store runs its own ERP; everything flows into **SORM** (Service Office Management), which feeds the website. Website managed by a marketing web manager plus Moni (Range).
- **Range dynamics:** full range turns over every ~3 years; updated quarterly and more often. Stock and price management is per-store and dynamic.
- **Users are employees too**, not only customers; Efrat asked for separate employee/customer segmentation.
- UX asks: wishlists by category (the current one is clumsy); Arabic and French; better exposure of non-physical services.
- Wants the system to be a **management tool** — a dashboard (maybe free-text chat) to track what customers want. His core interest: **detecting demand**.
- **Concerns:** (1) the agent "shortcuts the path" through store/site and hurts exposure and impulse sales; (2) it kills browsing-for-inspiration; (3) product comparison is missing today and the agent must cover it.
- Attached a long "ideal capabilities" page: catalogue and comparisons; design advice by material/colour/style/size/price; modular-system configuration; care and cleaning; complementary products; what's in the box and what to add; technical filters ("only solid wood"); extended-warranty flags; usage limits (weight, wet rooms, outdoor); country of origin; **package count/size/weight and "does it fit in car model X"**; inspiration images mid-conversation; Waze to the right store at the right hour; planner-tool support; B2B; kitchen-appointment booking across stores; small-space/rental fits; room-photo-based recommendations; payment-tier nudges ("add ₪100 for three instalments"); design tips (budget, style, hosting a table for 12, social trends, mattress/pillow fit by physiology); push on new collections and end-of-range; stock per store and location; back-in-stock push; shopping-list refresh on the day by stock/store; assembly videos; FAQ and customer recommendations; intent detection; purchase memory; "I'm here in the store, guide me".

## 3. Michal — VP Marketing (17 Feb)

Attendees: Arnon, Or; Efrat, Michal and one of her team (IKEA).

- Wants the agent to guide customers through **personal design worlds** by style and budget, learning from site content; use the internal **Toolbox** image library, including future collections.
- Post-purchase personalisation: complementary items, "style newsletter", push on relevant new collections.
- **Counter-view to Avi Bar:** customers *want* shortcuts; impulse "loading up" happens at the **end** of the journey, not mid-way — so leading straight to the product is fine.
- Ideas: a WhatsApp **group** with the agent for multi-person conversations; cross-referencing search/wish history with actual purchase (a gap today); a management dashboard on tastes, demographics, trends.
- **Concerns:** losing customers in the move from the functional website to WhatsApp — protect the value the site creates; **privacy** in personalisation is critical; there is an official **tone & style** document to hand over.
- Thinks restaurant/food info is **not** relevant to the agent's goals at this stage (disagreeing with Avi Yoktan).
- Action items recorded then: Michal to send the "messages" page for tone and branding; Arnon + Efrat to open a WhatsApp feedback group (done at the time).

## What is still open from this round

- Path vs. shortcut (Avi Bar vs. Michal) — never decided; the agent shipped as a shortcut.
- Website vs. WhatsApp attrition (Michal) — no measurement exists.
- Restaurant info — parked (requirements map #14).
- The tone-and-style handover happened (the PDF is in Drive `Context - Agent`), but "Tone & Style in the agent" was still unticked on the June requirements map.

## Action items

- [ ] Put the path-vs-shortcut question to Avi Bar and Michal together, with two weeks of live employee data, before the customer pilot design locks (Shai)
- [ ] Name Avi Bar's "detect demand" ask as the dashboard's headline use case — it is the cheapest way to make the VP Range an ally (Shai)
