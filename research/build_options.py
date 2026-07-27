#!/usr/bin/env python3
"""Uru options catalog — a choose-from catalog in the website's own design
language. Bags use the website's product photos; every other piece is drawn
from the site's occasion/journal flat-lays (kraft window boxes, plain smooth
brass incl. the long ripple + lotus incense holders and the bangle stand,
deckled seed card, ivory linen). Signature pieces are badged."""
import base64, io
from PIL import Image

OPT  = "/tmp/claude-0/-home-user-Urustudio/814f9f28-ad79-514d-83be-0430254fdf3b/scratchpad/options"
REPO = "/home/user/Urustudio"

def uri(path, maxw=680, q=80):
    im = Image.open(path).convert("RGB")
    if im.width > maxw:
        im = im.resize((maxw, round(im.height*maxw/im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()

# each item: (path, name, descriptor, size) or (path, name, descriptor, size, "sig")
SECTIONS = [
 ("Bags","The website collection — six styles to choose from, in its own product photos.",[
   (f"{REPO}/images/p-thamboolam-potli.jpg","Drawstring Koodai","Rust &amp; beige korai · cinch top","~15 × 15 cm"),
   (f"{REPO}/images/p-thamboolam-bag.jpg","Thamboolam Bag","Terracotta &amp; ivory · open tote","~18 × 14 cm"),
   (f"{REPO}/images/p-marigold.jpg","Marigold Tote","Korai · rust band · open","~16 × 16 cm"),
   (f"{REPO}/images/p-bucket.jpg","Bucket Bag","Sage &amp; natural · folded cuff","~14 × 12 cm"),
   (f"{REPO}/images/p-clutch.jpg","Reed Clutch","Fine korai · zip close","~20 × 12 cm"),
   (f"{REPO}/images/p-flap.jpg","Flap Bag","Natural korai · wooden button","~17 × 12 cm"),
 ]),
 ("Sweets &amp; treats","We're not a sweet shop — just a few assortments you can add. Kraft window boxes; made near the date.",[
   (f"{OPT}/kw-sweets.png","Assorted Sweets","Mysore pak · peda · burfi · laddu","~10 cm box"),
   (f"{OPT}/kw-murukku.png","Assorted Savouries","Murukku · mixture · thattai","~10 cm box"),
   (f"{OPT}/kw-toffee.png","Assorted Toffees","Chocolate &amp; toffee, foil-wrapped","~10 cm box"),
   (f"{OPT}/kw-dryfruit.png","Dry Fruit &amp; Nuts","Almond · cashew · raisin","~10 cm box"),
 ]),
 ("Brass &amp; metal","Plain smooth brass, as on the website — our signature pieces and the everyday keepsakes. Made to order.",[
   (f"{OPT}/br2-incenselong.png","Long Incense Holder","Rippled oval tray · lay-flat stick","~20 cm","sig"),
   (f"{OPT}/br2-bangle.png","Bangle Holder","Brass stand · glass bangles","~14 cm","sig"),
   (f"{OPT}/br2-incenselotus.png","Lotus Incense Holder","Brass lotus · stick hole","~7 cm","sig"),
   (f"{OPT}/br2-leafdish.png","Leaf Catchall","Brass leaf tray · keys &amp; rings","~14 cm"),
   (f"{OPT}/br2-tumbler.png","Brass Tumbler","Chombu · drinking cup","~8 cm"),
   (f"{OPT}/br2-pot.png","Brass Pot","Small chombu / kalasham","~8 cm"),
   (f"{OPT}/br2-lidpot.png","Lidded Kalasham","Domed-lid brass pot","~10 cm"),
   (f"{OPT}/br2-diya.png","Brass Diya","Oil lamp","~6 cm"),
   (f"{OPT}/br2-diyapair.png","Brass Diya Pair","Two oil lamps","~6 cm each"),
   (f"{OPT}/br2-kumkum.png","Kumkum &amp; Turmeric Pots","Lidded brass pots","~4 cm each"),
   (f"{OPT}/br2-spicecups.png","Spice Cups","Open brass cups · kumkum &amp; manjal","~4 cm each"),
   (f"{OPT}/br2-leaf.png","Betel-leaf Plate","Brass leaf tray","~10 cm"),
   (f"{OPT}/br2-thali.png","Round Thali","Brass plate","~12 cm"),
   (f"{OPT}/br2-bowl.png","Brass Bowl","Small round bowl","~7 cm"),
   (f"{OPT}/br2-bell.png","Pooja Bell","Brass hand bell","~6 cm"),
   (f"{OPT}/br2-incense.png","Fan Incense Holder","Brass scallop · standing sticks","~8 cm"),
   (f"{OPT}/br2-spoons.png","Measuring Spoons","Brass, set of four","set"),
   (f"{OPT}/br2-box.png","Lidded Box","Round brass box","~5 cm"),
   (f"{OPT}/br2-silverset.png","Silver Tumbler &amp; Spoon","For baby &amp; naming","~8 cm"),
 ]),
 ("Fragrance &amp; light","Scents to pair with the incense holders above.",[
   (f"{OPT}/ot2-agarbatti.png","Agarbatti","Incense sticks","short bundle"),
   (f"{OPT}/ot2-sambrani.png","Sambrani Cups","Dhoop incense","4–6 cups"),
   (f"{OPT}/ot2-candle.png","Candle","Soy · small cup","~5 cm"),
   (f"{OPT}/ot2-attar.png","Attar Roll-on","Jasmine / sandal / oudh","~5 cm"),
 ]),
 ("Grow &amp; green","Plantable options — a favour that keeps growing.",[
   (f"{OPT}/ot2-seedcard.png","Seed-paper Card","Deckled · botanical sprig","~5 × 7 cm"),
   (f"{OPT}/ot2-seedballs.png","Seed Balls","Tulsi / marigold","3–5 balls"),
   (f"{OPT}/ot2-seedpacket.png","Seed Packet","Herb &amp; flower seeds","~5 g"),
 ]),
 ("Keepsakes &amp; extras","Cloth, woven and botanical pieces — the things that get kept and used.",[
   (f"{OPT}/ot2-coasters.png","Coasters","Woven rattan · set of four","~9 cm"),
   (f"{OPT}/ot2-napkin.png","Cotton Napkin · Rust","Rust check · napkin or wrap","folds ~10 cm"),
   (f"{OPT}/ot2-napkin-mustard.png","Cotton Napkin · Mustard","Mustard check · napkin or wrap","folds ~10 cm"),
   (f"{OPT}/ot2-napkin-blue.png","Cotton Napkin · Blue","Blue &amp; rust plaid · napkin or wrap","folds ~10 cm"),
   (f"{OPT}/ot2-muslin.png","Muslin Pouch","Drawstring · natural","~10 cm"),
   (f"{OPT}/ot2-gajra.png","Jasmine Gajra","Fresh jasmine","small ring"),
   (f"{OPT}/ot2-driedflowers.png","Dried Flowers","Grasses &amp; blooms · posy","small posy"),
   (f"{OPT}/ot2-coconut.png","Coconut","Whole, for the tray","1 pc"),
   (f"{OPT}/ot2-soap.png","Handmade Soap","Sandalwood / jasmine","~60 g bar"),
   (f"{OPT}/ot2-tag.png","Paper Tags","Deckled · jute string","~5 × 7 cm"),
 ]),
]

def card(item):
    path, name, desc, size = item[0], item[1], item[2], item[3]
    sig = len(item) > 4 and item[4] == "sig"
    badge = '<span class="sig-badge">★ Signature</span>' if sig else ''
    cls = "opt sig" if sig else "opt"
    return (f'<figure class="{cls}"><div class="opt-img" style="background-image:url(\'{uri(path)}\')">{badge}</div>'
            f'<figcaption><h4>{name}</h4><p class="d">{desc}</p><p class="s">{size}</p></figcaption></figure>')

def section(title, note, items):
    return (f'<section class="page"><div class="page-head"><h2>{title}</h2>'
            f'<p class="note">{note}</p></div>'
            f'<div class="grid">{"".join(card(it) for it in items)}</div></section>')

BODY = "".join(section(*s) for s in SECTIONS)

HTML = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Uru · Catalog</title>
<style>
:root{{--bg:#f4efe7;--panel:#fffdf9;--ink:#2c2723;--muted:#6f6659;--line:#e4dccf;--terra:#b0703f;--gold:#8a6d3b;--chip:#efe7d6;}}
@media(prefers-color-scheme:dark){{:root{{--bg:#1c1916;--panel:#252119;--ink:#ece5d8;--muted:#a99f8f;--line:#3a342a;--terra:#d0975f;--gold:#d8b877;--chip:#33291a;}}}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);line-height:1.5;
 font-family:"Jost",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif}}
h1,h2{{font-family:"Cormorant Garamond","Iowan Old Style",Palatino,Georgia,serif;font-weight:500}}
.wrap{{max-width:1120px;margin:0 auto;padding:0 1.25rem 4rem}}
header.top{{padding:2.4rem 0 1.2rem;border-bottom:1px solid var(--line);margin-bottom:.6rem}}
h1{{font-size:clamp(1.8rem,4vw,2.6rem);margin:0 0 .2em}}
.sub{{color:var(--muted);max-width:64ch;font-size:.98rem;margin:0}}
.page{{margin:2.2rem 0 0;border-top:2px solid var(--chip);padding-top:1.1rem}}
.page-head{{display:flex;align-items:baseline;gap:.9rem;flex-wrap:wrap;margin-bottom:1rem}}
.page-head h2{{margin:0;font-size:1.5rem}}
.page-head .note{{margin:0;color:var(--muted);font-size:.9rem}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:1.1rem}}
.opt{{margin:0;background:var(--panel);border:1px solid var(--line);border-radius:12px;overflow:hidden}}
.opt.sig{{border-color:var(--gold);box-shadow:0 0 0 1px var(--gold) inset}}
.opt-img{{position:relative;aspect-ratio:1/1;background-size:cover;background-position:center;border-bottom:1px solid var(--line)}}
.sig-badge{{position:absolute;top:.55rem;left:.55rem;background:var(--gold);color:#fff;font-size:.66rem;
 letter-spacing:.05em;text-transform:uppercase;padding:.2rem .5rem;border-radius:999px;font-weight:600}}
.opt figcaption{{padding:.7rem .85rem .85rem}}
.opt h4{{margin:0 0 .15em;font-size:1.05rem}}
.opt .d{{margin:0 0 .5em;color:var(--muted);font-size:.85rem}}
.opt .s{{margin:0;display:inline-block;color:var(--terra);font-size:.76rem;font-weight:500;
 border:1px solid var(--line);background:var(--chip);border-radius:999px;padding:.1rem .55rem}}
footer{{margin-top:2.6rem;padding-top:1.2rem;border-top:1px solid var(--line);color:var(--muted);font-size:.82rem}}
@media(max-width:820px){{.grid{{grid-template-columns:repeat(2,1fr)}}}}
@media(max-width:520px){{.grid{{grid-template-columns:1fr}}}}
</style></head><body><div class="wrap">
<header class="top">
  <h1>The Catalog</h1>
  <p class="sub">A catalog to choose from, in the website's own design language — pick a bag, then the pieces that suit the occasion. Signature pieces marked ★. Made to order, gift-scale, no plastic in the gift; everything indicative and confirmed per order.</p>
</header>
{BODY}
<footer>Uru · handwoven return-gift sets, made to order in Tamil Nadu · uru.studio · hello@uru.studio. Bags shown in the website's product photos; other pieces shown as gift-scale references matched to the site. Sizes, availability and price confirmed per batch.</footer>
</div></body></html>"""

out = "/home/user/Urustudio/research/options-contact-sheet.html"
open(out,"w").write(HTML)
print("wrote", out, round(len(HTML)/1024), "KB")
