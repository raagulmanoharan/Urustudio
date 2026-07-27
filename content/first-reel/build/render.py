#!/usr/bin/env python3
"""URU first reel — compositor.
Avatar (founder VO) intercut with catalog product b-roll, synced captions, end logo.
Output: 1080x1920, 30fps, H.264 + AAC (VO from avatar.mp4).
"""
import os, math, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import imageio.v2 as imageio
from fontTools.ttLib import TTFont

ROOT = "/home/user/Urustudio"
CS = f"{ROOT}/scratch/cs"
GEN = f"{ROOT}/scratch/gen"
OUT = f"{ROOT}/scratch/out"
os.makedirs(OUT, exist_ok=True)
W, H, FPS = 1080, 1920, 30
CREAM = (247, 244, 239)

# ---- fonts: woff2 -> ttf ----
def woff2ttf(src, dst):
    if not os.path.exists(dst):
        TTFont(src).save(dst)
    return dst
ARCH = woff2ttf(f"{ROOT}/fonts/Archivo-Bold.woff2", f"{GEN}/Archivo-Bold.ttf")
def f_arch(sz): return ImageFont.truetype(ARCH, sz)

# ---- catalog b-roll base builder (linen-extended 9:16 + slight motion) ----
_cache = {}
def broll_base(idx):
    if idx in _cache: return _cache[idx]
    im = Image.open(f"{CS}/img_{idx:02d}.jpg").convert("RGB")
    sq = im.resize((W, W), Image.LANCZOS)                      # 1080x1080 sharp
    # blurred cover backdrop to fill 9:16 seamlessly
    scale = max(W / im.size[0], H / im.size[1]) * 1.15
    bg = im.resize((int(im.size[0]*scale), int(im.size[1]*scale)), Image.LANCZOS)
    x = (bg.size[0]-W)//2; y=(bg.size[1]-H)//2
    bg = bg.crop((x, y, x+W, y+H)).filter(ImageFilter.GaussianBlur(40))
    bg = ImageEnhance.Brightness(bg).enhance(1.02)
    canvas = bg.copy()
    canvas.paste(sq, (0, (H-W)//2 - 90))                       # product slightly above centre
    # soft drop shadow line under product
    _cache[idx] = canvas
    return canvas

def ken(img, prog, z0=1.02, z1=1.09):
    """prog 0..1 -> zoomed crop for gentle push-in."""
    z = z0 + (z1-z0)*prog
    cw, ch = int(W/z), int(H/z)
    x = (W-cw)//2; y=(H-ch)//2
    return img.crop((x, y, x+cw, y+ch)).resize((W, H), Image.LANCZOS)

# ---- avatar frames: tight crop + warm grade ----
_av = imageio.get_reader(f"{GEN}/avatar.mp4")
_av_meta = _av.get_meta_data(); _av_fps = _av_meta.get("fps", 25); _av_n = _av.count_frames()
_avcache = {}
def avatar_frame(t):
    idx = min(int(round(t*_av_fps)), _av_n-1)
    if idx in _avcache: base = _avcache[idx]
    else:
        arr = _av.get_data(idx)
        base = Image.fromarray(arr).convert("RGB")
        _avcache[idx] = base
        if len(_avcache) > 8: _avcache.pop(next(iter(_avcache)))
    # source 720x1280 (9:16). zoom 1.28 centred slightly high to drop the ceiling fan
    sw, sh = base.size
    z = 1.28
    cw, ch = int(sw/z), int(sh/z)
    cx = sw//2; cy = int(sh*0.44)
    x = max(0, min(sw-cw, cx-cw//2)); y = max(0, min(sh-ch, cy-ch//2))
    im = base.crop((x, y, x+cw, y+ch)).resize((W, H), Image.LANCZOS)
    # warm filmic grade
    r, g, b = im.split()
    r = r.point(lambda v: min(255, v*1.06+4)); b = b.point(lambda v: v*0.94)
    im = Image.merge("RGB", (r, g, b))
    im = ImageEnhance.Contrast(im).enhance(1.06)
    im = ImageEnhance.Color(im).enhance(1.05)
    # vignette
    yy, xx = np.mgrid[0:H, 0:W]
    d = np.sqrt(((xx-W/2)/(W*0.72))**2 + ((yy-H*0.5)/(H*0.72))**2)
    vig = np.clip(1.0-0.32*d, 0.55, 1.0)[..., None]
    im = Image.fromarray((np.asarray(im).astype(np.float32)*vig).clip(0,255).astype("uint8"))
    return im

# ---- clips ----
class Clip:
    def __init__(s, start, end, kind, idx=None):
        s.start, s.end, s.kind, s.idx = start, end, kind, idx
    def render(s, t):
        if s.kind == "avatar":
            return avatar_frame(t)                              # identity map -> lip sync
        prog = (t - s.start)/max(0.1, (s.end - s.start))
        return ken(broll_base(s.idx), min(1.2, max(0.0, prog)))

clips = [
    Clip(0.00, 3.30, "avatar"),
    Clip(3.30, 5.60, "broll", 0),    # drawstring koodai
    Clip(5.60, 7.75, "broll", 1),    # thamboolam filled
    Clip(7.75, 13.10, "avatar"),
    Clip(13.10, 15.10, "broll", 5),  # flap bag weave
    Clip(15.10, 15.95, "broll", 6),  # assorted sweets
    Clip(15.95, 16.75, "broll", 41), # jasmine gajra
    Clip(16.75, 18.05, "broll", 2),  # marigold tote
    Clip(18.05, 20.57, "broll", 0),  # end hero (drawstring) + logo
]
D = 0.30  # dissolve

def frame_at(t):
    cur = clips[-1]
    for c in clips:
        if c.start <= t < c.end: cur = c; break
    img = cur.render(t)
    # dissolve from previous clip at the head of cur
    if t < cur.start + D and cur is not clips[0]:
        pi = clips.index(cur)-1
        prev = clips[pi]
        a = (t-cur.start)/D
        pv = prev.render(t)
        img = Image.blend(pv, img, a)
    return img

# ---- captions ----
CAPS = [
    (0.30, 3.10, "In Tamil Nadu, we once gave newlyweds"),
    (3.15, 5.55, "a mat woven from river grass — with their names on it"),
    (5.80, 7.75, "Meant to last their whole marriage."),
    (8.26, 10.80, "Now we hand out plastic that's in the bin by Monday."),
    (11.24, 13.00, "So I started Uru."),
    (13.37, 14.95, "Still woven by hand."),
    (15.21, 16.55, "Filled for your day —"),
    (16.55, 18.00, "and made to be kept, long after."),
]
def wrap(draw, text, font, maxw):
    words = text.split(); lines=[]; cur=""
    for w in words:
        t=(cur+" "+w).strip()
        if draw.textlength(t, font=font) <= maxw: cur=t
        else: lines.append(cur); cur=w
    if cur: lines.append(cur)
    return lines

def draw_caption(img, text, alpha):
    if alpha <= 0: return img
    d = ImageDraw.Draw(img, "RGBA")
    # bottom scrim
    grad = Image.new("L", (1, H), 0)
    for y in range(H):
        v = 0 if y < H*0.66 else int(150*((y-H*0.66)/(H*0.34)))
        grad.putpixel((0, y), v)
    scrim = Image.new("RGBA", (W, H), (18, 14, 10, 0))
    scrim.putalpha(grad.resize((W, H)))
    scrim = Image.blend(Image.new("RGBA",(W,H),(0,0,0,0)), scrim, alpha)
    img = Image.alpha_composite(img.convert("RGBA"), scrim).convert("RGB")
    d = ImageDraw.Draw(img)
    sz = 50; font=f_arch(sz)
    lines = wrap(d, text, font, 940)
    while len(lines) > 2 and sz > 34:
        sz -= 4; font=f_arch(sz); lines=wrap(d, text, font, 940)
    lh = int(sz*1.22); total=lh*len(lines); y0 = 1600 - total//2
    A = int(255*alpha)
    for i, ln in enumerate(lines):
        tw = d.textlength(ln, font=font); x=(W-tw)//2; y=y0+i*lh
        for ox,oy in ((-2,2),(2,2),(0,3)):
            d.text((x+ox,y+oy), ln, font=font, fill=(10,8,6,int(140*alpha)))
        d.text((x,y), ln, font=font, fill=(250,247,242,A))
    return img

def cap_alpha(t):
    for a,b,txt in CAPS:
        if a-0.2 <= t <= b+0.2:
            fade=0.2
            al = min((t-(a-0.2))/fade, ((b+0.2)-t)/fade, 1.0)
            return max(0.0,al), txt
    return 0.0, None

# ---- end logo ----
def draw_logo(img, alpha):
    if alpha<=0: return img
    d=ImageDraw.Draw(img,"RGBA")
    # darken hero a touch to let logo read
    ov=Image.new("RGBA",(W,H),(20,16,12,int(90*alpha)))
    img=Image.alpha_composite(img.convert("RGBA"),ov).convert("RGB")
    d=ImageDraw.Draw(img)
    A=int(255*alpha)
    logo=f_arch(150); markY=790
    tw=d.textlength("uru",font=logo); d.text(((W-tw)//2,markY),"uru",font=logo,fill=(250,247,242,A))
    # tagline letterspaced
    tag="KEEPSAKES WORTH KEEPING"; tf=f_arch(30); ls=8
    total=sum(d.textlength(c,font=tf)+ls for c in tag)-ls
    x=(W-total)//2; y=markY+180
    for c in tag:
        d.text((x,y),c,font=tf,fill=(232,226,216,A)); x+=d.textlength(c,font=tf)+ls
    return img

def logo_alpha(t):
    if t < 18.35: return 0.0
    return min((t-18.35)/0.5, 1.0)

# ---- render ----
TOTAL = 20.57
NF = int(TOTAL*FPS)
writer = imageio.get_writer(f"{OUT}/silent.mp4", fps=FPS, codec="libx264",
                            quality=None, macro_block_size=1,
                            output_params=["-crf","18","-pix_fmt","yuv420p","-preset","medium"])
print(f"rendering {NF} frames...")
for i in range(NF):
    t = i/FPS
    img = frame_at(t)
    la = logo_alpha(t)
    if la > 0:
        img = draw_logo(img, la)
    else:
        al, txt = cap_alpha(t)
        if txt: img = draw_caption(img, txt, al)
    writer.append_data(np.asarray(img))
    if i % 60 == 0: print(f"  {i}/{NF}  t={t:.1f}")
writer.close()
print("silent.mp4 done")
