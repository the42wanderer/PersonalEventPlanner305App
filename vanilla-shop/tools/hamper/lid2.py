# The Christmas hamper lid, 365 x 227 mm, assembled from the tested elements in forms.py.
# Legibility at arm's length comes from flat fills (ivory, a muted rose tint, champagne foil) laid on the garnet;
# the wine engraving sits on top of those fills, where it has contrast, and carries the craft up close.
# Asymmetric frame: the large arrangement lower left (open vanilla orchid, leaves, pods along the foot, a ribbon),
# a smaller answer upper right (a second orchid, leaves, berries, a fir sprig, a ribbon turn), foil vines running on
# along the edges and stopping short, stars in the gaps, the centre open for the logo and the collection name.
#   python3 lid2.py OUTDIR  -> lid-print.svg (garnet, rose, ivory, wine), lid-foil.svg (black = foil), lid-preview.svg
import sys, os, re
import numpy as np
from shapely.geometry import Point, Polygon
from shapely.ops import unary_union
from shapely import affinity
sys.path.insert(0, os.path.dirname(__file__))
import forms as Fm
import engrave as E

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
W, H, BL = 365.0, 227.0, 3.0
COL = dict(garnet='#751F2B', rose='#93404B', ivory='#F2E8D8', wine='#330C14')
GAP = 0.45                     # garnet line left between overlapping forms
SPEC = Fm.SPEC

ITEMS = []                     # back to front: dict(sil=geometry, parts=[(geometry, colour)])
def add(sil, parts): ITEMS.append(dict(sil=sil, parts=[(g, c) for g, c in parts if g is not None and not g.is_empty]))
U = lambda gs: unary_union([g for g in gs if g is not None])

def mirror(g, cx): return affinity.scale(g, -1, 1, origin=(cx, 0))

# ---- elements --------------------------------------------------------------------------------------------------
def leaf(base, ang, L, Wd, kind, bow=0.07, flip=1, asym=0.12):
    lf = Fm.Leaf(base, ang, L, Wd, bow=bow, flip=flip, asym=asym); o = lf.outline()
    if kind == 'foil':                                   # solid foil, its veins and shading cut through to the garnet
        cuts = U(lf.engrave('foil')).intersection(o.buffer(-0.35)).buffer(0.03)
        g = o.difference(cuts).buffer(-SPEC['foil']['min_line'] / 2).buffer(SPEC['foil']['min_line'] / 2).intersection(o)
        add(o, [(Fm.drop_specks(g, SPEC['foil']['min_line']), 'foil')])
    else:
        add(o, [(o, kind), (U(lf.engrave('print')), 'wine')])

def pod(a, b, bow=0.05, flip=1):
    p = Fm.Pod(a, b, bow=bow, flip=flip); o = p.outline()
    add(o, [(o, 'rose'), (U(p.engrave_negative('print')), 'wine')])

def orchid(c, s, flipx=False, ang_lip=30):
    f = Fm.BrandFlower(c, ang_lip, s); hatch, outl = f.engrave_parts('print')
    m = (lambda g: mirror(g, c[0])) if flipx else (lambda g: g)
    sil = m(f.silhouette())
    throat = m(f.throat.buffer(-0.25))
    add(sil, [(sil, 'ivory'), (m(U(hatch)), 'wine'), (m(U(outl)), 'wine'), (throat, 'foil')])

def ribbon(segs, Wd, notch=(True, True)):
    r = Fm.FoldRibbon(segs, Wd, notch=notch)
    add(r.silhouette(), [(U(r.engrave('foil')), 'foil')])

def stem(pts, w0, w1, kind='foil'):
    C = E.resample(E.catmull(pts, 400), 300)
    g = E.ribbon_poly(C, np.linspace(w0, w1, len(C)), taper=0.6)
    add(g, [(g, kind)])

