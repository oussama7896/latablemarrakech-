#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════
  seo-setup.py — All-in-one Technical SEO Setup (VERCEL EDITION)
  La Table Marrakech · latablemarrakech.com
═══════════════════════════════════════════════════════════════════════

WHAT THIS SCRIPT DOES:
  1. Creates robots.txt in your project root
  2. Creates sitemap.xml in your project root (23 URLs with hreflang)
  3. Creates vercel.json in your project root (redirects, headers, caching)
  4. Removes any stale .htaccess (useless on Vercel)
  5. Injects <link rel="canonical"> + hreflang into every HTML file

HOW TO RUN (in VS Code Terminal):
  python3 seo-setup.py              # do everything
  python3 seo-setup.py --dry-run    # preview changes, don't write anything

REQUIREMENTS:
  Python 3.6+ (no third-party packages needed)

SAFETY:
  - Idempotent: safe to re-run as many times as you want
  - --dry-run mode shows what WOULD change without writing
  - Only modifies HTML <head> sections
═══════════════════════════════════════════════════════════════════════
"""

import os
import re
import sys
import json
import argparse

DOMAIN = "https://latablemarrakech.com"
TODAY = "2026-04-29"

# ════════════════════════════════════════════════════════════════════
#  FILE 1: robots.txt
# ════════════════════════════════════════════════════════════════════
ROBOTS_TXT = f"""# robots.txt for La Table Marrakech
# {DOMAIN}
# Last updated: {TODAY}

User-agent: *
Allow: /

