"""Paint a grainy ground for the box wrap: a mesh of soft, angled colour fields, or a flat colour.

Each field is an ellipse (centre, radii and angle in mm) whose colour blends into its neighbours,
so close tones drift across the box at different angles instead of running top to bottom.
Grain is two layers: a fine monochrome noise and a softer clumped noise, like risograph paper.

Usage: python3 tools/mesh_plate.py NAME   (presets below)  ->  plates/generated/v6-ground-NAME-<face>.jpg
"""
import sys
import numpy as np
from PIL import Image, ImageFilter

PPM = 12
STRIP_W, STRIP_H = 350.65, 90.74            # the four walls plus 3 mm bleed at each end and edge
FACES = {'front': (0, 87.66), 'sideA': (87.66, 84.57), 'back': (172.23, 87.58), 'sideB': (259.81, 84.84)}
# Long 25-bag box: front, right side, back, left side (mm, from its dieline).
LONG = len(sys.argv) > 2 and sys.argv[2] == 'long'
if LONG:
    FACES = {'front': (0, 175.93), 'sideA': (175.93, 85.12), 'back': (261.05, 175.02), 'sideB': (436.07, 84.49)}
    STRIP_W = 520.56 + 6

# (x, y, rx, ry, angle_deg, colour) in strip mm (x 0 = 3 mm before the front's left edge).
PRESETS = {
    # Close custard tones; the front's type corner stays light, warmth gathers behind the flower.
    'custard': dict(base='#FAEFD4', grain=7.5, fields=[
        (10, 10, 70, 40, -20, '#FCF4E2'),
        (75, 50, 60, 34, 25, '#F7DDA4'),
        (40, 92, 70, 26, -8, '#F3C995'),
        (140, 20, 55, 40, 35, '#F8E6BC'),
        (165, 86, 60, 30, 15, '#EFC4AE'),
        (230, 30, 70, 38, -30, '#EEE5BF'),
        (300, 70, 65, 36, 20, '#F5D7A4'),
        (345, 10, 50, 35, 0, '#FBEED3'),
    ]),
    # One diagonal sweep of golden-hour light, cut at an angle across the walls.
    'golden': dict(base='#F8E2B3', grain=9, angle=-28, stops=[(0, '#FCF2DC'), (0.35, '#F8DFA6'), (0.62, '#F2C48C'), (0.85, '#ECB9A4'), (1, '#F4D2A0')], period=150),
    'butter': dict(base='#F6E6BE', grain=5, fields=[]),
    'sage': dict(base='#E6E7CB', grain=5, fields=[]),
}

hexrgb = lambda c: np.array([int(c[i:i + 2], 16) for i in (1, 3, 5)], float)
name = sys.argv[1]
P = PRESETS[name]
W, H = round(STRIP_W * PPM), round(STRIP_H * PPM)
yy, xx = np.mgrid[0:H, 0:W] / PPM
rng = np.random.default_rng(17)

if 'stops' in P:
    a = np.radians(P['angle'])
    t = ((xx * np.cos(a) + yy * np.sin(a)) / P['period']) % 2
    t = np.where(t > 1, 2 - t, t)                   # mirror so the sweep repeats without a seam
    pos = np.array([s for s, _ in P['stops']]); cols = np.array([hexrgb(c) for _, c in P['stops']])
    img = np.stack([np.interp(t, pos, cols[:, k]) for k in range(3)], 2)
else:
    acc = np.zeros((H, W, 3)) + hexrgb(P['base']) * 0.6
    wsum = np.full((H, W), 0.6)
    for x, y, rx, ry, ang, c in P['fields']:
        a = np.radians(ang)
        dx, dy = xx - x, yy - y
        u, v = (dx * np.cos(a) + dy * np.sin(a)) / rx, (-dx * np.sin(a) + dy * np.cos(a)) / ry
        wgt = np.exp(-(u * u + v * v) * 1.6)
        acc += wgt[..., None] * hexrgb(c)
        wsum += wgt
    img = acc / wsum[..., None]

fine = rng.normal(0, P['grain'], (H, W))
clump = np.asarray(Image.fromarray(np.clip(rng.normal(128, 60, (H, W)), 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.4))).astype(float) - 128
img = img + (fine + clump * 0.35)[..., None] + rng.normal(0, 1.2, (H, W, 3))
im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
if len(sys.argv) > 2 and sys.argv[2] == 'strip':   # whole wrap, for other box sizes
    im.save(f'plates/generated/v6-ground-{name}-strip.jpg', quality=90)
for k, (x, w) in FACES.items():
    im.crop((round(x * PPM), 0, round((x + w + 6) * PPM), H)).save(f'plates/generated/v6-ground-{name}{"-long" if LONG else ""}-{k}.jpg', quality=90)
print(name, im.size)
