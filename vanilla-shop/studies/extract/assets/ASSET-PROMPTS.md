# Extract labels: Nihonga paintings

Attach `nihonga-moodboard.jpg` and `board-2-layout.jpg`. The moodboard holds:
- 1–3: the Midjourney Nihonga references (plums, plum branch, apricots);
- 4: our vanilla painting made from them;
- 5: the Velvet candle, our tone-on-tone painting.

## Why the first try came out too realistic

The composition was right: the fan rising from the base, and empty cream above. The rendering was wrong:
wrinkled bark-like pods, leaf veins, a seed cavity and red-brown dried-leaf realism. In references 1–3 the forms are
simplified and smooth, almost flat volumes that glow from within, rendered in a stippled, granular grain with soft
edges and almost no surface detail. My prompt asked for "wrinkles" and "tiny black seeds", and detail like that pulls
the model towards realism. The new prompts follow the reference prompts' own wording ("japanese nihonga on gofun silk
paper", "soft organic silhouettes glowing", "--raw", and a `--no` list), and the split pods are gone.

## Reference prompts (the originals, for comparison)

```
extreme close-up of ripe plums, soft organic silhouettes glowing at the lower centre, smooth gradient from warm cream #FFE7C1 at the top, through golden ochre #E59E51, into dusty mauve-brown #957171, deepening to a deep plum violet core #4B2981 at the base, painterly nihonga texture, soft focus, fine grain, vast empty space around, quiet and elegant, mono-no-aware --ar 16:9 --stylize 50
```

```
extreme close-up of ripe apricots on a branch, japanese nihonga on gofun silk paper, soft glowing fruit, warm hazy summer light, gradient of golden apricot #E59E51, peach #FFC69C and pale cream #FFE7C1, delicate and luminous, painterly texture, soft focus, fine grain, vast empty space, serene and warm, mono-no-aware --no neon, harsh, busy, photo realistic, frame, text, watermark --ar 16:9 --raw --stylize 50
```

## No. 01 · With alcohol (vermilion)

```
extreme close-up of slender cured vanilla pods and long vanilla leaves rising from the lower centre, fanning out like a quiet ikebana arrangement, a single pale vanilla orchid flower among them, smooth simplified rounded forms, soft organic silhouettes glowing at the lower centre, smooth gradient from warm cream #FBF1DE at the top, through soft apricot #EBB08C, into vermilion #B83A24, deepening to an oxblood core #4A120C at the base, japanese nihonga on gofun silk paper, stippled granular mineral pigment, painterly nihonga texture, soft focus, fine grain, vast empty space above, quiet and elegant, mono-no-aware --no photo realistic, wrinkles, veins, seeds, harsh, busy, frame, text, watermark --ar 2:1 --raw --stylize 50
```

## No. 02 · Alcohol-free (honey)

```
extreme close-up of pale vanilla orchid flowers and closed buds on a vine rising from the lower centre, long smooth leaves fanning out like a quiet ikebana arrangement, two cured vanilla pods at the base, smooth simplified rounded forms, soft organic silhouettes glowing at the lower centre, smooth gradient from warm cream #FBF1DE at the top, through pale honey #F0CF8E, into golden ochre #D89A2E, deepening to a burnt amber core #5E3A0C at the base, japanese nihonga on gofun silk paper, stippled granular mineral pigment, painterly nihonga texture, soft focus, fine grain, vast empty space above, quiet and elegant, mono-no-aware --no photo realistic, wrinkles, veins, harsh, busy, frame, text, watermark --ar 2:1 --raw --stylize 50
```

## No. 03 · Syrup (green)

```
extreme close-up of bunches of long green vanilla pods hanging from an arching vine that rises from the lower centre, long smooth leaves fanning out like a quiet ikebana arrangement, one small drop of golden syrup at the tip of a pod, smooth simplified rounded forms, soft organic silhouettes glowing at the lower centre, smooth gradient from warm cream #F6F2DE at the top, through soft sage #C6D3A6, into leaf green #4F7448, deepening to a deep forest core #16301C at the base, japanese nihonga on gofun silk paper, stippled granular mineral pigment, painterly nihonga texture, soft focus, fine grain, vast empty space above, quiet and elegant, mono-no-aware --no photo realistic, wrinkles, veins, harsh, busy, frame, text, watermark --ar 2:1 --raw --stylize 50
```

## In GPT

GPT ignores the flags. Delete everything from `--no` onwards, ask for a wide landscape image, and add at the end:

> Match the technique of references 1 to 3 exactly: smooth, simplified forms that glow softly from within, rendered
> in a fine stippled granular grain, soft edges, almost no surface detail. Not photorealistic: no wrinkles, no leaf
> veins, no seeds, no bark texture. Follow the layout of the second attachment: empty cream across the upper half,
> the plant rising from the lower centre.

For No. 02 and No. 03, also attach the No. 01 result you keep, and start with: "A companion to the attached No. 01
painting: same composition, scale and technique; only the subject and colours change."

## Checks

- Smooth forms and grain like the plums, not textured realism.
- The upper half is empty cream.
- The colour deepens to the bottom edge.
- It reads as vanilla: a pale flower with a trumpet lip, and long slim pods.
- No text or watermark.
