# 100 g kraft pouch labels, front and back, with live type (tools/label.mjs drew the approved fronts with every
# letter outlined; this draws the same design as live text, for Illustrator masters and print PDFs).
#   front: the approved design (Dusk ground, woven name); the barcode card at the foot becomes a card with the name
#          in Sinhala, the second language of the main panel (the barcode moves to the back)
#   back:  the same die and ground, the tendril and trailing leaves; the name in Tamil, stacked like the front;
#          net weight in English, Sinhala and Tamil; the distributor, as on the tea pack on sale; the barcode with
#          the batch fields labelled in all three languages
#   python3 tools/pouch_labels.py OUTDIR [approved]   (approved: the front exactly as label.mjs, for checking)
import sys, os, re, html
import uharfbuzz as hb
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = {'IS': 'instrument-serif-italic.ttf', 'G': 'geist-regular.ttf', 'GM': 'geist-medium.ttf',
        'SiB': 'noto-serif-sinhala.ttf', 'TaB': 'noto-serif-tamil.ttf', 'SiS': 'noto-sans-sinhala.ttf', 'TaS': 'noto-sans-tamil.ttf'}
FONT = {k: f'{R}/fonts/{v}' for k, v in FONT.items()}
INK, SOFT = '#143A1D', '#5C6F5F'
W, H, SHOULDER, BLEED, L = 70, 110, 8.5, 3, 7
n = lambda v, d=3: f'{round(v, d):g}'
_hb = {}
def width(t, f, sz, track=0):
    if f not in _hb: face = hb.Face(hb.Blob.from_file_path(FONT[f])); _hb[f] = (hb.Font(face), face.upem)
    font, upm = _hb[f]; b = hb.Buffer(); b.add_str(t); b.guess_segment_properties(); hb.shape(font, b)
    return sum(p.x_advance for p in (b.glyph_positions or [])) / upm * sz + track * sz * max(len(t) - 1, 0)
def text(f, s, sz, x, y, anchor='start', track=0, fill=INK, caps=False, op=None):
    s = s.upper() if caps else s; w = width(s, f, sz, track)
    x0 = x - w if anchor == 'end' else x - w / 2 if anchor == 'middle' else x
    ls = f' letter-spacing="{n(track * sz, 4)}"' if track else ''
    o = f' opacity="{op}"' if op else ''
    return f'<text x="{n(x0)}" y="{n(y)}" font-family="{f}" font-size="{n(sz, 4)}"{ls} fill="{fill}"{o} xml:space="preserve">{html.escape(s, False)}</text>'
label = lambda s, x, y, size=1.9, anchor='start', fill=INK: text('GM', s, size, x, y, anchor, 0.14, fill, True)
def mark(f):
    s = open(f'{R}/brand/{f}').read(); vw, vh = map(float, re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)', s).groups())
    return vw, vh, re.search(r' d="([^"]+)"', s).group(1)
LOGO, LION = mark('vanilla-shop-logo.svg'), mark('ceylon-tea-lion.svg')
logo = lambda x, y, w: f'<path id="Logo" fill="{INK}" fill-rule="evenodd" d="{LOGO[2]}" transform="translate({n(x)} {n(y)}) scale({n(w / LOGO[0], 6)})"/>'
lion = lambda x, y, w: f'<path id="Ceylon_Tea_lion" fill="{INK}" fill-rule="evenodd" d="{LION[2]}" transform="translate({n(x)} {n(y)}) scale({n(w / LION[0], 6)})"/>'
img = lambda f, x, y, w, h: f'<image href="file://{R}/plates/generated/{f}" x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}" preserveAspectRatio="none"/>'
def outline(i=0):
    return (f'M{n(i)} {n(H - i)}V{n(SHOULDER + i)}H{n(5 + i)}C12 {n(1 + i)} {n(W - 12)} {n(1 + i)} {n(W - 5 - i)} {n(SHOULDER + i)}'
            f'H{n(W - i)}V{n(H - i)}Z')
