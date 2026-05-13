/**
 * BookingForm — React island, brand-register surface.
 *
 *   <form id="booking-home" data-track-form="booking-enquiry" data-form-id="booking-home">
 *     <input name="bname"/> <input name="bemail"/> <input name="bdate"/>
 *     <select name="bguests"/> <select name="btime"/> <textarea name="bnotes"/>
 *
 * Brand decisions:
 *  - Hairline bottom-border inputs (no boxed input boxes)
 *  - Mono uppercase eyebrow labels above each field
 *  - Native <select> for mobile-friendly chooser; <input type="date"> for the calendar
 *  - Submit is the canonical ember pill, not a shadcn Button
 *  - Inline WhatsApp message preview lives above submit so the user sees what they're sending
 *  - <noscript> fallback under the form so a JS failure still routes to WhatsApp
 *
 * Submission opens WhatsApp pre-filled with a localised multi-line message
 * (EN / FR / AR), then replaces the form with a success card showing the
 * exact message + reopen / copy / reset controls.
 *
 * The global PERF:ANALYTICS-RICH listener (in Layout) fires
 * booking_enquiry_submit independently — no gtag call here.
 */

import { useEffect, useId, useMemo, useState, type FormEvent } from 'react';

const WHATSAPP = '212721354757';

const GUEST_OPTIONS = ['2', '3', '4', '5', '6', '7', '8', '10', '12', '20+'] as const;
const TIME_OPTIONS = [
  '12:00 — Lunch',
  '13:00 — Lunch',
  '19:00 — Dinner',
  '20:00 — Dinner',
  '21:00 — Dinner',
] as const;

type Lang = 'en' | 'fr' | 'ar';

interface MessageTemplate {
  intro: string;
  outro: string;
  labels: {
    name: string;
    email: string;
    date: string;
    time: string;
    guests: string;
    notes: string;
  };
  fieldLabels: {
    name: string;
    email: string;
    date: string;
    time: string;
    guests: string;
    notes: string;
  };
  fieldPlaceholders: {
    name: string;
    email: string;
    notes: string;
  };
  fieldHints: {
    date: string;
    notes: string;
  };
  previewHeading: string;
  submitCta: string;
  microFooter: string;
  noscriptLine: string;
  successTitle: string;
  successBody: string;
  reopenCta: string;
  copyCta: string;
  copiedCta: string;
  resetCta: string;
}

