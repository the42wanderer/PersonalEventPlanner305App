"""Clean the George De Alwis Vanilla planifolia plate for print.

Crops inside the ruled border, white-balances the aged paper to the brand cream
(#FEF8E9), flattens paper texture and removes a stray red mark. Coordinates are
fractions of the source, so the same script works on the 960 px preview and the
5595 x 7805 px original from Wikimedia Commons.

Usage: python3 tools/prepare_plate.py SOURCE.jpg plates/de-alwis-vanilla.jpg [max_width]
"""
import sys
import numpy as np
from PIL import Image, ImageFilter

CREAM = np.array([254, 248, 233], float)
CROP = (0.026, 0.028, 0.976, 0.917)          # inside the ruled border
STAINS = [(0.60, 0.40, 0.68, 0.47), (0.90, 0.29, 0.995, 0.38)]        # red mark right of the vine

src, out = sys.argv[1], sys.argv[2]
max_w = int(sys.argv[3]) if len(sys.argv) > 3 else 0
im = Image.open(src).convert('RGB')
W, H = im.size
im = im.crop((int(CROP[0] * W), int(CROP[1] * H), int(CROP[2] * W), int(CROP[3] * H)))
if max_w and im.width > max_w:
    im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
a = np.asarray(im).astype(float)
h, w, _ = a.shape

# Paper colour = median of the brightest, least saturated pixels.
sat = a.max(2) - a.min(2)
lum = a.mean(2)
paper_px = a[(sat < 40) & (lum > np.percentile(lum, 70))]
paper = np.median(paper_px, 0)

bal = np.clip(a / paper * CREAM, 0, 255)

# Flatten paper grain: pixels close to paper blend fully to cream.
dist = np.sqrt(((a - paper) ** 2).sum(2))
k = np.clip((dist - 10) / 26, 0, 1)
k = np.asarray(Image.fromarray((k * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(max(1, w / 900)))) / 255.0
bal = bal * k[..., None] + CREAM * (1 - k[..., None])

for x0, y0, x1, y1 in STAINS:
    xs, ys = slice(int(x0 * w), int(x1 * w)), slice(int(y0 * h), int(y1 * h))
    reg = bal[ys, xs]
    red = (reg[..., 0] - reg[..., 1]) > 8
    reg[red] = CREAM

Image.fromarray(bal.astype(np.uint8)).save(out, quality=92, subsampling=0)
print('paper', paper.round(), '->', out, w, 'x', h)
