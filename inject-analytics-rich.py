#!/usr/bin/env python3
"""
inject-analytics-rich.py — replaces the PERF:ANALYTICS-RICH end-of-body
script block on every production page with the canonical version.

This block listens for:
  * whatsapp_click  — clicks on [data-event="whatsapp_click"] or any wa.me link
  * email_click     — clicks on a[href^="mailto:"]
  * phone_click     — clicks on a[href^="tel:"]
  * scroll_depth    — 25/50/75/90% scroll on high-intent pages
  * faq_open        — <details> toggle and .faq-question clicks
  * booking_enquiry_submit — submit on any <form data-track-form="booking-enquiry">

It NEVER blocks navigation: every event is fire-and-forget, push to dataLayer
plus gtag('event', ...) if gtag is loaded. Idempotent — running twice is a no-op.

Companion to inject-analytics.py (which handles the head-side gtag loader).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

SKIP_PATTERNS = (
    ".bak", "backup", "_deleted", ".impeccable",
    "temporary screenshots", "node_modules", ".git/",
    "screenshot-helper", "social-logo",
)

CANONICAL_BLOCK = """<!-- PERF:ANALYTICS-RICH START — enriched WhatsApp + scroll + FAQ + form tracking -->
<script>
(function () {
  'use strict';
  function device() {
    return window.matchMedia('(max-width: 768px)').matches ? 'mobile' : 'desktop';
  }
  function normalizeLabel(el) {
    var t = (el.getAttribute('aria-label') || el.textContent || '').trim();
    t = t.replace(/[\\u{1F300}-\\u{1FAFF}\\u{2600}-\\u{27BF}]/gu, '');
    t = t.replace(/\\s+/g, ' ').replace(/[^\\w\\s\\-À-ſ&'.,—]/g, '').trim();
    return (t || 'unlabeled').substring(0, 80);
  }
  function ctaPosition(link) {
    if (link.closest('.wa-float, .lt-stickywa, .sticky-mobile-bar, [class*="floating"]')) return 'sticky';
    if (link.closest('header, nav, .nav, [class*="nav-"]')) return 'navbar';
    if (link.closest('.hero, #hero, .hero-cta-row')) return 'hero';
    if (link.closest('footer, .site-footer')) return 'footer';
    if (link.closest('.tier-card, .tier-grid, .price-table')) return 'pricing-tier';
    if (link.closest('.inline-cta, .cta, #contact')) return 'cta-block';
    return 'inline';
  }
  // Dev-detection: auto-on for localhost / 127.0.0.1 / file: / vercel preview
  // domains, opt-in for prod via ?debug=1 or localStorage.analytics_debug = '1'.
  // NEVER true on the live latablemarrakech.com domain unless a human opts in.
  function isDev() {
    try {
      var h = location.hostname;
      if (h === 'localhost' || h === '127.0.0.1' || h === '0.0.0.0') return true;
      if (location.protocol === 'file:') return true;
      if (/\\.vercel\\.app$/.test(h)) return true;
      if (/[?&]debug=1\\b/.test(location.search)) return true;
      if (window.localStorage && localStorage.getItem('analytics_debug') === '1') return true;
    } catch (e) { /* sandboxed iframes can throw on localStorage */ }
    return false;
  }
  var DEV = isDev();
  if (DEV && typeof console !== 'undefined' && console.info) {
    console.info('%c[ANALYTICS DEV] enabled', 'color:#C1622F;font-weight:bold',
      '— set localStorage.analytics_debug=\"0\" to silence');
  }
  function fire(name, params) {
    try {
      params = params || {};
      params.page_path = window.location.pathname;
      params.page_title = document.title;
      // GA4 DebugView routing — set in CONSENT MODE block when on /analytics-qa/?debug=1.
      // No-op everywhere else, so production traffic is untouched.
      if (window.__gaDebugMode) params.debug_mode = true;
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push(Object.assign({ event: name }, params));
      if (typeof gtag === 'function') gtag('event', name, params);
      if (DEV && typeof console !== 'undefined' && console.log) {
        console.log('%c[ANALYTICS DEV] ' + name, 'color:#0a8f3c;font-weight:bold', params);
      }
      if (window.__gaDebugMode && typeof console !== 'undefined' && console.log) {
        console.log('%c[GA4 DEBUG] sending event', 'color:#c1622f;font-weight:bold', name, params);
      }
    } catch (e) { /* never block UX on tracking */ }
  }

  // ---- WhatsApp clicks ----
  document.addEventListener('click', function (e) {
    var link = e.target.closest('[data-event="whatsapp_click"], a[href*="wa.me"], a[href*="api.whatsapp.com"]');
    if (!link) return;
    fire('whatsapp_click', {
      cta_label: normalizeLabel(link),
      cta_position: ctaPosition(link),
      device: device(),
      link_url: link.href,
      button_location: link.getAttribute('data-location') || ctaPosition(link)
    });
  }, { passive: true });

  // ---- mailto: clicks ----
  document.addEventListener('click', function (e) {
    var link = e.target.closest('a[href^="mailto:"]');
    if (!link) return;
    fire('email_click', {
      cta_label: normalizeLabel(link),
      cta_position: ctaPosition(link),
      link_url: link.href
    });
  }, { passive: true });

  // ---- tel: clicks ----
  document.addEventListener('click', function (e) {
    var link = e.target.closest('a[href^="tel:"]');
    if (!link) return;
    fire('phone_click', {
      cta_label: normalizeLabel(link),
      cta_position: ctaPosition(link),
      link_url: link.href
    });
  }, { passive: true });

  // ---- Booking / enquiry form submits ----
  // Any <form data-track-form="booking-enquiry"> fires booking_enquiry_submit.
  // We fire after the form's own onsubmit (which usually opens WhatsApp).
  // Use a WeakSet to guard against double-fire if a form is re-submitted in <300ms.
  var formFired = new WeakSet();
  document.addEventListener('submit', function (e) {
    var form = e.target.closest('form[data-track-form="booking-enquiry"]');
    if (!form || formFired.has(form)) return;
    formFired.add(form);
    setTimeout(function () { formFired.delete(form); }, 1000);
    var guests = form.querySelector('[name="bguests"]');
    var date = form.querySelector('[name="bdate"]');
    var email = form.querySelector('[name="bemail"]');
    var notes = form.querySelector('[name="bnotes"]');
    var occasion = form.querySelector('[name="occasion"]');
    fire('booking_enquiry_submit', {
      form_id: form.getAttribute('data-form-id') || form.id || 'unknown',
      form_name: form.getAttribute('data-form-id') || form.id || 'unknown',
      group_size: guests ? String(guests.value || '').trim() : undefined,
      occasion: occasion ? String(occasion.value || '').trim() || undefined : undefined,
      has_date: date ? !!date.value : false,
      has_email: email ? !!email.value : false,
      has_notes: notes ? !!notes.value : false
    });
  }, true); // capture phase so we fire even if a child handler stops propagation

  // ---- Scroll depth (high-intent pages only) ----
  var SCROLL_PAGES = ['/', '/private-chef-cost-marrakech/', '/marrakech-villa-with-private-chef/',
    '/marrakech-cooking-class-vs-private-chef/', '/the-experience/', '/analytics-qa/'];
  var path = window.location.pathname;
  var pathNorm = path.endsWith('/') ? path : path + '/';
  if (SCROLL_PAGES.indexOf(path) > -1 || SCROLL_PAGES.indexOf(pathNorm) > -1) {
    var thresholds = [25, 50, 75, 90];
    var fired = {};
    var ticking = false;
    function checkScroll() {
      var doc = document.documentElement;
      var max = Math.max(doc.scrollHeight, document.body.scrollHeight) - window.innerHeight;
      if (max <= 0) return;
      var pct = (window.scrollY / max) * 100;
      thresholds.forEach(function (t) {
        if (pct >= t && !fired[t]) {
          fired[t] = true;
          fire('scroll_depth', { depth_percentage: t });
        }
      });
    }
    window.addEventListener('scroll', function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () { checkScroll(); ticking = false; });
    }, { passive: true });
  }

  // ---- FAQ open ----
  document.querySelectorAll('details').forEach(function (d) {
    d.addEventListener('toggle', function () {
      if (!d.open) return;
      var sum = d.querySelector('summary');
      fire('faq_open', { question_text: normalizeLabel(sum || d).substring(0, 120) });
    });
  });
  var faqClicked = new WeakSet();
  document.addEventListener('click', function (e) {
    var trigger = e.target.closest('.faq-question, [class*="faq-q"], [data-faq-trigger]');
    if (!trigger || faqClicked.has(trigger)) return;
    faqClicked.add(trigger);
    setTimeout(function () { faqClicked.delete(trigger); }, 300);
    fire('faq_open', { question_text: normalizeLabel(trigger).substring(0, 120) });
  }, { passive: true });
})();
</script>
<!-- PERF:ANALYTICS-RICH END -->"""

BLOCK_RE = re.compile(
    r"<!--\s*PERF:ANALYTICS-RICH START.*?<!--\s*PERF:ANALYTICS-RICH END\s*-->",
    re.DOTALL,
)


def should_skip(path: Path) -> bool:
    s = str(path)
    return any(p in s for p in SKIP_PATTERNS)


def transform(html: str) -> str:
    if not BLOCK_RE.search(html):
        # Page lacks the block entirely — don't try to inject; that's beyond
        # the safe scope of this codemod (no obvious anchor point).
        return html
    return BLOCK_RE.sub(lambda _: CANONICAL_BLOCK, html, count=1)


def main() -> int:
    changed = []
    skipped = []
    for path in sorted(ROOT.rglob("*.html")):
        if should_skip(path):
            skipped.append(path)
            continue
        original = path.read_text(encoding="utf-8")
        new = transform(original)
        if new != original:
            path.write_text(new, encoding="utf-8")
            changed.append(path)

    print(f"Changed: {len(changed)} files")
    for p in changed:
        print(f"  ~ {p.relative_to(ROOT)}")
    print(f"Skipped/unchanged: {len(skipped)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
