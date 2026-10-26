# The Christmas hamper lid, 365 x 227 mm top: an engraved Christmas garden in wine on garnet, with champagne-gold foil
# kept for the ribbons, the orchid's outline, the stars and the brand. Lower left the largest arrangement (an open
# vanilla orchid, cured pods curling along the foot, vine leaves, a ribbon flowing out from behind the flower); upper
# right a smaller answer (vine leaves, berries, a ribbon turn); fine tendrils along the edges that stop short, leaving
# gaps; a few stars; the centre left open for the logo and "The Christmas Collection".
#   python3 lid.py OUTDIR   -> lid-print.svg (ground + wine), lid-foil.svg (black = foil), lid-preview.svg, parts.json
import sys, os, json, re
import numpy as np
from shapely.geometry import Polygon, Point
from shapely.ops import unary_union
sys.path.insert(0, os.path.dirname(__file__))
import engrave as E

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
W, H, BL = 365.0, 227.0, 3.0
GARNET, WINE, IVORY = '#751F2B', '#501923', '#F2E8D8'
GAP = 0.45                                                    # the clear line between overlapping forms

rng = np.random.default_rng(12)
def pod_r(u): return np.clip(np.sin(np.pi * np.clip(u * 0.97 + 0.015, 0, 1)) ** 0.28, 0.12, 1) * (1 - 0.28 * u)
def stem_r(u): return 1 - 0.55 * u
def tendril_r(u): return 1 - 0.75 * u

# ---- the forms, back to front: (form, hatch layer, contour layer); 'foil' or 'print'
F = []
def add(form, hatch='print', contour='print'): F.append((form, hatch, contour))

# lower left: the vine up the left edge, its leaves, the big leaf under the flower
add(E.Tube([(-8, 236), (12, 214), (30, 184), (36, 150), (30, 118), (20, 86), (15, 62), (19, 50), (25, 53)], 2.1, lengthwise=True, rprofile=stem_r))
add(E.Leaf((22, 104), -118, 34, 14, bow=0.10))
add(E.Leaf((33, 148), -152, 44, 18, bow=-0.08))
add(E.Leaf((26, 190), 196, 46, 19, bow=0.09))
add(E.Leaf((56, 202), 6, 64, 24, bow=-0.07, curl=0.25))
# the pods, curling along the foot
add(E.Tube([(84, 192), (98, 214), (106, 236)], 2.6, lengthwise=True, rprofile=pod_r))
add(E.Tube([(90, 184), (122, 210), (158, 220), (190, 221), (206, 213), (209, 204), (203, 200)], 3.1, lengthwise=True, rprofile=pod_r))
add(E.Tube([(94, 178), (130, 194), (170, 202), (203, 197), (221, 186), (224, 175), (217, 171)], 3.4, lengthwise=True, rprofile=pod_r))
# the bottom-edge tendril running on from the pods, curling to an end
add(E.Tube([(206, 214), (232, 218), (256, 214), (268, 205), (264, 198), (258, 202)], 0.9, lengthwise=True, rprofile=tendril_r))
add(E.Leaf((236, 218), -20, 16, 6.5, bow=0.1))
# the ribbon: out of the left edge, behind the orchid, out over the pods and curling to its end
add(E.Band([(-8, 116), (20, 124), (52, 136), (86, 152), (118, 166), (146, 176), (170, 190), (176, 205), (166, 214), (150, 212)], 9.0,
           [15, 35, 70, 110, 150, 195, 240, 285, 325, 355]), 'foil', 'foil')
# the orchid: back tepals, then the side ones, then the lip in front
C = np.array([80.0, 146.0])
for ang, L, Wd, bend, tw in ((-96, 41, 11.5, 0.10, 0.35), (-162, 38, 11, -0.12, -0.3), (-24, 39, 11, 0.12, 0.4)):
    add(E.Petal(C, ang, L, Wd, bend=bend, twist=tw), 'print', 'foil')
for ang, L, Wd, bend, tw in ((142, 35, 10.5, 0.11, -0.3), (36, 36, 10.5, -0.10, 0.3)):
    add(E.Petal(C, ang, L, Wd, bend=bend, twist=tw), 'print', 'foil')
