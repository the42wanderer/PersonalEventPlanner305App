# Pouch labels handover: Illustrator masters, print PDFs (3 mm bleed), cut lines, previews, fonts, copy sheet.
#   python3 tools/handover/pouch_package.py OUTDIR
import sys, os, re, json, shutil, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); sys.path.insert(0, R + '/tools')
import svgmaster as SM, copysheet as CS, pouch_labels as PL
OUT = sys.argv[1]; WORK = OUT + '/_work'
for d in ('1_EDITABLE', '2_PRINT', '3_CUTLINE', 'previews', 'fonts', '_work'): os.makedirs(f'{OUT}/{d}', exist_ok=True)
FONTS = SM.Fonts(PL.FONT, ('SiB', 'TaB', 'SiS', 'TaS'))
css = ''.join(f"@font-face{{font-family:{k};src:url(file://{v})}}" for k, v in PL.FONT.items())
NAMES = {'natural-vanilla-tea-100g': 'Vanilla Tea 100 g', 'vanilla-cinnamon-tea-100g': 'Vanilla & Cinnamon Tea 100 g'}
pages, items_all = [], []
for k in PL.PRODUCTS:
    for side, fn in (('front', PL.front), ('back', PL.back)):
        svg = fn(k); name = f'{k}_{side}'
        master, items = SM.convert(svg, FONTS, None, f'The Vanilla Shop {NAMES[k]} pouch label, {side}, 70 x 110 mm, 3 mm bleed')
        master = master.replace('<path id="Cut_line"', '<g id="Dieline_do_not_print"><path id="Cut_line"', 1)
        master = re.sub(r'(<path id="Cut_line"[^>]*/>)', r'\1</g>', master, count=1)
        open(f'{OUT}/1_EDITABLE/{name}_EDITABLE.svg', 'w', encoding='utf-8').write(master)
        items_all.append((f'{NAMES[k]}', side, items))
        pw, ph = PL.W + 2 * PL.BLEED, PL.H + 2 * PL.BLEED
        art = re.sub(r'<path id="Cut_line"[^>]*/>', '', svg)
        art = re.sub(r'width="[\d.]+mm" height="[\d.]+mm"', f'width="{pw}mm" height="{ph}mm"', art, count=1)
        cut = re.sub(r'<g id="Label".*?</g></svg>', '</svg>', svg, flags=re.S)
        for kind, body in (('PRINT', art), ('CUTLINE', cut)):
            h = (f'<html><head><meta charset="utf-8"><style>{css}@page{{size:{pw}mm {ph}mm;margin:0}}html,body{{margin:0}}'
                 f'svg{{display:block}}</style></head><body>{body}</body></html>')
            f = f'{WORK}/{name}_{kind}'; open(f + '.html', 'w', encoding='utf-8').write(h); pages.append([f, pw, ph])
json.dump(pages, open(f'{WORK}/man.json', 'w'))
subprocess.run(['node', '/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/ext/d/printpdf.mjs', f'{WORK}/man.json'], check=True)
for f, _, _ in pages:
    b = os.path.basename(f); shutil.move(f + '.pdf', f'{OUT}/{"2_PRINT" if b.endswith("PRINT") else "3_CUTLINE"}/{b}.pdf')
for f in ('instrument-serif-italic.ttf', 'geist-regular.ttf', 'geist-medium.ttf', 'noto-serif-sinhala.ttf', 'noto-serif-tamil.ttf',
          'noto-sans-sinhala.ttf', 'noto-sans-tamil.ttf', 'OFL-instrument-serif.txt'):
    shutil.copy(f'{R}/fonts/{f}', f'{OUT}/fonts/')
LABELS = {'IS': 'Instrument Serif Italic', 'G': 'Geist Regular', 'GM': 'Geist Medium', 'SiB': 'Noto Serif Sinhala Bold',
          'TaB': 'Noto Serif Tamil Bold', 'SiS': 'Noto Sans Sinhala Medium', 'TaS': 'Noto Sans Tamil Medium'}
products = [(f'{n} ({side})', its, LABELS, {'Label': side.capitalize()}) for n, side, its in items_all]
colours = [['Both', 'Ink (all text, logo, lion, barcode)', '#143A1D', 'Deep green, as on the approved labels'],
           ['Both', 'Soft ink (batch field labels, dotted lines)', '#5C6F5F', ''],
           ['Both', 'Cards', '#FFFFFF', 'White card with a 0.18 mm rule in the ink at 50%'],
           ['Both', 'Ground and paintings', 'embedded images', 'Dusk paper ground, vine, tendril and trailing leaves']]
todo = [['Both', 'MRP, MFD, EXP and batch number', 'Back, batch card', 'Left blank to stamp per batch, as on the current pouch'],
        ['Both', 'Sinhala and Tamil names', 'Front card, back', 'Native speaker to check; கறுவா is the Sri Lankan Tamil word for cinnamon'],
        ['Both', 'Back sticker size', 'Back', 'Drawn on the front\'s die (70 x 110 mm); confirm it fits the pouch back'],
        ['Both', 'Barcode size', 'Back', 'About 67% of nominal, as on the current pouch; test-scan before print'],
        ['Both', 'Net weight in bold', 'Front top bar, back', 'The regulations ask for bold net contents; confirm the treatment with the FCAU']]
readme = ['The Vanilla Shop: 100 g tea pouch labels, front and back, copy sheet',
          'Every piece of text on the four labels. Copy from column D instead of retyping, Sinhala and Tamil included.',
          'Pink rows are placeholders; the "To fill" tab lists what is outstanding.']
print('rows', CS.write(f'{OUT}/Pouch-labels_COPY-SHEET.xlsx', products, colours, todo, readme))
shutil.rmtree(WORK)
