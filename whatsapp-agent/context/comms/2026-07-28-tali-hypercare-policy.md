# Tali — Hypercare / availability policy for the employee release (2026-07-28)

Received by WhatsApp from Tali, to be stated at the IKEA morning meeting on 2026-07-29 ahead of
the 1,500-employee release. Passed to Shai to confirm against our own notes before it goes to the
client.

## Text as received (Hebrew, verbatim)

> במהלך שלושת הימים הראשונים לאחר העלייה לאוויר, צוות הפיתוח יעבוד במתכונת Hypercare על מנת להבטיח מענה מהיר לתקלות.
>
> מדיניות הזמינות:
> • ⏱️ Acknowledgment לכל תקלה – עד 15 דקות.
> • 🚨 תקלות קריטיות – יעד למענה/תיקון בתוך כשעה מרגע הדיווח (בהתאם לאופי התקלה).
>
> מדיניות זו תהיה בתוקף עד לעדכון סטטוס נוסף.

## Translation

During the first three days after go-live, the development team will work in Hypercare mode to
ensure fast response to incidents.

Availability policy:
- Acknowledgment of any incident — within 15 minutes.
- Critical incidents — target response/fix within about an hour of report (depending on the nature
  of the incident).

This policy is in force until further status update.

## Reconciliation against our own notes — three gaps

These are unresolved as of writing. Each one is a commitment that lands on a team of effectively
one developer during launch week (Tali is out for two weeks from 2026-08-02).

| # | Tali's text says | Our record says | Source |
|---|---|---|---|
| 1 | Hypercare for **3 days** | IKEA was told **24/7 support for the first 1-2 months** | 2026-07-22 status sync; internal position paper §4 G0 ("24/7 support staffed in writing — two people") |
| 2 | Critical incidents fixed **within ~1 hour** | Two-tier policy: acknowledge fast, **fix allowed to take hours** | 2026-07-28 internal sync; PRD §4 US-02 |
| 3 | — | Acknowledge **≤15 min** | Matches. No gap. |

**Gap 1 is the one the client will notice.** Moving from "24/7 for 1-2 months" (stated 2026-07-22)
to "Hypercare for 3 days" is a narrowing of a commitment already made. It may well be the right
call given the team we have, but it should be said deliberately rather than slipped in — otherwise
it surfaces later on IKEA's terms.

**Gap 2 tightens a commitment the room deliberately loosened.** On 2026-07-28 the agreed policy was
explicitly that the fix may take hours. Committing to ~1 hour for critical incidents is a harder
bar than we agreed internally, with fewer people than we assumed.

_Decision owed by Shai before the 2026-07-29 morning meeting._