def berries(cl):
    """foil berries on fine stalks from a common point: a solid disc with a soft crescent of light cut from it"""
    hub = np.mean([c for c, _ in cl], 0) + np.array([4.0, -6.0])
    for (x, y), r in cl:
        mid = (hub + np.array([x, y])) / 2 + np.array([1.2, -0.8])
        stem([tuple(hub), tuple(mid), (x, y)], 0.32, 0.22)
    for (x, y), r in cl:
        d = Point(x, y).buffer(r, 64); L = Fm.LIGHT2D
        hi = Point(x + L[0] * r * 0.30, y + L[1] * r * 0.30).buffer(r * 0.52, 48).difference(
             Point(x + L[0] * r * 0.18, y + L[1] * r * 0.18).buffer(r * 0.50, 48))
        hi = hi.buffer(-0.06).buffer(0.06)
        cal = Point(x - L[0] * r * 0.62, y - L[1] * r * 0.62).buffer(max(0.25, r * 0.08), 16)
        add(d, [(d.difference(U([hi, cal])), 'foil')])

def fir(pts, L0, kind='rose', dens=1.4):
    """an evergreen sprig: a tapered stem with needles set forward along it, shortening to the tip"""
    C = E.resample(E.catmull(pts, 400), 400); T, N = E.frames(C)
    s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(C, axis=0), axis=1))]; Ltot = s[-1]
    parts = [E.ribbon_poly(C, np.linspace(0.8, 0.3, len(C)), taper=0.5)]
    for side in (1, -1):
        for sk in np.arange(2.0 + (0.5 if side < 0 else 0), Ltot - 0.6, dens):
            i = np.searchsorted(s, sk); u = sk / Ltot
            ln = L0 * (0.55 + 0.45 * np.sin(np.pi * min(1, 0.25 + u * 0.9))) * (1 - 0.55 * u ** 2)
            a = np.radians(42 + 8 * np.sin(sk * 1.7))
            d = T[i] * np.cos(a) + N[i] * side * np.sin(a)
            P = np.array([C[i] + d * ln * k + N[i] * side * 0.12 * ln * np.sin(np.pi * k) for k in np.linspace(0, 1, 12)])
            parts.append(E.ribbon_poly(P, np.linspace(0.75, 0.24, 12), taper=0.4))
    g = U(parts)
    add(g, [(g, kind)])

def stars(lst):
    for (x, y), r in lst:
        g = E.star((x, y), r, 4, 0.16)
        if r > 2.4: g = g.union(E.star((x, y), r * 0.42, 4, 0.22, rot=45))
        add(g, [(g, 'foil')])

# ---- composition -----------------------------------------------------------------------------------------------
def vine(pts, leaves, w0=1.0, w1=0.22):
    """a foil vine with leaves set along it: leaves = (u along the vine, side, length, kind)"""
    C = E.resample(E.catmull(pts, 400), 400); T, N = E.frames(C)
    stem(pts, w0, w1)
    for u, side, ln, kind in leaves:
        i = int(u * (len(C) - 1)); a = np.degrees(np.arctan2(*(T[i] * 0.55 + N[i] * side * 0.83)[::-1]))
        leaf(tuple(C[i]), a, ln, ln * 0.36, kind, bow=0.08 * side, flip=side)

# lower left, back to front
vine([(52, 150), (34, 124), (24, 96), (24, 70), (32, 48), (46, 34), (60, 30), (64, 37), (58, 40)],
     [(0.18, 1, 24, 'ivory'), (0.30, -1, 22, 'rose'), (0.46, 1, 20, 'foil'), (0.60, -1, 17, 'ivory'), (0.74, 1, 14, 'rose')])
vine([(200, 214), (232, 220), (262, 216), (284, 206), (292, 194), (288, 186), (281, 190)],
     [(0.22, -1, 18, 'ivory'), (0.40, 1, 15, 'rose'), (0.58, -1, 14, 'foil'), (0.76, 1, 11, 'ivory')], 0.9, 0.2)
