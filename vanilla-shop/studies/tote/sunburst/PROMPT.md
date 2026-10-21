# Tote stamp on GPT Image 2.5 Sunburst

Follows OpenAI's GPT Image 2.5 prompting guide:
- labelled sections in the order scene, subject, details, constraints;
- a numbered role for each reference image;
- "change only X" plus a list of what must be preserved;
- one change per edit.

## Settings

| Parameter | Value | Why |
|---|---|---|
| model | `gpt-image-2.5-sunburst` | the quality model; best at editing and keeping subjects intact |
| size | `1712x2144` | 4:5, the largest size below the experimental range (multiples of 16) |
| quality | `high`, then try `xhigh` | the guide says to raise quality only if a result falls short |
| background | `opaque` | |
| output_format | `png` | lossless, for tracing |
| n | `4` | pick the best of four |

Optional, after a pick: one try at `2560x3200` (4:5, experimental above 2560×1440) for more detail to trace.

## Inputs, in this order

1. `input-1-composition.png`: the approved stamp. It sets the composition, the people and the frame.
2. `input-2-pods.jpg`: our real vanilla pods (Agro Ventures).
3. `input-3-flowers.jpg`: a real vanilla flower, from the side (left) and the front (right).

## Prompt 1: the one-ink stamp

```
Redraw image 1 as a single-colour engraved postage stamp for a screen-printed tote bag, keeping its composition and people, and correct the vanilla plant using images 2 and 3.

Roles of the inputs:
- Image 1: composition, people, poses, frame and layout. This is the design to keep.
- Image 2: the exact shape of the vanilla pods.
- Image 3: the exact shape of the vanilla flowers (side view on the left, front view on the right).

Medium:
A 1930s Ceylon recess-engraved postage stamp printed in ONE ink: deep black (#1A1714) on warm off-white paper (#F1E9D6). Every tone is built only from engraved lines and solid black: parallel lines, cross-hatching and flicks that follow each form, denser for shadow, open for light. No grey wash, no colour, no gradients, no halftone dots, no airbrushing. The engraving is bold enough to screen-print at 27 cm wide: no hairlines, no tiny specks, gaps between lines as wide as the lines. Light areas stay as bare paper. Slightly uneven, inked line quality, like a real print, not a digital filter.

Keep exactly from image 1:
- The composition and framing: the thatched house on the left, the coconut palms, the hills, the morning sun with engraved rays, the large vanilla vine on its support tree down the right.
- The woman: her face, pose, both raised arms, her hands holding the thin pollinating stick to a flower, her white jacket, bun, wrapped cloth, standing on the ground.
- The man: his face, upward gaze, pose, both hands holding the woven basket, the cloth over his shoulder, his sarong.
- The frame and layout: the perforated edge, the ornamented frame with flower corners, the empty top banner, the empty square tablet bottom left, the empty caption box along the bottom. In one ink, the frame is solid black with its ornaments cut out in paper; the banner, tablet and caption box stay plain paper and completely empty.

Change:
- Pods: every pod becomes a real vanilla pod like image 2: long and very slim, about 25 times longer than it is wide, round, smooth, gently curved, each on its own short stalk. Eight to ten per bunch, hanging loosely with gaps between them. No stripes, no bulges, no drops at the tips. The pods in the man's basket match: slim, laid lengthways.
- Flowers: every flower becomes a real vanilla orchid like image 3: five narrow, pointed, pale tepals spread like a loose star, round a pale lip rolled into a tube with a frilled mouth. Each flower is smaller than one leaf. Add two or three small clusters of round buds beside them.
- Remove the small stray figure-like mark at the bottom of the man's cloth.

Constraints:
- One ink and paper only, as above.
- No ladder, no extra people, no extra hands or fingers: each visible hand has four fingers and a thumb.
- No text, letters or numbers anywhere: every banner, tablet and box stays empty (the lettering is added later in vector).
- No watermark, no signature, no added logo.
```

## Edits after picking a result (same settings, the chosen image as input 1)

One change per edit, with the preserve list repeated each time. If an edit changes anything you didn't ask for,
throw it away and redo it from the previous image.

**Fixing pods only:**
```
Change only the vanilla pods. Make each one long, very slim and round, like image 2, eight to ten per bunch, hanging loosely. Keep everything else exactly the same: the people, their faces and hands, the leaves, the flowers, the frame, the one-ink engraved style, the paper colour and the empty banners.
```

**Fixing flowers only:**
```
Change only the flowers. Make each one a real vanilla orchid like image 3: five narrow pointed pale tepals round a pale rolled tube lip with a frilled mouth, smaller than a leaf. Keep everything else exactly the same: the people, the pods, the leaves, the frame, the one-ink engraved style, the paper and the empty banners.
```

**Making it bolder for print:**
```
Change only the line weight: make the engraved lines bolder and slightly more widely spaced across the whole image, merging the finest hatching into solid black where needed, so it screen-prints cleanly at 27 cm wide. Keep the drawing, composition, people and frame exactly the same.
```

## Prompt 2: no references (fallback)

```
Create a single-colour engraved postage stamp for a screen-printed tote bag, portrait 4:5.

Scene: a small vanilla garden beside a village house with a deep thatched roof in Sri Lanka, early morning. Coconut palms and low green hills behind, the rising sun drawn as engraved rays in the upper left.

Subject: a village woman in a white short-sleeved jacket and an ankle-length wrapped cloth, hair in a low bun, stands on the ground and reaches up with both hands to a vanilla flower, touching it with a thin wooden stick to pollinate it. Beside her and a step behind, a man in a white sarong with a cloth over one shoulder holds a woven basket of freshly picked green vanilla pods in both hands and looks up at her work. Full bodies visible, feet on the ground, natural proportions, four fingers and a thumb on every visible hand.

The vanilla vine: a thick, smooth vine climbs a support tree down the right third, with thick fleshy oval leaves placed alternately. Vanilla flowers: pale orchids with five narrow pointed tepals spread like a loose star round a pale lip rolled into a tube with a frilled mouth, each smaller than a leaf, with small clusters of round buds. Vanilla pods: long, very slim, round, smooth and gently curved, about 25 times longer than wide, eight to ten per bunch, hanging loosely from short stalks.

Frame: a perforated stamp edge; a solid black frame with small flower ornaments in the corners cut out in paper; an empty plain banner across the top; an empty square tablet at bottom left; an empty plain caption box along the bottom.

Medium: a 1930s Ceylon recess-engraved stamp printed in one ink, deep black (#1A1714) on warm off-white paper (#F1E9D6). Every tone built from engraved lines, cross-hatching and solid black that follow each form; light areas are bare paper. Bold enough to screen-print at 27 cm wide: no hairlines, no specks. Slightly uneven inked line quality, like a real print.

Constraints: one ink only, no grey, no colour, no gradients, no halftone dots; no ladder; no text, letters or numbers anywhere (all banners and boxes empty); no watermark, signature or logo.
```

## Checking a result

- **Ink:** zoom in. Only black and paper; no grey or soft shading.
- **Hands:** count the fingers on every hand.
- **Plant:** the pods are slim with gaps between them, and the flowers have a tube lip and are smaller than a leaf.
- **Kept from image 1:** both faces, both poses and the frame layout.
- **Empty areas:** all three are blank, with no stray letters.

Then send it to me. I'll clean it to a pure black film, set CEYLON / ලංකා / இலங்கை, 25c and THE VANILLA SHOP ·
NEGOMBO in the empty areas, and make the mock-up.
