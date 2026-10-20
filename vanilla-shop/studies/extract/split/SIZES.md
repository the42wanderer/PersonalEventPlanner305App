# Label sizes for 200 and 100 ml

The label content comes from the labels now on sale (`vanilla_labeels__final-01.pdf`). The only figures from
elsewhere are:
- the 200 and 100 ml label sizes, worked out below;
- the 200 and 100 ml prices, from the shop's product pages and Glomark, since there was no old label for those sizes.

## 1. Bottle and label sizes

| | 500 ml | 200 ml | 100 ml |
|---|---|---|---|
| Diameter | **72 mm** (226 ÷ π) | **53 mm** | **42 mm** |
| Wrap length (π × D) | **226 mm** | **166 mm** | **132 mm** |
| Label height | **70 mm** | **42 mm** | **35 mm** |
| Status | the template | estimate | estimate, least certain |

How:

1. **Diameter of the 500 ml.** The template wraps the bottle exactly once: 226 mm = π × 72 mm.
2. **Diameters of the smaller bottles.** They are the same flask shape, so volume grows with the diameter cubed:
   - 200 ml: 72 × (200/500)^⅓ = **53 mm**;
   - 100 ml: 72 × (100/500)^⅓ = **42 mm**.
   - The photo of the three bottles agrees within perspective (body widths 287, 203 and 162 px).
3. **Label heights.** Each label's height was measured against its bottle's width in the photo:
   - 500 ml: 0.976. The template gives 70/72 = 0.972, so the method works.
   - 200 ml: 0.80 × 53 = **42 mm**.
   - 100 ml: 0.82 × 42 = **35 mm**.
4. **Cross-check from the shop's gross weights.**
   - The 200 ml glass weighs what a same-shape bottle should.
   - The 100 ml glass is lighter than expected, so that bottle may be a different shape.

**Check the 500 ml template size too.** In `vanilla_labeels__final-01.pdf` the label boxes measure **274 × 84 mm**,
and "8.5 cm" is written beside them. The design was made at 226 × 70 mm, which has the same proportions, so it scales
up without any change of layout. If the real label is 274 × 85 mm:
- the 500 ml bottle is 87 mm across;
- the 200 and 100 ml estimates scale up the same way: about **202 × 51 mm** and **160 × 42 mm**.

**Before print:** measure each bottle with a tape round the label area, and measure the flat label band height.

## 2. Prices (MRP)

| | 100 ml | 200 ml | 500 ml |
|---|---|---|---|
| No. 01 with alcohol | 4,100 | 8,000 | **20,000** |
| No. 02 alcohol-free | 3,500 | 6,900 | **17,000** |
| No. 03 syrup | – | – | **12,500** |

- **Bold:** printed on the current labels.
- **The rest:** from the shop's product pages, with Glomark matching for 100 ml.
- The website now lists the 500 ml No. 01 at 20,100. The labels keep 20,000, as printed.
- The syrup is only sold in 500 ml.

## 3. What changes on the 200 and 100 ml labels

Scaling the 500 ml label down would shrink the back to unreadable type, so the parts are re-set:

- **Colour art** is scaled to the label height and set against the bottle's centre, as on the 500 ml.
- **Front card** scales with the label. The volume stays large enough to read, with numerals 3 mm high (4 mm on the
  500 ml).
- **Story:** a two-sentence version of the 500 ml story.
- **Nutrition:**
  - 200 ml: the same table as the 500 ml, smaller;
  - 100 ml: the same figures set as one running line.
- **Barcode:**
  - 500 ml: 0.25 mm module.
  - 200 ml: 0.22 mm module.
  - 100 ml: turned to run up the bottle. Lying flat on a 42 mm bottle it would curve too far round to scan well.
  - The printer should verify all three.
- **Maker block:**
  - 100 ml: name, full address, website and one phone number;
  - the other sizes carry the full block.
- **The three marks** (USDA Organic, SGS, EU organic) are on every size: 5.6 mm high on the 500 ml, 4.2 mm on the
  200 ml, 3.3 mm on the 100 ml.
