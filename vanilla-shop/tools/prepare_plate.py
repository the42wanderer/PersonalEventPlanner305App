"""Clean the George De Alwis Vanilla planifolia plate for print.

Crops inside the ruled border, white-balances the aged paper to the brand cream
(#FEF8E9), flattens paper texture and removes a stray red mark. Coordinates are
fractions of the source, so the same script works on the 960 px preview and the
5595 x 7805 px original from Wikimedia Commons.

Usage: python3 tools/prepare_plate.py SOURCE.jpg plates/de-alwis-vanilla.jpg [max_width]

Also writes a PNG next to the JPEG where the paper is transparent, so the painting
sits directly on the box stock with no visible rectangle.
"""
import sys
import numpy as np
from PIL import Image, ImageFilter

CREAM = np.array([254, 248, 233], float)
CROP = (0.026, 0.034, 0.976, 0.917)          # inside the ruled border
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

# Cut-out: alpha follows how far each pixel is from the *local* paper colour (the
# sheet is unevenly aged), estimated with a max filter that skips over the paint.
small = im.resize((max(8, w // 8), max(8, h // 8)), Image.BILINEAR)
local = small.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(4)).resize((w, h), Image.BILINEAR)
local = np.asarray(local).astype(float)
ldist = np.sqrt(((a - local) ** 2).sum(2))
alpha = np.clip((ldist - 16) / 28, 0, 1)
# Areas clearly unlike paper (wide leaves the max filter cannot skip) stay opaque.
alpha = np.maximum(alpha, np.clip((dist - 34) / 22, 0, 1))
for x0, y0, x1, y1 in STAINS:
    xs, ys = slice(int(x0 * w), int(x1 * w)), slice(int(y0 * h), int(y1 * h))
    red = (a[ys, xs, 0] - a[ys, xs, 1]) > 8
    alpha[ys, xs][red] = 0
alpha = np.asarray(Image.fromarray((alpha * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(max(0.6, w / 1600)))) / 255.0
safe = np.maximum(alpha, 1e-3)[..., None]
col = np.clip((bal - CREAM * (1 - alpha[..., None])) / safe, 0, 255)
rgba = np.dstack([col, alpha * 255]).astype(np.uint8)
Image.fromarray(rgba, 'RGBA').save(out.rsplit('.', 1)[0] + '.png', optimize=True)
print('paper', paper.round(), '->', out, w, 'x', h)
