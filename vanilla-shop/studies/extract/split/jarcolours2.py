# Colour study 2 for the jar labels, from what each holds: the paste glossy, dark and seeded, so its label takes the
# amber of the light caught in it, with a scatter of seeds; the powder dry, matte and pale brown, so its label is pale
# and matte with a fine dusting, inked in the powder's own brown.  python3 jarcolours2.py OUTDIR
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comp as C, jarart as JA, jarwrap as JW
from comp import mix
POD_INK, POD_SOFT = '#3F2A1E', '#7A5C46'          # the ground pod's brown, for the powder's type
def pal(g, light):
    if not light:
        return dict(ground=g, tep_core=mix('#FFFFFF', g, 0.05), tep_edge=mix(g, '#FFFFFF', 0.5), lip_core=mix('#FFFFFF', g, 0.03),
                    lip_edge=mix(g, '#FFFFFF', 0.68), throat_core='#F2C460', throat_edge='#D99A42', leaf_core=mix(g, '#FFFFFF', 0.3),
                    leaf_edge=mix(g, '#000000', 0.45), pod_core='#22120A', pod_edge='#120804', bud_core=mix('#FFFFFF', g, 0.12),
                    bud_edge=mix(g, '#FFFFFF', 0.35), stem=mix(g, '#FFFFFF', 0.3))
    return dict(ground=g, tep_core='#FFFDF8', tep_edge=mix(g, POD_SOFT, 0.28), lip_core='#FFFEFA', lip_edge=mix(g, '#FFFFFF', 0.45),
                throat_core='#F0C25E', throat_edge='#D2963E', leaf_core=mix(g, POD_SOFT, 0.22), leaf_edge=mix(g, POD_INK, 0.5),
                pod_core='#3A2418', pod_edge='#21140C', bud_core='#FFFBF2', bud_edge=mix(g, POD_SOFT, 0.3), stem=mix(g, POD_SOFT, 0.4))
def look(g, light):
    if light: return dict(dark=POD_INK, deep=POD_SOFT, on=POD_INK, on2=POD_SOFT)
    return dict(dark=mix(g, '#000000', 0.5), deep=g, on=mix('#FFFFFF', g, 0.08), on2=mix(g, '#FFFFFF', 0.6))
OPTS = {'04': [('Molasses amber', '#7A3F1D', False), ('Burnt caramel', '#9A5126', False)],
        '05': [('Parchment', '#E3D2B3', True), ('Ash', '#BDAE9E', True)]}
if __name__ == '__main__':
    out = sys.argv[1]; JW.JAR['04']['texture'] = 'seeds'; JW.JAR['05']['texture'] = 'dust'
    for k, opts in OPTS.items():
        for i, (name, g, light) in enumerate(opts):
            d = f'{out}/{k}-{i}'; os.makedirs(d, exist_ok=True)
            C.PAL[k] = pal(g, light); (JA.comp04 if k == '04' else JA.comp05)().save(f'{d}/wart-{k}.png')
            JW.JAR[k]['look'] = look(g, light)
            open(f'{d}/jar-{k}.svg', 'w', encoding='utf-8').write(JW.svg(JW.wrap(k, d)))
            print(k, name, flush=True)
