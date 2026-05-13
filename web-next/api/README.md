# /api/bookings — Telegram-backed booking endpoint

A Vercel Edge Function that receives booking enquiries from the homepage form
and forwards them to your Telegram via the Bot API. The guest never opens
WhatsApp; they see a confirmation card on the site, and you receive an
instant push notification on your phone.

## One-time setup (5 minutes)

### 1. Create a Telegram bot

1. Open Telegram on your phone, search for `@BotFather`, and start a chat.
2. Send `/newbot`.
3. Pick a display name, e.g. **La Table Bookings**.
4. Pick a username — must end in `bot`, e.g. `latable_bookings_bot`.
5. BotFather replies with a token like `7384217391:AAH8c-...`. **Copy it.**
   This is your `TELEGRAM_BOT_TOKEN`.

### 2. Get your chat ID

1. In Telegram, search for the bot you just created and send it any message
   (e.g. "hi").
2. In a browser, open:
   `https://api.telegram.org/bot<TOKEN>/getUpdates`
   (replace `<TOKEN>` with the token from step 1).
3. Find `"chat":{"id":<NUMBER>` in the JSON. That number is your
   `TELEGRAM_CHAT_ID`. **Copy it.**

> If you want bookings going to a Telegram **group** instead of your personal
> chat: add the bot to the group first, send a message in the group, then
> repeat step 2 — the chat id will be negative (e.g. `-100123456789`).

### 3. Add env vars to Vercel

Open your project on vercel.com → **Settings → Environment Variables**, then
add:

| Name | Value |
|------|-------|
| `TELEGRAM_BOT_TOKEN` | the token from step 1 |
| `TELEGRAM_CHAT_ID`   | the chat id from step 2 |
| `ALLOWED_ORIGIN`     | `https://latablemarrakech.com` *(optional, for CORS hardening)* |

Set them for **Production, Preview, and Development**. Re-deploy.

## How it works

```
guest fills form ──POST─► /api/bookings ──HTTPS──► Telegram Bot API ──► your phone
                              │
                              └── returns { ok: true }
                                  → form shows "We'll WhatsApp you back"
```

The function:
- Validates the payload with Zod (no garbage gets sent to your phone)
- HTML-escapes user input before formatting the Telegram message
- Uses the Edge runtime (sub-100ms responses, no cold start)
- Includes a `wa.me` shortcut link so you can open WhatsApp with the guest
  pre-loaded in one tap

## Local development

`astro dev` does **not** run Vercel functions. The `BookingForm` component
detects `import.meta.env.DEV` and shows a mock success state without hitting
the endpoint — useful for iterating on the form UI.

To test the function end-to-end locally:

```bash
npm install -g vercel
vercel dev
```

This starts a local server that emulates Vercel's runtime, so `/api/bookings`
becomes available at `http://localhost:3000/api/bookings`. Add a
`.env.local` file with `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` for it to
actually post to Telegram.

## When something goes wrong

- **No Telegram message arrives** → check Vercel function logs (Dashboard →
  Logs). Look for `telegram_failed` or `server_not_configured`.
- **`server_not_configured`** → env vars aren't set. Re-add them and redeploy.
- **`validation_failed`** → the form sent malformed data. Inspect the
  Vercel request body in the function logs.
- **Form shows the error fallback** → guest will see "Open WhatsApp instead"
  link, so bookings still flow even if the endpoint dies.

## Switching to real WhatsApp later

If you eventually want messages to land *inside WhatsApp* instead of
Telegram, the form payload is the same. Swap `sendTelegram()` in
`api/bookings.ts` for a call to Twilio's WhatsApp API or AiSensy / Gupshup.
The frontend doesn't need to change.
