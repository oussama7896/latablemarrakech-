# GA4 + Google Ads — VA brief

A tight, copy-paste-able checklist for completing the dashboard work.
Aimed at someone who has access to GA4 + Google Ads but doesn't know the codebase.

- **GA4 property:** `latablemarrakech` — Measurement ID `G-J2QTMMMYLD`
- **Google Ads:** customer ID `665-792-1235` (or `999-576-6435` — both linked)
- **Internal QA URL:** https://latablemarrakech.com/analytics-qa/?debug=1
- **Time required:** ~45 minutes total
- **Reference (longer version with screenshots-worth of detail):** [`ga4-setup.md`](./ga4-setup.md)

> Do the sections in order. Don't skip ahead — Section 4 won't work until Section 3 is done, and Section 6 won't work until Section 5 is done.

---

## ☐ Section 1 — Confirm tracking is firing (5 min)

1. Open an **Incognito** browser window.
2. Go to https://latablemarrakech.com/analytics-qa/?debug=1
3. Accept the cookie banner if it appears.
4. Open DevTools (Mac: `Cmd+Option+I`, Windows: `F12`) → **Console** tab.
5. You should see: `[ANALYTICS DEV] enabled — set localStorage.analytics_debug="0" to silence`
6. Click each test card on the page and watch the console:
   - ☐ Click **Test WhatsApp button** → console shows `[ANALYTICS DEV] whatsapp_click {...}`
   - ☐ Click **Test email link** (cancel the mail window) → `[ANALYTICS DEV] email_click {...}`
   - ☐ Click **Test phone link** → `[ANALYTICS DEV] phone_click {...}`
   - ☐ Submit the **Booking enquiry test form** → `[ANALYTICS DEV] booking_enquiry_submit {...}` containing `form_id: "booking-test"`, `group_size: "6"`, `occasion: "anniversary"`
   - ☐ Open the **Test FAQ** disclosure → `[ANALYTICS DEV] faq_open {...}`
   - ☐ Scroll slowly to the bottom → 4 lines `[ANALYTICS DEV] scroll_depth { depth_percentage: 25 / 50 / 75 / 90, ... }`

If any one of these does NOT fire, **stop here and ping the developer with a screenshot of the console**. Don't continue — the dashboard work below depends on every event being live.

---

## ☐ Section 2 — Confirm events appear in GA4 Realtime (5 min)

1. In a second tab, go to https://analytics.google.com → property `G-J2QTMMMYLD` → left sidebar → **Reports** → **Realtime**.
2. Back on the QA page, repeat any one of the actions above (e.g. click WhatsApp).
3. Within 30 seconds, the event name should appear in the **"Event count by event name"** card on Realtime.
4. ☐ Confirm at least one of the new event names is visible there: `whatsapp_click`, `email_click`, `phone_click`, `booking_enquiry_submit`, `faq_open`, `scroll_depth`.

If Realtime stays empty, the most likely cause is the cookie banner — events sit in the queue but GA4 ignores them until consent is granted. In DevTools console, run `localStorage.getItem('cookie_consent')` and confirm it returns `"accepted"`.

---

## ☐ Section 3 — Mark events as Key Events (5 min, but wait 24h after first run if events aren't listed yet)

Path: **Admin** (gear, bottom-left) → under **Data display** → **Events**

For each event below, find its row in the list and toggle the **Mark as key event** column on the right (it turns blue).

- ☐ `whatsapp_click`
- ☐ `booking_enquiry_submit`
- ☐ `email_click` (optional, recommended)
- ☐ `phone_click` (optional, recommended)

If an event isn't in the list yet:
- It hasn't fired enough times. Trigger it on the QA page a couple more times.
- OR it's been less than 24 hours since the first time it fired. Come back tomorrow.

To verify: Admin → Data display → **Key events**. The toggled events should be listed.

---

## ☐ Section 4 — Register custom dimensions (15 min)

Path: **Admin** → under **Data display** → **Custom definitions** → **Custom dimensions** tab → **Create custom dimension** (top right).

Create one for each row below. Every dimension has **Scope = Event**.

| Dimension name | Event parameter |
|---|---|
| ☐ Form ID | `form_id` |
| ☐ Form name | `form_name` |
| ☐ Group size | `group_size` |
| ☐ Occasion | `occasion` |
| ☐ Has date | `has_date` |
| ☐ Has email | `has_email` |
| ☐ Has notes | `has_notes` |
| ☐ WhatsApp button location | `button_location` |
| ☐ WhatsApp CTA position | `cta_position` |
| ☐ WhatsApp CTA label | `cta_label` |
| ☐ Device | `device` |