PIECE = {
    'vine': dict(file='v7-vine-upright-b.png', pw=1024, ph=1536, box=(89, 126, 930, 1438)),
    'vineCinnamon': dict(file='v7-vine-upright-cinnamon.png', pw=1024, ph=1536, box=(89, 126, 930, 1438)),
    'tip': dict(file='v8-crop-climb-tip.png', pw=580, ph=680, box=(76, 20, 523, 679)),
    'trail': dict(file='v8-crop-vine-trail.png', pw=1219, ph=859, box=(0, 367, 1047, 770)),
}
TIP = dict(piece='tip', at=(-1, 12.2), height=21, rotate=90)
TRAIL = dict(piece='trail', at=(-1.5, 81), width=30)
def art(d):
    a = PIECE[d['piece']]; x0, y0, x1, y1 = a['box']
    s = d['height'] / (y1 - y0) if 'height' in d else d['width'] / (x1 - x0)
    inner = img(a['file'], -x0 * s, -y0 * s, a['pw'] * s, a['ph'] * s)
    rot = f'translate({n((y1 - y0) * s)} 0) rotate(90)' if d.get('rotate') == 90 else f'translate({n((x1 - x0) * s)} 0) scale(-1 1)' if d.get('flip') else ''
    return f'<g transform="translate({n(d["at"][0])} {n(d["at"][1])}) {rot}">{inner}</g>'
PRODUCTS = {
    'natural-vanilla-tea-100g': dict(ground='v6-label-ground-dusk-vanilla.jpg', over='Authentic Ceylon', flavour=['Vanilla'],
        under=['Ceylon black tea', 'with natural vanilla'], gtin='4796034220243', vine='vine',
        si='වැනිලා තේ', ta=['வெனிலா', 'தேயிலை']),
    'vanilla-cinnamon-tea-100g': dict(ground='v6-label-ground-dusk-cinnamon.jpg', over='Authentic Ceylon', flavour=['Vanilla &', 'Cinnamon'],
        under=['Vanilla and cinnamon', 'blended with pure', 'Ceylon tea'], gtin='4796034220250', vine='vineCinnamon',
        si='වැනිලා කුරුඳු තේ', ta=['வெனிலா', 'கறுவா', 'தேயிலை']),
}
# The name in Sinhala and Tamil: bold, the letters without ascenders or descenders 3 mm high (Noto Serif Sinhala Bold
# 0.59 em, Noto Serif Tamil Bold 0.57 em). Translations are ours (கறுவா: the Sri Lankan Tamil word for cinnamon);
# a native reader checks them on a printed proof.
SI = round(3 / 0.59, 2)
DISTRIBUTOR = ['Marketed and Distributed by:', 'Agro Ventures Exports (Pvt) Ltd,', 'No.48, Sir Marcus Fernando Mawatha,', 'Colombo 07.',
               'www.agroventuresexports.com', 'info@agroventuresexports.com', 'Hot Line: 011 2 187 287']     # as on the tea pack
BATCH = [('MRP Rs.', 'උ.සි.මි.රු.', 'விலைரூபா'), ('MFD', 'නි.දි.', 'பொ.செ திகதி'), ('EXP', 'කා.ඉ.දි.', 'மு.திகதி'), ('B.N.', 'කා.අ.', 'தொகுதி இல')]

def ean13(code, x, y, bar_h=10):
    Lc = ['0001101', '0011001', '0010011', '0111101', '0100011', '0110001', '0101111', '0111011', '0110111', '0001011']
    Gc = ['0100111', '0110011', '0011011', '0100001', '0011101', '0111001', '0000101', '0010001', '0001001', '0010111']
    Rc = ['1110010', '1100110', '1101100', '1000010', '1011100', '1001110', '1010000', '1000100', '1001000', '1110100']
    PAR = ['LLLLLL', 'LLGLGG', 'LLGGLG', 'LLGGGL', 'LGLLGG', 'LGGLLG', 'LGGGLL', 'LGLGLG', 'LGLGGL', 'LGGLGL']
    dg = [int(c) for c in code]; assert (10 - sum(v * (3 if i % 2 else 1) for i, v in enumerate(dg[:12])) % 10) % 10 == dg[12]
    bits = '101'; guards = [0, 1, 2]
    for i, d in enumerate(dg[1:7]): bits += (Lc if PAR[dg[0]][i] == 'L' else Gc)[d]
    guards += [len(bits) + 1, len(bits) + 3]; bits += '01010'
    for d in dg[7:]: bits += Rc[d]
    guards += [len(bits), len(bits) + 2]; bits += '101'
    m = 0.264; qz = 11 * m; d = ''; i = 0
    while i < len(bits):
        if bits[i] != '1': i += 1; continue
        j = i
        while j + 1 < len(bits) and bits[j + 1] == '1' and ((j + 1) in guards) == (i in guards): j += 1
        h = bar_h + (1.32 if i in guards else 0)
        d += f'M{n(x + qz + i * m)} {n(y)}h{n((j - i + 1) * m)}v{n(h)}h{n(-(j - i + 1) * m)}Z'; i = j + 1
    sz = 2.2; ty = y + bar_h + 0.35 + sz * 0.72
    return (f'<path d="{d}" fill="{INK}"/>' + text('G', code[0], sz, x + qz - 1.6 * m, ty, 'end') +
            text('G', code[1:7], sz, x + qz + 24 * m, ty, 'middle', 0.06) + text('G', code[7:], sz, x + qz + 71 * m, ty, 'middle', 0.06))

