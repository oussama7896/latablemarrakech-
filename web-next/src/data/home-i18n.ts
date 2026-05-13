// Trilingual content registry for the homepage.
// Every prop-driven component reads from here — keep the shape identical
// across the three locales so a missing string in FR / AR is a hard
// TypeScript error.

export type HomeStrings = {
  layout: {
    title: string;
    description: string;
  };
  hero: {
    eyebrow: string;
    titleLines: [string, string, string];
    tagline: string;
    slate: { label: string; value: string }[];
    bottomTrust: [string, string, string];
    cta: string;
    ghostCta: string;
    scrollLabel: string;
  };
  trusted: {
    caption: string;
    verifiedLabel: string;
    verified: { label: string; value: string }[];
  };
  booking: {
    eyebrow: string;
    headHead: string;
    headEm: string;
    body: string;
    trust: [string, string][];
    whatsapp: string;
    formTitle: string;
    formMeta: string;
    noscriptLine: string;
    footerLine: string;
  };
  intermission: {
    line: string;
    meta: string;
  };
  about: {
    eyebrow: string;
    titleHead: string;
    titleEm: string;
    paragraphs: [string, string];
    pullQuote: string;
    pullQuoteAttribution: string;
    signatureLine: string;
    ctaLabel: string;
    frames: { caption: string; time: string }[];
  };
  menu: {
    eyebrow: string;
    titleHead: string;
    titleEm: string;
    intro: string;
    meta: {
      coursesLabel: string; coursesValue: string;
      serviceLabel: string; serviceValue: string;
      cleanupLabel: string; cleanupValue: string;
      dietLabel: string;    dietValue: string;
    };
    fullMenuCta: string;
    carteEyebrow: string;
    carteSub: string;
    cartePlace: string;
    showMore: string;
    showLess: string;
    chefQuote: string;
    chefAttribution: string;
    courses: { n: string; name: string; body: string; note: string; image: string; imageAlt: string }[];
    moreCourses: { n: string; name: string; body: string; note: string; image: string; imageAlt: string }[];
  };
  testimonials: {
    eyebrow: string;
    rating: string;
    ratingLabel: string;
    headlineHead: string;
    headlineEm: string;
    sub: string;
    readAll: string;
    heroDish: { label: string; href: string };
    quotes: { author: string; context: string; quote: string }[];
  };
  whyus: {
    eyebrow: string;
    titleHead: string;
    titleEm: string;
    intro: string;
    ctaLabel: string;
    reasons: { n: string; eyebrow: string; title: string; body: string }[];
  };
  howto: {
    eyebrow: string;
    titleHead: string;
    titleEm: string;
    titleTail: string;
    ctaLabel: string;
    steps: { n: string; eyebrow: string; title: string; body: string; image?: string; imageAlt?: string; detail: string; poster?: boolean }[];
  };
  faq: {
    eyebrow: string;
    titleHead: string;
    titleEm: string;
    intro: string;
    whatsappCta: string;
    faqs: { q: string; a: string }[];
  };
};

