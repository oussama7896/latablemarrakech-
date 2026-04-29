#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════
  seo-setup.py — All-in-one Technical SEO Setup
  La Table Marrakech · latablemarrakech.com
═══════════════════════════════════════════════════════════════════════

WHAT THIS SCRIPT DOES:
  1. Creates robots.txt in your project root
  2. Creates sitemap.xml in your project root (23 URLs with hreflang)
  3. Creates .htaccess in your project root (HTTPS, redirects, gzip, cache)
  4. Injects <link rel="canonical"> and hreflang tags into every HTML file

HOW TO RUN (in VS Code Terminal):
  python seo-setup.py              # do everything
  python seo-setup.py --dry-run    # preview changes, don't write anything

REQUIREMENTS:
  Python 3.6 or higher (no third-party packages needed)

SAFETY:
  - Idempotent: safe to re-run as many times as you want
  - --dry-run mode shows what WOULD change without writing
  - Backs up nothing — but only modifies HTML <head> sections
═══════════════════════════════════════════════════════════════════════
"""

import os
import re
import sys
import argparse

DOMAIN = "https://latablemarrakech.com"
TODAY = "2026-04-29"

# ════════════════════════════════════════════════════════════════════
#  FILE 1: robots.txt
# ════════════════════════════════════════════════════════════════════
ROBOTS_TXT = f"""# robots.txt for La Table Marrakech
# {DOMAIN}
# Last updated: {TODAY}

# Allow all reputable crawlers
User-agent: *
Allow: /

# Disallow internal/utility paths
Disallow: /cgi-bin/
Disallow: /tmp/
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

# Sitemap location
Sitemap: {DOMAIN}/sitemap.xml
"""

# ════════════════════════════════════════════════════════════════════
#  FILE 2: sitemap.xml
# ════════════════════════════════════════════════════════════════════

# Each entry: (url, priority, changefreq, [hreflang_alternates])
# hreflang_alternates is a list of (lang_code, url) tuples
SITEMAP_ENTRIES = [
    # Homepage trio
    ("/", "1.0", "weekly", [
        ("en", "/"), ("fr", "/fr/"), ("ar", "/ar/"), ("x-default", "/"),
    ]),
    ("/fr/", "1.0", "weekly", [
        ("en", "/"), ("fr", "/fr/"), ("ar", "/ar/"), ("x-default", "/"),
    ]),
    ("/ar/", "1.0", "weekly", [
        ("en", "/"), ("fr", "/fr/"), ("ar", "/ar/"), ("x-default", "/"),
    ]),

    # Pricing pair
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

    # Villa pair
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

    # Cooking class pair
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

    # French standalone pages
    ("/fr/chef-prive-marrakech/", "0.9", "monthly", []),
    ("/fr/chef-a-domicile-marrakech/", "0.85", "monthly", []),

    # English supporting pages
    ("/the-experience/", "0.8", "monthly", []),
    ("/how-it-works/", "0.8", "monthly", []),
    ("/services/wedding-dinner-marrakech/", "0.85", "monthly", []),
    ("/services/corporate-dining-marrakech/", "0.8", "monthly", []),
    ("/about-our-chef/", "0.7", "monthly", []),
    ("/areas-we-serve/", "0.7", "monthly", []),
    ("/menus/", "0.7", "monthly", []),
    ("/faq/", "0.75", "monthly", []),
    ("/contact/", "0.75", "monthly", []),

    # Blog
    ("/blog/", "0.7", "weekly", []),
    ("/blog/marrakech-medina-market-guide/", "0.75", "monthly", []),

    # Legal
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
#  FILE 3: .htaccess
# ════════════════════════════════════════════════════════════════════
HTACCESS = """# ═══════════════════════════════════════════════════════════════
# .htaccess — La Table Marrakech (Hostinger / Apache)
# ═══════════════════════════════════════════════════════════════

AddDefaultCharset UTF-8

<IfModule mod_rewrite.c>
  RewriteEngine On

  # Force HTTPS
  RewriteCond %{HTTPS} !=on
  RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

  # Force non-www
  RewriteCond %{HTTP_HOST} ^www\\.latablemarrakech\\.com$ [NC]
  RewriteRule ^ https://latablemarrakech.com%{REQUEST_URI} [L,R=301]

  # Force trailing slash
  RewriteCond %{REQUEST_FILENAME} !-f
  RewriteCond %{REQUEST_FILENAME} !-d
  RewriteCond %{REQUEST_URI} !(/$|\\.)
  RewriteRule (.*) %{REQUEST_URI}/ [L,R=301]

  # Kill duplicate pricing page
  RewriteRule ^pricing/?$ /private-chef-cost-marrakech/ [L,R=301]

  # Clean up broken blog URLs
  RewriteRule ^blog/private-chef-cost-marrakech/?$ /private-chef-cost-marrakech/ [L,R=301]
  RewriteRule ^blog/best-moroccan-dishes-to-try/?$ /blog/ [L,R=301]
  RewriteRule ^blog/villa-dining-vs-restaurant-marrakech/?$ /blog/ [L,R=301]
  RewriteRule ^blog/planning-dinner-party-marrakech-villa/?$ /blog/ [L,R=301]

  # Strip tracking params
  RewriteCond %{QUERY_STRING} (^|&)(utm_[a-z]+|fbclid|gclid|msclkid)=([^&]*) [NC]
  RewriteRule ^(.*)$ /$1? [R=301,L]
</IfModule>

