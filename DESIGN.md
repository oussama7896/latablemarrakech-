---
name: La Table Marrakech
description: Private chef in Marrakech — chef-led Moroccan dinners brought to your villa or riad.
colors:
  ink: "#080604"
  ink-light: "#100D08"
  ember: "#C1622F"
  ember-light: "#D97040"
  gold: "#B8935A"
  gold-light: "#D4AA70"
  sand: "#F0E6D0"
  sand-muted: "#B0A48A"
  muted-deep: "#5C5040"
  whatsapp-green: "#25D366"
typography:
  display:
    fontFamily: "Bebas Neue, Arial Black, Impact, sans-serif"
    fontSize: "clamp(3rem, 9vw, 7.25rem)"
    fontWeight: 400
    lineHeight: 0.92
    letterSpacing: "0.02em"
  headline:
    fontFamily: "Bebas Neue, Arial Black, Impact, sans-serif"
    fontSize: "clamp(2.25rem, 4.5vw, 3.75rem)"
    fontWeight: 400
    lineHeight: 1
    letterSpacing: "0.04em"
  serif-italic:
    fontFamily: "Libre Baskerville, Times New Roman, Georgia, serif"
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.55
    letterSpacing: "normal"
  body:
    fontFamily: "Karla, -apple-system, Helvetica Neue, sans-serif"
    fontSize: "15px"
    fontWeight: 300
    lineHeight: 1.7
    letterSpacing: "normal"
  lead:
    fontFamily: "Karla, -apple-system, Helvetica Neue, sans-serif"
    fontSize: "17px"
    fontWeight: 300
    lineHeight: 1.7
    letterSpacing: "normal"
  eyebrow:
    fontFamily: "DM Mono, ui-monospace, Courier, monospace"
    fontSize: "11px"
    fontWeight: 400
    lineHeight: 1
    letterSpacing: "0.32em"
  label:
    fontFamily: "DM Mono, ui-monospace, Courier, monospace"
    fontSize: "10px"
    fontWeight: 400
    lineHeight: 1
    letterSpacing: "0.28em"
rounded:
  square: "0px"
  xs: "2px"
  pill: "999px"
spacing:
  xs: "8px"
  sm: "16px"
  md: "24px"
  lg: "40px"
  xl: "64px"
  xxl: "96px"
  hero: "120px"
  nav: "76px"
components:
  button-primary:
    backgroundColor: "{colors.ember}"
    textColor: "{colors.sand}"
    typography: "{typography.eyebrow}"
    rounded: "{rounded.pill}"
    padding: "16px 36px"
  button-primary-hover:
    backgroundColor: "{colors.ember-light}"
    textColor: "{colors.sand}"
  button-ghost:
    backgroundColor: "transparent"
    textColor: "{colors.gold-light}"
    typography: "{typography.eyebrow}"
    rounded: "{rounded.square}"
    padding: "0"
  button-disclosure:
    backgroundColor: "transparent"
    textColor: "{colors.gold-light}"
    typography: "{typography.eyebrow}"
    rounded: "{rounded.pill}"
    padding: "12px 24px"
  whatsapp-cta:
    backgroundColor: "{colors.whatsapp-green}"
    textColor: "#FFFFFF"
    typography: "{typography.label}"
    rounded: "{rounded.pill}"
    padding: "14px 20px"
  card-editorial:
    backgroundColor: "{colors.ink-light}"
    textColor: "{colors.sand}"
    rounded: "{rounded.square}"
    padding: "28px 32px"
  pill-rating:
    backgroundColor: "rgba(8,6,4,0.4)"
    textColor: "{colors.gold-light}"
    typography: "{typography.label}"
    rounded: "{rounded.pill}"
    padding: "4px 12px"
---

# Design System: La Table Marrakech

## 1. Overview

**Creative North Star: "Cinema for Dinner"**

The site is a film about a meal. Every section is a frame, every block is a moment, and the whole sequence is paced and shot like a small piece of cinema. Where a typical restaurant site is a list of facts (menu, location, price, reviews), La Table Marrakech is a sequence of *experiences*: the riad at dusk, the brass tray landing on a low table, the steam off a tagine. That cinematic frame is the unifying instruction; every visual decision is judged by whether it makes the next frame more vivid.

