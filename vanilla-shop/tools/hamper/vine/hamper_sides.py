# The Christmas hamper lid's sides, 14.5 x 9 x 4.5 in box, drawn with the lid top's own vocabulary (draw_hamper_v3.py).
#
# How the sides are seen, and what follows from it:
#  - On a table or a shelf the box is seen from above at 30-45 degrees: the top, one long side and one end at once.
#    The sides are foreshortened, so they carry fewer, larger forms than the top, laid horizontally.
#  - Stacked, shelved, or wrapped in hamper cellophane with a bow, the top is covered and a side faces the viewer,
#    so each long side carries the logo and the collection name; each end carries the logo alone.
#  - The content sits in the middle band of the skirt: the lid's top edge is where hands lift and scuff it, the
#    lower edge sits in the shadow of the lid over the base.
#  - The vine runs out from the centre and stops well short of the corners, where the wrap folds and wears; the
#    double rule, a single continuous line, carries round the corners instead and echoes the top's border.
#  - The lid depth is LID_D (3.5 in by default), leaving 1 in of the base showing below the lid; the base walls are
#    plain garnet with the tone-on-tone ground.
#   python3 hamper_sides.py OUTDIR  -> side-long.svg, side-end.svg, lid-wrap-layout.svg, base-wall.svg
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import draw_hamper_v3 as V
from draw_hamper_v3 import p, place, group, leaf, berries, fir, star_anise, sparkle, R, G, I, MM, IN

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent
LID_D = 3.5 * IN                     # lid skirt depth
BOX_H = 4.5 * IN
LONG_W, END_W = V.TOP_W, V.TOP_H
TURN = 15 * MM                       # turn-in round the lid's lower edge, inside the skirt

def garland(x0, x1, y, seed=0):
    """a vine running left from x0 to x1 on the line y, leaves alternating above and below, a berry sprig and a fir
    tip along it, a star anise where it ends; drawn for the left half and mirrored by the caller"""
    L = x0 - x1; out = []
    out.append(p(f'M{x0} {y} C{x0-L*0.25} {y-12} {x0-L*0.42} {y+12} {x0-L*0.62} {y} C{x0-L*0.78} {y-10} {x1+L*0.10} {y+8} {x1} {y-2}',
                 'none', G, 2.4))
    styles = ['light', 'gold', 'muted', 'light', 'dark', 'gold', 'light', 'muted']
    n = max(5, int(L / 40))
    for i in range(n):
        t = (i + 0.6) / (n + 0.4); x = x0 - L * t; up = i % 2 == 0
        a = (-58 if up else -122) + (6 if i % 3 == 1 else -4)
        s = 0.52 - 0.14 * t
        out.append(place(leaf((i + seed) % 5, styles[(i + seed) % len(styles)]), round(x, 1), y + (-2 if up else 2), a, round(s, 3)))
    out.insert(1, place(fir(), round(x0 - L * 0.80, 1), y, -78, 0.5))
    out.insert(1, place(leaf(1, 'muted'), round(x0 - L * 0.30, 1), y, -100, 0.55))
    out.insert(1, place(leaf(0, 'muted'), round(x0 - L * 0.62, 1), y, -70, 0.5))
    out.append(place(berries(), round(x0 - L * 0.38, 1), y - 4, -28, 0.5))
    out.append(place(berries(), round(x0 - L * 0.70, 1), y + 4, -150, 0.42))
    out.append(place(star_anise(), round(x1 - 38, 1), y - 2, 8, 0.6))
    return ''.join(out)

def panel(W, H, centre, reach):
    """a lid side W x H: ground, double rule (no centre break), centre content, and the garland both ways"""
    cx, cy = W / 2, H / 2
    g = garland(round(cx - reach[0], 1), round(reach[1], 1), round(cy, 1))
    mirror = f'<g transform="translate({W:.2f} 0) scale(-1 1)">{g}</g>'
    stars = ''.join(sparkle(round(x, 1), round(y, 1), r) for x, y, r in
                    [(cx - reach[0] * 0.55 - 30, cy - 96, 7), (cx + reach[0] * 0.55 + 30, cy - 96, 7),
                     (cx - reach[0] * 0.9 - 60, cy + 92, 5), (cx + reach[0] * 0.9 + 60, cy + 92, 5)])
    return (f'<g id="background"><rect x="{-V.BLEED}" y="{-V.BLEED}" width="{W+2*V.BLEED:.2f}" height="{H+2*V.BLEED:.2f}" fill="{R}"/></g>'
            f'<g id="ground-pattern">{V.ground_pattern(W+V.BLEED, H+V.BLEED, -int(V.BLEED), -int(V.BLEED))}</g>'
            f'<g id="border">{V.border(W, H, mid=False)}</g>'
            f'<g id="garland">{g}{mirror}{stars}</g>{centre}')

