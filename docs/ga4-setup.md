# GA4 + Google Ads — Click-by-click setup

A practical UI guide for finishing analytics configuration after the code-side work is done. Aimed at a non-technical operator (you or a VA). Follow top to bottom.

- **GA4 property:** `latablemarrakech` — Measurement ID **`G-J2QTMMMYLD`**
- **Google Ads conversion ID:** `AW-18017405402`
- **Site:** https://latablemarrakech.com

> Code is already deployed. This guide only covers the GA4 + Ads UI work.

---

## 1. Verify GA4 property and Measurement ID

1. Go to https://analytics.google.com and sign in with the account that owns the property (Account ID `387143309`, Property ID `527838372`).
2. In the left sidebar at the bottom, click **Admin** (the gear icon).
3. In the **Property** column, click **Data streams**.
4. Click **Web** at the top, then click the row for `https://www.latablemarrakech.com`.
5. On the right-hand panel, confirm:
   - **Measurement ID** = `G-J2QTMMMYLD`
   - **Stream URL** = `https://www.latablemarrakech.com`
   - **Enhanced measurement** is ON (toggle at top — leave defaults)
6. Close the panel.

If the Measurement ID does not match, stop and let the developer know — the code on the site will not be sending data to this property.

---

## 2. See new events in DebugView and Realtime

You need to confirm the new events (`whatsapp_click`, `email_click`, `phone_click`, `booking_enquiry_submit`, `scroll_depth`, `faq_open`) actually arrive in GA4 before doing the rest.

### Easiest way — use the QA page

1. Open a new browser window in **Incognito / private mode**.
2. Visit https://latablemarrakech.com/analytics-qa/?debug=1 (this is the internal test page — it intentionally is not linked from the public nav and is hidden from search engines).
3. Accept the cookie banner if it appears.
4. In a second browser tab, open https://analytics.google.com → property `G-J2QTMMMYLD` → left sidebar → **Reports** → **Realtime**.
5. Back on the QA page, click each test card in turn:
   - Click **Test WhatsApp button** → Realtime should show `whatsapp_click` within ~30 seconds.
   - Click **Test email link** → Realtime should show `email_click`. (Cancel the mail-client window if one opens.)
   - Click **Test phone link** → Realtime should show `phone_click`.
   - Submit the **Booking enquiry test form** → Realtime should show `booking_enquiry_submit`.
   - Open the **Test FAQ** disclosure → Realtime should show `faq_open`.
   - Slowly scroll the page top-to-bottom → Realtime should show `scroll_depth` (with parameter `depth_percentage` = 25, 50, 75, 90).
6. The test cards on the page also light up green as each event fires — useful sanity check independent of GA4.

### DebugView (optional, more detail per event)

DebugView shows every event with its parameters in real time, so it is the definitive way to confirm each parameter is being sent.

1. In the same Incognito window with the QA page open, install the Chrome extension **GA Debugger** (search the Chrome Web Store for "Google Analytics Debugger" — official one is published by Google).
2. Click the extension's icon to switch it to **ON** (the icon turns blue).
3. Reload the QA page.
4. In GA4 → left sidebar → **Admin** → under **Data display** → click **DebugView**.
5. Select your debug device from the dropdown at the top (it shows a generated label for your browser).
6. Trigger an event on the QA page. Within a few seconds it appears in DebugView with all parameters expanded — confirm `cta_label`, `cta_position`, `link_url`, `button_location` etc. are populated.

---

## 3. Mark events as Key Events (formerly "conversions")

Until you mark an event as a Key Event, GA4 only counts it for general reports — bid strategies in Google Ads cannot use it. Do this for the two business-critical ones first.

1. In GA4 → left sidebar → **Admin** → under **Data display** → **Events**.
2. Wait until each new event has appeared in this list (it can take 24 hours after the first time the event fires). Refresh occasionally.
3. When `whatsapp_click` shows up:
   - Find the row.
   - In the right-hand column **Mark as key event**, click the toggle so it turns blue.
4. Repeat for `booking_enquiry_submit`.
5. Optionally also do `email_click` and `phone_click` if you want phone/email to count as conversions.
6. To verify, go to **Admin** → **Data display** → **Key events**. You should see your toggled events listed there.

> **You only need to do this once per event.** It does not need re-doing if the underlying code changes.

---

## 4. Create custom dimensions

By default, GA4 ignores the parameters attached to your events when building reports. To filter and group by `form_id`, `group_size`, etc., each parameter has to be registered as a **custom dimension** first.

1. In GA4 → left sidebar → **Admin** → under **Data display** → **Custom definitions**.
2. Click the blue **Create custom dimension** button (top right).
3. Fill in the dialog as below, click **Save**, then repeat for each row in the table.

| Dimension name (you choose) | Scope | Event parameter | Description (optional) |
|---|---|---|---|
| Form ID | Event | `form_id` | Which booking form was submitted (`booking-home`, `booking-contact`, etc.) |
| Form name | Event | `form_name` | Same value as Form ID — kept separate for future divergence |
| Group size | Event | `group_size` | Number of guests on the enquiry |
| Occasion | Event | `occasion` | Birthday / anniversary / business / wedding / family |
| Has date | Event | `has_date` | Whether the enquiry included a date |
| Has email | Event | `has_email` | Whether the enquiry included an email |
| Has notes | Event | `has_notes` | Whether the enquiry included a notes field |
| WhatsApp button location | Event | `button_location` | Which page the WhatsApp click came from |
| WhatsApp CTA position | Event | `cta_position` | Where on the page (hero, navbar, sticky, footer, etc.) |
| WhatsApp CTA label | Event | `cta_label` | The button text or aria-label |
| Device | Event | `device` | mobile or desktop |