The aesthetic is editorial-Moroccan luxury. The dominant scene is **deep**: the body sits on near-black warm ink (`#080604`) lit by oil-lamp brass and souk-ember terracotta. When the page steps "indoors" — long-form articles, FAQ rail, blog body — the surface flips to argan-sand (`#F0E6D0`), the editorial-magazine inversion. Display type is **Bebas Neue at extreme scale** (up to 7.25rem / ~116px), tracked open and uppercase, like a movie title card. Body text is restrained, low-weight Karla. Italic Libre Baskerville carries inline emphasis in a single brass color. A monospaced micro-eyebrow (DM Mono, 11px, letter-spacing 0.32em) runs through every section as the connective tissue, like a film slate.

The homepage is structured as a sequence of eight numbered sections (01 through 08), preceded by an unindexed cinematic Hero with looped silent video and followed by a sign-off Footer. Each section is one moment, never a feature list. Sections alternate between cold ink (`#080604`) for atmospheric stages and ink-light (`#100D08`) for editorial reading panels, building rhythm without monotony.

This system explicitly rejects: aggregator-listicle layouts, platform-booking transactional UI, generic "Moroccan-themed" tourist kitsch (red-and-gold gradients, mosaic-pattern wallpaper, lantern clipart, decorative-Arabic display fonts), and SaaS-tech minimalism (white background, Inter / Geist, gradient hero, spacious uniform card grids). When a choice could go any of those directions, it goes the other way.

**Key Characteristics:**
- Dark by default (ink); inverts to argan-sand for editorial reading surfaces (article pages, FAQ body)
- Massive Bebas Neue display type, used like a film title — never as a generic "headline"
- Mono uppercase eyebrows (0.32em tracking) connect every block like a film slate
- Saturated, committed ember + brass; ember earns ≤15% of any screen
- SVG grain overlay over Hero only; flat hairlines (1px brass at 12–18% opacity) carry depth on internal sections
- Diamond glyphs (rotated 45° 1.5–7px squares) replace bullets, dots, arrows, and chevrons
- Fixed nav with scroll-aware backdrop; one canonical CTA across the entire site ("Book your dinner")
- Animations are transform / opacity only, ease-out exponential, ≤1200ms, `prefers-reduced-motion` aware

## 2. Colors

A four-family palette derived from a Moroccan night interior: deep stone, parchment, brass, terracotta. Saturated and committed; nothing is muted toward "tasteful neutral."

### Primary

- **Souk Ember** (`#C1622F`): the brand's voice. Used on primary CTAs (the canonical "Book your dinner" pill), rotated-square accents in eyebrows, list-bullet diamonds, hero radial-gradient cores, hairline reveal accents on hover, and the numeric stamps in the HowTo timeline. The single color a visitor should read as "La Table." Hover steps to `#D97040` (Souk Ember Light).

### Secondary

- **Marrakech Brass** (`#B8935A`): the second voice — warmer, quieter than ember. Used for faint hairline rules (`rgba(184,147,90,0.12–0.30)`), eyebrow text on dark surfaces, ghost-button border, the rotated-diamond separators between marquee items. Light tint `#D4AA70` (Riad Brass) is the link / emphasis color on dark surfaces and the color of all italic Libre Baskerville inline accents.

### Tertiary

The system runs on Primary + Secondary + Neutral. No tertiary accent.

### Neutral (warm, never gray)

- **Riad Ink** (`#080604`): the dominant surface — body background, Hero, BookingSection, Testimonials, WhyUs, HowTo, MoreLinks, footer base. Tinted warm; never pure black.
- **Riad Ink Soft** (`#100D08`): the alternating section band — TrustedBy press strip, About, Features, FeaturedMenu, FAQ. Also the surface for all editorial cards (testimonial cards, featured-journal article card, FeaturedMenu carte container).
- **Argan Sand** (`#F0E6D0`): the editorial inversion — body background for long-form article pages, FAQ answer text on dark surfaces. The cream paper the dark site flips into when content density rises.
- **Sand Muted** (`#B0A48A`): muted variant for secondary text on dark surfaces. The everyday body-text-on-ink color.
- **Medina Stone** (`#5C5040`): low-priority text on light surfaces; appears in the dark site as `--muted-deep` only inside legal-line tertiary text.

### Service-only

- **WhatsApp Green** (`#25D366`): used **only** on the WhatsApp number link in the nav and the "Message us on WhatsApp" sign-off CTA in the footer. Treated as an external brand artifact, not part of the system's voice. Never appears anywhere else.

### Named Rules

**The One Ember Rule.** Souk Ember is the brand's only "voice" color. It earns ≤15% of any screen and is never used decoratively (no ember backgrounds for paragraph blocks, no ember-tinted card surfaces). It runs primary CTAs, single-pixel accent rules, list-bullet diamonds, the hot center of the Hero radial gradient, and section numeral stamps — and that is all.

