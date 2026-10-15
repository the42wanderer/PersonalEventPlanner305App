"""Paint a soft, grainy vertical gradient plate in the style of the v5 motif's background.

The colour runs top to bottom through the given stops. Low-frequency mottling keeps it from
looking like a flat digital gradient, and a fine grain matches the painted texture of the motif.

Usage: python3 tools/gradient_plate.py OUT.png WIDTH_MM HEIGHT_MM PX_PER_MM "0:#FCF0D8,0.5:#F7D693,1:#A86A78" [seed]
"""
import sys
import numpy as np
from PIL import Image, ImageFilter

out, wmm, hmm, ppm, stops = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
seed = int(sys.argv[6]) if len(sys.argv) > 6 else 3
W, H = round(wmm * ppm), round(hmm * ppm)
rng = np.random.default_rng(seed)

pts = []
for s in stops.split(','):
    p, c = s.split(':')
    pts.append((float(p), [int(c[i:i + 2], 16) for i in (1, 3, 5)]))
pos = np.array([p for p, _ in pts])
cols = np.array([c for _, c in pts], float)


def field(cells_x, cells_y, blur):
    """Smooth random field in [-1, 1], from an upscaled coarse grid."""
    g = rng.random((cells_y, cells_x))
    im = Image.fromarray((g * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)
    im = im.filter(ImageFilter.GaussianBlur(blur * ppm))
    f = np.asarray(im).astype(float)
    return (f - f.mean()) / (np.abs(f - f.mean()).max() + 1e-6)


# Wavy horizontal bands, like washes laid across the silk: shift the gradient position a little.
t = np.linspace(0, 1, H)[:, None].repeat(W, 1)
t = np.clip(t + 0.045 * field(max(2, int(wmm / 40)), 5, 6), 0, 1)
img = np.stack([np.interp(t, pos, cols[:, k]) for k in range(3)], 2)
# Gentle light and shade, and a fine grain.
img *= (1 + 0.025 * field(max(3, int(wmm / 25)), 6, 4))[..., None]
img += rng.normal(0, 5.0, (H, W, 1)) + rng.normal(0, 1.6, (H, W, 3))
Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).save(out)
print(out, W, H)
