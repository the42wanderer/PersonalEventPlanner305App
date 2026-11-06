# 100 g jar wraps, No. 04 Vanilla Paste and No. 05 Vanilla Powder, on the printer's template: 200 x 42 mm, 3 mm bleed.
# The extract labels' Split design (splitwrap.py) at print size (no scaling): the colour half with the painted
# flower, the brand line, the story and the facts; the cream half with the front card (English and Sinhala names,
# the net weight) and, to its right, the name in Tamil, ingredients, price, barcode, dates and maker.
# Nothing here comes from a label on sale: anything still to confirm is boxed (PLACE) and listed in TO_FILL.
#   python3 jarwrap.py ARTDIR OUTDIR
import sys, os
sys.path.insert(0, '/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/ext/w')
from kit import width, logo, txt, caps, rule, para, ean13
from content import MAKER
W, H, CX, B = 200, 42, 100, 3.0
PAPER = '#F7EFDC'
# 3 mm letter height for the names (Noto Serif Sinhala Bold 0.59 em, Tamil Bold 0.57 em), printed at this size
SI, TA = round(3 / 0.59, 2), round(3 / 0.57, 2)
SHORT = 'Grown in the hills of Kandy, Matale and Nuwara Eliya, where every vanilla flower is pollinated by hand.'
JAR = {
    '04': dict(no='No. 04', l1='Vanilla', l2='Paste', kind='NATURAL VANILLA PASTE', si='වැනිලා පේස්ට්', ta='வெனிலா பேஸ்ட்',
               tail=' Made from the cured pods, seeds and all.', best='Baking and desserts',
               look=dict(dark='#3E2418', deep='#7A4A30', on='#FBEBDD', on2='#E2B999')),
    '05': dict(no='No. 05', l1='Vanilla', l2='Powder', kind='NATURAL VANILLA POWDER', si='වැනිලා කුඩු', ta='வெனிலா தூள்',
               tail=' The cured pods, dried and ground.', best='Drinks and baking',
               look=dict(dark='#45182D', deep='#8A3D62', on='#FBE9EF', on2='#E6B3C6')),
}
PH_EAN = '2000000000008'            # in-store number range, never a real product: an obvious placeholder
MASTER = False                     # True: placeholder boxes drawn (they become the TO_FILL layer)
def place(x, y, w, h):
    return f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="#FF2BA6" opacity="0.3" rx="0.4"/>' if MASTER else ''
DATE3 = (('MFD', 'නි.දි.', 'பொ.செ திகதி'), ('EXP', 'කා.ඉ.දි.', 'மு.திகதி'))

def art(k, artdir):
    """the painting (jarart.py, 172 x 70 mm) scaled to the label height; its right 103 mm are the colour half and its
    left bleed; the top and bottom bleed repeat the edge rows"""
    import numpy as np
    from PIL import Image
    im = Image.open(f'{artdir}/wart-{k}.png').convert('RGB'); s = H / 70
    im = im.resize((round(im.width * s), round(H * 20)), Image.LANCZOS)
    full = round((CX + B) * 20); im = im.crop((im.width - full, 0, im.width, im.height))
    a = np.pad(np.asarray(im), ((round(B * 20),) * 2, (0, 0), (0, 0)), mode='reflect')
    p = f'{artdir}/jart-{k}.jpg'; Image.fromarray(a).save(p, quality=94); return p

