# Copy sheet: every piece of text on a set of masters, one row each (paragraphs joined), so the designer can paste
# text (Sinhala and Tamil included) instead of retyping it, and the client can mark changes in one place.
#   copysheet.write(path, products=[(product name, items, font labels)], colours=[(product, role, hex)], todo=[...])
import math, re
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter
import svgmaster as SM

PT = 72 / 25.4
def lang(t):
    if re.search('[඀-෿]', t): return 'Sinhala'
    if re.search('[஀-௿]', t): return 'Tamil'
    return 'English'
def todo_flag(t):
    return bool(re.search(r'__|PLACEHOLDER|2000000000008|REPLACE', t))
HEAD = Font(bold=True, color='FFFFFF'); HFILL = PatternFill('solid', fgColor='4A2C08'); TFILL = PatternFill('solid', fgColor='FFD3EA')

def sheet(ws, header, rows, widths):
    ws.append(header)
    for c in ws[1]: c.font = HEAD; c.fill = HFILL; c.alignment = Alignment(vertical='center')
    for r in rows: ws.append(r)
    for i, w in enumerate(widths, 1): ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2):
        for c in row: c.alignment = Alignment(wrap_text=True, vertical='top')
    ws.freeze_panes = 'A2'

def write(path, products, colours, todo, readme):
    wb = Workbook(); ws = wb.active; ws.title = 'Read me'
    for line in readme: ws.append([line])
    ws.column_dimensions['A'].width = 120
    ws['A1'].font = Font(bold=True, size=14)
    rows = []
    for name, items, labels, panel_names in products:
        for p in SM.paragraphs(items):
            t = p['text'].strip()
            if not t or re.fullmatch(r'\d{1,6}', t): continue           # barcode digits: part of the barcode
            m = p['ctm']; k = math.sqrt(abs(m[0] * m[3] - m[1] * m[2]))
            rows.append([name, panel_names.get(p['panel'], p['panel']), lang(t), t, labels.get(p['font'], p['font']),
                         round(p['size'] * k * PT, 1), ('Gold foil + ' if p.get('foil') else '') + (p['fill'] or '').upper(),
                         'TO FILL' if todo_flag(t) else ''])
    ws2 = wb.create_sheet('Copy')
    sheet(ws2, ['Product', 'Panel', 'Language', 'Text (copy from here)', 'Font', 'Size (pt)', 'Colour', 'Status'], rows,
          [22, 22, 10, 90, 30, 9, 16, 10])
    for row in ws2.iter_rows(min_row=2):
        if row[7].value == 'TO FILL':
            for c in row: c.fill = TFILL
    ws3 = wb.create_sheet('Colours')
    sheet(ws3, ['Product', 'Use', 'Hex', 'Note'], colours, [22, 30, 12, 60])
    ws4 = wb.create_sheet('To fill')
    sheet(ws4, ['Product', 'What', 'Where', 'Status'], todo, [22, 50, 30, 30])
    wb.save(path)
    return len(rows)
