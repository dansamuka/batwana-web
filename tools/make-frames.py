#!/usr/bin/env python3
"""
Generate the placeholder frame sequence for the scroll act.

    python3 tools/make-frames.py

Writes assets/act/f000.webp .. f071.webp plus still.webp (the static fallback).

These are PLACEHOLDERS. Replace them with a real setup-day sequence — see
docs/SHOT-LIST.md. Keep the same filenames, count and 16:9 ratio and nothing
in index.html needs to change.

The narrative arc, which the scroll reveals in order:
    0.00-0.10  empty lawn, van arrives
    0.16-0.36  bouncy castle inflates
    0.30-0.48  water pool fills
    0.44-0.70  children arrive, activity builds
    0.60-1.00  light warms to dusk, lanterns come on

Light matters: the first half must be pale enough for dark type, the second
half dark enough for white type. The navbar flips colour at p = 0.55.
"""
from PIL import Image, ImageDraw, ImageFilter
import math, os

W, H, N = 1280, 720, 72
OUT = "assets/act"

def lerp(a, b, t): return a + (b - a) * t
def mix(c1, c2, t): return tuple(int(round(lerp(c1[i], c2[i], t))) for i in range(3))
def ramp(t, stops):
    if t <= stops[0][0]: return stops[0][1]
    if t >= stops[-1][0]: return stops[-1][1]
    for (p0, c0), (p1, c1) in zip(stops, stops[1:]):
        if p0 <= t <= p1: return mix(c0, c1, (t - p0) / (p1 - p0))
    return stops[-1][1]
def ease(t): return t * t * (3 - 2 * t)
def seg(t, a, b):
    if t <= a: return 0.0
    if t >= b: return 1.0
    return ease((t - a) / (b - a))

SKY_TOP = [(0,(214,224,240)),(0.30,(196,214,238)),(0.55,(246,206,150)),(0.72,(120,86,140)),(1,(42,34,102))]
SKY_BOT = [(0,(240,244,250)),(0.30,(228,238,248)),(0.55,(255,232,178)),(0.72,(214,124,110)),(1,(74,58,120))]
GROUND  = [(0,(150,186,110)),(0.30,(157,205,89)),(0.55,(140,178,84)),(0.72,(78,96,74)),(1,(38,44,72))]

def build_vignette():
    """Smooth radial falloff, built small and blurred so it never bands."""
    s = 64
    m = Image.new("L", (s, s), 0)
    d = ImageDraw.Draw(m)
    for y in range(s):
        for x in range(s):
            dx = (x - s / 2) / (s / 2); dy = (y - s / 2) / (s / 2)
            r = min(1.0, math.hypot(dx * 0.92, dy) / 1.32)
            d.point((x, y), int(74 * r ** 2.4))
    m = m.resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(18))
    v = Image.new("RGBA", (W, H), (18, 14, 40, 0))
    v.putalpha(m)
    return v

VIGNETTE = build_vignette()