**The Warm-Ink Rule.** No `#000`, no `#fff`, ever. Black is `#080604` (warm ink). White is `#F0E6D0` (argan sand). The Hero grain overlay reads off this distinction.

**The Service-Only Green Rule.** WhatsApp green appears in exactly two scoped places — the nav phone number and the footer's "Message us on WhatsApp" alternate-path CTA. Do not pull it into the system as a success / confirmation color, do not tint cards with it, do not let it leak.

## 3. Typography

**Display Font:** Bebas Neue (with Arial Black, Impact fallbacks)
**Serif Italic:** Libre Baskerville italic only (with Times New Roman, Georgia fallbacks)
**Body Font:** Karla, weight 300 (with -apple-system, Helvetica Neue fallbacks)
**Mono / Eyebrow Font:** DM Mono (with ui-monospace, Courier fallbacks)
**Arabic Pairing:** Noto Sans Arabic (paired across all roles for AR pages; never auto-fallback)

**Character:** Bebas at extreme scale gives the page a film-poster gravity that no humanist sans can produce; Karla 300 is its quiet conversational counterpart. Libre Baskerville italic appears only in brass for inline emphasis or pull-quote moods — never in upright Roman, never as body. DM Mono is the connective tissue: every section opens with a tracked-out 11px micro-eyebrow that names the moment, like a film slate.

### Hierarchy

- **Display** (Bebas Neue, weight 400, `clamp(3rem, 9vw, 7.25rem)`, line-height 0.92, letter-spacing 0.02em, uppercase): the title card. The Hero headline only. Standalone, with a short serif-italic descender allowed underneath at `0.42em` of the display size.
- **Headline** (Bebas Neue, 400, `clamp(2.25rem, 4.5vw, 3.75rem)`, line-height 1, letter-spacing 0.04em, uppercase): section H2. Every numbered homepage section uses this. Carries an inline serif-italic phrase in `gold-light` color for warmth.
- **Sub-display** (Bebas Neue, 400, `clamp(1.6rem, 2.6vw, 2.4rem)`, line-height 1.05): card titles inside sections (each timeline step in HowTo, each experience tile, each FeaturedMenu course note).
- **Serif Italic** (Libre Baskerville italic, 400, 14–22px depending on context, line-height 1.55–1.65, color `gold-light`): inline emphasis only. Pull-quote feel. Used inside `<em>` tags within display/headline text and as testimonial blockquote body. Never used upright. Never used for body or labels.
- **Body** (Karla, 300, 15px global / 15–17px in section bodies, line-height 1.65–1.75, max-width 64ch / 58ch / 42ch depending on column width): paragraph copy. Lower weight is intentional — gives the page its breath.
- **Lead** (Karla, 300, 17px, line-height 1.7): hero body / opening paragraph; slightly larger than body.
- **Eyebrow** (DM Mono, 400, 11px, letter-spacing 0.32em, uppercase, color `gold-light`): named-section connectors, the "01 · The truth" labels, breadcrumbs. The single most-repeated typographic element. Always paired with a 6×6 ember rotated-square dot to the left.
- **Label** (DM Mono, 400, 10px, letter-spacing 0.22–0.28em, uppercase, color varies — `gold-light` for accents, `sand-muted` for meta): button text, micro-trust lines, course notes ("Main · 90 min"), aggregate stats, "Read all reviews" links, hairline-text CTAs.

### Named Rules

**The Bebas-or-Karla Rule.** Display is Bebas, body is Karla, eyebrows are DM Mono, italics-only is Libre Baskerville. There are no other faces. Do not introduce a fifth font for "variety" — variety lives in scale and weight contrast within these four.

**The Tracked-Mono Rule.** Every uppercase label, eyebrow, button, breadcrumb, table header, and meta line is DM Mono with letter-spacing in the 0.18em–0.34em range. Tracking ≤0.18em looks like a bug; tracking ≥0.36em starts to disintegrate. Stay inside the corridor.

**The No-Upright-Serif Rule.** Libre Baskerville is italic only, in `gold-light` color, for inline emphasis. Upright Libre Baskerville is forbidden — it becomes "luxury restaurant menu" cliché and breaks the editorial frame.

**The Italic-Em Rule.** Every section headline pairs an uppercase Bebas main phrase with a short italic-serif accent inside a single `<em>` element. The accent is one to four words, lowercased, in `gold-light` at `0.42–0.55em` of the display size, blocked under the main phrase via `display: block`. Example: *Three questions. One reply.* / *— confirmed in 24 hours.*

