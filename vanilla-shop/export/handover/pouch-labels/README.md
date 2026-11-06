# The Vanilla Shop: 100 g tea pouch labels, designer handover

Two products, each with a front and a back label. Both are 70 × 110 mm on the same arched die, with 3 mm bleed.

| Label | What it carries |
|---|---|
| Front | The approved design. The card at the foot now carries the name in **Sinhala** (වැනිලා තේ / වැනිලා කුරුඳු තේ); the barcode has moved to the back. |
| Back | The name in **Tamil** (வெனிலா தேயிலை / வெனிலா கறுவா தேயிலை), stacked like the English on the front. Then the net weight in English, Sinhala and Tamil, the distributor (as on the tea pack on sale), and the barcode with MRP, MFD, EXP and B.N. labelled in all three languages. |

Why: Sri Lanka's labelling regulations (in force 1 July 2026) ask for the common name in two languages on the main
panel and the third on any panel. The expiry date needs two languages. The names are bold, with letters 3 mm high.

## Folders

| Folder | What it is |
|---|---|
| `1_EDITABLE/` | **Work in these.** Illustrator masters: File > Open, then save as `.ai`. |
| `2_PRINT/` | Print PDFs with bleed, fonts embedded. |
| `3_CUTLINE/` | The die line alone, in magenta, in the same position. |
| `previews/` | Each label, and all four side by side. |
| `fonts/` | Every font used. All free (SIL Open Font License). Install before opening the masters. |
| `Pouch-labels_COPY-SHEET.xlsx` | All the text, ready to copy, with fonts, sizes, inks and what is still open. |

## In the masters

**English text:** live, one text object per line. The earlier pouch-label files had every letter outlined; these
don't. Centred and right-aligned lines are placed by their left edge, so they open in place. Re-centre with the
Align panel after editing.

**Sinhala and Tamil:** these are outlines, shaped correctly; Illustrator's default text engine cannot shape these
scripts. Each has an editable copy in the hidden layer `Sinhala_Tamil_live_text`. To change one:
1. Show the layer.
2. Turn on Paragraph > World-Ready Paragraph Composer.
3. Edit or paste the text from the copy sheet.
4. Delete the outline.

**Paintings and ground:** embedded images. The front's vine leaf crossing the name is a clipped copy of the vine,
on top of the type.

**Die line:** in the layer `Dieline_do_not_print`.

## Before print

- **Translations:** a native Sinhala and Tamil reader checks the names. கறுவா is the Sri Lankan Tamil word for
  cinnamon.
- **Back sticker:** confirm the pouch can take one at 70 × 110 mm. It can be made smaller if needed.
- **Batch fields:** MRP, MFD, EXP and B.N. are left blank to stamp per batch, as on the current pouch.
- **Barcode:** about 67% of nominal size, as on the current pouch. Test-scan it.
- **Net weight in bold:** confirm with the FCAU, as for the tea boxes.