def frame(body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W + 2 * BLEED}mm" height="{H + 2 * BLEED}mm" '
            f'viewBox="{-BLEED} {-BLEED} {W + 2 * BLEED} {H + 2 * BLEED}"><title>{title}</title>'
            f'<defs><clipPath id="bleed"><path d="{outline(-BLEED)}"/></clipPath></defs>'
            f'<g id="Label" clip-path="url(#bleed)">{body}</g>'
            f'<path id="Cut_line" d="{outline()}" fill="none" stroke="#E4007C" stroke-width="0.2"/></svg>')

def card(cy, ch, cw, cx=L - 1.5):
    return f'<rect x="{n(cx)}" y="{n(cy)}" width="{n(cw)}" height="{n(ch)}" rx="1" fill="#FFFFFF" stroke="{INK}" stroke-opacity=".5" stroke-width="0.18"/>'

def head(p, out):
    out += [img(p['ground'], -BLEED, -BLEED, W + 2 * BLEED, H + 2 * BLEED)]
def top(p, out, with_lion=True):
    out.append(logo(W / 2 - 6.5, 6.5, 13))
    if with_lion: out.append(lion(W - L - 12, 6.5 + 13 * LOGO[1] / LOGO[0] - 12 * LION[1] / LION[0], 12))
    out += [label(p['over'], L, 24.4), label('100 g', W - L, 24.4, anchor='end'),
            f'<path d="M{n(L)} 26.4H{n(W - L)}" stroke="{INK}" stroke-opacity=".5" stroke-width="0.18"/>']

def front(k, approved=False):
    p = PRODUCTS[k]; out = []; head(p, out)
    vine = dict(piece=p['vine'], at=(28, 12), height=94)
    out += [art(TIP), art(TRAIL), art(vine)]; top(p, out)
    lines = p['flavour'] + ['Tea']
    sz = min([18] + [57 / width(l, 'IS', 1) for l in lines]); lead = sz * 0.88; b1 = 29.5 + sz * 0.72
    out += [text('IS', l, sz, L - 0.5, b1 + i * lead) for i, l in enumerate(lines)]
    nxt = b1 + (len(lines) - 1) * lead + 5
    a = PIECE[vine['piece']]; sc = vine['height'] / (a['box'][3] - a['box'][1])
    mm = lambda px, py: (vine['at'][0] + (px - a['box'][0]) * sc, vine['at'][1] + (py - a['box'][1]) * sc)
    (x0, y0), (x1, y1) = mm(385, 415), mm(520, 540)
    out.append(f'<clipPath id="leaf"><rect x="{n(x0)}" y="{n(y0)}" width="{n(x1 - x0)}" height="{n(y1 - y0)}"/></clipPath><g clip-path="url(#leaf)">{art(vine)}</g>')
    out += [text('G', u, 2.2, L, nxt + i * 3) for i, u in enumerate(p['under'])]
    K, pad, M = 0.84, 1.6, 0.264; barsW = 95 * M * K; bcH = (10 + 2.6) * K
    ch = bcH + 2 * pad; cx = L - 1.5; cy = H - 5.2 - ch
    if approved:
        bx = cx + pad + 1.2; divX = bx + barsW + pad; fx = divX + pad; lx0 = fx + 7.4; ll = 11.5; cw = lx0 + ll + pad - cx
        out.append(card(cy, ch, cw))
        out.append(f'<g transform="translate({n(bx - 11 * M * K)} {n(cy + pad)}) scale({K})">{ean13(p["gtin"], 0, 0)}</g>')
        out.append(f'<path d="M{n(divX)} {n(cy + pad)}V{n(cy + ch - pad)}" stroke="{INK}" stroke-width="0.12"/>')
        rows = ['MRP Rs.', 'MFD', 'EXP', 'BTN']; t0 = cy + pad + 1.15; step = (ch - 2 * pad - 1.15) / (len(rows) - 1)
        for i, r in enumerate(rows):
            y = t0 + i * step; out.append(label(r, fx, y, 1.35))
            out.append(f'<path d="M{n(lx0)} {n(y + 0.2)}H{n(lx0 + ll)}" stroke="{SOFT}" stroke-width="0.1" stroke-dasharray="0.35 0.35"/>')
    else:
        # the same card, in the same place, now carrying the name in Sinhala
        cw = max(46.0, width(p['si'], 'SiB', SI) + 2 * pad + 4)
        out.append(card(cy, ch, cw))
        out.append(text('SiB', p['si'], SI, cx + cw / 2, cy + ch / 2 + SI * 0.30, 'middle'))
    return frame(''.join(out), f'The Vanilla Shop {k} pouch label, front, 70 x 110 mm, 3 mm bleed')