fir([(70, 178), (44, 196), (20, 212), (2, 226)], 7.0, 'foil', 1.5)
fir([(76, 160), (52, 132), (40, 112), (34, 92)], 6.0, 'rose', 1.4)
leaf((74, 168), 194, 80, 27, 'rose', bow=0.07)
leaf((80, 160), -122, 78, 26, 'foil', bow=-0.06, flip=-1)
leaf((86, 182), 158, 68, 23, 'ivory', bow=0.08)
leaf((112, 186), 6, 74, 23, 'rose', bow=-0.06, flip=-1)
leaf((104, 168), -50, 62, 21, 'ivory', bow=0.07)
pod((104, 190), (232, 204), bow=0.05)
pod((100, 196), (214, 220), bow=0.035, flip=-1)
pod((108, 184), (196, 172), bow=0.06, flip=-1)
ribbon([[(-6, 112), (22, 118), (52, 132), (78, 154), (104, 180), (134, 196), (166, 200)],
        [(166, 200), (186, 210), (196, 224)], [(196, 224), (214, 226), (236, 220)]], 9.5)
berries([((136, 168), 3.8), ((143, 174), 3.3), ((133, 177), 3.0), ((145, 165), 2.6)])
orchid((92, 148), 3.0)
leaf((70, 192), 214, 40, 13, 'ivory', bow=0.08)

# upper right, back to front
vine([(270, 14), (240, 8), (212, 9), (192, 16), (194, 25), (201, 22)],
     [(0.20, 1, 16, 'ivory'), (0.42, -1, 14, 'rose'), (0.62, 1, 12, 'foil')], 0.9, 0.2)
vine([(330, 86), (346, 110), (354, 138), (350, 164), (342, 172), (338, 165)],
     [(0.22, 1, 17, 'ivory'), (0.44, -1, 15, 'rose'), (0.66, 1, 12, 'foil')], 1.0, 0.22)
fir([(318, 44), (338, 28), (356, 12), (370, 2)], 6.0, 'rose', 1.4)
leaf((306, 56), -140, 58, 20, 'rose', bow=0.07)
leaf((312, 58), -32, 62, 21, 'foil', bow=-0.07, flip=-1)
leaf((318, 72), 50, 56, 19, 'ivory', bow=0.08)
leaf((320, 64), 8, 46, 16, 'rose', bow=-0.07, flip=-1)
ribbon([[(252, -6), (266, 18), (290, 34)], [(290, 34), (272, 48), (258, 64)]], 7.5)
berries([((270, 70), 3.4), ((277, 76), 3.0), ((267, 78), 2.7), ((279, 67), 2.3)])
orchid((304, 66), 2.0, flipx=True)

stars([((150, 32), 3.4), ((128, 22), 1.8), ((222, 38), 2.0), ((112, 64), 2.2), ((300, 172), 3.4), ((324, 198), 2.0),
       ((268, 166), 1.6), ((170, 222), 1.6), ((330, 128), 1.4), ((82, 20), 1.6), ((246, 92), 1.4)])
for x, y in [(140, 46), (120, 36), (236, 48), (120, 84), (284, 152), (312, 186), (256, 180), (96, 52)]:
    g = Point(x, y).buffer(0.55, 16); add(g, [(g, 'foil')])

def build():
    layers = {k: [] for k in ('rose', 'ivory', 'wine', 'foil')}; front = None
    for it in reversed(ITEMS):
        cut = front.buffer(GAP) if front is not None else None
        for g, c in it['parts']:
            layers[c].append(g.difference(cut) if cut is not None else g)
        front = it['sil'] if front is None else front.union(it['sil'])
    frame = Polygon([(-BL, -BL), (W + BL, -BL), (W + BL, H + BL), (-BL, H + BL)])
    return {k: U(v).intersection(frame) for k, v in layers.items()}

# ---- centre: the logo and the collection name ------------------------------------------------------------------
def logo_path():
    s = open(os.path.join(ROOT, 'brand', 'vanilla-shop-logo.svg')).read()
    d = re.search(r' d="([^"]+)"', s).group(1); vb = [float(x) for x in re.search(r'viewBox="([\d.\s]+)"', s).group(1).split()]
    return d, vb

