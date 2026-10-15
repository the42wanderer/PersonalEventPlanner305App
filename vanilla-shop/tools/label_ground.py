"""Angled, grainy gradient grounds for the pouch labels (76 x 116 mm incl. bleed), in the same family
as the boxes' golden hour but tuned to stand off brown kraft. One preset per name; each makes a
vanilla and a cinnamon version (the cinnamon one warmer).
Usage: python3 tools/label_ground.py NAME  ->  plates/generated/v6-label-ground-NAME-{vanilla,cinnamon}.jpg
"""
import sys
import numpy as np
from PIL import Image, ImageFilter

PPM, WMM, HMM = 12, 76, 116
PRESETS = {
    # The painting's own sky: cream light top-left, butter, a soft rose-mauve dusk low right.
    'dusk':  {'angle': 58, 'vanilla': ['#FCF5E6', '#F9E9C4', '#F1D3B6', '#DDB7BC'], 'cinnamon': ['#FCF3E4', '#F6DFBF', '#EBC0A0', '#D69E94']},
    # Morning sage: cream into pale pistachio; green reads "tea" and parts cleanly from brown.
    'sage':  {'angle': 58, 'vanilla': ['#FBF6E8', '#F1F0D6', '#DFE6C6', '#C9D6B8'], 'cinnamon': ['#FBF4E6', '#F3E8D0', '#E6D2B4', '#D2B79A']},
    # Lilac haze: cream into a light lavender-mauve, the coolest against kraft.
    'lilac': {'angle': 58, 'vanilla': ['#FCF6EC', '#F5EADF', '#E7DAE2', '#D3C4D8'], 'cinnamon': ['#FCF4E9', '#F4E2D4', '#E6CBC6', '#D3B0AE']},
}
hexrgb = lambda c: np.array([int(c[i:i + 2], 16) for i in (1, 3, 5)], float)
name = sys.argv[1]; P = PRESETS[name]
W, H = WMM * PPM, HMM * PPM
yy, xx = np.mgrid[0:H, 0:W] / PPM
rng = np.random.default_rng(23)
a = np.radians(P['angle'])
t = (xx * np.cos(a) + yy * np.sin(a)); t = (t - t.min()) / (t.max() - t.min())
# A soft wave across the sweep so the bands are not ruler-straight.
t = np.clip(t + 0.035 * np.sin(xx / 9 + yy / 23), 0, 1)
for kind in ('vanilla', 'cinnamon'):
    cols = np.array([hexrgb(c) for c in P[kind]]); pos = np.linspace(0, 1, len(cols))
    img = np.stack([np.interp(t, pos, cols[:, k]) for k in range(3)], 2)
    fine = rng.normal(0, 6.5, (H, W))
    clump = np.asarray(Image.fromarray(np.clip(rng.normal(128, 60, (H, W)), 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.4))).astype(float) - 128
    img = img + (fine + clump * 0.3)[..., None] + rng.normal(0, 1.2, (H, W, 3))
    Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).save(f'plates/generated/v6-label-ground-{name}-{kind}.jpg', quality=90)
print(name)
