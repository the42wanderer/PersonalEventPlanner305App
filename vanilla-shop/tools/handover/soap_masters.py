# Soap boxes: Illustrator masters and a copy sheet, from the approved build (soap-boxes-final/scripts/build.py).
#   python3 soap_masters.py OUTDIR
import sys, os, re, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, '/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/soap/full')
import svgmaster as SM
import build as BD                       # the approved soap-box build (writes its own print pages on import)
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
GOLD = '#B8924A'                         # stands for the gold foil in the master; the FOIL plate PDF is the reference
FONTS = SM.Fonts({k: v for k, v in BD.kit.FONTS.items() if k in ('G', 'GB', 'IS', 'ISR', 'RW', 'NSi', 'NTa')}, ('NSi', 'NTa'))
PANELS = [('Back (printed upside down)', 'back'), ('Top wall', 'top_wall'), ('Front', 'front'), ('Left wall', 'left_wall'),
          ('Bottom wall', 'bottom_wall'), ('Right wall', 'right_wall')]

def sheet_svg(k, parts):
    W, H, B = BD.SW, BD.SH, BD.B
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W + 2 * B:.1f}mm" height="{H + 2 * B:.1f}mm" '
            f'viewBox="{-B} {-B} {W + 2 * B} {H + 2 * B}">' + ''.join(parts) + '</svg>')

def dieline():
    X0, X1, FLY, SW, SH, FY0, FY1 = BD.FX0, BD.FX1, BD.FLY, BD.SW, BD.SH, BD.FY0, BD.FY1
    cut = f'M{X0} 0H{X1}V{FLY}H{SW}V{SH}H0V{FLY}H{X0}Z'
    folds = ''.join(f'<path d="M{a} {b}L{c} {d}"/>' for a, b, c, d in
                    ((0, FY0, SW, FY0), (0, FY1, SW, FY1), (X0, FLY, X0, SH), (X1, FLY, X1, SH), (X0, FLY, X1, FLY)))
    return (f'<g id="Dieline_do_not_print"><path d="{cut}" fill="none" stroke="#EC008C" stroke-width="0.25"/>'
            f'<g fill="none" stroke="#00A0E0" stroke-width="0.2" stroke-dasharray="1.2 0.8">{folds}</g></g>')

def master(k):
    s = BD.SOAP[k]; BD.MODE = 'proof'                         # proof mode: foil shown, placeholders boxed
    art = [f'<image href="file://{BD.O}art-{k}.jpg" x="{-BD.B}" y="{-BD.B}" width="{BD.SW + 2 * BD.B}" height="{BD.SH + 2 * BD.B}" preserveAspectRatio="none"/>']
    parts, rows = [], []
    for label, fn in PANELS:
        f = getattr(BD, fn); g = f(s, k) if fn == 'back' else f(s)
        parts.append(f'<g id="{fn}">' + ''.join(g) + '</g>')
    svg = sheet_svg(k, [f'<defs>{BD.FOILG}</defs>', '<g id="art">' + art[0] + '</g>'] + parts)
    out, items = SM.convert(svg, FONTS, GOLD, f'The Vanilla Shop {BD.NAMES[k]} soap box, flat {BD.SW} x {BD.SH} mm, 3 mm bleed')
    out = out.replace('</svg>', dieline() + '</svg>')
    open(f'{OUT}/{k}_box_EDITABLE.svg', 'w', encoding='utf-8').write(out)
    return svg, out, items

if __name__ == '__main__':
    res = {}
    for k in BD.SOAP:
        res[k] = master(k)
    json.dump({k: [dict(i, ctm=list(i['ctm'])) for i in v[2]] for k, v in res.items()}, open(f'{OUT}/_items.json', 'w'), ensure_ascii=False)
    for k, (ref, out, _) in res.items():
        open(f'{OUT}/_ref-{k}.svg', 'w', encoding='utf-8').write(ref)
    print('ok', {k: len(v[2]) for k, v in res.items()})
