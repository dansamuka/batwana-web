# Batwana — website

An overhaul of the single-page Batwana site. One self-contained `index.html`,
no build step, no dependencies. Open it and it works.

**Full review of what changed and why: [`docs/OVERHAUL.md`](docs/OVERHAUL.md).**

---

## Deploy

Drop these at the root of the `batwana-web` repo, on whichever branch GitHub Pages
serves, and push.

```
index.html          the whole site
404.html            branded not-found page
favicon.ico         .png
site.webmanifest    robots.txt   sitemap.xml   .nojekyll
assets/
  logo/             lockups and app icons, derived from the source PNG
  splat/            section dividers, clip-path masks, the three splats
  photos/           placeholder slots — replace with real photography
  og-image.png      1200×630 share card
docs/
  OVERHAUL.md       the review
  brand-logo-source.png
```

Every path is **relative**, so the site works under the `/batwana-web/` project
subpath. Do not change them to root-absolute (`/assets/...`) — that breaks
GitHub Pages project sites.

`.nojekyll` stops GitHub from running Jekyll over the folder.

## Preview locally

```bash
python3 -m http.server 8000     # then open http://localhost:8000
```

## Editing

Everything lives in one file, in this order:

1. `<head>` — title, description, canonical, OG tags, icons, fonts
2. `<style>` — tokens first, then components, in the order they appear on the page
3. the page itself, section by section
4. two `application/ld+json` blocks — `LocalBusiness` and `FAQPage`
5. one `<script>` — header state, drawer, ripple, sticky bar, copyright year

**If you change a price, change it in three places:** the card, the FAQ answer,
and the `hasOfferCatalog` block in the `LocalBusiness` schema. Search for the
figure and you will find all three.

**If you change the phone number or email**, search for `254702876305` and
`batwanakenyaltd@gmail.com` — they appear in the WhatsApp deep links, the
`tel:`/`mailto:` links, the contact cards, the footer and the schema.

## Two things worth knowing

**Splat dividers need two classes.** A divider paints the incoming section's
colour as the shape over the outgoing section's colour as the background:

```html
<div class="divider to-paper from-deep">   <!-- white splat over indigo -->
```

Set only `to-*` and a white splat lands on a white page and vanishes.

**Pink and red never carry small text.** Measured at 3.37:1 and 3.83:1 against
indigo, both fail AA for body copy. They are shape colours. Every button is
ink on yellow, at 9.9:1.

## Outstanding

- Replace `assets/photos/*-slot.svg` with real photographs — written parental
  consent required for any identifiable child
- Confirm the prices against the real rate card
- Commission a vector logo with the three splats as separate paths
- Verify the insurance and safety claims before publishing them

---

© Batwana Kenya Limited.
