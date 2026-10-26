# Vanilla Tea, 12 bags: final artwork (Plum)

The cube carton on its real dieline, every panel: front, How to brew, back, What's inside, lid and base.
Sheet 421.5 × 371.5 mm, 3 mm bleed on every printed edge.

| File | What it is |
|---|---|
| `vanilla-tea-12bag-plum_EDITABLE.svg` | The master. One file, artwork embedded, all type live. Open in Illustrator (File > Open), then Save As `.ai`. |
| `vanilla-tea-12bag-plum_EDITABLE-linked.svg` + `art/` | The same, with the panel artwork as linked files in `art/`, for retouching or swapping a panel. Keep the folder next to the SVG. |
| `vanilla-tea-12bag-plum_PROOF.pdf` | Proof at actual size. **Not for press** (see Fonts). |
| `vanilla-tea-12bag-plum_flat-preview.jpg`, `_3d.jpg` | Previews. |

## Layers

`Background` · `Ground` (the landscape artwork, one image per wall and one for the lid) · `Painting` · `Name`
(Vanilla / Tea / the Sinhala name) · `Weave` · `Texture` (fine grain over the artwork, 25%) · `Type_and_Icons` (grouped
per panel: `Front`, `Side_How_to_brew`, `Back`, `Side_Whats_inside`, `Base`, `Lid`) · `Sinhala_Tamil_live_text`
(hidden, see below) · `Barcode` · `Lid_ring_path` · `Dieline` (magenta; not to print).

## Fonts

Install these before opening, or Illustrator will substitute them. All English type is live text.

| Font (PostScript name) | Used for | Where to get it |
|---|---|---|
| Instrument Serif Italic (`InstrumentSerif-Italic`) | Vanilla, Tea, the headings | Google Fonts (OFL). Also in the repo: `fonts/instrument-serif-italic.ttf` |
| Roc Grotesk (`RocGrotesk-Regular`) | Body text | Adobe Fonts |
| Roc Grotesk Wide (`RocGroteskWide-Regular`, `-Light`, `-Bold`) | Labels, 12 TEA BAGS, NET WT., brew steps | Adobe Fonts |
| Noto Serif Sinhala Bold (`NotoSerifSinhala-Bold`) | වැනිලා තේ (front) | Google Fonts (OFL). Also `fonts/noto-serif-sinhala.ttf` |
| Noto Serif Tamil Bold (`NotoSerifTamil-Bold`) | வெனிலா தேயிலை (What's inside) | Google Fonts (OFL). Also `fonts/noto-serif-tamil.ttf` |
| Noto Sans Sinhala Medium / Noto Sans Tamil Medium | Brew steps, net weight labels, base | Google Fonts (OFL). Also `fonts/noto-sans-*.ttf` |

**The proof PDF was made with the free demo of Roc Grotesk**, which lacks a few characters ( · 4 ’ ( ) @ ); those
characters are borrowed from Archivo / Geist in the proof only. The SVG names the real fonts. Make the press PDF from
Illustrator with the licensed Roc Grotesk from Adobe Fonts installed.

### Sinhala and Tamil

They print as outlines, shaped exactly (HarfBuzz) from the Noto fonts above, so they render correctly on any machine
and in any RIP. Each line also has a **live twin** in the hidden layer `Sinhala_Tamil_live_text`, set in the same font
at the same size and position. To change the wording: show that layer, edit the text (Illustrator's World-Ready
Paragraph Composer must be on for correct Sinhala/Tamil shaping), check it against the outline, then delete the old
outline and keep the live text, or create outlines from it.

## Before press

- **Logo and Ceylon Tea lion are traced mock-ups.** Replace them with the masters (the logo is in `Type_and_Icons >
  Front` and on the lid; the lion on the front).
- **Colour:** the artwork is RGB at 305 ppi (12 px/mm). Convert to the printer's CMYK profile and proof the plum
  and amber, which can shift; the gold "Vanilla" is a gradient (#8A6424 → #E6C77E). If it is to be foil, make it a
  separate spot layer.
- **Barcode** (EAN-13 4796034220229) is drawn at 85%; confirm the number and have it verified.
- **Translations:** the Sinhala and Tamil should be checked by a native speaker.
- **Labelling questions still open** (see `research/label-text-rules.md`, "The Estate 12-bag carton"): the English
  name's type treatment, the "natural vanilla" and "own farms" claims, and the Tea Board's approval of the lion.
