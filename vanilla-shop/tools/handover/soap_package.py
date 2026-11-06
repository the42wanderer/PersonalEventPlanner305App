# Assemble the soap-box handover: masters, print/foil/proof PDFs, previews, fonts, copy sheet, README.
import sys, os, json, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import copysheet as CS
R = '/home/user/PersonalEventPlanner305App/vanilla-shop'; SB = R + '/export/soap-boxes-final'
SRC = sys.argv[1]; OUT = sys.argv[2]
for d in ('1_EDITABLE', '2_PRINT', '3_FOIL', '4_PROOF', 'previews', 'fonts'): os.makedirs(f'{OUT}/{d}', exist_ok=True)
NAMES = {'vanilla': 'Vanilla Bathing Bar', 'rosette': 'Vanilla & Rose', 'charcoal': 'Vanilla & Charcoal+', 'aloe': 'Vanilla & Aloe Vera'}
for k in NAMES:
    shutil.copy(f'{SRC}/{k}_box_EDITABLE.svg', f'{OUT}/1_EDITABLE/')
    shutil.copy(f'{SB}/print/{k}_box_PRINT.pdf', f'{OUT}/2_PRINT/'); shutil.copy(f'{SB}/foil/{k}_box_FOIL.pdf', f'{OUT}/3_FOIL/')
    shutil.copy(f'{SB}/proof/{k}_box_PROOF.pdf', f'{OUT}/4_PROOF/')
for f in ('fronts.png', 'mockup-boxes.png', 'all-four-proofs.jpg', 'back-detail.jpg'): shutil.copy(f'{SB}/{f}', f'{OUT}/previews/')
FONTFILES = ['instrument-serif.ttf', 'instrument-serif-italic.ttf', 'geist-regular.ttf', 'geist-bold.ttf', 'archivo-expanded-regular.ttf',
             'noto-serif-sinhala.ttf', 'noto-serif-tamil.ttf', 'OFL-instrument-serif.txt', 'OFL-archivo.txt']
for f in FONTFILES: shutil.copy(f'{R}/fonts/{f}', f'{OUT}/fonts/')
items = json.load(open(f'{SRC}/_items.json', encoding='utf-8'))
LABELS = {'G': 'Geist Regular', 'GB': 'Geist Bold', 'IS': 'Instrument Serif Italic', 'ISR': 'Instrument Serif Regular',
          'RW': 'Archivo Expanded (SemiBold Expanded)', 'NSi': 'Noto Serif Sinhala Bold', 'NTa': 'Noto Serif Tamil Bold'}
PANELS = {'back': 'Back (upside down)', 'top_wall': 'Top wall', 'front': 'Front', 'left_wall': 'Left wall',
          'bottom_wall': 'Bottom wall', 'right_wall': 'Right wall'}
INK = {'vanilla': ('#5A3410', '#8A5A10'), 'rosette': ('#5A1426', '#9A3550'), 'charcoal': ('#141414', '#55504B'), 'aloe': ('#16301C', '#3F7A47')}
colours = []
for k, (i, d) in INK.items():
    colours += [[NAMES[k], 'Main ink (names, text)', i, ''], [NAMES[k], 'Second ink (small capitals, labels)', d, '']]
colours += [['All four', 'Gold foil', '#B8924A in the masters', 'Stand-in colour only. Foil: "Vanilla" on the front and right wall, the pod on the back. Use the FOIL plate PDF; make it a spot swatch named Foil_Gold, set to overprint.'],
            ['All four', 'Background art', 'embedded image', 'The flower and paper texture under everything, one image per box.']]
todo = [['Vanilla & Charcoal+', 'Barcode (EAN-13)', 'Left wall', 'Placeholder 2000000000008'], ['Vanilla & Aloe Vera', 'Barcode (EAN-13)', 'Left wall', 'Placeholder 2000000000008'],
        ['Vanilla & Charcoal+', 'MFD / EXP', 'Left wall', 'Blank'], ['Vanilla & Aloe Vera', 'MFD / EXP', 'Left wall', 'Blank'],
        ['Vanilla & Charcoal+', 'TFM %', 'Top wall', 'Blank'], ['Vanilla & Aloe Vera', 'TFM %', 'Top wall', 'Blank'],
        ['All four', 'Full ingredients list', 'Back, bottom', 'Stops at "glycerin," on the boxes on sale: production to supply'],
        ['All four', 'Net weight: 100 g (boxes) or 114 g (website)', 'Front, top wall', 'Confirm'],
        ['Vanilla & Charcoal+', 'What the + stands for', 'Front', 'Decide; add a line on the back if it means something'],
        ['All four', 'Tamil text', 'Back, top wall', 'Native speaker to check'],
        ['All four', 'Claims: 100% natural, reduces fine lines, own farms', 'Front, back', 'Check against NMRA cosmetic rules']]
products = [(NAMES[k], [dict(i, ctm=tuple(i['ctm'])) for i in items[k]], LABELS, PANELS) for k in NAMES]
readme = ['The Vanilla Shop: soap boxes, copy sheet',
          'Every piece of text on the four boxes, in reading order by panel. Copy text from column D instead of retyping it (Sinhala and Tamil included).',
          'Pink rows are placeholders still to fill. The "To fill" tab lists everything outstanding; the "Colours" tab has every ink.',
          'To request a change, edit the text here and highlight the cell.']
n = CS.write(f'{OUT}/Soap-boxes_COPY-SHEET.xlsx', products, colours, todo, readme)
print('rows', n)