def back(k):
    p = PRODUCTS[k]; out = []; head(p, out)
    out += [art(TIP)]
    top(p, out, with_lion=False)
    # the name in Tamil, stacked as the English is on the front
    tz = 8.0 if len(p['ta']) == 2 else 7.0; lead = tz * 1.32; y = 26.4 + 3.2 + tz * 0.8
    for i, l in enumerate(p['ta']): out.append(text('TaB', l, tz, L - 0.3, y + i * lead))
    y += (len(p['ta']) - 1) * lead + 7.2
    # net weight, labelled in all three languages (CAA Direction 71), as on the tea boxes
    x = L; out.append(label('Net weight', x, y, 1.9)); x += width('NET WEIGHT', 'GM', 1.9, 0.14) + 2.2
    out.append(text('SiS', 'ශුද්ධ බර', 2.4, x, y)); x += width('ශුද්ධ බර', 'SiS', 2.4) + 2.2
    out.append(text('TaS', 'நிகர எடை', 2.3, x, y)); x += width('நிகர எடை', 'TaS', 2.3) + 2.6
    out.append(text('G', '100 g', 2.6, W - L, y, 'end'))
    out.append(f'<path d="M{n(L)} {n(y + 2.2)}H{n(W - L)}" stroke="{INK}" stroke-opacity=".5" stroke-width="0.18"/>')
    y += 6.4
    for i, l in enumerate(DISTRIBUTOR):
        out.append(text('G', l, 2.0, L, y + i * 2.75, fill=INK))
    # barcode and batch card, at the front card's place; fields in English, Sinhala and Tamil
    K, pad, M = 0.84, 1.6, 0.264; barsW = 95 * M * K; bcH = (10 + 2.6) * K
    ch = bcH + 2 * pad + 1.6; cx = L - 1.5; cy = H - 5.2 - ch; cw = W - 2 * L + 3
    # the vine's trailing leaves come in from the right edge, as they come in from the left on the front
    out.insert(2, art(dict(piece='trail', at=(W - 25 + 1.5, cy - 17), width=25, flip=True)))
    out.append(card(cy, ch, cw))
    bx = cx + pad + 1.2
    out.append(f'<g transform="translate({n(bx - 11 * M * K)} {n(cy + pad + 0.8)}) scale({K})">{ean13(p["gtin"], 0, 0)}</g>')
    divX = bx + barsW + pad; fx = divX + pad
    out.append(f'<path d="M{n(divX)} {n(cy + pad)}V{n(cy + ch - pad)}" stroke="{INK}" stroke-width="0.12"/>')
    t0 = cy + pad + 1.7; step = (ch - 2 * pad - 1.9) / (len(BATCH) - 1)
    for i, (en, si, ta) in enumerate(BATCH):
        yy = t0 + i * step; xx = fx
        out.append(label(en, xx, yy, 1.3)); xx += 7.4
        out.append(text('SiS', si, 1.75, xx, yy, fill=SOFT)); xx += width(si, 'SiS', 1.75) + 1.0
        out.append(text('TaS', ta, 1.55, xx, yy, fill=SOFT))
        out.append(f'<path d="M{n(fx)} {n(yy + 0.75)}H{n(cx + cw - pad)}" stroke="{SOFT}" stroke-width="0.1" stroke-dasharray="0.35 0.35"/>')
    return frame(''.join(out), f'The Vanilla Shop {k} pouch label, back, 70 x 110 mm, 3 mm bleed')

if __name__ == '__main__':
    out = sys.argv[1]; os.makedirs(out, exist_ok=True); approved = 'approved' in sys.argv
    for k in PRODUCTS:
        open(f'{out}/{k}_front{"_approved" if approved else ""}.svg', 'w', encoding='utf-8').write(front(k, approved))
        if not approved: open(f'{out}/{k}_back.svg', 'w', encoding='utf-8').write(back(k))
    print('ok')