const TEMPLATES: Record<Lang, MessageTemplate> = {
  en: {
    intro: "Hi La Table, I'd like to book a private chef.",
    outro: 'Looking forward to your reply.',
    labels: {
      name: 'Name', email: 'Email', date: 'Date',
      time: 'Time', guests: 'Guests', notes: 'Notes',
    },
    fieldLabels: {
      name: 'Your name', email: 'Email', date: 'Preferred date',
      time: 'Preferred time', guests: 'Guests', notes: 'Anything we should know',
    },
    fieldPlaceholders: {
      name: 'First and last',
      email: 'name@example.com',
      notes: 'Anniversary, allergies, dietary needs.',
    },
    fieldHints: {
      date: 'At least 72 hours from now.',
      notes: 'Optional. The more we know, the better the menu.',
    },
    previewHeading: 'This is the message we will receive',
    submitCta: 'Book your dinner',
    microFooter: 'Confirmed within 24 hours via WhatsApp · Minimum 2 guests · 72h notice',
    noscriptLine: 'If the form is not loading, message us directly on WhatsApp:',
    successTitle: 'Check your WhatsApp',
    successBody: "We've opened WhatsApp with your booking ready to send. Tap send and we'll reply within one hour.",
    reopenCta: 'Open WhatsApp again',
    copyCta: 'Copy message',
    copiedCta: 'Copied',
    resetCta: 'Send another booking',
  },
  fr: {
    intro: 'Bonjour La Table, je souhaite réserver un chef privé.',
    outro: 'Dans l’attente de votre réponse.',
    labels: {
      name: 'Nom', email: 'Email', date: 'Date',
      time: 'Heure', guests: 'Convives', notes: 'Notes',
    },
    fieldLabels: {
      name: 'Votre nom', email: 'Email', date: 'Date souhaitée',
      time: 'Heure souhaitée', guests: 'Convives', notes: 'Ce qu’il faut savoir',
    },
    fieldPlaceholders: {
      name: 'Prénom et nom',
      email: 'vous@exemple.com',
      notes: 'Anniversaire, allergies, régime alimentaire.',
    },
    fieldHints: {
      date: 'Au moins 72 heures à l’avance.',
      notes: 'Optionnel. Plus nous savons, mieux nous cuisinons.',
    },
    previewHeading: 'Voici le message que nous allons recevoir',
    submitCta: 'Réserver un dîner',
    microFooter: 'Confirmation sous 24 heures via WhatsApp · 2 convives minimum · 72 h de préavis',
    noscriptLine: 'Si le formulaire ne se charge pas, écrivez-nous directement sur WhatsApp :',
    successTitle: 'Vérifiez votre WhatsApp',
    successBody: 'Nous avons ouvert WhatsApp avec votre demande prête à envoyer. Appuyez sur envoyer, nous répondons sous une heure.',
    reopenCta: 'Rouvrir WhatsApp',
    copyCta: 'Copier le message',
    copiedCta: 'Copié',
    resetCta: 'Nouvelle réservation',
  },
  ar: {
    intro: 'السلام عليكم، أرغب في حجز طاهٍ خاص لدى لا تابل.',
    outro: 'في انتظار ردكم.',
    labels: {
      name: 'الاسم', email: 'البريد الإلكتروني', date: 'التاريخ',
      time: 'الوقت', guests: 'عدد الضيوف', notes: 'ملاحظات',
    },
    fieldLabels: {
      name: 'الاسم', email: 'البريد الإلكتروني', date: 'التاريخ المرغوب',
      time: 'الوقت المرغوب', guests: 'عدد الضيوف', notes: 'ما يجب أن نعرفه',
    },
    fieldPlaceholders: {
      name: 'الاسم الكامل',
      email: 'name@example.com',
      notes: 'مناسبة، حساسيات، نظام غذائي.',
    },
    fieldHints: {
      date: 'قبل 72 ساعة على الأقل.',
      notes: 'اختياري. كلما عرفنا أكثر، كان المنيو أفضل.',
    },
    previewHeading: 'هذه هي الرسالة التي سنستلمها',
    submitCta: 'احجز عشاءك',
    microFooter: 'تأكيد خلال 24 ساعة عبر واتساب · من ضيفين كحد أدنى · إشعار 72 ساعة',
    noscriptLine: 'إذا لم يعمل النموذج، راسلنا مباشرة على واتساب:',
    successTitle: 'افتح واتساب',
    successBody: 'فتحنا واتساب مع طلب الحجز جاهزًا للإرسال. اضغط على إرسال، وسنرد في غضون ساعة.',
    reopenCta: 'افتح واتساب مرة أخرى',
    copyCta: 'نسخ الرسالة',
    copiedCta: 'تم النسخ',
    resetCta: 'حجز جديد',
  },
};

function detectLang(): Lang {
  if (typeof document === 'undefined') return 'en';
  const raw = (document.documentElement.lang || 'en').toLowerCase().split('-')[0];
  return raw === 'fr' || raw === 'ar' ? raw : 'en';
}

interface Draft {
  name: string;
  email: string;
  date: string;
  time: string;
  guests: string;
  notes: string;
}