def wrap(k, artdir):
    j = JAR[k]; L = j['look']; c, d, on, on2 = L['dark'], L['deep'], L['on'], L['on2']
    o = [f'<rect x="{-B}" y="{-B}" width="{W + 2 * B}" height="{H + 2 * B}" fill="{PAPER}"/>',
         f'<image href="file://{art(k, artdir)}" x="{-B}" y="{-B}" width="{CX + B}" height="{H + 2 * B}" preserveAspectRatio="none"/>']
    # ---- colour half: brand line, story, facts, number
    x0, x1 = 5.5, 48
    o.append(txt('Savor the calm.', x0, 8.4, 3.6, on, 'IS'))
    p, ye = para(SHORT + j['tail'], x0, 13.2, x1 - x0, 1.75, 2.35, on); o += p
    o.append(place(x0 - 0.4, ye - 1.7, x1 - x0 + 0.8, 2.3))                 # the closing line: copy to confirm
    for i, (a, av, b_, bv) in enumerate((('SPECIES', 'Vanilla planifolia', 'ORIGIN', 'Sri Lanka'), ('BEST FOR', j['best'], 'PRODUCT', '100% natural'))):
        y = 25.6 + i * 7.0
        o += [rule(x0, y, x1, y, on, 0.18, 0.5), caps(a, x0, y + 2.7, 1.1, on2, tr=0.22), txt(av, x0, y + 5.5, 1.7, on),
              caps(b_, x0 + (x1 - x0) * 0.57, y + 2.7, 1.1, on2, tr=0.22), txt(bv, x0 + (x1 - x0) * 0.57, y + 5.5, 1.7, on)]
    o.append(txt(j['no'], CX - 3.5, 38.8, 4.4, on, 'IS', 'end'))
    # ---- front card: logo, the English name, the Sinhala name, what it is, the net weight
    cx0, cx1 = CX + 3, CX + 41; mx = (cx0 + cx1) / 2; a = 2.2
    for bx, by, dx, dy in ((cx0, 3.2, 1, 1), (cx1, 3.2, -1, 1), (cx0, 38.8, 1, -1), (cx1, 38.8, -1, -1)):
        o.append(f'<path d="M{bx:.2f} {by + dy * a:.2f}V{by:.2f}H{bx + dx * a:.2f}" fill="none" stroke="{c}" stroke-width="0.24"/>')
    o += [logo(mx, 7.0, 5.2, c), txt(j['l1'], mx, 15.6, 7.4, c, 'IS', 'middle'), txt(j['l2'], mx, 21.6, 7.4, c, 'IS', 'middle'),
          txt(j['si'], mx, 27.7, SI, c, 'SiB', 'middle'), caps(j['kind'], mx, 31.7, 1.15, d, 'middle', 0.22),
          txt('100 g', mx, 38.0, 4.2, c, 'IS', 'middle')]
    # ---- right of the card: the name in Tamil, ingredients, price, barcode, dates, maker
    rx0, rx1 = CX + 44.5, W - 4
    o.append(txt(j['ta'], rx0, 8.0, TA, d, 'TaB'))                     # the name in Tamil, in the second ink
    o += [caps('INGREDIENTS', rx0, 12.4, 1.1, d, tr=0.22)]
    ing = 'To be supplied by production.'
    o += [place(rx0 + 13.6, 10.7, rx1 - rx0 - 13.6, 2.3), txt(ing, rx0 + 14.0, 12.4, 1.55, c)]
    o.append(rule(rx0, 14.2, rx1, 14.2, c, 0.15, 0.4))
    b, bw = ean13(PH_EAN, rx0 + 1.2, 16.2, 0.22, 6.0, '#1A120C'); o += b
    o += [place(rx0 - 0.2, 15.2, bw + 3.2, 9.6), caps('PLACEHOLDER · REPLACE', rx0, 26.6, 0.9, '#C0007A', tr=0.12)]
    bx = rx0 + bw + 7.6
    o += [txt('MRP Rs. ____', rx1, 17.4, 1.9, c, 'GB', 'end'), place(rx1 - width('MRP Rs. ____', 'GB', 1.9) - 0.4, 15.6, width('MRP Rs. ____', 'GB', 1.9) + 0.8, 2.4)]
    for i, ((en, si, ta), v) in enumerate(zip(DATE3, ('__/__/____', '__/__/____'))):
        yy = 20.6 + i * 4.0
        o += [caps(en, bx, yy, 0.95, d, tr=0.2), txt(v, bx + 5.0, yy, 1.8, c, 'GB'),
              txt(si, bx, yy + 1.9, 1.45, d, 'SiS'), txt(ta, bx + width(si, 'SiS', 1.45) + 1.0, yy + 1.9, 1.3, d, 'TaS')]
    o.append(place(bx + 4.8, 18.9, 11.2, 7.8))
    y = 30.6
    o += [caps('MANUFACTURED & MARKETED BY', rx0, y, 0.95, d, tr=0.2), caps('PRODUCT OF SRI LANKA', rx1, y, 0.95, d, 'end', 0.2)]
    for i, l in enumerate(MAKER): o.append(txt(l, rx0, y + 2.3 + i * 1.75, 1.42, c, 'GB' if i == 0 else 'G'))
    return o

def svg(o, w=W, h=H):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w + 2 * B}mm" height="{h + 2 * B}mm" viewBox="{-B} {-B} {w + 2 * B} {h + 2 * B}">'
            + ''.join(o) + '</svg>')
if __name__ == '__main__':
    artdir, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
    for k in JAR:
        open(f'{out}/jar-{k}.svg', 'w', encoding='utf-8').write(svg(wrap(k, artdir)))
    print('ok')
