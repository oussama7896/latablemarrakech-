/**
 * /api/bookings — Vercel Edge function.
 *
 * Receives a booking enquiry from the homepage form and forwards it to the
 * business owner via Telegram. The guest never opens WhatsApp; we tell them
 * "we'll WhatsApp you back" on the form-side success state.
 *
 * Required env vars (set in Vercel project settings):
 *   TELEGRAM_BOT_TOKEN  →  from @BotFather, looks like "12345:ABC-..."
 *   TELEGRAM_CHAT_ID    →  numeric chat id (your own user, or a group id)
 *
 * Optional:
 *   ALLOWED_ORIGIN      →  CORS allowlist (comma-separated for multiple).
 *                          Defaults to the production origin — fails closed,
 *                          not open. Override only for local / preview.
 *
 * Production hardening:
 *   - Zod-validated input
 *   - HTML-escaped Telegram message (defense-in-depth)
 *   - Request body size cap (8 KB)
 *   - Per-IP token-bucket rate limit (5/min, 20/hour)
 *   - Retry with exponential backoff on Telegram transient failures
 *   - Fail-closed CORS (no wildcard fallback)
 */
import { z } from 'zod';

export const config = { runtime: 'edge' } as const;

const DEFAULT_ALLOWED_ORIGIN = 'https://latablemarrakech.com';
const MAX_BODY_BYTES = 8 * 1024; // 8 KB — form payload is ~1 KB
const RATE_PER_MINUTE = 5;
const RATE_PER_HOUR = 20;
const TELEGRAM_TIMEOUT_MS = 5_000;
const TELEGRAM_RETRIES = 3;

const ALLOWED_LANGS = ['en', 'fr', 'ar'] as const;

const bookingSchema = z.object({
  name: z.string().trim().min(2).max(120),
  email: z.string().trim().email().max(160),
  phone: z.string().trim().min(6).max(32),
  date: z.string().trim().regex(/^\d{4}-\d{2}-\d{2}$/),
  time: z.string().trim().min(2).max(64),
  guests: z.string().trim().min(1).max(8),
  notes: z.string().trim().max(2000).optional().default(''),
  lang: z.enum(ALLOWED_LANGS).optional().default('en'),
});

type Booking = z.infer<typeof bookingSchema>;

interface OkBody { ok: true; }
interface ErrBody { ok: false; error: string; }

function jsonResponse(status: number, body: OkBody | ErrBody, origin: string): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      'content-type': 'application/json; charset=utf-8',
      'access-control-allow-origin': origin,
      'access-control-allow-methods': 'POST, OPTIONS',
      'access-control-allow-headers': 'content-type',
      'cache-control': 'no-store',
      'vary': 'origin',
    },
  });
}

/* ───────── CORS ──────────────────────────────────────────────────────── */

function resolveOrigin(req: Request): string {
  const allowlist = (process.env.ALLOWED_ORIGIN ?? DEFAULT_ALLOWED_ORIGIN)
    .split(',')
    .map((o) => o.trim())
    .filter(Boolean);
  const reqOrigin = req.headers.get('origin') ?? '';
  if (allowlist.includes(reqOrigin)) return reqOrigin;
  // Fail closed: echo back the first allowed origin so the browser blocks
  // the response when the requester wasn't on the list.
  return allowlist[0] ?? DEFAULT_ALLOWED_ORIGIN;
}

/* ───────── Rate limit (in-memory, per-region) ────────────────────────── */

const ipHits = new Map<string, number[]>();

function getClientIp(req: Request): string {
  const fwd = req.headers.get('x-forwarded-for') ?? '';
  const first = fwd.split(',')[0]?.trim();
  return first || req.headers.get('x-real-ip') || 'unknown';
}

function rateLimited(ip: string, now: number): boolean {
  const hits = ipHits.get(ip) ?? [];
  // Drop anything older than one hour
  const oneHour = 60 * 60 * 1000;
  const oneMinute = 60 * 1000;
  const recent = hits.filter((t) => now - t < oneHour);
  const lastMinute = recent.filter((t) => now - t < oneMinute);
  if (lastMinute.length >= RATE_PER_MINUTE) return true;
  if (recent.length >= RATE_PER_HOUR) return true;
  recent.push(now);
  ipHits.set(ip, recent);
  // Opportunistic GC so the map doesn't grow forever
  if (ipHits.size > 2_000) {
    for (const [key, times] of ipHits) {
      if (!times.some((t) => now - t < oneHour)) ipHits.delete(key);
    }
  }
  return false;
}

/* ───────── Telegram with retry + timeout ─────────────────────────────── */

interface TelegramResult { ok: boolean; status: number; error?: string; }

