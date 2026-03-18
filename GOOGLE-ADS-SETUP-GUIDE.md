# Google Ads Complete Setup Guide — La Table Marrakech

**Account ID:** 665-792-1235
**CID:** 8088972847
**Website:** https://www.latablemarrakech.com
**Date:** 2026-03-14

---

## TABLE OF CONTENTS

1. [Account-Level Settings](#1-account-level-settings)
2. [Conversion Actions](#2-conversion-actions)
3. [Audience Lists](#3-audience-lists)
4. [Negative Keyword Lists](#4-negative-keyword-lists)
5. [Campaign 1: Search — Brand](#5-campaign-1-search--brand)
6. [Campaign 2: Search — High Intent EN](#6-campaign-2-search--high-intent-en)
7. [Campaign 3: Search — High Intent FR](#7-campaign-3-search--high-intent-fr)
8. [Campaign 4: Search — Mid Intent](#8-campaign-4-search--mid-intent)
9. [Ad Extensions (Account-Level)](#9-ad-extensions-account-level)
10. [Budget & Bidding Strategy](#10-budget--bidding-strategy)
11. [Launch Checklist](#11-launch-checklist)
12. [Week 1-4 Optimization Calendar](#12-week-1-4-optimization-calendar)

---

## 1. ACCOUNT-LEVEL SETTINGS

Do these FIRST before creating any campaigns.

### Account Settings (Gear icon > Account Settings)
| Setting | Value |
|---------|-------|
| Time zone | (GMT+01:00) Morocco/Casablanca |
| Currency | EUR (€) |
| Auto-tagging | ON (enables gclid for GA4) |
| Tracking template | Leave blank (using gtag directly) |

### Enhanced Conversions (Goals > Settings)
1. Go to **Goals > Conversions > Settings**
2. Turn on **Enhanced Conversions**
3. Select **Global site tag (gtag.js)** as the method
4. Click **Save**

### Link GA4 (Tools > Data Manager > Linked accounts)
1. Click **Link** next to Google Analytics (GA4)
2. Select the property with ID **G-J2QTMMMYLD**
3. Enable **Import site metrics** and **Audiences**
4. Click **Link**

---

## 2. CONVERSION ACTIONS

### Go to: Goals > Conversions > Summary > New conversion action

#### Conversion 1: Booking Form Submit (Primary)
| Field | Value |
|-------|-------|
| Category | Submit lead form |
| Conversion name | Booking Request |
| Value | Use the same value for each conversion: **€85** |
| Count | Every conversion |
| Click-through window | 30 days |
| View-through window | 1 day |
| Attribution model | Data-driven (default) |
| Primary/Secondary | **Primary** (used for bidding) |

> **Note:** This is already firing from the website code with `AW-18016239415/GcryCOOr1IgcELf-545D`. Just ensure this conversion action exists in Google Ads and matches this send_to label.

#### Conversion 2: WhatsApp Click (Primary)
| Field | Value |
|-------|-------|
| Category | Contact |
| Conversion name | WhatsApp Click |
| Value | Use the same value for each conversion: **€85** |
| Count | One (per click, not every click) |
| Click-through window | 30 days |
| Attribution model | Data-driven |
| Primary/Secondary | **Primary** |

> Already firing with the same conversion label `AW-18016239415/GcryCOOr1IgcELf-545D`.

#### Conversion 3: Phone Call Click (Secondary)
| Field | Value |
|-------|-------|
| Category | Contact |
| Conversion name | Phone Call Click |
| Value | €85 |
| Count | One |
| Primary/Secondary | **Secondary** (observation only, not for bidding) |

> This fires via dataLayer event `phone_call`. To track in Google Ads, import from GA4 after linking.

---

## 3. AUDIENCE LISTS

### Go to: Tools > Audience Manager

#### Audience 1: All Website Visitors
| Field | Value |
|-------|-------|
| Segment name | All Visitors - 90 days |
| Segment members | Visitors of a page |
| Visited page URL | Contains: `latablemarrakech.com` |
| Membership duration | 90 days |

#### Audience 2: Booking Page Visitors (didn't convert)
| Field | Value |
|-------|-------|
| Segment name | Booking Section Visitors - 30 days |
| Visited page URL | Contains: `latablemarrakech.com` |
| Also visited | Page URL contains: `#booking` |
| Membership duration | 30 days |

#### Audience 3: Converters (Exclude list)
| Field | Value |
|-------|-------|
| Segment name | Converters - 30 days |
| Segment members | Users who performed a conversion |
| Conversion action | Booking Request + WhatsApp Click |
| Membership duration | 30 days |

---

## 4. NEGATIVE KEYWORD LISTS

### Go to: Tools > Shared Library > Negative keyword lists

Import the file: `google-ads-negative-keywords.csv` (already in your project folder)

Or create these 6 lists manually:

### List 1: Jobs & Careers (20 keywords)
```
"chef jobs"
"chef job"
"hiring chef"
"chef salary"
"chef career"
"chef employment"
"chef vacancy"
"chef resume"
"chef cv"
"work as chef"
"become a chef"
"chef training"
"culinary school"
"chef course"
"chef apprenticeship"
"emploi chef"
"offre emploi"
"recrutement chef"
"salaire chef"
"formation chef"
```

### List 2: Recipes & DIY (15 keywords)
```
"recipe"
"recipes"
"how to cook"
"how to make"
"ingredients"
"tutorial"
"cooking video"
"step by step"
"homemade"
"easy recipe"
"recette"
"recettes"
"comment faire"
"comment cuisiner"
"fait maison"
```

### List 3: Other Cities (14 keywords)
```
"casablanca chef"
"rabat chef"
"fes chef"
"tangier chef"
"agadir chef"
"essaouira chef"
"paris chef"
"london chef"
"dubai chef"
"chef casablanca"
"chef rabat"
"chef fes"
"chef tanger"
"chef agadir"
```

### List 4: Free & Cheap (12 keywords)
```
[free]
"cheap"
"budget"
"discount"
"coupon"
"promo code"
"deal"
"gratuit"
"pas cher"
"bon marché"
"réduction"
"promotion"
```

### List 5: Restaurants & Dining Out (11 keywords)
```
"restaurant marrakech"
"best restaurant"
"restaurant review"
"food delivery"
"takeaway"
"uber eats"
"glovo"
"reservation restaurant"
"menu restaurant"
"livraison repas"
"meilleur restaurant"
```

### List 6: Irrelevant Services (12 keywords)
```
"cleaning service"
"maid service"
"hotel chef"
"chef knife"
"chef hat"
"chef uniform"
"chef coat"
"kitchen equipment"
"cooking class"
"cours de cuisine"
"atelier cuisine"
"cooking workshop"
```

**After creating all 6 lists → Apply ALL lists to ALL campaigns.**

---

## 5. CAMPAIGN 1: SEARCH — BRAND

### Campaign Settings
| Setting | Value |
|---------|-------|
| Campaign name | `LTM_Search_Brand` |
| Campaign type | Search |
| Networks | Search Network ONLY (uncheck Display Network, uncheck Search Partners) |
| Locations | All countries |
| Location options | **Presence: People in your targeted locations** |
| Languages | English, French, Arabic |
| Budget | €3/day (€90/month) |
| Bidding | Maximize Clicks (cap at €1.50 CPC) |
| Ad schedule | All day |
| Start date | Today |

### Ad Group: Brand Terms
**Ad Group name:** `Brand — La Table Marrakech`

#### Keywords (Exact + Phrase match):
```
[la table marrakech]
"la table marrakech"
[latablemarrakech]
"latablemarrakech"
[table marrakech chef]
"table marrakech chef"
[la table marrakech chef]
```

#### RSA (Responsive Search Ad):

**Headlines (15 headlines):**
```
La Table Marrakech
Private Chef Marrakech
From €85/Day — Book Now
Chef Privé à Marrakech
4.9/5 ★ — 200+ Reviews
Moroccan Feast at Your Villa
WhatsApp Booking — 24h Reply
Fresh Souk Ingredients Daily
Up to 30 Guests Served
Full Service & Cleanup
Book Your Private Chef
Dès 85€/Jour — Réservez
Villa Chef — Marrakech
Tagine, Pastilla, Couscous
La Table Marrakech — Chef
```

**Descriptions (4 descriptions):**
```
Private chef for your Marrakech villa. Fresh souk ingredients, full service. From €85/day.
Réservez un chef privé à Marrakech dès 85€/jour. Service complet et nettoyage inclus.
4.9/5 from 200+ guests. Tagine, pastilla, couscous at your villa. Book via WhatsApp.
Souk shopping, cooking, table service & cleanup included. Serve 2 to 30 guests easily.
```

**Pinning:**
- Pin "La Table Marrakech" to Headline Position 1

---

## 6. CAMPAIGN 2: SEARCH — HIGH INTENT EN

### Campaign Settings
| Setting | Value |
|---------|-------|
| Campaign name | `LTM_Search_HighIntent_EN` |
| Campaign type | Search |
| Networks | Search Network ONLY |
| Locations | Morocco, France, United Kingdom, Germany, Belgium, Netherlands, Spain, Italy, United States, Canada, Australia |
| Location options | **Presence or interest: People in or regularly in your targeted locations** |
| Languages | English |
| Budget | €10/day (€300/month) |
| Bidding | Maximize Conversions (no target CPA yet — wait for 15+ conversions) |
| Ad schedule | All hours (tourists search all day) |
| Start date | Today |

### Ad Group 1: Private Chef Marrakech
**Ad Group name:** `EN — Private Chef Marrakech`

#### Keywords:
```
[private chef marrakech]
"private chef marrakech"
[private chef in marrakech]
"private chef in marrakech"
[hire private chef marrakech]
"hire private chef marrakech"
[personal chef marrakech]
"personal chef marrakech"
[private cook marrakech]
"private cook marrakech"
```

#### RSA:

**Headlines:**
```
Private Chef in Marrakech
From €85/Day — Book Now
4.9/5 ★ from 200+ Guests
Fresh Souk Ingredients Daily
Your Chef Cooks at Your Villa
Multi-Course Moroccan Feast
WhatsApp Booking — 24h Reply
Tagine, Pastilla & Couscous
Full Service & Cleanup
Book a Private Chef Today
Up to 30 Guests — No Problem
Hire a Chef in Marrakech
Authentic Moroccan Cooking
From Market to Your Table
Villa Dining — Marrakech
```

**Descriptions:**
```
Private chef in Marrakech from €85/day. Souk-fresh ingredients, full service & cleanup.
Your chef shops the medina, cooks at your villa. 2-30 guests. Book via WhatsApp now.
4.9/5 from 200+ guests. Souk-fresh ingredients, table service, and full cleanup included.
Professional chef prepares authentic Moroccan cuisine at your villa. From €40/person.
```

### Ad Group 2: Villa Chef Morocco
**Ad Group name:** `EN — Villa Chef Morocco`

#### Keywords:
```
[villa chef marrakech]
"villa chef marrakech"
[villa chef morocco]
"villa chef morocco"
[chef for villa marrakech]
"chef for villa marrakech"
[riad chef marrakech]
"riad chef marrakech"
[in villa dining marrakech]
"in villa dining marrakech"
```

#### RSA:

**Headlines:**
```
Villa Chef — Marrakech
Chef Comes to Your Villa
From €85/Day for 10 Guests
4.9/5 ★ — 200+ Villa Guests
Souk-Fresh Moroccan Feast
Full Kitchen Service & Cleanup
Book via WhatsApp — Fast
Multi-Course Villa Dining
Tagine at Your Marrakech Villa
Professional Villa Chef
Serve 2-30 Guests Easily
Your Private Villa Chef
Authentic Riad Dining
From Souk to Your Table
Luxury Villa Chef Service
```

**Descriptions:**
```
Chef for your Marrakech villa. Souk shopping, cooking, service & cleanup. From €85/day.
Villa dining made easy — chef handles everything from souk to cleanup. 2-30 guests.
4.9/5 from 200+ guests. Fresh ingredients, authentic recipes, full service included.
Your chef prepares a Moroccan feast while you relax. Book via WhatsApp — confirmed 24h.
```

### Ad Group 3: Hire Chef Marrakech
**Ad Group name:** `EN — Hire Chef Marrakech`

#### Keywords:
```
[hire a chef marrakech]
"hire a chef marrakech"
[book a chef marrakech]
"book a chef marrakech"
[chef for hire marrakech]
"chef for hire marrakech"
[chef service marrakech]
"chef service marrakech"
[catering marrakech]
"catering marrakech"
[private catering marrakech]
```

#### RSA:

**Headlines:**
```
Hire a Chef in Marrakech
Book a Chef — From €85/Day
4.9/5 ★ — 200+ Happy Guests
Full Catering at Your Villa
Fresh Souk Ingredients
Multi-Course Moroccan Feast
WhatsApp Booking — Easy
Tagine, Pastilla, Couscous
Chef Service & Cleanup
Serve 2 to 30 Guests
Professional Chef Service
Book Now — Confirmed in 24h
Private Chef Experience
Authentic Moroccan Cuisine
Villa Catering — Marrakech
```

**Descriptions:**
```
Hire a chef in Marrakech. Souk ingredients, multi-course feast & cleanup. From €85/day.
We shop the souk, cook at your villa, serve & clean up. 4.9/5 from 200+ reviews.
Private chef & catering in Marrakech. Authentic cuisine at your villa. 2-30 guests.
Full-service private dining. Chef handles shopping to cleanup. From €40/person.
```

---

## 7. CAMPAIGN 3: SEARCH — HIGH INTENT FR

### Campaign Settings
| Setting | Value |
|---------|-------|
| Campaign name | `LTM_Search_HighIntent_FR` |
| Campaign type | Search |
| Networks | Search Network ONLY |
| Locations | France, Belgium, Switzerland, Morocco, Canada, Luxembourg |
| Location options | **Presence or interest** |
| Languages | French |
| Budget | €8/day (€240/month) |
| Bidding | Maximize Conversions |
| Ad schedule | All hours |

### Ad Group 1: Chef Privé Marrakech
**Ad Group name:** `FR — Chef Privé Marrakech`

#### Keywords:
```
[chef privé marrakech]
"chef privé marrakech"
[chef privé à marrakech]
"chef privé à marrakech"
[chef à domicile marrakech]
"chef à domicile marrakech"
[chef personnel marrakech]
"chef personnel marrakech"
[cuisinier privé marrakech]
"cuisinier privé marrakech"
```

#### RSA:

**Headlines:**
```
Chef Privé à Marrakech
Dès 85€/Jour — Réservez
4.9/5 ★ — 200+ Avis Clients
Ingrédients Frais du Souk
Festin Marocain à la Villa
Service Complet & Nettoyage
Réservation WhatsApp — 24h
Tagine, Pastilla, Couscous
Chef à Domicile — Marrakech
Jusqu'à 30 Convives
Votre Chef Personnel
Du Souk à Votre Table
Cuisine Marocaine Authentique
Dès 40€/Personne
La Table Marrakech
```

**Descriptions:**
```
Chef privé pour votre villa dès 85€/jour. Ingrédients du souk, service et nettoyage.
Votre chef fait le souk et cuisine dans votre villa. 2 à 30 convives. Réservez WhatsApp.
4.9/5 de 200+ clients. Ingrédients frais, service à table et nettoyage. Confirmé 24h.
Cuisine marocaine authentique dans votre villa. Chef professionnel. Dès 40€/personne.
```

### Ad Group 2: Villa Chef Maroc
**Ad Group name:** `FR — Villa Chef Maroc`

#### Keywords:
```
[chef villa marrakech]
"chef villa marrakech"
[chef villa maroc]
"chef villa maroc"
[chef pour villa marrakech]
"chef pour villa marrakech"
[repas privé marrakech]
"repas privé marrakech"
[dîner privé marrakech]
"dîner privé marrakech"
[traiteur villa marrakech]
"traiteur villa marrakech"
```

#### RSA:

**Headlines:**
```
Chef pour Votre Villa
Marrakech — Dès 85€/Jour
4.9/5 ★ — Avis Vérifiés
Souk Frais Chaque Matin
Festin dans Votre Villa
Service & Nettoyage Inclus
Réservez via WhatsApp
Tagine, Pastilla, Couscous
Dîner Privé — Marrakech
2 à 30 Convives
Traiteur Villa Marrakech
Expérience Gastronomique
Cuisine 100% Marocaine
Confirmé en 24h
Villa & Riad — Marrakech
```

**Descriptions:**
```
Chef pour villa ou riad à Marrakech. Souk, cuisine, service et nettoyage. Dès 85€/jour.
Dîner privé dans votre villa. Votre chef gère tout, du souk au nettoyage. 2-30 convives.
4.9/5 de 200+ clients. Ingrédients frais, recettes authentiques, service complet inclus.
Votre chef prépare un festin marocain chez vous. Réservez via WhatsApp — confirmé 24h.
```

---

## 8. CAMPAIGN 4: SEARCH — MID INTENT

### Campaign Settings
| Setting | Value |
|---------|-------|
| Campaign name | `LTM_Search_MidIntent` |
| Campaign type | Search |
| Networks | Search Network ONLY |
| Locations | All target countries (same as Campaign 2) |
| Languages | English, French |
| Budget | €5/day (€150/month) |
| Bidding | Maximize Conversions |

### Ad Group 1: Dining Experience Marrakech
**Ad Group name:** `MID — Dining Experience`

#### Keywords:
```
"private dining marrakech"
"dining experience marrakech"
"food experience marrakech"
"moroccan food experience"
"marrakech food experience"
"luxury dining marrakech"
"authentic moroccan dinner"
"moroccan feast marrakech"
"expérience culinaire marrakech"
"gastronomie marrakech"
```

#### RSA:

**Headlines:**
```
Dining Experience Marrakech
Private Moroccan Feast
From €85/Day — Your Villa
4.9/5 ★ — 200+ Reviews
Chef Cooks at Your Place
Fresh Souk Ingredients
Full Service & Cleanup
Book via WhatsApp Today
Tagine, Pastilla, Couscous
Authentic Moroccan Dining
For 2 to 30 Guests
Luxury Food Experience
Confirmed in 24 Hours
From Market to Your Table
Personal Chef Service
```

**Descriptions:**
```
Private chef shops the souk, cooks a Moroccan feast at your villa & cleans up. €85/day.
Skip restaurants — authentic feast at your villa. Souk-fresh ingredients. 4.9/5 rating.
Your chef prepares tagine, pastilla, couscous at your villa. 2-30 guests. Book now.
Private dining made easy. Chef handles shopping to cleanup. From €40/person.
```

### Ad Group 2: Special Occasions
**Ad Group name:** `MID — Special Occasions`

#### Keywords:
```
"birthday dinner marrakech"
"celebration dinner marrakech"
"anniversary dinner marrakech"
"group dinner marrakech"
"party catering marrakech"
"hen party marrakech food"
"marrakech wedding dinner"
"private party chef marrakech"
```

#### RSA:

**Headlines:**
```
Celebrate in Marrakech
Private Chef for Your Party
From €85/Day — Up to 30
Multi-Course Moroccan Feast
4.9/5 ★ — 200+ Events
Your Villa, Your Chef
Birthday Dinner Marrakech
WhatsApp Booking — 24h
Group Dining Made Easy
Full Service & Cleanup
Special Occasion Chef
Fresh Souk Ingredients
Book Your Chef Today
Authentic Moroccan Cuisine
Unforgettable Villa Dinner
```

**Descriptions:**
```
Hire a private chef for your villa celebration. Moroccan feast, up to 30 guests. €85/day.
Make your Marrakech celebration unforgettable. Chef shops souk & cooks. Book WhatsApp.
Birthday or group dinner? Your chef handles everything. 4.9/5 from 200+ guests.
Celebrate at your villa. Professional chef, souk-fresh ingredients, full service included.
```

---

## 9. AD EXTENSIONS (Account-Level)

### Go to: Ads & Extensions > Extensions

### Sitelinks (4 required, create 6)
| Sitelink text | Description 1 | Description 2 | Final URL |
|---------------|---------------|---------------|-----------|
| Book via WhatsApp | Fast booking, confirmed in 24h | Reply within minutes | https://wa.me/212721354757 |
| See Our Menu | Tagine, pastilla, couscous & more | Fresh souk ingredients daily | https://latablemarrakech.com/#menu |
| Pricing — From €85/Day | Up to 10 guests included | Full service & cleanup | https://latablemarrakech.com/#pricing |
| Guest Reviews — 4.9/5 | Read 200+ verified reviews | See what guests say | https://latablemarrakech.com/#reviews |
| How It Works | Book → Chef shops → Cooks → Cleanup | Simple 4-step process | https://latablemarrakech.com/#how-it-works |
| Contact Us | Phone, WhatsApp or email | We reply within hours | https://latablemarrakech.com/#booking |

### Callout Extensions (create 8)
```
From €85/Day
4.9/5 ★ Rating
200+ Happy Guests
Fresh Souk Ingredients
Full Cleanup Included
2-30 Guests Welcome
Confirmed in 24h
Authentic Moroccan Cuisine
```

### Structured Snippets (create 2)
| Header | Values |
|--------|--------|
| Types | Tagine, Pastilla, Couscous, Salads, Desserts, Mint Tea |
| Amenities | Souk Shopping, Cooking, Table Service, Full Cleanup, Custom Menu |

### Call Extension
| Field | Value |
|-------|-------|
| Phone number | +212 721 354 757 |
| Country | Morocco |
| Call reporting | ON |
| Count calls as conversions | Yes |

### Image Extensions
Upload these images from your website folder:
- `private-chef-marrakech-tagine.webp`
- `chef-cooking-marrakech-kitchen.webp`
- `moroccan-feast-villa-terrace.webp`
- `chicken-tagine-marrakech.webp`

---

## 10. BUDGET & BIDDING STRATEGY

### Monthly Budget Allocation
| Campaign | Daily | Monthly | % of Total |
|----------|-------|---------|------------|
| LTM_Search_Brand | €3 | €90 | 12% |
| LTM_Search_HighIntent_EN | €10 | €300 | 38% |
| LTM_Search_HighIntent_FR | €8 | €240 | 31% |
| LTM_Search_MidIntent | €5 | €150 | 19% |
| **TOTAL** | **€26** | **€780** | **100%** |

### Bidding Strategy Progression
| Phase | When | Strategy |
|-------|------|----------|
| Launch (Week 1-4) | 0 conversions | **Maximize Conversions** (all campaigns except Brand) |
| Brand | Always | **Maximize Clicks** (cap €1.50) |
| Optimization (Month 2+) | After 15+ conversions/month | Switch to **Target CPA** (start at €25-€30) |
| Scale (Month 3+) | After 30+ conversions/month | Lower Target CPA gradually, increase budgets on winners |

---

## 11. LAUNCH CHECKLIST

### Before launching (do in this order):

- [ ] **1. Account settings** — Time zone, currency, auto-tagging
- [ ] **2. Link GA4** — Property G-J2QTMMMYLD
- [ ] **3. Enable Enhanced Conversions** — In Goals > Settings
- [ ] **4. Verify conversion action** — Ensure `AW-18016239415/GcryCOOr1IgcELf-545D` is active in Goals > Conversions
- [ ] **5. Create negative keyword lists** — All 6 lists (or import CSV)
- [ ] **6. Create audience lists** — All 3 audiences
- [ ] **7. Create Campaign 1 (Brand)** — With ad group + keywords + RSA
- [ ] **8. Create Campaign 2 (High Intent EN)** — 3 ad groups + keywords + RSAs
- [ ] **9. Create Campaign 3 (High Intent FR)** — 2 ad groups + keywords + RSAs
- [ ] **10. Create Campaign 4 (Mid Intent)** — 2 ad groups + keywords + RSAs
- [ ] **11. Add extensions** — Sitelinks, callouts, snippets, call, images (account-level)
- [ ] **12. Apply negative lists** — To ALL campaigns
- [ ] **13. Double-check location targeting** — Must be "People in" (not "People in or interested in") for Brand; use "Presence or interest" for non-brand
- [ ] **14. Double-check networks** — Display Network OFF on all Search campaigns
- [ ] **15. Submit test booking** — Verify conversion fires in Goals > Conversions (may take 1-3 hours to show)
- [ ] **16. Enable campaigns** — Go live!

---

## 12. WEEK 1-4 OPTIMIZATION CALENDAR

### Week 1 (Days 1-7): Monitor
- [ ] Check conversion tracking is recording (Goals > Conversions)
- [ ] Review Search Terms report daily — add negatives for irrelevant terms
- [ ] Ensure no campaigns are "Limited by Budget" (unless intentional)
- [ ] Check Ad Strength — aim for "Good" or "Excellent" on all RSAs
- [ ] Verify ads are showing (use Google Ads Preview & Diagnosis tool)

### Week 2 (Days 8-14): First Optimizations
- [ ] Review Search Terms — add 10-20 more negatives
- [ ] Pause any keywords with 50+ clicks and 0 conversions
- [ ] Check device performance — adjust bids if mobile converts better/worse
- [ ] Review ad group impression share — increase bids/budgets where share is low
- [ ] Test 2-3 new headline variations

### Week 3 (Days 15-21): Refine
- [ ] Analyze which ad groups have best CTR and CVR
- [ ] Shift budget toward top performers
- [ ] Add new keywords from Search Terms report (terms you're converting on)
- [ ] Review location performance — exclude any countries with clicks but no conversions
- [ ] Check Quality Score — flag any keywords below 5

### Week 4 (Days 22-30): Evaluate & Scale
- [ ] Calculate actual CPA (total spend / total conversions)
- [ ] If CPA < €30 and 15+ conversions: switch to Target CPA bidding
- [ ] If CPA > €40: review keywords, tighten match types, add negatives
- [ ] Consider launching PMax campaign if conversion data is strong
- [ ] Review Auction Insights — see who you're competing against
- [ ] Plan Month 2 budget based on results

---

## IMPORTANT NOTES

### Location Targeting — Critical Setting
When creating each campaign, in the "Locations" section:
1. Click **"Location options"**
2. For **Target**: Select **"Presence: People in your targeted locations"** (for Brand campaign) or **"Presence or interest"** (for non-brand, since tourists search before traveling)
3. For **Exclude**: Always select **"Presence: People in your excluded locations"**

### Ad Strength Tips
If your RSA shows "Average" or "Poor" Ad Strength:
- Add more unique headlines (different angles, not just rewording)
- Include keywords in at least 3 headlines
- Include a CTA in at least 2 headlines ("Book Now", "Réservez")
- Make descriptions meaningfully different from each other
- Don't over-pin — only pin brand name to Position 1

### Search Partners
Keep Search Partners OFF initially. After 30 days, you can test enabling them and compare conversion rates. If Search Partner CVR is >50% lower than Search, keep them off.

---

*Setup guide generated 2026-03-14 for La Table Marrakech — Google Ads Account 665-792-1235*
