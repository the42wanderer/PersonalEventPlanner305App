# Tote bag, The Vanilla Shop Negombo: Ceylon stamp, one ink, halftone (front)

This is the chosen front. It replaces the three-ink stamp in `../3ink/`.

## The print

- **Bag:** natural cotton canvas, 15 × 16 in (381 × 406 mm).
- **Art:** 270 × 338 mm, centred left to right, 48 mm below the top seam.
- **One screen:** black. Water-based or discharge ink is best, so the print stays soft; about 46% of the art area is
  black.

## Files

- **`tote-stamp-halftone_FILM.pdf` / `.png`:**
  - one positive, black on white, at actual size;
  - 1-bit, 20 px/mm (508 dpi);
  - all lettering already in it.
- **`tote-stamp-halftone_mockup.jpg`, `_mockup-detail.jpg`:** for approval only.

## Notes for the printer

- **The grey tones are a true halftone:** round dots at 45°, 1.3 mm apart (about 20 lpi). Keep them as dots. Do not
  re-screen or smooth them.
- **Smallest marks:**
  - halftone dots about 0.32 mm across;
  - lines about 0.3 mm.
- **Mesh:** a fine mesh, about 110–160 T (280–355 in US threads).
- **Test first:** print one bag on the actual canvas before the run. Check that the light dots in the sky hold and
  that the dark tints don't close up.

## Lettering

- **Top banner:** CEYLON, with ලංකා and இலங்கை, following the arch.
- **Tablet:** 25c.
- **Caption box:** THE VANILLA SHOP / NEGOMBO.
- **Fonts:** Gloock, Geist, Noto Serif Sinhala and Noto Serif Tamil, all OFL.
- **Before the film is made,** have a native speaker check the Sinhala and Tamil.

## How it was made

The illustration was generated with GPT Image 2.5 Sunburst (`source-sunburst.webp`; the prompt is in
`studies/tote/sunburst/PROMPT-comic-halftone.txt`), then finished in code (`film2.py`, `rescreen.py`):
- **Line work:** the brush line work is kept.
- **Halftone:** the generator's uneven mix of dot patterns is replaced with one consistent halftone sized for
  canvas. The faces keep their original drawing.
- **Flower:** the flower at the woman's hands, which had come out lily-shaped, is given its vanilla trumpet lip.
- **Lettering:** set in the empty boxes.
- **Clean-up:** specks too small to print are removed.

`mock1.py` makes the mock-up.