add(E.Bell((C[0] + 1.5, C[1] + 3.0, 6.0), (0.30, 0.55, 0.78), 17, 2.6, 9.6), 'print', 'foil')

# upper right: the vine in from the top, leaves, berries on fine stalks, a ribbon turn
add(E.Tube([(330, 6), (300, 9), (270, 8), (246, 12), (232, 20), (236, 28), (243, 24)], 0.85, lengthwise=True, rprofile=tendril_r))
add(E.Band([(250, -6), (268, 16), (288, 32), (308, 36), (322, 26), (330, 12)], 7.5, [25, 70, 130, 200, 250, 290]), 'foil', 'foil')
add(E.Tube([(296, -8), (318, 14), (336, 38), (350, 64), (360, 96), (356, 124), (349, 134), (345, 128)], 1.9, lengthwise=True, rprofile=stem_r))
for base, ang, L, Wd, bow in (((318, 15), 196, 34, 14, 0.10), ((336, 39), 158, 30, 12.5, -0.08), ((350, 66), 118, 28, 11, 0.08),
                              ((326, 25), -38, 24, 10, -0.08), ((359, 104), 210, 18, 7.5, 0.1)):
    add(E.Leaf(base, ang, L, Wd, bow=bow))
BER = [((296, 58), 4.2), ((304, 64), 3.8), ((292, 67), 3.6), ((300, 72), 3.3), ((288, 57), 3.4), ((306, 55), 3.0), ((297, 49), 2.8),
       ((343, 113), 3.4), ((337, 119), 3.0), ((347, 121), 2.7)]
for (bx, by), r in BER:
    src = (322, 30) if bx < 320 else (352, 100)
    mid = ((src[0] + bx) / 2 + 2, (src[1] + by) / 2 - 3)
    add(E.Tube([src, mid, (bx, by)], 0.45, lengthwise=True))
for (bx, by), r in BER:
    add(E.Berry((bx, by), r))

# stars and a few points of light, kept off the centre
STARS = [((136, 38), 3.6), ((116, 64), 2.0), ((62, 30), 3.0), ((94, 16), 2.0), ((176, 26), 1.6), ((254, 188), 3.0), ((284, 162), 2.2),
         ((320, 150), 3.6), ((344, 190), 2.4), ((226, 48), 2.0), ((300, 194), 1.6), ((150, 60), 1.4), ((46, 66), 1.6), ((268, 74), 1.6)]
DOTS = [(128, 48), (104, 30), (70, 46), (150, 30), (242, 196), (296, 176), (330, 172), (312, 132), (214, 40), (84, 54), (276, 150)]

def build():
    """occlusion back to front; returns print and foil geometries"""
    outlines = [f.outline() for f, _, _ in F]
    prints, foils = [], []
    for i, (f, hl, cl) in enumerate(F):
        front = unary_union(outlines[i + 1:]).buffer(GAP) if i + 1 < len(F) else None
        cut = (lambda g: g.difference(front)) if front is not None else (lambda g: g)
        hatch = f.hatch() + (f.midrib() if hasattr(f, 'midrib') else []) + (f.throat() if hasattr(f, 'throat') else [])
        cont = f.contour()
        if isinstance(f, E.Band) and hl == 'foil':
            solid = outlines[i].difference(unary_union(hatch)) if hatch else outlines[i]
            foils.append(cut(solid))
            continue
        hg = cut(unary_union(hatch)) if hatch else None; cg = cut(unary_union(cont)) if cont else None
        for g, layer in ((hg, hl), (cg, cl)):
            if g is None or g.is_empty: continue
            (foils if layer == 'foil' else prints).append(g)
    st = [E.star(c, r, 4, 0.16, rot=0) for c, r in STARS] + [E.star(c, r * 0.45, 4, 0.2, rot=45) for c, r in STARS if r > 2.5]
    foils.append(unary_union(st + [Point(*d).buffer(0.55, 16) for d in DOTS]))
    return unary_union(prints), unary_union(foils)

