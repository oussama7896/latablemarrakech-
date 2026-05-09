/**
 * ContactForm — React island for the /contact/ page enquiry form.
 *
 * Same tracking contract as the live static site:
 *   <form id="booking-contact" data-track-form="booking-enquiry" data-form-id="booking-contact">
 *     <input name="bname"/> <input name="bdate"/> <input name="bguests"/>
 *     <input name="bvenue"/> <input name="bdiet"/> <textarea name="bnotes"/>
 *
 * Submit opens WhatsApp pre-filled. The global PERF:ANALYTICS-RICH listener
 * (in Layout.astro) fires booking_enquiry_submit independently — no gtag
 * call needed here.
 */

import { useId, type FormEvent } from 'react';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';

const WHATSAPP = '212721354757';

export function ContactForm() {
  const ids = {
    name: useId(), date: useId(), guests: useId(), venue: useId(), diet: useId(), notes: useId(),
  };

  function onSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const data = new FormData(e.currentTarget);
    const lines = [
      'Hi La Table Marrakech — I would like to book a private chef.',
      `Name: ${data.get('bname') || ''}`,
      `Date: ${data.get('bdate') || ''}`,
      `Guests: ${data.get('bguests') || ''}`,
      `Address / venue: ${data.get('bvenue') || ''}`,
      `Dietary needs: ${data.get('bdiet') || ''}`,
      `Notes: ${data.get('bnotes') || ''}`,
    ].join('\n');
    window.open(
      `https://wa.me/${WHATSAPP}?text=${encodeURIComponent(lines)}`,
      '_blank',
      'noopener',
    );
  }

  return (
    <form
      id="booking-contact"
      data-track-form="booking-enquiry"
      data-form-id="booking-contact"
      onSubmit={onSubmit}
      className="grid gap-4"
    >
      <div className="grid gap-2">
        <Label htmlFor={ids.name}>Your name</Label>
        <Input id={ids.name} name="bname" type="text" required />
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        <div className="grid gap-2">
          <Label htmlFor={ids.date}>Date (or window)</Label>
          <Input id={ids.date} name="bdate" type="text" placeholder="e.g. 14 Nov, or 12-15 Nov" />
        </div>
        <div className="grid gap-2">
          <Label htmlFor={ids.guests}>Guests</Label>
          <Input id={ids.guests} name="bguests" type="number" min={2} placeholder="e.g. 6" />
        </div>
      </div>

      <div className="grid gap-2">
        <Label htmlFor={ids.venue}>Address or venue</Label>
        <Input
          id={ids.venue}
          name="bvenue"
          type="text"
          placeholder="Villa name, neighbourhood, or full address"
        />
      </div>

      <div className="grid gap-2">
        <Label htmlFor={ids.diet}>Dietary needs</Label>
        <Input
          id={ids.diet}
          name="bdiet"
          type="text"
          placeholder="e.g. 1 vegetarian, 1 gluten-free, halal default"
        />
      </div>

      <div className="grid gap-2">
        <Label htmlFor={ids.notes}>Anything else?</Label>
        <Textarea
          id={ids.notes}
          name="bnotes"
          placeholder="Occasion (anniversary, birthday, business), preferred menu style, special requests…"
        />
      </div>

      <div className="mt-2 flex flex-wrap items-center gap-4">
        <Button type="submit" size="lg">Send via WhatsApp</Button>
        <span className="font-mono text-[11px] uppercase tracking-[0.18em] text-muted-foreground">
          Opens WhatsApp pre-filled
        </span>
      </div>
    </form>
  );
}
