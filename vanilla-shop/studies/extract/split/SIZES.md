# Label sizes and the numbers on the labels: how they were worked out

The sources are:
- the current label file (`vanilla_labeels__final-01.pdf`, 226 × 70 mm);
- the shop's own product pages, for ingredients, prices and gross weights;
- Glomark and Kapruka;
- the photo of the 500, 200 and 100 ml bottles.

Anything worked out here is marked in the proof: cyan where it was calculated or taken from a listing, magenta where
it is an estimate.

## 1. Bottle and label sizes

| | 500 ml | 200 ml | 100 ml |
|---|---|---|---|
| Diameter | **72 mm** (226 ÷ π) | **53 mm** | **42 mm** |
| Wrap length (π × D) | **226 mm** | **166 mm** | **132 mm** |
| Label height | **70 mm** | **42 mm** | **35 mm** |
| Status | the original template | estimate | estimate, least certain |

How:

1. **Diameter of the 500 ml.** The template wraps the bottle exactly once: 226 mm = π × 72 mm.
2. **Diameters of the smaller bottles.** They are the same flask shape, so volume grows with the diameter cubed:
   - 200 ml: 72 × (200/500)^⅓ = 72 × 0.737 = **53 mm**.
   - 100 ml: 72 × (100/500)^⅓ = 72 × 0.585 = **42 mm**.
   - The photo agrees within perspective. The body widths are 287, 203 and 162 px, ratios 0.71 and 0.56, which gives
     51 and 41 mm.
3. **Label heights.** Each label's height was measured against its bottle's width in the photo:
   - 500 ml: 280/287 = 0.976. The template gives 70/72 = 0.972, so the method works.
   - 200 ml: 163/203 = 0.80 × 53 = **42 mm**.
   - 100 ml: 133/162 = 0.82 × 42 = **35 mm**.
4. **Cross-check from weight.** These are the shop's gross weights, with the No. 01 liquid at about 0.957 g/ml (35% vol):

   | | 500 ml | 200 ml | 100 ml |
   |---|---|---|---|
   | Gross weight | 1,074 g | 507 g | 229 g |
   | Liquid | 479 g | 191 g | 96 g |
   | Glass and cap | 596 g | 316 g | 133 g |

   - If the bottles are the same shape, glass weight goes with surface area (V^⅔). That predicts 323 g for the 200 ml,
     against 316 g actual, which fits.
   - It predicts 204 g for the 100 ml, against 133 g actual. The 100 ml bottle is thinner or a different shape, so its
     size is the least certain.

**Before print:** measure each bottle with a tape round the label area, and measure the flat label band height. Wrap
length = circumference, minus 1–2 mm if the printer wants a gap at the seam.

## 2. Energy and nutrition

The current label's figures come from the USDA entry for vanilla extract, per teaspoon: 0.5 g carbohydrate,
0.5 g sugars, 1 mg sodium. Its calories line is blank.

- **No. 01, 12 kcal per teaspoon.**
  - Carbohydrate: 0.5 g × 4 = 2 kcal.
  - Alcohol: 5 ml × 35% = 1.75 ml × 0.789 g/ml = 1.38 g, × 7 = 9.7 kcal.
  - Total: 12 kcal, the same as the USDA figure. Depends on the alcohol strength.
- **No. 02, about 6 kcal per teaspoon.**
  - The bottles' weights give the liquid's density. Glass and cap are taken from No. 01, so this assumes the same
    bottle:
    - 100 ml: 238 − 133 = 105 g, so 1.05 g/ml.
    - 200 ml: 526 − 316 = 210 g, so 1.05 g/ml.
  - A glycerine–water mix at 1.05 g/ml is about **20% glycerine** by weight.
  - So a teaspoon (5.25 g) holds about 1 g glycerine, which is 4.5 kcal. Add 2 kcal from the extract: about 6 kcal.
  - Total carbohydrate is then 1.5 g, of which about 1 g is glycerine. Production should confirm the recipe.
- **No. 03, per 2 teaspoons (10 ml), an estimate.**
  - Assumes a typical café syrup of 60% sugar by weight, at 1.29 g/ml.
  - 10 ml = 12.9 g, holding 7.7 g sugar: **8 g carbohydrate, 8 g sugars, 31 kcal, 3% DV**.
  - A 1:1 simple syrup would be 6 g and 25 kcal instead.
  - Needs the real recipe.
- **Servings per bottle:**
  - extract: 100 teaspoons in 500 ml, 40 in 200 ml, 20 in 100 ml;
  - syrup: 50 servings of 10 ml in 500 ml.

## 3. Optional: pods in a bottle

The US standard for vanilla extract is 13.35 oz of beans per gallon, about 100 g of beans per litre.

| | 500 ml | 200 ml | 100 ml |
|---|---|---|---|
| Beans | 50 g | 20 g | 10 g |
| Cured pods, at 3–5 g each | 10–17 | about 5 | 2–3 |

If production confirms its own ratio, this could become a line on the label, such as "About a dozen cured Ceylon pods
in every bottle". It is not on the labels yet.

## 4. Prices (MRP)

| | 100 ml | 200 ml | 500 ml |
|---|---|---|---|
| No. 01 with alcohol | 4,100 | 8,000 | 20,100 |
| No. 02 alcohol-free | 3,500 | 6,900 | 17,000 |
| No. 03 syrup | – | – | 12,500 |

The prices come from the shop's own product pages. Glomark matches for 100 ml. The syrup is only sold in 500 ml, so it
has no small labels.

## 5. What changes on the 200 and 100 ml labels

Scaling the 500 ml label down would shrink the back to unreadable type, so the parts are re-set:

- **Colour art** is scaled to the label height and set against the bottle's centre, as on the 500 ml.
- **Front card** scales with the label. The volume keeps a legal size, with numerals at least 3 mm high (4 mm on the
  500 ml), as most net-quantity rules ask (OIML R79). Check the Sri Lankan rule (Measurement Units, Standards and
  Services Dept.).
- **Story:**
  - 200 ml: a two-sentence version;
  - 100 ml: one sentence;
  - the species/origin row is dropped on both (origin stays in the address).
- **Nutrition:**
  - 200 ml: a compact table;
  - 100 ml: a single running line, the usual small-pack format.
- **Barcode:**
  - 500 ml: 0.25 mm module (95%).
  - 200 ml: 0.22 mm module (83%). On a 53 mm bottle the code covers about 53° of the curve, which is still fine.
  - 100 ml: turned to run up the bottle (ladder orientation). Lying flat on a 42 mm bottle it would cover 67° of the
    curve and read badly.
  - The printer should verify all three with a barcode verifier.
- **Maker block:**
  - 100 ml: name, full address, website and one phone number;
  - the other sizes carry the full block.
- **Smallest type:** 1.15 mm on the 100 ml (maker block and nutrition). Section 2 of `TO-CONFIRM.md` asks for a check
  of the legal minimum.
