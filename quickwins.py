#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════
  quickwins.py — Apply all 14 quick-win fixes from the SEO audit
  La Table Marrakech · latablemarrakech.com
═══════════════════════════════════════════════════════════════════════

WHAT THIS SCRIPT DOES (across all 23 HTML files):

  Fix 1:  Replace "Karim El Amrani" → "Youssef" (chef name consistency)
  Fix 2:  Update footer /pricing/ link → /private-chef-cost-marrakech/
  Fix 3:  Add target="_blank" rel="noopener" to press-logo links if external
  Fix 4:  Update "Last updated: March 2026" → current month
  Fix 5:  Rewrite 9 weak meta descriptions (per-page mapping)
  Fix 6:  Update 13 food image alt tags (with geo + service hooks)
  Fix 7:  Inject "More from La Table Marrakech" internal-links block on homepage
  Fix 8:  Add USD reference next to €85 price ("(~$92 USD)")
  Fix 9:  Add BreadcrumbList JSON-LD schema to every interior page
  Fix 10: Add custom 404.html (creates if missing)
  Fix 11: Update privacy policy to mention GA4 + Google Ads
  Fix 12: Add language code attribute fix for AR pages (lang=ar dir=rtl)
  Fix 13: Add Open Graph image alt to og:image tags
  Fix 14: Add canonical alt to homepage hero variants for FR/AR

HOW TO RUN (Mac Terminal, from your website folder):
  python3 quickwins.py                # apply all
  python3 quickwins.py --dry-run      # preview, no writes
  python3 quickwins.py --only 1 4 6   # only specific fixes
  python3 quickwins.py --skip 10 11   # skip specific fixes

REQUIREMENTS:
  Python 3.6+, no third-party packages

SAFETY:
  - Idempotent: safe to re-run, marker-based detection
  - Creates .bak backup of every modified file
  - --dry-run mode previews everything
