#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════
  quickwins-v2.py — Apply remaining SEO quick wins
  La Table Marrakech · latablemarrakech.com
═══════════════════════════════════════════════════════════════════════

CHANGES FROM v1:
  - Fix 1 (chef name) → REPLACED with full deletion of /about-our-chef/
                        plus scrub of all references to it across the site
  - Fixes 2, 4, 5, 6, 7, 8, 9, 10, 11, 12 → unchanged

WHAT THIS SCRIPT DOES:

  Fix 1:  DELETE /about-our-chef/ folder + scrub all internal links
          (sitemap.xml, nav menus, footer links across all HTML files)
  Fix 2:  Update footer /pricing/ link → /private-chef-cost-marrakech/
  Fix 4:  Update "Last updated: March 2026" → current month
  Fix 5:  Rewrite weak meta descriptions (per-page mapping)
  Fix 6:  Update food image alt tags (with geo + service hooks)
  Fix 7:  Inject "More from La Table Marrakech" internal-links block
  Fix 8:  Add USD reference next to €85 price ("(~$92 USD)")
  Fix 9:  Add BreadcrumbList JSON-LD schema to interior pages
  Fix 10: Create custom 404.html (if missing)
  Fix 11: Update privacy policy to mention GA4 + Google Ads
  Fix 12: Fix Arabic page lang="ar" dir="rtl" attributes

HOW TO RUN (Mac Terminal, from your website folder):
  python3 quickwins-v2.py              # apply all
  python3 quickwins-v2.py --dry-run    # preview, no writes
  python3 quickwins-v2.py --only 1     # only delete /about-our-chef/
  python3 quickwins-v2.py --skip 1     # skip the deletion (just run others)

REQUIREMENTS: Python 3.6+, no third-party packages

SAFETY:
  - Idempotent: safe to re-run, marker-based detection
  - Creates .bak backups of every modified HTML file
  - The deleted /about-our-chef/ folder is moved to ./_deleted-about-our-chef/
    so you can restore it manually if needed
  - --dry-run mode previews everything without writes
