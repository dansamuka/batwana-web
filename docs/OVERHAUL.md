# Batwana site overhaul

A review of `dansamuka.github.io/batwana-web` as deployed, and what this version changes.
I read the source from `raw.githubusercontent.com` rather than judging the rendered page,
so everything below is a code-level finding.

---

## 1. What the deployed site got right

Worth stating first, because the overhaul keeps all of it:

- **One self-contained `index.html`.** No dependencies, no build step, no framework. For a
  business with no booking engine, this is the correct architecture. It will still work in
  three years with nobody maintaining it.
- **`<details>` for the FAQ.** Native disclosure gives keyboard operation, screen-reader
  semantics and in-page find-on-page for free. Most sites reimplement this badly in JS.
- **`lang="en-KE"`, a skip link, `aria-expanded` on the menu toggle.** Small things, often missed.
- **The palette and the Baloo 2 / Figtree pairing** carried over intact.
- **Fluid type with `clamp()`** rather than a stack of breakpoint overrides.

---

## 2. What was wrong

### 2.1 The logo is not on the website

The mark was a letter in a box:

```html
<a class="brand" href="#top"><span class="brand-mark">B</span>Batwana</a>
```

Two consequences. It renders as **“BBatwana”**, which reads as a typo, in both the header
and the footer. And Batwana owns a distinctive paint-splat mark that appears nowhere on
its own site. That mark is the single asset in this brand that no competitor can copy.

There were also **zero images on the entire page**, and the only iconography was three
emoji — 🎈 ✨ 🎡 — which render as different artwork on every operating system and read as
unfinished on a business site.

### 2.2 The strategic reversal

Three things were removed that were the whole competitive argument:

| Removed | Why it mattered |
|---|---|
| **Prices** | Replaced with “confirmed with you before booking”. Every competitor in Nairobi makes a parent WhatsApp for a quote. Publishing a number was the differentiator, and the site gave it up. |
| **Safety numbers** | “Crew are assigned to inflatables, water play, rides and games based on the activity” is an adjective. “One crew member per inflatable, one per five children on water play” is a commitment a school head or mall compliance officer can test. |
| **Equipment specifics** | Footprint in metres and power draw are what actually decide whether a parent’s compound works. Nobody in this market publishes them. |

### 2.3 Technical gaps

- **No favicon, no Open Graph tags, no canonical, no JSON-LD, no sitemap, no 404 page.**
  Sharing the link on WhatsApp — the single most likely way this site gets distributed —
  produced a bare URL with no image, title card or description.
- **`scroll-behavior:smooth` with no `prefers-reduced-motion` guard.** Smooth scroll is a
  vestibular trigger. The CSS contained no `prefers-reduced-motion` block at all.
- **No focus styles.** The word `outline` did not appear in the stylesheet.
- **Mobile menu had no focus trap and no Escape handler.** Once opened with a keyboard,
  tab focus escaped behind the overlay.
- **Seven font faces** loaded (Baloo 2 at 600/700/800, Figtree at 400/500/600/700) where
  four are used.
- **A dead link**: “Based in Nairobi, Kenya” pointed at `href="#"`.

---

## 3. What changed

### 3.1 The brand is now on the site

Everything visual was derived programmatically from `docs/brand-logo-source.png`:

- **A reversed lockup** — white wordmark, splats untouched — for the indigo header and footer.
  Near-white pixels became transparent, wordmark pixels were recoloured, splat pixels left alone.
- **The three splats extracted individually by hue**, since the red and amber overlap and a
  connected-component pass merged them. They live in `assets/splat/mark-*.png` and are
  available for future use.
- **A favicon set** (`.ico` at 16/32/48, PNG at 32/180/512, plus a maskable 512 on an indigo field).
- **A 1200×630 Open Graph image**, so a WhatsApp or Facebook share now shows the brand.

Emoji are gone. Icons are inline SVG at a consistent 2px stroke.

### 3.2 The splat became a system, not an ornament

Six **section dividers** carry an irregular wet edge with detached droplets, alternating
shape so no two adjacent bands repeat.

One implementation note worth keeping, because it is the bug that made them invisible in the
first draft: a divider paints the **incoming** section’s colour as the shape, over the
**outgoing** section’s colour as the background. Set only the shape colour and a white splat
sits on a white page and disappears. Hence the paired classes:

```html
<div class="divider to-paper from-deep">   <!-- white splat over indigo -->
<div class="divider to-dark from-paper">   <!-- indigo splat over white -->
```

Clip-path masks (`#m1`–`#m3`) are defined for splat-shaped photography, with a rounded-rectangle
fallback via `@supports`, ready for when real images arrive.

### 3.3 Substance restored

- **Prices back on the cards**, each with a spec strip showing children / hours / crew, plus
  the per-extra-child rate and the travel band included.
