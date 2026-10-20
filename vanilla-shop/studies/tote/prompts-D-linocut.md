# Tote stamp, one ink: the linocut prompts

Attach `linocut-references.jpg` (numbered 1 to 12) every time.
- **1 to 6, style:** real carved prints.
- **7 to 12, subject:** real vanilla, our pods and the garden.

## Why this should work where the last one didn't

The last result looked AI-made because it was a smooth, realistic painting with an engraving texture laid on top:
- soft gradients;
- airbrushed skin;
- even detail everywhere.

That polish is the giveaway. These prompts commit to a technique that cannot be smooth:
- a **hand-carved linocut printed in one black ink**, so every tone is a cut mark;
- big simple shapes and strong blacks;
- no people's faces or hands in view.

## How it's split

The image generator only makes the pictures. I build the stamp around them in vector:
- the perforated edge;
- the solid black frame;
- CEYLON, ලංකා, இலங்கை and 25c;
- VANILLA PLANIFOLIA;
- THE VANILLA SHOP · NEGOMBO.

So nobody asks the generator for lettering or layout, which it does badly.

1. **Prompt 1, the scene:** the picture inside the stamp's window.
2. **Prompt 2, the vine:** the vanilla vine on its own, to lay over the right of the stamp and break out past its edge.

   Generate it in the same conversation as the scene you pick, or attach that scene, so the carving matches.

## Prompt 1: the scene (portrait 4:5)

> Make a hand-carved linocut print, printed by hand in a single black ink on off-white paper, using the attached
> board: match the carving of references 1 to 6 and the subject of references 7 to 12.
>
> **Technique.** Pure black ink and bare paper only: no grey, no gradients, no halftone dots, no soft shading.
> - Every tone is carved:
>   - in dark areas, white gouge marks are cut out of solid black;
>   - in light areas, black lines are left standing on white paper.
> - The cuts are confident and slightly irregular, and they follow each form, like references 2 and 6:
>   - long level sweeps across the sky;
>   - short stacked nicks on the hills;
>   - vertical gouges down the tree trunks;
>   - curved cuts along each leaf.
> - Simplify like a printmaker: large shapes first, few details, and no mark thinner than a matchstick at poster size.
> - The print shows how it was made: slightly uneven ink at the edges of the blacks, tiny flecks of paper showing
>   through the solid areas, a faint grain from the block.
> - About 45% of the picture is solid black.
>
> **Scene.** Early morning in a small vanilla garden in the hills of central Sri Lanka.
> - **The garden.** Rows of slim support trees, lopped at head height (reference 11), run away from us in
>   perspective towards the left. Each has a fan of thin, feathery shoots at the top.
> - **The vines.** A vanilla vine with thick, fleshy oval leaves climbs every trunk, loops over the top and hangs
>   back down (reference 10). A few long, slim pod bunches hang from the nearer vines.
> - **The ground.** Bare earth between the rows, with a narrow footpath running straight away from us into the
>   garden.
> - **The woman.** On the path, small and about a third of the way up the picture, a village woman walks away from
>   us, seen from behind. She carries a flat woven basket on her head and her arms hang at her sides. She wears an
>   ankle-length wrapped cloth and a white short-sleeved jacket, with her hair in a low bun (reference 12). Her
>   face is not visible.
> - **Behind.** Two ranges of low, rounded hills, then a big pale sky carved in long level cuts with three or four
>   flat clouds.
> - **The light.** The rising sun is out of the picture on the right, so the trunks and rows throw long shadows
>   towards the left across the ground.
>
> **Composition.** The path and the rows lead the eye to the woman and the hills.
> - Keep the right third of the picture dark and quiet: dense black foliage with a few carved leaves. A separate
>   vine will be laid over it.
> - The foreground at the bottom is dark earth, so the picture sits firmly on its base.
>
> **Leave out:**
> - no frame, border, stamp, perforations or margin: the picture fills the canvas edge to edge;
> - no text, letters or numbers;
> - no colour;
> - no realistic or photographic rendering, no digital-painting or airbrushed look, no smooth vector clip art, no
>   fine pen hatching, no glowing light, no sun disc;
> - no faces or hands in view.

## Prompt 2: the vine (portrait 2:3, same conversation, or attach the chosen scene)