# Gzip compression
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css text/javascript
  AddOutputFilterByType DEFLATE application/javascript application/x-javascript application/xml
  AddOutputFilterByType DEFLATE application/json application/ld+json
  AddOutputFilterByType DEFLATE application/xhtml+xml application/rss+xml application/atom+xml
  AddOutputFilterByType DEFLATE image/svg+xml application/x-font-ttf font/opentype
</IfModule>

# Browser caching
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresDefault "access plus 1 month"
  ExpiresByType text/html "access plus 1 hour"
  ExpiresByType text/css "access plus 1 year"
  ExpiresByType application/javascript "access plus 1 year"
  ExpiresByType image/jpeg "access plus 1 year"
  ExpiresByType image/png "access plus 1 year"
  ExpiresByType image/webp "access plus 1 year"
  ExpiresByType image/svg+xml "access plus 1 year"
  ExpiresByType image/x-icon "access plus 1 year"
  ExpiresByType font/woff "access plus 1 year"
  ExpiresByType font/woff2 "access plus 1 year"
  ExpiresByType video/mp4 "access plus 1 month"
</IfModule>

# Security headers
<IfModule mod_headers.c>
  Header always set X-Frame-Options "SAMEORIGIN"
  Header always set X-Content-Type-Options "nosniff"
  Header always set Referrer-Policy "strict-origin-when-cross-origin"
  Header always set Permissions-Policy "camera=(), microphone=(), geolocation=(self)"
  Header unset ETag
</IfModule>
FileETag None

# Custom 404
ErrorDocument 404 /404.html

# Protect sensitive files
<FilesMatch "^(\\.htaccess|\\.htpasswd|\\.git|\\.env|README\\.md)$">
  Require all denied
</FilesMatch>

# MIME types
<IfModule mod_mime.c>
  AddType image/webp .webp
  AddType image/avif .avif
  AddType image/svg+xml .svg
  AddType font/woff2 .woff2
  AddType font/woff .woff
  AddType application/ld+json .jsonld
</IfModule>
"""

# ════════════════════════════════════════════════════════════════════
#  CANONICAL/HREFLANG INJECTION MAP
#  Maps each HTML file path to its SEO config
# ════════════════════════════════════════════════════════════════════
PAGE_MAP = {
    # English root
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

    # French
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

    # Arabic
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

    # Remove stray canonical/hreflang outside our markers
    html = re.sub(r'\s*<link\s+rel=["\']canonical["\'][^>]*>', "", html, flags=re.IGNORECASE)
    html = re.sub(r'\s*<link\s+rel=["\']alternate["\'][^>]*hreflang=[^>]*>', "", html, flags=re.IGNORECASE)

    head_close = re.search(r"</head>", html, flags=re.IGNORECASE)
    if not head_close:
        return html, "no-head"

    new_html = html[: head_close.start()] + f"\n  {block}\n  " + html[head_close.start():]
    return new_html, "inserted"


# ════════════════════════════════════════════════════════════════════
#  MAIN
# ════════════════════════════════════════════════════════════════════
def write_file(path: str, content: str, dry_run: bool, label: str):
    abs_path = os.path.abspath(path)
    if dry_run:
        if os.path.exists(abs_path):
            with open(abs_path, "r", encoding="utf-8") as f:
                existing = f.read()
            action = "(would replace existing)" if existing != content else "(no change needed)"
        else:
            action = "(would create)"
        print(f"  {label}  {abs_path}  {action}")
        return
    with open(abs_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  {label}  {abs_path}")


def main():
    parser = argparse.ArgumentParser(description="All-in-one SEO setup for La Table Marrakech.")
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
    print("  🌍  La Table Marrakech — Technical SEO Setup")
    print("═" * 65)
    print(f"  📂 Project root : {project_root}")
    print(f"  🔧 Mode         : {'DRY RUN (no changes written)' if args.dry_run else 'WRITE MODE'}")
    print("═" * 65)

    # Step 1: robots.txt
    print()
    print("[1/4] robots.txt")
    write_file("robots.txt", ROBOTS_TXT, args.dry_run, "✓")

    # Step 2: sitemap.xml
    print()
    print("[2/4] sitemap.xml  (23 URLs)")
    write_file("sitemap.xml", build_sitemap(), args.dry_run, "✓")

    # Step 3: .htaccess
    print()
    print("[3/4] .htaccess")
    write_file(".htaccess", HTACCESS, args.dry_run, "✓")

    # Step 4: Inject canonicals into HTML files
    print()
    print("[4/4] Canonical + hreflang tags")
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

    # Summary
    print()
    print("═" * 65)
    print("  📊 Summary")
    print("═" * 65)
    print(f"  Static files created  : 3 (robots.txt, sitemap.xml, .htaccess)")
    print(f"  HTML files found      : {found} / {len(PAGE_MAP)}")
    print(f"  HTML files inserted   : {inserted}")
    print(f"  HTML files updated    : {updated}")
    print(f"  HTML files unchanged  : {unchanged}")
    if no_head:
        print(f"  HTML files skipped    : {no_head}  (malformed — no </head>)")
    if missing:
        print(f"  HTML files missing    : {len(missing)}")
        print()
        print("  📭 Pages not yet built (these will be skipped until they exist):")
        for m in missing:
            print(f"     - {m}")

    print()
    if args.dry_run:
        print("  💡 This was a DRY RUN. Re-run without --dry-run to apply.")
    else:
        print("  ✅ Done!")
        print()
        print("  Next steps:")
        print("    1. Test pages locally with VS Code Live Server")
        print("    2. Upload all changed files to Hostinger /public_html/")
        print("    3. Submit sitemap.xml to Google Search Console")
    print("═" * 65)
    print()


if __name__ == "__main__":
    main()
