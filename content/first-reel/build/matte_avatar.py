#!/usr/bin/env python3
"""Matte the founder out of the room and composite over the blurred workshop backdrop.
Produces avatar_workshop.mp4 (with original VO audio)."""
import numpy as np, imageio.v2 as imageio
from PIL import Image, ImageFilter
from rembg import remove, new_session
import subprocess, imageio_ffmpeg, os

GEN="/home/user/Urustudio/scratch/gen"
sess=new_session('u2net_human_seg')
rd=imageio.get_reader(f"{GEN}/avatar.mp4"); meta=rd.get_meta_data(); fps=meta.get("fps",25)
n=rd.count_frames(); W,H=rd.get_data(0).shape[1], rd.get_data(0).shape[0]
print("frames",n,"size",W,H,"fps",fps)
bg=Image.open(f"{GEN}/bg_workshop.jpg").convert("RGB").resize((W,H), Image.LANCZOS)
bg_np=np.asarray(bg).astype(np.float32)

wr=imageio.get_writer(f"{GEN}/avatar_workshop_silent.mp4", fps=fps, codec="libx264",
                      quality=None, macro_block_size=1,
                      output_params=["-crf","16","-pix_fmt","yuv420p","-preset","medium"])
prev_a=None
for i in range(n):
    frame=Image.fromarray(rd.get_data(i)).convert("RGB")
    out=remove(frame, session=sess)                       # RGBA straight
    arr=np.asarray(out).astype(np.float32)
    a=arr[...,3]/255.0
    # erode 1px (min) to kill bright halo, then feather
    ai=Image.fromarray((a*255).astype("uint8"))
    ai=ai.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
    a=np.asarray(ai).astype(np.float32)/255.0
    # temporal smoothing to reduce edge flicker
    if prev_a is not None:
        a=0.65*a+0.35*prev_a
    prev_a=a
    a3=a[...,None]
    comp=(frame_np:=np.asarray(frame).astype(np.float32))*a3 + bg_np*(1-a3)
    wr.append_data(comp.clip(0,255).astype("uint8"))
    if i%50==0: print(f"  matte {i}/{n}")
wr.close(); print("silent matte done")

FF=imageio_ffmpeg.get_ffmpeg_exe()
subprocess.run([FF,"-y","-i",f"{GEN}/avatar_workshop_silent.mp4","-i",f"{GEN}/avatar.mp4",
                "-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-b:a","192k","-shortest",
                f"{GEN}/avatar_workshop.mp4","-loglevel","error"],check=True)
print("avatar_workshop.mp4 ready")
