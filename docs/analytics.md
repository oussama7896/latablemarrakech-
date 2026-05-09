# Analytics — La Table Marrakech

Single source of truth for tracking on `latablemarrakech.com`.

- **GA4 Measurement ID:** `G-J2QTMMMYLD`
- **Google Ads Conversion ID:** `AW-18017405402`
- **Implementation:** plain `gtag.js`, no GTM container, no analytics libraries
- **Consent:** Consent Mode v2, denied-by-default, restored from `localStorage.cookie_consent`

---

## How it loads

Every page has two inline `<script>` blocks in `<head>`, in this order:

1. **CONSENT MODE V2** — sets default consent (denied) and restores granted state if the visitor previously accepted the cookie banner. Defines the global `gtag()` function.
2. **PERF:GTAG-LAZY** — lazy-loads `gtag.js` on first user interaction (`scroll`, `mousemove`, `touchstart`, `keydown`, `click`) or after a 5-second timeout, whichever comes first. This keeps the third-party script off the critical path so it doesn't blow up our Total Blocking Time.

Every page also has a third inline block at the **end of `<body>`**:

3. **PERF:ANALYTICS-RICH** — a single IIFE that listens for clicks, form submits, scroll, and FAQ toggles and forwards them as GA4 events.

All three blocks are **canonical** — identical byte-for-byte across every page. Don't hand-edit them. If the canonical version changes, update `inject-analytics.py` (head loader) and `inject-analytics-rich.py` (end-of-body block) and re-run them.

---

## Events fired

| Event | Where it fires | Key params |
|---|---|---|
| `whatsapp_click` | Click on `[data-event="whatsapp_click"]`, `a[href*="wa.me"]`, or `a[href*="api.whatsapp.com"]` | `cta_label`, `cta_position`, `device`, `link_url`, `button_location`, `page_path`, `page_title` |
| `email_click` | Click on `a[href^="mailto:"]` | `cta_label`, `cta_position`, `link_url`, `page_path`, `page_title` |
| `phone_click` | Click on `a[href^="tel:"]` | `cta_label`, `cta_position`, `link_url`, `page_path`, `page_title` |
| `booking_enquiry_submit` | Submit on `<form data-track-form="booking-enquiry">` | `form_id`, `form_name`, `group_size`, `has_date`, `has_email`, `has_notes`, `page_path`, `page_title` |
| `scroll_depth` | 25%, 50%, 75%, 90% scroll on high-intent pages (`/`, `/private-chef-cost-marrakech/`, `/marrakech-villa-with-private-chef/`, `/marrakech-cooking-class-vs-private-chef/`, `/the-experience/`) | `depth_percentage`, `page_path`, `page_title` |
| `faq_open` | `<details>` toggle or click on `.faq-question` / `[class*="faq-q"]` / `[data-faq-trigger]` | `question_text`, `page_path`, `page_title` |
| `conversion` (Google Ads) | Homepage booking form submit + every WhatsApp click (see `index.html` per-page block at line ~2880) | `send_to`, `value`, `currency` |

All events are dual-pushed: into `window.dataLayer` AND `gtag('event', ...)`. The `gtag` call is guarded with `typeof gtag === 'function'` so missing gtag never throws.

---

## How to add tracking to a new CTA

### A WhatsApp button

Add the two data attributes — the global listener picks them up automatically:

```html
<a data-event="whatsapp_click"
   data-location="<page-slug>"
   href="https://wa.me/212721354757?text=…"
   target="_blank"
   rel="noopener noreferrer">
  Chat on WhatsApp
</a>
```

The `data-location` value is the page slug (see the table in `GA4-WHATSAPP-SETUP.md`). If you forget it, the listener falls back to the CSS-class-based `cta_position` so the click still gets attributed to a position bucket like `hero` or `footer`.

### A new booking / enquiry form

Add three attributes to the `<form>` tag:

```html
<form id="booking-<page>"
      data-track-form="booking-enquiry"
      data-form-id="booking-<page>"
      onsubmit="event.preventDefault(); /* …open WhatsApp… */">
  <input name="bname" required>
  <input type="email" name="bemail">
  <input name="bdate">
  <select name="bguests">…</select>
  <textarea name="bnotes"></textarea>
</form>
```

