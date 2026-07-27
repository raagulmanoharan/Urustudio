#!/usr/bin/env python3
"""Assemble the Uru lookbook as a single self-contained HTML file.
Reads real product renders + generated photography, embeds each as a
compressed JPEG data-URI, and writes research/uru-lookbook.html."""
import base64, io, os
from PIL import Image

REPO = "/home/user/Urustudio"
LB   = "/tmp/claude-0/-home-user-Urustudio/814f9f28-ad79-514d-83be-0430254fdf3b/scratchpad/lookbook"
SCR  = "/tmp/claude-0/-home-user-Urustudio/814f9f28-ad79-514d-83be-0430254fdf3b/scratchpad"

SRC = {
    "cover":   f"{LB}/01-cover.png",
    "spreadA": f"{LB}/02-spreadA.png",
    "spreadB": f"{LB}/03-spreadB.png",
    "koodai":  f"{LB}/04-koodai.png",
    "tote":    f"{LB}/05-tote.png",
    "bucket":  f"{LB}/06-bucket.png",
    "tassels": f"{LB}/07-tassels.png",
    "linings": f"{LB}/08-linings.png",
    "menu":    f"{LB}/09-content-menu.png",
    "soap":    f"{LB}/10-soap.png",
    "sweets":  f"{LB}/11-sweets.png",
    "kept":    f"{LB}/12-kept.png",
    "brass":   f"{SCR}/ref-brass-keepsake.png",
    "token":   f"{SCR}/ref-brass-token.png",
    "box":     f"{SCR}/ref-kraft-box.png",
    "hangtag": f"{SCR}/ref-hangtag-card.png",
    "seedtag": f"{SCR}/ref-seedpaper-tag.png",
    # real renders already used on the website
    "b_potli": f"{REPO}/images/p-thamboolam-potli.jpg",
    "b_bag":   f"{REPO}/images/p-thamboolam-bag.jpg",
    "b_mari":  f"{REPO}/images/p-marigold.jpg",
    "b_buck":  f"{REPO}/images/p-bucket.jpg",
    "b_clut":  f"{REPO}/images/p-clutch.jpg",
    "b_flap":  f"{REPO}/images/p-flap.jpg",
    "makers":  f"{REPO}/images/makers.jpg",
    "weave":   f"{REPO}/images/process-weave.jpg",
}

def data_uri(path, maxw=1500, q=82):
    im = Image.open(path).convert("RGB")
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format="JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

IMG = {k: data_uri(p) for k, p in SRC.items()}

def bag(img, name, tamil, specs):
    chips = "".join(f"<span>{s}</span>" for s in specs)
    return f"""<figure class="bagcard"><div class="bagimg" style="background-image:url('{IMG[img]}')"></div>
      <figcaption><h4>{name} <em>{tamil}</em></h4><div class="chips">{chips}</div></figcaption></figure>"""

BAGS = "".join([
    bag("b_potli","Drawstring Koodai","koodai","korai grass · ~15×15 cm · cotton drawcord + tassel · holds ~250–400 g".split(" · ")),
    bag("b_bag","Thamboolam Bag","tāmbūlam","palmyra / korai · open tote ~18×14 cm · flat plaited base · no closure".split(" · ")),
    bag("b_mari","Marigold Tote","","korai · ~16×16 cm · contrast rim band · open mouth".split(" · ")),
    bag("b_buck","Bucket Bag","","korai · ~14×12 cm · folded cuff · two short woven handles".split(" · ")),
    bag("b_clut","Reed Clutch","","fine korai · ~20×12 cm · antique-brass zip · tighter weave".split(" · ")),
    bag("b_flap","Flap Bag","","korai · ~17×12 cm · wooden button + woven loop".split(" · ")),
])

def fill(name, note):
    return f"<li><b>{name}</b><span>{note}</span></li>"