function buildMessage(draft: Draft, lang: Lang): string {
  const t = TEMPLATES[lang];
  const lines = [t.intro, '', `${t.labels.name}: ${draft.name || '—'}`];
  if (draft.email) lines.push(`${t.labels.email}: ${draft.email}`);
  lines.push(`${t.labels.date}: ${draft.date || '—'}`);
  lines.push(`${t.labels.time}: ${draft.time || '—'}`);
  lines.push(`${t.labels.guests}: ${draft.guests || '—'}`);
  if (draft.notes) lines.push(`${t.labels.notes}: ${draft.notes}`);
  lines.push('', t.outro);
  return lines.join('\n');
}

function buildWaUrl(message: string): string {
  return `https://wa.me/${WHATSAPP}?text=${encodeURIComponent(message)}`;
}

interface SentState {
  message: string;
  waUrl: string;
}

export function BookingForm() {
  const today = new Date().toISOString().slice(0, 10);
  const [draft, setDraft] = useState<Draft>({
    name: '',
    email: '',
    date: '',
    time: '20:00 — Dinner',
    guests: '6',
    notes: '',
  });
  const [sent, setSent] = useState<SentState | null>(null);
  const [copied, setCopied] = useState(false);
  const [lang, setLang] = useState<Lang>('en');
  const ids = {
    name: useId(), email: useId(), date: useId(), notes: useId(),
    guests: useId(), time: useId(),
  };

  useEffect(() => { setLang(detectLang()); }, []);

  const t = TEMPLATES[lang];

  const previewMessage = useMemo(() => buildMessage(draft, lang), [draft, lang]);

  function update<K extends keyof Draft>(key: K, value: Draft[K]): void {
    setDraft((d) => ({ ...d, [key]: value }));
  }

  function onSubmit(e: FormEvent<HTMLFormElement>): void {
    e.preventDefault();
    const message = buildMessage(draft, lang);
    const waUrl = buildWaUrl(message);
    window.open(waUrl, '_blank', 'noopener');
    setSent({ message, waUrl });
    setCopied(false);
  }

  async function copyMessage(): Promise<void> {
    if (!sent) return;
    try {
      if (navigator.clipboard?.writeText) {
        await navigator.clipboard.writeText(sent.message);
      } else {
        const ta = document.createElement('textarea');
        ta.value = sent.message;
        ta.style.position = 'fixed';
        ta.style.opacity = '0';
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
      }
      setCopied(true);
      window.setTimeout(() => setCopied(false), 2200);
    } catch {
      setCopied(false);
    }
  }

  function reset(): void {
    setSent(null);
    setCopied(false);
  }

  if (sent) {
    return (
      <div
        role="status"
        aria-live="polite"
        className="flex flex-col gap-5 border border-ember/40 bg-ink/40 p-6 sm:p-7"
      >
        <div className="flex items-center gap-3">
          <span aria-hidden="true" className="inline-flex size-7 items-center justify-center rounded-full bg-ember text-sand">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <polyline points="20 6 9 17 4 12"/>
            </svg>
          </span>
          <h3 className="font-display text-[1.25rem] tracking-[0.03em] text-sand">{t.successTitle}</h3>
        </div>
        <p className="text-[14.5px] leading-[1.65] text-sand-muted">{t.successBody}</p>
        <pre className="overflow-x-auto whitespace-pre-wrap break-words border border-gold/15 bg-ink/60 p-4 font-mono text-[12.5px] leading-[1.6] text-sand/90">
          {sent.message}
        </pre>
        <div className="flex flex-wrap items-center gap-3">
          <a
            href={sent.waUrl}
            target="_blank"
            rel="noopener noreferrer"
            data-event="whatsapp_click"
            data-location="booking-success"
            className="inline-flex items-center gap-2 rounded-full bg-ember px-5 py-2.5 font-mono text-[11px] uppercase tracking-[0.22em] text-sand transition hover:bg-ember-light hover:-translate-y-px"
          >
            {t.reopenCta}
            <span aria-hidden="true" className="inline-block size-1.5 rotate-45 bg-sand"></span>
          </a>
          <button
            type="button"
            onClick={copyMessage}
            className="inline-flex items-center gap-2 rounded-full border border-gold/30 px-5 py-2.5 font-mono text-[11px] uppercase tracking-[0.22em] text-gold-light transition hover:border-ember hover:text-sand"
          >
            {copied ? t.copiedCta : t.copyCta}
          </button>
          <button
            type="button"
            onClick={reset}
            className="ms-auto font-mono text-[11px] uppercase tracking-[0.22em] text-sand-muted underline-offset-4 transition hover:text-sand hover:underline"
          >
            {t.resetCta}
          </button>
        </div>
      </div>
    );
  }

  return (
    <form
      id="booking-home"
      data-track-form="booking-enquiry"
      data-form-id="booking-home"
      onSubmit={onSubmit}
      className="lt-bf grid gap-6 sm:gap-7"
    >
      <div className="grid gap-6 sm:grid-cols-2 sm:gap-7">
        <FieldText
          id={ids.name}
          name="bname"
          label={t.fieldLabels.name}
          placeholder={t.fieldPlaceholders.name}
          autoComplete="name"
          value={draft.name}
          onChange={(v) => update('name', v)}
          required
        />
        <FieldText
          id={ids.email}
          name="bemail"
          type="email"
          label={t.fieldLabels.email}
          placeholder={t.fieldPlaceholders.email}
          autoComplete="email"
          value={draft.email}
          onChange={(v) => update('email', v)}
          required
        />
        <FieldSelect
          id={ids.guests}
          name="bguests"
          label={t.fieldLabels.guests}
          options={GUEST_OPTIONS as readonly string[]}
          value={draft.guests}
          onChange={(v) => update('guests', v)}
        />
        <FieldText
          id={ids.date}
          name="bdate"
          type="date"
          label={t.fieldLabels.date}
          value={draft.date}
          onChange={(v) => update('date', v)}
          min={today}
          hint={t.fieldHints.date}
          required
        />
        <div className="sm:col-span-2">
          <FieldSelect
            id={ids.time}
            name="btime"
            label={t.fieldLabels.time}
            options={TIME_OPTIONS as readonly string[]}
            value={draft.time}
            onChange={(v) => update('time', v)}
          />
        </div>
        <div className="sm:col-span-2">
          <FieldTextarea
            id={ids.notes}
            name="bnotes"
            label={t.fieldLabels.notes}
            placeholder={t.fieldPlaceholders.notes}
            value={draft.notes}
            onChange={(v) => update('notes', v)}
            hint={t.fieldHints.notes}
          />
        </div>
      </div>

      {/* Inline message preview — show what gets sent before they tap submit */}
      <div className="border border-gold/15 bg-ink/50 p-5">
        <p className="font-mono text-[10px] uppercase tracking-[0.28em] text-gold-light">
          {t.previewHeading}
        </p>
        <pre className="mt-3 overflow-x-auto whitespace-pre-wrap break-words font-mono text-[12.5px] leading-[1.65] text-sand/85">
          {previewMessage}
        </pre>
      </div>

      <div className="flex flex-col items-center gap-3">
        <button
          type="submit"
          className="group inline-flex items-center gap-3 rounded-full bg-ember px-9 py-4 font-mono text-[12px] uppercase tracking-[0.22em] text-sand shadow-[0_18px_40px_-12px_rgba(184,79,46,0.55)] transition hover:bg-ember-light hover:-translate-y-px"
        >
          {t.submitCta}
          <span aria-hidden="true" className="inline-block size-2 rotate-45 bg-sand transition group-hover:translate-x-0.5"></span>
        </button>
        <p className="text-center font-mono text-[10px] uppercase tracking-[0.22em] text-sand-muted">
          {t.microFooter}
        </p>
      </div>

    </form>
  );
}

