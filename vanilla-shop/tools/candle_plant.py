"""Cut the plant out of each candle painting: pixels close to the flat ground colour become transparent.
Used for the weave, where the plant is drawn again over the scent name.
Usage: python3 tools/candle_plant.py  ->  plates/generated/v9-candle-<scent>-plant.png"""
import numpy as np
from PIL import Image, ImageFilter
ART = {'aura': 'v9-candle-aura-boswellia.jpg', 'zest': 'v9-candle-zest-tea.jpg',
       'velvet': 'v9-candle-velvet-rose.jpg', 'harmony': 'v9-candle-harmony-almond.jpg'}
for key, f in ART.items():
    im = np.asarray(Image.open('plates/generated/' + f).convert('RGB')).astype(float)
    ground = np.median(im[50:500, 50:400].reshape(-1, 3), 0)          # the empty upper left is pure ground
    d = np.sqrt(((im - ground) ** 2).sum(2))
    a = Image.fromarray((np.clip((d - 20) / 30, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
    Image.fromarray(np.dstack([im, np.asarray(a)]).astype(np.uint8), 'RGBA').save(f'plates/generated/v9-candle-{key}-plant.png', optimize=True)
    print(key, ground.astype(int))
