# The long box's landscape/cream edge, unrolled round the four walls, with the type's ink and the clearance line.
# BOX=long python3 curve_diagram.py <ink.json> <out.png>
import json, sys, glob, numpy as np
import boundary as BD
from PIL import Image, ImageDraw, ImageFont
ink, out = sys.argv[1], sys.argv[2]
F = glob.glob('/usr/share/fonts/**/*.ttf', recursive=True)
f = ImageFont.truetype([p for p in F if p.endswith('DejaVuSans.ttf')][0], 22); fb = ImageFont.truetype([p for p in F if p.endswith('DejaVuSans-Bold.ttf')][0], 26)
fm = ImageFont.truetype([p for p in F if p.endswith('DejaVuSansMono.ttf')][0], 22)
s = 4.4; ox, oy = 60, 170; W = int(BD.P * s) + 2 * ox; Hh = int(BD.H * s) + oy + 150
im = Image.new('RGB', (W, Hh), (250, 247, 240)); d = ImageDraw.Draw(im)
X = lambda u: ox + u * s; Y = lambda y: oy + y * s
d.rectangle([X(0), Y(0), X(BD.P), Y(BD.H)], outline=(120, 110, 100), width=2)
d.rectangle([X(BD.F), Y(0), X(BD.F + BD.SA), Y(BD.H)], fill=(72, 30, 58))
for name, a in (('front', 0), ('How to brew (plum, no cream)', BD.F), ('back', BD.F + BD.SA), ("what's inside", BD.F + BD.SA + BD.BK)):
    d.text((X(a) + 8, Y(0) - 32), name, fill=(60, 50, 45), font=f)
for u in (BD.F, BD.F + BD.SA, BD.F + BD.SA + BD.BK): d.line([X(u), Y(0) - 6, X(u), Y(BD.H) + 6], fill=(228, 0, 124), width=2)
for u in (BD.VM['MU'], BD.VM['MU2']):
    for yy in range(int(Y(0)), int(Y(BD.H)), 12): d.line([X(u), yy, X(u), yy + 6], fill=(150, 70, 40), width=1)
for g in json.load(open(ink)):
    if g['panel'] in BD.ORIGIN and g['panel'] != 'sideA':
        o = BD.ORIGIN[g['panel']]; d.rectangle([X(o + g['x0']), Y(g['y0']), X(o + g['x1']), Y(g['y1'])], fill=(205, 190, 165))
u = np.linspace(0, BD.P, 4000); y = BD.y(u)
d.line([(X(a), Y(b)) for a, b in zip(u, y)], fill=(150, 70, 40), width=4)
d.line([(X(a), Y(b + BD.CLEAR)) for a, b in zip(u, y)], fill=(150, 70, 40), width=1)
v = BD.VM
d.text((ox, 20), 'The 25-bag carton: the landscape/cream edge, unrolled round the four walls (u in mm, y down)', fill=(30, 25, 20), font=fb)
d.text((ox, 62), 'y(u) = H [ Y0 + A exp(k(cos(2pi(u-m)/P) - 1)) + A2 exp(k2(cos(2pi(u-m2)/P) - 1)) ]', fill=(30, 25, 20), font=fm)
d.text((ox, 92), f"H = {BD.H} mm, P = {BD.P:.2f} mm;  Y0 = {v['Y0']}, A = {v['A']}, k = {v['KAPPA']:g}, m = {v['MU']:g} mm (under the logo);  A2 = {v['A2']}, k2 = {v['KAPPA2']:g}, m2 = {v['MU2']:.1f} mm (centre of the back)", fill=(60, 50, 45), font=f)
d.text((ox, Y(BD.H) + 20), 'thick: the edge;  thin: 0.04 H below it, the clear space every glyph keeps (tan: the ink of the type and the lion);  dashed: m and m2;  magenta: folds', fill=(60, 50, 45), font=f)
d.text((ox, Y(BD.H) + 52), 'periodic in P, so it meets itself at the glue flap with every derivative equal; no anchors, no joins', fill=(60, 50, 45), font=f)
im.save(out); print('lift', BD.lift(ink, ('sideA',)))