## 4. Elevation

The system is **flat by default**: surfaces don't lift off the canvas via shadow; depth comes from tonal layering (`ink` → `ink-light`), 1px hairline rules in faint brass, and **soft radial gradients** that read as warm light pooling into the frame. Three named atmospheric devices carry depth without geometry: the Hero grain overlay, the radial ember glows, and the rotated-diamond mark system.

The only places shadow appears:
1. **Primary CTA buttons.** A copper-tinted drop shadow (`0 18px 40px -12px rgba(184, 79, 46, 0.55)` on standard pills, `0 22px 50px -16px rgba(184, 79, 46, 0.55)` on the footer sign-off variant) — the button "ignites" rather than "lifts."
2. **The About chef-inset card.** A deep ambient drop (`0 22px 50px -20px rgba(0, 0, 0, 0.65)`) anchors the overlapping inset photo against the larger portrait behind it.

### Shadow Vocabulary

- **Ember Ignite** (`box-shadow: 0 18px 40px -12px rgba(184, 79, 46, 0.55)`): primary CTA pills (Hero, BookingSection, HowTo close).
- **Ember Ignite Deep** (`box-shadow: 0 22px 50px -16px rgba(184, 79, 46, 0.55)`): the footer sign-off WhatsApp CTA pill, slightly larger drop for section-closing weight.
- **Ambient Drop** (`box-shadow: 0 22px 50px -20px rgba(0, 0, 0, 0.65)`): the overlapping inset photo in About only.

### Named Rules

**The Grain Rule.** A fixed SVG-noise grain (inline data URI, `mix-blend-mode: overlay`, opacity 0.08) sits over the Hero only. It is the difference between a flat dark hero and a Moroccan night interior. The BookingFlowInfographic carries the same grain at opacity 0.06 to share that hero-warm paper feel.

**The Hairline Rule.** Borders are 1px in faint brass (`border-gold/15` or `rgba(184,147,90,0.15)`) by default; stronger rules go to `border-gold/30`; faintest dividers go to `border-gold/12`. Never use a 2px+ solid border; never use a default-gray border.

**The Layered-Radial Rule.** Hero, BookingSection, FeaturedMenu, the Hero Quote testimonial card, and the BookingFlowInfographic each carry one soft ember radial glow (`bg-ember/8–15`, `blur-3xl`) anchored above center to evoke "lit interior" warmth. Always behind content, always blurred, never decorative-only — it must do the work of conveying warmth in the absence of shadow.

**The Duotone Rule.** Signature photographic images (Hero video, BookingSection plate, About filmstrip frames, HowTo step images, Intermission) carry the `lt-duotone-soft` filter — an SVG `feColorMatrix` + `feComponentTransfer` chain that maps shadows → ink, midtones → ember, highlights → sand. The filter definition lives once at the top of `<body>` (Layout.astro). It composes with the existing `bg-ember/10–20 mix-blend-multiply` overlay; the combination reads as a warm film print, not a tinted photograph. Photo cards that already have their own colour grading (logos, brand photography) opt out by omitting the class.

**The Parallax Rule.** Any signature image inside an `overflow-hidden` wrapper may opt into scroll-driven parallax via `data-parallax="0.08–0.18"`. Factors above 0.2 read as jittery and are clamped by the script. The Layout-level rAF-throttled handler updates a `--lt-py` CSS variable on each tracked element; the global `[data-parallax]` rule translates by that variable. Elements outside the viewport are skipped, and the entire system is disabled under `prefers-reduced-motion`. Use sparingly: hero video, BookingSection plate, About filmstrip top frame, Intermission image, and HowTo step images — and nowhere else. Parallax everywhere is parallax nowhere.

## 5. Components

For each component, lead with a short character line, then specify shape, color assignment, states, and any distinctive behavior.

### Buttons

