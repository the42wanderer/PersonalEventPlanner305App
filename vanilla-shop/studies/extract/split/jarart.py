# Colour art for the 100 g jar labels, in the extract labels' technique (comp.py): No. 04 Vanilla Paste in cocoa,
# No. 05 Vanilla Powder in plum. Drawn 70 mm high and 172 mm wide (the jar's colour half and its bleed, at 70/42),
# the composition against the right edge, so the pods run on to their own ends instead of being cut and mirrored.
#   python3 jarart.py OUTDIR
import sys
import comp as C
from comp import Canvas, leaves, pods, flower, stem, bud, mix
C.PAL['04'] = dict(ground='#5E3A2A', tep_core='#FFF3E6', tep_edge='#D8A27E', lip_core='#FFF9F0', lip_edge='#EEC9A6',
                   throat_core='#F2C460', throat_edge='#D69A42', leaf_core='#A27258', leaf_edge='#3E2418',
                   pod_core='#241309', pod_edge='#130A05', bud_core='#F5DECA', bud_edge='#C9946E', stem='#9E7058')
C.PAL['05'] = dict(ground='#6A2C4A', tep_core='#FFF1F4', tep_edge='#DB9DB6', lip_core='#FFF8F8', lip_edge='#F0C8D4',
                   throat_core='#F2C46A', throat_edge='#D9963E', leaf_core='#A66C88', leaf_edge='#45182D',
                   pod_core='#2C1220', pod_edge='#170910', bud_core='#F7DDE7', bud_edge='#CB8CA6', stem='#AA7290')
def comp04(W=172, H=70, ox=112):
    """No. 04, paste: a bundle of cured pods, the seeds' source, fanned behind a flower turned to the card"""
    p = C.PAL['04']; cv = Canvas(W, H, ox)
    leaves(cv, p, [((-4, 76), -58, 46, 8.2, 0.5)], 2.4, 0.8)
    pods(cv, p, [((-10, 66), -30, 86, 3.1, 0.28, 1), ((-2, 78), -40, 84, 2.9, 0.24, -1), ((6, 86), -52, 78, 2.7, 0.20, 1)], 0.6)
    flower(cv, (30, 33), 24, 2.0, p, blurs=(0.45, 0.38, 0.7))
    return cv.render(p['ground'], seed=14)
def comp05(W=172, H=70, ox=112):
    """No. 05, powder: the vine in bud, a flower facing out, a single pod below"""
    p = C.PAL['05']; cv = Canvas(W, H, ox)
    leaves(cv, p, [((-6, 66), -20, 42, 8.0, 0.5), ((66, 78), -150, 40, 7.4, -0.5)], 2.4, 0.9)
    pods(cv, p, [((-6, 74), -24, 70, 2.6, 0.22, 1)], 0.7)
    st = [(26, 44), (33, 31), (41, 19), (50, 8), (58, -2)]
    cv.add([stem(st, 0.9)], mix(p['stem'], '#FFFFFF', 0.25), p['stem'], 0.6)
    cv.add([stem([(41, 19), (36, 15), (31, 13)], 0.45), stem([(50, 8), (55, 6), (60, 6)], 0.4)], mix(p['stem'], '#FFFFFF', 0.25), p['stem'], 0.6)
    cv.add([bud((31, 13), -168, 12, 2.6, -0.3), bud((60, 6), -5, 11, 2.3, 0.3)], p['bud_core'], p['bud_edge'], 0.55, glow=1.2)
    flower(cv, (24, 45), 80, 1.85, p, blurs=(0.45, 0.38, 0.7))
    return cv.render(p['ground'], seed=15)
if __name__ == '__main__':
    out = sys.argv[1]
    comp04().save(f'{out}/wart-04.png'); comp05().save(f'{out}/wart-05.png'); print('ok')