> Using the same carving as the attached scene and references 1 to 6, make a hand-carved linocut of a single
> vanilla vine, printed in one black ink on plain off-white paper. Nothing else on the paper: no background, no
> ground, no frame, no text. The vine stands alone in the middle with clear paper all round, for cutting out.
>
> **The vine.**
> - **Stem:** a thick, smooth, fleshy stem enters from the bottom edge and climbs to the top edge in one long,
>   gentle S-curve. Short aerial roots hang from two of its joints.
> - **Leaves:** five large leaves, placed alternately: thick, oval, pointed, and slightly twisted, so that one shows
>   its darker underside.
> - **The bunch:** about two-fifths of the way up, a bunch of nine to eleven long, slim vanilla pods hangs from one
>   joint, exactly like reference 9:
>   - each pod is pencil-thin, round and gently curved, on its own short stalk;
>   - the pods hang close together and overlap, some a little longer than others;
>   - they reach down almost to the bottom edge.
> - **Flowers:** two vanilla flowers, exactly like references 7 and 8, each a little smaller than a leaf:
>   - one near the top seen from the side, showing the lip rolled into a trumpet with a frilled mouth;
>   - one lower down seen from the front, with its three narrow sepals and two petals spread like a loose star
>     round the trumpet.
>   - Beside the top flower, a small cluster of round green buds.
>
> **Carving.**
> - Carve each form in the same way as the scene:
>   - the pods dark, with one bright carved highlight down each;
>   - the leaves half black, half lit, with cuts running along their length;
>   - the flowers mostly bare paper, outlined in black, with a few cuts at their bases;
>   - the trumpet's throat solid black.
> - Pure black and paper only, slightly uneven ink, tiny flecks of paper in the blacks.
>
> **Leave out:** no daffodils, lilies or frangipani, no fat or banana-like pods, no colour, no grey, no smooth
> vector look, no outline halo.

## Midjourney versions

Use reference images 1 to 6 as the style reference (`--sref`) and 7 to 12 as image prompts.

> hand-carved linocut print, single black ink on off-white paper, a small vanilla garden in the hills of Sri
> Lanka at dawn, rows of lopped support trees with vanilla vines looped over them receding to the left, a
> footpath leading away, a village woman seen from behind carrying a flat basket on her head, low rounded hills,
> sky in long level gouge cuts, bold carved gouge marks following every form, white cuts out of solid black,
> slightly uneven hand-burnished ink, paper flecks in the blacks, the right third dark dense foliage --ar 4:5
> --style raw --stylize 75 --no color, grey, gradient, halftone, photorealistic, digital painting, airbrush,
> vector, frame, border, text, face

> hand-carved linocut print, single black ink, one vanilla vine alone on plain off-white paper, thick fleshy
> stem climbing in an S-curve, five fleshy oval leaves, a hanging bunch of ten long pencil-thin vanilla pods,
> two vanilla orchid flowers with a trumpet-shaped frilled lip, a cluster of round buds, bold carved gouge
> marks, white cuts out of black, uneven hand-burnished ink --ar 2:3 --style raw --stylize 75 --no color, grey,
> gradient, daffodil, lily, banana, background, frame, text

## Picking a result

Generate four or more of each. Keep one only if it passes all of these:
1. **Black and paper only:** no greys or soft fades. Zoom in on the sky and the shadows.
2. **It looks carved:** you can see individual gouge marks, and they follow the forms.
3. **The woman** is seen from behind, simple, standing on the path; no face, and no hands that matter.
4. **The plant** (in the vine piece): every flower has a trumpet lip; the pods are slim; nothing like a daffodil
   or a banana.
5. **Nothing too fine:** no hairlines that would disappear when screen-printed at 27 cm.
6. **No lettering, frame or border.**

Small faults are fine: I can fix a stray mark, a fused shape or a missing highlight in vector.

## What I do with them

1. **Trace:** make both pictures pure 1-bit at print resolution, removing specks below 0.4 mm and opening up
   joins that would fill in.
2. **Assemble:** set the scene into the window of the vector stamp and lay the vine over the right side, breaking
   past the edge.
3. **Type:** CEYLON with ලංකා and இலங்கை, 25c, VANILLA PLANIFOLIA, and THE VANILLA SHOP · NEGOMBO, cut into the
   black frame. A native speaker checks the Sinhala and Tamil.
4. **Print files:** one film, black ink; plus a mock-up on canvas.
