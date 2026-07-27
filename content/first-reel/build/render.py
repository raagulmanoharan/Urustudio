#!/usr/bin/env python3
"""URU first reel v2 — richer craft cut.
Avatar (founder VO) + generated brand-style stills + catalog contents + reframed site wedding shot.
Output 1080x1920 30fps, muxed with HeyGen VO afterwards.
"""
import os, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import imageio.v2 as imageio
from fontTools.ttLib import TTFont

ROOT="/home/user/Urustudio"; CS=f"{ROOT}/scratch/cs"; GEN=f"{ROOT}/scratch/gen"; OUT=f"{ROOT}/scratch/out"
os.makedirs(OUT, exist_ok=True)
W,H,FPS=1080,1920,30

def woff2ttf(s,d):
    if not os.path.exists(d): TTFont(s).save(d)
    return d
ARCH=woff2ttf(f"{ROOT}/fonts/Archivo-Bold.woff2", f"{GEN}/Archivo-Bold.ttf")
def f_arch(sz): return ImageFont.truetype(ARCH,sz)

# prep 9:16 crop of site wedding hero (once)
HERO=f"{GEN}/hero_9x16.jpg"
if not os.path.exists(HERO):
    im=Image.open(f"{ROOT}/images/Uru_Hero.jpg").convert("RGB")
    w,h=im.size; cw=int(h*9/16); cx=int(w*0.66); x=max(0,min(w-cw,cx-cw//2))
    im.crop((x,0,x+cw,h)).save(HERO,quality=92)

_cache={}
def photo_base(path):
    if path in _cache: return _cache[path]
    im=Image.open(path).convert("RGB")
    s=max(W/im.size[0], H/im.size[1]); rs=im.resize((int(im.size[0]*s+1),int(im.size[1]*s+1)),Image.LANCZOS)
    x=(rs.size[0]-W)//2; y=(rs.size[1]-H)//2; im=rs.crop((x,y,x+W,y+H))
    _cache[path]=im; return im

def catalog_base(idx):
    k=f"cat{idx}"
    if k in _cache: return _cache[k]
    im=Image.open(f"{CS}/img_{idx:02d}.jpg").convert("RGB")
    sq=im.resize((W,W),Image.LANCZOS)
    s=max(W/im.size[0],H/im.size[1])*1.15; bg=im.resize((int(im.size[0]*s),int(im.size[1]*s)),Image.LANCZOS)
    x=(bg.size[0]-W)//2; y=(bg.size[1]-H)//2
    bg=bg.crop((x,y,x+W,y+H)).filter(ImageFilter.GaussianBlur(40))
    bg=ImageEnhance.Brightness(bg).enhance(1.02); bg.paste(sq,(0,(H-W)//2-90))
    _cache[k]=bg; return bg

def ken(img,prog,z0=1.03,z1=1.10):
    z=z0+(z1-z0)*min(1.2,max(0,prog)); cw,ch=int(W/z),int(H/z); x=(W-cw)//2; y=(H-ch)//2
    return img.crop((x,y,x+cw,y+ch)).resize((W,H),Image.LANCZOS)

_av=imageio.get_reader(f"{GEN}/avatar_workshop.mp4"); _avfps=_av.get_meta_data().get("fps",25); _avn=_av.count_frames()
_avc={}
def avatar_frame(t):
    idx=min(int(round(t*_avfps)),_avn-1)
    if idx in _avc: base=_avc[idx]
    else:
        base=Image.fromarray(_av.get_data(idx)).convert("RGB"); _avc[idx]=base
        if len(_avc)>8: _avc.pop(next(iter(_avc)))
    sw,sh=base.size; z=1.10; cw,ch=int(sw/z),int(sh/z); cx=sw//2; cy=int(sh*0.47)
    x=max(0,min(sw-cw,cx-cw//2)); y=max(0,min(sh-ch,cy-ch//2))
    im=base.crop((x,y,x+cw,y+ch)).resize((W,H),Image.LANCZOS)
    r,g,b=im.split(); r=r.point(lambda v:min(255,v*1.05+3)); b=b.point(lambda v:v*0.95)
    im=Image.merge("RGB",(r,g,b)); im=ImageEnhance.Contrast(im).enhance(1.04); im=ImageEnhance.Color(im).enhance(1.04)
    yy,xx=np.mgrid[0:H,0:W]; d=np.sqrt(((xx-W/2)/(W*0.72))**2+((yy-H*0.5)/(H*0.72))**2)
    vig=np.clip(1.0-0.20*d,0.7,1.0)[...,None]
    return Image.fromarray((np.asarray(im).astype(np.float32)*vig).clip(0,255).astype("uint8"))

class Clip:
    def __init__(s,start,end,kind,ref=None): s.start,s.end,s.kind,s.ref=start,end,kind,ref
    def render(s,t):
        if s.kind=="avatar": return avatar_frame(t)
        prog=(t-s.start)/max(0.1,s.end-s.start)
        base=photo_base(s.ref) if s.kind=="photo" else catalog_base(s.ref)
        return ken(base,prog)

clips=[
    Clip(0.00,3.30,"avatar"),
    Clip(3.30,4.55,"photo",f"{GEN}/grass.png"),        # river grass
    Clip(4.55,5.60,"photo",f"{GEN}/name_tag.png"),     # with their names on it
    Clip(5.60,7.75,"photo",HERO),                      # wedding — meant to last
    Clip(7.75,13.10,"avatar"),
    Clip(13.10,15.10,"photo",f"{GEN}/weaving.png"),    # still woven by hand
    Clip(15.10,15.95,"catalog",6),                     # filled for your day — sweets
    Clip(15.95,16.75,"catalog",41),                    # jasmine gajra
    Clip(16.75,18.05,"catalog",0),                     # made to be kept — drawstring hero
    Clip(18.05,20.57,"photo",f"{GEN}/basket_home.png"),# outlast it — second life + logo
]
D=0.30
def frame_at(t):
    cur=clips[-1]
    for c in clips:
        if c.start<=t<c.end: cur=c; break
    img=cur.render(t)
    if t<cur.start+D and cur is not clips[0]:
        prev=clips[clips.index(cur)-1]; a=(t-cur.start)/D
        img=Image.blend(prev.render(t),img,a)
    return img

CAPS=[
    (0.30,3.10,"In Tamil Nadu, we once gave newlyweds"),
    (3.15,5.55,"a mat woven from river grass — with their names on it"),
    (5.80,7.75,"Meant to last their whole marriage."),
    (8.26,10.80,"Now we hand out plastic that's in the bin by Monday."),
    (11.24,13.00,"So I started Uru."),
    (13.37,14.95,"Still woven by hand."),
    (15.21,16.55,"Filled for your day —"),
    (16.55,18.00,"and made to be kept, long after."),
]
def wrap(d,text,font,mw):
    out=[]; cur=""
    for w in text.split():
        t=(cur+" "+w).strip()
        if d.textlength(t,font=font)<=mw: cur=t
        else: out.append(cur); cur=w
    if cur: out.append(cur)
    return out
def draw_caption(img,text,alpha):
    grad=Image.new("L",(1,H),0)
    for y in range(H):
        grad.putpixel((0,y), 0 if y<H*0.66 else int(150*((y-H*0.66)/(H*0.34))))
    scrim=Image.new("RGBA",(W,H),(18,14,10,0)); scrim.putalpha(grad.resize((W,H)))
    scrim=Image.blend(Image.new("RGBA",(W,H),(0,0,0,0)),scrim,alpha)
    img=Image.alpha_composite(img.convert("RGBA"),scrim).convert("RGB")
    d=ImageDraw.Draw(img); sz=50; font=f_arch(sz); lines=wrap(d,text,font,940)
    while len(lines)>2 and sz>34: sz-=4; font=f_arch(sz); lines=wrap(d,text,font,940)
    lh=int(sz*1.22); y0=1600-lh*len(lines)//2; A=int(255*alpha)
    for i,ln in enumerate(lines):
        tw=d.textlength(ln,font=font); x=(W-tw)//2; y=y0+i*lh
        for ox,oy in ((-2,2),(2,2),(0,3)): d.text((x+ox,y+oy),ln,font=font,fill=(10,8,6,int(140*alpha)))
        d.text((x,y),ln,font=font,fill=(250,247,242,A))
    return img
def cap_at(t):
    for a,b,txt in CAPS:
        if a-0.2<=t<=b+0.2:
            return max(0.0,min((t-(a-0.2))/0.2,((b+0.2)-t)/0.2,1.0)),txt
    return 0.0,None
def draw_logo(img,alpha):
    ov=Image.new("RGBA",(W,H),(20,16,12,int(95*alpha)))
    img=Image.alpha_composite(img.convert("RGBA"),ov).convert("RGB")
    d=ImageDraw.Draw(img); A=int(255*alpha); logo=f_arch(150); mY=800
    tw=d.textlength("uru",font=logo); d.text(((W-tw)//2,mY),"uru",font=logo,fill=(250,247,242,A))
    tag="KEEPSAKES WORTH KEEPING"; tf=f_arch(30); ls=8
    tot=sum(d.textlength(c,font=tf)+ls for c in tag)-ls; x=(W-tot)//2; y=mY+185
    for c in tag: d.text((x,y),c,font=tf,fill=(232,226,216,A)); x+=d.textlength(c,font=tf)+ls
    return img
def logo_a(t): return 0.0 if t<18.35 else min((t-18.35)/0.5,1.0)

TOTAL=20.57; NF=int(TOTAL*FPS)
wr=imageio.get_writer(f"{OUT}/silent2.mp4",fps=FPS,codec="libx264",quality=None,macro_block_size=1,
                      output_params=["-crf","18","-pix_fmt","yuv420p","-preset","medium"])
print("rendering",NF,"frames")
for i in range(NF):
    t=i/FPS; img=frame_at(t); la=logo_a(t)
    if la>0: img=draw_logo(img,la)
    else:
        al,txt=cap_at(t)
        if txt: img=draw_caption(img,txt,al)
    wr.append_data(np.asarray(img))
    if i%90==0: print(f"  {i}/{NF}")
wr.close(); print("silent2 done")
