#!/usr/bin/env python3
"""One-time Batwana hero migration.

- Extract the four supplied photos currently embedded in the first four occasion SVGs.
- Save them as dedicated WebP hero assets.
- Restore the occasion-card artwork from the pre-photo commit.
- Replace the scroll-sequence/illustrated top act with a full-bleed, seamless photo hero.
"""
from __future__ import annotations

import base64
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
BASE_COMMIT = "d5d286dcc0dbbb280dfead29822ed6adafbff7ae"

SLOTS = [
    ("assets/photos/party-slot.svg", "assets/photos/hero-01.webp"),
    ("assets/photos/school-slot.svg", "assets/photos/hero-02.webp"),
    ("assets/photos/corporate-slot.svg", "assets/photos/hero-03.webp"),
    ("assets/photos/crew-slot.svg", "assets/photos/hero-04.webp"),
]


def extract_photo(svg_path: Path, out_path: Path) -> None:
    text = svg_path.read_text(encoding="utf-8")
    match = re.search(r"data:image/webp;base64,([A-Za-z0-9+/=]+)", text)
    if not match:
        raise RuntimeError(f"No embedded WebP found in {svg_path}")
    out_path.write_bytes(base64.b64decode(match.group(1)))


def restore_from_commit(rel_path: str) -> None:
    data = subprocess.check_output(
        ["git", "show", f"{BASE_COMMIT}:{rel_path}"], cwd=ROOT
    )
    (ROOT / rel_path).write_bytes(data)


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        if new in text:
            return text
        raise RuntimeError(f"Could not locate {label}")
    return text.replace(old, new, 1)


def main() -> None:
    # Preserve the supplied images as real, directly-loadable hero assets first.
    for slot, hero in SLOTS:
        extract_photo(ROOT / slot, ROOT / hero)

    # Put the occasion cards back exactly as they were before the accidental update.
    for slot, _ in SLOTS:
        restore_from_commit(slot)

    html = INDEX.read_text(encoding="utf-8")

    html = replace_once(
        html,
        '.act{display:none}\n[data-tier="coarse"] .act,[data-tier="full"] .act{display:block}\n[data-tier="coarse"] .hero,[data-tier="full"] .hero{display:none}',
        '.act{display:none!important}',
        "scroll-act visibility rules",
    )

    old_hero_css = '''.hero{
  position:relative;display:flex;align-items:flex-end;
  min-height:min(90svh,780px);padding-top:calc(var(--header-h) + 56px);padding-bottom:clamp(56px,8vw,104px);
  background:var(--indigo-900);color:#fff;overflow:hidden
}
.hero__bg{position:absolute;inset:0}
.hero__bg img{width:100%;height:100%;object-fit:cover}
.hero__bg::after{content:"";position:absolute;inset:0;background:linear-gradient(175deg,rgba(42,34,102,.62),rgba(42,34,102,.9))}'''

    new_hero_css = '''.hero{
  position:relative;display:flex;align-items:flex-end;
  min-height:100svh;padding-top:calc(var(--header-h) + 56px);padding-bottom:clamp(72px,9vw,112px);
  background:var(--indigo-900);color:#fff;overflow:hidden
}
.hero__bg{position:absolute;inset:0;background:var(--indigo-900)}
.hero__slide{
  position:absolute;inset:0;width:100%;height:100%;object-fit:cover;
  opacity:0;transform:scale(1.045);will-change:opacity,transform;
  animation:heroCrossfade 24s linear infinite
}
.hero__slide:nth-child(1){animation-delay:0s}
.hero__slide:nth-child(2){animation-delay:6s}
.hero__slide:nth-child(3){animation-delay:12s}
.hero__slide:nth-child(4){animation-delay:18s}
.hero__bg::after{
  content:"";position:absolute;inset:0;z-index:2;pointer-events:none;
  background:
    linear-gradient(90deg,rgba(28,23,66,.76) 0%,rgba(28,23,66,.56) 42%,rgba(28,23,66,.24) 76%,rgba(28,23,66,.18) 100%),
    linear-gradient(180deg,rgba(18,15,48,.18) 0%,rgba(18,15,48,.12) 54%,rgba(18,15,48,.42) 100%)
}
.hero .eyebrow{color:var(--yellow)}
.hero .confetti{display:none}
.hero h1{max-width:13ch;text-shadow:0 3px 28px rgba(20,16,44,.38)}
.hero p{color:rgba(255,255,255,.92);text-shadow:0 2px 18px rgba(20,16,44,.32)}
@keyframes heroCrossfade{
  0%{opacity:0;transform:scale(1.045)}
  4%{opacity:1}
  23%{opacity:1;transform:scale(1.005)}
  27%{opacity:0;transform:scale(1)}
  100%{opacity:0;transform:scale(1)}
}
@media(max-width:700px){
  .hero{min-height:100svh;padding-top:calc(var(--header-h) + 36px);padding-bottom:calc(104px + env(safe-area-inset-bottom))}
  .hero__slide{object-position:54% center}
  .hero__slide:nth-child(1){object-position:55% center}
  .hero__slide:nth-child(2){object-position:45% center}
  .hero__slide:nth-child(3){object-position:50% center}
  .hero__slide:nth-child(4){object-position:50% center}
  .hero__bg::after{
    background:
      linear-gradient(180deg,rgba(28,23,66,.28) 0%,rgba(28,23,66,.22) 28%,rgba(28,23,66,.52) 66%,rgba(28,23,66,.78) 100%),
      linear-gradient(90deg,rgba(28,23,66,.34),rgba(28,23,66,.10))
  }
  .hero h1{max-width:12ch}
  .hero p{max-width:34ch}
  .hero__strip{gap:7px 18px;margin-top:24px;padding-top:18px;font-size:.84rem}
}
@media(prefers-reduced-motion:reduce){
  .hero__slide{animation:none!important;opacity:0!important;transform:none!important}
  .hero__slide:first-child{opacity:1!important}
}'''

    html = replace_once(html, old_hero_css, new_hero_css, "hero CSS")

    html = replace_once(
        html,
        '<div class="hero__bg"><img src="assets/photos/hero.svg" alt="" width="1600" height="900" fetchpriority="high"></div>',
        '''<div class="hero__bg" aria-hidden="true">
    <img class="hero__slide" src="assets/photos/hero-01.webp" alt="" width="2048" height="1152" fetchpriority="high">
    <img class="hero__slide" src="assets/photos/hero-02.webp" alt="" width="2048" height="1152" decoding="async">
    <img class="hero__slide" src="assets/photos/hero-03.webp" alt="" width="2048" height="1152" decoding="async">
    <img class="hero__slide" src="assets/photos/hero-04.webp" alt="" width="2048" height="1152" decoding="async">
  </div>''',
        "hero background markup",
    )

    # The old canvas sequence is intentionally retained in source for easy rollback,
    # but never initialised or downloaded after this change.
    html = replace_once(
        html,
        "if (act && tier !== 'static') {",
        "if (false && act && tier !== 'static') {",
        "scroll-act JavaScript guard",
    )

    INDEX.write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
