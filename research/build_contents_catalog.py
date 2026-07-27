#!/usr/bin/env python3
"""Build the Uru 'What Goes Inside' contents catalog as one self-contained HTML.
Dual-purpose: a vendor spec and a customer personalisation menu. Every item
carries a gift-scale size so contents stay mindful of the keepsake they fill."""
import base64, io
from PIL import Image

SCR = "/tmp/claude-0/-home-user-Urustudio/814f9f28-ad79-514d-83be-0430254fdf3b/scratchpad"
LB  = f"{SCR}/lookbook"

THUMBS = {
    "hero":   f"{LB}/09-content-menu.png",
    "sweets": f"{LB}/11-sweets.png",
    "soap":   f"{LB}/10-soap.png",
    "brass":  f"{SCR}/ref-brass-keepsake.png",
    "seed":   f"{SCR}/ref-seedpaper-tag.png",
    "token":  f"{SCR}/ref-brass-token.png",
}
def uri(path, maxw, q=80):
    im = Image.open(path).convert("RGB")
    if im.width > maxw:
        im = im.resize((maxw, round(im.height*maxw/im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()
IMG = {k: uri(p, 1200 if k=="hero" else 720) for k, p in THUMBS.items()}

# category: (icon, title, tamil, intent, thumb-key or None, [ (name, desc, size, [tags]) ... ])
CATS = [
 ("🍬","Sweets &amp; Savouries","Inippu · Bakshanam","The taste of the day, packed fresh.","sweets",[
    ("Mysore pak","Ghee-rich, melt-in-the-mouth — the wedding classic.","2–3 pcs · ~80 g",["fresh","core"]),
    ("Besan / boondi laddu","Festive staple; travels reasonably well.","2 pcs · ~70 g",["fresh"]),
    ("Adhirasam","Jaggery-rice sweet; keeps a little longer.","2 pcs",["fresh"]),
    ("Mini halwa","Badam or carrot; rich single-serve.","~60 g cup",["fresh"]),
    ("Dry-fruit laddu","No added sugar; keeps longer than milk sweets.","2–3 pcs",["keeps"]),
    ("Mixture / murukku","For guests who prefer non-sweet.","~50 g pouch",["keeps"]),
 ]),
 ("🥜","Dry Fruit &amp; Nuts",None,"Keeps for months; can be packed well ahead.","token",[
    ("Almond · cashew · pista mix","Classic premium favour.","~60–80 g pouch",["keeps"]),
    ("Stuffed / plain dates","Naturally sweet, ages well.","3–4 pcs",["keeps"]),
    ("Fig &amp; apricot","Soft dried fruit, gift pouch.","~60 g",["keeps"]),
    ("Roasted spiced nuts","Lightly masala-roasted.","~60 g",["keeps"]),
 ]),
 ("🧼","Body &amp; Wellness",None,"Everyday care, gently and naturally scented.","soap",[
    ("Handmade soap","Sandalwood, jasmine, turmeric or rose; cold-process.","~50–60 g bar · ~6 cm",["plastic-free","core"]),
    ("Manjal ubtan / bath powder","Turmeric &amp; herb bath blend.","~40 g pouch",["plastic-free"]),
    ("Herbal face oil","Kumkumadi-style, small glass vial.","5–10 ml · ~5 cm",["keeps"]),
    ("Lip balm / body butter","Mini tin, natural.","~10 g tin",["keeps"]),
    ("Bath sachet","Vetiver, rose petals, dried herbs.","~30 g",["plastic-free"]),
 ]),
 ("🪔","Sacred &amp; Auspicious","Mangala","A small blessing to keep and use.","brass",[
    ("Brass diya / kuthuvilakku","Gift-scale lamp; engravable base.","~5–6 cm",["keeps","heirloom"]),
    ("Kumkum chimizh (brass box)","Filled with manjal &amp; kumkum.","~4 cm box",["keeps","heirloom"]),
    ("Manjal &amp; kumkum sachet","Turmeric root + kumkum; auspicious.","twin sachet",["fresh"]),
    ("Akshata pouch","Turmeric-tinted rice for blessings.","~30 g",["keeps"]),
    ("Thamboolam","Betel leaf &amp; areca nut — added day-of.","2 leaves + nut",["fresh"]),
    ("Brass bell (manikatti)","Delicate pooja bell.","~5 cm",["keeps","heirloom"]),
 ]),
 ("🕯️","Fragrance &amp; Light",None,"The scent-memory of the day.",None,[
    ("Agarbatti (incense)","Custom scent; plain paper band.","8–10 short sticks",["plastic-free"]),
    ("Sambrani / dhoop cups","Traditional resin incense.","4–6 cups",["plastic-free"]),
    ("Soy / natural candle","Small poured candle, private-label.","~5 cm tin · 40 g",["keeps"]),
    ("Potpourri sachet","Dried rose &amp; marigold.","~30 g",["plastic-free"]),
    ("Attar roll-on","Jasmine, sandal or oudh.","3–5 ml · ~5 cm",["keeps"]),
 ]),
 ("🌱","Grow &amp; Green",None,"A gift that keeps growing.","seed",[
    ("Plantable seed-paper tag","The tag itself is planted.","flat · ~5×7 cm",["plastic-free","core"]),
    ("Seed balls","Tulsi, marigold or wildflower.","3–4 balls",["plastic-free","core"]),
    ("Seed packet","Tulsi, marigold, curry leaf, coriander.","~5 g",["plastic-free","core"]),
    ("Terracotta pot + seed","A little pot to start.","~5 cm pot",["keeps"]),
 ]),
 ("✨","Keepsakes &amp; Trinkets",None,"Small things that outlast the day.","token",[
    ("Engraved brass token","Name &amp; date; ties to the keepsake.","~3–4 cm",["keeps","personalise"]),
    ("Brass / kansa trinket","A little bowl or spoon.","~6–8 cm",["keeps","heirloom"]),
    ("Wooden trinket / holder","Turned wood, natural finish.","~5 cm",["keeps"]),
    ("Kalava / sacred thread","Auspicious red-yellow thread.","small coil",["fresh"]),
    ("Handloom kerchief","Small cotton square, woven in TN.","folds to ~8 cm",["keeps"]),
 ]),
 ("☕","Tea, Coffee &amp; Spice",None,"A taste of home to carry back.",None,[
    ("Filter coffee sachet","Kumbakonam degree blend.","~25 g sachet",["keeps"]),
    ("Masala chai blend","Small tin or pouch.","~25 g pouch",["keeps"]),
    ("Podi sampler","Idli podi, curry podi.","2 × ~30 g",["keeps"]),
    ("Saffron vial","A few strands, gift-scale.","~1 g · ~4 cm",["keeps"]),
    ("Mini honey jar","Local, single-origin.","~30–50 g jar",["keeps"]),
 ]),
]

TAGLABEL = {"fresh":"fresh · make near the date","keeps":"keeps well","plastic-free":"plastic-free",
            "core":"site staple","heirloom":"heirloom","personalise":"personalised"}
def tag(t): return f'<span class="tag t-{t}">{TAGLABEL.get(t,t)}</span>'

def card(name, desc, size, tags):
    return (f'<article class="item"><h4>{name}</h4><p>{desc}</p>'
            f'<p class="size">Gift-scale · {size}</p>'
            f'<div class="tags">{"".join(tag(t) for t in tags)}</div></article>')

def section(icon, title, tamil, intent, thumb, items):
    tam = f'<em>{tamil}</em>' if tamil else ''
    th = (f'<div class="cat-thumb" style="background-image:url(\'{IMG[thumb]}\')"></div>' if thumb else '')
    cards = "".join(card(*it) for it in items)
    return f"""<section class="cat">
      <div class="cat-head"><div class="cat-title"><span class="ic">{icon}</span>
        <h2>{title} {tam}</h2></div><p class="intent">{intent}</p></div>
      <div class="cat-body">{th}<div class="items">{cards}</div></div>
    </section>"""
SECTIONS = "".join(section(*c) for c in CATS)

CAPS = [
 ("Drawstring Koodai","~15 × 15 cm, cinched","~250–400 g; items to ~10 cm"),
 ("Thamboolam Tote","~18 × 14 cm, open","bulkier / taller items"),
 ("Bucket Bag","~14 × 12 cm","compact; holds its shape"),
 ("Reed Clutch","~20 × 12 cm, flat","flat items — soap, cards, flat sweets"),
 ("Flap Bag","~17 × 12 cm","medium; flap closure"),
]
CAP_ROWS = "".join(f"<tr><td><b>{n}</b></td><td>{d}</td><td>{h}</td></tr>" for n,d,h in CAPS)

OCC = [
 ("Wedding &amp; reception","Sweets + brass diya + seed-paper tag"),
 ("Housewarming (Gruhapravesam)","Soap + brass diya + spice podi"),
 ("Festival &amp; pooja","Sweets + sambrani/agarbatti + kumkum box"),
 ("Baby &amp; naming","Soap + seed balls + brass bell"),
 ("Corporate &amp; bulk","Dry fruit + candle + engraved token"),
]
OCC_ROWS = "".join(f"<tr><td>{o}</td><td>{s}</td></tr>" for o,s in OCC)

HTML = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Uru · What Goes Inside — Contents Catalog</title>
<style>
:root{{--bg:#f4efe7;--panel:#fffdf9;--ink:#2c2723;--muted:#6f6659;--line:#e4dccf;
 --terra:#b0703f;--rose:#c08a82;--sage:#7f8f6f;--gold:#8a6d3b;--chip:#efe7d6;}}
@media(prefers-color-scheme:dark){{:root{{--bg:#1c1916;--panel:#252119;--ink:#ece5d8;--muted:#a99f8f;
 --line:#3a342a;--terra:#d0975f;--rose:#d6a59d;--sage:#a3b191;--gold:#d8b877;--chip:#33291a;}}}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);line-height:1.5;
 font-family:"Jost",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif}}
h1,h2{{font-family:"Cormorant Garamond","Iowan Old Style",Palatino,Georgia,serif;font-weight:500}}
.wrap{{max-width:1120px;margin:0 auto;padding:0 1.25rem 4rem}}
header.top{{padding:2.6rem 0 1.4rem;border-bottom:1px solid var(--line);margin-bottom:1.6rem}}
h1{{font-size:clamp(1.9rem,4.2vw,2.9rem);margin:0 0 .2em;letter-spacing:.01em}}
.sub{{color:var(--muted);max-width:66ch;font-size:1rem;margin:.2em 0 0}}
.hero{{margin:1.3rem 0 0;height:230px;border-radius:12px;background-size:cover;background-position:center;
 box-shadow:inset 0 0 0 1px var(--line)}}
.guide{{display:flex;flex-wrap:wrap;gap:.8rem;margin:1.3rem 0 0}}
.guide div{{flex:1 1 210px;background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:.7rem .9rem}}
.guide b{{font-size:.9rem}} .guide p{{margin:.2em 0 0;color:var(--muted);font-size:.82rem}}
.legend{{display:flex;flex-wrap:wrap;gap:.4rem;margin:1rem 0 0}}
.caps{{margin:1.6rem 0 0;background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:1rem 1.1rem}}
.caps h3{{margin:0 0 .2em;font-size:1rem}}.caps .sub{{margin:0 0 .4em}}
.cat{{margin:2.2rem 0 0;border-top:2px solid var(--chip);padding-top:1.1rem}}
.cat-head{{margin-bottom:.9rem}}
.cat-title{{display:flex;align-items:baseline;gap:.6rem}}
.cat-title .ic{{font-size:1.3rem}}
.cat-title h2{{margin:0;font-size:1.4rem}}
.cat-title em{{color:var(--muted);font-size:.9rem;font-style:italic;font-family:"Jost",sans-serif}}
.intent{{margin:.2em 0 0 2rem;color:var(--terra);font-size:.92rem}}
.cat-body{{display:flex;gap:1.1rem;align-items:flex-start}}
.cat-thumb{{flex:0 0 210px;height:250px;border-radius:12px;background-size:cover;background-position:center;
 box-shadow:inset 0 0 0 1px var(--line)}}
.items{{flex:1;display:grid;grid-template-columns:repeat(auto-fill,minmax(215px,1fr));gap:.8rem}}
.item{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:.8rem .9rem;display:flex;flex-direction:column}}
.item h4{{margin:0 0 .25em;font-size:1rem}}
.item p{{margin:0 0 .4em;color:var(--muted);font-size:.85rem;line-height:1.45}}
.item .size{{margin:0 0 .5em;color:var(--terra);font-size:.78rem;font-weight:500;letter-spacing:.01em}}
.tags{{display:flex;flex-wrap:wrap;gap:.3rem;margin-top:auto}}
.tag{{font-size:.68rem;letter-spacing:.02em;border-radius:999px;padding:.12rem .5rem;border:1px solid var(--line);
 color:var(--muted);background:var(--chip)}}
.t-core{{background:var(--gold);color:#fff;border-color:transparent}}
.t-fresh{{color:#a5561f;border-color:#e6c9a8}}
.t-plastic-free{{color:var(--sage);border-color:#cdd8bf}}
.t-heirloom,.t-personalise{{color:var(--rose);border-color:#e6cfc9}}
@media(prefers-color-scheme:dark){{.t-fresh{{color:#e8b483;border-color:#5a4326}}
 .t-plastic-free{{border-color:#3f5230}}.t-heirloom,.t-personalise{{border-color:#5a3f3a}}}}
.occ{{margin:2.4rem 0 0}}
table{{width:100%;border-collapse:collapse;margin-top:.5rem;font-size:.9rem}}
th,td{{text-align:left;padding:.5rem .7rem;border-bottom:1px solid var(--line);vertical-align:top}}
th{{color:var(--muted);font-weight:600;font-size:.78rem;letter-spacing:.03em;text-transform:uppercase}}
footer{{margin-top:2.6rem;padding-top:1.2rem;border-top:1px solid var(--line);color:var(--muted);font-size:.82rem}}
@media(max-width:760px){{.cat-body{{flex-direction:column}}.cat-thumb{{flex-basis:auto;width:100%;height:190px}}}}
</style></head><body><div class="wrap">
<header class="top">
  <h1>What goes inside</h1>
  <p class="sub">The keepsake is the gift you keep — this is the menu of what fills it. Curated, grouped, and always chosen to the occasion. Sweets, seeds and soap sit at the heart; everything else is an accent. Every item is <b>gift-scale</b>, sized to the woven keepsake it goes into.</p>
  <div class="hero" style="background-image:url('{IMG['hero']}')"></div>
  <div class="guide">
    <div><b>How to fill a set</b><p>Pick one hero filling + one or two accents. Keep it plastic-free. We confirm shelf-life and lead time per item.</p></div>
    <div><b>Sized to the keepsake</b><p>Nothing over ~10 cm. Drawstring styles hold ~250–400 g total; flat items (soap, cards) suit the reed clutch. We size each item to the style you choose.</p></div>
    <div><b>Made to order</b><p>Nothing off a shelf. Fresh items are made near your date; keepsakes and dry goods can be prepared ahead.</p></div>
    <div><b>Sourced in Tamil Nadu</b><p>Soap (Coimbatore), sweets &amp; dry fruit (Chennai), brass (Nachiarkoil/Kumbakonam), incense (Sivakasi), seed paper (Avinashi).</p></div>
  </div>
  <div class="legend">
    {tag('core')}{tag('fresh')}{tag('keeps')}{tag('plastic-free')}{tag('heirloom')}{tag('personalise')}
  </div>
  <div class="caps">
    <h3>Keepsake capacities</h3>
    <p class="sub">Match the fill to the style — indicative interior sizes.</p>
    <table><thead><tr><th>Style</th><th>Interior</th><th>Holds</th></tr></thead><tbody>{CAP_ROWS}</tbody></table>
  </div>
</header>
{SECTIONS}
<section class="occ">
  <h2 style="font-size:1.4rem;margin:0">Filling by occasion</h2>
  <p class="sub" style="margin-top:.3em">A starting point — mix freely.</p>
  <table><thead><tr><th>Occasion</th><th>Suggested fill</th></tr></thead><tbody>{OCC_ROWS}</tbody></table>
</section>
<footer>All items indicative, gift-scale and made to order; availability, exact size, shelf-life, MOQ and price confirmed per batch. Contents are plastic-free wherever possible. Uru · uru.studio · hello@uru.studio</footer>
</div></body></html>"""

out = "/home/user/Urustudio/research/contents-catalog.html"
open(out,"w").write(HTML)
print("wrote", out, round(len(HTML)/1024), "KB")