def frame(i):
    t = i / (N - 1)
    im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im, "RGBA")
    horizon = int(H * 0.62)

    ct, cb = ramp(t, SKY_TOP), ramp(t, SKY_BOT)
    for y in range(horizon):
        d.line([(0, y), (W, y)], fill=mix(ct, cb, y / horizon))

    sx = int(W * (0.18 + 0.62 * t)); sy = int(H * (0.14 + 0.44 * ease(min(1, t / 0.85))))
    glow = ramp(t, [(0,(255,255,240)),(0.5,(255,236,180)),(0.75,(255,168,110)),(1,(255,138,96))])
    for r, a in [(230,26),(160,34),(96,56),(52,150)]:
        d.ellipse([sx-r, sy-r, sx+r, sy+r], fill=glow + (a,))

    hill = mix(ramp(t, GROUND), (90,110,150), 0.45)
    d.polygon([(0,horizon),(W*0.18,horizon-64),(W*0.42,horizon-18),(W*0.66,horizon-78),
               (W*0.88,horizon-26),(W,horizon-50),(W,horizon+6),(0,horizon+6)], fill=hill + (200,))

    g = ramp(t, GROUND)
    d.rectangle([0, horizon, W, H], fill=g)
    d.rectangle([0, horizon, W, horizon + 3], fill=mix(g, (255,255,255), .20))

    warm = t > 0.62
    def shade(c, k=0.42): return mix(c, (38,34,74), k) if warm else c

    vx = int(lerp(-320, W * 0.075, seg(t, 0.0, 0.10))); vy = horizon + 34
    body = shade((248,248,250), .30)
    d.rounded_rectangle([vx, vy-92, vx+230, vy], 12, fill=body)
    d.rounded_rectangle([vx+186, vy-92, vx+266, vy-34], 10, fill=body)
    d.rectangle([vx+196, vy-84, vx+256, vy-52], fill=shade((150,190,225), .35))
    d.ellipse([vx+30, vy-22, vx+74, vy+22], fill=(38,34,58))
    d.ellipse([vx+196, vy-22, vx+240, vy+22], fill=(38,34,58))
    for ox, cc in [(24,(157,205,89)),(74,(238,67,46)),(124,(254,185,27))]:
        d.ellipse([vx+ox, vy-72, vx+ox+34, vy-38], fill=shade(cc, .25))

    inf = seg(t, 0.16, 0.36); cw = 300; ch = int(lerp(16, 190, inf))
    cx = int(W * 0.60); cbm = horizon + 56
    if inf > 0.02:
        wob = math.sin(t * 34) * 3 * inf
        d.rounded_rectangle([cx-cw//2, cbm-ch, cx+cw//2, cbm], int(18*inf)+4, fill=shade((248,200,0), .30))
        if inf > 0.35:
            wh = int(ch * 0.52)
            d.rounded_rectangle([cx-cw//2+18, cbm-ch+10+wob, cx-14, cbm-ch+10+wh], 12, fill=shade((238,67,46), .30))
            d.rounded_rectangle([cx+14, cbm-ch+10+wob, cx+cw//2-18, cbm-ch+10+wh], 12, fill=shade((74,58,174), .30))
            d.rounded_rectangle([cx-46, cbm-int(ch*0.46), cx+46, cbm], 22, fill=shade((42,34,102), .25))
        d.rectangle([cx+cw//2+8, cbm-18, cx+cw//2+34, cbm], fill=shade((110,110,130), .3))

    fl = seg(t, 0.30, 0.48); px, py = int(W*0.235), horizon + 118
    d.ellipse([px-108, py-34, px+108, py+34], fill=shade((236,236,244), .35))
    if fl > 0.02:
        rw = int(96 * fl)
        d.ellipse([px-rw, py-int(28*fl), px+rw, py+int(28*fl)], fill=shade((104,178,222), .30))

    def person(x, y, h, c, bounce=0.0):
        yy = y - int(bounce)
        d.ellipse([x-h//7, yy-h, x+h//7, yy-h+h//4], fill=shade((60,48,44), .3))
        d.rounded_rectangle([x-h//6, yy-h+h//5, x+h//6, yy-h//4], h//8, fill=shade(c, .28))
        d.line([x-h//9, yy-h//4, x-h//8, yy], fill=shade((48,44,70), .3), width=max(2, h//14))
        d.line([x+h//9, yy-h//4, x+h//8, yy], fill=shade((48,44,70), .3), width=max(2, h//14))

    if t > 0.04:
        for k, (fx, ph) in enumerate([(0.20,0.0),(0.545,0.03),(0.72,0.06)]):
            if t > 0.04 + k * 0.05:
                person(int(W*fx), horizon+128+k*14, 70, (248,200,0), math.sin(t*10+ph*60)*2)

    kids = seg(t, 0.44, 0.70); n = int(round(14 * kids))
    cols = [(238,67,46),(74,58,174),(248,80,136),(157,205,89),(254,185,27),(120,200,230)]
    for k in range(n):
        a = (k*47) % 100 / 100
        x = int(W * (0.14 + 0.74 * a)); yb = horizon + 96 + int(66 * ((k*29) % 100) / 100)
        person(x, yb, 40 + int(10 * ((k*13) % 100) / 100), cols[k % len(cols)],
               abs(math.sin(t*26 + k*1.7)) * 9 * kids)

    if t > 0.60:
        gl = seg(t, 0.60, 0.80)
        for k in range(12):
            lx = int(W * (0.06 + k * 0.08)); ly = horizon - 46 + int(16 * math.sin(k * 0.9))
            for r, a in [(22, int(46*gl)), (9, int(210*gl))]:
                d.ellipse([lx-r, ly-r, lx+r, ly+r], fill=(255,214,140,a))

    if t > 0.46:
        cf = seg(t, 0.46, 0.62)
        for k in range(16):
            a = (k*37) % 100 / 100; b = (k*61) % 100 / 100
            x = int(W * (0.05 + 0.9 * a)); y = int(H * (0.10 + 0.5 * b) - (t * 180) % (H * 0.5))
            r = int(4 + 5 * b)
            d.ellipse([x-r, y-r, x+r, y+r], fill=cols[k % len(cols)] + (int(200*cf),))

    return Image.alpha_composite(im.convert("RGBA"), VIGNETTE).convert("RGB")

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    total = 0
    for i in range(N):
        p = f"{OUT}/f{i:03d}.webp"
        frame(i).save(p, "WEBP", quality=72, method=4)
        total += os.path.getsize(p)
    frame(int(0.72 * (N - 1))).save(f"{OUT}/still.webp", "WEBP", quality=80, method=5)
    print(f"{N} frames, {total/1024:.0f} KB, avg {total/N/1024:.1f} KB")
