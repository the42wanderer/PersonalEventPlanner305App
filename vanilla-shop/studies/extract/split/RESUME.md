# Extract labels: paused here (20 Oct 2026)

Start here when we pick this up again.

## Where it stands

- **Direction:** Split, on the original rectangular wrap.
  - The colour half holds the drawn vanilla and the story; the cream half holds the front card, nutrition, marks,
    barcode, dates and maker.
  - No. 03's drawing is the coded Watercolour version.
- **Labels designed:**
  - No. 01 and No. 02 at 500, 200 and 100 ml;
  - No. 03 at 500 ml, its only size.
- **Content rule (the user's):** the labels carry only the information on the labels now on sale
  (`vanilla_labeels__final-01.pdf`). The one change kept is the corrected history line. Nothing else is added: no
  ingredients, storage, alcohol strength, dose or calculated figures. `TO-CONFIRM.md` lists exactly where each item
  comes from.
- **Certification marks:** the real USDA Organic, SGS and EU organic icons, taken from the old label file (`marks/`).

## Open questions, waiting on the user or the printer

1. **500 ml label size.** The old file's boxes measure 274 × 84 mm with "8.5 cm" written beside them; the design is
   at 226 × 70 mm.
   - The proportions are the same, so the 500 ml scales evenly with no layout change.
   - The user is passing the files to the printer, who will confirm the size.
2. **200 and 100 ml sizes.** These are estimates (`SIZES.md`).
   - The printer should measure the real labels or bottles.
   - Then re-set the layouts to those sizes. Do not let the printer scale them: if the proportions differ, the
     layout distorts.
3. **Barcodes** for the 200 and 100 ml sizes. They use the 500 ml code as a stand-in for now.
4. **Font licence.** The small capitals use Roc Grotesk Wide. The user's copy is the Fontspring **demo**, which is
   not licensed for commercial print. Buy the licence before production, or swap in another wide grotesque.

## Next steps

1. Get the real sizes, re-set the 200 and 100 ml layouts in `wrap_small()`, and scale the 500 ml if needed.
2. Export clean print PDFs, one per label:
   - exact size, 3 mm bleed and crop marks;
   - no proof highlights;
   - vector text;
   - CMYK, as the printer specifies.
3. Restyle the neck strip: "100% pure natural vanilla", as on the old strip.

## How to rebuild

The scripts were run from the old session's scratch folder. Everything they need is in the repo:

- `splitwrap.py`: the labels.
  - `python3 splitwrap.py` writes `SW-*.html`.
  - `python3 splitwrap.py proof` writes `PR-*.html`, with highlights.
- `build/shot.mjs`: renders the HTML at 20 px/mm. Run `node shot.mjs <w px> <h px> <file without .html>`:
  - 500 ml: 4520 × 1400;
  - 200 ml: 3320 × 840;
  - 100 ml: 2640 × 700.
- `mock.py` with `bottle3.py`: the bottle mock-ups at true relative size.
- `proofpdf2.mjs`: the proof PDF with bleed and crop marks. `build/pdf.mjs`: the actual-size PDF.
- `build/wart-0*.png`: the colour art for the 500 ml wraps (113 × 70 mm at 20 px/mm).
  - `green.py` with `podstyles.py`, `draw.py` and `comp.py` regenerate the art. No. 03 uses `optE('watercolour', 113, 70, 53)`.
- `build/kit.py`, `build/content.py`: type, logo, barcode and the shared content.
- `build/restore.sh <scratchpad dir>`: copies all of this back into the folder layout the scripts expect. It also
  unpacks Roc Grotesk from the user's uploaded zip, if present. The scripts hard-code the old scratch path in `T`, so
  either restore to that same path or update `T`.

Fonts: Geist and Instrument Serif are in `vanilla-shop/fonts`. Roc Grotesk is not committed (demo licence).
