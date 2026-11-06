# Turn a layout SVG (as drawn by our build scripts) into an Illustrator master:
#  - English text stays live, one text object per line (style runs kept as tspans), fonts named by PostScript name,
#    centred / right-aligned lines placed by their left edge so they open exactly in place;
#  - Sinhala and Tamil become HarfBuzz-shaped outlines, each with a live twin in the hidden layer
#    Sinhala_Tamil_live_text (same font, size, place);
#  - placeholder boxes (fill #FF2BA6) move to the layer TO_FILL, at the same place on the sheet;
#  - images are embedded, so the file is self-contained.
import re, io, base64, math, html
import xml.etree.ElementTree as ET
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from PIL import Image

NS = 'http://www.w3.org/2000/svg'; ET.register_namespace('', NS); q = lambda t: f'{{{NS}}}{t}'
PLACEHOLDER = '#FF2BA6'

class Fonts:
    """alias -> font file; PostScript names read from the files"""
    def __init__(self, files, complex_aliases):
        self.files = files; self.complex = set(complex_aliases); self._hb = {}; self._ps = {}
    def ps(self, a):
        if a not in self._ps: self._ps[a] = TTFont(self.files[a])['name'].getDebugName(6)
        return self._ps[a]
    def _font(self, a):
        if a not in self._hb:
            f = self.files[a]; face = hb.Face(hb.Blob.from_file_path(f)); tt = TTFont(f)
            self._hb[a] = (hb.Font(face), face.upem, tt.getGlyphSet(), tt.getGlyphOrder())
        return self._hb[a]
    def shape(self, t, a):
        font, upm, gs, order = self._font(a); buf = hb.Buffer(); buf.add_str(t); buf.guess_segment_properties(); hb.shape(font, buf)
        return buf.glyph_infos or [], buf.glyph_positions or [], upm, gs, order
    def width(self, t, a, sz):
        if not t: return 0.0
        _, pos, upm, _, _ = self.shape(t, a); return sum(p.x_advance for p in pos) / upm * sz
    def outline(self, t, a, sz, x, y):
        infos, pos, upm, gs, order = self.shape(t, a); pen = SVGPathPen(gs); k = sz / upm; cx = 0
        for i, p in zip(infos, pos):
            gs[order[i.codepoint]].draw(TransformPen(pen, (k, 0, 0, -k, x + (cx + p.x_offset) * k, y - p.y_offset * k))); cx += p.x_advance
        return pen.getCommands()

def parse_transform(s):
    m = [1, 0, 0, 1, 0, 0]
    for name, args in re.findall(r'(\w+)\s*\(([^)]*)\)', s or ''):
        v = [float(x) for x in re.split(r'[\s,]+', args.strip()) if x]
        if name == 'translate': t = [1, 0, 0, 1, v[0], v[1] if len(v) > 1 else 0]
        elif name == 'scale': t = [v[0], 0, 0, v[1] if len(v) > 1 else v[0], 0, 0]
        elif name == 'rotate':
            r = math.radians(v[0]); c, s_ = math.cos(r), math.sin(r); t = [c, s_, -s_, c, 0, 0]
            if len(v) == 3: t = mul(mul([1, 0, 0, 1, v[1], v[2]], t), [1, 0, 0, 1, -v[1], -v[2]])
        elif name == 'matrix': t = v
        else: continue
        m = mul(m, t)
    return m
def mul(a, b):
    return [a[0]*b[0]+a[2]*b[1], a[1]*b[0]+a[3]*b[1], a[0]*b[2]+a[2]*b[3], a[1]*b[2]+a[3]*b[3],
            a[0]*b[4]+a[2]*b[5]+a[4], a[1]*b[4]+a[3]*b[5]+a[5]]
def mstr(m): return 'matrix(' + ' '.join(f'{v:.6g}' for v in m) + ')'

def runs(el, inh):
    """the text runs of a <text>: (string, font alias, size, letter-spacing, dx)"""
    f = el.get('font-family', inh.get('font-family')); sz = float(el.get('font-size', inh.get('font-size', 0)))
    ls = float(el.get('letter-spacing', inh.get('letter-spacing', 0)) or 0)
    out = [(el.text or '', f, sz, ls, 0.0)]
    for t in el:
        tf = t.get('font-family', f); tsz = float(t.get('font-size', sz)); tls = float(t.get('letter-spacing', ls) or 0)
        out.append((t.text or '', tf, tsz, tls, float(t.get('dx', 0) or 0)))
        out.append((t.tail or '', f, sz, ls, 0.0))
    return out