- **A “what moves the price” table** — distance, hours, headcount, power, ground conditions,
  water access. Stating the whole list is more persuasive than hiding it.
- **An equipment table** giving ages, space in metres, power draw and capacity for nine units.
  This is the strongest content on the page and the thing no competitor publishes.
- **Safety as four published ratios** — 1:1 per inflatable, 1:5 on water, inspected twice,
  1:20 on games — set as large figures rather than prose.
- **Three named commercial models** in the partners section, because the two questions a
  leasing manager asks in the first meeting are who funds the capital cost and how revenue
  splits. Answering them on the page shortens the sales cycle.
- **Nine FAQ answers** rewritten to carry the actual numbers, including the cancellation ladder.

### 3.4 Technical

| Area | Change |
|---|---|
| Social | Canonical, full OG set, `twitter:card`, 1200×630 image |
| Structured data | `LocalBusiness` with hours, area served, price range and an offer catalogue; `FAQPage` with six questions |
| Discovery | `sitemap.xml`, `robots.txt`, `site.webmanifest`, `.nojekyll`, a branded `404.html` |
| Motion | `prefers-reduced-motion` now disables animation, transitions **and** `scroll-behavior` |
| Focus | 3px yellow ring at 2px offset, legible on both light and dark surfaces |
| Menu | Focus trap, Escape to close, focus returned to the trigger on close |
| Fonts | Four faces instead of seven, with `preload` on the stylesheet |
| Targets | Nav links raised to a 44px minimum |
| Links | Dead `href="#"` replaced with real content |
| Year | Copyright year set from `Date`, so it can never go stale |

### 3.5 Two design calls worth explaining

**The hero splat cluster was removed.** The first draft placed the three splats in the top-right
of the hero. They sat about 100px below the same mark in the header — repeating a logo twice on
one screen is duplication, not craft. The page-load moment now belongs to the headline itself:
a 14px rise with a 70ms stagger across headline, subhead, buttons and proof strip, played once
per session and switched off entirely under reduced motion.

**A three-line proof strip sits under the hero CTAs.** “From KES 35,000 · 1 crew member on every
inflatable · 1 working day to reply” puts the price, the safety commitment and the response
promise above the fold, where the three objections actually live.

---

## 4. Verified, not assumed

Rendered headlessly at 1440×900 and 390×844:

- No horizontal overflow at either width
- Exactly one `h1`, no heading-order skips
- Every local reference resolves; no `href="#"` remaining
- Both JSON-LD blocks parse
- **14.8 KB gzipped** for the whole page
- Zero contrast pairs below AA — measured, not eyeballed

| Pair | Ratio |
|---|---|
| Ink on white | 15.69 |
| White on indigo-900 | 13.82 |
| White on indigo-700 | 10.91 |
| **Ink on yellow (every button)** | **9.90** |
| Yellow on indigo-700 | 6.89 |
| Muted white on indigo | 6.50 |

Pink (3.37:1) and red (3.83:1) fail AA for body text, so they are used only as shape colours
and never carry small text. That is a rule, not a preference.

Three bugs surfaced during rendering and were fixed:

1. Dividers invisible on light-to-dark transitions — the shape colour matched the page background.
2. The hero proof strip stacking one item per line — it is a `<p>`, and the global
   `p{max-width:66ch}` was constraining a flex row.
3. Images stretched vertically — an `<img>` `height` attribute is a presentational hint that
   still applies when CSS sets only `width`. Fixed with a global `img{height:auto}`.

The site was also rendered with Google Fonts blocked. It holds up on the system fallback stack,
which is the state a first-time visitor on poor mobile data actually sees.

---

## 5. Before this goes live

**Prices.** These are the figures from the specification, not confirmed by the business. Check
them against the real rate card before publishing. The footer already carries the honest caveat:
*“Prices are indicative and confirmed in writing before payment.”* If you decide the market is
not ready for published prices, remove the three `.price` blocks and the FAQ answer — but the
recommendation is to keep them. It is the one move competitors cannot easily copy, because
copying it means committing to a number.

**Photography.** Every `assets/photos/*-slot.svg` is a labelled placeholder. Real photographs
from real Batwana events are the largest single improvement still available. Written parental
consent before any identifiable child is published, filed against the specific image.

**A vector logo.** Every mark on this site is derived from a 192×113 raster, so the large icons
are upscaled. An SVG lockup with the three splats as separate paths would sharpen the icons and
reopen the staggered splat animation.

**Claims to verify.** Insurance cover is described as in force; the ratios, inspection routine
and incident reporting are stated as fact. Publish only what the business actually staffs to.

**Legal.** There are no forms on this page, so no personal data is collected by the site itself
and the Kenya Data Protection Act exposure is low. That changes the moment a form appears.
A privacy notice and a child safeguarding policy are worth having regardless — schools and mall
compliance officers ask for both.
