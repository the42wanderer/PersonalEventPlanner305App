# Jar labels (No. 04 Vanilla Paste, No. 05 Vanilla Powder, 100 g, 200 x 42 mm) handover: Illustrator masters with a
# TO_FILL layer, print PDFs with bleed, cut lines, trimmed previews, fonts, copy sheet.
#   python3 tools/handover/jar_package.py ARTDIR OUTDIR
import sys, os, re, json, shutil, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); sys.path.insert(0, R + '/studies/extract/split')
import svgmaster as SM, copysheet as CS, jarwrap as JW
import kit
ARTDIR, OUT = sys.argv[1], sys.argv[2]; WORK = OUT + '/_work'
for d in ('1_EDITABLE', '2_PRINT', '3_CUTLINE', 'previews', 'fonts', '_work'): os.makedirs(f'{OUT}/{d}', exist_ok=True)
USED = ('G', 'GB', 'IS', 'RW', 'SiB', 'TaB', 'SiS', 'TaS')
FONTS = SM.Fonts({k: kit.FONTS[k] for k in USED}, ('SiB', 'TaB', 'SiS', 'TaS'))
NAMES = {'04': 'No04-Vanilla-Paste-100g', '05': 'No05-Vanilla-Powder-100g'}
W2, H2 = JW.W + 2 * JW.B, JW.H + 2 * JW.B
cut = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W2}mm" height="{H2}mm" viewBox="{-JW.B} {-JW.B} {W2} {H2}">'
       f'<rect width="{JW.W}" height="{JW.H}" fill="none" stroke="#EC008C" stroke-width="0.25"/></svg>')
pages, items_all = [], []
for k, name in NAMES.items():
    JW.MASTER = True; m = JW.svg(JW.wrap(k, ARTDIR))
    master, items = SM.convert(m, FONTS, None, f'The Vanilla Shop {name} jar wrap, 200 x 42 mm, 3 mm bleed')
    master = master.replace('</svg>', f'<g id="Dieline_do_not_print"><rect width="{JW.W}" height="{JW.H}" fill="none" stroke="#EC008C" stroke-width="0.25"/></g></svg>')
    open(f'{OUT}/1_EDITABLE/{name}_EDITABLE.svg', 'w', encoding='utf-8').write(master); items_all.append((name, items))
    JW.MASTER = False; p = JW.svg(JW.wrap(k, ARTDIR))
    for kind, body in (('PRINT', p), ('CUTLINE', cut)):
        h = (f'<html><head><meta charset="utf-8"><style>{kit.css}@page{{size:{W2}mm {H2}mm;margin:0}}html,body{{margin:0}}svg{{display:block}}</style>'
             f'</head><body>{body}</body></html>')
        f = f'{WORK}/{name}_{kind}'; open(f + '.html', 'w', encoding='utf-8').write(h); pages.append([f, W2, H2])
    pv = re.sub(r'width="[\d.]+mm" height="[\d.]+mm" viewBox="[^"]+"', f'width="2000" height="420" viewBox="0 0 {JW.W} {JW.H}"', p, count=1)
    open(f'{WORK}/{name}_preview.html', 'w', encoding='utf-8').write(f'<html><head><meta charset="utf-8"><style>{kit.css}html,body{{margin:0}}</style></head><body>{pv}</body></html>')
json.dump(pages, open(f'{WORK}/man.json', 'w'))
T = '/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/ext/d/'
subprocess.run(['node', T + 'printpdf.mjs', f'{WORK}/man.json'], check=True)
subprocess.run(['node', T + 'shot.mjs', '2000', '420'] + [f'{WORK}/{n}_preview' for n in NAMES.values()], check=True)
for f, _, _ in pages:
    b = os.path.basename(f); shutil.move(f + '.pdf', f'{OUT}/{"2_PRINT" if b.endswith("PRINT") else "3_CUTLINE"}/{b}.pdf')
from PIL import Image
ims = []
for n in NAMES.values():
    im = Image.open(f'{WORK}/{n}_preview.png').convert('RGB'); im.save(f'{OUT}/previews/{n}.jpg', quality=90); ims.append(im)
both = Image.new('RGB', (2000, 860), 'white'); both.paste(ims[0], (0, 0)); both.paste(ims[1], (0, 440)); both.save(f'{OUT}/previews/both.jpg', quality=88)
for f in ('instrument-serif-italic.ttf', 'geist-regular.ttf', 'geist-bold.ttf', 'archivo-expanded-regular.ttf', 'noto-serif-sinhala.ttf',
          'noto-serif-tamil.ttf', 'noto-sans-sinhala.ttf', 'noto-sans-tamil.ttf', 'OFL-instrument-serif.txt', 'OFL-archivo.txt'):
    shutil.copy(f'{R}/fonts/{f}', f'{OUT}/fonts/')
LABELS = {'G': 'Geist Regular', 'GB': 'Geist Bold', 'IS': 'Instrument Serif Italic', 'RW': 'Archivo Expanded (SemiBold Expanded)',
          'SiB': 'Noto Serif Sinhala Bold', 'TaB': 'Noto Serif Tamil Bold', 'SiS': 'Noto Sans Sinhala Medium', 'TaS': 'Noto Sans Tamil Medium'}
products = [(n, its, LABELS, {}) for n, its in items_all]
colours = []
for k, n in NAMES.items():
    L = JW.JAR[k]['look']
    colours += [[n, 'Colour half (painted ground)', {'04': '#5E3A2A', '05': '#6A2C4A'}[k], 'Cocoa for the paste, plum for the powder; the painting is an embedded image'],
                [n, 'Main ink (cream half)', L['dark'], ''], [n, 'Second ink (small capitals, Tamil name)', L['deep'], ''],
                [n, 'Text on the colour half', L['on'], 'Captions in ' + L['on2']]]
colours.append(['Both', 'Cream half', JW.PAPER, 'Could be left as paper on a cream stock'])
todo = [['Both', 'Ingredients', 'Right of the front card', 'Production to supply'],
        ['Both', 'Barcode (EAN-13)', 'Right of the front card', 'Placeholder 2000000000008'],
        ['Both', 'MRP', 'Right of the front card', 'Website: paste Rs 3,700 (100 ml), powder Rs 4,100 (listed as 50 g); confirm for 100 g'],
        ['Both', 'MFD / EXP', 'Right of the front card', 'Blank: stamp per batch or supply'],
        ['Both', 'Closing line of the story', 'Colour half', 'Ours: confirm it describes how each is made'],
        ['Both', 'Best for, 100% natural', 'Colour half', 'Confirm'],
        ['Both', 'Nutrition panel', 'Not on the label', 'Add if production supplies figures (the extracts carry one)'],
        ['Both', 'Certification marks (USDA, SGS, EU organic)', 'Not on the label', 'Add only if these products are certified'],
        ['Both', 'Sinhala and Tamil names', 'Front card, right block', 'Native speaker to check'],
        ['Both', 'Net weight', 'Front card', '100 g on the printer template; the website lists the powder as 50 g']]
readme = ['The Vanilla Shop: jar labels No. 04 Vanilla Paste and No. 05 Vanilla Powder, copy sheet',
          'Every piece of text on both labels. Copy from column D instead of retyping, Sinhala and Tamil included.',
          'Pink rows are placeholders; the "To fill" tab lists what is outstanding.']
print('rows', CS.write(f'{OUT}/Jar-labels_COPY-SHEET.xlsx', products, colours, todo, readme))
shutil.rmtree(WORK)