def logo_path():
    s = open(os.path.join(ROOT, 'brand', 'vanilla-shop-logo.svg')).read()
    d = re.search(r' d="([^"]+)"', s).group(1); vb = [float(x) for x in re.search(r'viewBox="([\d.\s]+)"', s).group(1).split()]
    return d, vb

def svgs(pr, fo, out):
    d, vb = logo_path(); lw = 58.0; sc = lw / vb[2]; lh = vb[3] * sc
    lx, ly = W / 2 - lw / 2, 64.0
    logo = lambda fill: f'<path d="{d}" fill="{fill}" fill-rule="evenodd" transform="translate({lx:.3f} {ly:.3f}) scale({sc:.6f})"/>'
    tb = ly + lh + 15.0
    text = lambda fill: (f'<text x="{W/2}" y="{tb:.2f}" text-anchor="middle" font-family="\'InstrumentSerif-Italic\'" font-size="9.2" '
                         f'fill="{fill}">The Christmas Collection</text>')
    vb_ = f'{-BL} {-BL} {W + 2*BL} {H + 2*BL}'
    head = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W + 2*BL}mm" height="{H + 2*BL}mm" viewBox="{vb_}">'
    P, Fo = E.to_path(pr), E.to_path(fo)
    open(os.path.join(out, 'lid-print.svg'), 'w').write(
        head + f'<g id="Ground"><rect x="{-BL}" y="{-BL}" width="{W+2*BL}" height="{H+2*BL}" fill="{GARNET}"/></g>'
        f'<g id="Engraving_wine"><path d="{P}" fill="{WINE}" fill-rule="nonzero"/></g></svg>')
    open(os.path.join(out, 'lid-foil.svg'), 'w').write(
        head + f'<g id="Foil_champagne_gold"><path d="{Fo}" fill="#000"/>{logo("#000")}{text("#000")}</g></svg>')
    json.dump(dict(logo=[lx, ly, lw, lh], text_baseline=tb), open(os.path.join(out, 'parts.json'), 'w'))
    return P, Fo, logo, text, head

if __name__ == '__main__':
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    pr, fo = build()
    P, Fo, logo, text, head = svgs(pr, fo, out)
    # approval preview: the ground with a faint paper grain, the wine, the foil as a champagne metal
    fonts = f"@font-face{{font-family:'InstrumentSerif-Italic';src:url(file://{ROOT}/fonts/instrument-serif-italic.ttf)}}"
    foil = ('<linearGradient id="foil" x1="0" y1="0" x2="1" y2="0.55"><stop offset="0" stop-color="#9C7C47"/><stop offset=".22" stop-color="#E9D6A6"/>'
            '<stop offset=".42" stop-color="#B8955B"/><stop offset=".63" stop-color="#F3E5BE"/><stop offset=".82" stop-color="#A9874F"/><stop offset="1" stop-color="#D9C08A"/></linearGradient>'
            '<filter id="emb" x="-5%" y="-5%" width="110%" height="110%"><feGaussianBlur in="SourceAlpha" stdDeviation="0.12"/><feOffset dx="0.10" dy="0.12"/>'
            '<feComponentTransfer><feFuncA type="linear" slope="0.55"/></feComponentTransfer><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
            '<filter id="paper"><feTurbulence type="fractalNoise" baseFrequency="2.2" numOctaves="2" seed="4"/><feColorMatrix type="matrix" '
            'values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.10 0"/></filter>')
    open(os.path.join(out, 'lid-preview.svg'), 'w').write(
        head + f'<defs><style>{fonts}</style>{foil}</defs>'
        f'<rect x="{-BL}" y="{-BL}" width="{W+2*BL}" height="{H+2*BL}" fill="{GARNET}"/>'
        f'<rect x="{-BL}" y="{-BL}" width="{W+2*BL}" height="{H+2*BL}" filter="url(#paper)"/>'
        f'<path d="{P}" fill="{WINE}"/>'
        f'<g filter="url(#emb)"><path d="{Fo}" fill="url(#foil)"/>{logo("url(#foil)")}{text("url(#foil)")}</g></svg>')
    print('ok', len(P) // 1000, 'k print,', len(Fo) // 1000, 'k foil')