- **Shape:** mostly **fully rounded pills** (`rounded-full`) for primary CTAs — a deliberate departure from the previous 2px-radius square — to evoke the warmth of a reduction rather than the snap of a tech UI. Disclosure / show-more buttons also use pill radius. Hairline-with-text CTAs (text + expanding underline) have no radius.
- **Primary** (`bg-ember px-9 py-4 rounded-full`): souk-ember background, white text, DM Mono 12px letter-spacing 0.22em uppercase. Hover ignites with Ember Ignite shadow + `-translate-y-px` lift + steps to `ember-light`. Paired with a 7×7 white rotated-square glyph instead of an arrow. **The canonical CTA: "Book your dinner."** Used in Hero, BookingSection, HowTo close. The footer's primary CTA is a sibling variant with deeper drop shadow ("Message us on WhatsApp").
- **Disclosure pill** (`rounded-full border border-gold/30 px-6 py-3`): the FeaturedMenu's "Show 5 more plates" button. Mono caps, `text-gold-light` default, hover gains `border-ember` + `bg-ember/10` + `text-sand`. A small rotated-diamond chevron rotates 225° when the disclosure is expanded.
- **Hairline-text CTA** (text + expanding rule): the most-used "ghost" pattern. DM Mono 11px tracked 0.28em uppercase `text-gold-light`, followed by a 10-wide brass hairline (`h-px w-10 bg-gold/60`). On hover the rule widens to `w-16` and changes color to `bg-ember`. Used in About, WhyUs sidebar, FAQ sidebar, FeaturedMenu, MoreLinks, anywhere the page needs a quiet "more" affordance.
- **WhatsApp link**: green `#25D366` text-color only inside the Nav phone number; the footer sign-off CTA is an ember pill, not WhatsApp-green.

### Eyebrow

The connective tissue of the system. **DM Mono 11px, letter-spacing 0.32em, uppercase, color `gold-light`.** Always paired with a 6×6 souk-ember rotated-square diamond (`size-1.5 rotate-45 bg-ember`) to the left. Sits above every major section title. Carries the section number for homepage sections: *"01 · The truth"*, *"02 · The all-in"*, *"03 · A sample tasting"*, etc. Numbering is sequential 01–08 in page order — no skips, no out-of-order.

### Cards / Containers

- **Editorial card surface:** `border border-gold/15 bg-ink-light` with no radius (sharp corners). Hover state lifts the border to `border-ember/50` or `border-ember/60`. Used for: review cards, testimonial featured card, featured journal article, FeaturedMenu carte container.
- **Card-on-card depth:** when a `bg-ink-light` card sits inside a `bg-ink` section (Testimonials, MoreLinks), the contrast is intentional — the card "lifts out" of the dark stage. Inverse never happens.
- **The FeaturedMenu carte:** `border border-gold/20 bg-ink` with **four 12×12 ember corner marks** at the outer corners (the four `:before/:after`-style L-brackets). These corner marks are the carte's signature — they appear only here and on the BookingFlowInfographic, which is itself a sub-card with the same treatment. Combined with a soft ember radial glow above the header line and a divided ordered-list interior, the carte reads as a printed restaurant menu set in a candlelit room.

### Disclosure pattern

The FeaturedMenu uses a **show-more disclosure** to surface five additional courses (VI–X) beneath the main tasting. The hidden list is `<ol [hidden]>` until a button toggles `aria-expanded`. On expand: each `<li>` fades up (`translateY(8px) → 0` + opacity, 600ms ease-out, 60ms stagger), the button label flips to "Show fewer plates," and a rotated-diamond glyph rotates 225° to point up. On collapse: list re-hides via the `hidden` attribute, button scrolls itself back into view via `scrollIntoView({behavior:'smooth', block:'center'})`. `prefers-reduced-motion` disables the stagger entirely.

### Image cards

- **Aspect ratios:** `aspect-square` for course thumbnails in FeaturedMenu (uniform across all 10 courses), `aspect-[5/4]` for HowTo timeline photos and BookingFlowInfographic, `aspect-[4/5]` for the About chef portrait. `aspect-[16/10]` is now unused on the homepage.
- **Color treatment:** every photo card gets `bg-ember/10–20 mix-blend-multiply` to push warmth + `bg-gradient-to-t from-ink via-ink/35–55 to-transparent` for readability of any overlaid copy. The BookingFlowInfographic is the explicit exception — no color overlay, because its content is typeset text rather than photographic.
- **Hover:** image plates scale `1.03–1.05` over 1200ms ease-out. No other state changes on hover.

### Inputs / Fields (BookingForm)

The BookingForm is a React island using shadcn primitives themed to the brand: `Input` and `Select` triggers use `border-input` (faint brass via `--border`), 32px height (`h-8`), `rounded-lg` (8px — softer than the rest of the site, intentionally because form fields are utilitarian). Labels are Karla 14px (`text-sm`) — *not* DM Mono uppercase — because input labels should feel like prose, not slate. The submit button uses the brand's `Button` shadcn primitive in `bg-primary` + size `lg`. On submit, the form opens WhatsApp pre-filled and replaces itself with a success card (`border-ember/40 bg-ink/40 p-6` with a small ember check disc, the message in a `bg-ink/60 font-mono` `<pre>` block, plus reopen / copy / reset controls). Localized EN / FR / AR via `document.documentElement.lang`.

