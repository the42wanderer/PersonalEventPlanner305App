"""Shape Sinhala and Tamil label text with HarfBuzz and save outlined SVG paths.

opentype.js cannot reorder Indic vowel signs or form conjuncts, so these strings are
shaped here and written to brand/shaped-labels.json as path data at 1 unit = 1 em
(baseline at y = 0, y down), ready for tools/box.mjs to scale and place.

Usage: python3 tools/shape_labels.py
"""
import json
import os
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LABELS = {
    # Batch block field labels, as on the current pack.
    'sinhala': ['කා.අ.', 'නි.දි.', 'කා.ඉ.දි.', 'උ.සි.මි.රු.'],
    'tamil': ['தொகுதி இல', 'பொ.செ திகதி', 'மு.திகதி', 'விலை ரூபா', 'விலைரூபா'],
}
FONTS = {'sinhala': 'noto-sans-sinhala.ttf', 'tamil': 'noto-sans-tamil.ttf'}
# The Estate carton: the product name in Sinhala and Tamil (bold serif, after Instrument Serif; keys prefixed 'B:'),
# and the How to brew steps in Sinhala (sans, after Roc Grotesk). The bold fonts are Noto Serif Sinhala/Tamil Bold
# (OFL) from NOTO_BOLD_DIR; only their outlines are kept here, not the font files.
EXTRA = {
    'B:වැනිලා තේ': ('NotoSerifSinhala-Bold.ttf', 'වැනිලා තේ'),
    'B:வெனிலா தேயிலை': ('NotoSerifTamil-Bold.ttf', 'வெனிலா தேயிலை'),
    'උණු වතුරට තේ බෑගයක්': ('noto-sans-sinhala.ttf', 'උණු වතුරට තේ බෑගයක්'),
    'විනාඩි 5කින් බෑගය ඉවත් කරන්න': ('noto-sans-sinhala.ttf', 'විනාඩි 5කින් බෑගය ඉවත් කරන්න'),
    'හෝ නිවා අයිස් මත වත් කරන්න': ('noto-sans-sinhala.ttf', 'හෝ නිවා අයිස් මත වත් කරන්න'),
    'ශුද්ධ බර': ('noto-sans-sinhala.ttf', 'ශුද්ධ බර'),                                  # net weight (CAA Direction 71: three languages)
    'நிகர எடை': ('noto-sans-tamil.ttf', 'நிகர எடை'),
}

def shape(path, s):
    """HarfBuzz-shaped outline of s: path data at 1 unit = 1 em (baseline y = 0, y down), advance, ink bbox"""
    font = hb.Font(hb.Face(hb.Blob.from_file_path(path)))
    tt = TTFont(path); upem = tt['head'].unitsPerEm; glyphs = tt.getGlyphSet(); order = tt.getGlyphOrder()
    buf = hb.Buffer(); buf.add_str(s); buf.guess_segment_properties(); hb.shape(font, buf)
    pen = SVGPathPen(glyphs); bp = BoundsPen(glyphs); x = 0
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        k = 1 / upem
        for pn in (pen, bp): glyphs[order[info.codepoint]].draw(TransformPen(pn, (k, 0, 0, -k, (x + pos.x_offset) * k, -pos.y_offset * k)))
        x += pos.x_advance
    return {'d': pen.getCommands(), 'advance': x / upem, 'bbox': [round(v, 4) for v in bp.bounds]}

out = {}
for key, (f, s) in EXTRA.items():
    d = os.environ.get('NOTO_BOLD_DIR', '') if f.startswith('NotoSerif') else os.path.join(ROOT, 'fonts')
    out[key] = shape(os.path.join(d, f), s)
for script, strings in LABELS.items():
    path = os.path.join(ROOT, 'fonts', FONTS[script])
    blob = hb.Blob.from_file_path(path)
    font = hb.Font(hb.Face(blob))
    tt = TTFont(path)
    upem = tt['head'].unitsPerEm
    glyphs = tt.getGlyphSet()
    order = tt.getGlyphOrder()
    for s in strings:
        buf = hb.Buffer()
        buf.add_str(s)
        buf.guess_segment_properties()
        hb.shape(font, buf)
        pen = SVGPathPen(glyphs)
        x = 0
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            k = 1 / upem
            t = TransformPen(pen, (k, 0, 0, -k, (x + pos.x_offset) * k, -pos.y_offset * k))
            glyphs[order[info.codepoint]].draw(t)
            x += pos.x_advance
        out[s] = {'d': pen.getCommands(), 'advance': x / upem}
dest = os.path.join(ROOT, 'brand', 'shaped-labels.json')
json.dump(out, open(dest, 'w'), ensure_ascii=False)
print('wrote', len(out), 'labels to', dest)
