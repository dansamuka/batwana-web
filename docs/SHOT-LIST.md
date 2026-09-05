# Shot list — the scroll act

The frames in `assets/act/` are placeholders. This is how to shoot the real thing.

## What the act has to do

Seventy-two frames, scrubbed by scroll, showing **one setup day in order**: an
empty lawn becomes a Batwana funpark. The scroll *is* the story, which is why it
earns 300vh instead of being decoration.

It also makes the sales argument physically. "We arrive early, we set up, we run
it, we clear away" is a claim. Watching it happen as you scroll is proof.

## Shooting

**One camera, one position, locked off.** Tripod, no pan, no zoom, no handheld.
Every frame must align or the scrub judders. Mark the tripod feet with tape and do
not move them for the whole day.

**Interval, not video.** An intervalometer at one frame every 20–30 seconds across
a 5-hour setup and party gives 600–900 frames; cull to 72. Video pulled to stills
also works but the file is larger for no benefit.

**Manual everything.** Fixed ISO, aperture and white balance. Auto-exposure will
flicker frame to frame and the flicker is far more obvious when scrubbed than when
played. Accept that the morning is a little dark or the afternoon a little hot.

**Frame for the arc.** A three-quarter wide that holds the gate, the lawn where the
castle goes, and open sky. The van needs to enter frame; the castle needs room to
inflate to full height; you want sky for the light to change in.

## The beats the code expects

The frame index is the story position. Keep these roughly where they are or the
text will land on the wrong picture.

| Frames | Progress | What is on screen |
|---|---|---|
| 000–007 | 0.00–0.10 | Empty lawn. Van arrives at the gate. |
| 008–026 | 0.11–0.36 | Crew unload. Castle goes from flat to full height. |
| 021–035 | 0.30–0.48 | Pool fills. Rigging, anchoring, cable runs. |
| 032–050 | 0.44–0.70 | First children arrive. Activity builds. |
| 043–071 | 0.60–1.00 | Full party. Light warms to golden, then dusk. Lanterns on. |

## The one thing that will break it

**The first half must be pale. The second half must be dark.**

Beats 1 and 2 set dark indigo type on the footage; beat 3 sets white type, and the
navbar flips colour at exactly `p = 0.55`. Shooting a bright party at 2pm and stopping
before sunset gives you white text on a bright sky and it will be unreadable.

Start early enough that the opening frames are genuinely pale — soft morning light,
overcast is fine — and keep shooting past golden hour into dusk with the lanterns lit.
The light change is doing as much work as the action.

## Consent

Written parental consent before any identifiable child appears, signed on the day and
filed against the specific frames. A child who walks through the background of frame
048 is as identifiable as one in close-up. If consent is refused, either reshoot or
choose a framing where that child is not recognisable.

## Delivering the frames

```
1280 × 720, 16:9, WebP quality ~72, target under 40 KB each
assets/act/f000.webp … f071.webp        (exactly 72, zero-padded to 3 digits)
assets/act/still.webp                   (a single strong frame, roughly index 51)
```

`still.webp` is the blurred backdrop behind the canvas while frames load, and the
hero image for anyone on the `static` tier.

Nothing in `index.html` changes as long as the count, names and ratio hold. If you
deliver a different number of frames, change `var N = 72` in the act runtime and
`N = 72` in `tools/make-frames.py`.

## Regenerating placeholders

```bash
python3 tools/make-frames.py
```

Rewrites all 72 placeholder frames plus the still. Useful for testing timing changes
before the real shoot exists.
