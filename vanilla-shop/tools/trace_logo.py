"""Trace the raster Vanilla Shop logo into a single-colour vector SVG.

Usage: python3 tools/trace_logo.py brand/logo-source.webp brand/vanilla-shop-logo.svg [#hex]
Writes a tightly cropped SVG with one evenodd path, recoloured with the given fill.
"""
import sys
import numpy as np
import potrace
from PIL import Image

src, out = sys.argv[1], sys.argv[2]
fill = sys.argv[3] if len(sys.argv) > 3 else '#143A1D'
im = Image.open(src).convert('RGBA')
a = np.asarray(im).astype(float)
lum = a[..., :3].mean(2)
ink = (a[..., 3] > 127) & (lum < 128)
ys, xs = np.where(ink)
pad = 6
y0, y1, x0, x1 = ys.min() - pad, ys.max() + pad, xs.min() - pad, xs.max() + pad
ink = ink[y0:y1, x0:x1]

# potracer treats False as ink, so pass the inverse.
paths = potrace.Bitmap(~ink).trace(turdsize=4, alphamax=1.0, opticurve=True, opttolerance=0.2)
f = lambda p: f'{p.x:.2f} {p.y:.2f}'
d = []
for curve in paths:
    d.append('M' + f(curve.start_point))
    for seg in curve.segments:
        if seg.is_corner:
            d.append('L' + f(seg.c) + 'L' + f(seg.end_point))
        else:
            d.append('C' + f(seg.c1) + ' ' + f(seg.c2) + ' ' + f(seg.end_point))
    d.append('Z')
h, w = ink.shape
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
       f'<title>The Vanilla Shop</title><path fill="{fill}" fill-rule="evenodd" d="{"".join(d)}"/></svg>')
open(out, 'w').write(svg)
print(out, w, 'x', h, len(paths), 'shapes', len(svg) // 1024, 'KB')
