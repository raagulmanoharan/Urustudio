#!/usr/bin/env python3
"""Minimal REST caller for Gemini image generation (nano-banana-2),
bypassing the google-genai SDK (broken system cryptography binding here).
Usage:
  GEMINI_API_KEY=... python gen_image.py --prompt "..." --output out.png \
      --aspect-ratio 9:16 --resolution 2K --ref a.jpg --ref b.jpg
"""
import argparse, base64, json, mimetypes, os, sys, urllib.request

MODEL = "gemini-3.1-flash-image-preview"
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={k}"


def part_from_image(path):
    mime = mimetypes.guess_type(path)[0] or "image/jpeg"
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    return {"inline_data": {"mime_type": mime, "data": data}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--aspect-ratio", default="9:16")
    ap.add_argument("--resolution", default="2K")
    ap.add_argument("--ref", action="append", default=[])
    args = ap.parse_args()

    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        sys.exit("GEMINI_API_KEY not set")

    parts = [{"text": args.prompt}] + [part_from_image(p) for p in args.ref]
    body = {
        "contents": [{"role": "user", "parts": parts}],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"],
            "imageConfig": {"aspectRatio": args.aspect_ratio, "imageSize": args.resolution},
        },
    }
    req = urllib.request.Request(
        ENDPOINT.format(m=MODEL, k=key),
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            resp = json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read().decode()[:800]}")

    saved = False
    for cand in resp.get("candidates", []):
        for part in cand.get("content", {}).get("parts", []):
            if "text" in part and part["text"].strip():
                print("[model text]", part["text"][:300])
            inline = part.get("inline_data") or part.get("inlineData")
            if inline and not saved:
                with open(args.output, "wb") as f:
                    f.write(base64.b64decode(inline["data"]))
                print("saved:", args.output)
                saved = True
    if not saved:
        print("NO IMAGE. Raw (trimmed):", json.dumps(resp)[:800])
        sys.exit(2)


if __name__ == "__main__":
    main()
