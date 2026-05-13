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
 *   ALLOWED_ORIGIN      →  CORS allowlist, e.g. "https://latablemarrakech.com"
 *                          (omit in dev — defaults to "*")
 */
import { z } from 'zod';

export const config = { runtime: 'edge' } as const;

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

const j = (status: number, body: OkBody | ErrBody, origin: string): Response =>
  new Response(JSON.stringify(body), {
    status,
    headers: {
      'content-type': 'application/json; charset=utf-8',
      'access-control-allow-origin': origin,
      'access-control-allow-methods': 'POST, OPTIONS',
      'access-control-allow-headers': 'content-type',
      'cache-control': 'no-store',
    },
  });

function escapeHtml(s: string): string {
  return s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

function renderMessage(b: Booking): string {
  const flag = b.lang === 'fr' ? '🇫🇷' : b.lang === 'ar' ? '🇲🇦' : '🇬🇧';
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
    `<i>Reply via WhatsApp:</i> <a href="https://wa.me/${encodeURIComponent(b.phone.replace(/\D/g, ''))}">open chat</a>`,
    `<i>Lang:</i> ${flag} <code>${b.lang}</code>`,
  ]
    .filter(Boolean)
    .join('\n');
}

async function sendTelegram(token: string, chatId: string, text: string): Promise<{ ok: boolean; status: number; error?: string }> {
  const res = await fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({
      chat_id: chatId,
      text,
      parse_mode: 'HTML',
      disable_web_page_preview: true,
    }),
  });
  if (res.ok) return { ok: true, status: res.status };
  const errText = await res.text().catch(() => '');
  return { ok: false, status: res.status, error: errText.slice(0, 200) };
}

export default async function handler(req: Request): Promise<Response> {
  const origin = process.env.ALLOWED_ORIGIN ?? '*';

  if (req.method === 'OPTIONS') return j(204 as 200, { ok: true }, origin);
  if (req.method !== 'POST') {
    return j(405, { ok: false, error: 'method_not_allowed' }, origin);
  }

  let payload: unknown;
  try {
    payload = await req.json();
  } catch {
    return j(400, { ok: false, error: 'invalid_json' }, origin);
  }

  const parsed = bookingSchema.safeParse(payload);
  if (!parsed.success) {
    return j(400, { ok: false, error: 'validation_failed' }, origin);
  }

  const token = process.env.TELEGRAM_BOT_TOKEN;
  const chatId = process.env.TELEGRAM_CHAT_ID;
  if (!token || !chatId) {
    return j(500, { ok: false, error: 'server_not_configured' }, origin);
  }

  const text = renderMessage(parsed.data);
  const sent = await sendTelegram(token, chatId, text);
  if (!sent.ok) {
    return j(502, { ok: false, error: 'telegram_failed' }, origin);
  }

  return j(200, { ok: true }, origin);
}