// --------------------------------------------------------------------
// ENGLISH
// --------------------------------------------------------------------
export const en: HomeStrings = {
  layout: {
    title: 'Private Chef Marrakech — Villa Dinners from €85 | La Table Marrakech',
    description: 'A private Moroccan chef at your Marrakech villa or riad. Souk-fresh, multi-course, from €85 per person. 4.9★, 200+ guests. Confirmed in 24h.',
  },
  hero: {
    eyebrow: 'Private chef · Marrakech',
    titleLines: ['A PRIVATE', 'MOROCCAN', 'FEAST.'],
    tagline: '— cooked at your villa tonight.',
    slate: [
      { label: 'Location', value: 'Marrakech · 7 nights / week' },
      { label: 'Courses',  value: 'Five · 3 hours' },
      { label: 'Price',    value: 'From €85 / person' },
      { label: 'Reply',    value: 'Within 1 hour' },
    ],
    bottomTrust: [
      '★ 4.9 · 200+ villa guests',
      'Reply within 1 hour',
      'Confirmed in 24h',
    ],
    cta: 'Book your dinner',
    ghostCta: 'Or message us on WhatsApp',
    scrollLabel: 'Scroll',
  },
  trusted: {
    caption: 'As featured in',
    verifiedLabel: 'Verified',
    verified: [
      { label: 'Google',  value: '4.9 ★ · 200+ guests' },
      { label: 'Villas',  value: '400+ Marrakech evenings' },
      { label: 'Reply',   value: 'Within 1 hour, 7 days' },
      { label: 'Cancel',  value: 'Free up to 72 hours' },
    ],
  },
  booking: {
    eyebrow: 'Book your dinner',
    headHead: 'Three questions. One reply.',
    headEm: '— confirmed in 24 hours.',
    body: 'Date, headcount, anything we should know about your group. We reply within an hour, write your menu the same day, and shop the medina souk the morning of service.',
    trust: [
      ['Reply window', 'Within 1 hour, 7 days a week'],
      ['Confirmation', 'Within 24 hours via WhatsApp'],
      ['Cancellation', 'Free up to 72 hours before — refunded in full'],
      ['Total price', '€85 per person, all-in. No surcharges.'],
    ],
    whatsapp: 'Prefer WhatsApp? Message us directly',
    formTitle: 'Reservation enquiry',
    formMeta: 'No payment now',
    noscriptLine: 'If the form does not load, message us directly on WhatsApp',
    footerLine: 'We never share your details. One reply, from one human.',
  },
  intermission: {
    line: 'Brass lanterns. Steam off the tagine. The room goes quiet.',
    meta: 'Marrakech · Interior · 20:07',
  },
  about: {
    eyebrow: '01 · The chef',
    titleHead: 'Cooked for you.',
    titleEm: '— and no one else.',
    paragraphs: [
      'The medina has a thousand restaurants. None of them know your name, your allergies, your daughter who only eats plain rice, or that it&rsquo;s your anniversary.',
      'A private chef changes the maths. The menu is written for your table. Courses arrive when you&rsquo;re ready, not when the kitchen is. The terrace is yours, the pace is yours, and the only people in the room are people you chose to be there.',
    ],
    pullQuote: 'Tell us what you love, and what you don&rsquo;t. The rest is our job.',
    pullQuoteAttribution: '— the chef, in the kitchen, every time',
    signatureLine: 'Hand-written menus · Souk-fresh · Discreet service',
    ctaLabel: 'Book your dinner',
    frames: [
      { caption: 'At the souk',   time: '06:42' },
      { caption: 'At the stove',  time: '17:18' },
      { caption: 'At your table', time: '20:30' },
    ],
  },
  menu: {
    eyebrow: '02 · The carte',
    titleHead: 'What an evening',
    titleEm: 'tastes like.',
    intro: 'Not the only menu — every dinner is composed for your table. Read this as one example. We&rsquo;ll write yours after the first message.',
    meta: {
      coursesLabel: 'Courses',  coursesValue: 'Five',
      serviceLabel: 'Service',  serviceValue: '2.5 — 3 h',
      cleanupLabel: 'Cleanup',  cleanupValue: 'Included',
      dietLabel: 'Diet',        dietValue: 'All accommodated',
    },
    fullMenuCta: 'See full menu library',
    carteEyebrow: 'La Table · Carte du soir',
    carteSub: 'For two — or for forty.',
    cartePlace: 'Marrakech · 20:00',
    showMore: 'Show 5 more plates',
    showLess: 'Show fewer plates',
    chefQuote: 'Anything here can change. Tell us what you love, and what you don&rsquo;t — the rest is our job.',
    chefAttribution: '— The chef',
    courses: [
      { n: 'I',   name: 'Harira · the Marrakchi opener',                  body: 'Slow-simmered tomato, lentil and lamb broth, sharpened with coriander and a squeeze of lemon. The way Marrakech starts every great meal.', note: 'Starter',         image: '/lt-harira-bowl.jpg',          imageAlt: 'A bowl of harira — Moroccan tomato and lentil soup with lamb, served with lemon and dates' },
      { n: 'II',  name: 'Kefta mkaouara · meatballs and eggs',            body: 'Hand-rolled lamb kefta poached in spiced tomato with cumin and ras-el-hanout. Eggs cracked into the sauce at the last minute, brought to the table still bubbling.', note: 'Mezze · clay',  image: '/lt-kefta-eggs-clay.jpg',      imageAlt: 'Kefta mkaouara — Moroccan meatballs and eggs poached in spiced tomato sauce in a clay dish' },
      { n: 'III', name: 'Pastilla · almond, cinnamon, icing sugar',       body: 'A two-day brick of warqa pastry layered with almond and orange-flower, baked to a deep gold, dusted with cinnamon and icing sugar at the table.', note: 'Signature', image: '/lt-pastilla-silver-tray.jpg',  imageAlt: 'Sweet pastilla on a silver service tray, dusted with icing sugar and toasted almonds' },
      { n: 'IV',  name: 'Tagine of lamb, prunes and toasted almonds',     body: 'Shoulder cooked low for four hours over coals until the meat falls from the bone. Soft prunes, pine-nut crunch, a reduction of ras-el-hanout and Atlas honey.', note: 'Main · 90 min', image: '/lt-lamb-tagine-prunes.jpg',    imageAlt: 'A clay tagine of lamb shoulder with soft prunes and toasted pine nuts' },
      { n: 'V',   name: 'Seffa medfouna · mint tea poured from height',   body: 'Steamed vermicelli, toasted almonds, cinnamon, a small mountain of icing sugar. The traditional Marrakchi close — followed by mint tea from the silver pot.', note: 'Dessert · tea', image: '/lt-seffa-vermicelli.jpg',      imageAlt: 'Seffa medfouna — sweet vermicelli with toasted almonds, cinnamon and powdered sugar' },
    ],
    moreCourses: [
      { n: 'VI', name: 'Couscous royale · seven vegetables', body: 'Friday speciality. Slow-steamed semolina, lamb-and-vegetable broth, seven seasonal vegetables, saffron, raisins — served from an etched copper plate at the centre of the table.', note: 'Friday classic', image: '/lt-couscous-carved-plate.jpg', imageAlt: 'Couscous royale with seven vegetables on a carved Berber serving plate' },
      { n: 'VII', name: 'Rfissa · chicken on shredded msemen and lentils', body: 'Pulled chicken slow-cooked with fenugreek and ras-el-hanout, served over shredded msemen flatbread with lentils. A Marrakchi Sunday on a single plate.', note: 'Sunday classic', image: '/rfissa-chicken-msemen.jpg', imageAlt: 'Rfissa — chicken on shredded msemen with lentils, served on a clay platter' },
      { n: 'VIII', name: 'El Oualidia oysters · shallot mignonette', body: 'Brought up from the Atlantic that morning. Cracked at the table over crushed ice, finished with a sharp shallot vinegar and a turn of black pepper.', note: 'From the Atlantic', image: '/El-Oualidia-Oysters-with-Red-Wine-Vinegar-560x300.png.webp', imageAlt: 'El Oualidia oysters on crushed ice with shallot mignonette' },
      { n: 'IX', name: 'Seafood pastilla · prawn, white fish, chermoula', body: 'Warqa pastry parcels of prawn and white fish bound with chermoula, finished with a squeeze of preserved-lemon. The lighter pastilla.', note: 'Pescatarian', image: '/seafood-pastilla-shrimp.webp', imageAlt: 'Seafood pastilla with white fish and chermoula in warqa pastry' },
      { n: 'X', name: 'Chicken tagine · preserved lemon and olives', body: 'The classic. Free-range chicken braised with confit preserved lemons, green olives, ginger and saffron, finished with fresh coriander.', note: 'House classic', image: '/chicken-tagine-marrakech.webp', imageAlt: 'Chicken tagine with preserved lemon and green olives in a clay tagine' },
    ],
  },
  testimonials: {
    eyebrow: '03 · The guests',
    rating: '4.9',
    ratingLabel: '4.9 / 5 from 200+ guests',
    headlineHead: '4.9 / 5 from',
    headlineEm: '200+ guests',
    sub: 'Real reviews. Real villas. Real Friday-night couscous.',
    readAll: 'Read all reviews',
    heroDish: { label: 'Tasted the pastilla', href: '#menu' },
    quotes: [
      { author: 'Sophie & Marc', context: 'Anniversary · Palmeraie villa', quote: 'The pastilla on night three. Still thinking about it three months later. Our chef made every evening feel like a private celebration.' },
      { author: 'James W.',       context: 'Family stay · Hivernage riad',  quote: "The endive salad with roquefort and cashews to start, then a perfect tagine. Every course was a surprise. The best anniversary dinner we've ever had." },
      { author: 'Anna & Thomas',  context: 'Family of 6 · Atlas valley',    quote: 'The couscous on Friday night was unforgettable. Seven vegetables, slow-cooked lamb, saffron broth — our kids went back for thirds. A real family feast.' },
    ],
  },
  whyus: {
    eyebrow: '04 · The reasons',
    titleHead: 'Six reasons',
    titleEm: 'it lands the way you imagined.',
    intro: 'Anyone can cook a tagine. What you&rsquo;re paying for is the part you don&rsquo;t see — the morning at the souk, the cleanup at midnight, the bottle that fits the second course you didn&rsquo;t expect to love.',
    ctaLabel: 'Book your dinner',
    reasons: [
      { n: 'I',   eyebrow: 'Marrakech-native',         title: 'Chefs who grew up in this kitchen.',       body: 'Born and trained in Marrakech. They know which spice merchant opens at six, which olive press finishes the new oil in November, which farmer brings the best figs.' },
      { n: 'II',  eyebrow: 'Souk-fresh, that morning', title: 'From the souk, not the freezer.',          body: 'Produce, fish, herbs, spices — picked up at the medina souk the day of service. The tagine is built in your kitchen, not transported from a back office.' },
      { n: 'III', eyebrow: 'Villa expertise',          title: 'We know your kitchen already.',            body: 'Tight medina kitchens, fifteen-burner palmeraie galleys, rooftop service with no plumbing — we&rsquo;ve cooked in all of them. We bring what your kitchen lacks.' },
      { n: 'IV',  eyebrow: 'Menus, not templates',     title: 'Your menu is written for your evening.',   body: 'A tasting flight for two, a feast for forty. Dietary needs, allergies, religious requirements, kids who only eat plain rice — all designed in before the chef shops.' },
      { n: 'V',   eyebrow: 'Full hospitality',         title: 'Service, plating, dessert, cleanup.',      body: 'The chef plates each course at the table. A second hand handles drinks and the kitchen reset. You leave the terrace; we leave the villa cleaner than we found it.' },
      { n: 'VI',  eyebrow: 'Discreet luxury',          title: 'No uniforms, no fuss, no upselling.',      body: 'You shouldn&rsquo;t see the logistics. One contact, one quote, one confirmation. The work that should be invisible, is.' },
    ],
  },
  howto: {
    eyebrow: '05 · The flow',
    titleHead: 'From WhatsApp to',
    titleEm: 'first course',
    titleTail: ', in three steps.',
    ctaLabel: 'Book your dinner',
    steps: [
      { n: '01', eyebrow: 'Step one · The message', title: 'Choose your experience.', body: 'Pick your date, number of guests, and any dietary needs. Choose from curated Moroccan menus — tagine, couscous, pastilla, or a full royal feast. Send it via WhatsApp or the form. Confirmation within 24 hours.', image: '', imageAlt: '', detail: 'Reply within an hour · 7 days a week', poster: true },
      { n: '02', eyebrow: 'Step two · The morning', title: 'Your chef arrives.', body: 'Your personal chef shops the medina souk that morning for the freshest ingredients, then arrives at your villa with everything needed — spices, produce, cookware, tableware.', image: '/blue-tagine-moroccan-spices.webp', imageAlt: 'A blue ceramic tagine and Moroccan spices on a souk stall, photographed at first light', detail: 'Souk: 06:30 — 09:00 · Mise en place: 17:00' },
      { n: '03', eyebrow: 'Step three · The evening', title: 'Sit down and enjoy.', body: 'A multi-course Moroccan feast served course by course on your terrace. Appetizers, mains, dessert, traditional mint tea. After the meal, full kitchen, dish, and table cleanup is included.', image: '/lamb-tagine-prunes-almonds.webp', imageAlt: 'A clay tagine of lamb with prunes and toasted almonds, plated on a stone table ready to serve', detail: '4 to 6 courses · 2.5 to 3 hours · We leave the villa cleaner' },
    ],
  },
  faq: {
    eyebrow: '06 · The questions',
    titleHead: 'Before you write,',
    titleEm: 'a few answers.',
    intro: 'The ones we hear most often. If yours isn&rsquo;t here, the fastest reply will always be on WhatsApp — usually within an hour.',
    whatsappCta: 'Still curious? Ask on WhatsApp',
    faqs: [],
  },
};

