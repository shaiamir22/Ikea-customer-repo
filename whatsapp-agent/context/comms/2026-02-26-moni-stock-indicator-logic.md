# Moni (IKEA Range) — how IKEA's stock indicator actually works (26 Feb 2026)

- Source: Drive `חיווי מלאי` (Google Doc — an inbound email from Moni, Range/website, following a call the day before). Read 2026-09-03.
- Why it matters: this is the authoritative rule set behind the stock colours the agent shows. Track 05 of the retainer plan (data & feed accuracy) rests on it.

## Sellable vs. physical stock

- The website shows **only sellable stock** — units a customer can pick up now. Example HEMNES 2-drawer chest (80242627), Netanya: site shows **18**, store physically holds **70**.
- Breakdown of the 70: `STOCK SELLABLE` 18 (the only figure the site uses); `INCL AS SELLABLE` 48 — high-bay / distribution-centre stock not reachable on the sales floor; 3 units on display, counted under `BLOCKED LOCATION`; 1 unit sold but not yet posted (`QTY SOLD NOT POSTED`), deducted afterwards.
- Implication for the agent: "in stock: 18" is correct by IKEA's own definition even when the store has far more. Any answer that shows physical stock would contradict the site.

## Colour rules (global IKEA rules, local tweaks only for warehouse-only items)

- **Green** — in stock.
- **Yellow** — low stock: system compares sellable quantity against average daily sales; below one day of sales turns yellow.
- **Red empty circle** — out of stock; shows an expected return date if one exists, otherwise "no expected return".
- **Red circle with a line** — not sold in this store. Almost never appears in Israel; usually a fault. Used to be the warehouse-only indicator; changed since.
- **Grey** — appears mainly during sales: discontinued item, no stock, no orders in transit; closed in the system.
- The same article can be grey in Netanya, green in Rishon, yellow in Kiryat Ata and red-empty in Beer Sheva at the same moment.
- **Warehouse-only items** (sold only via the distribution centre) get a unique yellow with the text "for more information please contact a sales representative in store".
- The indicator on the **category/list page differs from the product page** — different rendering rules; the agent should mirror the product-page logic.

## Action items

- [ ] Check the agent's stock-colour logic against these five rules, especially yellow (sales-velocity based, not a fixed threshold) and the warehouse-only case (Niv / Tali)
- [ ] Add Moni's example (HEMNES 80242627, 18 vs. 70) to the golden regression set as the canonical "sellable ≠ physical" case (Niv)