Disallow: /api/
Disallow: /_next/
Disallow: /*.json$
Disallow: /*?*utm_
Disallow: /*?*fbclid
Disallow: /*?*gclid

# Block AI scrapers that don't drive traffic
User-agent: GPTBot
Disallow: /

User-agent: CCBot
Disallow: /

# Allow AI crawlers that drive citations
User-agent: anthropic-ai
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: PerplexityBot
Allow: /

Sitemap: {DOMAIN}/sitemap.xml
"""

# ════════════════════════════════════════════════════════════════════
#  FILE 2: sitemap.xml
# ════════════════════════════════════════════════════════════════════
SITEMAP_ENTRIES = [
    ("/", "1.0", "weekly", [("en", "/"), ("fr", "/fr/"), ("ar", "/ar/"), ("x-default", "/")]),
    ("/fr/", "1.0", "weekly", [("en", "/"), ("fr", "/fr/"), ("ar", "/ar/"), ("x-default", "/")]),
    ("/ar/", "1.0", "weekly", [("en", "/"), ("fr", "/fr/"), ("ar", "/ar/"), ("x-default", "/")]),
    ("/private-chef-cost-marrakech/", "0.95", "monthly", [
        ("en", "/private-chef-cost-marrakech/"),
        ("fr", "/fr/chef-prive-prix-marrakech/"),
        ("x-default", "/private-chef-cost-marrakech/"),
    ]),
    ("/fr/chef-prive-prix-marrakech/", "0.95", "monthly", [
        ("en", "/private-chef-cost-marrakech/"),
        ("fr", "/fr/chef-prive-prix-marrakech/"),
        ("x-default", "/private-chef-cost-marrakech/"),
    ]),
    ("/marrakech-villa-with-private-chef/", "0.9", "monthly", [
        ("en", "/marrakech-villa-with-private-chef/"),
        ("fr", "/fr/villa-marrakech-chef-prive/"),
        ("x-default", "/marrakech-villa-with-private-chef/"),
    ]),
    ("/fr/villa-marrakech-chef-prive/", "0.9", "monthly", [
        ("en", "/marrakech-villa-with-private-chef/"),
        ("fr", "/fr/villa-marrakech-chef-prive/"),
        ("x-default", "/marrakech-villa-with-private-chef/"),
    ]),
    ("/marrakech-cooking-class-vs-private-chef/", "0.85", "monthly", [
        ("en", "/marrakech-cooking-class-vs-private-chef/"),
        ("fr", "/fr/cours-de-cuisine-marrakech/"),
        ("x-default", "/marrakech-cooking-class-vs-private-chef/"),
    ]),
    ("/fr/cours-de-cuisine-marrakech/", "0.85", "monthly", [
        ("en", "/marrakech-cooking-class-vs-private-chef/"),
        ("fr", "/fr/cours-de-cuisine-marrakech/"),
        ("x-default", "/marrakech-cooking-class-vs-private-chef/"),
    ]),
    ("/fr/chef-prive-marrakech/", "0.9", "monthly", []),
    ("/fr/chef-a-domicile-marrakech/", "0.85", "monthly", []),
    ("/the-experience/", "0.8", "monthly", []),
    ("/how-it-works/", "0.8", "monthly", []),
    ("/services/wedding-dinner-marrakech/", "0.85", "monthly", []),
    ("/services/corporate-dining-marrakech/", "0.8", "monthly", []),
    ("/about-our-chef/", "0.7", "monthly", []),
    ("/areas-we-serve/", "0.7", "monthly", []),
    ("/menus/", "0.7", "monthly", []),
    ("/faq/", "0.75", "monthly", []),
    ("/contact/", "0.75", "monthly", []),
    ("/blog/", "0.7", "weekly", []),
    ("/blog/marrakech-medina-market-guide/", "0.75", "monthly", []),
    ("/privacy/", "0.3", "yearly", []),
]


def build_sitemap() -> str:
    parts = ['<?xml version="1.0" encoding="UTF-8"?>']
    parts.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"')
    parts.append('        xmlns:xhtml="http://www.w3.org/1999/xhtml">')
    parts.append("")
    for path, priority, changefreq, alternates in SITEMAP_ENTRIES:
        parts.append("  <url>")
        parts.append(f"    <loc>{DOMAIN}{path}</loc>")
        parts.append(f"    <lastmod>{TODAY}</lastmod>")
        parts.append(f"    <changefreq>{changefreq}</changefreq>")
        parts.append(f"    <priority>{priority}</priority>")
        for lang, alt_path in alternates:
            parts.append(f'    <xhtml:link rel="alternate" hreflang="{lang}" href="{DOMAIN}{alt_path}"/>')
        parts.append("  </url>")
    parts.append("</urlset>")
    return "\n".join(parts) + "\n"


# ════════════════════════════════════════════════════════════════════
#  FILE 3: vercel.json — Vercel's equivalent of .htaccess
#  Handles redirects, security headers, caching
#  (Vercel handles HTTPS + non-www automatically via the dashboard)
# ════════════════════════════════════════════════════════════════════
VERCEL_CONFIG = {
    "trailingSlash": True,
    "cleanUrls": True,
    "redirects": [
        # Kill duplicate pricing page
        {
            "source": "/pricing",
            "destination": "/private-chef-cost-marrakech",
            "permanent": True,
        },
        # Clean up broken blog URLs
        {
            "source": "/blog/private-chef-cost-marrakech",
            "destination": "/private-chef-cost-marrakech",
            "permanent": True,
        },
        {
            "source": "/blog/best-moroccan-dishes-to-try",
            "destination": "/blog",
            "permanent": True,
        },
        {
            "source": "/blog/villa-dining-vs-restaurant-marrakech",
            "destination": "/blog",
            "permanent": True,
        },
        {
            "source": "/blog/planning-dinner-party-marrakech-villa",
            "destination": "/blog",
            "permanent": True,
        },
    ],
    "headers": [
        # Security headers on every page
        {
            "source": "/(.*)",
            "headers": [
                {"key": "X-Frame-Options", "value": "SAMEORIGIN"},
                {"key": "X-Content-Type-Options", "value": "nosniff"},
                {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
                {"key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=(self), interest-cohort=()"},
            ],
        },
        # Long cache for images and fonts (1 year, immutable)
        {
            "source": "/(.*)\\.(jpg|jpeg|png|webp|avif|svg|ico|woff|woff2|ttf)",
            "headers": [
                {"key": "Cache-Control", "value": "public, max-age=31536000, immutable"},
            ],
        },
        # Long cache for CSS/JS
        {
            "source": "/(.*)\\.(css|js)",
            "headers": [
                {"key": "Cache-Control", "value": "public, max-age=31536000, immutable"},
            ],
        },
        # Short cache for HTML (so updates appear quickly)
        {
            "source": "/(.*)",
            "headers": [
                {"key": "Cache-Control", "value": "public, max-age=0, must-revalidate"},
            ],
        },
    ],
}


def build_vercel_json() -> str:
    return json.dumps(VERCEL_CONFIG, indent=2) + "\n"


# ════════════════════════════════════════════════════════════════════
#  CANONICAL/HREFLANG INJECTION MAP
# ════════════════════════════════════════════════════════════════════
PAGE_MAP = {
    "index.html": {
        "canonical": f"{DOMAIN}/",
        "hreflang": {"en": f"{DOMAIN}/", "fr": f"{DOMAIN}/fr/", "ar": f"{DOMAIN}/ar/", "x-default": f"{DOMAIN}/"},
    },
    "the-experience/index.html": {"canonical": f"{DOMAIN}/the-experience/"},
    "how-it-works/index.html": {"canonical": f"{DOMAIN}/how-it-works/"},
    "private-chef-cost-marrakech/index.html": {
        "canonical": f"{DOMAIN}/private-chef-cost-marrakech/",
        "hreflang": {
            "en": f"{DOMAIN}/private-chef-cost-marrakech/",
            "fr": f"{DOMAIN}/fr/chef-prive-prix-marrakech/",
            "x-default": f"{DOMAIN}/private-chef-cost-marrakech/",
        },
    },
    "marrakech-villa-with-private-chef/index.html": {
        "canonical": f"{DOMAIN}/marrakech-villa-with-private-chef/",
        "hreflang": {
            "en": f"{DOMAIN}/marrakech-villa-with-private-chef/",
            "fr": f"{DOMAIN}/fr/villa-marrakech-chef-prive/",
            "x-default": f"{DOMAIN}/marrakech-villa-with-private-chef/",
        },
    },
    "marrakech-cooking-class-vs-private-chef/index.html": {
        "canonical": f"{DOMAIN}/marrakech-cooking-class-vs-private-chef/",
        "hreflang": {
            "en": f"{DOMAIN}/marrakech-cooking-class-vs-private-chef/",
            "fr": f"{DOMAIN}/fr/cours-de-cuisine-marrakech/",
            "x-default": f"{DOMAIN}/marrakech-cooking-class-vs-private-chef/",
        },
    },
    "services/wedding-dinner-marrakech/index.html": {"canonical": f"{DOMAIN}/services/wedding-dinner-marrakech/"},
    "services/corporate-dining-marrakech/index.html": {"canonical": f"{DOMAIN}/services/corporate-dining-marrakech/"},
    "about-our-chef/index.html": {"canonical": f"{DOMAIN}/about-our-chef/"},
    "areas-we-serve/index.html": {"canonical": f"{DOMAIN}/areas-we-serve/"},
    "menus/index.html": {"canonical": f"{DOMAIN}/menus/"},
    "faq/index.html": {"canonical": f"{DOMAIN}/faq/"},
    "contact/index.html": {"canonical": f"{DOMAIN}/contact/"},
    "blog/index.html": {"canonical": f"{DOMAIN}/blog/"},
    "blog/marrakech-medina-market-guide/index.html": {"canonical": f"{DOMAIN}/blog/marrakech-medina-market-guide/"},
    "privacy/index.html": {"canonical": f"{DOMAIN}/privacy/"},
    "fr/index.html": {
        "canonical": f"{DOMAIN}/fr/",
        "hreflang": {"en": f"{DOMAIN}/", "fr": f"{DOMAIN}/fr/", "ar": f"{DOMAIN}/ar/", "x-default": f"{DOMAIN}/"},
    },
    "fr/chef-prive-marrakech/index.html": {
        "canonical": f"{DOMAIN}/fr/chef-prive-marrakech/",
        "hreflang": {"fr": f"{DOMAIN}/fr/chef-prive-marrakech/", "en": f"{DOMAIN}/", "x-default": f"{DOMAIN}/"},
    },
    "fr/chef-prive-prix-marrakech/index.html": {
        "canonical": f"{DOMAIN}/fr/chef-prive-prix-marrakech/",
        "hreflang": {
            "en": f"{DOMAIN}/private-chef-cost-marrakech/",
            "fr": f"{DOMAIN}/fr/chef-prive-prix-marrakech/",
            "x-default": f"{DOMAIN}/private-chef-cost-marrakech/",
        },
    },
    "fr/chef-a-domicile-marrakech/index.html": {
        "canonical": f"{DOMAIN}/fr/chef-a-domicile-marrakech/",
        "hreflang": {"fr": f"{DOMAIN}/fr/chef-a-domicile-marrakech/"},
    },
    "fr/villa-marrakech-chef-prive/index.html": {
        "canonical": f"{DOMAIN}/fr/villa-marrakech-chef-prive/",
        "hreflang": {
            "en": f"{DOMAIN}/marrakech-villa-with-private-chef/",
            "fr": f"{DOMAIN}/fr/villa-marrakech-chef-prive/",
            "x-default": f"{DOMAIN}/marrakech-villa-with-private-chef/",
        },
    },
    "fr/cours-de-cuisine-marrakech/index.html": {
        "canonical": f"{DOMAIN}/fr/cours-de-cuisine-marrakech/",
        "hreflang": {
            "en": f"{DOMAIN}/marrakech-cooking-class-vs-private-chef/",
            "fr": f"{DOMAIN}/fr/cours-de-cuisine-marrakech/",
            "x-default": f"{DOMAIN}/marrakech-cooking-class-vs-private-chef/",
        },
    },
    "ar/index.html": {
        "canonical": f"{DOMAIN}/ar/",
        "hreflang": {"en": f"{DOMAIN}/", "fr": f"{DOMAIN}/fr/", "ar": f"{DOMAIN}/ar/", "x-default": f"{DOMAIN}/"},
    },
}

MARKER_START = "<!-- SEO:CANONICAL-BLOCK START -->"
MARKER_END = "<!-- SEO:CANONICAL-BLOCK END -->"


def build_canonical_block(config: dict) -> str:
    lines = [MARKER_START, f'<link rel="canonical" href="{config["canonical"]}">']
    hreflang = config.get("hreflang", {})
    keys = sorted([k for k in hreflang.keys() if k != "x-default"])
    if "x-default" in hreflang:
        keys.append("x-default")
    for lang in keys:
        lines.append(f'<link rel="alternate" hreflang="{lang}" href="{hreflang[lang]}">')
    lines.append(MARKER_END)
    return "\n  ".join(lines)


def inject_into_html(html: str, block: str):
    pattern = re.compile(re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END), re.DOTALL)
    if pattern.search(html):
        return pattern.sub(block, html), "updated"
    html = re.sub(r'\s*<link\s+rel=["\']canonical["\'][^>]*>', "", html, flags=re.IGNORECASE)
    html = re.sub(r'\s*<link\s+rel=["\']alternate["\'][^>]*hreflang=[^>]*>', "", html, flags=re.IGNORECASE)
    head_close = re.search(r"</head>", html, flags=re.IGNORECASE)
    if not head_close:
        return html, "no-head"
    new_html = html[: head_close.start()] + f"\n  {block}\n  " + html[head_close.start():]
    return new_html, "inserted"


def write_file(path: str, content: str, dry_run: bool, label: str):
    abs_path = os.path.abspath(path)
    if dry_run:
        action = "(would create)" if not os.path.exists(abs_path) else "(would overwrite)"
        print(f"  {label}  {abs_path}  {action}")
        return
    with open(abs_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  {label}  {abs_path}")


def remove_file_if_exists(path: str, dry_run: bool, reason: str):
    if not os.path.exists(path):
        return False
    if dry_run:
        print(f"  🗑  {path}  (would remove — {reason})")
        return True
    os.remove(path)
    print(f"  🗑  {path}  (removed — {reason})")
    return True


def main():
    parser = argparse.ArgumentParser(description="All-in-one SEO setup for La Table Marrakech (Vercel).")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    parser.add_argument("--root", default=".", help="Project root (default: current directory)")
    args = parser.parse_args()

    project_root = os.path.abspath(args.root)
    if not os.path.isdir(project_root):
        print(f"❌ Not a directory: {project_root}")
        sys.exit(1)

    os.chdir(project_root)

    print()
    print("═" * 65)
    print("  🌍  La Table Marrakech — Technical SEO Setup (VERCEL)")
    print("═" * 65)
    print(f"  📂 Project root : {project_root}")
    print(f"  🔧 Mode         : {'DRY RUN (no changes)' if args.dry_run else 'WRITE MODE'}")
    print("═" * 65)

    print()
    print("[1/5] robots.txt")
    write_file("robots.txt", ROBOTS_TXT, args.dry_run, "✓")

    print()
    print("[2/5] sitemap.xml  (23 URLs)")
    write_file("sitemap.xml", build_sitemap(), args.dry_run, "✓")

    print()
    print("[3/5] vercel.json  (redirects, headers, caching)")
    write_file("vercel.json", build_vercel_json(), args.dry_run, "✓")

    print()
    print("[4/5] Cleanup stale Apache config")
    removed = remove_file_if_exists(".htaccess", args.dry_run, "useless on Vercel")
    if not removed:
        print("  ✓  no .htaccess to remove")

    print()
    print("[5/5] Canonical + hreflang tags")
    found = inserted = updated = unchanged = no_head = 0
    missing = []

    for rel_path, config in PAGE_MAP.items():
        abs_path = os.path.join(project_root, rel_path)
        if not os.path.isfile(abs_path):
            missing.append(rel_path)
            continue
        found += 1
        with open(abs_path, "r", encoding="utf-8") as f:
            html = f.read()
        block = build_canonical_block(config)
        new_html, action = inject_into_html(html, block)

        if action == "no-head":
            print(f"  ⚠  {rel_path}  (no </head> tag — skipped)")
            no_head += 1
            continue
        if new_html == html:
            print(f"  ✓  {rel_path}  (already correct)")
            unchanged += 1
            continue
        if not args.dry_run:
            with open(abs_path, "w", encoding="utf-8") as f:
                f.write(new_html)
        if action == "updated":
            print(f"  🔄 {rel_path}  (updated)")
            updated += 1
        else:
            print(f"  ➕ {rel_path}  (injected)")
            inserted += 1

    print()
    print("═" * 65)
    print("  📊 Summary")
    print("═" * 65)
    print(f"  Static files          : robots.txt, sitemap.xml, vercel.json")
    print(f"  HTML files found      : {found} / {len(PAGE_MAP)}")
    print(f"  HTML files inserted   : {inserted}")
    print(f"  HTML files updated    : {updated}")
    print(f"  HTML files unchanged  : {unchanged}")
    if no_head:
        print(f"  HTML files skipped    : {no_head}  (no </head>)")
    if missing:
        print(f"  HTML files missing    : {len(missing)}")
        print()
        print("  📭 Pages not yet built (script will pick them up later):")
        for m in missing[:10]:
            print(f"     - {m}")
        if len(missing) > 10:
            print(f"     ... and {len(missing) - 10} more")

    print()
    if args.dry_run:
        print("  💡 DRY RUN — re-run without --dry-run to apply.")
    else:
        print("  ✅ Done!")
        print()
        print("  Next steps:")
        print("    1. Test pages locally with VS Code Live Server")
        print("    2. Commit & push:    git add . && git commit -m 'Add SEO config' && git push")
        print("       (Vercel will auto-deploy)")
        print("    3. Or deploy with:   vercel --prod")
        print("    4. Verify live:      https://latablemarrakech.com/sitemap.xml")
        print("    5. Submit sitemap to Google Search Console")
    print("═" * 65)
    print()


if __name__ == "__main__":
    main()