The global listener auto-detects:
- `[name="bguests"]` → `group_size`
- `[name="bdate"]` → `has_date` (boolean)
- `[name="bemail"]` → `has_email` (boolean)
- `[name="bnotes"]` → `has_notes` (boolean)

So as long as you keep those `name` attributes consistent, the new form gets tracked with no JS changes.

### A `mailto:` or `tel:` link

Just write a normal anchor — the global listener handles it:

```html
<a href="mailto:hello@latablemarrakech.com">Email us</a>
<a href="tel:+212721354757">Call us</a>
```

---

## How to add tracking to a new page (full HTML page)

The two codemod scripts at the repo root handle this for you:

```bash
python3 inject-analytics.py        # ensures head consent + gtag loader
python3 inject-analytics-rich.py   # ensures end-of-body event listeners
```

Both are **idempotent** — running them on a page that already has the canonical blocks is a no-op. Run them after creating any new `index.html`. They skip backups, the `_deleted-*` directories, screenshot helpers, and the social-logo render template.

For the codemod to work, the new page must contain:
- `<head>` with a `<meta name="viewport">` tag (insertion anchor for the head blocks)
- The `<!-- PERF:ANALYTICS-RICH START -->...<!-- PERF:ANALYTICS-RICH END -->` markers in `<body>` if you want events tracked. The codemod does **not** insert this block from scratch — copy it from any existing page first.

---

## Verifying tracking is live

### Real-time sanity check

1. Open https://analytics.google.com → property `G-J2QTMMMYLD` → **Reports → Realtime**
2. Open the live site in a private/incognito window (avoids cached consent state)
3. Accept the cookie banner if it appears
4. **Trigger the lazy-load** by scrolling or moving your mouse — until then `gtag.js` isn't loaded yet
5. Click a WhatsApp button. Within 30 seconds, `whatsapp_click` should appear in the Realtime "Event count by event name" card
6. Repeat for `email_click`, `phone_click`, `booking_enquiry_submit`

### DevTools sanity check

In the page's DevTools console:

```js
typeof gtag === 'function'                                  // true after 5s or first interaction
window.dataLayer.filter(e => e.event === 'whatsapp_click')  // grows by one per click
document.querySelectorAll('[data-event="whatsapp_click"]')  // every WA button on the page
document.querySelectorAll('form[data-track-form="booking-enquiry"]')  // every tracked form
```

---

## What lives where

| File | Role |
|---|---|
| `inject-analytics.py` | Codemod — head consent + lazy gtag loader |
| `inject-analytics-rich.py` | Codemod — end-of-body event listeners |
| `docs/analytics.md` | This file — single source of truth |
| `GA4-WHATSAPP-SETUP.md` | Original WhatsApp tracking setup guide. Still valid for the GA4 UI parts (Key Events, Explorations, Google Ads conversion import). |
| `GOOGLE-ADS-SETUP-GUIDE.md` | Google Ads-specific setup (Enhanced Conversions, conversion actions). |
| `index.html` ~line 2880 | **Per-homepage** Enhanced Conversions block — fires Google Ads `conversion` with hashed email + name on booking form submit. Keep this. |

---

## Known gotchas

1. **The lazy loader had a `\|` typo bug for ~17 pages until the 2026-05-09 cleanup.** The bitwise pipe made the loader silently throw "0 is not a function" and never fire any events. The codemods now overwrite all loaders with the canonical version, so this can't drift again as long as you re-run them after edits.
2. **Events fire into `dataLayer` even if `gtag.js` hasn't loaded yet.** Without consent OR before first interaction, events sit in the queue and are flushed once `gtag.js` arrives. If the visitor declines cookies, `analytics_storage` stays denied so GA4 ignores them.
3. **The cookie banner is what flips Consent Mode from `denied` to `granted`.** It writes `localStorage.cookie_consent = 'accepted'`. The consent block reads that on every page load and replays the `gtag('consent', 'update', …)` so granted state survives navigation.
4. **Dev-only `<script src="http://localhost:8400/live.js">`** sometimes appears at the end of `<body>` from the local Impeccable tool. This **must not ship to production** — strip it before deploying. It's harmless locally; in prod it'll just 404 on every page load.
