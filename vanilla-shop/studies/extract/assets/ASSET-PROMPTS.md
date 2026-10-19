# Extract labels: paintings, in the candle way

The last brief (a grey, centred vignette on white) asked for clip art, and that is what it produced. The candles
work because each one is a whole colour world: the plant is painted tone-on-tone in that colour, with one light
accent, nihonga texture on washi and a lot of quiet space. The extracts get the same treatment, with two changes
for a bottle:

- **The painting is the whole label.** Cream at the top, where the name sits, deepening to the product's colour
  at the base, and on into the dark extract below the label. Cream and one colour per product, as chosen, but
  painted rather than printed in a single ink.
- **The plant rises from the lower centre and fans out**, like a quiet ikebana arrangement, so the label is
  centred on the bottle. On the candles it entered from the side.

Each product carries its own part of the vanilla story, as each candle carries its own ingredient:

| | Colour world | Subject | Light accent |
|---|---|---|---|
| No. 01 With alcohol | Vermilion to oxblood | Cured pods, some split open: the classic, deepest extract | One pale vanilla flower |
| No. 02 Alcohol-free | Honey to burnt amber | The vine in flower: the gentle one | Cream flowers with golden throats |
| No. 03 Syrup | Sage to deep forest | Green pods hanging in bunches: the sweet fruit | One drop of golden syrup |

Attach `board-1-style.jpg` (the four candle paintings and the tea vine) and `board-2-layout.jpg` (the label
layout). Make No. 01 first. Once it is right, attach it as well when you make No. 02 and No. 03, so all three
share a scale and composition.

In GPT, leave out the `--ar` and `--stylize` flags and ask for a wide landscape image. I'll extend the sides
to the full 226 mm wrap myself.

## No. 01 · With alcohol

```
close-up of a tall spray of cured vanilla pods rising from the lower centre and fanning out like a quiet ikebana arrangement, long slender pods with soft wrinkles, two of them split open showing tiny black seeds, a few long vanilla leaves among them and a single pale waxy vanilla orchid flower near the centre, soft organic silhouettes glowing at the lower centre, smooth gradient from warm cream #FBF1DE at the top, through soft apricot #EBB08C, into vermilion #B83A24, deepening to an oxblood core #4A120C at the base, pods and leaves painted in vermilion and oxblood tones close to the ground around them, the pale cream orchid as the only light accent, soft flat Japanese nihonga painting, mineral pigments on washi paper, delicate gofun white highlights, gentle tonal washes, no glossy highlights, no 3D shading, softly painted edges, painterly nihonga texture, soft focus, fine grain, vast empty cream space across the upper half, quiet and elegant, mono-no-aware --ar 2:1 --stylize 50
```

## No. 02 · Alcohol-free

```
close-up of a flowering vanilla orchid vine rising from the lower centre and fanning out like a quiet ikebana arrangement, several pale waxy orchid flowers with trumpet-shaped lips and a few closed buds, long glossy leaves on smooth thin stems, two cured vanilla pods resting at the base, soft organic silhouettes glowing at the lower centre, smooth gradient from warm cream #FBF1DE at the top, through pale honey #F0CF8E, into golden ochre #D89A2E, deepening to a burnt amber core #5E3A0C at the base, leaves and stems painted in honey and ochre tones close to the ground around them, the cream flowers with golden throats as the only light accent, soft flat Japanese nihonga painting, mineral pigments on washi paper, delicate gofun white highlights, gentle tonal washes, no glossy highlights, no 3D shading, softly painted edges, painterly nihonga texture, soft focus, fine grain, vast empty cream space across the upper half, quiet and elegant, mono-no-aware --ar 2:1 --stylize 50
```

## No. 03 · Syrup

```
close-up of a vanilla vine rising from the lower centre and arching outward like a quiet ikebana arrangement, heavy bunches of long green vanilla pods hanging from it, long glossy leaves on smooth thin stems, one small pale orchid bud, a single drop of golden syrup forming at the tip of one pod, soft organic silhouettes glowing at the lower centre, smooth gradient from warm cream #F6F2DE at the top, through soft sage #C6D3A6, into leaf green #4F7448, deepening to a deep forest core #16301C at the base, pods and leaves painted in sage and forest tones close to the ground around them, the glowing golden syrup drop as the only warm accent, soft flat Japanese nihonga painting, mineral pigments on washi paper, delicate gofun white highlights, gentle tonal washes, no glossy highlights, no 3D shading, softly painted edges, painterly nihonga texture, soft focus, fine grain, vast empty cream space across the upper half, quiet and elegant, mono-no-aware --ar 2:1 --stylize 50
```

## For No. 02 and No. 03, start the prompt with

> Paint a companion to the attached No. 01 painting: the same composition, scale, framing and nihonga technique,
> with the plant rising from the same point. Only the subject and the colour world change, as follows:

## If it comes out 3D or glossy (as the first candles did)

> Keep this exact composition, colours and plant. Repaint it as a flat, soft Japanese nihonga painting: mineral
> pigment on washi paper, no glossy highlights, no 3D shading, no airbrushed gradients. Thin, smooth stems with no
> texture or knots. Edges softly painted, not crisp. Fine paper grain throughout.

## Checks

- Vanilla, not some other orchid: a pale flower with a trumpet-shaped lip, long slender pods, and leaves that are
  fleshy and alternate.
- The upper half is empty cream: no leaves, mist shapes or birds where the name goes.
- The colour deepens to the bottom edge. Nothing important is cut off at the bottom, because the label's base meets
  the bottle there.
- No text, signature or border.

After that I set the name on the cream sky in the product's dark colour, add the logo and the numbered neck strip,
extend the gradient round to the back panels, and mock all three up on the bottles. The edge bands from the last
round probably aren't needed, because the painting already brings the colour to the base. I'll show both ways.
