# Google Ads Audit Report — La Table Marrakech

**Website:** https://www.latablemarrakech.com
**Account:** 665-792-1235
**Date:** 2026-03-15
**Status:** Post-fix (tracking implemented)

---

## Google Ads Health Score: 72/100 (Grade: C — Needs Improvement)

```
Conversion Tracking: 75/100   ████████░░  (25%)
Wasted Spend:        N/A      ░░░░░░░░░░  (20%) — Requires campaign data
Account Structure:   N/A      ░░░░░░░░░░  (15%) — New account
Keywords:            N/A      ░░░░░░░░░░  (15%) — New account
Ads & Assets:        65/100   ██████░░░░  (15%)
Settings:            70/100   ███████░░░  (10%)
```

---

## Conversion Tracking (25% weight)

| ID | Check | Result | Finding |
|----|-------|--------|---------|
| G42 | Conversion actions defined | **PASS** | Booking form + WhatsApp click conversions active with `AW-18016239415/GcryCOOr1IgcELf-545D` |
| G43 | Enhanced conversions enabled | **PASS** | `allow_enhanced_conversions: true` in gtag config. Email + name hashed from booking form. |
| G44 | Server-side tracking | **WARNING** | No GTM Server-Side container. Recommend for future. |
| G45 | Consent Mode v2 | **PASS** | Implemented with `ad_storage`, `ad_user_data`, `ad_personalization`, `analytics_storage`. Defaults denied, updates on cookie accept/decline. |
| G46 | Conversion window | **PASS** | 30-day click window appropriate for travel/hospitality lead gen. |
| G47 | Micro vs macro separation | **PASS** | Booking + WhatsApp = Primary. Phone call = Secondary. CTA clicks = dataLayer only. |
| G48 | Attribution model | **PASS** | Data-driven attribution (default). |
| G49 | Conversion value | **PASS** | Static value €85 EUR assigned — matches service pricing. |
| G-CT1 | No duplicate counting | **WARNING** | Both booking form and WhatsApp use same conversion label. Create separate conversion actions. |
| G-CT2 | GA4 linked | **WARNING** | GA4 (`G-J2QTMMMYLD`) active. Needs linking in Google Ads (Tools > Data Manager). |
| G-CT3 | Google Tag firing | **PASS** | `gtag.js` loads with `AW-18016239415` on all 3 pages (EN, FR, AR). |

---

## Ads & Assets (15% weight) — Landing Page

| ID | Check | Result | Finding |
|----|-------|--------|---------|
| G35 | Ad copy relevance | **PASS** | Title "Private Chef Marrakech" matches target keywords exactly. |
| G59 | Mobile speed | **WARNING** | Hero video + SVG textures may slow mobile LCP. Estimated 2.5-4.0s. |
| G60 | Landing page relevance | **PASS** | Clear CTA, pricing (€85/day), social proof (4.9/5, 200+ reviews), booking form. |
| G61 | Schema markup | **PASS** | FoodService, FAQPage, HowTo, BreadcrumbList, AggregateRating — excellent. |

---

## Settings & Targeting (10% weight)

| ID | Check | Result | Finding |
|----|-------|--------|---------|
| G54 | Call extensions | **WARNING** | Phone number on site with dataLayer tracking but no Google forwarding number. |
| G60 | Landing page relevance | **PASS** | Strong match — H1, pricing, CTA, trust signals all present. |
| G61 | Schema markup | **PASS** | 5 schema types implemented — best in class. |

---

## What Was Fixed (2026-03-15)

| Issue | Before | After |
|-------|--------|-------|
| Conversion tracking | Commented out with placeholder `AW-XXXXXXX` | Active with real `AW-18016239415/GcryCOOr1IgcELf-545D` |
| Consent Mode v2 | Missing entirely | Full implementation with default denied + cookie banner integration |
| Enhanced Conversions | Not configured | Enabled with hashed email + name from booking form |
| Cookie consent | Basic localStorage only | Integrated with `gtag('consent', 'update', ...)` |
| Negative keywords | None | 84 keywords across 6 themed lists |

---

## Remaining Action Items

| Priority | Action | Where |
|----------|--------|-------|
| 1 | Link GA4 to Google Ads | Google Ads > Tools > Data Manager |
| 2 | Enable Enhanced Conversions in Google Ads UI | Goals > Settings |
| 3 | Create separate conversion actions (Booking vs WhatsApp) | Goals > Conversions |
| 4 | Import negative keyword lists | Tools > Shared Library |
| 5 | Complete advertiser verification (Individual + passport) | Settings > Verification |
| 6 | Launch campaigns per setup guide | See GOOGLE-ADS-SETUP-GUIDE.md |
| 7 | Optimize mobile page speed (LCP < 2.5s) | Website code |
| 8 | Set up Google call forwarding number | Ad Extensions > Call |

---

*Report generated 2026-03-15 — La Table Marrakech*