FILLS = "".join([
    fill("Handmade soap","Cold-process, botanical. Plastic-free wrap. MOQ ~50 · Coimbatore."),
    fill("Dried fruit &amp; nuts","Long shelf-life; ships and stores ahead. From ~25 packs · Chennai."),
    fill("Brass diya / kumkum box","Gift-scale brass keepsake, engravable. Made to order · Nachiarkoil / Chennai."),
    fill("Natural incense","Custom scent, branded band. Sivakasi hub."),
    fill("Plantable seed paper","The favour itself can be planted — on-brand, no waste."),
    fill("Sweets","Fresh milk/ghee sweets; short shelf-life, made near the date. No MOQ · Chennai."),
])

PAGES = f"""
<!-- COVER -->
<section class="page cover" style="background-image:url('{IMG['cover']}')">
  <div class="cover__scrim"></div>
  <div class="cover__text">
    <p class="kicker">The Lookbook · 2026</p>
    <h1>uru</h1>
    <p class="tagline">Keepsakes worth keeping</p>
    <p class="foot">Handwoven return-gift sets · made to order in Tamil Nadu</p>
  </div>
</section>

<!-- MANIFESTO -->
<section class="page split">
  <div class="split__img" style="background-image:url('{IMG['makers']}')"></div>
  <div class="split__body">
    <p class="eyebrow">Uru means to make — to give something form</p>
    <p class="lead">Months of planning, and the day itself is over in hours. What we make is the part that stays: a handwoven keepsake, small enough to keep and good enough to use, that sends everyone home with a little of your happiest day.</p>
    <p class="note">Every set is made to order. No plastic in the gift. Each piece leaves a loom with a name behind it — women-led weaving clusters across Tamil Nadu.</p>
  </div>
</section>

<!-- ANATOMY OF THE SET -->
<section class="page split reverse">
  <div class="split__img" style="background-image:url('{IMG['spreadB']}')"></div>
  <div class="split__body">
    <p class="eyebrow">Anatomy of a set</p>
    <h2>One finished keepsake, thoughtfully filled</h2>
    <p class="note">The woven bag is made as <b>one finished piece</b> — lined, banded, tasselled, closed and labelled by the weaver. Around it sit five simple add-ons:</p>
    <ol class="anatomy">
      <li><b>The woven bag</b> — the keepsake you keep</li>
      <li><b>A personalised tag</b> — name &amp; date, in wood or brass</li>
      <li><b>Hang &amp; care cards</b> — the story, and how to keep it</li>
      <li><b>A kraft gift box</b> — cushioned in tissue &amp; natural fill</li>
      <li><b>A brass keepsake</b> — an optional heirloom accent</li>
      <li><b>The filling</b> — chosen to the occasion</li>
    </ol>
    <p class="tiny">Indicative build ₹450–700 / set before assembly &amp; margin.</p>
  </div>
</section>

<!-- BAG OPTIONS -->
<section class="page grid-page">
  <div class="page-head"><p class="eyebrow">The pieces</p><h2>Bag options</h2>
    <p class="note">Six woven silhouettes, each delivered finished. Dimensions and capacities are indicative and confirmed per weave.</p></div>
  <div class="baggrid">{BAGS}</div>
</section>

<!-- BAG FEATURE: KOODAI -->
<section class="page split">
  <div class="split__img tall" style="background-image:url('{IMG['koodai']}')"></div>
  <div class="split__body">
    <p class="eyebrow">In detail · Drawstring Koodai</p>
    <h2>Holds its shape, cinches shut</h2>
    <p class="note"><b>Physics &amp; make.</b> A drawstring channel is woven into the rim; korai grass is stiff enough to hold a rounded body when filled (~250–400 g). The cotton cord and tassel are added at finishing, dyed to your accent shade.</p>
    <div class="chips"><span>korai grass</span><span>~15×15 cm</span><span>cotton drawcord</span><span>dusty-rose tassel</span></div>
  </div>
</section>

<!-- BAG FEATURE: TOTE + BUCKET -->
<section class="page grid-page">
  <div class="page-head"><p class="eyebrow">In detail · Open styles</p><h2>Thamboolam tote &amp; bucket bag</h2></div>
  <div class="duo">
    <figure><div class="duoimg" style="background-image:url('{IMG['tote']}')"></div>
      <figcaption><h4>Thamboolam Tote</h4><p>Flat plaited base for stability; open mouth suits bulkier contents — betel, sweets, a small pouch. No closure needed.</p></figcaption></figure>
    <figure><div class="duoimg" style="background-image:url('{IMG['bucket']}')"></div>
      <figcaption><h4>Bucket Bag</h4><p>A folded cuff doubles the rim for structure; two short woven handles. Sage &amp; natural straw.</p></figcaption></figure>
  </div>
</section>

<!-- CONTENT / FILL MENU -->
<section class="page split reverse">
  <div class="split__img" style="background-image:url('{IMG['menu']}')"></div>
  <div class="split__body">
    <p class="eyebrow">Fill it your way</p>
    <h2>Content options</h2>
    <p class="note">Each keepsake is gifted filled. Mix to the occasion; we keep it plastic-free.</p>
    <ul class="fillmenu">{FILLS}</ul>
  </div>
</section>

<!-- CONTENT DETAILS -->
<section class="page grid-page">
  <div class="page-head"><p class="eyebrow">Content, up close</p><h2>Chosen to the occasion</h2></div>
  <div class="trio">
    <figure><div class="trioimg" style="background-image:url('{IMG['soap']}')"></div><figcaption>Botanical soap · dusty rose</figcaption></figure>
    <figure><div class="trioimg" style="background-image:url('{IMG['sweets']}')"></div><figcaption>Sweets &amp; dry fruit · kraft box</figcaption></figure>
    <figure><div class="trioimg" style="background-image:url('{IMG['brass']}')"></div><figcaption>Brass diya &amp; kumkum box</figcaption></figure>
  </div>
</section>

<!-- COMPONENTS: TRIMS -->
<section class="page grid-page">
  <div class="page-head"><p class="eyebrow">Components</p><h2>Trims &amp; linings</h2>
    <p class="note">Colours matched to your palette by swatch. Cotton and silk; a cotton lining stops fine contents slipping through the weave.</p></div>
  <div class="duo">
    <figure><div class="duoimg" style="background-image:url('{IMG['tassels']}')"></div><figcaption><h4>Tassels &amp; cords</h4><p>Bound-neck cotton &amp; silk tassels, twisted drawcords — dusty rose, ivory, sage, terracotta.</p></figcaption></figure>
    <figure><div class="duoimg" style="background-image:url('{IMG['linings']}')"></div><figcaption><h4>Linings &amp; bands</h4><p>Handloom cotton linings and a narrow ivory rim band, folded to order.</p></figcaption></figure>
  </div>
</section>

<!-- COMPONENTS: MARKS -->
<section class="page grid-page">
  <div class="page-head"><p class="eyebrow">Components · Personalisation</p><h2>Marks &amp; tags</h2>
    <p class="note">The couple's name and date, pressed by hand. Choose paper, wood or brass.</p></div>
  <div class="trio">
    <figure><div class="trioimg" style="background-image:url('{IMG['hangtag']}')"></div><figcaption>Hang &amp; care cards · cotton paper</figcaption></figure>
    <figure><div class="trioimg" style="background-image:url('{IMG['token']}')"></div><figcaption>Engraved brass token</figcaption></figure>
    <figure><div class="trioimg" style="background-image:url('{IMG['seedtag']}')"></div><figcaption>Plantable seed-paper tag</figcaption></figure>
  </div>
</section>

<!-- PACKAGING -->
<section class="page split">
  <div class="split__img tall" style="background-image:url('{IMG['box']}')"></div>
  <div class="split__body">
    <p class="eyebrow">The unboxing</p>
    <h2>Kraft box, no plastic</h2>
    <p class="note">A rigid kraft box cushions the keepsake in cream tissue and natural crinkle fill — or dyed korai shred and dried marigold, if you'd rather keep it all one material. Recycled and biodegradable options throughout.</p>
    <div class="chips"><span>kraft / recycled</span><span>tissue wrap</span><span>natural fill</span><span>plastic-free</span></div>
  </div>
</section>

<!-- FULL SPREAD: WEDDING TABLE -->
<section class="page full" style="background-image:url('{IMG['spreadA']}')">
  <div class="full__cap"><p>Fifty to two thousand — a table of finished sets, woven to your colours.</p></div>
</section>

<!-- PROVENANCE -->
<section class="page split reverse">
  <div class="split__img" style="background-image:url('{IMG['weave']}')"></div>
  <div class="split__body">
    <p class="eyebrow">Signed by hand</p>
    <h2>Made by women-led clusters in Tamil Nadu</h2>
    <p class="note">Chettinad palm-leaf (kottan), Pattamadai and Musiri korai grass, Thoothukudi palmyra — many GI-tagged crafts. Order a batch and you keep a craft in practice for another season.</p>
  </div>
</section>

<!-- CLOSING -->
<section class="page full closing" style="background-image:url('{IMG['kept']}')">
  <div class="full__scrim"></div>
  <div class="closing__text">
    <h2>A gift from your day should outlast it.</h2>
    <p>uru.studio · hello@uru.studio · WhatsApp +91 80563 97813</p>
  </div>
</section>
"""

