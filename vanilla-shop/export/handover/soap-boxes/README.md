# The Vanilla Shop: soap boxes, designer handover

Four boxes on the current soap box's flat layout: 190.3 × 221.5 mm flat, 3 mm bleed. The back panel prints upside
down so it reads correctly once folded.

| Box | Files |
|---|---|
| Vanilla Bathing Bar | `vanilla_box_*` |
| Vanilla & Rose | `rosette_box_*` |
| Vanilla & Charcoal+ | `charcoal_box_*` |
| Vanilla & Aloe Vera | `aloe_box_*` |

## Folders

| Folder | What it is |
|---|---|
| `1_EDITABLE/` | **Work in these.** One Illustrator master per box: File > Open, then save as `.ai`. |
| `2_PRINT/` | Print PDFs as approved: CMYK art, foil areas left as paper. For the printer, not for editing. |
| `3_FOIL/` | Foil plates, in register with the print files (solid black = gold foil). |
| `4_PROOF/` | Proofs: magenta = cut, cyan dashes = folds, pink = text to check, foil simulated. |
| `previews/` | Fronts, the four boxes in 3D and the proofs side by side. |
| `fonts/` | Every font used. All free, under the SIL Open Font License. Install before opening the masters. |
| `Soap-boxes_COPY-SHEET.xlsx` | All the text, ready to copy. Also lists the inks and what is still to fill. |

## In the masters

The layers:
- **`Artwork`:** everything that prints.
- **`TO_FILL`:** pink boxes over each placeholder. Delete them once filled.
- **`Sinhala_Tamil_live_text`:** hidden. Editable copies of the Sinhala and Tamil.
- **`Dieline_do_not_print`:** cut in magenta, folds in cyan.

**English text:** live, one text object per line, so nothing opens split up word by word. Paragraphs come in as
separate lines. To reflow one, paste it from the copy sheet into one text box.

**Alignment:** centred and right-aligned lines are placed by their left edge, so they open exactly in place. After
editing one, re-centre it with the Align panel. Text on the side walls and back is rotated, as it is on the box.

**Sinhala and Tamil:** these are outlines, shaped correctly; Illustrator's default text engine cannot shape these
scripts. To change one:
1. Show `Sinhala_Tamil_live_text`.
2. Turn on Paragraph > World-Ready Paragraph Composer.
3. Edit the copy, or paste the text from the copy sheet.
4. Check it against the outline.
5. Delete the outline.

**Gold foil:** "Vanilla" on the front and on the right wall, and the small pod on the back. In the masters it is
coloured #B8924A as a stand-in. For print:
1. Make it a spot swatch named `Foil_Gold`, set to overprint.
2. Check it against `3_FOIL/`.
3. Leave the print layer unprinted under the foil.

**Background:** each box's flower and paper texture is one embedded image.

## Still to fill

The `To fill` tab in the copy sheet lists these:
- **Vanilla & Charcoal+ and Vanilla & Aloe Vera:** barcodes, MFD/EXP and TFM.
- **All four:**
  - the full ingredients;
  - the net weight: 100 g on the boxes, 114 g on the website;
  - a native speaker's check of the Tamil;
  - the claims, checked against the NMRA cosmetic rules.
- **Vanilla & Charcoal+:** what the "+" stands for.
