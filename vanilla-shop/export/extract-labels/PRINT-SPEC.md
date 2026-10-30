# The Vanilla Shop extract labels: print files

Ten labels, each a PDF in `print/`:
- **Wraps:** No. 01 and No. 02 at 500, 200 and 100 ml; No. 03 at 500 ml.
- **Neck seals:** one per product.

Each page has:
- the artwork at actual size, with 3 mm bleed on every side;
- crop marks at the trim;
- a note under it with the product, size and status.

Text is live vector type with the fonts embedded, so it stays sharp at any size. The colour artwork is an image at
over 400 dpi at these sizes.

`cutlines/` holds one matching file per label, with only the cut line in magenta in the same position as the artwork.
Use it to make the die, or redraw the die from your own template.

## Editable files: open these, not the PDFs

`editable/` holds one SVG master per label. **Open them in Illustrator with File > Open**, then save as `.ai`. Don't
edit the print PDFs: opening a PDF in Illustrator breaks its text into fragments and garbles the Sinhala and Tamil.

In the masters:
- **English text is live.** Each line is one text object, so it stays one object when opened, not split word by
  word. Install the fonts listed below first, or Illustrator will substitute them.
- **Alignment:** centred and right-aligned lines are placed by their left edge, so they open exactly in place. After
  editing one, re-centre it by eye or with the Align panel.
- **Sinhala and Tamil print as outlines,** shaped correctly. Illustrator's default text engine cannot shape these
  scripts, which is why they aren't live.
  - Each has a **live twin** in the hidden layer `Sinhala_Tamil_live_text`: same font, size and position.
  - To change the wording:
    1. Show that layer.
    2. Turn on Paragraph > World-Ready Paragraph Composer.
    3. Edit the text.
    4. Check it against the outline.
    5. Delete the outline.
- **The artwork and certification marks are embedded,** so the file is self-contained.
- **The cut line** is in the `Dieline` layer, in magenta. It does not print.

## Sizes

| Label | Trim size | Status |
|---|---|---|
| 500 ml wraps (No. 01, 02, 03) | 274.0 × 84.9 mm | **The size of the current labels** (`vanilla_labeels__final-01.pdf`, marked 8.5 cm) |
| 200 ml wraps (No. 01, 02) | 201.3 × 50.9 mm | **Estimated.** Measure the bottle and adjust |
| 100 ml wraps (No. 01, 02) | 160.0 × 42.4 mm | **Estimated.** Measure the bottle and adjust |
| Neck seals (No. 01, 02, 03) | 120.1 × 22.6 mm | **The current seal's size and die shape** |

How the 200 and 100 ml sizes were estimated: the 500 ml wrap goes once round the bottle. The smaller bottles were
scaled from it by volume and checked against a photo of all three. The details are in
`studies/extract/split/SIZES.md`.

### Adjusting the 200 and 100 ml labels

- Measure the bottle's circumference at the label and the height of the flat label band.
- **If the real size is close (a few millimetres either way):** scale the artwork to fit, keeping its proportions.
- **If the proportions are clearly different:** don't stretch it. Ask us for a re-set file, which is quick to make.
- **The neck seal is the same for all three bottle sizes,** like the current one. If the 100 ml and 200 ml necks are
  narrower, shorten its arms.

## Languages (Sri Lanka's labelling regulations, in force 1 July 2026)

As on the tea boxes: the product's name in English and Sinhala on the front card, in Tamil on the colour side, and
the dates labelled in all three. `previews/` shows every label.

| Where | Text | Size |
|---|---|---|
| Front card, under the English name | වැනිලා සාරය (Nos. 01, 02) · වැනිලා සිරප් (No. 03), Noto Serif Sinhala Bold | Letters 3 mm high |
| Colour side | வெனிலா சாறு (Nos. 01, 02) · வெனிலா சிரப் (No. 03), Noto Serif Tamil Bold | Letters 3 mm high |
| MFD and EXP | Labelled නි.දි. / பொ.செ திகதி and කා.ඉ.දි. / மு.திகதி, as on the tea pack on sale; dates in bold | Figures 1.5 mm high |

"3 mm" is measured on the letters with no strokes above or below (in Sinhala ය, න, ස; in Tamil வ, ம), as the rule
measures lowercase letters.

The 3 mm minimum does not shrink with the label, so the smaller sizes are re-set:
- **500 ml:** the Sinhala name on one line under "Vanilla Extract". The English is a little smaller to make room, and
  the lower rule is gone.
- **200 ml:** the Sinhala name in two lines, the logo smaller, "Premium quality" and the rules removed. The Tamil
  name is on one line under the story.
- **100 ml:** the same front, without the corner marks. The logo moves to the colour side, and the Tamil name, in two
  lines, takes the story's place.

**Before printing:**
- Have a native Sinhala and Tamil reader check the names on a printed proof. The translations are ours.
- Ask the Food Control Administration Unit whether "with alcohol" / "alcohol-free" is part of the common name. If it
  is, it needs translating too.
- Two points are still open, as on the tea boxes:
  - The regulations ask for the common name and the net contents in bold. "Vanilla Extract" and "500 ml" are in
    Instrument Serif Italic, which has no bold.
  - The 100 ml English name is at the 3 mm minimum.

## Placeholders to replace before printing

- **Barcodes on the 200 and 100 ml labels** are placeholders: they repeat the 500 ml code. Each size needs its own
  EAN-13.
- **The 500 ml barcodes** are from the current labels: …0007 (No. 01), …0038 (No. 02) and …0083 (No. 03). Confirm
  they still belong to these products.
- **MFD and EXP** (01/02/2025, 31/01/2027) are as printed on the current labels. Change them for each print run.
- **MRP for 200 and 100 ml** is taken from the shop's website and Glomark. Check it.

## Colour and finish

- **Colour:** the files are RGB. Convert to CMYK, or match to your press, with your own profile.
- **Product colours:**

  | Product | Colour |
  |---|---|
  | No. 01 | vermilion #B83A24 |
  | No. 02 | honey #C98A22 |
  | No. 03 | green #2F5A33 |
  | Cream | #F7EFDC |

  The cream half was designed to look like the paper, so on a cream or uncoated stock you could leave it unprinted.
  Tell us if you do.
- **Stock and finish:** a matt or uncoated label stock suits the soft artwork. If you print on clear film, the cream
  areas need a white underprint.
- **Run a proof first.** Check the smallest type: the 100 ml back goes down to about 1.4 mm at this size. Check the
  barcodes with a scanner.

## Fonts (all free to use in print)

- Instrument Serif;
- Geist;
- Archivo Expanded (the spaced capitals);
- Noto Serif Sinhala Bold and Noto Serif Tamil Bold (the names);
- Noto Sans Sinhala Medium and Noto Sans Tamil Medium (the date labels).

All are under the SIL Open Font License; the files are in `vanilla-shop/fonts`.

## Rebuilding

`scripts/export.py` makes these files from the design (`splitwrap.py` for the wraps, `neck.py` for the seals).
`studies/extract/split/RESUME.md` explains the setup.
