# Internal IKEA sync — 2026-07-28 (contract scope and commercial reset)

- Attendees: Shai Amir, Arnon Meltser, Hai Morgenstern, David Mintz, Elad Kobi
- Source: Hebrew recording — transcript plus auto-summary. The auto-summary attributes nearly every line to a single speaker and is unreliable on attribution; points below are recorded as room decisions unless the transcript names someone unambiguously.
- Paper taken into the room: `../../whatsapp-agent/outputs/2026-07-28-internal-position-path-to-customers.md`
- Product half of this meeting: `../../whatsapp-agent/context/meetings/2026-07-28-internal-ikea-sync.md`

## Purpose

Align internally on what was promised to IKEA versus what has been delivered, and decide how the remaining work gets funded before the account lead takes it to the client.

## Key points

- **December is a decision gate, not a launch date.** What goes in front of IKEA's CEO is a working single-branch customer pilot plus data — not a promise of national coverage. The room treated this as the central reframe and agreed to say it with one voice. It is both stronger evidence and survivable with the team we have.
- **Nothing is committed in writing.** No SLA, latency target, or concurrency number appears in the SOW or the quote. This matters in both directions: we cannot claim to have met a bar that was never written, and IKEA cannot hold us to one either. The conclusion was that we define the bar ourselves now, rather than letting IKEA define it for us in December.
- **The client thinks we are already in the maintenance phase.** Efrat's understanding is that the project is in its SLA / bug-fix stage. That is not what the room believes the product's actual state is, and the gap has to be closed deliberately rather than left to surface on its own.
- **The project is fixed-price and running at a loss.** Finishing is estimated at roughly **₪140,000** of additional cost (about ₪70k/month for two months), with ₪200,000 named as the plausible worse case. The room was explicit that this is a consequence of taking a fixed-price project at too low a price and not finishing it on schedule — not something to bill IKEA for retroactively.
- **The recovery vehicle is new paid scope, not an overrun invoice.** The intent is to walk into the August meeting already knowing the number, and to recover it by selling the extensions IKEA actually wants — Shuki's new request being one live example — rather than asking to be paid more for work already promised.
- **The client meeting slips to the second half of August.** Efrat is travelling abroad and Avi follows her. It is to be run as a commercial meeting — current state, new scope, and price — not a status review and not a future-ideas deck. The room specifically ruled out going in with an open-ended discussion.
- **The retainer boundary has to be written down.** While it stays undefined, every new request lands inside it by default. Agreeing the boundary internally comes before putting it to IKEA.
- **A post-mortem was requested** on why a fixed-price project ran roughly four months past plan and is still not finished. Raised as a genuine question to answer, not an accusation — the room noted the slip is not one-sided, since IKEA pushed the pilot more than once and the sale period moved it again.
- **A fraud-detection environment has been billing ~$250/month for about three months** with nobody using it — it fell between the chairs. The base is ready and the workstream is still gated on a coordinated conversation with IKEA's CISO. Worth reviving in the business conversation rather than quietly cancelling.
- **The ~₪150k/month ambition is a team goal, not a project commitment.** Recorded here so it stops leaking into scope discussions about this project. Getting there means more IKEA projects, not more unpaid scope on this one.

## Next steps

- **Shai:** book the second-half-of-August client meeting once the work plan exists, and prepare the scope-and-price framing for it.
- **Leadership (Hai, David, Elad):** agree the retainer boundary internally, and decide who carries the arrears conversation.
- **Shai, with Arnon:** price the delta list — the items that sit outside the retainer — so the August meeting has real numbers.

## Action items

- [ ] Agree the retainer definition of done internally, then put it to IKEA (Shai, with Hai/David/Arnon)
- [ ] Price the delta list of out-of-retainer items ahead of the August meeting (Shai, with Arnon)
- [ ] Book the commercial meeting with IKEA for the second half of August — scope and price, not a status review (Shai)
- [ ] Run the post-mortem on why the fixed-price project ran ~4 months past plan (Shai, with Arnon)
- [ ] Attach the arrears conversation to the scope reset rather than running it separately — confirm owner via Elad/Eldar (Elad Kobi)
- [ ] Revive fraud detection in the business conversation and stop or use the ~$250/month environment currently idle (Shai)
- [ ] Arrange the coordinated CISO conversation that gates fraud detection (Shai)