/* ────────────────────────────────────────────────────────────────────────── */
/*  Field primitives — hairline-bottom inputs, no shadcn dependency.        */
/* ────────────────────────────────────────────────────────────────────────── */

interface FieldShellProps {
  id: string;
  label: string;
  hint?: string;
  children: React.ReactNode;
}

function FieldShell({ id, label, hint, children }: FieldShellProps): React.ReactElement {
  return (
    <div className="flex flex-col gap-2">
      <label
        htmlFor={id}
        className="font-mono text-[10px] uppercase tracking-[0.28em] text-gold-light"
      >
        {label}
      </label>
      {children}
      {hint ? (
        <span className="text-[11px] leading-[1.5] text-sand-muted/85">{hint}</span>
      ) : null}
    </div>
  );
}

interface FieldTextProps {
  id: string;
  name: string;
  label: string;
  type?: 'text' | 'email' | 'date';
  placeholder?: string;
  autoComplete?: string;
  value: string;
  onChange: (v: string) => void;
  min?: string;
  hint?: string;
  required?: boolean;
}

function FieldText({
  id, name, label, type = 'text', placeholder, autoComplete,
  value, onChange, min, hint, required,
}: FieldTextProps): React.ReactElement {
  return (
    <FieldShell id={id} label={label} hint={hint}>
      <input
        id={id}
        name={name}
        type={type}
        placeholder={placeholder}
        autoComplete={autoComplete}
        value={value}
        onChange={(e) => onChange(e.currentTarget.value)}
        min={min}
        required={required}
        className="lt-bf-input border-0 border-b border-gold/25 bg-transparent px-0 py-2.5 text-[15px] text-sand placeholder:text-sand-muted/60 outline-none transition-colors focus:border-ember focus-visible:shadow-[0_2px_0_0_rgba(180,90,40,1)]"
      />
    </FieldShell>
  );
}