def long_side():
    W, H = LONG_W, LID_D; cx, cy = W / 2, H / 2
    lh, gap, fs = 140, 24, 46                       # logo height, gap, title size (units, 4 per mm)
    top = cy - (lh + gap + fs * 0.75) / 2
    c = (V.logo_mark(round(cx, 2), round(top, 2), lh) +
         f'<g id="editable-type" fill="{I}" text-anchor="middle"><text x="{cx:.2f}" y="{top+lh+gap+fs*0.75:.2f}" '
         f'font-family="\'InstrumentSerif-Italic\'" font-size="{fs}">The Christmas Collection</text></g>')
    return panel(W, H, c, (300, 120))

def end_side():
    W, H = END_W, LID_D; cx, cy = W / 2, H / 2
    lh = 168
    return panel(W, H, V.logo_mark(round(cx, 2), round(cy - lh / 2, 2), lh), (118, 110))

def base_wall(W):
    H = BOX_H
    return (f'<g id="background"><rect x="{-V.BLEED}" y="{-V.BLEED}" width="{W+2*V.BLEED:.2f}" height="{H+2*V.BLEED:.2f}" fill="{R}"/></g>'
            f'<g id="ground-pattern">{V.ground_pattern(W+V.BLEED, H+V.BLEED, -int(V.BLEED), -int(V.BLEED))}</g>')

def wrap_layout():
    """the lid wrap laid flat: the top, each side folded down from its edge (art upright when folded), a turn-in
    beyond each side. Indicative only: the box maker's dieline sets the corner flaps and the turn-in."""
    W, H, D, T = V.TOP_W, V.TOP_H, LID_D, TURN
    ox, oy = D + T, D + T                       # top's origin on the sheet
    SW, SH = W + 2 * (D + T), H + 2 * (D + T)
    clips = {'top': (ox, oy, W, H), 'side-front': (ox, oy + H, W, D), 'side-back': (ox, oy - D, W, D),
             'side-left': (ox - D, oy, D, H), 'side-right': (ox + W, oy, D, H)}
    defs = '<defs>' + ''.join(f'<clipPath id="c-{k}"><rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}"/></clipPath>'
                              for k, (x, y, w, h) in clips.items()) + '</defs>'
    clip = lambda k, tr, body: f'<g id="{k}" clip-path="url(#c-{k})"><g transform="{tr}">{body}</g></g>'
    L, E = long_side(), end_side()
    # front skirt below the top, upright; back above, turned 180; ends left and right, turned +-90
    top = clip('top', f'translate({ox:.2f} {oy:.2f})', V.top_body(True))
    sides = (clip('side-front', f'translate({ox:.2f} {oy+H:.2f})', L) + clip('side-back', f'translate({ox+W:.2f} {oy:.2f}) rotate(180)', L)
             + clip('side-left', f'translate({ox:.2f} {oy:.2f}) rotate(90)', E) + clip('side-right', f'translate({ox+W:.2f} {oy+H:.2f}) rotate(-90)', E))
    turn = (f'<path d="M{ox} 0H{ox+W}V{T}H{ox}Z M{ox} {SH-T}H{ox+W}V{SH}H{ox}Z M0 {oy}H{T}V{oy+H}H0Z M{SW-T} {oy}H{SW}V{oy+H}H{SW-T}Z" fill="{R}"/>')
    cut = (f'<g id="dieline-indicative" fill="none" stroke="#EC008C" stroke-width="0.6">'
           f'<rect x="{ox}" y="{oy}" width="{W:.2f}" height="{H:.2f}" stroke-dasharray="6 4"/>'
           f'<rect x="{ox}" y="{oy-D}" width="{W:.2f}" height="{H+2*D:.2f}" stroke-dasharray="6 4"/>'
           f'<rect x="{ox-D}" y="{oy}" width="{W+2*D:.2f}" height="{H:.2f}" stroke-dasharray="6 4"/></g>')
    body = f'{defs}<rect width="{SW:.2f}" height="{SH:.2f}" fill="#FFFFFF"/>{turn}{sides}{top}{cut}'
    return SW, SH, body

if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'side-long.svg').write_text(V.svg(LONG_W, LID_D, long_side(), 'Christmas hamper lid, long side (x2), 14.5 x 3.5 in'))
    (OUT / 'side-end.svg').write_text(V.svg(END_W, LID_D, end_side(), 'Christmas hamper lid, end (x2), 9 x 3.5 in'))
    (OUT / 'base-wall-long.svg').write_text(V.svg(LONG_W - 6 * MM, BOX_H, base_wall(LONG_W - 6 * MM), 'Christmas hamper base wall'))
    SW, SH, body = wrap_layout()
    (OUT / 'lid-wrap-layout.svg').write_text(V.svg(SW, SH, body, 'Christmas hamper lid wrap, flat layout (indicative)', b=0))
    print('sides written', OUT)