### Navigation

- **Top nav** (`header.nav`): `position: fixed`, transparent at top of page, transitions to `bg-ink/86 + backdrop-blur(14px) + border-bottom: 1px solid rgba(184,147,90,0.12)` once scroll passes 24px. The state swap is driven by a `data-state="top|scrolled"` attribute toggled by a `scroll` listener (passive). Height: 76px, set via `--lt-nav-h: 76px` in `global.css`.
- **Brand mark:** an outlined ember diamond (11×11px, 1.5px border) followed by "LA TABLE" in Bebas at 22px tracked 3px, then a 1px brass divider rule, then "Marrakech" in Libre Baskerville italic 13px. The whole mark is a single anchor to `#hero`.
- **Nav links:** DM Mono 11px letter-spacing 2.4px uppercase `sand-muted`, hover lifts to `sand`. WhatsApp number gets the service-only green color. Below 900px, links hide and a hamburger button appears.
- **Mobile drawer:** fullscreen slide-down (`position: fixed; inset: 76px 0 0 0`) with a `bg-ink/96 + backdrop-blur(14px)` panel and ember-pill primary CTA at the bottom. Escape closes; body scroll locks via an `html.nav-locked` class.

### Signature: The Diamond Glyph

A small rotated square (1–8px square, transformed `rotate(45deg)`) appears: (1) inside eyebrow rows as a colored ember dot, (2) inside primary buttons as a directional glyph, (3) as `<li>` bullets in the BookingSection trust-list and About signature line, (4) as separators between marquee press items, (5) as menu-chip separators in BookingFlowInfographic. It is the visual equivalent of "the slate." Use it instead of arrow icons, instead of bullet circles, instead of plain dots — anywhere a small punctuation mark is needed.

### Signature: The BookingFlowInfographic

A horizontal, native-code reinterpretation of a poster that would otherwise be a static PNG. Lives inside HowTo step 01's image slot, fits the same `aspect-[5/4]` box as steps 02 and 03 so the timeline rhythm holds. Contents (top to bottom inside the 5:4 tile): ornamental eyebrow band → display headline → five-node numbered row with a gradient gold hairline connecting them → menu-chips strip (Tagine · Couscous · Pastilla · Royal feast, italic serif with diamond separators) → bottom mono-typeset promise band (`Reply within 1h` / `Confirmation · 24h`). Same ember corner marks as the FeaturedMenu carte. **This component is the model for any future "infographic in a photo slot" pattern** — typeset in real text, not rasterized.

### Signature: The Alternating Timeline (HowTo)

Three-step booking flow rendered as a vertical timeline with a centered hairline rule, oversized ember serif numerals (01 / 02 / 03) stamped on the rule, and rows that alternate image-left / image-right. Step text alternates side accordingly. On desktop the gradient hairline runs through the middle of the grid; on mobile it shifts to a left rail. The numeric stamp sits in the gutter where the hairline meets each row. This pattern is for sequential narrative content where the page wants to read like a film's reel, one frame at a time.

### Signature: The Press Marquee (TrustedBy)

Slow infinite-marquee horizontal scroll of italic-serif press names with rotated-diamond separators. Two duplicated tracks animate `transform: translateX(0) → -100%` linearly over 42s. Edge-faded via `mask-image: linear-gradient(to right, transparent, black 8%, black 92%, transparent)`. Top and bottom hairlines (`bg-gradient-to-r from-transparent via-gold/30 to-transparent`). `prefers-reduced-motion` disables the animation entirely — the list becomes a centered flex-wrap row.

### Signature: The Frame Slate

A persistent cinematic film-slate that connects the page's six numbered scenes into one cinematic sequence — the system's connective tissue at scale. On desktop (≥1024px) it sits as a fixed vertical strip on the inline-end edge of the viewport: a tracked-mono "Now showing" label, the current scene number in Bebas ember, the scene's eyebrow rotated vertically in `gold-light`, and a 120px hairline progress bar mapping page-scroll percentage. On mobile it collapses to a thin 2px ember-gold ribbon directly below the nav.

Sections opt in by setting `data-frame="NN|Label"` on their root `<section>`. The slate's script picks the frame whose center is closest to the viewport center via a single rAF-throttled scroll listener, updates the rail labels with an opacity tween, and scales the progress bar by `scrollY / maxScroll`. RTL-aware: the strip auto-flips to the inline-start edge in `dir="rtl"`. `aria-hidden="true"` because the section it's describing already has a heading; the slate is decorative scaffolding for sighted readers.