═══════════════════════════════════════════════════════════════════════
"""

import os
import re
import sys
import shutil
import argparse
from datetime import datetime
from pathlib import Path

RED = "\033[91m"; YELLOW = "\033[93m"; GREEN = "\033[92m"
BLUE = "\033[94m"; BOLD = "\033[1m"; DIM = "\033[2m"; RESET = "\033[0m"

DOMAIN = "https://latablemarrakech.com"
TODAY_LONG = datetime.now().strftime("%B %Y")

# ════════════════════════════════════════════════════════════════════
#  FIX 1 — Delete /about-our-chef/ folder + scrub all references
# ════════════════════════════════════════════════════════════════════

def fix_1a_delete_folder(root: Path, dry_run: bool):
    """Move /about-our-chef/ to /_deleted-about-our-chef/ (recoverable)."""
    target = root / "about-our-chef"
    backup = root / "_deleted-about-our-chef"

    if not target.exists():
        if backup.exists():
            return "already deleted (backup at /_deleted-about-our-chef/)"
        return "folder not found"

    if dry_run:
        return f"would move {target.name}/ → _deleted-about-our-chef/"

    if backup.exists():
        # Backup already exists — just remove the live folder
        shutil.rmtree(target)
        return "removed (previous backup retained)"

    shutil.move(str(target), str(backup))
    return "moved to _deleted-about-our-chef/ (recoverable)"


# Patterns to scrub (links pointing TO the deleted page, in any form)
ABOUT_PATH_RE = re.compile(
    r'https?://(?:www\.)?latablemarrakech\.com/about-our-chef/?',
    re.IGNORECASE
)
ABOUT_RELATIVE_RE = re.compile(
    r'(?<![\w/])/about-our-chef/?(?!["\'\w])',
    re.IGNORECASE
)


def fix_1b_scrub_html(html, file_rel):
    """Remove <li>...about-our-chef...</li> and similar nav/footer links."""
    if "PERF:CHEF-LINKS-SCRUBBED" in html:
        return html, "already patched"

    original = html
    changes = 0

    # Strategy 1: Remove entire <li> list items containing the link
    # Match <li ...> ... about-our-chef ... </li>
    li_pattern = re.compile(
        r'<li\b[^>]*>[^<]*(?:<[^>]+>[^<]*)*?'
        r'<a\b[^>]*href\s*=\s*["\'][^"\']*about-our-chef[^"\']*["\'][^>]*>'
        r'.*?</a>'
        r'(?:[^<]*<[^>]+>[^<]*)*?</li>',
        re.IGNORECASE | re.DOTALL
    )
    new_html, n = li_pattern.subn('', html)
    changes += n

    # Strategy 2: Standalone <a href="/about-our-chef/">...</a> not inside <li>
    a_pattern = re.compile(
        r'<a\b[^>]*href\s*=\s*["\'][^"\']*about-our-chef[^"\']*["\'][^>]*>'
        r'.*?</a>',
        re.IGNORECASE | re.DOTALL
    )
    new_html, n2 = a_pattern.subn('', new_html)
    changes += n2

    # Strategy 3: Footer "•" or "|" delimited inline links
    # Pattern like " • [About the Chef](/about-our-chef/)"
    new_html = re.sub(
        r'\s*[•·|]\s*(?:<[^>]+>)?\s*\[About[^]]*\]\([^)]*about-our-chef[^)]*\)',
        '',
        new_html,
        flags=re.IGNORECASE
    )

    # Clean up double spaces / orphan separators that may result
    new_html = re.sub(r'\s*•\s*•\s*', ' • ', new_html)
    new_html = re.sub(r'\s*\|\s*\|\s*', ' | ', new_html)
    new_html = re.sub(r'>\s*•\s*<', '><', new_html)

    if changes == 0 and new_html == original:
        return html, "no /about-our-chef/ references"

    # Add marker to <head> so re-runs detect this
    if "</head>" in new_html and "PERF:CHEF-LINKS-SCRUBBED" not in new_html:
        new_html = new_html.replace(
            "</head>",
            "  <!-- PERF:CHEF-LINKS-SCRUBBED -->\n</head>",
            1
        )

    return new_html, f"removed {changes} link element(s)"


def fix_1c_scrub_sitemap(root: Path, dry_run: bool):
    """Remove the <url> block referencing /about-our-chef/ from sitemap.xml."""
    sitemap = root / "sitemap.xml"
    if not sitemap.exists():
        return "no sitemap.xml found"

    content = sitemap.read_text(encoding="utf-8")
    if "about-our-chef" not in content:
        return "no /about-our-chef/ entry in sitemap"

    # Remove entire <url>...</url> block containing about-our-chef
    pattern = re.compile(
        r'\s*<url>\s*<loc>[^<]*about-our-chef[^<]*</loc>.*?</url>',
        re.DOTALL | re.IGNORECASE
    )
    new_content, n = pattern.subn('', content)

    if n == 0:
        return "entry exists but couldn't isolate <url> block"

    if dry_run:
        return f"would remove {n} sitemap entry"

    sitemap.write_text(new_content, encoding="utf-8")
    return f"removed {n} sitemap entry"


# ════════════════════════════════════════════════════════════════════
#  FIX 2 — Footer /pricing/ link
# ════════════════════════════════════════════════════════════════════
def fix_2_footer_pricing(html, file_rel):
    if "PERF:FOOTER-PRICING-FIXED" in html:
        return html, "already patched"

    pattern = re.compile(
        r'href\s*=\s*["\']'
        r'(?:https?://(?:www\.)?latablemarrakech\.com)?/pricing/?["\']',
        re.IGNORECASE
    )

    matches = pattern.findall(html)
    if not matches:
        return html, "no /pricing/ links"

    new_html = pattern.sub('href="/private-chef-cost-marrakech/"', html)
    new_html = new_html.replace(
        "</head>",
        "  <!-- PERF:FOOTER-PRICING-FIXED -->\n</head>",
        1
    )
    return new_html, f"updated {len(matches)} link(s)"


# ════════════════════════════════════════════════════════════════════
#  FIX 4 — Last updated date
# ════════════════════════════════════════════════════════════════════
def fix_4_date(html, file_rel):
    pattern = re.compile(
        r'(Last\s+updated[:\s]+)([A-Z][a-z]+\s+\d{4})',
        re.IGNORECASE
    )
    matches = pattern.findall(html)
    if not matches:
        return html, "no 'Last updated' found"

    if all(m[1].lower() == TODAY_LONG.lower() for m in matches):
        return html, "already current"

    new_html = pattern.sub(rf'\g<1>{TODAY_LONG}', html)
    return new_html, f"updated {len(matches)} date(s)"


# ════════════════════════════════════════════════════════════════════
#  FIX 5 — Meta descriptions (chef-page entry removed since page is gone)
# ════════════════════════════════════════════════════════════════════
META_DESCRIPTIONS = {
    "menus/index.html": "Custom Moroccan menus by your private chef in Marrakech — tagine, pastilla, royal couscous, seafood, vegan & halal options. From €85 per person at your villa.",
    "areas-we-serve/index.html": "Private chef service across Marrakech — Medina, Palmeraie, Hivernage, Gueliz, Amelkis, Agafay Desert, Ourika Valley. Multi-course Moroccan dining from €85 per person.",
    "contact/index.html": "Book a private chef in Marrakech via WhatsApp, email, or contact form. Confirmed within 24 hours. From €85 per person, 72-hour notice required.",
    "services/wedding-dinner-marrakech/index.html": "Private chef for weddings in Marrakech — multi-course Moroccan feasts at your villa or riad with full service and custom menus. From 20 to 200 guests.",
    "services/corporate-dining-marrakech/index.html": "Corporate private dining in Marrakech — private chef for client dinners, retreats, and team events. Bespoke menus and full service from €85 per person.",
    "the-experience/index.html": "Watch what happens behind the scenes — your private chef shopping the Marrakech medina souk, cooking at your villa, and serving a multi-course Moroccan feast.",
    "how-it-works/index.html": "How it works — pick a date, choose a menu, your chef shops the Marrakech souk and cooks at your villa. Full cleanup included. From €85 per person.",
    "faq/index.html": "Private chef in Marrakech — booking, pricing, dietary restrictions, group sizes, cancellation policy. All your questions answered. From €85 per person.",
}


def fix_5_meta_descriptions(html, file_rel):
    if file_rel not in META_DESCRIPTIONS:
        return html, "skipped (not a target page)"

    new_desc = META_DESCRIPTIONS[file_rel]
    pattern = re.compile(
        r'<meta\s+name\s*=\s*["\']description["\']\s+content\s*=\s*["\']([^"\']*)["\']',
        re.IGNORECASE
    )

    match = pattern.search(html)
    if not match:
        return html, "no meta description tag"

    if match.group(1) == new_desc:
        return html, "already correct"

    new_tag = f'<meta name="description" content="{new_desc}"'
    new_html = pattern.sub(new_tag, html, count=1)
    return new_html, "updated"


# ════════════════════════════════════════════════════════════════════
#  FIX 6 — Food image alt tags
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
}


def fix_6_alt_tags(html, file_rel):
    changed = 0

    def process_img(match):
        nonlocal changed
        tag = match.group(0)
        src_match = re.search(r'src\s*=\s*["\']([^"\']+)["\']', tag, re.IGNORECASE)
        if not src_match:
            return tag

        src = src_match.group(1)
        for key, new_alt in ALT_REWRITES.items():
            if key.lower() in src.lower():
                alt_match = re.search(r'alt\s*=\s*["\']([^"\']*)["\']', tag, re.IGNORECASE)
                if alt_match:
                    if alt_match.group(1) == new_alt:
                        return tag
                    new_tag = re.sub(
                        r'alt\s*=\s*["\'][^"\']*["\']',
                        f'alt="{new_alt}"',
                        tag,
                        count=1,
                        flags=re.IGNORECASE
                    )
                    changed += 1
                    return new_tag
                break
        return tag

    img_pattern = re.compile(r'<img\s[^>]*?>', re.IGNORECASE | re.DOTALL)
    new_html = img_pattern.sub(process_img, html)

    if changed == 0:
        return html, "no matching food images"
    return new_html, f"updated {changed} alt tag(s)"


# ════════════════════════════════════════════════════════════════════
#  FIX 7 — Internal-links section (no longer references about-our-chef)
# ════════════════════════════════════════════════════════════════════
INTERNAL_LINKS_BLOCK_EN = '''
<!-- PERF:INTERNAL-LINKS START -->
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
    is_en = file_rel == "index.html"
    is_fr = file_rel == "fr/index.html"
    if not (is_en or is_fr):
        return html, "skipped (not a target homepage)"
    if "PERF:INTERNAL-LINKS START" in html:
        return html, "already patched"

    block = INTERNAL_LINKS_BLOCK_FR if is_fr else INTERNAL_LINKS_BLOCK_EN
    footer_match = re.search(r'<footer\b', html, re.IGNORECASE)
    main_close_match = re.search(r'</main>', html, re.IGNORECASE)

    target_pos = None
    if footer_match:
        target_pos = footer_match.start()
    elif main_close_match:
        target_pos = main_close_match.start()

    if target_pos is None:
        return html, "no <footer> or </main>"

    new_html = html[:target_pos] + block + html[target_pos:]
    return new_html, "injected"


# ════════════════════════════════════════════════════════════════════
#  FIX 8 — USD reference next to €85
# ════════════════════════════════════════════════════════════════════
def fix_8_usd_reference(html, file_rel):
    if "PERF:USD-REF" in html:
        return html, "already patched"

    pattern = re.compile(r'(€\s*85)(?!\s*\(~\$)', re.IGNORECASE)
    matches = pattern.findall(html)
    if not matches:
        return html, "no €85 references"

    new_html = pattern.sub(r'\1 (~$92 USD)', html)
    new_html = new_html.replace(
        "</head>",
        "  <!-- PERF:USD-REF -->\n</head>",
        1
    )
    return new_html, f"updated {len(matches)} reference(s)"


# ════════════════════════════════════════════════════════════════════
#  FIX 9 — BreadcrumbList schema (no chef page entry)
# ════════════════════════════════════════════════════════════════════
BREADCRUMB_MAP = {
    "the-experience/index.html": ("The Experience", "/the-experience/"),
    "how-it-works/index.html": ("How It Works", "/how-it-works/"),
    "private-chef-cost-marrakech/index.html": ("Pricing", "/private-chef-cost-marrakech/"),
    "marrakech-villa-with-private-chef/index.html": ("Villa Dining Guide", "/marrakech-villa-with-private-chef/"),
    "marrakech-cooking-class-vs-private-chef/index.html": ("Cooking Class vs Private Chef", "/marrakech-cooking-class-vs-private-chef/"),
    "services/wedding-dinner-marrakech/index.html": ("Wedding Dinners", "/services/wedding-dinner-marrakech/"),
    "services/corporate-dining-marrakech/index.html": ("Corporate Dining", "/services/corporate-dining-marrakech/"),
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


def build_breadcrumb_jsonld(name, path):
    return f'''<!-- PERF:BREADCRUMB-SCHEMA -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "{DOMAIN}/" }},
    {{ "@type": "ListItem", "position": 2, "name": "{name}", "item": "{DOMAIN}{path}" }}
  ]
}}
</script>'''


def fix_9_breadcrumbs(html, file_rel):
    if file_rel not in BREADCRUMB_MAP:
        return html, "skipped (not a mapped page)"
    if "PERF:BREADCRUMB-SCHEMA" in html:
        return html, "already patched"

    name, path = BREADCRUMB_MAP[file_rel]
    block = build_breadcrumb_jsonld(name, path)

    head_close = re.search(r'</head>', html, re.IGNORECASE)
    if not head_close:
        return html, "</head> not found"

    new_html = html[:head_close.start()] + "  " + block + "\n" + html[head_close.start():]
    return new_html, "injected"


# ════════════════════════════════════════════════════════════════════
#  FIX 10 — Custom 404 page
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
  <!-- PERF:404-CUSTOM -->
</body>
</html>
'''


def fix_10_custom_404(root: Path, dry_run: bool):
    target = root / "404.html"
    if target.exists():
        existing = target.read_text(encoding="utf-8")
        if "PERF:404-CUSTOM" in existing or len(existing) > 500:
            return "already exists"
    if dry_run:
        return "would create 404.html"
    target.write_text(CUSTOM_404, encoding="utf-8")
    return "created 404.html"


# ════════════════════════════════════════════════════════════════════
#  FIX 11 — Privacy policy GA4/Google Ads update
# ════════════════════════════════════════════════════════════════════
def fix_11_privacy(html, file_rel):
    if "PERF:PRIVACY-UPDATED" in html:
        return html, "already patched"

    old_phrase = "We do not use tracking cookies, advertising pixels, or third-party analytics unless you accept cookies"
    new_phrase = ("We use Google Analytics 4 (GA4) and Google Ads conversion tracking to improve our service. "
                  "These cookies only activate after you accept them via our cookie banner. "
                  "Pixel data is processed by Google in line with their privacy practices")

    if old_phrase not in html:
        return html, "old privacy phrase not found"

    new_html = html.replace(old_phrase, new_phrase)
    new_html = new_html.replace(
        "</head>",
        "  <!-- PERF:PRIVACY-UPDATED -->\n</head>",
        1
    )
    return new_html, "updated privacy policy text"


# ════════════════════════════════════════════════════════════════════
#  FIX 12 — Arabic page lang/dir
# ════════════════════════════════════════════════════════════════════
def fix_12_arabic(html, file_rel):
    if not file_rel.startswith("ar/"):
        return html, "skipped (not an Arabic page)"
    if "PERF:AR-ATTRS" in html:
        return html, "already patched"

    pattern = re.compile(r'<html\b[^>]*>', re.IGNORECASE)
    match = pattern.search(html)
    if not match:
        return html, "no <html> tag"

    current = match.group(0)
    if (re.search(r'lang\s*=\s*["\']ar["\']', current, re.IGNORECASE) and
        re.search(r'dir\s*=\s*["\']rtl["\']', current, re.IGNORECASE)):
        return html, "already correct"

    new_html = pattern.sub('<html lang="ar" dir="rtl">', html, count=1)
    new_html = new_html.replace(
        "</head>",
        "  <!-- PERF:AR-ATTRS -->\n</head>",
        1
    )
    return new_html, "fixed lang+dir"


# ════════════════════════════════════════════════════════════════════
#  RUNNER
# ════════════════════════════════════════════════════════════════════
HTML_FIXES = [
    (2, "Footer /pricing/ link", fix_2_footer_pricing),
    (4, "'Last updated' date", fix_4_date),
    (5, "Weak meta descriptions", fix_5_meta_descriptions),
    (6, "Food image alt tags", fix_6_alt_tags),
    (7, "Internal-links section", fix_7_internal_links),
    (8, "USD price reference", fix_8_usd_reference),
    (9, "BreadcrumbList schema", fix_9_breadcrumbs),
    (11, "Privacy policy update", fix_11_privacy),
    (12, "Arabic lang/dir attrs", fix_12_arabic),
]


def find_html_files(root):
    skip_dirs = {".git", "node_modules", ".vercel", ".next", "dist", "build",
                 "_deleted-about-our-chef", "about-our-chef"}
    for path in root.rglob("*.html"):
        if any(p in skip_dirs for p in path.parts):
            continue
        if path.suffix == ".bak" or path.name.endswith(".html.bak"):
            continue
        yield path


def backup_file(path):
    backup = path.with_suffix(path.suffix + ".bak")
    if not backup.exists():
        shutil.copy2(path, backup)


def main():
    ap = argparse.ArgumentParser(description="Apply remaining quick-win fixes (v2: deletes /about-our-chef/).")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--root", default=".")
    ap.add_argument("--skip", nargs="+", type=int, default=[], metavar="N")
    ap.add_argument("--only", nargs="+", type=int, default=[], metavar="N")
    ap.add_argument("--no-backup", action="store_true")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"{RED}❌ Not a directory: {root}{RESET}")
        sys.exit(1)

    all_nums = {1, 10} | {f[0] for f in HTML_FIXES}
    enabled = set(all_nums)
    if args.only:
        enabled = set(args.only) & all_nums
    enabled -= set(args.skip)

    print()
    print(f"{BOLD}{BLUE}{'═' * 70}{RESET}")
    print(f"{BOLD}{BLUE}  ⚡ Quick Wins v2 · La Table Marrakech{RESET}")
    print(f"{BOLD}{BLUE}{'═' * 70}{RESET}")
    print(f"  📂 Root        : {root}")
    print(f"  🔧 Mode        : {'DRY RUN' if args.dry_run else 'WRITE'}")
    print(f"  🩹 Fixes       : {sorted(enabled)}")
    print(f"  📅 Date        : {TODAY_LONG}")
    print(f"{BOLD}{BLUE}{'═' * 70}{RESET}")

    if not enabled:
        print(f"{YELLOW}  No fixes enabled. Exiting.{RESET}")
        return

    # FIX 1 — Delete /about-our-chef/ folder + scrub references
    if 1 in enabled:
        print()
        print(f"{BOLD}  🗑  Fix 1: Delete /about-our-chef/ + scrub references{RESET}")
        result = fix_1a_delete_folder(root, args.dry_run)
        print(f"     [1a] Folder: {GREEN}{result}{RESET}")
        sitemap_result = fix_1c_scrub_sitemap(root, args.dry_run)
        print(f"     [1c] Sitemap: {GREEN}{sitemap_result}{RESET}")

    # FIXES on every HTML file
    files = sorted(find_html_files(root))
    if not files:
        print(f"{RED}  No HTML files found.{RESET}")
        return

    summary = {n: {"applied": 0, "already": 0, "other": 0} for n in all_nums}
    files_modified = 0

    # Add Fix 1b (HTML scrub) to the loop if enabled
    fixes_to_run = []
    if 1 in enabled:
        fixes_to_run.append((1, "Scrub /about-our-chef/ links", fix_1b_scrub_html))
    for num, label, fn in HTML_FIXES:
        if num in enabled:
            fixes_to_run.append((num, label, fn))

    for path in files:
        rel = str(path.relative_to(root)).replace("\\", "/")
        try:
            html = path.read_text(encoding="utf-8")
        except Exception as e:
            print(f"  {RED}⚠  Could not read {rel}: {e}{RESET}")
            continue

        original = html
        actions = []
        for num, label, fn in fixes_to_run:
            html, status = fn(html, rel)
            actions.append((num, label, status))
            sl = status.lower()
            if any(k in sl for k in ["applied", "updated", "injected", "fixed", "removed", "created"]):
                summary[num]["applied"] += 1
            elif "already" in sl:
                summary[num]["already"] += 1
            else:
                summary[num]["other"] += 1

        if html != original:
            files_modified += 1
            print()
            print(f"{BOLD}  📝 {rel}{RESET}")
            for num, label, status in actions:
                sl = status.lower()
                if any(k in sl for k in ["applied", "updated", "injected", "fixed", "removed", "created"]):
                    print(f"     {GREEN}✓{RESET} [{num}] {label}: {status}")
                elif "already" in sl:
                    print(f"     {DIM}·{RESET} [{num}] {label}: {DIM}{status}{RESET}")
                # skip noise for "skipped" and "no X found"

            if not args.dry_run:
                if not args.no_backup:
                    backup_file(path)
                path.write_text(html, encoding="utf-8")

    # FIX 10 — 404 page
    if 10 in enabled:
        result = fix_10_custom_404(root, args.dry_run)
        print()
        print(f"{BOLD}  📝 404.html (root){RESET}")
        if any(k in result.lower() for k in ["created", "would create"]):
            print(f"     {GREEN}✓{RESET} [10] Custom 404 page: {result}")
            summary[10]["applied"] += 1
        else:
            print(f"     {DIM}·{RESET} [10] Custom 404 page: {DIM}{result}{RESET}")
            summary[10]["already"] += 1

    # SUMMARY
    print()
    print(f"{BOLD}{BLUE}{'═' * 70}{RESET}")
    print(f"{BOLD}  📊 Summary{RESET}")
    print(f"{BOLD}{BLUE}{'═' * 70}{RESET}")
    print(f"  HTML files scanned : {len(files)}")
    print(f"  Files modified     : {files_modified}")
    print()
    print(f"  {'Fix':<35} {'Applied':>8} {'Already':>8} {'Other':>8}")
    print(f"  {'-' * 35} {'-' * 8} {'-' * 8} {'-' * 8}")

    fix_labels = {1: "Scrub /about-our-chef/ links", 10: "Custom 404 page"}
    for num, label, _ in HTML_FIXES:
        fix_labels[num] = label

    for num in sorted(enabled):
        s = summary[num]
        label = fix_labels.get(num, f"Fix {num}")
        print(f"  [{num:>2}] {label:<31} {s['applied']:>8} {s['already']:>8} {s['other']:>8}")

    print()
    if args.dry_run:
        print(f"  {YELLOW}💡 DRY RUN — re-run without --dry-run to apply.{RESET}")
    else:
        print(f"  {GREEN}✅ Done!{RESET}")
        if not args.no_backup:
            print(f"  {DIM}HTML backups: *.bak  ·  Folder backup: _deleted-about-our-chef/{RESET}")
        print()
        print(f"  {BOLD}Next steps:{RESET}")
        print(f"    1. Test locally with VS Code Live Server")
        print(f"    2. Verify /about-our-chef/ no longer appears in nav/footer")
        print(f"    3. git add . && git commit -m 'Remove chef page + apply quick wins' && git push")
        print(f"    4. After Vercel deploys (~60s):")
        print(f"       - Test https://latablemarrakech.com/about-our-chef/ → should 404")
        print(f"       - Test https://latablemarrakech.com/404 → should show custom page")
    print(f"{BOLD}{BLUE}{'═' * 70}{RESET}")
    print()


if __name__ == "__main__":
    main()
