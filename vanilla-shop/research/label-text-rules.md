# Label text: legibility rules for the tea packs

Notes gathered October 2026 for the Natural Vanilla Tea boxes and pouches. Not legal advice; confirm with the
Food Control Administration Unit (Ministry of Health) or a regulatory consultant before print.

## Sri Lanka: Food (Labelling and Advertising) Regulations 2026

Source read: the Ministry of Health's "Labelling Regulations Final – 11.02.2026" PDF
(eohfs.health.gov.lk/food/images/Labelling_Regulations_Final_-_11.02.2026.pdf). Regulation 1 says they come into
operation on 1 July 2026 and replace the 2005 regulations; check the gazetted text matches this draft.

| What | Where | Size (regulation) |
|---|---|---|
| Common name | Main panel, bold, all three languages (or two on the main panel, the third on any panel) | ≥ 3 mm and ≥ 1/3 of the brand or trade name's letter height (5(a)) |
| Net contents | Main panel, bold, `g` | Schedule II: ≥ 1.5 mm if the main panel ≤ 120 cm², ≥ 3 mm if larger (5(d)) |
| Ingredients | Any panel, any language, descending order by weight | ≥ 1.5 mm (5(e)) |
| Name and address of manufacturer, distributor, packer | Any panel | ≥ 1.5 mm (5(e)) |
| Batch number, date of manufacture (= packing date for tea, 4(5)) | Any panel | Dates bold, Schedule II height |
| Date of expiry | Any panel, two of the three languages | Bold, Schedule II height. Exemption only for tea in wholesale packs. |
| Storage and use instructions, if given | Any panel, at least two of the three languages | ≥ 1.5 mm (5(e)) |
| Nutrition panel | Not required for tea with only flavourings added (Schedule III, 1.2) | — |

"Letter size" is the height of capitals, or of lowercase letters without ascenders or descenders (x-height), so
lowercase text is measured by its x-height. All text must contrast with its background (5(c)).

Our panels: cube front 8.8 × 8.5 cm = 74 cm² (Schedule II: 1.5 mm); long-box front 17.6 × 8.5 cm = 150 cm² (3 mm).

## Other references used for good practice

- EU Regulation 1169/2011, Art. 13 and Annex IV: mandatory text x-height ≥ 1.2 mm (0.9 mm when the largest
  surface is under 80 cm²).
- Hong Kong Centre for Food Safety legibility guideline: ≥ 1.2 mm x-height recommended, dark single-colour text on a
  light single-colour background.
- EU Commission legibility work (Council WK 4187/2023): contrast and line spacing (≥ 120%) matter as much as size.
- Packaging legibility research (Bix et al., Journal of Design Communication 2002): contrast and letterform affect
  legibility more than point size alone.

## How the tea boxes apply this (tools/tea_box.mjs, `DECL`)

- Body text in Roc Grotesk Regular at 3.05 mm (x-height 0.494 → 1.51 mm); line spacing 4.2 mm (138%).
- Capital labels in Roc Grotesk Wide at 2.3 mm (cap height 0.658 → 1.51 mm).
- Sinhala (Noto Sans Sinhala) at 2.8 mm and Tamil (Noto Sans Tamil) at 2.75 mm, both ≈ 1.5 mm x-height.
- Text sits on the plain part of each panel, never over the painting; the grain layer runs under the type.

## What the packs carry

The legal and product text is copied from the pack on sale now (Vanilla_Tea_P.pdf, 25 bags): the bag
description, "Net Weight - 50g (2g x 25)", the batch block (B.N., MFD., EXP., MRP. Rs. in Sinhala, English and
Tamil), the barcode and the distributor block, word for word. That pack has no ingredients list or storage line,
so the new packs add none. The design sections (How to brew, "Vanilla was never plain", What's inside) stay; they
are not declarations.

The Ceylon Tea lion is on every tea pack, as on the current one: cube and long-box fronts (top right, 14 and
15 mm wide) and both pouch labels (top right, 12 mm). It is the Sri Lanka Tea Board's quality mark and needs the
packer's licence from the Board; check the licence covers these packs and any minimum size or colour rules.

## Open points

- The 12-bag cube uses the 25-bag wording with its own count and weight, and needs its own GTIN.
- Main panels still to check against 4(1) and 5(a), 5(d): the common name in bold and in two or three languages,
  and net contents in bold at the Schedule II height (3 mm on the long box).