def convert(svg, fonts, gold=None, title=''):
    """svg: a complete <svg> string; returns (master svg string, list of all text items for the copy sheet)"""
    root = ET.fromstring(svg); twins = []; todo = []; items = []
    def walk(el, ctm, inh):
        ctm = mul(ctm, parse_transform(el.get('transform')))
        inh = dict(inh)
        for k in ('font-family', 'font-size', 'letter-spacing', 'fill'):
            if el.get(k) is not None: inh[k] = el.get(k)
        if el.get('id'): inh['_id'] = el.get('id')                     # the panel a text item sits on
        for ch in list(el):
            tag = ch.tag.split('}')[1]
            if tag == 'rect' and (ch.get('fill') or '').upper() == PLACEHOLDER:
                todo.append(f'<rect x="{ch.get("x")}" y="{ch.get("y")}" width="{ch.get("width")}" height="{ch.get("height")}" '
                            f'fill="{PLACEHOLDER}" fill-opacity="0.3" transform="{mstr(mul(ctm, parse_transform(ch.get("transform"))))}"/>')
                el.remove(ch); continue
            if tag == 'text': fix_text(el, ch, ctm, inh); continue
            if tag == 'image': embed(ch)
            if gold:
                for a in ('fill', 'stroke'):
                    if ch.get(a) == 'url(#foil)': ch.set(a, gold)
            walk(ch, ctm, inh)
    def fix_text(parent, el, ctm, inh):
        ctm2 = mul(ctm, parse_transform(el.get('transform')))
        rs = runs(el, inh); f0 = rs[0][1]; sz0 = rs[0][2]
        w = sum(fonts.width(t, f, sz) + ls * len(t) + dx for t, f, sz, ls, dx in rs)
        anc = el.get('text-anchor', inh.get('text-anchor', 'start')); x = float(el.get('x', 0)); y = float(el.get('y', 0))
        x0 = x - (w / 2 if anc == 'middle' else w if anc == 'end' else 0)
        text = ''.join(t for t, *_ in rs)
        fill = el.get('fill') or next((t.get('fill') for t in el if t.get('fill') not in (None, 'url(#foil)', 'none')), inh.get('fill', '#000'))
        foil = any(t_.get('fill') == 'url(#foil)' for t_ in [el] + list(el))
        if gold:
            for t_ in [el] + list(el):
                if t_.get('fill') == 'url(#foil)': t_.set('fill', gold)
        items.append(dict(text=text, font=f0, size=sz0, fill=fill, x=x0, y=y, ctm=ctm2, foil=foil, panel=inh.get('_id', ''),
                          ls=float(el.get('letter-spacing', inh.get('letter-spacing', 0)) or 0)))
        if f0 in fonts.complex and len(el) == 0:
            twins.append(f'<text x="{x0:.3f}" y="{y:.3f}" font-family="\'{fonts.ps(f0)}\'" font-size="{sz0}" fill="{fill}" '
                         f'xml:space="preserve" transform="{mstr(ctm2)}">{html.escape(text, False)}</text>')
            p = ET.Element(q('path'), {'d': fonts.outline(text, f0, sz0, x0, y), 'fill': fill})
            if el.get('opacity'): p.set('opacity', el.get('opacity'))
            if el.get('transform'): p.set('transform', el.get('transform'))
            parent.insert(list(parent).index(el), p); parent.remove(el); return
        el.set('x', f'{x0:.3f}')
        for a in ('text-anchor',): el.attrib.pop(a, None)
        el.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
        for t_ in [el] + list(el):
            if t_.get('font-family'): t_.set('font-family', f"'{fonts.ps(t_.get('font-family'))}'")
        if not el.get('font-family'): el.set('font-family', f"'{fonts.ps(f0)}'")
        if el.get('letter-spacing') in ('0', '0.000'): el.attrib.pop('letter-spacing')
    def embed(ch):
        href = ch.get('href') or ch.get('{http://www.w3.org/1999/xlink}href') or ''
        if not href.startswith('file://'): return
        p = href[7:]; im = Image.open(p); buf = io.BytesIO()
        if im.mode in ('RGBA', 'LA', 'P') and 'A' in im.getbands(): im.save(buf, 'PNG'); mime = 'image/png'
        else: im.convert('RGB').save(buf, 'JPEG', quality=92); mime = 'image/jpeg'
        ch.set('href', f'data:{mime};base64,' + base64.b64encode(buf.getvalue()).decode())
    walk(root, [1, 0, 0, 1, 0, 0], {})
    body = ''.join(ET.tostring(c, encoding='unicode') for c in root)
    head = re.match(r'<svg[^>]*>', svg).group(0)
    out = (f'<?xml version="1.0" encoding="UTF-8"?>\n{head}' + (f'<title>{html.escape(title)}</title>' if title else '')
           + f'<g id="Artwork">{body}</g>'
           + f'<g id="TO_FILL">{"".join(todo)}</g>'
           + f'<g id="Sinhala_Tamil_live_text" display="none">{"".join(twins)}</g></svg>')
    return out, items

def paragraphs(items):
    """join a text item to the one before when it continues the same paragraph (same font, size, x, transform,
    the next line down)"""
    out = []
    for it in items:
        if out:
            p = out[-1]; l = p['last']
            if (it['font'] == l['font'] and abs(it['size'] - l['size']) < 1e-6 and abs(it['x'] - l['x']) < 0.05 and
                    it['ctm'] == l['ctm'] and 0 < it['y'] - l['y'] < it['size'] * 1.8):
                p['text'] += ' ' + it['text']; p['last'] = it; continue
        d = dict(it); d['last'] = it; out.append(d)
    return out
