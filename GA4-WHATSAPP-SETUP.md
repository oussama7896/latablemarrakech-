# GA4 WhatsApp Conversion Tracking — Setup Guide

**Site:** latablemarrakech.com
**GA4 property:** `G-J2QTMMMYLD`
**Google Ads conversion ID:** `AW-18017405402`
**Implementation:** **gtag-only** (no GTM container — events fire directly from inline JS)
**Last updated:** 2026-05-01

---

## Architecture overview

Every WhatsApp link on the site has been tagged with two data attributes:

```html
<a href="https://wa.me/212721354757?text=…"
   data-event="whatsapp_click"
   data-location="home">
   Reserve your table
</a>
```

A small inline script at the bottom of every `<body>` listens for clicks on any element with `data-event="whatsapp_click"`. When clicked, it fires a GA4 event:

```javascript
gtag('event', 'whatsapp_click', {
  'button_location': '<the data-location value>',
  'link_url': '<the wa.me URL>',
  'page_location': '<window.location.href>'
});
```

**Why gtag-only and not GTM?** The site already uses lazy-loaded gtag (`requestIdleCallback`-deferred). Adding GTM would mean ~28 KB extra JS for one event. The inline listener is ~200 bytes and integrates cleanly with the existing consent-mode v2 setup.

---

## Page → location-slug mapping

| Page URL | `data-location` value |
|---|---|
| `/` | `home` |
| `/fr/` | `home_fr` |
| `/ar/` | `home_ar` |
| `/private-chef-cost-marrakech/` | `pricing` |
| `/marrakech-villa-with-private-chef/` | `villa-guide` |
| `/marrakech-cooking-class-vs-private-chef/` | `class-vs-chef` |
| `/services/wedding-dinner-marrakech/` | `weddings` |
| `/services/corporate-dining-marrakech/` | `corporate` |
| `/the-experience/` | `experience` |
| `/how-it-works/` | `how-it-works` |
| `/faq/` | `faq` |
| `/contact/` | `contact` |
| `/menus/` | `menus` |
| `/areas-we-serve/` | `areas` |
| `/blog/marrakech-medina-market-guide/` | `blog-medina-guide` |
| `/fr/chef-prive-marrakech/` | `service_fr` |
| `/fr/chef-prive-prix-marrakech/` | `pricing_fr` |
| `/fr/chef-a-domicile-marrakech/` | `domicile_fr` |
| `/fr/villa-marrakech-chef-prive/` | `villa-guide_fr` |
| `/fr/cours-de-cuisine-marrakech/` | `class-vs-chef_fr` |
| *(all other pages)* | `<slug>` per `quickwins-v2.py` SLUG_MAP table |

---

## PART A — GA4 event definition (already done by code)

| Field | Value |
|---|---|
| **Event name** | `whatsapp_click` |
| **Event parameters** | `button_location`, `link_url`, `page_location` |

**No setup needed in the code** — this is already firing on every page. You only need to do Parts B–D in the GA4 web UI.

---

## ~~PART B — GTM setup~~ *(SKIPPED — Option B has no GTM)*

If you ever decide to migrate to GTM later, this section can be filled in. For now, no action.

---

## PART C — Mark `whatsapp_click` as a Key Event in GA4

> **Why this matters:** Until you mark it as a Key Event (formerly "conversion"), `whatsapp_click` is just an event in the firehose — invisible to Google Ads bid strategies and to the Conversions report.

### Step-by-step

1. Open https://analytics.google.com → choose property **`G-J2QTMMMYLD`**
2. Left sidebar → **Admin** (gear icon, bottom-left)
3. Under "Property" column → **Events**
4. **Wait 24 hours after the deploy** for the event to start appearing here. (Events show up ~24h after they first fire in Realtime.)
5. When `whatsapp_click` appears in the events list:
   - Find the row → toggle the **"Mark as key event"** column on the right
   - The toggle turns blue when active
6. Verify by clicking **Admin → Property → Key events** — you should see `whatsapp_click` listed

### How to test it's working before the 24h wait