interface FieldSelectProps {
  id: string;
  name: string;
  label: string;
  options: readonly string[];
  value: string;
  onChange: (v: string) => void;
}

function FieldSelect({ id, name, label, options, value, onChange }: FieldSelectProps): React.ReactElement {
  return (
    <FieldShell id={id} label={label}>
      <div className="relative">
        <select
          id={id}
          name={name}
          value={value}
          onChange={(e) => onChange(e.currentTarget.value)}
          className="lt-bf-input w-full appearance-none border-0 border-b border-gold/25 bg-transparent px-0 py-2.5 pe-7 text-[15px] text-sand outline-none transition-colors focus:border-ember focus-visible:shadow-[0_2px_0_0_rgba(180,90,40,1)]"
        >
          {options.map((opt) => (
            <option key={opt} value={opt} className="bg-ink text-sand">
              {opt}
            </option>
          ))}
        </select>
        <span
          aria-hidden="true"
          className="pointer-events-none absolute end-0 top-1/2 inline-block size-1.5 -translate-y-1/2 rotate-45 border-b border-r border-gold-light"
        ></span>
      </div>
    </FieldShell>
  );
}

interface FieldTextareaProps {
  id: string;
  name: string;
  label: string;
  placeholder?: string;
  value: string;
  onChange: (v: string) => void;
  hint?: string;
}

function FieldTextarea({
  id, name, label, placeholder, value, onChange, hint,
}: FieldTextareaProps): React.ReactElement {
  return (
    <FieldShell id={id} label={label} hint={hint}>
      <textarea
        id={id}
        name={name}
        placeholder={placeholder}
        value={value}
        onChange={(e) => onChange(e.currentTarget.value)}
        rows={3}
        className="lt-bf-input border-0 border-b border-gold/25 bg-transparent px-0 py-2.5 text-[15px] leading-[1.6] text-sand placeholder:text-sand-muted/60 outline-none transition-colors focus:border-ember focus-visible:shadow-[0_2px_0_0_rgba(180,90,40,1)] resize-none"
      />
    </FieldShell>
  );
}