The slate currently registers six scenes — `01 The chef`, `02 The carte`, `03 The guests`, `04 The reasons`, `05 The flow`, `06 The questions`. Hero, TrustedBy, BookingSection, Intermission, and Footer are intentionally unnumbered — they are atmospheric or transitional frames in the sequence, not numbered scenes. New sections added between scenes must either pick a slot (and renumber subsequent scenes contiguously) or stay unnumbered.

### Signature: The Intermission

A single full-bleed atmospheric frame between two dense sections (currently BookingSection → About). The component takes one image bleeding edge-to-edge, one Libre Baskerville italic line of poetry overlaid in `gold-light` at `clamp(1.5rem, 3.4vw, 2.6rem)`, a top hairline strip with a tracked-mono meta line ("Marrakech · Terrace · 19:42"), and nothing else. No CTA, no list, no card. Carries the hero's CSS-noise grain at opacity 0.07 to share the lit-interior shell, the duotone filter on the image, and parallax at factor 0.12 on the image. Heights are tunable via the `height` prop — `short` (`58svh`) is the default, `tall` (`80svh`) for full-bleed brand moments.

This is the system's "breathe" pattern. Use one Intermission per page maximum. Two is monotony; zero is a missed beat between long sections.

### Signature: The Title-Card Hero

The hero is composed like a film title card. Desktop layout is asymmetric: left column carries the eyebrow, a Bebas display title broken poster-style across three short lines (e.g. `A PRIVATE / MOROCCAN / FEAST.`), an italic-serif descender at `0.22em` of the title size, and the primary CTA pill paired with a WhatsApp hairline-text CTA. Right column carries a vertical credit slate — a `dl` of four rows with `gold-light` tracked-mono `dt` labels and `sand` serif-italic `dd` values, each row separated by a 1px brass hairline. A bottom hairline strip beneath the grid carries the trust line ("★ 4.9 · 200+ villa guests · Reply within 1 hour · Confirmed in 24h") and a `Scroll` affordance.

Below `lg` the columns stack center-aligned, the slate collapses gracefully to a `max-width:420px` `ml-auto` block, and the bottom strip wraps. The video and poster sit at `h-[115%]` so the parallax (factor 0.18) never reveals an edge.

### Signature: The Filmstrip Portrait

Replaces the legacy single-portrait + tagine-inset About image. Three vertical frames (souk → stove → table), each `aspect-[5/4]` with the duotone filter, a small Bebas ember frame number (`01 / 02 / 03`) stamped top-start, and a bottom caption strip showing the moment + a time stamp (`At the souk · 06:42`). The frames are hairline-separated and bracketed by two faint CSS-only perforation strips down the outer edges, evoking a literal piece of film stock without becoming clipart. The text column carries a Libre Baskerville italic pull-quote at `clamp(1.4rem, 2.2vw, 2rem)` in `gold-light`, separated from the body by a 1px brass `border-s` rule. The chef stays anonymous on purpose — the voice line and the kitchen detail carry the credibility.

### Signature: The Hero Quote Testimonial

One massive featured quote at film-poster scale carries the entire emotional load of the Testimonials scene; two quieter supporting cards run below. The hero quote sits inside an `bg-ink-light` editorial card with the same four ember corner marks as the FeaturedMenu carte, a soft ember radial glow above it, a giant Bebas opening curly-quote at `clamp(4rem, 8vw, 7rem)` in `ember/70`, and a Libre Baskerville italic blockquote at `clamp(1.6rem, 3vw, 2.6rem)` in `gold-light`. The figcaption pairs the author + context in tracked-mono with a single "tasted the [dish]" rounded-pill chip that links directly into the FeaturedMenu carte — turning social proof into a menu cross-sell.

### Signature: The Roman-Numeral Grid

Replaces the lucide-icon list pattern for "reasons" sections. Six (or three / four / nine) items laid out in a 2-column grid on `sm+` (1-column on mobile), each row marked with an oversized ember Bebas Roman numeral (`I / II / III …`) at `clamp(2.5rem, 4vw, 3.5rem)`. The numeral hovers a few pixels up on hover. Headlines are short declarative phrases; bodies are restrained at `max-width: 42ch`. Drops the slightly-generic icon set; goes pure-typographic and more cinematic. Use this pattern any time the system wants a numbered grid that doesn't read as a feature table.

### Signature: The Nav Offset Pattern