Open https://analytics.google.com → **Reports** → **Realtime**. Then:
1. Open the live site in a new tab
2. Click any WhatsApp button (it'll open WhatsApp in another tab — close that)
3. Switch to GA4 Realtime tab
4. Within ~30 seconds, look for `whatsapp_click` in the **"Event count by event name"** card

If you see it → the event is firing correctly. ✅
If not → see *Troubleshooting* at the bottom.

---

## PART D — Build the conversion exploration in GA4

> **Why this matters:** GA4's standard reports won't show `button_location` breakdowns by default. You need a custom Exploration to see *"how many clicks from the pricing page vs the villa guide vs the homepage."*

### Step-by-step

1. In GA4 → **Explore** (left sidebar) → **Blank** template
2. **Variables panel** (left column inside Explore):
   - **Dimensions:** click `+`, search & add:
     - `Event name`
     - `Page path and screen class`
   - **Custom dimensions:** click `+` → register `button_location` and `link_url` if not already registered (Admin → Custom definitions → Create custom dimension → Event-scoped, parameter name `button_location`, display name "WhatsApp Button Location")
   - **Metrics:** click `+`, add:
     - `Event count`
     - `Total users`
3. **Settings panel** (middle column):
   - **Technique:** Free form
   - **Rows:** drag in `button_location`, then `Page path and screen class`
   - **Values:** drag in `Event count`, `Total users`
   - **Filters:** drag in `Event name`, set to `exactly matches` → `whatsapp_click`
4. Name the exploration **"WhatsApp clicks by button location"**
5. Save

### What you'll see

```
button_location    Page path                                    Event count   Total users
─────────────────  ────────────────────────────────────────  ────────────  ───────────
home               /                                                   142            96
pricing            /private-chef-cost-marrakech/                        47            38
villa-guide        /marrakech-villa-with-private-chef/                  31            25
home_fr            /fr/                                                 18            14
weddings           /services/wedding-dinner-marrakech/                  12            10
…
```

This tells you which pages drive WhatsApp engagement, and lets you compare CTR per visit across pages.

---

## PART E — Verify in real time (post-deploy)

After Vercel finishes deploying:

1. Open https://analytics.google.com → **Reports → Realtime**
2. Open https://latablemarrakech.com in a new browser tab (preferably Incognito to avoid existing GA cookies confusing you)
3. **Important:** the gtag library is lazy-loaded. To see the event in Realtime, you need to **trigger the lazy-load first**: scroll the page, move your mouse, or wait 5 seconds. Only after that will `gtag.js` actually load.
4. Click any WhatsApp button. WhatsApp will open — close that tab.
5. Switch to GA4 Realtime. Within 30 seconds you should see:
   - `whatsapp_click` in **"Event count by event name"**
   - The user count in **"Users in the last 30 minutes"** matches your test session
6. Click WhatsApp buttons on different pages (`/`, `/private-chef-cost-marrakech/`, `/fr/`, etc.) and verify each shows a different `button_location` value

### Per-button verification checklist

For each page below, click the most prominent WhatsApp button and confirm the event fires with the expected `button_location`:

- [ ] `/` → `home`
- [ ] `/private-chef-cost-marrakech/` → `pricing`
- [ ] `/marrakech-villa-with-private-chef/` → `villa-guide`
- [ ] `/services/wedding-dinner-marrakech/` → `weddings`
- [ ] `/fr/` → `home_fr`
- [ ] `/fr/chef-prive-prix-marrakech/` → `pricing_fr`
- [ ] Sticky/floating WhatsApp button (any page) → matches that page's slug
- [ ] Footer "WhatsApp" link (any page) → matches that page's slug

---

## Bonus — Connect to Google Ads as a conversion

Once `whatsapp_click` is a Key Event in GA4, you can import it as a Google Ads conversion to optimize bids.

1. https://ads.google.com → **Tools & settings → Conversions**
2. **+ New conversion action** → **Import** → **Google Analytics 4 properties** → **Web**
3. Select property `G-J2QTMMMYLD`
4. Find `whatsapp_click` in the list → check it → **Import and continue**
5. Set the **Value** to a placeholder (e.g., €5 per click — refine later from your booking close-rate)
6. Set **Counting** to "Every" (because each click is its own intent signal — different from a confirmed booking)

After 24–48h Google Ads will start using this for Smart Bidding signals. **Don't switch your campaigns to "Maximize Conversions" yet** — you need 30+ conversions first.

---

## Troubleshooting

### "I clicked WhatsApp but Realtime shows nothing"

Most common cause: gtag.js never loaded. Fix:
1. Open browser DevTools (F12) → Network tab
2. Reload the page
3. Scroll the page or move your mouse (this triggers the lazy-load)
4. In the Network tab filter, type `gtag` — you should see a request to `googletagmanager.com/gtag/js?id=AW-18017405402` returning HTTP 200
5. If you don't see it, check that `localStorage.getItem('cookie_consent')` is `"accepted"` (the consent banner blocks tracking until accepted)

### "Event fires but `button_location` is missing"

Open DevTools → Console → paste:
```javascript
document.querySelectorAll('[data-event="whatsapp_click"]').forEach(a =>
  console.log(a.getAttribute('data-location'), a.href)
);
```

Every result should print a non-empty location. If any are blank, that page's `data-location` attribute wasn't set during deploy — re-run the tagging script.

### "Event fires from one page but not another"

Open DevTools → Console on the broken page → paste:
```javascript
typeof gtag === 'function'
```

Should return `true`. If `false`, gtag isn't loading on that page — check the `<head>` for the `PERF:GTAG-LAZY` block.

Then check for the tracker:
```javascript
document.querySelector('[data-event="whatsapp_click"]') !== null
```

Should return `true` if any WA links exist on that page.

---

## What "good" looks like

After 7–14 days of data:

- **Top button locations** should be `home`, `pricing`, `home_fr` (highest-traffic pages)
- **Click rate** = `whatsapp_click` / Total users on that page → typically 2–8% for a hospitality service like this
- **Cross-page funnel:** users who click WA on `/` are first-touch; users who click WA on `/private-chef-cost-marrakech/` are mid-funnel (price-shopping). Different events but same intent — combine them as "all WA clicks" for the conversion total.

If `home` is dominant (>80% of clicks), the homepage is doing all the conversion work — the new internal-links section + content cluster need more time to compound. If pricing/villa-guide page clicks rise over time → SEO content is converting.
