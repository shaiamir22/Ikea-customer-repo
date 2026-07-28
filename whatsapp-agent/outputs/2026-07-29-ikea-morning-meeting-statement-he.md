# IKEA morning meeting statement — 2026-07-29 (Hebrew)

**For:** the 08:30 IKEA status sync, 2026-07-29 — Shuki, Avi (+ Efrat if present)
**Purpose:** confirm the release date move, state the availability policy, and show concrete
weekly progress rather than Sunday's plan.
**Author:** Shai Amir

> **Two things to settle before sending** — see the notes under the message.

---

## Message (Hebrew)

*עדכון סטטוס — סוכן ה-WhatsApp, לקראת ההשקה לעובדים*

*1. מועד ההשקה*
ההשקה ל-1,500 העובדים תתבצע ביום ראשון 2/8, ולא ביום חמישי 30/7. תקופת המבצע מסתיימת ב-30/7, ואנחנו מעדיפים לא להעלות שינוי רחב באמצע המבצע. הפרסום הפנימי, כולל הסרטון של אבי, ייצא אחרי סיום המבצע.

*2. פיצ'ר המבצע*
פיצ'ר המבצע יכובה לקראת ההשקה. ‎[לאשר את הניסוח המדויק]

*3. מה הושלם השבוע*
• *תמיכה מלאה באנגלית, מקצה לקצה.* שדה החומר וסוג המוצר מגיעים כעת מפיד PIA באנגלית רשמית — כיסוי 99.9% ו-100%, בלי תרגום מכונה. כל 31 כפתורי המתכנן תורגמו, יחידות המידה הומרו (ק"ג, ס"מ, ליטר), ו-Flow רשימת האיסוף באנגלית פורסם כ-Flow נפרד — כך שה-Flow בעברית לא נגע כלל ואין שום סיכון למשתמשים הקיימים.
• *ETA לחידוש מלאי.* כרטיס של מוצר שאזל מציג כעת תאריך הגעה צפוי מתוך הפיד, בניסוח זהה לזה שבאתר.
• *חוסן הזנת המלאי.* הפיד נקרא לפי כותרות עמודות במקום לפי מיקום, עם התראה אוטומטית על שינוי סכימה. זו הייתה נקודת שבירה אמיתית.
• *משמעת מתכנן החלל.* המתכנן מופיע רק כשהלקוח מבקש אותו במפורש — באכיפה כפולה, גם בהנחיה וגם בשער דטרמיניסטי ביציאה.
• *התאוששות עצמית.* עותק פגום של מסד המוצרים המקומי מתקן את עצמו בכל המסלולים — חיפוש, פרטי מוצר ובדיקת מלאי — ולא רק באחד מהם.
• *ניטור איכות.* דשבורד חדש: אחוז כשלים, חיפושים ריקים, תשובות מעל 10 שניות ונטישות. בנוסף הפרדנו בדוחות בין לקוחות אמיתיים לעובדים פנימיים, כך שהמספרים אמינים.

*4. מה נשאר עד יום ראשון*
• רשימת תורנויות שמית לימי ההשקה.
• בדיקות אחרונות על מסלול ה-fallback בין ספקי המודל, כדי שתקלה אצל הספק לא תפיל את הסוכן כפי שקרה ב-21/7.
• בדיקת קצה-לקצה של קישור מעקב המשלוח וההרכבה.

*5. מדיניות זמינות בהשקה*
במהלך שלושת הימים הראשונים לאחר העלייה לאוויר, צוות הפיתוח יעבוד במתכונת Hypercare על מנת להבטיח מענה מהיר לתקלות.

מדיניות הזמינות:
• ⏱️ Acknowledgment לכל תקלה – עד 15 דקות.
• 🚨 תקלות קריטיות – יעד למענה/תיקון בתוך כשעה מרגע הדיווח (בהתאם לאופי התקלה).

מדיניות זו תהיה בתוקף עד לעדכון סטטוס נוסף.

*6. מה בעבודה בשבוע הבא*
• *מנוע ידע מדורג.* היום הסוכן עונה על שאלות שירות מתוך כ-50 קבצים שנבחרו ידנית. המנוע החדש מכסה כ-1,383 עמודי תוכן מהאתר ב-26 קטגוריות, עם חומה בין קטגוריות כך ששאלה על החזרות לא יכולה להיענות מעמוד השראה. הקוד כבר כתוב ומכובה בייצור — בשבוע הבא הוא עולה ל-staging עם eval וקנרי לפני הפעלה.
• *שיפור נוסף בדיוק החיפוש* — השלב הבא שסוכם אחרי מדידות החודש.
• *מעקב הקשר בין תורות* — המקרים שבהם הסוכן מאבד לאיזה מוצר הלקוח מתייחס.

---

## Before sending — two open items

### 1. The sale-feature line (§2) is a placeholder

The instruction was ambiguous between two readings, and they say different things to the client:

- **(a)** A sale/promotions feature *in the agent* gets switched off ahead of the release.
- **(b)** Some other feature is switched off *for the duration of the sale*, and comes back after.

Pick one and the line rewrites in a sentence. Note the engineering brief lists proactive
messaging — restock and sale alerts — as blocked on consent and scheduling, i.e. not built, so if
the point is about sale alerts, the honest framing is that it is not shipping rather than being
switched off.

### 2. The Hypercare policy narrows a commitment already made

Logged in full at `../context/comms/2026-07-28-tali-hypercare-policy.md`. Two gaps against our own
record:

- **3 days of Hypercare vs. the 24/7-for-1-2-months IKEA was told on 2026-07-22.** This is a real
  narrowing. It may be the right call, but say it deliberately — if it lands as a quiet swap it
  resurfaces later on IKEA's terms.
- **"Critical fixed within ~1 hour" is tighter than the room agreed on 2026-07-28**, which was
  acknowledge fast, fix allowed to take hours. It is a harder bar than we set for ourselves, being
  committed for a launch week when Tali is out and Niv is effectively solo.

The ≤15-minute acknowledgment matches our notes exactly — no issue there.

---

_Sources: engineering status brief 2026-07-28 (`../context/research/2026-07-28-engineering-status-brief.md`);
Tali's Hypercare text (`../context/comms/2026-07-28-tali-hypercare-policy.md`); internal sync
2026-07-28; IKEA status sync 2026-07-22._