For each one:
1. Click **Create custom dimension**
2. **Dimension name:** copy from the left column above
3. **Scope:** `Event`
4. **Description:** leave blank or paste the parameter name
5. **Event parameter:** copy from the right column above (must match exactly — case-sensitive, no spaces)
6. Click **Save**
7. Repeat

Custom dimensions take **24–48 hours** to appear in standard reports, but show up immediately in **Explore**.

---

## ☐ Section 5 — Confirm GA4 ↔ Google Ads link (2 min)

Path: GA4 → **Admin** → under **Property** → scroll to **Product links** → **Google Ads links**.

- ☐ Confirm at least one of `665-792-1235` or `999-576-6435` is listed with status **Linked**. If yes, skip to Section 6.

If neither is listed:
1. Click **Link** → **Choose Google Ads accounts** → tick the account → **Confirm**.
2. **Next** → leave **Personalised Advertising** ON → **Next** → **Submit**.

---

## ☐ Section 6 — Import conversions into Google Ads (10 min)

Path: https://ads.google.com → top-right **Tools** (wrench icon) → under **Measurement** → **Conversions** → **+ Create conversion action**.

Do this twice — once for the booking form, once for the WhatsApp click.

### 6A — `booking_enquiry_submit` (the priority one)

1. ☐ **Goal:** Import → **Google Analytics 4 properties** → **Web** → **Continue**
2. ☐ Find `booking_enquiry_submit` from the `latablemarrakech` property → tick the row → **Import and continue**
3. ☐ **Conversion category:** `Submit lead form`
4. ☐ **Value:** select **Use the same value for each conversion** → enter `85` → currency `EUR`
5. ☐ **Count:** `One`
6. ☐ **Click-through conversion window:** 30 days
7. ☐ **View-through conversion window:** 1 day
8. ☐ **Attribution model:** `Data-driven` (or whatever the default is)
9. ☐ Click **Save**

### 6B — `whatsapp_click` (intent signal)

1. ☐ Repeat steps 1–2 above, this time pick `whatsapp_click`
2. ☐ **Conversion category:** `Contact`
3. ☐ **Value:** `Don't use a value` (or `Use the same value` → `5` `EUR` if you want a placeholder)
4. ☐ **Count:** `Every` (each click = its own intent signal)
5. ☐ Same conversion windows + attribution as 6A
6. ☐ Click **Save**

After 24–48 hours, Google Ads will start using these signals for Smart Bidding.

> **Important:** Do NOT switch any campaign to "Maximize conversions" until you have at least **30 imported conversions in the last 30 days** — the algorithm needs that much volume to bid intelligently.

---

## ☐ Section 7 — Quick exploration to see it all (optional, 5 min)

Path: GA4 → left sidebar → **Explore** → **Blank** template.

1. ☐ Variables panel (left): add Dimensions `Event name`, `Page path and screen class`, `WhatsApp button location`, `Form ID`, `Group size`, `Occasion`. Add Metrics `Event count`, `Total users`.
2. ☐ Settings panel (middle): Technique = `Free form`. Drag `Event name`, `Page path and screen class`, `WhatsApp button location` into **Rows**. Drag `Event count`, `Total users` into **Values**. In **Filters**, add `Event name` `exactly matches` `whatsapp_click` (and optionally a second filter row for `booking_enquiry_submit`).
3. ☐ Top right: rename to **"Conversion events by page"** → click the disk icon to save.

This becomes your weekly review report.

---

## When you're done — report back

Send the developer a 1-line confirmation per section:

```
✓ Section 1 — events fire in console
✓ Section 2 — events appear in GA4 Realtime
✓ Section 3 — Key Events marked: whatsapp_click, booking_enquiry_submit, email_click, phone_click
✓ Section 4 — 11 custom dimensions created
✓ Section 5 — Google Ads link confirmed (account 665-792-1235)
✓ Section 6A — booking_enquiry_submit imported into Ads, value 85 EUR
✓ Section 6B — whatsapp_click imported into Ads, no value
✓ Section 7 — exploration saved (optional)
```

Or if anything is blocked, say which section + paste the error/screenshot.
