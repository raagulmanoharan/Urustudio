# URU — First Story (Awareness Reel)

The first social story for URU: a founder-led Instagram Reel built to create **awareness + curiosity**
without reading as an ad or as "AI slop." This folder holds the finished reel, the generated stills, the
build scripts, and the strategy behind it.

- **Deliverable:** [`uru-reel.mp4`](./uru-reel.mp4) — 20.6s · 9:16 · 1080×1920 · H.264/AAC
- **Angle:** *"The gift that was meant to be kept"* (heritage → now)
- **On camera:** founder, avatar (HeyGen) in the founder's own cloned voice, matted into a warm workshop
- **Picture:** founder avatar + generated brand-style stills + product catalog + a reframed site wedding shot

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
| 0.0–3.3 | Founder (workshop backdrop) | "In Tamil Nadu, we once gave newlyweds…" |
| 3.3–5.6 | Soaked *korai* grass → keepsake with a name tag | "…woven from river grass — with their names on it." |
| 5.6–7.8 | Reframed site wedding shot (basket carried) | "Meant to last their whole marriage." |
| 7.8–13.1 | Founder (the pivot + mission) | "Now? …plastic in the bin by Monday. So I started Uru." |
| 13.1–15.1 | Hands weaving *korai* | "Still woven by hand." |
| 15.1–16.8 | Sweets box → jasmine gajra (catalog) | "Filled for your day…" |
| 16.8–18.1 | Drawstring Koodai, filled (catalog) | "…and made to be kept, long after." |
| 18.1–20.6 | Basket living at home + `uru` wordmark | "A gift from your day should outlast it." |

## Research synthesis (what the reel is built on)

Four parallel research streams (Indian craft D2C · global slow-craft & quiet-luxury · short-form hook
mechanics · unknown-brand launch playbook) converged on the same rules:

1. **Open on a person / mid-action — never a logo or title card.** The first ~1.7s decide reach.
2. **The VO carries it; no music bed.** A generic track "that could sell anything" is a top ad/slop tell.
3. **Withhold the pitch.** No price, no "shop now." Awareness earns the *follow* by being satisfying and
   slightly unfinished. Reveal the object; withhold the who/where/why.
4. **Native texture over polish.** Handheld feel, natural light, one consistent warm grade.
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

## Generated stills (URU style, Gemini / Nano Banana 2)

Made in the site/catalogue style to fill story gaps the catalog doesn't cover. Reusable assets:

- [`stills/soaked-korai-grass.png`](./stills/soaked-korai-grass.png) — river grass (the material)
- [`stills/keepsake-name-tag.png`](./stills/keepsake-name-tag.png) — the name-inscribed keepsake
- [`stills/weaving-hands.png`](./stills/weaving-hands.png) — hands weaving *korai*
- [`stills/basket-second-life.png`](./stills/basket-second-life.png) — the emptied basket living at home

## Production notes

- **Avatar backdrop:** HeyGen couldn't matte this instant-avatar look (its `remove_background` returned a
  fully opaque frame), so the founder is segmented locally (`rembg`, `u2net_human_seg`) and composited over
  a blurred, warm workshop backdrop derived from the site's own weaving photo, with edge feathering and mild
  temporal smoothing to reduce flicker.
- **Sound:** VO only, no music (anti-"AI-slop" per the research).
- **Captions:** burned in the site's Archivo brand font for muted autoplay.
- Build intermediates (raw avatar render, extracted catalog, QC frames) live under `/scratch/` and are
  git-ignored.

## Rebuild

```bash
pip install pillow numpy imageio imageio-ffmpeg fonttools brotli rembg onnxruntime pooch
# 1) generate the brand-style stills (needs a Gemini image key)
GEMINI_API_KEY=... python build/gen_image.py --prompt "..." --output out.png --aspect-ratio 9:16 --ref <site image>
# 2) render the founder VO clip via the HeyGen CLI -> scratch/gen/avatar.mp4
#    heygen video create -d '{"type":"avatar","avatar_id":"...","voice_id":"...","script":"...","aspect_ratio":"9:16"}' --wait
# 3) matte the founder onto the workshop backdrop -> scratch/gen/avatar_workshop.mp4
python build/matte_avatar.py
# 4) compose the reel (expects catalog imgs in scratch/cs, stills in scratch/gen) then mux the VO
python build/render.py
```