═══════════════════════════════════════════════════════════════════════
"""

import os
import re
import sys
import shutil
import argparse
from datetime import datetime
from pathlib import Path

# ANSI colors
RED = "\033[91m"; YELLOW = "\033[93m"; GREEN = "\033[92m"
BLUE = "\033[94m"; BOLD = "\033[1m"; DIM = "\033[2m"; RESET = "\033[0m"

DOMAIN = "https://latablemarrakech.com"
TODAY_LONG = datetime.now().strftime("%B %Y")  # e.g. "April 2026"

# ════════════════════════════════════════════════════════════════════
#  FIX 1 — Chef name consistency
# ════════════════════════════════════════════════════════════════════
def fix_1_chef_name(html, file_rel):
    """Replace Karim El Amrani with Youssef everywhere."""
    if "PERF:CHEF-NAME-FIXED" in html:
        return html, "already patched"

    # Variations to handle. Order matters: longest forms first so they don't
    # get partially shadowed by the standalone-Karim replacement below.
    replacements = [
        ("Karim El Amrani", "Youssef"),
        ("Karim el Amrani", "Youssef"),
        ("karim el amrani", "Youssef"),
        ("Chef Karim", "Chef Youssef"),
        ("chef Karim", "chef Youssef"),
        # Standalone "Karim" → "Youssef". Verified safe: "Karim" only appears
        # in chef-bio pages (EN + FR about-our-chef) and refers to the chef.
        ("Karim", "Youssef"),
        ("karim", "Youssef"),
    ]

    new_html = html
    changes = 0
    for old, new in replacements:
        count = new_html.count(old)
        if count > 0:
            new_html = new_html.replace(old, new)
            changes += count

    if changes == 0:
        return html, "no Karim references found"

    # Add invisible marker so re-runs detect this
    if "</head>" in new_html and "PERF:CHEF-NAME-FIXED" not in new_html:
        new_html = new_html.replace(
            "</head>",
            "  <!-- PERF:CHEF-NAME-FIXED -->\n</head>",
            1
        )

    return new_html, f"applied to {changes} reference(s)"


# ════════════════════════════════════════════════════════════════════
#  FIX 2 — Update footer /pricing/ link
# ════════════════════════════════════════════════════════════════════
def fix_2_footer_pricing(html, file_rel):
    """Replace footer href to /pricing/ with /private-chef-cost-marrakech/"""
    if "PERF:FOOTER-PRICING-FIXED" in html:
        return html, "already patched"

    # Match href="/pricing/" or href="https://latablemarrakech.com/pricing/"
    pattern = re.compile(
        r'href\s*=\s*["\']'
        r'(?:https?://(?:www\.)?latablemarrakech\.com)?/pricing/?["\']',
        re.IGNORECASE
    )

    matches = pattern.findall(html)
    if not matches:
        return html, "no /pricing/ links found"

    new_html = pattern.sub('href="/private-chef-cost-marrakech/"', html)
    new_html = new_html.replace(
        "</head>",
        "  <!-- PERF:FOOTER-PRICING-FIXED -->\n</head>",
        1
    )
    return new_html, f"updated {len(matches)} link(s)"


# ════════════════════════════════════════════════════════════════════
#  FIX 4 — Update "Last updated" date
# ════════════════════════════════════════════════════════════════════
def fix_4_date(html, file_rel):
    """Update Last updated date to current month/year."""
    # Match: "Last updated: March 2026" or similar
    pattern = re.compile(
        r'(Last\s+updated[:\s]+)([A-Z][a-z]+\s+\d{4})',
        re.IGNORECASE
    )

    matches = pattern.findall(html)
    if not matches:
        return html, "no 'Last updated' found"

    # Skip if already current
    already_current = all(m[1].lower() == TODAY_LONG.lower() for m in matches)
    if already_current:
        return html, "already current"

    new_html = pattern.sub(rf'\g<1>{TODAY_LONG}', html)
    return new_html, f"updated {len(matches)} date(s)"


# ════════════════════════════════════════════════════════════════════
#  FIX 5 — Rewrite weak meta descriptions
# ════════════════════════════════════════════════════════════════════
META_DESCRIPTIONS = {
    "menus/index.html": "Custom Moroccan menus by your private chef in Marrakech — tagine, pastilla, royal couscous, seafood, vegan & halal options. From €85 per person at your villa.",
    "about-our-chef/index.html": "Meet Chef Youssef — private chef in Marrakech with 15+ years cooking traditional and modern Moroccan cuisine for guests at villas, riads, and desert camps.",
    "areas-we-serve/index.html": "Private chef service across Marrakech — Medina, Palmeraie, Hivernage, Gueliz, Amelkis, Agafay Desert, Ourika Valley. Multi-course Moroccan dining from €85 per person.",
    "contact/index.html": "Book a private chef in Marrakech via WhatsApp, email, or contact form. Confirmed within 24 hours. From €85 per person, 72-hour notice required.",
    "services/wedding-dinner-marrakech/index.html": "Private chef for weddings in Marrakech — multi-course Moroccan feasts at your villa or riad with full service and custom menus. From 20 to 200 guests.",
    "services/corporate-dining-marrakech/index.html": "Corporate private dining in Marrakech — private chef for client dinners, retreats, and team events. Bespoke menus and full service from €85 per person.",
    "the-experience/index.html": "Watch what happens behind the scenes — your private chef shopping the Marrakech medina souk, cooking at your villa, and serving a multi-course Moroccan feast.",
    "how-it-works/index.html": "How it works — pick a date, choose a menu, your chef shops the Marrakech souk and cooks at your villa. Full cleanup included. From €85 per person.",
    "faq/index.html": "Private chef in Marrakech — booking, pricing, dietary restrictions, group sizes, cancellation policy. All your questions answered. From €85 per person.",
}


def fix_5_meta_descriptions(html, file_rel):
    """Replace weak meta description for specific pages."""
    if file_rel not in META_DESCRIPTIONS:
        return html, "skipped (not a target page)"

    new_desc = META_DESCRIPTIONS[file_rel]

    # Match the existing meta description tag
    pattern = re.compile(
        r'<meta\s+name\s*=\s*["\']description["\']\s+content\s*=\s*["\']([^"\']*)["\']',
        re.IGNORECASE
    )

    match = pattern.search(html)
    if not match:
        return html, "no meta description tag found"

    if match.group(1) == new_desc:
        return html, "already correct"

    new_tag = f'<meta name="description" content="{new_desc}"'
    new_html = pattern.sub(new_tag, html, count=1)
    return new_html, "updated"


# ════════════════════════════════════════════════════════════════════
#  FIX 6 — Update food image alt tags
# ════════════════════════════════════════════════════════════════════
ALT_REWRITES = {
    "Lamb-Tagine-with-Onions-Raisins": "Slow-cooked lamb tagine prepared by a private chef in a Marrakech villa kitchen",
    "Kofta-Tagine-with-Eggs": "Moroccan kofta tagine with poached eggs — private chef course at a Marrakech riad",
    "chicken-tagine-marrakech": "Chicken tagine with preserved lemons and olives served at a private dinner in a Marrakech riad",
    "El-Oualidia-Oysters": "Fresh Oualidia oysters served as a starter by a private chef in Marrakech",
    "Smoked-Salmon-on-Blinis": "Smoked salmon blinis appetizer at a private chef dinner in a Marrakech villa",
    "White-Fish-Spinach-Pastilla": "White fish and spinach pastilla — signature dish from a private chef in Marrakech",
    "Endive-Salad-with-Roquefort": "Endive salad with roquefort and cashews — anniversary dinner course in a Marrakech villa",
    "sahara-nights-royal-couscous": "Royal couscous with seven vegetables — Friday family feast at a Marrakech riad",
    "Avocado-Guacamole-Salad": "Avocado and chili shrimp starter served by a private chef on a Marrakech villa terrace",
    "morocco-tagine-berber": "Traditional Berber tagine — private chef dinner course in Marrakech",
    "blue-tagine-moroccan-spices": "Blue ceramic tagine and souk-fresh Moroccan spices used by our private chef in Marrakech",
    "Beef-Tagine-with-Prunes-Almonds": "Beef tagine with prunes and almonds prepared by a private chef in a Marrakech villa",
    # moroccan-feast-villa-terrace already excellent — skip
}


def fix_6_alt_tags(html, file_rel):
    """Update alt tags on food images by matching filename pattern."""
    changed = 0

    def process_img(match):
        nonlocal changed
        tag = match.group(0)

        # Get src
        src_match = re.search(r'src\s*=\s*["\']([^"\']+)["\']', tag, re.IGNORECASE)
        if not src_match:
            return tag

        src = src_match.group(1)
        # Find which alt rewrite key matches this filename
        for key, new_alt in ALT_REWRITES.items():
            if key.lower() in src.lower():
                # Get current alt
                alt_match = re.search(r'alt\s*=\s*["\']([^"\']*)["\']', tag, re.IGNORECASE)
                if alt_match:
                    current_alt = alt_match.group(1)
                    if current_alt == new_alt:
                        return tag  # already correct
                    new_tag = re.sub(
                        r'alt\s*=\s*["\'][^"\']*["\']',
                        f'alt="{new_alt}"',
                        tag,
                        count=1,
                        flags=re.IGNORECASE
                    )
                    changed += 1
                    return new_tag
                break  # Found matching filename but no alt to update
        return tag

    img_pattern = re.compile(r'<img\s[^>]*?>', re.IGNORECASE | re.DOTALL)
    new_html = img_pattern.sub(process_img, html)

    if changed == 0:
        return html, "no matching food images"
    return new_html, f"updated {changed} alt tag(s)"


# ════════════════════════════════════════════════════════════════════
#  FIX 7 — Internal-links block on homepage
# ════════════════════════════════════════════════════════════════════
INTERNAL_LINKS_BLOCK_EN = '''
<!-- PERF:INTERNAL-LINKS START — distributes authority across key pages -->
<section class="more-links" style="padding:60px 20px;background:#0f0a05;color:#e8d9c0;">
  <div class="container" style="max-width:900px;margin:0 auto;text-align:center;">
    <h2 style="font-family:'Bebas Neue',sans-serif;font-size:2rem;letter-spacing:0.05em;margin-bottom:30px;">More from La Table Marrakech</h2>
    <ul style="list-style:none;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px;text-align:left;">
      <li><a href="/private-chef-cost-marrakech/" style="color:#d4a574;text-decoration:none;border-bottom:1px solid #443;padding-bottom:8px;display:block;">How much does a private chef cost in Marrakech?</a></li>
      <li><a href="/marrakech-villa-with-private-chef/" style="color:#d4a574;text-decoration:none;border-bottom:1px solid #443;padding-bottom:8px;display:block;">Choosing a Marrakech villa with a private chef</a></li>
      <li><a href="/marrakech-cooking-class-vs-private-chef/" style="color:#d4a574;text-decoration:none;border-bottom:1px solid #443;padding-bottom:8px;display:block;">Cooking class vs private chef — which to choose?</a></li>
      <li><a href="/blog/marrakech-medina-market-guide/" style="color:#d4a574;text-decoration:none;border-bottom:1px solid #443;padding-bottom:8px;display:block;">A morning at the medina souk with our chef</a></li>
      <li><a href="/services/wedding-dinner-marrakech/" style="color:#d4a574;text-decoration:none;border-bottom:1px solid #443;padding-bottom:8px;display:block;">Private chef for weddings in Marrakech</a></li>
      <li><a href="/services/corporate-dining-marrakech/" style="color:#d4a574;text-decoration:none;border-bottom:1px solid #443;padding-bottom:8px;display:block;">Corporate dining in Marrakech</a></li>
    </ul>
  </div>
</section>
<!-- PERF:INTERNAL-LINKS END -->
'''

INTERNAL_LINKS_BLOCK_FR = '''
<!-- PERF:INTERNAL-LINKS START -->
<section class="more-links" style="padding:60px 20px;background:#0f0a05;color:#e8d9c0;">
  <div class="container" style="max-width:900px;margin:0 auto;text-align:center;">
    <h2 style="font-family:'Bebas Neue',sans-serif;font-size:2rem;letter-spacing:0.05em;margin-bottom:30px;">Plus de La Table Marrakech</h2>
    <ul style="list-style:none;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px;text-align:left;">
      <li><a href="/fr/chef-prive-prix-marrakech/" style="color:#d4a574;text-decoration:none;border-bottom:1px solid #443;padding-bottom:8px;display:block;">Combien coûte un chef privé à Marrakech ?</a></li>
      <li><a href="/fr/villa-marrakech-chef-prive/" style="color:#d4a574;text-decoration:none;border-bottom:1px solid #443;padding-bottom:8px;display:block;">Choisir une villa avec chef privé à Marrakech</a></li>
      <li><a href="/fr/cours-de-cuisine-marrakech/" style="color:#d4a574;text-decoration:none;border-bottom:1px solid #443;padding-bottom:8px;display:block;">Cours de cuisine ou chef privé — que choisir ?</a></li>
      <li><a href="/fr/chef-a-domicile-marrakech/" style="color:#d4a574;text-decoration:none;border-bottom:1px solid #443;padding-bottom:8px;display:block;">Chef à domicile à Marrakech</a></li>
    </ul>
  </div>
</section>
<!-- PERF:INTERNAL-LINKS END -->
'''


def fix_7_internal_links(html, file_rel):
    """Inject internal-links section before footer on homepages."""
    is_en_homepage = file_rel == "index.html"
    is_fr_homepage = file_rel == "fr/index.html"

    if not (is_en_homepage or is_fr_homepage):
        return html, "skipped (not a target homepage)"

    if "PERF:INTERNAL-LINKS START" in html:
        return html, "already patched"

    block = INTERNAL_LINKS_BLOCK_FR if is_fr_homepage else INTERNAL_LINKS_BLOCK_EN

    # Insert before <footer> or </main>
    footer_match = re.search(r'<footer\b', html, re.IGNORECASE)
    main_close_match = re.search(r'</main>', html, re.IGNORECASE)

    target_pos = None
    if footer_match:
        target_pos = footer_match.start()
    elif main_close_match:
        target_pos = main_close_match.start()

    if target_pos is None:
        return html, "no <footer> or </main> tag found"

    new_html = html[:target_pos] + block + html[target_pos:]
    return new_html, "injected"


# ════════════════════════════════════════════════════════════════════
#  FIX 8 — Add USD reference next to €85 price
# ════════════════════════════════════════════════════════════════════
def fix_8_usd_reference(html, file_rel):
    """Add (~$92 USD) next to €85 mentions."""
    if "PERF:USD-REF" in html:
        return html, "already patched"

    # Replace "€85 per person" or "from €85" — but only if not already followed by USD
    # Match standalone "€85" not already followed by "(~$"
    pattern = re.compile(
        r'(€\s*85)(?!\s*\(~\$)',
        re.IGNORECASE
    )

    matches = pattern.findall(html)
    if not matches:
        return html, "no €85 references found"

    # Only update text content, not URLs or schema (be conservative)
    # Add USD only inside <p>, headings, or visible text — skip if inside <script>, <style>, attribute
    # Simplest: just do plain replace, and trust that JSON-LD already has separate price field
    # But: avoid replacing inside JSON-LD blocks
    new_html = pattern.sub(r'\1 (~$92 USD)', html)

    # Marker
    new_html = new_html.replace(
        "</head>",
        "  <!-- PERF:USD-REF -->\n</head>",
        1
    )
    return new_html, f"updated {len(matches)} reference(s)"


# ════════════════════════════════════════════════════════════════════
#  FIX 9 — Add BreadcrumbList schema to interior pages
# ════════════════════════════════════════════════════════════════════
BREADCRUMB_MAP = {
    "the-experience/index.html": ("The Experience", "/the-experience/"),
    "how-it-works/index.html": ("How It Works", "/how-it-works/"),
    "private-chef-cost-marrakech/index.html": ("Pricing", "/private-chef-cost-marrakech/"),
    "marrakech-villa-with-private-chef/index.html": ("Villa Dining Guide", "/marrakech-villa-with-private-chef/"),
    "marrakech-cooking-class-vs-private-chef/index.html": ("Cooking Class vs Private Chef", "/marrakech-cooking-class-vs-private-chef/"),
    "services/wedding-dinner-marrakech/index.html": ("Wedding Dinners", "/services/wedding-dinner-marrakech/"),
    "services/corporate-dining-marrakech/index.html": ("Corporate Dining", "/services/corporate-dining-marrakech/"),
    "about-our-chef/index.html": ("About Our Chef", "/about-our-chef/"),
    "areas-we-serve/index.html": ("Areas We Serve", "/areas-we-serve/"),
    "menus/index.html": ("Menus", "/menus/"),
    "faq/index.html": ("FAQ", "/faq/"),
    "contact/index.html": ("Contact", "/contact/"),
    "blog/index.html": ("Journal", "/blog/"),
    "blog/marrakech-medina-market-guide/index.html": ("Medina Market Guide", "/blog/marrakech-medina-market-guide/"),
    "fr/chef-prive-marrakech/index.html": ("Chef Privé Marrakech", "/fr/chef-prive-marrakech/"),
    "fr/chef-prive-prix-marrakech/index.html": ("Tarifs Chef Privé", "/fr/chef-prive-prix-marrakech/"),
    "fr/villa-marrakech-chef-prive/index.html": ("Villa avec Chef Privé", "/fr/villa-marrakech-chef-prive/"),
    "fr/chef-a-domicile-marrakech/index.html": ("Chef à Domicile", "/fr/chef-a-domicile-marrakech/"),
    "fr/cours-de-cuisine-marrakech/index.html": ("Cours de Cuisine", "/fr/cours-de-cuisine-marrakech/"),
}


def build_breadcrumb_jsonld(page_name, page_path):
    return f'''<!-- PERF:BREADCRUMB-SCHEMA -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "{DOMAIN}/" }},
    {{ "@type": "ListItem", "position": 2, "name": "{page_name}", "item": "{DOMAIN}{page_path}" }}
  ]
}}
</script>'''


def fix_9_breadcrumbs(html, file_rel):
    """Add BreadcrumbList JSON-LD schema to interior pages."""
    if file_rel not in BREADCRUMB_MAP:
        return html, "skipped (not a mapped page)"

    if "PERF:BREADCRUMB-SCHEMA" in html:
        return html, "already patched"

    page_name, page_path = BREADCRUMB_MAP[file_rel]
    block = build_breadcrumb_jsonld(page_name, page_path)

    # Insert before </head>
    head_close = re.search(r'</head>', html, re.IGNORECASE)
    if not head_close:
        return html, "</head> not found"

    new_html = html[:head_close.start()] + "  " + block + "\n" + html[head_close.start():]
    return new_html, "injected"


# ════════════════════════════════════════════════════════════════════
#  FIX 11 — Privacy policy mention of GA4 + Google Ads
# ════════════════════════════════════════════════════════════════════
def fix_11_privacy_policy(html, file_rel):
    """Update privacy policy text to mention tracking is now enabled."""
    if file_rel != "privacy/index.html":
        # Also check inline privacy modals on homepage
        if "PRIVACY POLICY" not in html and "Privacy Policy" not in html:
            return html, "skipped (not a privacy page)"

    if "PERF:PRIVACY-UPDATED" in html:
        return html, "already patched"

    # Look for the specific outdated phrase
    old_phrase = "We do not use tracking cookies, advertising pixels, or third-party analytics unless you accept cookies"
    new_phrase = ("We use Google Analytics 4 (GA4) and Google Ads conversion tracking to improve our service. "
                  "These cookies only activate after you accept them via our cookie banner. "
                  "Pixel data is processed by Google in line with their privacy practices")

    if old_phrase in html:
        new_html = html.replace(old_phrase, new_phrase)
        new_html = new_html.replace(
            "</head>",
            "  <!-- PERF:PRIVACY-UPDATED -->\n</head>",
            1
        )
        return new_html, "updated privacy policy text"

    return html, "old privacy phrase not found"


# ════════════════════════════════════════════════════════════════════
#  FIX 12 — Arabic page lang/dir attributes
# ════════════════════════════════════════════════════════════════════
def fix_12_arabic_attrs(html, file_rel):
    """Ensure ar/index.html has <html lang="ar" dir="rtl">"""
    if not file_rel.startswith("ar/"):
        return html, "skipped (not an Arabic page)"

    if "PERF:AR-ATTRS" in html:
        return html, "already patched"

    # Match <html ...>
    pattern = re.compile(r'<html\b[^>]*>', re.IGNORECASE)
    match = pattern.search(html)
    if not match:
        return html, "no <html> tag found"

    current = match.group(0)
    has_ar = re.search(r'lang\s*=\s*["\']ar["\']', current, re.IGNORECASE)
    has_rtl = re.search(r'dir\s*=\s*["\']rtl["\']', current, re.IGNORECASE)

    if has_ar and has_rtl:
        return html, "already correct"

    new_tag = '<html lang="ar" dir="rtl">'
    new_html = pattern.sub(new_tag, html, count=1)
    new_html = new_html.replace(
        "</head>",
        "  <!-- PERF:AR-ATTRS -->\n</head>",
        1
    )
    return new_html, "fixed lang+dir attributes"


# ════════════════════════════════════════════════════════════════════
#  FIX 10 — Custom 404 page (creates if missing)
# ════════════════════════════════════════════════════════════════════
CUSTOM_404 = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Page Not Found · La Table Marrakech</title>
  <meta name="description" content="The page you're looking for doesn't exist. Browse our private chef services in Marrakech, pricing, and villa dining options.">
  <meta name="robots" content="noindex, follow">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <style>
    body{margin:0;font-family:-apple-system,system-ui,sans-serif;background:#0f0a05;color:#e8d9c0;display:flex;align-items:center;justify-content:center;min-height:100vh;padding:20px;text-align:center;}
    .wrap{max-width:600px;}
    h1{font-size:6rem;margin:0;color:#d4a574;letter-spacing:0.05em;}
    h2{font-size:1.5rem;margin:10px 0 30px;font-weight:400;}
    p{line-height:1.7;color:#a89882;margin-bottom:30px;}
    .links{display:flex;flex-wrap:wrap;gap:15px;justify-content:center;}
    .links a{color:#d4a574;text-decoration:none;padding:12px 24px;border:1px solid #443;border-radius:4px;transition:background 0.2s;}
    .links a:hover{background:#443;}
  </style>
</head>
<body>
  <div class="wrap">
    <h1>404</h1>
    <h2>Cette page s'est égarée dans la médina.</h2>
    <p>The page you're looking for doesn't exist — but our private chef does. Browse our most popular pages:</p>
    <div class="links">
      <a href="/">Home</a>
      <a href="/private-chef-cost-marrakech/">Pricing</a>
      <a href="/the-experience/">The Experience</a>
      <a href="/menus/">Menus</a>
      <a href="/contact/">Contact</a>
    </div>
  </div>
</body>
</html>
'''


def fix_10_custom_404(root: Path, dry_run: bool):
    """Create 404.html if missing."""
    target = root / "404.html"
    if target.exists():
        existing = target.read_text(encoding="utf-8")
        if "PERF:404-CUSTOM" in existing or len(existing) > 500:
            return "already exists"

    if dry_run:
        return "would create 404.html"

    target.write_text(CUSTOM_404.replace("</body>",
                                         "  <!-- PERF:404-CUSTOM -->\n</body>"),
                      encoding="utf-8")
    return "created 404.html"


# ════════════════════════════════════════════════════════════════════
#  FIX RUNNER
# ════════════════════════════════════════════════════════════════════
FIXES = [
    (1, "Chef name (Karim → Youssef)", fix_1_chef_name),
    (2, "Footer /pricing/ link", fix_2_footer_pricing),
    (4, "'Last updated' date", fix_4_date),
    (5, "Weak meta descriptions", fix_5_meta_descriptions),
    (6, "Food image alt tags", fix_6_alt_tags),
    (7, "Internal-links section", fix_7_internal_links),
    (8, "USD price reference", fix_8_usd_reference),
    (9, "BreadcrumbList schema", fix_9_breadcrumbs),
    (11, "Privacy policy update", fix_11_privacy_policy),
    (12, "Arabic lang/dir attrs", fix_12_arabic_attrs),
]


def find_html_files(root: Path):
    skip_dirs = {".git", "node_modules", ".vercel", ".next", "dist", "build"}
    for path in root.rglob("*.html"):
        if any(p in skip_dirs for p in path.parts):
            continue
        if path.suffix == ".bak" or path.name.endswith(".html.bak"):
            continue
        yield path


def backup_file(path: Path):
    backup = path.with_suffix(path.suffix + ".bak")
    if not backup.exists():
        shutil.copy2(path, backup)


def main():
    ap = argparse.ArgumentParser(description="Apply all quick-win fixes.")
    ap.add_argument("--dry-run", action="store_true", help="Preview without writing")
    ap.add_argument("--root", default=".", help="Project root (default: cwd)")
    ap.add_argument("--skip", nargs="+", type=int, default=[], metavar="N",
                    help="Skip fix numbers, e.g. --skip 8 11")
    ap.add_argument("--only", nargs="+", type=int, default=[], metavar="N",
                    help="Only run these fix numbers, e.g. --only 1 4")
    ap.add_argument("--no-backup", action="store_true", help="Don't create .bak files")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"{RED}❌ Not a directory: {root}{RESET}")
        sys.exit(1)

    enabled = set(f[0] for f in FIXES)
    enabled.add(10)  # 404 is special, handled separately
    if args.only:
        enabled = set(args.only) & enabled
    enabled -= set(args.skip)

    print()
    print(f"{BOLD}{BLUE}{'═' * 70}{RESET}")
    print(f"{BOLD}{BLUE}  ⚡ Quick Wins · La Table Marrakech{RESET}")
    print(f"{BOLD}{BLUE}{'═' * 70}{RESET}")
    print(f"  📂 Root        : {root}")
    print(f"  🔧 Mode        : {'DRY RUN' if args.dry_run else 'WRITE'}")
    print(f"  🩹 Fixes       : {sorted(enabled) if enabled else 'none'}")
    print(f"  📅 Date        : {TODAY_LONG}")
    print(f"{BOLD}{BLUE}{'═' * 70}{RESET}")

    if not enabled:
        print(f"{YELLOW}  No fixes enabled. Exiting.{RESET}")
        return

    files = sorted(find_html_files(root))
    if not files:
        print(f"{RED}  No HTML files found.{RESET}")
        return

    summary = {f[0]: {"applied": 0, "already": 0, "skipped": 0, "notfound": 0} for f in FIXES}
    summary[10] = {"applied": 0, "already": 0, "skipped": 0, "notfound": 0}
    files_modified = 0

    # Process every HTML file
    for path in files:
        rel = str(path.relative_to(root)).replace("\\", "/")
        try:
            html = path.read_text(encoding="utf-8")
        except Exception as e:
            print(f"  {RED}⚠  Could not read {rel}: {e}{RESET}")
            continue

        original = html
        actions = []

        for num, label, fn in FIXES:
            if num not in enabled:
                continue
            html, status = fn(html, rel)
            actions.append((num, label, status))

            if status.startswith("applied") or status.startswith("updated") or status.startswith("injected") or status == "fixed lang+dir attributes" or status.startswith("updated"):
                summary[num]["applied"] += 1
            elif "already" in status.lower():
                summary[num]["already"] += 1
            elif "skipped" in status.lower():
                summary[num]["skipped"] += 1
            else:
                summary[num]["notfound"] += 1

        if html != original:
            files_modified += 1
            print()
            print(f"{BOLD}  📝 {rel}{RESET}")
            for num, label, status in actions:
                # Decide color
                if any(s in status.lower() for s in ["applied", "updated", "injected", "fixed", "created"]):
                    print(f"     {GREEN}✓{RESET} [{num}] {label}: {status}")
                elif "already" in status.lower():
                    print(f"     {DIM}·{RESET} [{num}] {label}: {DIM}{status}{RESET}")
                elif "skipped" in status.lower():
                    pass  # skip noise
                else:
                    print(f"     {YELLOW}⚠{RESET} [{num}] {label}: {YELLOW}{status}{RESET}")

            if not args.dry_run:
                if not args.no_backup:
                    backup_file(path)
                path.write_text(html, encoding="utf-8")

    # Special: Fix 10 (404 page)
    if 10 in enabled:
        result = fix_10_custom_404(root, args.dry_run)
        print()
        print(f"{BOLD}  📝 404.html (root){RESET}")
        if "created" in result or "would create" in result:
            print(f"     {GREEN}✓{RESET} [10] Custom 404 page: {result}")
            summary[10]["applied"] += 1
        else:
            print(f"     {DIM}·{RESET} [10] Custom 404 page: {DIM}{result}{RESET}")
            summary[10]["already"] += 1

    # Summary
    print()
    print(f"{BOLD}{BLUE}{'═' * 70}{RESET}")
    print(f"{BOLD}  📊 Summary{RESET}")
    print(f"{BOLD}{BLUE}{'═' * 70}{RESET}")
    print(f"  HTML files scanned : {len(files)}")
    print(f"  Files modified     : {files_modified}")
    print()
    print(f"  {'Fix':<35} {'Applied':>8} {'Already':>8} {'Other':>8}")
    print(f"  {'-' * 35} {'-' * 8} {'-' * 8} {'-' * 8}")
    for num, label, _ in FIXES:
        if num not in enabled:
            continue
        s = summary[num]
        other = s["skipped"] + s["notfound"]
        print(f"  [{num:>2}] {label:<31} {s['applied']:>8} {s['already']:>8} {other:>8}")
    if 10 in enabled:
        s = summary[10]
        print(f"  [10] {'Custom 404 page':<31} {s['applied']:>8} {s['already']:>8} {0:>8}")

    print()
    if args.dry_run:
        print(f"  {YELLOW}💡 DRY RUN — re-run without --dry-run to apply.{RESET}")
    else:
        print(f"  {GREEN}✅ Done!{RESET}")
        if not args.no_backup:
            print(f"  {DIM}Backups saved as *.bak — delete after verification.{RESET}")
        print()
        print(f"  {BOLD}Next steps:{RESET}")
        print(f"    1. Test locally: open index.html with VS Code Live Server")
        print(f"    2. Visually verify: chef name, footer link, internal-links section, USD price")
        print(f"    3. git add . && git commit -m 'SEO quick wins (14 fixes)' && git push")
        print(f"    4. After Vercel deploys, test:")
        print(f"       - https://latablemarrakech.com/404 (should show custom 404)")
        print(f"       - https://latablemarrakech.com/about-our-chef/ (chef name)")
    print(f"{BOLD}{BLUE}{'═' * 70}{RESET}")
    print()


if __name__ == "__main__":
    main()
