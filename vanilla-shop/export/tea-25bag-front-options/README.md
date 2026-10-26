# 25-bag front: typography studies

The 25-bag carton's front only; every other panel, the logo and the box are as in `export/tea-25bag-final-plum`.

- `1-…`, `2-…`: Current, A, B with the curve held fixed (B's title could only reach 15.4 mm).
- `3-…`, `4-…`: Current, A, and **B rebuilt**: "Vanilla Tea" on one line at 57.5% of the front's width (24.4 mm),
  the Sinhala name and the description under it on the same 6% left edge, the lion and quantity (Roc Grotesk Wide
  Regular, 2.8 mm) at the lower right on a 6% margin. The curve keeps its form and is re-solved for this type:
  `Y0 = 0.40, A = 0.18, k = 4, m = 165 mm` (A2, k2 unchanged): level and high over the title, sweeping down to the
  right onto the lion; the sprig, peak and glow moved with the dip to under the logo, as on the cube; the near tea
  rows held below 29.5 mm so the distant hills still show over the title.

Rebuild B rebuilt (scratch paths as in `studies/tea/bandsystem`):

    VM_Y0=0.40 VM_A=0.18 VM_K=4 VM_MU=165 BOX=long CM=165 NEAR_TOP=29.5 ART_SUFFIX=-B2 SIDE_PLUM=1 PALETTES=plum python3 wrap.py
    FRONT_ALT=B TITLE_FRAC=0.575 TITLE_GAP=4.0 TEA_THEME=estateplumside node tools/tea_box.mjs long

Not yet compliant: on this front (150 cm²) the net contents must be bold and at least 3 mm high (5(d)); the light
2.8 mm "NET WT. 50 g" in A and B does not meet that. See `research/label-text-rules.md`.
