#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════
  perf-fix.py — Apply all performance patches in one go
  La Table Marrakech · latablemarrakech.com  ·  v2
═══════════════════════════════════════════════════════════════════════

WHAT THIS SCRIPT DOES (across index.html and all 22 sub-pages):

  Patch 1: Replace autoplay <video> with static poster <img> on hero
  Patch 2: Lazy-load Google Analytics + Google Ads on user interaction
  Patch 3: Fix duplicate CSS preload pattern (preload-then-promote)
  Patch 4: Add fetchpriority="high" + type="image/webp" to hero preload
  Patch 5: Inject desktop-only video lazy-loader before </body>
  Patch 6: Add loading="lazy" + decoding="async" to all non-hero images

CHANGELOG (v2):
  - Patch 1: matches <video> regardless of attribute order
  - Patch 2: anchors on scripts directly; no comment dependency
  - Patch 3: flexible attribute order on both link tags
  - Patch 4: handles either as=image / href= ordering
═══════════════════════════════════════════════════════════════════════
"""

import os
import re
import sys
import shutil
import argparse
from pathlib import Path

RED = "\033[91m"; YELLOW = "\033[93m"; GREEN = "\033[92m"
BLUE = "\033[94m"; BOLD = "\033[1m"; DIM = "\033[2m"; RESET = "\033[0m"

DOMAIN = "https://latablemarrakech.com"

# ════════════════════════════════════════════════════════════════════
HERO_VIDEO_PATTERN = re.compile(
    r'<video\b[^>]*?\bclass\s*=\s*["\'][^"\']*\bhero-video\b[^"\']*["\'][^>]*>'
    r'.*?</video>',
    re.DOTALL | re.IGNORECASE
)

HERO_IMG_REPLACEMENT = '''<!-- PERF:HERO-IMG START — replaces autoplay video on mobile -->
    <img class="hero-video" id="heroPoster"
         src="/private-chef-marrakech-tagine.webp"
         alt="Private chef in Marrakech serving a multi-course Moroccan tagine dinner at a villa terrace"
         width="1920" height="1080"
         fetchpriority="high"
         decoding="async">
    <!-- PERF:HERO-IMG END -->'''


def patch_1_hero_video(html, file_rel):
    is_homepage = file_rel in ("index.html", "fr/index.html", "ar/index.html")
    if not is_homepage:
        return html, "skipped (not a homepage)"
    if "PERF:HERO-IMG START" in html:
        return html, "already patched"
    match = HERO_VIDEO_PATTERN.search(html)
    if not match:
        return html, 'no <video class="hero-video"> found'
    return html[:match.start()] + HERO_IMG_REPLACEMENT + html[match.end():], "applied"


# ════════════════════════════════════════════════════════════════════
GTAG_EXTERNAL_RE = re.compile(
    r'<script\b[^>]*?\bsrc\s*=\s*["\']https://www\.googletagmanager\.com/gtag/js[^"\']*["\'][^>]*></script>',
    re.IGNORECASE
)


def find_gtag_block(html):
    ext_match = GTAG_EXTERNAL_RE.search(html)
    if not ext_match:
        return None
    after = html[ext_match.end():ext_match.end() + 500]
    inline_re = re.compile(r'^\s*<script\b[^>]*>(.*?)</script>', re.DOTALL | re.IGNORECASE)
    inline_match = inline_re.match(after)
    if not inline_match or 'gtag' not in inline_match.group(1):
        return None
    inline_end = ext_match.end() + inline_match.end()
    start = ext_match.start()
    while True:
        prefix = html[max(0, start - 300):start]
        m = re.search(r'((?:[\t ]*<!--[^>]*?-->[\t ]*\n?)+)\s*$', prefix, re.DOTALL)
        if not m:
            break
        consumed = len(m.group(1))
        if consumed == 0:
            break
        start -= consumed
    return (start, inline_end)


GTAG_NEW_BLOCK = '''<!-- PERF:GTAG-LAZY START — Google Analytics + Google Ads loaded on user interaction -->
  <script>
    (function() {
      var loaded = false;
      function loadGtag() {
        if (loaded) return;
        loaded = true;
        var s1 = document.createElement('script');
        s1.async = true;
        s1.src = 'https://www.googletagmanager.com/gtag/js?id=AW-18017405402';
        document.head.appendChild(s1);
        s1.onload = function() {
          gtag('js', new Date());
          gtag('config', 'G-J2QTMMMYLD');
          gtag('config', 'AW-18017405402', { 'allow_enhanced_conversions': true });
        };
      }
      ['scroll', 'mousemove', 'touchstart', 'keydown', 'click'].forEach(function(evt) {
        window.addEventListener(evt, loadGtag, { passive: true, once: true });
      });
      setTimeout(loadGtag, 3000);
    })();
  </script>
  <!-- PERF:GTAG-LAZY END -->'''


def patch_2_lazy_gtag(html, file_rel):
    if "PERF:GTAG-LAZY START" in html:
        return html, "already patched"
    bounds = find_gtag_block(html)
    if not bounds:
        return html, "gtag block not found (file likely has no gtag, which is fine)"
    start, end = bounds
    return html[:start] + GTAG_NEW_BLOCK + html[end:], "applied"


# ════════════════════════════════════════════════════════════════════
CSS_PRELOAD_TAG = re.compile(
    r'<link\b[^>]*?\brel\s*=\s*["\']preload["\'][^>]*?\bas\s*=\s*["\']style["\'][^>]*?'
    r'\bhref\s*=\s*["\'](https://fonts\.googleapis\.com/css2\?[^"\']+)["\'][^>]*?>',
    re.IGNORECASE
)


def patch_3_css_preload(html, file_rel):
    if "PERF:CSS-PRELOAD" in html:
        return html, "already patched"
    preload_match = CSS_PRELOAD_TAG.search(html)
    if not preload_match:
        return html, "CSS preload tag not found"
    fonts_url = preload_match.group(1)
    fonts_url_escaped = re.escape(fonts_url)
    stylesheet_re = re.compile(
        r'<link\b[^>]*?\bhref\s*=\s*["\']' + fonts_url_escaped + r'["\'][^>]*?'
        r'\bmedia\s*=\s*["\']print["\'][^>]*?'
        r'\bonload\s*=\s*["\'][^"\']*?["\'][^>]*?>',
        re.IGNORECASE
    )
    stylesheet_match = stylesheet_re.search(html)
    if not stylesheet_match:
        return html, "CSS stylesheet tag (media=print + onload) not found"
    if abs(stylesheet_match.start() - preload_match.end()) > 500:
        return html, "preload and stylesheet tags too far apart (skipping for safety)"
    start = min(preload_match.start(), stylesheet_match.start())
    end = max(preload_match.end(), stylesheet_match.end())
    replacement = (
        '<!-- PERF:CSS-PRELOAD START — single async stylesheet load -->\n'
        f'  <link rel="preload" as="style" href="{fonts_url}" '
        f'onload="this.onload=null;this.rel=\'stylesheet\'">\n'
        f'  <noscript><link rel="stylesheet" href="{fonts_url}"></noscript>\n'
        '  <!-- PERF:CSS-PRELOAD END -->'
    )
    return html[:start] + replacement + html[end:], "applied"


# ════════════════════════════════════════════════════════════════════
HERO_PRELOAD_OLD = re.compile(
    r'<link\b[^>]*?\brel\s*=\s*["\']preload["\'][^>]*?'
    r'\bhref\s*=\s*["\']/?private-chef-marrakech-tagine\.webp["\'][^>]*?'
    r'\bas\s*=\s*["\']image["\'][^>]*?>',
    re.IGNORECASE
)
HERO_PRELOAD_OLD_ALT = re.compile(
    r'<link\b[^>]*?\brel\s*=\s*["\']preload["\'][^>]*?'
    r'\bas\s*=\s*["\']image["\'][^>]*?'
    r'\bhref\s*=\s*["\']/?private-chef-marrakech-tagine\.webp["\'][^>]*?>',
    re.IGNORECASE
)
HERO_PRELOAD_NEW = (
    '<!-- PERF:HERO-PRELOAD --><link rel="preload" as="image" '
    'href="/private-chef-marrakech-tagine.webp" '
    'fetchpriority="high" type="image/webp">'
)


def patch_4_hero_preload(html, file_rel):
    if "PERF:HERO-PRELOAD" in html:
        return html, "already patched"
    match = HERO_PRELOAD_OLD.search(html) or HERO_PRELOAD_OLD_ALT.search(html)
    if not match:
        return html, "hero preload tag not found"
    return html[:match.start()] + HERO_PRELOAD_NEW + html[match.end():], "applied"


# ════════════════════════════════════════════════════════════════════
DESKTOP_VIDEO_LOADER = '''
<!-- PERF:VIDEO-LAZY START — desktop-only hero video, loads after page is interactive -->
<script>
(function() {
  if (window.innerWidth < 1024) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  if (navigator.connection && (navigator.connection.saveData ||
      ['slow-2g', '2g', '3g'].includes(navigator.connection.effectiveType))) return;
  function loadHeroVideo() {
    var poster = document.getElementById('heroPoster');
    if (!poster) return;
    var video = document.createElement('video');
    video.className = 'hero-video';
    video.autoplay = true; video.muted = true; video.loop = true;
    video.playsInline = true; video.preload = 'auto';
    video.setAttribute('aria-label', 'Chef preparing Moroccan dishes in a Marrakech villa kitchen');
    var source = document.createElement('source');
    source.src = '/hero-video.mp4'; source.type = 'video/mp4';
    video.appendChild(source);
    video.style.opacity = '0';
    video.style.transition = 'opacity 0.6s';
    video.addEventListener('canplay', function() {
      poster.parentNode.insertBefore(video, poster);
      requestAnimationFrame(function() {
        video.style.opacity = '1';
        setTimeout(function() {
          if (poster.parentNode) poster.parentNode.removeChild(poster);
        }, 700);
      });
    }, { once: true });
  }
  if (document.readyState === 'complete') {
    setTimeout(loadHeroVideo, 1000);
  } else {
    window.addEventListener('load', function() { setTimeout(loadHeroVideo, 1000); });
  }
})();
</script>
<!-- PERF:VIDEO-LAZY END -->
'''


def patch_5_video_lazy(html, file_rel):
    is_homepage = file_rel in ("index.html", "fr/index.html", "ar/index.html")
    if not is_homepage:
        return html, "skipped (not a homepage)"
    if "PERF:VIDEO-LAZY START" in html:
        return html, "already patched"
    body_close = re.search(r'</body>', html, re.IGNORECASE)
    if not body_close:
        return html, "</body> tag not found"
    return html[:body_close.start()] + DESKTOP_VIDEO_LOADER + html[body_close.start():], "applied"


# ════════════════════════════════════════════════════════════════════
IMG_TAG_PATTERN = re.compile(r'<img\s[^>]*?>', re.IGNORECASE | re.DOTALL)


def patch_6_lazy_images(html, file_rel):
    changed = 0
    skipped = 0

    def process_img(match):
        nonlocal changed, skipped
        tag = match.group(0)
        if 'id="heroPoster"' in tag or "id='heroPoster'" in tag:
            skipped += 1
            return tag
        if re.search(r'\bloading\s*=', tag, re.IGNORECASE):
            skipped += 1
            return tag
        src_match = re.search(r'src\s*=\s*["\']([^"\']+)["\']', tag, re.IGNORECASE)
        if src_match:
            src = src_match.group(1)
            if src.startswith('data:'):
                skipped += 1
                return tag
            if 'logo' in src.lower() or 'nav-' in src.lower():
                skipped += 1
                return tag
        new_tag = tag.rstrip('>').rstrip('/').rstrip()
        if not re.search(r'\bloading\s*=', new_tag, re.IGNORECASE):
            new_tag += ' loading="lazy"'
        if not re.search(r'\bdecoding\s*=', new_tag, re.IGNORECASE):
            new_tag += ' decoding="async"'
        if tag.rstrip().endswith('/>'):
            new_tag += ' />'
        else:
            new_tag += '>'
        changed += 1
        return new_tag

    new_html = IMG_TAG_PATTERN.sub(process_img, html)
    if changed == 0 and skipped > 0:
        return html, f"already patched ({skipped} images already had loading=)"
    if changed == 0:
        return html, "no <img> tags found"
    return new_html, f"applied to {changed} image(s)"


# ════════════════════════════════════════════════════════════════════
PATCHES = [
    (1, "Hero video → poster image", patch_1_hero_video),
    (2, "Lazy-load gtag/Google Ads", patch_2_lazy_gtag),
    (3, "Fix CSS preload pattern", patch_3_css_preload),
    (4, "Hero preload polish", patch_4_hero_preload),
    (5, "Desktop video lazy-loader", patch_5_video_lazy),
    (6, "Lazy-load non-hero images", patch_6_lazy_images),
]


def find_html_files(root):
    skip_dirs = {".git", "node_modules", ".vercel", ".next", "dist", "build"}
    for path in root.rglob("*.html"):
        if any(p in skip_dirs for p in path.parts):
            continue
        yield path


def backup_file(path):
    backup = path.with_suffix(path.suffix + ".bak")
    if not backup.exists():
        shutil.copy2(path, backup)


def main():
    ap = argparse.ArgumentParser(description="Apply all performance patches.")
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

    enabled = set(p[0] for p in PATCHES)
    if args.only:
        enabled = set(args.only) & enabled
    enabled -= set(args.skip)

    print()
    print(f"{BOLD}{BLUE}{'═' * 70}{RESET}")
    print(f"{BOLD}{BLUE}  ⚡ Performance Fix · La Table Marrakech (v2){RESET}")
    print(f"{BOLD}{BLUE}{'═' * 70}{RESET}")
    print(f"  📂 Root        : {root}")
    print(f"  🔧 Mode        : {'DRY RUN' if args.dry_run else 'WRITE'}")
    print(f"  🩹 Patches     : {sorted(enabled) if enabled else 'none'}")
    print(f"  💾 Backups     : {'NO' if args.no_backup else 'YES (.bak)'}")
    print(f"{BOLD}{BLUE}{'═' * 70}{RESET}")

    if not enabled:
        print(f"{YELLOW}  No patches enabled. Exiting.{RESET}")
        return

    files = sorted(find_html_files(root))
    if not files:
        print(f"{RED}  No HTML files found.{RESET}")
        return

    summary = {p[0]: {"applied": 0, "skipped": 0, "already": 0, "notfound": 0} for p in PATCHES}
    files_modified = 0

    for path in files:
        rel = str(path.relative_to(root))
        try:
            html = path.read_text(encoding="utf-8")
        except Exception as e:
            print(f"  {RED}⚠  Could not read {rel}: {e}{RESET}")
            continue

        original = html
        actions = []
        for num, label, fn in PATCHES:
            if num not in enabled:
                continue
            html, status = fn(html, rel)
            actions.append((num, label, status))
            if status == "applied" or status.startswith("applied to"):
                summary[num]["applied"] += 1
            elif status == "already patched" or status.startswith("already patched"):
                summary[num]["already"] += 1
            elif status.startswith("skipped"):
                summary[num]["skipped"] += 1
            else:
                summary[num]["notfound"] += 1

        if html != original:
            files_modified += 1
            print()
            print(f"{BOLD}  📝 {rel}{RESET}")
            for num, label, status in actions:
                if status == "applied" or status.startswith("applied to"):
                    print(f"     {GREEN}✓{RESET} [{num}] {label}: {status}")
                elif status == "already patched" or status.startswith("already patched"):
                    print(f"     {DIM}·{RESET} [{num}] {label}: {DIM}{status}{RESET}")
                elif status.startswith("skipped"):
                    print(f"     {DIM}·{RESET} [{num}] {label}: {DIM}{status}{RESET}")
                else:
                    print(f"     {YELLOW}⚠{RESET} [{num}] {label}: {YELLOW}{status}{RESET}")
            if not args.dry_run:
                if not args.no_backup:
                    backup_file(path)
                path.write_text(html, encoding="utf-8")

    print()
    print(f"{BOLD}{BLUE}{'═' * 70}{RESET}")
    print(f"{BOLD}  📊 Summary{RESET}")
    print(f"{BOLD}{BLUE}{'═' * 70}{RESET}")
    print(f"  HTML files scanned : {len(files)}")
    print(f"  Files modified     : {files_modified}")
    print()
    print(f"  {'Patch':<35} {'Applied':>8} {'Already':>8} {'Skipped':>8} {'Not found':>10}")
    print(f"  {'-' * 35} {'-' * 8} {'-' * 8} {'-' * 8} {'-' * 10}")
    for num, label, _ in PATCHES:
        if num not in enabled:
            continue
        s = summary[num]
        print(f"  [{num}] {label:<31} {s['applied']:>8} {s['already']:>8} "
              f"{s['skipped']:>8} {s['notfound']:>10}")

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
        print(f"    2. git add . && git commit -m 'Perf: hero img, lazy gtag, lazy images' && git push")
        print(f"    3. After Vercel deploys, re-run PageSpeed Insights 5 times — take the median")
    print(f"{BOLD}{BLUE}{'═' * 70}{RESET}")
    print()


if __name__ == "__main__":
    main()
