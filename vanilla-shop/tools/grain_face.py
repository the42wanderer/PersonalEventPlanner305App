"""Paper grain and riso-like ink texture on a rendered face: soft fibre mottling, paper tooth, fine grain,
and uneven pressed ink with small knock-outs on the type. INK=#RRGGBB picks dark type on a light ground.
Usage: [INK=#2E2208] python3 tools/grain_face.py in.png out.png [in2.png out2.png ...]"""
import sys, numpy as np
from PIL import Image, ImageFilter
rng = np.random.default_rng(11)
def noise(h, w, blur, sd=60):
    n = Image.fromarray(np.clip(rng.normal(128, sd, (h, w)), 0, 255).astype(np.uint8))
    return np.asarray(n.filter(ImageFilter.GaussianBlur(blur))).astype(float) - 128 if blur else np.asarray(n).astype(float) - 128
def grain(src, out, ink_hex=None):
    im = np.asarray(Image.open(src).convert('RGB')).astype(float); h, w = im.shape[:2]
    if ink_hex:
        ic = np.array([int(ink_hex[i:i + 2], 16) for i in (1, 3, 5)], float)
        ink = (np.sqrt(((im - ic) ** 2).sum(2)) < 40).astype(float)
    else:
        ink = ((im[..., 0] > 190) & (im[..., 1] > 180) & (im[..., 2] > 160)).astype(float)
    ink = np.asarray(Image.fromarray((ink * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6))).astype(float) / 255
    # paper: soft fibre mottling, clumped tooth, fine grain
    mott = noise(h, w, 18, 90) * 0.10
    tooth = noise(h, w, 1.1, 70) * 0.22
    fine = rng.normal(0, 7, (h, w))
    paper = mott + tooth + fine
    out_im = im + paper[..., None] * (1 - ink[..., None] * 0.6)
    # ink: pressed unevenly, small knock-outs where the paper tooth is high
    holes = (noise(h, w, 0.7, 70) > 52).astype(float) * ink
    blot = noise(h, w, 9, 90) * 0.28 * ink
    base = np.median(im[20:200, 20:200].reshape(-1, 3), 0)
    out_im = out_im + blot[..., None]
    out_im = out_im * (1 - holes[..., None] * 0.4) + base * holes[..., None] * 0.4
    Image.fromarray(np.clip(out_im, 0, 255).astype(np.uint8)).save(out)
import os
for a, b in zip(sys.argv[1::2], sys.argv[2::2]): grain(a, b, os.environ.get('INK'))
