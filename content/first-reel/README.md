# URU — First Story (Awareness Reel)

The first social story for URU: a founder-led Instagram Reel built to create **awareness + curiosity**
without reading as an ad or as "AI slop." This folder holds the finished reel, the two generated
stills, the build scripts, and the strategy behind it.

- **Deliverable:** [`uru-reel-v1.mp4`](./uru-reel-v1.mp4) — 20.6s · 9:16 · 1080×1920 · H.264/AAC
- **Angle:** *"The gift that was meant to be kept"* (heritage → now)
- **Voice/VO:** founder avatar (HeyGen), founder's own cloned voice
- **Picture:** strictly the 46-item product catalog + the avatar (no stock, no invented product)

---

## The strategy in one paragraph

URU isn't inventing "gifts people keep" — it's **reviving a documented Tamil tradition**. The Pattamadai
*korai* weave is GI-tagged, ~200 years old, and historically newlyweds were given a grass mat woven with
their **names and wedding date** (a *Muhurtha Paai*), meant to last the whole marriage. Set against the
reality that most wedding return-gifts are plastic that's discarded within days, the contrarian message —
**"the vessel is the keepsake"** — lands as cultural restoration, not marketing. The first story tells
exactly that, in the founder's voice, and withholds the hard sell so it earns a *follow*, not a click.

## Script (the VO)

> In Tamil Nadu, we once gave newlyweds a mat woven from river grass, with their names on it.
> Meant to last their whole marriage.
> Now? We hand out plastic that's in the bin by Monday.
> So I started Uru.
> Still woven by hand. Filled for your day, and made to be kept, long after.
> Because a gift from your day should outlast it.

## Edit structure (20.6s)

| Time | Picture | Line |
|------|---------|------|
| 0.0–3.3 | Founder, to camera | "In Tamil Nadu, we once gave newlyweds…" |
| 3.3–7.8 | Drawstring Koodai → Thamboolam set | "…woven from river grass… meant to last their whole marriage." |
| 7.8–13.1 | Founder (the pivot + mission) | "Now? …plastic in the bin by Monday. So I started Uru." |
| 13.1–18.1 | Flap Bag → sweets → jasmine → Marigold Tote | "Still woven by hand. Filled for your day, and made to be kept…" |
| 18.1–20.6 | Drawstring hero + `uru` wordmark | "A gift from your day should outlast it." |

## Research synthesis (what the reel is built on)

Four parallel research streams (Indian craft D2C · global slow-craft & quiet-luxury · short-form hook
mechanics · unknown-brand launch playbook) converged on the same rules:

1. **Open mid-action / on a person — never a logo or title card.** The first ~1.7s decide reach.
2. **The VO carries it; no music bed.** A generic track "that could sell anything" is a top ad/slop tell.
   Here the founder's voice is the audio.
3. **Withhold the pitch.** No price, no "shop now." Awareness earns the *follow* by being satisfying and
   slightly unfinished. Reveal the object; withhold the who/where/why (that gap is the reason to follow).
4. **Native texture over polish.** Handheld feel, natural light, one consistent grade. Over-graded,
   studio-perfect B-roll reads as ad or AI.
5. **Burn captions** (brand font) for muted autoplay; keep to a few short lines.
6. **~20–30s, 9:16, built to loop.**

**The unlock:** the Pattamadai/*korai* heritage (GI tag; the name-inscribed *Muhurtha Paai*; a Pattamadai
mat gifted to Queen Elizabeth II at her 1953 coronation) plus hard data on return-gift waste
(≈1 in 4 Indian households receive gifts they never use; plastic favours discarded at the venue).

## Suggested post copy

> Uru means to make — to give something form.
>
> In Tamil Nadu, newlyweds were once given a mat woven from river grass, their names pressed in, meant to
> last the whole marriage. Somewhere along the way we swapped it for plastic that's in the bin by Monday.
>
> So we started Uru. Handwoven *korai* keepsakes — filled for your day, made to be kept long after it. 🌾
>
> Made to order in South India. Tell us the date.
>
> #uru #korai #pattamadai #handwoven #tamilwedding #returngifts #southindianwedding #weddingfavors
> #slowcraft #keepsake #madeinindia #sustainablegifting

## Known caveat

HeyGen did **not** apply the intended warm workshop backdrop to this instant-avatar look — the founder's
real room shows behind him (a faint ceiling fan up top). It's tightened and warm-graded so it reads as an
authentic founder selfie. A re-render with a matting-capable avatar type is the fix if the literal backdrop
is wanted.

## Stills (bonus, not used in the catalog-only v1)

Generated in URU's style (Gemini / Nano Banana 2) to fill story gaps the catalog doesn't cover. Kept here
as reusable assets:

- [`stills/soaked-korai-grass.png`](./stills/soaked-korai-grass.png) — material/process (the weaving hook)
- [`stills/basket-second-life.png`](./stills/basket-second-life.png) — the emptied basket living at home

## Rebuild

```bash
pip install pillow numpy imageio imageio-ffmpeg fonttools brotli
# 1) (optional) regenerate stills — needs a Gemini image key
GEMINI_API_KEY=... python build/gen_image.py --prompt "..." --output out.png --aspect-ratio 9:16 --ref <site image>
# 2) avatar VO clip is rendered via the HeyGen CLI (heygen video create) into scratch/gen/avatar.mp4
# 3) compose the reel (expects catalog imgs in scratch/cs, avatar in scratch/gen)
python build/render.py     # -> scratch/out/silent.mp4, then mux HeyGen audio
```

Build intermediates (raw avatar render, extracted catalog, QC frames) live under `/scratch/` and are
git-ignored.
