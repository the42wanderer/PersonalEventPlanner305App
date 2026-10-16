"""Paper grain and riso-like ink texture on a rendered face: soft fibre mottling, paper tooth, fine grain,
and uneven pressed ink with small knock-outs on light type.
Usage: python3 tools/grain_face.py in.png out.png [in2.png out2.png ...]"""
import sys, numpy as np
from PIL import Image, ImageFilter
rng = np.random.default_rng(11)
def noise(h, w, blur, sd=60):
    n = Image.fromarray(np.clip(rng.normal(128, sd, (h, w)), 0, 255).astype(np.uint8))
    return np.asarray(n.filter(ImageFilter.GaussianBlur(blur))).astype(float) - 128 if blur else np.asarray(n).astype(float) - 128
def grain(src, out):
    im = np.asarray(Image.open(src).convert('RGB')).astype(float); h, w = im.shape[:2]
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
    base = np.array([18, 27, 66], float)
    out_im = out_im + blot[..., None]
    out_im = out_im * (1 - holes[..., None] * 0.4) + base * holes[..., None] * 0.4
    Image.fromarray(np.clip(out_im, 0, 255).astype(np.uint8)).save(out)
for a, b in zip(sys.argv[1::2], sys.argv[2::2]): grain(a, b)
