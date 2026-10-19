# Turns a grey value painting (on white) into the three one-colour versions for the extract labels.
# Usage: python3 -I tone.py painting.png [out_prefix]
# White becomes transparent; values map dark -> product colour -> label cream, so the art sits on the cream paper.
import sys
import numpy as np
from PIL import Image

INKS = {  # dark, mid, paper
    'no01-with-alcohol': ('#5A1A10', '#B4432C', '#F6EEDA'),
    'no02-alcohol-free': ('#5E3A0C', '#B07818', '#F6EEDA'),
    'no03-syrup':        ('#16301C', '#4F7448', '#F6EEDA'),
}

def hx(c): return np.array([int(c[i:i + 2], 16) for i in (1, 3, 5)], np.float32) / 255

def tone(src, dark, mid, paper, white=0.97):
    im = Image.open(src).convert('RGBA'); a = np.asarray(im).astype(np.float32) / 255
    L = a[..., :3] @ np.array([0.299, 0.587, 0.114], np.float32)
    L = L * a[..., 3] + (1 - a[..., 3])                     # transparent counts as white
    t = np.clip(L / white, 0, 1)
    d, m, p = hx(dark), hx(mid), hx(paper)
    rgb = np.where((t < 0.55)[..., None], d + (m - d) * (t / 0.55)[..., None], m + (p - m) * ((t - 0.55) / 0.45)[..., None])
    alpha = np.clip((white + 0.02 - L) / 0.08, 0, 1)        # only the paper-white background drops out
    return Image.fromarray((np.dstack([rgb, alpha]) * 255).clip(0, 255).astype(np.uint8), 'RGBA')

if __name__ == '__main__':
    src = sys.argv[1]; pre = sys.argv[2] if len(sys.argv) > 2 else src.rsplit('.', 1)[0]
    for name, (d, m, p) in INKS.items():
        out = tone(src, d, m, p); out.crop(out.getbbox()).save(f'{pre}_{name}.png'); print(f'{pre}_{name}.png')