async function postTelegram(token: string, chatId: string, text: string): Promise<TelegramResult> {
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), TELEGRAM_TIMEOUT_MS);
  try {
    const res = await fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({
        chat_id: chatId,
        text,
        parse_mode: 'HTML',
        disable_web_page_preview: true,
      }),
      signal: ctrl.signal,
    });
    if (res.ok) return { ok: true, status: res.status };
    const errText = await res.text().catch(() => '');
    return { ok: false, status: res.status, error: errText.slice(0, 200) };
  } catch (e) {
    return {
      ok: false,
      status: 0,
      error: e instanceof Error ? e.message.slice(0, 200) : 'fetch_failed',
    };
  } finally {
    clearTimeout(timer);
  }
}

async function sendTelegramWithRetry(token: string, chatId: string, text: string): Promise<TelegramResult> {
  let last: TelegramResult = { ok: false, status: 0, error: 'no_attempt' };
  for (let i = 0; i < TELEGRAM_RETRIES; i++) {
    last = await postTelegram(token, chatId, text);
    if (last.ok) return last;
    // Don't retry on 4xx — those are our fault (bad token, bad chat_id, etc.)
    if (last.status >= 400 && last.status < 500) return last;
    if (i < TELEGRAM_RETRIES - 1) {
      // 200ms, 600ms, 1400ms — total <2.5s worst case
      const delay = 200 * Math.pow(3, i);
      await new Promise((r) => setTimeout(r, delay));
    }
  }
  return last;
}

/* ───────── Message rendering ─────────────────────────────────────────── */

function escapeHtml(s: string): string {
  return s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

function renderMessage(b: Booking): string {
  const flag = b.lang === 'fr' ? '🇫🇷' : b.lang === 'ar' ? '🇲🇦' : '🇬🇧';
  const digits = b.phone.replace(/\D/g, '');
  return [
    '<b>🍽️ New booking enquiry</b>',
    '',
    `<b>Name</b>     ${escapeHtml(b.name)}`,
    `<b>Phone</b>    <a href="tel:${escapeHtml(b.phone)}">${escapeHtml(b.phone)}</a>`,
    `<b>Email</b>    <a href="mailto:${escapeHtml(b.email)}">${escapeHtml(b.email)}</a>`,
    `<b>Date</b>     ${escapeHtml(b.date)}`,
    `<b>Time</b>     ${escapeHtml(b.time)}`,
    `<b>Guests</b>   ${escapeHtml(b.guests)}`,
    b.notes ? `<b>Notes</b>    ${escapeHtml(b.notes)}` : '',
    '',
    `<i>Reply via WhatsApp:</i> <a href="https://wa.me/${encodeURIComponent(digits)}">open chat</a>`,
    `<i>Lang:</i> ${flag} <code>${b.lang}</code>`,
  ]
    .filter(Boolean)
    .join('\n');
}

/* ───────── Handler ───────────────────────────────────────────────────── */

export default async function handler(req: Request): Promise<Response> {
  const origin = resolveOrigin(req);

  if (req.method === 'OPTIONS') {
    return new Response(null, {
      status: 204,
      headers: {
        'access-control-allow-origin': origin,
        'access-control-allow-methods': 'POST, OPTIONS',
        'access-control-allow-headers': 'content-type',
        'access-control-max-age': '86400',
        'vary': 'origin',
      },
    });
  }

  if (req.method !== 'POST') {
    return jsonResponse(405, { ok: false, error: 'method_not_allowed' }, origin);
  }

  // Body size — Content-Length is sent by every modern fetch client
  const declared = Number(req.headers.get('content-length') ?? '0');
  if (declared && declared > MAX_BODY_BYTES) {
    return jsonResponse(413, { ok: false, error: 'payload_too_large' }, origin);
  }

  // Rate limit
  const ip = getClientIp(req);
  if (rateLimited(ip, Date.now())) {
    return jsonResponse(429, { ok: false, error: 'rate_limited' }, origin);
  }

  // Parse + validate
  let payload: unknown;
  try {
    payload = await req.json();
  } catch {
    return jsonResponse(400, { ok: false, error: 'invalid_json' }, origin);
  }

  const parsed = bookingSchema.safeParse(payload);
  if (!parsed.success) {
    return jsonResponse(400, { ok: false, error: 'validation_failed' }, origin);
  }

  // Env vars
  const token = process.env.TELEGRAM_BOT_TOKEN;
  const chatId = process.env.TELEGRAM_CHAT_ID;
  if (!token || !chatId) {
    return jsonResponse(500, { ok: false, error: 'server_not_configured' }, origin);
  }

  // Send with retry
  const text = renderMessage(parsed.data);
  const sent = await sendTelegramWithRetry(token, chatId, text);
  if (!sent.ok) {
    return jsonResponse(502, { ok: false, error: 'telegram_failed' }, origin);
  }

  return jsonResponse(200, { ok: true }, origin);
}
