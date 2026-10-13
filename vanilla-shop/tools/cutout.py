"""Turn a generated illustration into a trimmed cut-out PNG for the box.

Keeps an existing alpha channel; otherwise removes the flat background colour
(sampled from the image border). Trims to the artwork's bounding box.

Usage: python3 tools/cutout.py SOURCE OUT.png
"""
import sys
import numpy as np
from PIL import Image, ImageFilter

src, out = sys.argv[1], sys.argv[2]
im = Image.open(src)
if im.mode == 'RGBA':
    rgba = np.asarray(im).astype(float)
    a = rgba[..., :3]
    alpha = rgba[..., 3] / 255.0
else:
    a = np.asarray(im.convert('RGB')).astype(float)
    b = np.concatenate([a[:12].reshape(-1, 3), a[-12:].reshape(-1, 3), a[:, :12].reshape(-1, 3), a[:, -12:].reshape(-1, 3)])
    bg = np.median(b, 0)
    dist = np.sqrt(((a - bg) ** 2).sum(2))
    alpha = np.clip((dist - 10) / 26, 0, 1)
    alpha = np.asarray(Image.fromarray((alpha * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7))) / 255.0
    # Un-premultiply against the background so soft edges keep the artwork's colour.
    safe = np.maximum(alpha, 1e-3)[..., None]
    a = np.clip((a - bg * (1 - alpha[..., None])) / safe, 0, 255)
    print('background', bg.round())

ys, xs = np.where(alpha > 0.04)
pad = 4
y0, y1 = max(0, ys.min() - pad), min(alpha.shape[0], ys.max() + pad + 1)
x0, x1 = max(0, xs.min() - pad), min(alpha.shape[1], xs.max() + pad + 1)
rgba = np.dstack([a, alpha * 255])[y0:y1, x0:x1].astype(np.uint8)
Image.fromarray(rgba, 'RGBA').save(out, optimize=True)
print(out, rgba.shape[1], 'x', rgba.shape[0])