def centre(fill):
    d, vb = logo_path(); lw = 64.0; sc = lw / vb[2]; lh = vb[3] * sc
    cx = W / 2 + 6; ly = 72.0; lx = cx - lw / 2
    rule_y = ly + lh + 9; tb = rule_y + 15
    g = (f'<path d="{d}" fill="{fill}" fill-rule="evenodd" transform="translate({lx:.3f} {ly:.3f}) scale({sc:.6f})"/>'
         f'<path d="M{cx-18:.2f} {rule_y:.2f}H{cx-2.2:.2f}M{cx+2.2:.2f} {rule_y:.2f}H{cx+18:.2f}" stroke="{fill}" stroke-width="0.22"/>'
         f'<path d="{E.to_path(E.star((cx, rule_y), 1.5, 4, 0.2))}" fill="{fill}"/>'
         f'<text x="{cx:.2f}" y="{tb:.2f}" text-anchor="middle" font-family="\'InstrumentSerif-Italic\'" font-size="11.5" '
         f'fill="{fill}">The Christmas Collection</text>')
    return g

if __name__ == '__main__':
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    L = build(); P = {k: E.to_path(g) for k, g in L.items()}
    vb_ = f'{-BL} {-BL} {W + 2*BL} {H + 2*BL}'
    head = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W + 2*BL}mm" height="{H + 2*BL}mm" viewBox="{vb_}">'
    ground = f'<rect x="{-BL}" y="{-BL}" width="{W+2*BL}" height="{H+2*BL}" fill="{COL["garnet"]}"/>'
    open(os.path.join(out, 'lid-print.svg'), 'w').write(
        head + f'<g id="Ground">{ground}</g><g id="Rose_tint"><path d="{P["rose"]}" fill="{COL["rose"]}"/></g>'
        f'<g id="Ivory"><path d="{P["ivory"]}" fill="{COL["ivory"]}"/></g><g id="Wine_engraving"><path d="{P["wine"]}" fill="{COL["wine"]}"/></g></svg>')
    open(os.path.join(out, 'lid-foil.svg'), 'w').write(head + f'<g id="Foil_champagne_gold"><path d="{P["foil"]}" fill="#000"/>{centre("#000")}</g></svg>')
    import base64
    b64 = base64.b64encode(open(os.path.join(ROOT, 'fonts', 'instrument-serif-italic.ttf'), 'rb').read()).decode()
    fonts = f"@font-face{{font-family:'InstrumentSerif-Italic';src:url(data:font/ttf;base64,{b64})}}"
    foil = ('<linearGradient id="foil" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="365" y2="227"><stop offset="0" stop-color="#B08F55"/>'
            '<stop offset=".18" stop-color="#E6D2A0"/><stop offset=".36" stop-color="#BE9D62"/><stop offset=".55" stop-color="#EEDDB2"/>'
            '<stop offset=".74" stop-color="#B39158"/><stop offset=".9" stop-color="#E2CB95"/><stop offset="1" stop-color="#B8975C"/></linearGradient>'
            '<filter id="paper"><feTurbulence type="fractalNoise" baseFrequency="2.2" numOctaves="2" seed="4"/><feColorMatrix type="matrix" '
            'values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.08 0"/></filter>')
    open(os.path.join(out, 'lid-preview.svg'), 'w').write(
        head + f'<defs><style>{fonts}</style>{foil}</defs>{ground}'
        f'<rect x="{-BL}" y="{-BL}" width="{W+2*BL}" height="{H+2*BL}" filter="url(#paper)"/>'
        f'<path d="{P["rose"]}" fill="{COL["rose"]}"/><path d="{P["ivory"]}" fill="{COL["ivory"]}"/>'
        f'<path d="{P["wine"]}" fill="{COL["wine"]}"/><path d="{P["foil"]}" fill="url(#foil)"/>{centre("url(#foil)")}</svg>')
    print('ok', {k: len(v) // 1000 for k, v in P.items()})