> All dimensions are **Event-scoped** (the parameter lives on the event itself, not the user). Leave the **Scope** dropdown on **Event** for every row.

4. After saving, the dimensions take **24–48 hours** to start appearing in standard reports. They are usable in **Explore** (Reports → Explore) immediately for any new data that arrives.

---

## 5. Link GA4 to Google Ads

If GA4 is not already linked to Google Ads, do this. The link is what lets you import GA4 events as Google Ads conversions.

1. Go to https://analytics.google.com → **Admin** → **Property** column.
2. Scroll down to **Product links** → click **Google Ads links**.
3. If you already see one or both of `665-792-1235` or `999-576-6435` listed with status **Linked**, you can skip this section.
4. Otherwise click **Link**.
5. Click **Choose Google Ads accounts** → check the box for the Google Ads account you want to link → **Confirm**.
6. Click **Next**.
7. Leave **Enable Personalised Advertising** ON.
8. Click **Next** → **Submit**.

It takes a few minutes for the link to propagate.

---

## 6. Import GA4 conversions into Google Ads

Now wire `booking_enquiry_submit` (and optionally `whatsapp_click`) into Google Ads as conversions so Smart Bidding can use them.

1. Go to https://ads.google.com and sign in.
2. In the top-right cog **Tools** → in the left panel under **Measurement** → click **Conversions**.
3. Click the blue **+ Create conversion action** button.
4. Choose **Import** → choose **Google Analytics 4 properties** → choose **Web** → **Continue**.
5. You will see a list of GA4 properties + their Key events. Find `booking_enquiry_submit` from the `latablemarrakech` property.
   - If it is missing, you have not yet marked it as a Key Event in GA4 (Section 3) OR the event has not fired yet.
6. Tick the row → click **Import and continue**.
7. On the next screen, set:
   - **Conversion category** → `Submit lead form`.
   - **Value** → either **Don't use a value** OR **Use the same value for each conversion** with `85` `EUR` (your starting price — this is a placeholder).
   - **Count** → `One` (each form submit counts once per session).
   - **Click-through conversion window** → 30 days.
   - **View-through conversion window** → 1 day.
   - **Attribution model** → `Data-driven` (default in newer accounts).
8. Click **Save**.
9. (Optional) Repeat 3–8 for `whatsapp_click`. For this one set:
   - **Conversion category** → `Contact`.
   - **Value** → leave empty or set to a small number like `5 EUR` (intent signal, not a confirmed booking).
   - **Count** → `Every` (each click is a separate intent signal).

After 24–48 hours Google Ads will start using these for Smart Bidding, but **don't switch any campaign to "Maximize conversions" until you have at least 30 imported conversions in the last 30 days** — otherwise the algorithm doesn't have enough signal.

---

## 7. (Optional) Build an Exploration to see all this together

Once custom dimensions exist (Section 4), you can pivot WhatsApp clicks by page + button location.

1. GA4 → left sidebar → **Explore** → **Blank** template.
2. **Variables** column on the left:
   - **Dimensions** → click **+** → search and add: `Event name`, `Page path and screen class`, `WhatsApp button location`, `Form ID`, `Group size`, `Occasion`.
   - **Metrics** → click **+** → add `Event count`, `Total users`.
3. **Settings** column in the middle:
   - **Technique** → `Free form`.
   - **Rows** → drag `Event name`, then `Page path and screen class`, then `WhatsApp button location`.
   - **Values** → drag `Event count`, `Total users`.
   - **Filters** → drag `Event name` → set to `exactly matches` → enter `whatsapp_click`. Add another row with `booking_enquiry_submit` to see both events at once.
4. Top-right rename to **"Conversion events by page"** and save.
5. Bookmark this Exploration for weekly review.

---

## Daily / weekly checks

- **Daily (first 14 days after launch):** GA4 → Reports → Realtime. Click a WhatsApp button on the live site. Confirm `whatsapp_click` appears.
- **Weekly:** Open the saved Exploration above. Look for: which pages drive the most `whatsapp_click`s, which forms get the most `booking_enquiry_submit`s, what `group_size` and `occasion` people pick most often.
- **If a number suddenly drops to zero:** check (a) is gtag still loading on the affected page (DevTools → Network → filter `gtag`), (b) did the cookie banner break (`localStorage.cookie_consent` should equal `'accepted'`).

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Realtime shows nothing after clicking | gtag never loaded — visitor scrolled before the 5-second timeout? Network blocked? Cookie banner not accepted? | Open DevTools → Network → filter `gtag` → reload + scroll. Should see `googletagmanager.com/gtag/js?id=AW-18017405402` returning HTTP 200. If declined cookies, no events flow to GA4 by design. |
| Event appears but parameter is missing in reports | Custom dimension not registered yet, OR registered <24h ago | Check **Admin → Custom definitions**. Wait 24–48h after creating dimensions before they show in standard reports (Explore is faster). |
| Event fires twice | Some legacy per-page handler is still wired up. The global listener has its own deduper but inline page scripts might fire on top. | Search HTML for the event name. There should only be one global handler in the `PERF:ANALYTICS-RICH` block. |
| Google Ads doesn't see the conversion | Ads ↔ GA4 link missing OR event is not yet a Key Event in GA4 OR <24h since the link | Repeat Sections 3 and 5. After linking, wait one full day. |

---

## Reference

- Code-side architecture & event catalog → [`analytics.md`](./analytics.md)
- Original WhatsApp setup notes → [`../GA4-WHATSAPP-SETUP.md`](../GA4-WHATSAPP-SETUP.md)
- Google Ads conversion details → [`../GOOGLE-ADS-SETUP-GUIDE.md`](../GOOGLE-ADS-SETUP-GUIDE.md)
- Internal QA page → https://latablemarrakech.com/analytics-qa/?debug=1
