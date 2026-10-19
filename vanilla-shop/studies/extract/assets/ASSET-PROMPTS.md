# Extract labels: new painted assets (GPT image)

The chosen direction is cream paper with each product in one colour. The painting, the type, the two edge bands and
the numbered neck strip are all vermilion for No. 01, ochre for No. 02 and green for No. 03. The current painting was made in
full colour, and in one colour the flower sinks into the leaves (board 3). So the new art is painted in grey
first, then coloured with `tone.py`.

Attach the three boards to every prompt, in this order:

1. `board-1-style.jpg`: our painting style (the tea range).
2. `board-2-layout.jpg`: where each asset goes and its size.
3. `board-3-values.jpg`: why it has to be a grey value painting.

Generate one asset per chat turn. Ask for the highest quality. Use landscape 1536 × 1024 for assets 1 and 2 and portrait
1024 × 1536 for asset 3.

## Shared block (paste at the start of every prompt)

Paint in exactly the style of board 1: the same smooth, softly airbrushed botanical painting, gentle gradients,
crisp clean silhouettes, no outlines, no visible brush strokes, no paper texture. Slightly stylised but botanically
correct Vanilla planifolia:
- flowers with three narrow sepals and two petals, and a trumpet-shaped lip rolled round the central column with a
  softly frilled edge;
- thick, fleshy, oblong leaves with pointed tips, set alternately on a smooth, succulent stem;
- cured pods that are long, slim, wrinkled and slightly flattened, with a small curled hook at the tip.

But paint it in greyscale only, as a monochrome value painting (grisaille) in neutral greys, on a pure white
background (#FFFFFF). The art will be printed in one colour on cream paper (board 3), so the values do the work:
- flower petals and lip: the lightest, white to pale grey, with soft grey modelling so their shape reads against
  the white;
- leaves: mid grey (30–60%), lighter at the edges, darker towards the midrib;
- stems: mid grey;
- cured pods: the darkest, near black, with lighter highlights along the wrinkles.

Every element must separate from what is behind it by value, not by colour. No colour at all, no cast shadow, no
ground, no frame or border, no text, letters or numbers, and nothing touching the edges of the image.

## Asset 1: front vignette (landscape)

[Shared block]
A wide, low, centred arrangement for the front of a bottle label, about twice as wide as it is tall (board 2,
asset 1: 40 × 18 mm). One open vanilla flower faces the viewer at the exact centre. Behind and just below it, two
cured vanilla pods cross in a shallow X, their curled tips reaching out to the left and to the right. A pair of
leaves sweeps out on each side, the left and right pairs balanced but not mirrored, so it looks natural rather than
like clip art. One small closed bud on a short stem rises behind the flower, slightly to the right. The whole group
sits in the middle of the image with generous white space all round, about 80% of the width and 45% of the
height.

## Asset 2: back vignette, hand pollination (landscape)

[Shared block]
A close view of a vanilla flower being pollinated by hand, as it is done in Sri Lankan home gardens (board 2,
asset 2: 40 × 30 mm; the label's history line ends "every flower, open for a single day, is still pollinated by
hand"). The open flower is seen from a slight angle, so the trumpet-shaped lip and the column inside it are clear.
From the right, a hand's thumb and forefinger hold a thin, pointed bamboo sliver, its tip just inside the lip. The
hand is relaxed and natural, with only the thumb and two fingers in view, cropped softly at the wrist. A short
length of vine with one leaf and a green unripe pod finishes the left side. Centred, with white space all round.

If the hand comes out wrong after two tries, use this fallback instead: a small bundle of seven cured vanilla pods
tied round the middle with a thin cotton string and a simple knot, lying slightly diagonally, the pod tips curling
naturally.

## Asset 3: climbing-vine border (portrait)

[Shared block]
A single slim vanilla vine climbing straight up through the centre of the image, for a narrow border strip
(board 2, asset 3: 12 × 60 mm). The stem rises with a gentle zigzag. Small leaves alternate left and right, about
seven in all, smaller towards the top. There is one short aerial root at a node and a curled growing tip at the top.
No flowers and no pods. Keep the whole vine inside a narrow column in the middle third of the image, with white on
both sides. We use it as it is on one side and mirrored on the other.

## Afterwards

1. Check each image for:
   - five narrow tepals plus the lip on each flower;
   - pods that stay separate;
   - no extra flowers growing from leaves;
   - a hand with the right number of fingers, joined naturally;
   - pure white behind;
   - no text or signatures.
   Fix with "Change only the [part]: …" rather than regenerating.
2. Download the PNG and run `python3 -I tone.py asset-1.png asset-1`. This writes three versions,
   `asset-1_no01-with-alcohol.png`, `_no02-alcohol-free.png` and `_no03-syrup.png`, with transparent backgrounds,
   ready to drop on the cream label.
3. Send them back and I will place them on the labels, the wrap and the bottle mock-ups.