Because the nav is `position: fixed`, the page body needs a top spacer or interior pages scroll under it. The system uses a global rule (`body { padding-top: var(--lt-nav-h, 76px) }`) plus a single negative-margin escape (`.lt-hero { margin-top: calc(var(--lt-nav-h) * -1) }`) so the Hero can still cover the full viewport while interior pages stay clear. Anchor targets (`#booking`, `#about`, etc.) all get `scroll-margin-top: 90px` so deep-links don't slide under the nav.

## 6. Do's and Don'ts

### Do:
- **Do** open every section with a DM Mono 11px eyebrow at 0.32em letter-spacing, paired with a souk-ember rotated-square dot. This is the brand's pulse.
- **Do** use Bebas Neue at *display* scale (3rem–7.25rem responsive clamp) for the Hero only; section headlines top out at 3.75rem. Using Bebas at 24px wastes it.
- **Do** number homepage sections sequentially 01 → 08 in actual page order. Sections may be added, removed, or reordered, but the visible numbers must stay sequential.
- **Do** flip dark → light when crossing from a marketing surface to an editorial reading surface (article body, FAQ rail body, blog). Ink for the cinematic moments; argan-sand for long-form reading.
- **Do** carry Libre Baskerville italic in `gold-light` color only, inside `<em>` tags within display/headline text and as testimonial blockquote body. Never as body, never upright.
- **Do** use the rotated-diamond glyph instead of arrow icons or plain bullet dots.
- **Do** ship Arabic with Noto Sans Arabic paired across all four roles, RTL-aware layout, copy reviewed natively. Never auto-fallback.
- **Do** keep one canonical CTA across the entire site — *"Book your dinner"* — for every in-page anchor to `#booking`. The footer's "Message us on WhatsApp" is the only alternate-path button.
- **Do** offset every in-page anchor target by `scroll-margin-top: 90px` so the fixed nav doesn't slide over them.
- **Do** apply the 6×6 ember corner marks (top-left / top-right / bottom-left / bottom-right) on the FeaturedMenu carte and the BookingFlowInfographic — they are the printed-menu signature.

### Don't:
- **Don't** use `#000` or `#fff`. Black is `#080604`, white is `#F0E6D0`.
- **Don't** introduce a fifth typeface. Bebas Neue / Libre Baskerville / Karla / DM Mono is the entire palette. No Inter, no Geist, no Playfair, no decorative-Arabic display fonts.
- **Don't** use Libre Baskerville upright. Italic-only-in-gold-light is the rule.
- **Don't** use Tailwind default colors. No default indigo / blue / slate. No `shadow-md`, no `transition-all`.
- **Don't** lay out content as an aggregator-listicle: identical tile cards in a 3×3 grid, each with image / heading / 2-line desc / "Learn more". *(PRODUCT.md anti-reference: Tripadvisor, GetYourGuide, Viator.)* Editorial primitives (timeline, bento, asymmetric grid) only.
- **Don't** present pricing as a fare table with calendar pickers and a sticky "Book now" CTA. *(PRODUCT.md anti-reference: OpenTable, Resy, SevenRooms.)* Pricing is named in editorial copy and confirmed via WhatsApp.
- **Don't** use red-and-gold gradients, mosaic patterns, lantern clipart, or "decorative" Arabic-style display fonts. *(PRODUCT.md anti-reference: generic Moroccan-themed tourist kitsch.)*
- **Don't** ship a white-background, Inter-bodied, gradient-hero, "AI-powered" landing page. *(PRODUCT.md anti-reference: SaaS-tech minimalism.)*
- **Don't** widen rules past 1px. Default rule weight is 1px in faint-brass at 12–18% opacity. 2px+ feels heavy and unspecial.
- **Don't** use `border-left` or `border-right` greater than 1px as a colored accent on cards, list items, callouts, or alerts. Use full borders, background tints, leading numbers/icons, or nothing.
- **Don't** use gradient text (`background-clip: text` with a gradient). Decorative, never meaningful. Use a single solid color. Emphasis via weight or size.
- **Don't** ship a modal as a first thought. Modals are usually laziness. The booking flow shows the form inline; the menu disclosure expands inline; the WhatsApp success state replaces the form inline.
- **Don't** let WhatsApp green leak. Two scoped places only: the nav phone number and the footer's "Message us on WhatsApp" alternate-path link. Not in success states, not in confirmation chips, not in highlights.
- **Don't** mute the ember radial glows for "performance" or "minimalism." They are the lit-interior effect. The Hero, BookingSection, FeaturedMenu, and BookingFlowInfographic each carry one.
