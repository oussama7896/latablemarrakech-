// SEO + structured data shapes for Layout.astro.
// Keep additive — fields are optional so pages opt in only to what they need.

export type Hreflang = {
  hreflang: string;       // e.g. "en", "fr", "ar", "x-default"
  href: string;           // absolute URL
};

export type SeoProps = {
  title: string;
  description: string;
  canonical: string;          // absolute URL
  ogImage?: string;           // absolute URL — defaults to brand OG
  ogLocale?: string;          // e.g. "en_US"
  ogLocaleAlternates?: string[];
  twitterTitle?: string;      // falls back to title
  twitterDescription?: string;// falls back to description
  htmlLang?: string;          // e.g. "en", "fr", "ar"
  htmlDir?: 'ltr' | 'rtl';
  robots?: string;            // defaults to standard SEO-friendly value
  hreflang?: Hreflang[];
  // Pre-stringified JSON-LD blocks. Each entry becomes one <script type="application/ld+json">.
  jsonLd?: Array<Record<string, unknown>>;
  // Optional preload hints (e.g. hero image)
  preloadImages?: Array<{ href: string; type?: string; fetchpriority?: 'high' | 'low' | 'auto' }>;
};

export const BRAND = {
  ga4Id: 'G-J2QTMMMYLD',
  adsId: 'AW-18017405402',
  ogImage: 'https://latablemarrakech.com/la-table-marrakech-og.png',
  themeColor: '#080604',
  geoRegion: 'MA-07',
  geoPlacename: 'Marrakech',
  geoPosition: '31.6295;-7.9811',
  geoIcbm: '31.6295, -7.9811',
} as const;
