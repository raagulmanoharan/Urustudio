#!/usr/bin/env python3
"""Build the Uru options contact sheet: dedicated pages for Bags, Brass
keepsakes, Kraft-box contents, and Other. Plain website language, no
eyebrow copy. Self-contained HTML with embedded studio shots."""
import base64, io
from PIL import Image

OPT = "/tmp/claude-0/-home-user-Urustudio/814f9f28-ad79-514d-83be-0430254fdf3b/scratchpad/options"
SCR = "/tmp/claude-0/-home-user-Urustudio/814f9f28-ad79-514d-83be-0430254fdf3b/scratchpad"
REPO = "/home/user/Urustudio"  # website's own product photos

def uri(path, maxw=680, q=80):
    im = Image.open(path).convert("RGB")
    if im.width > maxw:
        im = im.resize((maxw, round(im.height*maxw/im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()

# section: (title, note, [ (imgpath, name, descriptor, size) ... ])
SECTIONS = [
 ("Bags","The website collection, shown in its own product photos. Interior sizes indicative.",[
   (f"{REPO}/images/p-thamboolam-potli.jpg","Drawstring Koodai","Rust &amp; beige korai · cinch top","~15 × 15 cm"),
   (f"{REPO}/images/p-thamboolam-bag.jpg","Thamboolam Bag","Terracotta &amp; ivory · open tote","~18 × 14 cm"),
   (f"{REPO}/images/p-marigold.jpg","Marigold Tote","Korai · rust band · open","~16 × 16 cm"),
   (f"{REPO}/images/p-bucket.jpg","Bucket Bag","Sage &amp; natural · folded cuff","~14 × 12 cm"),
   (f"{REPO}/images/p-clutch.jpg","Reed Clutch","Fine korai · zip close","~20 × 12 cm"),
   (f"{REPO}/images/p-flap.jpg","Flap Bag","Natural korai · wooden button","~17 × 12 cm"),
 ]),
 ("Brass keepsakes","Small gift-scale brass, engravable, that gets kept and used. Made to order.",[
   (f"{OPT}/br-catchall.png","Catchall Dish","Keys &amp; rings tray","~10 cm"),
   (f"{OPT}/br-incense.png","Incense Holder","Agarbatti stand · ash tray","~12 cm"),
   (f"{OPT}/br-diya.png","Brass Diya","Kuthuvilakku · engravable base","~6 cm"),
   (f"{OPT}/br-kumkum.png","Kumkum Box","Kumkum chimizh · lidded","~4 cm"),
   (f"{OPT}/br-bell.png","Pooja Bell","Manikatti · hand bell","~6 cm"),
   (f"{OPT}/br-urli.png","Brass Urli","Shallow bowl","~7 cm"),
   (f"{OPT}/br-supari.png","Supari Box","Betel-nut box · lidded","~5 cm"),
   (f"{OPT}/br-token.png","Engraved Token","Name &amp; date tag","~3–4 cm"),
 ]),
 ("Kraft-box contents","Edible &amp; pooja items for the kraft box. Fresh items are made near the date.",[
   (f"{OPT}/kb-mysorepak.png","Mysore Pak","Ghee sweet","2–3 pcs"),
   (f"{OPT}/kb-laddu.png","Besan Laddu","Festive sweet","2 pcs"),
   (f"{OPT}/kb-toffee.png","Toffee &amp; Chocolate","Foil-wrapped","small handful"),
   (f"{OPT}/kb-kumkum.png","Kumkum &amp; Manjal","Vermilion &amp; turmeric","twin portion"),
   (f"{OPT}/kb-dryfruit.png","Dry Fruit &amp; Nuts","Almond · cashew · date","~60–80 g"),
   (f"{OPT}/kb-murukku.png","Murukku &amp; Mixture","Savoury","~50 g"),
 ]),
 ("Other","Useful keepsakes and natural extras — the pieces that get kept and used. Plastic-free where possible.",[
   (f"{OPT}/ot-coasters.png","Coaster Set","Woven korai · set of four","~9 cm"),
   (f"{OPT}/ot-napkin.png","Cotton Napkin","Handloom · napkin or wrap","folds to ~10 cm"),
   (f"{OPT}/ot-soap.png","Handmade Soap","Sandalwood / jasmine","~60 g bar"),
   (f"{OPT}/ot-seedpaper.png","Seed Paper","Plantable tag","flat"),
   (f"{OPT}/ot-agarbatti.png","Agarbatti","Incense sticks","short bundle"),
   (f"{OPT}/ot-candle.png","Candle","Soy · small tin","~5 cm"),
   (f"{OPT}/ot-potpourri.png","Potpourri Sachet","Rose &amp; marigold","~30 g"),
   (f"{OPT}/ot-attar.png","Attar Roll-on","Jasmine / sandal / oudh","~5 cm"),
 ]),
]

def card(path, name, desc, size):
    return (f'<figure class="opt"><div class="opt-img" style="background-image:url(\'{uri(path)}\')"></div>'
            f'<figcaption><h4>{name}</h4><p class="d">{desc}</p><p class="s">{size}</p></figcaption></figure>')

def section(title, note, items):
    return (f'<section class="page"><div class="page-head"><h2>{title}</h2>'
            f'<p class="note">{note}</p></div>'
            f'<div class="grid">{"".join(card(*it) for it in items)}</div></section>')

BODY = "".join(section(*s) for s in SECTIONS)

HTML = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Uru · Options</title>
<style>
:root{{--bg:#f4efe7;--panel:#fffdf9;--ink:#2c2723;--muted:#6f6659;--line:#e4dccf;--terra:#b0703f;--chip:#efe7d6;}}
@media(prefers-color-scheme:dark){{:root{{--bg:#1c1916;--panel:#252119;--ink:#ece5d8;--muted:#a99f8f;--line:#3a342a;--terra:#d0975f;--chip:#33291a;}}}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);line-height:1.5;
 font-family:"Jost",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif}}
h1,h2{{font-family:"Cormorant Garamond","Iowan Old Style",Palatino,Georgia,serif;font-weight:500}}
.wrap{{max-width:1120px;margin:0 auto;padding:0 1.25rem 4rem}}
header.top{{padding:2.4rem 0 1.2rem;border-bottom:1px solid var(--line);margin-bottom:.6rem}}
h1{{font-size:clamp(1.8rem,4vw,2.6rem);margin:0 0 .2em}}
.sub{{color:var(--muted);max-width:60ch;font-size:.98rem;margin:0}}
.page{{margin:2.2rem 0 0;border-top:2px solid var(--chip);padding-top:1.1rem}}
.page-head{{display:flex;align-items:baseline;gap:.9rem;flex-wrap:wrap;margin-bottom:1rem}}
.page-head h2{{margin:0;font-size:1.5rem}}
.page-head .note{{margin:0;color:var(--muted);font-size:.9rem}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:1.1rem}}
.opt{{margin:0;background:var(--panel);border:1px solid var(--line);border-radius:12px;overflow:hidden}}
.opt-img{{aspect-ratio:1/1;background-size:cover;background-position:center;border-bottom:1px solid var(--line)}}
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
  <h1>Options</h1>
  <p class="sub">A contact sheet of what makes up each set — the bag, and what goes inside. Made to order, gift-scale, no plastic in the gift. Colours and sizes to the website styles; all indicative and confirmed per order.</p>
</header>
{BODY}
<footer>Uru · handwoven return-gift sets, made to order in Tamil Nadu · uru.studio · hello@uru.studio. All items indicative and gift-scale; sizes, availability and price confirmed per batch.</footer>
</div></body></html>"""

out = "/home/user/Urustudio/research/options-contact-sheet.html"
open(out,"w").write(HTML)
print("wrote", out, round(len(HTML)/1024), "KB")