// --------------------------------------------------------------------
// FRENCH
// --------------------------------------------------------------------
export const fr: HomeStrings = {
  layout: {
    title: 'Chef Privé à Marrakech — Dîners de villa dès 85€ | La Table Marrakech',
    description: 'Un chef marocain privé dans votre villa ou riad de Marrakech. Frais du souk, multi-plats, dès 85€ par personne. 4.9★, 200+ convives. Confirmé en 24h.',
  },
  hero: {
    eyebrow: 'Chef privé · Marrakech',
    titleLines: ['UN FESTIN', 'MAROCAIN', 'PRIVÉ.'],
    tagline: '— cuisiné chez vous ce soir.',
    slate: [
      { label: 'Lieu',     value: 'Marrakech · 7 soirs / sem.' },
      { label: 'Plats',    value: 'Cinq · 3 heures' },
      { label: 'Tarif',    value: 'À partir de 85€ / pers.' },
      { label: 'Réponse',  value: 'Sous 1 heure' },
    ],
    bottomTrust: [
      '★ 4,9 · 200+ convives',
      'Réponse sous 1 h',
      'Confirmé en 24 h',
    ],
    cta: 'Réservez votre dîner',
    ghostCta: 'Ou écrivez-nous sur WhatsApp',
    scrollLabel: 'Défilez',
  },
  trusted: {
    caption: 'Vus dans',
    verifiedLabel: 'Vérifié',
    verified: [
      { label: 'Google',     value: '4,9 ★ · 200+ convives' },
      { label: 'Villas',     value: '400+ soirées à Marrakech' },
      { label: 'Réponse',    value: 'Sous 1 h, 7 jours / 7' },
      { label: 'Annulation', value: 'Gratuite jusqu&rsquo;à 72 h' },
    ],
  },
  booking: {
    eyebrow: 'Réservez votre dîner',
    headHead: 'Trois questions. Une réponse.',
    headEm: '— confirmée en 24 heures.',
    body: 'La date, le nombre de convives, et ce que nous devons savoir sur votre groupe. Nous répondons en moins d&rsquo;une heure, écrivons votre menu le jour même, et passons au souk de la médina le matin du service.',
    trust: [
      ['Délai de réponse', 'Sous 1 heure, 7 jours sur 7'],
      ['Confirmation',     'Sous 24 heures sur WhatsApp'],
      ['Annulation',       'Gratuite jusqu&rsquo;à 72 h avant — remboursée intégralement'],
      ['Tarif total',      '85€ par personne, tout compris. Aucun supplément.'],
    ],
    whatsapp: 'Vous préférez WhatsApp ? Écrivez-nous directement',
    formTitle: 'Demande de réservation',
    formMeta: 'Aucun paiement maintenant',
    noscriptLine: 'Si le formulaire ne charge pas, écrivez-nous sur WhatsApp',
    footerLine: 'Vos coordonnées restent privées. Une réponse, d&rsquo;une seule personne.',
  },
  intermission: {
    line: 'Lanternes de cuivre. Vapeur du tagine. La salle se tait.',
    meta: 'Marrakech · Intérieur · 20:07',
  },
  about: {
    eyebrow: '01 · Le chef',
    titleHead: 'Cuisiné pour vous.',
    titleEm: '— et pour personne d&rsquo;autre.',
    paragraphs: [
      'La médina compte mille restaurants. Aucun ne connaît votre prénom, vos allergies, votre fille qui ne mange que du riz nature, ou que c&rsquo;est votre anniversaire.',
      'Un chef privé change tout. Le menu est écrit pour votre table. Les plats arrivent quand vous êtes prêts, pas quand la cuisine l&rsquo;est. La terrasse est la vôtre, le rythme est le vôtre, et les seules personnes dans la pièce sont celles que vous avez choisies.',
    ],
    pullQuote: 'Dites-nous ce que vous aimez, et ce que vous n&rsquo;aimez pas. Le reste, c&rsquo;est notre métier.',
    pullQuoteAttribution: '— le chef, en cuisine, à chaque fois',
    signatureLine: 'Menus écrits à la main · Frais du souk · Service discret',
    ctaLabel: 'Réservez votre dîner',
    frames: [
      { caption: 'Au souk',          time: '06:42' },
      { caption: 'Au piano',         time: '17:18' },
      { caption: 'À votre table',    time: '20:30' },
    ],
  },
  menu: {
    eyebrow: '02 · La carte',
    titleHead: 'À quoi ressemble',
    titleEm: 'une soirée.',
    intro: 'Ce n&rsquo;est pas le seul menu — chaque dîner est composé pour votre table. Lisez ceci comme un exemple. Le vôtre s&rsquo;écrira après le premier message.',
    meta: {
      coursesLabel: 'Plats',     coursesValue: 'Cinq',
      serviceLabel: 'Service',   serviceValue: '2,5 — 3 h',
      cleanupLabel: 'Nettoyage', cleanupValue: 'Inclus',
      dietLabel: 'Régime',       dietValue: 'Tous accommodés',
    },
    fullMenuCta: 'Voir la bibliothèque de menus',
    carteEyebrow: 'La Table · Carte du soir',
    carteSub: 'Pour deux — ou pour quarante.',
    cartePlace: 'Marrakech · 20:00',
    showMore: 'Voir 5 plats de plus',
    showLess: 'Replier les plats',
    chefQuote: 'Tout ici peut changer. Dites-nous ce que vous aimez, et ce que vous n&rsquo;aimez pas — le reste, c&rsquo;est notre métier.',
    chefAttribution: '— Le chef',
    courses: [
      { n: 'I',   name: 'Harira · l&rsquo;ouverture marrakchie',           body: 'Bouillon mijoté de tomate, lentilles et agneau, relevé de coriandre et d&rsquo;un trait de citron. La manière dont Marrakech commence chaque grand repas.', note: 'Entrée',          image: '/lt-harira-bowl.jpg',          imageAlt: 'Un bol de harira — soupe marocaine à la tomate et aux lentilles avec agneau, servie avec citron et dattes' },
      { n: 'II',  name: 'Kefta mkaouara · boulettes et œufs',              body: 'Boulettes d&rsquo;agneau roulées à la main, pochées dans une tomate épicée au cumin et au ras-el-hanout. Œufs cassés dans la sauce à la dernière minute, servis à table encore frémissants.', note: 'Mezzé · plat en terre', image: '/lt-kefta-eggs-clay.jpg',     imageAlt: 'Kefta mkaouara — boulettes marocaines et œufs pochés dans une sauce tomate épicée dans un plat en terre' },
      { n: 'III', name: 'Pastilla · amande, cannelle, sucre glace',        body: 'Une brique de feuille de warqa montée sur deux jours, amande et fleur d&rsquo;oranger, cuite au four jusqu&rsquo;à un doré profond, saupoudrée de cannelle et de sucre glace à la table.', note: 'Signature',       image: '/lt-pastilla-silver-tray.jpg', imageAlt: 'Pastilla sucrée sur un plateau d&rsquo;argent, saupoudrée de sucre glace et d&rsquo;amandes grillées' },
      { n: 'IV',  name: 'Tagine d&rsquo;agneau, pruneaux et amandes',      body: 'Épaule cuite à feu doux quatre heures sur la braise, jusqu&rsquo;à ce que la viande tombe de l&rsquo;os. Pruneaux fondants, croquant de pignon, réduction de ras-el-hanout et de miel d&rsquo;Atlas.', note: 'Plat · 90 min',  image: '/lt-lamb-tagine-prunes.jpg',  imageAlt: 'Un tagine en terre d&rsquo;épaule d&rsquo;agneau avec pruneaux fondants et pignons grillés' },
      { n: 'V',   name: 'Seffa medfouna · thé à la menthe versé de haut',  body: 'Vermicelles à la vapeur, amandes grillées, cannelle, une petite montagne de sucre glace. La clôture marrakchie traditionnelle — suivie du thé à la menthe versé de la théière d&rsquo;argent.', note: 'Dessert · thé', image: '/lt-seffa-vermicelli.jpg',      imageAlt: 'Seffa medfouna — vermicelles sucrés aux amandes grillées, cannelle et sucre glace' },
    ],
    moreCourses: [
      { n: 'VI',   name: 'Couscous royal · sept légumes',                   body: 'Spécialité du vendredi. Semoule cuite à la vapeur lente, bouillon d&rsquo;agneau et légumes, sept légumes de saison, safran, raisins secs — servi depuis un plat berbère gravé au centre de la table.', note: 'Classique du vendredi', image: '/lt-couscous-carved-plate.jpg',          imageAlt: 'Couscous royal aux sept légumes sur un plat berbère gravé' },
      { n: 'VII',  name: 'Rfissa · poulet sur msemen effiloché et lentilles', body: 'Poulet effiloché mijoté au fenugrec et au ras-el-hanout, servi sur du msemen effiloché et des lentilles. Un dimanche marrakchi sur une seule assiette.', note: 'Classique du dimanche', image: '/rfissa-chicken-msemen.jpg',         imageAlt: 'Rfissa — poulet sur msemen effiloché et lentilles, servi sur un plat en terre' },
      { n: 'VIII', name: 'Huîtres d&rsquo;El Oualidia · mignonette à l&rsquo;échalote', body: 'Remontées de l&rsquo;Atlantique le matin même. Ouvertes à table sur glace pilée, finies au vinaigre d&rsquo;échalote relevé et d&rsquo;un tour de poivre noir.', note: 'De l&rsquo;Atlantique', image: '/El-Oualidia-Oysters-with-Red-Wine-Vinegar-560x300.png.webp', imageAlt: 'Huîtres d&rsquo;El Oualidia sur glace pilée avec mignonette à l&rsquo;échalote' },
      { n: 'IX',   name: 'Pastilla de poisson · crevette, poisson blanc, chermoula', body: 'Petits feuilletés de warqa garnis de crevette et de poisson blanc liés à la chermoula, finis d&rsquo;un trait de citron confit. La pastilla plus légère.', note: 'Pescétarien', image: '/seafood-pastilla-shrimp.webp', imageAlt: 'Pastilla de poisson au poisson blanc et chermoula en pâte warqa' },
      { n: 'X',    name: 'Tagine de poulet · citron confit et olives',     body: 'Le classique. Poulet fermier braisé au citron confit, olives vertes, gingembre et safran, fini à la coriandre fraîche.', note: 'Classique de la maison', image: '/chicken-tagine-marrakech.webp',         imageAlt: 'Tagine de poulet au citron confit et olives vertes dans un tagine en terre' },
    ],
  },
  testimonials: {
    eyebrow: '03 · Les convives',
    rating: '4,9',
    ratingLabel: '4,9 / 5 de plus de 200 convives',
    headlineHead: '4,9 / 5 de',
    headlineEm: 'plus de 200 convives',
    sub: 'Vrais avis. Vraies villas. Vrais couscous du vendredi soir.',
    readAll: 'Lire tous les avis',
    heroDish: { label: 'A goûté la pastilla', href: '#menu' },
    quotes: [
      { author: 'Sophie & Marc', context: 'Anniversaire · Villa palmeraie', quote: 'La pastilla du troisième soir. J&rsquo;y pense encore trois mois plus tard. Notre chef a transformé chaque soirée en célébration intime.' },
      { author: 'James W.',      context: 'Séjour familial · Riad Hivernage', quote: 'La salade d&rsquo;endives au roquefort et noix de cajou pour commencer, puis un tagine parfait. Chaque plat une surprise. Le meilleur dîner d&rsquo;anniversaire qu&rsquo;on ait eu.' },
      { author: 'Anna & Thomas', context: 'Famille de 6 · Vallée de l&rsquo;Atlas', quote: 'Le couscous du vendredi soir, inoubliable. Sept légumes, agneau confit, bouillon au safran — les enfants en ont repris trois fois. Un vrai festin de famille.' },
    ],
  },
  whyus: {
    eyebrow: '04 · Les raisons',
    titleHead: 'Six raisons',
    titleEm: 'pour que la soirée soit celle dont vous rêviez.',
    intro: 'Tout le monde peut cuisiner un tagine. Ce que vous payez, c&rsquo;est la part invisible — le passage au souk au matin, le nettoyage à minuit, la bouteille qui s&rsquo;accorde avec le deuxième plat que vous n&rsquo;attendiez pas.',
    ctaLabel: 'Réservez votre dîner',
    reasons: [
      { n: 'I',   eyebrow: 'Marrakech d&rsquo;origine',     title: 'Des chefs qui ont grandi dans cette cuisine.',    body: 'Nés et formés à Marrakech. Ils savent quel marchand d&rsquo;épices ouvre à six heures, quel moulin termine la nouvelle huile en novembre, quel paysan apporte les meilleures figues.' },
      { n: 'II',  eyebrow: 'Frais du souk, ce matin-là',   title: 'Du souk, pas du congélateur.',                    body: 'Légumes, poisson, herbes, épices — pris au souk de la médina le jour du service. Le tagine est monté dans votre cuisine, pas transporté depuis un labo.' },
      { n: 'III', eyebrow: 'Expérience villa',             title: 'Nous connaissons déjà votre cuisine.',            body: 'Cuisines étroites de la médina, galeries à quinze feux de la palmeraie, service en terrasse sans plomberie — nous avons cuisiné dans toutes. Nous apportons ce qui manque.' },
      { n: 'IV',  eyebrow: 'Menus, pas modèles',           title: 'Votre menu est écrit pour votre soirée.',         body: 'Un menu dégustation pour deux, un festin pour quarante. Régimes, allergies, exigences religieuses, enfants qui ne mangent que du riz nature — tout est intégré avant que le chef ne fasse les courses.' },
      { n: 'V',   eyebrow: 'Hospitalité complète',         title: 'Service, dressage, dessert, nettoyage.',          body: 'Le chef dresse chaque plat à la table. Une deuxième paire de mains gère les boissons et le retour de cuisine. Vous quittez la terrasse ; nous laissons la villa plus propre qu&rsquo;à l&rsquo;arrivée.' },
      { n: 'VI',  eyebrow: 'Luxe discret',                 title: 'Pas d&rsquo;uniformes, pas de fla-fla, pas de ventes additionnelles.', body: 'Vous ne devriez pas voir la logistique. Un contact, un devis, une confirmation. Le travail qui devrait être invisible, l&rsquo;est.' },
    ],
  },
  howto: {
    eyebrow: '05 · Le déroulé',
    titleHead: 'De WhatsApp au',
    titleEm: 'premier plat',
    titleTail: ', en trois étapes.',
    ctaLabel: 'Réservez votre dîner',
    steps: [
      { n: '01', eyebrow: 'Étape un · Le message',   title: 'Choisissez votre soirée.',     body: 'Choisissez la date, le nombre de convives, et tout besoin alimentaire. Choisissez parmi des menus marocains conçus — tagine, couscous, pastilla, ou un festin royal complet. Envoyez via WhatsApp ou le formulaire. Confirmation sous 24 heures.', image: '', imageAlt: '', detail: 'Réponse sous 1 h · 7 jours / 7', poster: true },
      { n: '02', eyebrow: 'Étape deux · Le matin',   title: 'Votre chef arrive.',            body: 'Votre chef privé passe au souk de la médina le matin même pour les ingrédients les plus frais, puis arrive chez vous avec tout le nécessaire — épices, produits, ustensiles, vaisselle.', image: '/blue-tagine-moroccan-spices.webp', imageAlt: 'Un tagine en céramique bleue et des épices marocaines sur un étal du souk, photographiés à l&rsquo;aube', detail: 'Souk : 06:30 — 09:00 · Mise en place : 17:00' },
      { n: '03', eyebrow: 'Étape trois · Le soir',   title: 'Asseyez-vous et profitez.',     body: 'Un festin marocain multi-plats servi plat par plat sur votre terrasse. Entrées, plats, dessert, thé à la menthe traditionnel. Après le repas, le nettoyage complet de la cuisine, de la vaisselle et de la table est inclus.', image: '/lamb-tagine-prunes-almonds.webp', imageAlt: 'Un tagine en terre d&rsquo;agneau aux pruneaux et amandes grillées, dressé sur une table de pierre prêt à servir', detail: '4 à 6 plats · 2,5 à 3 heures · Nous laissons la villa plus propre' },
    ],
  },
  faq: {
    eyebrow: '06 · Les questions',
    titleHead: 'Avant d&rsquo;écrire,',
    titleEm: 'quelques réponses.',
    intro: 'Celles qu&rsquo;on entend le plus souvent. Si la vôtre n&rsquo;y est pas, la réponse la plus rapide sera toujours sur WhatsApp — souvent en moins d&rsquo;une heure.',
    whatsappCta: 'Encore curieux ? Demandez sur WhatsApp',
    faqs: [
      { q: 'Combien coûte un chef privé à Marrakech ?', a: 'À partir de 85€ par personne, tout compris : ingrédients frais du souk, multi-plats, service à table, dessert, thé à la menthe et nettoyage complet de la cuisine, de la vaisselle et de la table. Minimum 2 convives. Pas de supplément caché.' },
      { q: 'Combien de temps à l&rsquo;avance dois-je réserver ?', a: 'Idéalement 7 à 14 jours pour la haute saison (octobre — avril, vacances). Pour de la disponibilité de dernière minute (48 à 72 h), écrivez-nous sur WhatsApp — nous arrivons souvent à arranger ça.' },
      { q: 'Pouvez-vous accommoder les allergies et régimes ?', a: 'Oui. Halal complet par défaut. Végétarien, végan, sans gluten, sans noix, kasher, allergies alimentaires — tout est intégré dans votre menu avant que le chef ne fasse les courses au souk. Précisez-le simplement dans votre demande.' },
      { q: 'Travaillez-vous avec les concierges et planificateurs de mariage ?', a: 'Oui. Tarifs trade pour les concierges de villa, planificateurs de mariage et opérateurs DMC. Écrivez-nous à hello@latablemarrakech.com avec votre demande et votre dossier.' },
      { q: 'Le chef peut-il cuisiner dans n&rsquo;importe quelle villa ?', a: 'Pratiquement toutes. Médina, palmeraie, Hivernage, route de l&rsquo;Ourika, vallée de l&rsquo;Atlas — nous cuisinons dans des cuisines étroites, des galeries à quinze feux, et des terrasses sans plomberie. Nous apportons ce que votre cuisine n&rsquo;a pas.' },
    ],
  },
};

