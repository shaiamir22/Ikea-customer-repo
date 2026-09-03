# Drive archive — `M.ai shared › Clients › IKEA` folder index

- Ingested: 2026-09-03 (Shai). Folder id `1CY2UskhBZyxC7w3y-5ieNIj2GQj0z75Y`, created 2026-01-21 under the shared-drive `Clients` folder — the Arnon-era account archive, Jan–Jul 2026.
- Why this lives at customer level: the folder mixes commercial paper (SOW, quote) with the whatsapp-agent workstream. Each item below was read and digested into the note named; anything that could not be read is flagged at the bottom.
- Everything in this folder pre-dates the 2026-07-21 handover except the retainer deck and the survey. It is the paper trail behind "what was promised vs. what was delivered".

## Files at the root

| File (Drive title) | Date | What it is | Digested to |
|---|---|---|---|
| IKEA Whatsapp Agent - SOW | 2026-01-21 | Original English SOW: two milestones (20 + 28 business days), AWS serverless + Twilio + LangGraph + Claude, web-scraping (no API), cost-optimisation strategies | `../comms/2026-01-29-sow-and-price-quote.md` |
| Ikea - הצעת מחיר | 2026-01-29 (edited to 2026-04-16) | Hebrew price quote + general T&Cs: ₪109,546 fixed + ₪10,000/mo support, payment and termination terms | `../comms/2026-01-29-sow-and-price-quote.md` |
| תוכנית עבודה_ IKEA Smart Agent (docx) | 2026-02-03 | Elad Kobi's 10-week work plan, 3 Feb → 13 Apr 2026, weekly milestones | `../../whatsapp-agent/context/research/2026-03-31-original-work-plan-and-product-spec.md` |
| Summary Meetings | 2026-02-16/17 | Discovery meetings with Avi Yoktan, Avi Bar (VP Range), Michal (VP Marketing) | `../../whatsapp-agent/context/meetings/2026-02-17-discovery-round-avi-yoktan-avi-bar-michal.md` |
| Communication | 2026-02-18 | Draft week-1 client status email + "version 0.01" architecture note | `../../whatsapp-agent/context/comms/2026-02-19-week1-status-update-v0.01.md` |
| סוכן חכם IKEA – מפת דרישות לתיעדוף | 2026-02-22 (edited to 2026-06-16) | Requirements map: 28 items in/out, sources, three tension points | `../../whatsapp-agent/context/research/2026-02-22-requirements-map.md` |
| חיווי מלאי | 2026-02-26 | Moni's email explaining IKEA's stock-indicator logic (sellable vs. physical stock, colour rules) | `../../whatsapp-agent/context/comms/2026-02-26-moni-stock-indicator-logic.md` |
| IKEA_Agent_Product_Spec_EN (docx) | 2026-03-31 | Internal engineering spec: 23 features, each with success metrics (latency, accuracy, uptime) | `../../whatsapp-agent/context/research/2026-03-31-original-work-plan-and-product-spec.md` |
| תוספות ורעיונות שיווק לתיעדוף | 2026-06-16 | Marketing sync: three new requests (#29–31), all parked | `../../whatsapp-agent/context/meetings/2026-06-16-marketing-sync-new-requests.md` |
| ikea_wa_bot_qr.jpeg | 2026-06-24 | QR code for the WhatsApp bot (employee onboarding asset) | asset only |
| elal_ppt (Slides, 49 MB) | 2026-07-06 | **Misfiled.** El Al weekly digital status deck — not IKEA material. See flags. | not ingested |
| אסטרטגיה-סוכן-חכם-איקאה (docx) | 2026-07-12 | Strategy/prioritisation doc: impact vs. effort for the follow-on projects | `../../whatsapp-agent/context/research/2026-07-13-strategy-and-roadmap-deck.md` |
| ikea_digital_agent_guide.pdf | 2026-07-12 | 5-page Hebrew employee guide to the agent (search, ready solutions vs. planning modular systems) | text unreadable — see flags |
| מצגת-סוכן-איקאה-סטטוס-ומפת-דרכים-preview.pdf | 2026-07-13 | "M.ai × IKEA" status + roadmap deck: system-today numbers, near-term goals, roadmap, go-live ask | `../../whatsapp-agent/context/research/2026-07-13-strategy-and-roadmap-deck.md` |
| סקר שביעות רצון — דוח תוצאות.pdf | 2026-07-20 | Employee satisfaction survey results, 12–20 Jul (104 sent, 30 answered) | `../../whatsapp-agent/context/research/2026-07-20-employee-satisfaction-survey.md` |

## Subfolders

| Folder | Contents | Digested to |
|---|---|---|
| `Context - Agent` | IKEA Hebrew tone-of-voice guideline (2021, 6.7 MB); "Guidelines for presentation of general use products in child space v5.0 Apr 2025" (5.7 MB) | Reference assets for the agent's persona and safety rules. Not digested — use directly. |
| `Kickoffs` | `ikea_kickoff (1).docx` (Apr 2026, client-facing kickoff pack); `ikea-kickoff.html` (19.4, React bundle); `ikea-kickoff-30.04.26.html` (two-week summary) | `../../whatsapp-agent/context/comms/2026-04-15-kickoff-pack-and-progress-decks.md` |
| `Slides` | `ikea-progress-03-06-26.html` ("the road we travelled", DoD framing); `ikea-status-29-07-26.html` (JS bundle, unreadable); `Work plan deck: retainer focus` (+ a copy) | progress → kickoff note above; retainer deck → `../../whatsapp-agent/context/research/2026-07-29-retainer-work-plan-deck.md` |
| `Stores self service maps` | 10 PDFs — self-serve floor maps for Netanya, Rishon LeZion, Kiryat Ata, Beer Sheva, Eshtaol (English set Apr–Jun, Hebrew set 2026-07-05) | Assets feeding the aisle/bin and in-store navigation features. Not digested. |
| `VIDEOS` | `ikea-agent-teaser-30-sec.mp4`, `ikea-agent-mobile.mp4` (Jul 2026) | Demo/marketing assets. |

## Flags

- **`elal_ppt` is misfiled.** It is El Al's weekly digital status deck (6 Jul 2026), with El Al-confidential programme detail. It should be moved out of the IKEA folder. One line in it matters to us commercially: El Al is using **Wonderful** (the competitor) as an interim agent vendor alongside its own build — worth a note in the competitor picture, not in this repo.
- **Two HTML decks could not be read**: `ikea-status-29-07-26.html` and `ikea-kickoff.html` are JavaScript-bundled React pages. Rendering them needs a browser; the 07-29 status deck is the most recent client-facing status and is worth recovering by opening it.
- **`ikea_digital_agent_guide.pdf`** extracts as scrambled RTL text. Headings recovered: product search; ready-made solutions vs. personal planning for modular systems (PAX, BESTÅ, METOD); a mention of the 1,500-employee rollout. Open the PDF directly if the content is needed.
- **`gdrive_folder_id` was "not configured"** in both `CUSTOMER-STATUS.md` and `whatsapp-agent/CLAUDE.md`. Set on 2026-09-03 to this folder.
