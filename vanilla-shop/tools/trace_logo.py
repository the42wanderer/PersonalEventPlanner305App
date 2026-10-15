"""Trace a raster logo into a single-colour vector SVG.

Usage: python3 tools/trace_logo.py SOURCE OUT.svg [#hex] [title]
Writes a tightly cropped SVG with one evenodd path, recoloured with the given fill.
"""
import sys
import numpy as np
import potrace
from PIL import Image

src, out = sys.argv[1], sys.argv[2]
fill = sys.argv[3] if len(sys.argv) > 3 else '#143A1D'
title = sys.argv[4] if len(sys.argv) > 4 else 'The Vanilla Shop'
im = Image.open(src).convert('RGBA')
if im.width < 1200:  # upscale small sources so the trace has smoother curves
    im = im.resize((im.width * 4, im.height * 4), Image.LANCZOS)
a = np.asarray(im).astype(float)
lum = a[..., :3].mean(2)
# Ink = anything clearly darker than white (works for black or coloured marks).
ink = (a[..., 3] > 127) & (np.sqrt(((a[..., :3] - 255) ** 2).sum(2)) > 90)
pad = 6
ink = np.pad(ink, pad)  # marks that touch the image edge still get a clean outline
ys, xs = np.where(ink)
ink = ink[ys.min() - pad:ys.max() + pad, xs.min() - pad:xs.max() + pad]

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
       f'<title>{title}</title><path fill="{fill}" fill-rule="evenodd" d="{"".join(d)}"/></svg>')
open(out, 'w').write(svg)
print(out, w, 'x', h, len(paths), 'shapes', len(svg) // 1024, 'KB')
