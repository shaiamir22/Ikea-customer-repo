# IKEA daily status sync — 2026-07-22

- Title (client-side): "פגישת סטטוס פרויקט - סוכן חכם איקאה - July 22"

## Purpose

Review project status, address stability issues, and plan for the upcoming employee rollout.

## Key points

- **Stability fix needed:** a fallback model is required to prevent agent crashes caused by external API failures (e.g. Gemini server issues). The agent crashed multiple times the prior day, halting Efrat's (employee tester) work. Root cause hypothesis: unstable Gemini servers, possibly tied to new model deployments upstream.
- **Employee rollout:** ~1,000 employees get access around **August 1st** — a high-stakes trial period ahead of a potential public launch in December. A disclaimer will warn users about possible AI errors; the project team will provide 24/7 support for the first 1-2 months.
- **Public launch decision (Dec):** the CEO will review agent performance in December to decide on a public launch. Success is critical to secure investment from the American owners, who hold high performance standards. The CEO will be added to the agent's user list for a passive review in the meantime.
- **Strategic feature priority:** integrating with the delivery/assembly status system is the top priority — it automates a high-volume customer service query and reduces call center load. Strategic focus stays on shopping assistance, not design tools.
- **Future vision (phase 3):** capture the full customer journey by linking agent interactions to in-store purchases; add food menus, allergy info, and mobile ordering for the restaurant.
- **Planning cadence:** a new team member ("Pistachio") will help structure a formal roadmap (short/medium/long-term) to avoid the unfocused effort of the past.
- Business framing: the agent is seen internally as a "game-changer" for product-catalog search and assembly guidance, already surpassing the official IKEA website — a stable launch is non-negotiable to avoid negative internal perception.

## Next steps

- **Arnon's team:** investigate the Gemini server crash to confirm root cause; implement the fallback model for service continuity; add the CEO to the agent's user list.
- **Avi & Efrat:** begin onboarding employees to the agent around August 1st.
- **Shai:** prepare a roadmap proposal for the next planning meeting — big-picture strategic goals, quick-win features (e.g. delivery status), and a data collection strategy.
- **All:** schedule a follow-up meeting to define the product roadmap.

## Action items

- [ ] Investigate the Gemini-outage crash root cause (Arnon's team)
- [ ] Implement a fallback model for service continuity (Arnon's team)
- [ ] Add the CEO to the agent's user list (Arnon's team)
- [ ] Begin employee onboarding ~Aug 1 (Avi & Efrat)
- [ ] Prepare a roadmap proposal — strategic goals, quick wins, data strategy (Shai)
- [ ] Schedule a follow-up meeting to define the product roadmap (all)
