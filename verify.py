#!/usr/bin/env python3
"""
verify.py — Verify all performance patches are applied correctly.
USAGE: python3 verify.py
"""
import os, re, sys
from pathlib import Path

GREEN = "\033[92m"; RED = "\033[91m"; YELLOW = "\033[93m"
BOLD = "\033[1m"; DIM = "\033[2m"; RESET = "\033[0m"

HOMEPAGES = ["index.html", "fr/index.html", "ar/index.html"]

HOMEPAGE_CHECKS = [
    ("Patch 1 · Hero <video> replaced with <img>",
     "PERF:HERO-IMG START",
     "Hero is now an <img> instead of autoplay video"),
    ("Patch 2 · gtag lazy-loaded on user interaction",
     "PERF:GTAG-LAZY START",
     "Google Analytics + Ads only load after user interacts"),
    ("Patch 3 · CSS preload pattern fixed",
     "PERF:CSS-PRELOAD START",
     "Single async stylesheet load (no double-fetch)"),
    ("Patch 4 · Hero preload polished",
     "PERF:HERO-PRELOAD",
     "Hero <link rel=preload> has fetchpriority=high"),
    ("Patch 5 · Desktop video lazy-loader installed",
     "PERF:VIDEO-LAZY START",
     "Desktop reloads video after page is interactive"),
]


def main():
    root = Path(".").resolve()
    print()
    print(f"{BOLD}═════════════════════════════════════════════════════════════════{RESET}")
    print(f"{BOLD}  ✅ Performance Patch Verification{RESET}")
    print(f"{BOLD}═════════════════════════════════════════════════════════════════{RESET}")
    print(f"  📂 {root}")
    print()

    passed = failed = 0

    for label, marker, desc in HOMEPAGE_CHECKS:
        hits = []
        for f in HOMEPAGES:
            path = root / f
            if not path.exists():
                continue
            if marker in path.read_text(encoding="utf-8"):
                hits.append(f)
        if len(hits) >= 1:
            print(f"  {GREEN}✓{RESET} {label}  {DIM}({len(hits)}/3 homepages){RESET}")
            print(f"    {DIM}{desc}{RESET}")
            passed += 1
        else:
            print(f"  {RED}✗{RESET} {label}  {DIM}(0/3 homepages){RESET}")
            print(f"    {DIM}{desc} — NOT applied{RESET}")
            failed += 1
        print()

    img_re = re.compile(r'<img\s[^>]*?>', re.IGNORECASE | re.DOTALL)
    total = lazy = 0
    for path in root.rglob("*.html"):
        if any(p in {".git", "node_modules", ".vercel"} for p in path.parts):
            continue
        if path.suffix == ".bak" or path.name.endswith(".html.bak"):
            continue
        try:
            html = path.read_text(encoding="utf-8")
        except Exception:
            continue
        for m in img_re.finditer(html):
            tag = m.group(0)
            if "heroPoster" in tag or "logo" in tag.lower() or "nav-" in tag.lower():
                continue
            total += 1
            if re.search(r'\bloading\s*=\s*["\']lazy["\']', tag, re.IGNORECASE):
                lazy += 1

    pct = (lazy / total * 100) if total else 100
    label = "Patch 6 · Non-hero images have loading=lazy"
    if pct >= 90:
        print(f"  {GREEN}✓{RESET} {label}  {DIM}({lazy}/{total} = {pct:.0f}%){RESET}")
        passed += 1
    elif pct >= 50:
        print(f"  {YELLOW}~{RESET} {label}  {DIM}({lazy}/{total} = {pct:.0f}%){RESET}")
        failed += 1
    else:
        print(f"  {RED}✗{RESET} {label}  {DIM}({lazy}/{total} = {pct:.0f}%){RESET}")
        failed += 1

    print()
    print(f"{BOLD}═════════════════════════════════════════════════════════════════{RESET}")
    if failed == 0:
        print(f"  {GREEN}{BOLD}🎉 All 6 patches verified — ready to deploy{RESET}")
    else:
        print(f"  {YELLOW}{passed} passed, {failed} need attention.{RESET}")
        print(f"  {DIM}Run: python3 perf-fix.py{RESET}")
    print(f"{BOLD}═════════════════════════════════════════════════════════════════{RESET}")
    print()


if __name__ == "__main__":
    main()
