# Editable masters for the extract labels: one SVG per label, for Illustrator (File > Open).
#  - Every English line is one live text object, its font named by its PostScript name so Illustrator finds the
#    installed font; centred and right-aligned lines are placed by their left edge (Illustrator reads the position
#    reliably, not always the alignment), so nothing shifts on opening.
#  - Sinhala and Tamil print as outlines shaped with HarfBuzz (Illustrator's default composer cannot shape them), each
#    with a live twin, same font, size and place, in the hidden layer Sinhala_Tamil_live_text.
#  - The artwork and marks are embedded; the dieline is its own layer.
#   python3 editable.py  -> editable/*.svg
import re, base64, io, os, html, sys
sys.path.insert(0, '../w')
from PIL import Image
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
import export as EX, splitwrap as SW, kit
T = SW.T; OUT = T + 'editable/'; os.makedirs(OUT, exist_ok=True)
PS = {'G': 'Geist-Regular', 'GM': 'Geist-Medium', 'GB': 'Geist-Bold', 'IS': 'InstrumentSerif-Italic',
      'RW': 'ArchivoSemiBoldExpanded-Regular', 'RWM': 'ArchivoSemiBoldExpanded-Medium',
      'SiB': 'NotoSerifSinhala-Bold', 'TaB': 'NotoSerifTamil-Bold', 'SiS': 'NotoSansSinhala-Medium', 'TaS': 'NotoSansTamil-Medium'}
COMPLEX = ('SiB', 'TaB', 'SiS', 'TaS')
_f = {}
def outline(t, f, sz, x, y):
    """the shaped string as one SVG path, left edge at x, baseline at y (units = label mm)"""
    if f not in _f:
        p = kit.FONTS[f]; face = hb.Face(hb.Blob.from_file_path(p)); tt = TTFont(p)
        _f[f] = (hb.Font(face), face.upem, tt.getGlyphSet(), tt.getGlyphOrder())
    font, upm, gs, order = _f[f]; buf = hb.Buffer(); buf.add_str(t); buf.guess_segment_properties(); hb.shape(font, buf)
    pen = SVGPathPen(gs); k = sz / upm; cx = 0
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        g = order[info.codepoint]
        tp = TransformPen(pen, (k, 0, 0, -k, x + (cx + pos.x_offset) * k, y - pos.y_offset * k))
        gs[g].draw(tp); cx += pos.x_advance
    return pen.getCommands()
def attrs(s): return dict(re.findall(r'([\w:-]+)="([^"]*)"', s))
TWINS = []
def fix_text(m):
    a = attrs(m.group(1)); t = html.unescape(m.group(2)); f = a['font-family']; sz = float(a['font-size'])
    tr = float(a.get('letter-spacing', 0)) / sz if sz else 0
    # the width as the browser sets it: HarfBuzz with kerning, the letter-spacing after every character (the last
    # too), so a centred or right-aligned line lands exactly where it was drawn
    w = (kit.hbwidth(t, f, sz) if t else 0) + tr * sz * len(t); anc = a.get('text-anchor', 'start'); x = float(a['x']); y = float(a['y'])
    x0 = x - (w / 2 if anc == 'middle' else w if anc == 'end' else 0)
    op = a.get('opacity', '1'); fill = a['fill']
    if f in COMPLEX:
        TWINS.append(f'<text x="{x0:.3f}" y="{y:.3f}" font-family="\'{PS[f]}\'" font-size="{sz}" fill="{fill}">{html.escape(t, False)}</text>')
        return f'<path d="{outline(t, f, sz, x0, y)}" fill="{fill}" opacity="{op}"/>'
    ls = f' letter-spacing="{a["letter-spacing"]}"' if float(a.get('letter-spacing', 0)) else ''
    return (f'<text x="{x0:.3f}" y="{y:.3f}" font-family="\'{PS[f]}\'" font-size="{sz}"{ls} fill="{fill}" xml:space="preserve"'
            + (f' opacity="{op}"' if op != '1' else '') + f'>{html.escape(t, False)}</text>')
def embed(m):
    p = m.group(1); im = Image.open(p)
    buf = io.BytesIO()
    if 'wart' in p: im.convert('RGB').save(buf, 'JPEG', quality=92); mime = 'image/jpeg'
    else: im.save(buf, 'PNG'); mime = 'image/png'
    return f'href="data:{mime};base64,{base64.b64encode(buf.getvalue()).decode()}"'
def master(name, inner, w, h, kind, title):
    global TWINS; TWINS = []
    b = EX.B / EX.S
    body = ''.join(inner)
    body = re.sub(r'<text ([^>]*)>(.*?)</text>', fix_text, body)
    body = re.sub(r'href="file://([^"]+)"', embed, body)
    die = EX.dieline(kind, w, h).replace('<g ', '<g id="Dieline" ', 1) if kind == 'seal' else \
          f'<g id="Dieline">{EX.dieline(kind, w, h)}</g>'
    svg = (f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="{(w + 2 * b) * EX.S:.2f}mm" height="{(h + 2 * b) * EX.S:.2f}mm" '
           f'viewBox="{-b:.4f} {-b:.4f} {w + 2 * b:.4f} {h + 2 * b:.4f}"><title>{title}</title>'
           f'<g id="Artwork">{body}</g>'
           f'<g id="Sinhala_Tamil_live_text" display="none">{"".join(TWINS)}</g>{die}</svg>')
    open(OUT + name + '_EDITABLE.svg', 'w', encoding='utf-8').write(svg)
    return svg
if __name__ == '__main__':
    names = {'01': 'No01-Vanilla-Extract-with-alcohol', '02': 'No02-Vanilla-Extract-alcohol-free', '03': 'No03-Vanilla-Syrup'}
    for k in ('01', '02', '03'):
        for size in SW.PRICE[k]:
            inner, w, h = EX.wrap_svg(k, size)
            master(f'{names[k]}_{size}ml', inner, w, h, 'rect', f'{names[k]} {size} ml wrap, 3 mm bleed')
        inner, w, h = EX.seal_svg(k)
        master(f'{names[k]}_neck-seal', inner, w, h, 'seal', f'{names[k]} neck seal, 3 mm bleed')
    print('ok', len(os.listdir(OUT)))
