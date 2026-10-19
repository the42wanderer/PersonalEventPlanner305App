# Direction: Bloom

Kept for future work: soaps, social media, and anything that needs a quiet but striking Vanilla Shop look. It was first
drawn for the extract labels; the extracts went with the Split direction instead.

## The idea

One vanilla flower, very large and soft-focus, filling the surface and running off its edges. The name sits over it
as a lockup. It comes from the Bloom coffee label and Nami Flow on the bottle board, and it has the same glow and
grain as the Nihonga plum references behind the tea paintings.

## Rules

- **One flower and nothing else.** No leaves, no props, no second motif. Its scale does the work: crop it hard.
- **Glow, not outline.** A light core fading to a saturated edge, softly blurred, with fine grain over everything.
  No crisp line drawing on top.
- **Cream ground** (#F7EFDC) and one colour world per product, the same three as the extracts:

  | | Edge | Core | Throat |
  |---|---|---|---|
  | Vermilion | #B8301C | #F5B08A | #E59A3A |
  | Honey | #C98418 | #F8D79A | #D9822A |
  | Green | #3E6B3A | #CFE0A8 | #C9A33A |

  New products (a soap, say) get a new colour world, built the same way: a deep edge, a pale core and a warm throat.
- **Type:** the main word in Instrument Serif Italic, large, across the flower in the product's darkest tone. A
  second word in Roc Grotesk Wide capitals, spaced to sit under it. Small capitals for everything else. The logo
  stays small.

## Files

- `bloom-three-colourways.jpg`: the three extract fronts that started it.
- `bloom-social-post-example.jpg`: a 4:5 post ("Savor the calm.").
- `bloom-art-01/02/03.png`: the flower art on cream, 120 × 70 mm at 20 px/mm.
- `orchid.py`, `bloom.py`: the generator. `bloom.bloom(name, W, H, cx, cy, R, edge, core, throat, ground, blur)` draws
  the flower centred at (cx, cy) with radius R, in mm. Use it for any size or colour.
