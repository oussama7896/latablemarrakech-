#!/usr/bin/env python3
"""
strip-impeccable.py — removes the local-dev <!-- impeccable-live-start -->
... <!-- impeccable-live-end --> block injected by the Impeccable plugin.

That block points at http://localhost:8400/live.js and would 404 on every
page load in production. Run before any deploy / commit.

Idempotent.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKIP = (".bak", "backup", "_deleted", ".impeccable", "temporary screenshots",
        "node_modules", ".git/", "screenshot-helper", "social-logo")

BLOCK_RE = re.compile(
    r"\s*<!--\s*impeccable-live-start\s*-->.*?<!--\s*impeccable-live-end\s*-->\s*",
    re.DOTALL,
)


def main() -> int:
    changed = 0
    for path in sorted(ROOT.rglob("*.html")):
        if any(p in str(path) for p in SKIP):
            continue
        original = path.read_text(encoding="utf-8")
        new = BLOCK_RE.sub("\n", original)
        if new != original:
            path.write_text(new, encoding="utf-8")
            changed += 1
            print(f"  ~ {path.relative_to(ROOT)}")
    print(f"Stripped impeccable-live block from {changed} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