HTML = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Uru · Lookbook</title>
<style>
:root{{--cream:#f4efe7;--ink:#2c2723;--muted:#6f6659;--rose:#c08a82;--terra:#b0703f;--sage:#8a9a7b;--gold:#8a6d3b;--line:#e2d9c9;}}
*{{box-sizing:border-box}}
html,body{{margin:0;background:#ded5c6;color:var(--ink);
  font-family:"Jost","Helvetica Neue",Arial,sans-serif;-webkit-font-smoothing:antialiased}}
.serif{{font-family:"Cormorant Garamond","Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif}}
h1,h2,h4,.tagline{{font-family:"Cormorant Garamond","Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif;font-weight:500;letter-spacing:.01em}}
.book{{max-width:1123px;margin:0 auto;padding:24px 16px 60px}}
.page{{position:relative;width:100%;aspect-ratio:1123/794;background:var(--cream);
  margin:0 auto 22px;border-radius:4px;overflow:hidden;box-shadow:0 10px 34px rgba(40,32,24,.18);
  display:flex}}
/* cover */
.cover{{background-size:cover;background-position:center;align-items:flex-end}}
.cover__scrim{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(20,16,12,.15),rgba(20,16,12,.55))}}
.cover__text{{position:relative;padding:6% 8%;color:#fdfaf4}}
.cover h1{{font-size:clamp(52px,11vw,140px);margin:.02em 0;line-height:.9}}
.kicker{{letter-spacing:.4em;text-transform:uppercase;font-size:12px;opacity:.85;margin:0}}
.tagline{{font-size:clamp(20px,3.6vw,34px);font-style:italic;margin:.1em 0 .3em}}
.cover .foot{{font-size:13px;letter-spacing:.05em;opacity:.9;margin:0}}
/* split pages */
.split{{background:var(--cream)}}
.split.reverse{{flex-direction:row-reverse}}
.split__img{{flex:0 0 52%;background-size:cover;background-position:center}}
.split__img.tall{{flex-basis:46%}}
.split__body{{flex:1;padding:6% 6.5%;display:flex;flex-direction:column;justify-content:center}}
.eyebrow{{color:var(--terra);letter-spacing:.22em;text-transform:uppercase;font-size:11px;margin:0 0 .8em}}
.split__body h2{{font-size:clamp(26px,3.4vw,40px);margin:0 0 .5em;line-height:1.05}}
.lead{{font-size:clamp(15px,1.7vw,20px);line-height:1.5;margin:.2em 0 1em}}
.note{{color:var(--muted);font-size:14.5px;line-height:1.6;margin:.3em 0}}
.tiny{{color:var(--muted);font-size:11.5px;letter-spacing:.03em;margin-top:1.2em}}
.eyebrow+.lead{{margin-top:0}}
ol.anatomy{{margin:.6em 0 0;padding-left:1.1em;color:var(--ink);font-size:14.5px;line-height:1.85}}
ol.anatomy b{{font-weight:600}}
/* grid pages */
.grid-page{{flex-direction:column;padding:4.6% 5.2%}}
.page-head{{margin-bottom:2.4%}}
.page-head h2{{font-size:clamp(24px,3.2vw,38px);margin:.1em 0 .3em}}
.baggrid{{flex:1;display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:1fr 1fr;gap:16px}}
.bagcard{{margin:0;display:flex;flex-direction:column;background:#fff;border:1px solid var(--line);border-radius:6px;overflow:hidden}}
.bagimg{{flex:1;background-size:cover;background-position:center;min-height:0}}
.bagcard figcaption{{padding:9px 11px}}
.bagcard h4{{margin:0 0 5px;font-size:17px}}
.bagcard h4 em{{color:var(--muted);font-size:12px;font-style:italic;font-family:"Jost",sans-serif}}
.chips{{display:flex;flex-wrap:wrap;gap:5px}}
.chips span{{font-size:10.5px;color:var(--muted);background:var(--cream);border:1px solid var(--line);
  border-radius:999px;padding:2px 8px;letter-spacing:.02em}}
.duo{{flex:1;display:grid;grid-template-columns:1fr 1fr;gap:20px}}
.duo figure{{margin:0;display:flex;flex-direction:column}}
.duoimg{{flex:1;background-size:cover;background-position:center;border-radius:6px;min-height:0}}
.duo figcaption{{padding-top:12px}}
.duo h4{{margin:0 0 4px;font-size:19px}}
.duo p{{margin:0;color:var(--muted);font-size:13.5px;line-height:1.55}}
.trio{{flex:1;display:grid;grid-template-columns:repeat(3,1fr);gap:16px}}
.trio figure{{margin:0;display:flex;flex-direction:column}}
.trioimg{{flex:1;background-size:cover;background-position:center;border-radius:6px;min-height:0}}
.trio figcaption{{padding-top:10px;color:var(--muted);font-size:12.5px;text-align:center}}
ul.fillmenu{{list-style:none;margin:.4em 0 0;padding:0}}
ul.fillmenu li{{padding:8px 0;border-top:1px solid var(--line);display:flex;flex-direction:column}}
ul.fillmenu li:first-child{{border-top:none}}
ul.fillmenu b{{font-size:15px}}
ul.fillmenu span{{color:var(--muted);font-size:12.5px;margin-top:2px}}
/* full-bleed */
.full{{background-size:cover;background-position:center;align-items:flex-end}}
.full__cap{{position:relative;padding:4% 6%;color:#fff}}
.full__cap p{{margin:0;font-size:clamp(15px,2vw,22px);font-family:"Cormorant Garamond",Georgia,serif;font-style:italic;
  text-shadow:0 1px 12px rgba(0,0,0,.5)}}
.full__scrim{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(20,16,12,.1),rgba(20,16,12,.6))}}
.closing{{align-items:center;justify-content:center;text-align:center}}
.closing__text{{position:relative;color:#fdfaf4;padding:0 8%}}
.closing__text h2{{font-size:clamp(26px,4vw,46px);margin:0 0 .5em;line-height:1.1}}
.closing__text p{{font-size:13px;letter-spacing:.08em;opacity:.92;margin:0}}
@media(max-width:720px){{
  .page{{aspect-ratio:auto;flex-direction:column!important}}
  .split__img,.split__img.tall{{flex-basis:auto;height:46vw}}
  .baggrid{{grid-template-columns:repeat(2,1fr);grid-template-rows:none}}
  .bagimg{{height:34vw}}.duo,.trio{{grid-template-columns:1fr}}
  .duoimg{{height:52vw}}.trioimg{{height:52vw}}.cover{{aspect-ratio:3/4}}
}}
@media print{{
  html,body{{background:#fff}}
  .book{{max-width:none;margin:0;padding:0}}
  .page{{margin:0;border-radius:0;box-shadow:none;width:100%;height:100vh;
    aspect-ratio:auto;page-break-after:always;break-after:page}}
}}
@page{{size:1123px 794px;margin:0}}
</style></head>
<body><div class="book">{PAGES}</div></body></html>"""

out = f"{REPO}/research/uru-lookbook.html"
with open(out, "w") as f:
    f.write(HTML)
print("wrote", out, round(len(HTML)/1024), "KB")
