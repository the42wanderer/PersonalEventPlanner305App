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

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LABELS = {
    'sinhala': ['කා.අ.', 'නි.දි.', 'කා.ඉ.දි.', 'උ.සි.මි.රු.'],
    'tamil': ['தொகுதி இல', 'பொ.செ திகதி', 'மு.திகதி', 'விலை ரூபா'],
}
FONTS = {'sinhala': 'noto-sans-sinhala.ttf', 'tamil': 'noto-sans-tamil.ttf'}

out = {}
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
