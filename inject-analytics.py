#!/usr/bin/env python3
"""
inject-analytics.py — idempotent codemod that ensures every production HTML page
on latablemarrakech.com loads the canonical Consent Mode v2 + lazy-gtag loader.

Why this exists
---------------
Audit (2026-05) found that of 36 production pages:
  * 4 pages had a working gtag loader (/, /fr/, /ar/, /menus/)
  * 17 pages had a BROKEN loader — bitwise `|` instead of logical `||` made
    `requestIdleCallback | function(...)` evaluate to 0, so `rIC()` threw
    "0 is not a function" and the entire loader silently died
  * 15 pages had no loader at all (contact, faq, the-experience, etc.)

This script replaces the loader on every page with one canonical version so
events flow into GA4 consistently. Run it any time the loader changes.

Behaviour
---------
For each .html file under repo root (excluding backups / deleted dirs):
  * Replaces the CONSENT MODE V2 <script> block with the canonical version
  * Replaces the PERF:GTAG-LAZY <script> block with the canonical version
  * If a block is missing, inserts it after the <meta name="viewport"> line

Idempotent: running it twice is a no-op.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

SKIP_PATTERNS = (
    ".bak",
    "backup",
    "_deleted",
    ".impeccable",
    "temporary screenshots",
    "node_modules",
    ".git/",
    "screenshot-helper",
    "social-logo",  # OG-image render template, not a real page
)

# Canonical Consent Mode v2 block — denied by default, restored from localStorage.
# Keep in sync with the cookie banner in PERF:ANALYTICS-RICH on each page.
CONSENT_BLOCK = """  <!-- CONSENT MODE V2 (must load before gtag) -->
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('consent', 'default', {
      'ad_storage': 'denied',
      'ad_user_data': 'denied',
      'ad_personalization': 'denied',
      'analytics_storage': 'denied',
      'wait_for_update': 500
    });
    if (localStorage.getItem('cookie_consent') === 'accepted') {
      gtag('consent', 'update', {
        'ad_storage': 'granted',
        'ad_user_data': 'granted',
        'ad_personalization': 'granted',
        'analytics_storage': 'granted'
      });
    }
  </script>
"""

# Canonical lazy-gtag loader. Loads gtag.js after first user interaction OR a
# 5s timeout, whichever comes first. Configures BOTH GA4 (G-J2QTMMMYLD) and
# Google Ads (AW-18017405402) from one script load.
GTAG_BLOCK = """  <!-- PERF:GTAG-LAZY START — Google Analytics + Google Ads loaded on idle, after user interaction -->
  <script>
    (function() {
      var loaded = false;
      var rIC = window.requestIdleCallback || function(fn) { return setTimeout(fn, 1); };
      function loadGtag() {
        if (loaded) return;
        loaded = true;
        rIC(function() {
          var s1 = document.createElement('script');
          s1.async = true;
          s1.src = 'https://www.googletagmanager.com/gtag/js?id=AW-18017405402';
          document.head.appendChild(s1);
          s1.onload = function() {
            rIC(function() {
              gtag('js', new Date());
              gtag('config', 'G-J2QTMMMYLD');
              gtag('config', 'AW-18017405402', { 'allow_enhanced_conversions': true });
            });
          };
        });
      }
      ['scroll', 'mousemove', 'touchstart', 'keydown', 'click'].forEach(function(evt) {
        window.addEventListener(evt, loadGtag, { passive: true, once: true });
      });
      setTimeout(loadGtag, 5000);
    })();
  </script>
  <!-- PERF:GTAG-LAZY END -->
"""

# Regex to match an existing CONSENT block (with or without surrounding whitespace).
# We match the comment marker through the closing </script> + trailing newline.
CONSENT_RE = re.compile(
    r"[ \t]*<!--\s*CONSENT MODE V2.*?</script>\s*\n",
    re.DOTALL,
)

# Match an existing PERF:GTAG-LAZY block start..end (inclusive of END marker).
GTAG_RE = re.compile(
    r"[ \t]*<!--\s*PERF:GTAG-LAZY START.*?<!--\s*PERF:GTAG-LAZY END\s*-->\s*\n",
    re.DOTALL,
)

# Where to inject when the page has no loader at all — right after the viewport
# meta tag is a safe, conventional spot in <head>.
VIEWPORT_RE = re.compile(
    r'(<meta\s+name=["\']viewport["\'][^>]*>\s*\n)',
    re.IGNORECASE,
)


def should_skip(path: Path) -> bool:
    s = str(path)
    return any(p in s for p in SKIP_PATTERNS)


def transform(html: str) -> str:
    """Apply both substitutions. Returns the new HTML (may be unchanged)."""
    # Step 1: drop any existing CONSENT/GTAG blocks. We then re-insert the
    # canonical pair together so they are always adjacent in <head>.
    had_consent = bool(CONSENT_RE.search(html))
    had_gtag = bool(GTAG_RE.search(html))
    html = CONSENT_RE.sub("", html, count=1)
    html = GTAG_RE.sub("", html, count=1)

    canonical = "\n" + CONSENT_BLOCK + "\n" + GTAG_BLOCK

    if had_consent or had_gtag:
        # Re-insert in the same neighbourhood by anchoring to viewport meta.
        m = VIEWPORT_RE.search(html)
        if not m:
            # Fall back to inserting after <head>.
            html = re.sub(r"(<head[^>]*>\s*\n)", r"\1" + canonical, html, count=1)
        else:
            html = html[: m.end()] + canonical + html[m.end() :]
    else:
        # No prior loader anywhere — insert after viewport.
        m = VIEWPORT_RE.search(html)
        if not m:
            return html  # No viewport tag — likely not a real page; leave it.
        html = html[: m.end()] + canonical + html[m.end() :]

    return html


def main() -> int:
    changed = []
    skipped = []
    for path in sorted(ROOT.rglob("*.html")):
        if should_skip(path):
            skipped.append(path)
            continue
        original = path.read_text(encoding="utf-8")
        # Quick filter: must have a <head> and a <meta viewport> to be a real page.
        if "<head" not in original or "viewport" not in original:
            skipped.append(path)
            continue
        new = transform(original)
        if new != original:
            path.write_text(new, encoding="utf-8")
            changed.append(path)

    print(f"Changed: {len(changed)} files")
    for p in changed:
        print(f"  ~ {p.relative_to(ROOT)}")
    print(f"Skipped: {len(skipped)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
