# Colour study for the jar labels: each option paints the jar's art in its own palette (derived from one ground colour)
# and sets the label's inks to match.  python3 jarcolours.py OUTDIR
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comp as C, jarart as JA, jarwrap as JW
from comp import mix
def pal(g, light):
    return dict(ground=g, tep_core=mix('#FFFFFF', g, 0.05), tep_edge=mix(g, '#FFFFFF', 0.5 if not light else 0.35),
                lip_core=mix('#FFFFFF', g, 0.03), lip_edge=mix(g, '#FFFFFF', 0.68), throat_core='#F2C460', throat_edge='#D99A42',
                leaf_core=mix(g, '#FFFFFF', 0.3), leaf_edge=mix(g, '#000000', 0.45), pod_core=mix('#2A160C', g, 0.15),
                pod_edge=mix('#140A05', g, 0.1), bud_core=mix('#FFFFFF', g, 0.12), bud_edge=mix(g, '#FFFFFF', 0.35), stem=mix(g, '#FFFFFF', 0.3))
def look(g, light):
    if light: return dict(dark=mix(g, '#000000', 0.72), deep=mix(g, '#000000', 0.45), on=mix(g, '#000000', 0.72), on2=mix(g, '#000000', 0.5))
    return dict(dark=mix(g, '#000000', 0.45), deep=g if mix(g, '#000000', 0) else g, on=mix('#FFFFFF', g, 0.08), on2=mix(g, '#FFFFFF', 0.62))
OPTS = {'04': [('Cocoa', '#5E3A2A', False), ('Burnt caramel', '#9A5126', False), ('Deep teal', '#1E5B5E', False), ('Midnight blue', '#24365A', False)],
        '05': [('Plum', '#6A2C4A', False), ('Oat', '#D8BE92', True), ('Dusty rose', '#C4877F', True), ('Orchid lilac', '#8C78AE', False)]}
if __name__ == '__main__':
    out = sys.argv[1]; JW.JAR['05']['si'] = 'වැනිලා පිටි'
    for k, opts in OPTS.items():
        for i, (name, g, light) in enumerate(opts):
            d = f'{out}/{k}-{i}'; os.makedirs(d, exist_ok=True)
            C.PAL[k] = pal(g, light); (JA.comp04 if k == '04' else JA.comp05)().save(f'{d}/wart-{k}.png')
            JW.JAR[k]['look'] = look(g, light)
            open(f'{d}/jar-{k}.svg', 'w', encoding='utf-8').write(JW.svg(JW.wrap(k, d)))
            print(k, name, flush=True)