// --------------------------------------------------------------------
// ARABIC (Modern Standard Arabic, RTL)
// --------------------------------------------------------------------
export const ar: HomeStrings = {
  layout: {
    title: 'شيف خاص في مراكش — عشاء فاخر بفيلتك من 85€ للشخص | La Table Marrakech',
    description: 'شيف خاص في مراكش يطبخ وليمة مغربية متعددة الأطباق بفيلتك — طاجين، بسطيلا، كسكس ملكي بمكونات طازجة من السوق. ابتداءً من 85€ للشخص. تأكيد الحجز عبر واتساب خلال 24 ساعة.',
  },
  hero: {
    eyebrow: 'شيف خاص · مراكش',
    titleLines: ['وليمة', 'مغربية', 'خاصة.'],
    tagline: '— تُطبخ في فيلتك الليلة.',
    slate: [
      { label: 'الموقع',  value: 'مراكش · 7 ليالٍ / أسبوع' },
      { label: 'الأطباق', value: 'خمسة · 3 ساعات' },
      { label: 'السعر',   value: 'من 85€ للشخص' },
      { label: 'الرد',    value: 'خلال ساعة' },
    ],
    bottomTrust: [
      '★ 4.9 · أكثر من 200 ضيف',
      'الرد خلال ساعة',
      'تأكيد خلال 24 ساعة',
    ],
    cta: 'احجز عشاءك',
    ghostCta: 'أو راسلنا عبر واتساب',
    scrollLabel: 'مرّر',
  },
  trusted: {
    caption: 'ظهرنا في',
    verifiedLabel: 'موثّق',
    verified: [
      { label: 'Google',  value: '4.9 ★ · 200+ ضيف' },
      { label: 'فيلات',   value: '400+ أمسية في مراكش' },
      { label: 'الرد',    value: 'خلال ساعة، 7 أيام' },
      { label: 'الإلغاء', value: 'مجاني حتى 72 ساعة' },
    ],
  },
  booking: {
    eyebrow: 'احجز عشاءك',
    headHead: 'ثلاثة أسئلة. رد واحد.',
    headEm: '— مؤكَّد خلال 24 ساعة.',
    body: 'التاريخ، عدد الضيوف، وأي شيء يجب أن نعرفه عن مجموعتك. نرد خلال ساعة، نكتب قائمتك في اليوم نفسه، ونمر بسوق المدينة صباح يوم الخدمة.',
    trust: [
      ['موعد الرد',     'خلال ساعة، 7 أيام في الأسبوع'],
      ['التأكيد',       'خلال 24 ساعة عبر واتساب'],
      ['الإلغاء',       'مجاني حتى 72 ساعة قبل الموعد — استرداد كامل'],
      ['السعر الإجمالي', '85€ للشخص، شامل كل شيء. لا رسوم إضافية.'],
    ],
    whatsapp: 'تفضل واتساب؟ راسلنا مباشرة',
    formTitle: 'طلب حجز',
    formMeta: 'لا دفع الآن',
    noscriptLine: 'إذا لم تظهر الاستمارة، راسلنا مباشرة على واتساب',
    footerLine: 'لا نشارك تفاصيلك. رد واحد، من شخص واحد.',
  },
  intermission: {
    line: 'فوانيس نحاسية. بخار الطاجين. تهدأ الغرفة.',
    meta: 'مراكش · داخل · 20:07',
  },
  about: {
    eyebrow: '01 · الشيف',
    titleHead: 'مطبوخ من أجلك.',
    titleEm: '— ولا أحد سواك.',
    paragraphs: [
      'في المدينة ألف مطعم. لا أحد منهم يعرف اسمك، أو حساسياتك، أو ابنتك التي لا تأكل سوى الأرز السادة، أو أن الليلة ذكرى زواجك.',
      'الشيف الخاص يغير المعادلة. القائمة مكتوبة لطاولتك. الأطباق تصل حين تكون مستعداً، لا حين يكون المطبخ كذلك. الشرفة لك، الإيقاع لك، وفي الغرفة فقط من اخترتهم.',
    ],
    pullQuote: 'أخبرنا بما تحبه، وبما لا تحبه. الباقي عملنا.',
    pullQuoteAttribution: '— الشيف، في المطبخ، في كل مرة',
    signatureLine: 'قوائم مكتوبة باليد · طازج من السوق · خدمة هادئة',
    ctaLabel: 'احجز عشاءك',
    frames: [
      { caption: 'في السوق',     time: '06:42' },
      { caption: 'في المطبخ',    time: '17:18' },
      { caption: 'على طاولتك',   time: '20:30' },
    ],
  },
  menu: {
    eyebrow: '02 · القائمة',
    titleHead: 'كيف يكون',
    titleEm: 'طعم الأمسية.',
    intro: 'ليست القائمة الوحيدة — كل عشاء يُكتب لطاولتك. اقرأ هذه كمثال. قائمتك ستُكتب بعد أول رسالة.',
    meta: {
      coursesLabel: 'الأطباق', coursesValue: 'خمسة',
      serviceLabel: 'الخدمة',  serviceValue: '2.5 — 3 ساعات',
      cleanupLabel: 'التنظيف', cleanupValue: 'مشمول',
      dietLabel: 'الحمية',     dietValue: 'كلها مُراعاة',
    },
    fullMenuCta: 'مكتبة القوائم كاملة',
    carteEyebrow: 'La Table · قائمة المساء',
    carteSub: 'لاثنين — أو لأربعين.',
    cartePlace: 'مراكش · 20:00',
    showMore: 'إظهار 5 أطباق إضافية',
    showLess: 'إخفاء الأطباق الإضافية',
    chefQuote: 'كل شيء هنا قابل للتغيير. أخبرنا بما تحبه، وبما لا تحبه — الباقي عملنا.',
    chefAttribution: '— الشيف',
    courses: [
      { n: 'I',   name: 'حريرة · افتتاحية مراكشية', body: 'مرق طماطم وعدس ولحم ضأن مطبوخ على نار هادئة، يُصقَل بالكزبرة وعصرة ليمون. الطريقة التي تبدأ بها مراكش كل وجبة كبرى.', note: 'مقبّل', image: '/lt-harira-bowl.jpg', imageAlt: 'وعاء حريرة — حساء مغربي بالطماطم والعدس واللحم، يُقدَّم مع الليمون والتمر' },
      { n: 'II',  name: 'كفتة مكاورة · كرات لحم وبيض', body: 'كرات لحم ضأن مدحرجة باليد ومسلوقة في طماطم متبّلة بالكمون ورأس الحانوت. تُكسر البيضات في الصلصة في آخر لحظة، وتُحضَر إلى الطاولة لا تزال تغلي.', note: 'مزّة · طاجين', image: '/lt-kefta-eggs-clay.jpg', imageAlt: 'كفتة مكاورة — كرات لحم مغربية وبيض مسلوق في صلصة طماطم متبّلة في طبق طيني' },
      { n: 'III', name: 'بسطيلة · لوز، قرفة، سكر ناعم', body: 'قالب من ورق الورقة محضّر على يومين، طبقات من اللوز وماء الزهر، مخبوز إلى لون ذهبي عميق، يُرشّ بالقرفة والسكر الناعم على الطاولة.', note: 'الطبق المميّز', image: '/lt-pastilla-silver-tray.jpg', imageAlt: 'بسطيلة حلوة على صينية فضية، مرشوشة بالسكر الناعم واللوز المحمّص' },
      { n: 'IV',  name: 'طاجين ضأن، برقوق ولوز محمّص', body: 'كتف مطبوخة ببطء أربع ساعات على الفحم حتى ينفصل اللحم عن العظم. برقوق طري، خشخشة صنوبر، تصفية من رأس الحانوت وعسل الأطلس.', note: 'طبق رئيس · 90 د', image: '/lt-lamb-tagine-prunes.jpg', imageAlt: 'طاجين طيني من كتف الضأن مع برقوق طري وصنوبر محمّص' },
      { n: 'V',   name: 'سفّة مدفونة · شاي بالنعناع يُسكب من عل', body: 'شعيرية مطبوخة بالبخار، لوز محمّص، قرفة، جبل صغير من السكر الناعم. الختام المراكشي التقليدي — يليه شاي بالنعناع من إبريق الفضة.', note: 'حلوى · شاي', image: '/lt-seffa-vermicelli.jpg', imageAlt: 'سفّة مدفونة — شعيرية حلوة باللوز المحمّص، القرفة والسكر الناعم' },
    ],
    moreCourses: [
      { n: 'VI',   name: 'كسكس ملكي · سبع خضار', body: 'تخصص يوم الجمعة. سميد مطبوخ بالبخار البطيء، مرق ضأن وخضار، سبع خضار موسمية، زعفران، زبيب — يُقدَّم في صحن أمازيغي محفور وسط الطاولة.', note: 'كلاسيكية الجمعة', image: '/lt-couscous-carved-plate.jpg', imageAlt: 'كسكس ملكي بسبع خضار على صحن أمازيغي محفور' },
      { n: 'VII',  name: 'رفيسة · دجاج على مسمن مفتوت وعدس', body: 'دجاج مفتوت مطبوخ ببطء بالحلبة ورأس الحانوت، يُقدَّم فوق مسمن مفتوت مع العدس. يوم أحد مراكشي في طبق واحد.', note: 'كلاسيكية الأحد', image: '/rfissa-chicken-msemen.jpg', imageAlt: 'رفيسة — دجاج على مسمن مفتوت مع عدس، تُقدَّم على صحن طيني' },
      { n: 'VIII', name: 'محار الوليدية · صلصة كراث', body: 'يُحضَر من الأطلسي في الصباح. يُفتح على الطاولة فوق ثلج مجروش، يُتمّ بخل الكراث الحاد ودورة فلفل أسود.', note: 'من الأطلسي', image: '/El-Oualidia-Oysters-with-Red-Wine-Vinegar-560x300.png.webp', imageAlt: 'محار الوليدية على ثلج مجروش مع صلصة كراث' },
      { n: 'IX',   name: 'بسطيلة بحرية · جمبري، سمك أبيض، شرمولة', body: 'لفائف ورق ورقة بحشوة جمبري وسمك أبيض مع شرمولة، تُتمّ بعصرة من الليمون المخلّل. البسطيلة الأخف.', note: 'بحري', image: '/seafood-pastilla-shrimp.webp', imageAlt: 'بسطيلة بحرية بالسمك الأبيض والشرمولة في عجين ورقة' },
      { n: 'X',    name: 'طاجين دجاج · ليمون مخلّل وزيتون', body: 'الكلاسيك. دجاج بلدي مطهو بالليمون المخلّل والزيتون الأخضر، الزنجبيل والزعفران، يُتمّ بالكزبرة الطازجة.', note: 'كلاسيكية البيت', image: '/chicken-tagine-marrakech.webp', imageAlt: 'طاجين دجاج بالليمون المخلّل والزيتون الأخضر في طاجين طيني' },
    ],
  },
  testimonials: {
    eyebrow: '03 · الضيوف',
    rating: '4.9',
    ratingLabel: '4.9 / 5 من أكثر من 200 ضيف',
    headlineHead: '4.9 / 5 من',
    headlineEm: 'أكثر من 200 ضيف',
    sub: 'تقييمات حقيقية. فيلات حقيقية. كسكس حقيقي ليلة الجمعة.',
    readAll: 'اقرأ كل التقييمات',
    heroDish: { label: 'ذاقا البسطيلة', href: '#menu' },
    quotes: [
      { author: 'صوفي ومارك', context: 'ذكرى زواج · فيلا بالبامرايا', quote: 'بسطيلة الليلة الثالثة. لا أزال أفكر فيها بعد ثلاثة أشهر. شيفنا حوّل كل أمسية إلى احتفال خاص.' },
      { author: 'جيمس و.',   context: 'إقامة عائلية · رياض الهيفرناج', quote: 'سلطة هندباء بالروكفور والكاجو للبدء، ثم طاجين متقن. كل طبق كان مفاجأة. أفضل عشاء ذكرى زواج تذوقناه.' },
      { author: 'آنا وتوماس', context: 'عائلة من 6 · وادي الأطلس', quote: 'كسكس ليلة الجمعة لا يُنسى. سبع خضار، ضأن بطيء الطهي، مرق زعفران — أطفالنا طلبوا الإعادة ثلاث مرات. وليمة عائلية حقيقية.' },
    ],
  },
  whyus: {
    eyebrow: '04 · الأسباب',
    titleHead: 'ستة أسباب',
    titleEm: 'تجعلها بالضبط كما تخيّلتها.',
    intro: 'أي أحد يقدر يطبخ طاجين. اللي تدفع مقابله هو الجزء اللي ما تشوفوش — صباح السوق، تنظيف منتصف الليل، الزجاجة اللي تليق بالطبق الثاني اللي ما توقّعت أن تحبّه.',
    ctaLabel: 'احجز عشاءك',
    reasons: [
      { n: 'I',   eyebrow: 'مراكش بالأصل',          title: 'شيوف نشأوا في هذا المطبخ.',          body: 'وُلدوا وتدرّبوا في مراكش. يعرفون أي تاجر بهارات يفتح في السادسة، أي معصرة تنهي زيت موسم نونبر، أي فلاح يجلب أفضل التين.' },
      { n: 'II',  eyebrow: 'طازج من السوق، صباحاً',  title: 'من السوق، لا من الفريزر.',           body: 'خضار، سمك، أعشاب، بهارات — تُجلب من سوق المدينة يوم الخدمة. الطاجين يُبنى في مطبخك، لا يُنقل من مختبر خلفي.' },
      { n: 'III', eyebrow: 'خبرة الفيلات',           title: 'نعرف مطبخك سلفاً.',                   body: 'مطابخ ضيقة في المدينة، مطابخ بخمسة عشر موقداً في البامرايا، خدمة على السطح بلا سباكة — طبخنا في كلها. نأتي بما ينقص مطبخك.' },
      { n: 'IV',  eyebrow: 'قوائم، لا قوالب',        title: 'قائمتك مكتوبة لأمسيتك.',              body: 'وجبة تذوّق لاثنين، وليمة لأربعين. حميات، حساسيات، اشتراطات دينية، أطفال لا يأكلون سوى الأرز السادة — كلها مُدمَجة قبل أن يتسوق الشيف.' },
      { n: 'V',   eyebrow: 'ضيافة كاملة',           title: 'خدمة، تقديم، حلوى، تنظيف.',           body: 'الشيف يقدّم كل طبق على الطاولة. يد ثانية تتولى المشروبات وإعادة ترتيب المطبخ. أنتم تتركون الشرفة؛ نحن نترك الفيلا أنظف مما وجدناها.' },
      { n: 'VI',  eyebrow: 'فخامة هادئة',           title: 'لا أزياء رسمية، لا ضوضاء، لا بيع زائد.', body: 'لا ينبغي أن ترى اللوجستيك. جهة اتصال واحدة، عرض سعر واحد، تأكيد واحد. العمل الذي ينبغي أن يكون خفياً، يكون.' },
    ],
  },
  howto: {
    eyebrow: '05 · السير',
    titleHead: 'من واتساب إلى',
    titleEm: 'الطبق الأول',
    titleTail: ' في ثلاث خطوات.',
    ctaLabel: 'احجز عشاءك',
    steps: [
      { n: '01', eyebrow: 'الخطوة الأولى · الرسالة', title: 'اختر أمسيتك.', body: 'اختر التاريخ، عدد الضيوف، وأي احتياجات غذائية. اختر من قوائم مغربية مُعدّة — طاجين، كسكس، بسطيلة، أو وليمة ملكية كاملة. أرسل عبر واتساب أو الاستمارة. تأكيد خلال 24 ساعة.', image: '', imageAlt: '', detail: 'الرد خلال ساعة · 7 أيام في الأسبوع', poster: true },
      { n: '02', eyebrow: 'الخطوة الثانية · الصباح',  title: 'يصل شيفك.', body: 'شيفك الخاص يمر بسوق المدينة صباح ذلك اليوم لأفضل المكونات، ثم يصل إلى فيلتك ومعه كل ما يحتاجه — بهارات، خضار، أدوات طهي، أواني تقديم.', image: '/blue-tagine-moroccan-spices.webp', imageAlt: 'طاجين خزفي أزرق وبهارات مغربية على واجهة سوق، مصوّرة عند بزوغ الفجر', detail: 'السوق: 06:30 — 09:00 · التحضير: 17:00' },
      { n: '03', eyebrow: 'الخطوة الثالثة · المساء', title: 'اجلس واستمتع.', body: 'وليمة مغربية متعددة الأطباق تُقدَّم طبقاً طبقاً على شرفتك. مقبّلات، أطباق رئيسية، حلوى، شاي بالنعناع التقليدي. بعد الوجبة، تنظيف كامل للمطبخ والأطباق والطاولة مشمول.', image: '/lamb-tagine-prunes-almonds.webp', imageAlt: 'طاجين طيني من ضأن مع برقوق ولوز محمّص، مُقدَّم على طاولة حجرية جاهز للأكل', detail: '4 إلى 6 أطباق · 2.5 إلى 3 ساعات · نترك الفيلا أنظف' },
    ],
  },
  faq: {
    eyebrow: '06 · الأسئلة',
    titleHead: 'قبل أن تكتب،',
    titleEm: 'بعض الأجوبة.',
    intro: 'الأكثر شيوعاً. إن لم يكن سؤالك هنا، فأسرع رد سيكون دائماً عبر واتساب — عادةً خلال ساعة.',
    whatsappCta: 'لا تزال فضولياً؟ اسأل عبر واتساب',
    faqs: [
      { q: 'كم يكلّف شيف خاص في مراكش؟', a: 'من 85€ للشخص، شامل كل شيء: مكونات طازجة من السوق، أطباق متعددة، خدمة على الطاولة، حلوى، شاي بالنعناع وتنظيف كامل للمطبخ والأطباق والطاولة. الحد الأدنى ضيفان. لا رسوم خفية.' },
      { q: 'كم من الوقت يجب أن أحجز مسبقاً؟', a: 'مثالياً 7 إلى 14 يوماً للموسم العالي (أكتوبر — أبريل، العطل). للتوافر في آخر لحظة (48 إلى 72 ساعة)، راسلنا على واتساب — كثيراً ما نتمكن من ترتيب الأمر.' },
      { q: 'هل تراعون الحساسيات والحميات؟', a: 'نعم. حلال بالكامل افتراضياً. نباتي، نباتي صرف، خالٍ من الجلوتين، خالٍ من المكسرات، كوشير، حساسيات غذائية — كلها مُدمَجة في قائمتك قبل أن يتسوق الشيف من السوق. يكفي أن تذكرها في طلبك.' },
      { q: 'هل تعملون مع منظمي الزفاف والكونسيرج؟', a: 'نعم. أسعار خاصة بالقطاع لكونسيرج الفيلات، منظمي الزفاف ومشغّلي DMC. راسلنا على hello@latablemarrakech.com بطلبك وملف عميلك.' },
      { q: 'هل يستطيع الشيف الطهي في أي فيلا؟', a: 'تقريباً كلها. المدينة، البامرايا، الهيفرناج، طريق أوريكا، وادي الأطلس — نطبخ في مطابخ ضيقة، مطابخ بخمسة عشر موقداً، وشرفات بلا سباكة. نأتي بما ينقص مطبخك.' },
    ],
  },
};

// Fill EN faqs from the existing JSON to avoid duplicating the source of
// truth — the JSON-LD on the homepage reads from the same file.
import enFaqsJson from '@/data/home-faqs.json';
en.faq.faqs = enFaqsJson as { q: string; a: string }[];

export const home = { en, fr, ar } as const;
export type HomeLang = keyof typeof home;
