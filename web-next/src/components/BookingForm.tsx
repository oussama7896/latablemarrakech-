/**
 * BookingForm — React island. Renders the homepage booking form using shadcn
 * primitives and the EXACT same tracking attributes as the static site:
 *
 *   <form id="booking-home" data-track-form="booking-enquiry" data-form-id="booking-home">
 *     <input name="bname"/> <input name="bemail"/> <input name="bdate"/>
 *     <select name="bguests"/> <select name="btime"/> <textarea name="bnotes"/>
 *
 * Submission opens WhatsApp pre-filled with the enquiry, identical to the
 * static-site behaviour. The global PERF:ANALYTICS-RICH listener (in Layout)
 * fires booking_enquiry_submit independently — no need to call gtag here.
 */

import { useId, useState, type FormEvent } from 'react';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Select, SelectContent, SelectItem, SelectTrigger, SelectValue,
} from '@/components/ui/select';
import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';

const WHATSAPP = '212721354757';

const GUEST_OPTIONS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', '12', '15', '20', '25', '30+'];
const TIME_OPTIONS = [
  '08:00 - Breakfast', '09:00 - Breakfast', '10:00 - Brunch', '11:00 - Brunch',
  '12:00 - Lunch', '13:00 - Lunch',
  '18:00 - Dinner', '19:00 - Dinner', '20:00 - Dinner', '21:00 - Dinner',
];

export function BookingForm() {
  const today = new Date().toISOString().slice(0, 10);
  const [guests, setGuests] = useState('6');
  const [time, setTime] = useState('20:00 - Dinner');
  const ids = {
    name: useId(), email: useId(), date: useId(), notes: useId(),
  };

  function onSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const f = e.currentTarget;
    const data = new FormData(f);
    const lines = [
      'Booking Request:',
      `Name: ${data.get('bname') || ''}`,
      `Email: ${data.get('bemail') || ''}`,
      `Date: ${data.get('bdate') || ''}`,
      `Time: ${data.get('btime') || ''}`,
      `Guests: ${data.get('bguests') || ''}`,
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
      id="booking-home"
      data-track-form="booking-enquiry"
      data-form-id="booking-home"
      onSubmit={onSubmit}
      className="grid gap-4 sm:grid-cols-2"
    >
      <div className="grid gap-2 sm:col-span-1">
        <Label htmlFor={ids.name}>Your name</Label>
        <Input id={ids.name} name="bname" type="text" placeholder="First and last name" required />
      </div>

      <div className="grid gap-2 sm:col-span-1">
        <Label htmlFor={ids.email}>Email</Label>
        <Input id={ids.email} name="bemail" type="email" placeholder="email@example.com" required />
      </div>

      <div className="grid gap-2 sm:col-span-1">
        <Label htmlFor="bguests">Number of guests</Label>
        {/* Hidden native input keeps name="bguests" so the analytics listener
            picks up group_size without us writing any extra code. */}
        <input type="hidden" name="bguests" value={guests} />
        <Select value={guests} onValueChange={setGuests}>
          <SelectTrigger id="bguests"><SelectValue /></SelectTrigger>
          <SelectContent>
            {GUEST_OPTIONS.map((n) => (<SelectItem key={n} value={n}>{n}</SelectItem>))}
          </SelectContent>
        </Select>
      </div>

      <div className="grid gap-2 sm:col-span-1">
        <Label htmlFor={ids.date}>Preferred date</Label>
        <Input id={ids.date} name="bdate" type="date" min={today} required />
      </div>

      <div className="grid gap-2 sm:col-span-2">
        <Label htmlFor="btime">Preferred time</Label>
        <input type="hidden" name="btime" value={time} />
        <Select value={time} onValueChange={setTime}>
          <SelectTrigger id="btime"><SelectValue /></SelectTrigger>
          <SelectContent>
            {TIME_OPTIONS.map((t) => (<SelectItem key={t} value={t}>{t}</SelectItem>))}
          </SelectContent>
        </Select>
      </div>

      <div className="grid gap-2 sm:col-span-2">
        <Label htmlFor={ids.notes}>Special requests or allergies</Label>
        <Textarea
          id={ids.notes}
          name="bnotes"
          placeholder="Anniversary, birthday, dietary needs, anything we should know."
        />
      </div>

      <div className="grid gap-2 sm:col-span-2">
        <Button type="submit" size="lg" className="w-full">
          Send booking request via WhatsApp
        </Button>
        <p className="text-center text-[10px] tracking-widest uppercase text-muted-foreground">
          We confirm within 24 hours · Minimum 2 guests · 72h notice
        </p>
      </div>
    </form>
  );
}
