# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
Single-page static website for **La Table Marrakech** — a private chef service in Marrakech, Morocco. The site is a single `index.html` with inline styles, Tailwind CSS via CDN, structured data (JSON-LD), and multilingual hreflang support (EN/FR/AR). Domain: `latablemarrakech.com`.

## Always Do First
- **Invoke the `frontend-design` skill** before writing any frontend code, every session, no exceptions.

## Local Server
- **Always serve on localhost** — never screenshot a `file:///` URL.
- Start the dev server: `node serve.mjs` (serves the project root at `http://localhost:3000`)
- `serve.mjs` is a minimal Node.js static file server in the project root. Start it in the background before taking any screenshots.
- If the server is already running, do not start a second instance.

## Screenshot Workflow
- Use the Python screenshot tool: `python3 screenshot.py <url> [label]`
- Requires `websocket-client` pip package.
- Uses Chrome DevTools Protocol (headless Chrome at `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`).
- Screenshots are saved automatically to `./temporary screenshots/screenshot-N[-label].png` (auto-incremented, never overwritten).
- After screenshotting, read the PNG from `temporary screenshots/` with the Read tool — Claude can see and analyze the image directly.

## Reference Image Workflow
- If a reference image is provided: match layout, spacing, typography, and color exactly. Do not improve or add to the design.
- Screenshot your output, compare against reference, fix mismatches, re-screenshot. Do at least 2 comparison rounds. Stop only when no visible differences remain or user says so.
- When comparing, be specific: "heading is 32px but reference shows ~24px", "card gap is 16px but should be 24px"
- Check: spacing/padding, font size/weight/line-height, colors (exact hex), alignment, border-radius, shadows, image sizing

## Output Defaults
- Single `index.html` file, all styles inline, unless user says otherwise
- Tailwind CSS via CDN: `<script src="https://cdn.tailwindcss.com"></script>`
- Placeholder images: `https://placehold.co/WIDTHxHEIGHT`
- Mobile-first responsive

## Brand Assets
- Logo: `la-table-marrakech-logo.svg` in project root
- Brand guidelines PDF: `la-table-marrakech-brand-guidelines.pdf` in project root
- Food images: `.webp` and `.jpg` files in project root (tagine, pastilla, couscous, etc.)
- Use real assets — do not use placeholders where these exist.

## Key Site Details
- WhatsApp booking: `+212721354757` (primary CTA)
- Pricing: from €85/day
- Structured data: FoodService (LocalBusiness) + FAQPage schemas in `<head>`
- SEO: hreflang tags, geo meta tags, Open Graph, Twitter cards

## Anti-Generic Guardrails
- **Colors:** Never use default Tailwind palette (indigo-500, blue-600, etc.). Use brand colors from the guidelines.
- **Shadows:** Never use flat `shadow-md`. Use layered, color-tinted shadows with low opacity.
- **Typography:** Never use the same font for headings and body. Pair a display/serif with a clean sans. Apply tight tracking (`-0.03em`) on large headings, generous line-height (`1.7`) on body.
- **Gradients:** Layer multiple radial gradients. Add grain/texture via SVG noise filter for depth.
- **Animations:** Only animate `transform` and `opacity`. Never `transition-all`. Use spring-style easing.
- **Interactive states:** Every clickable element needs hover, focus-visible, and active states.
- **Images:** Add a gradient overlay (`bg-gradient-to-t from-black/60`) and a color treatment layer with `mix-blend-multiply`.
- **Spacing:** Use intentional, consistent spacing tokens — not random Tailwind steps.
- **Depth:** Surfaces should have a layering system (base → elevated → floating).

## Hard Rules
- Do not add sections, features, or content not in the reference
- Do not "improve" a reference design — match it
- Do not stop after one screenshot pass
- Do not use `transition-all`
- Do not use default Tailwind blue/indigo as primary color
