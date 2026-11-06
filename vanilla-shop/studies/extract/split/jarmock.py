# A clear 100 g jar seen from the front, holding its contents, with the wrap label round it: the label is mapped onto
# the cylinder (the front card facing), so the label's colour can be judged against what the jar holds.
#   jar(label_png, contents) -> PIL image;  contents: 'paste' | 'powder'
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
PX = 8                                            # px per mm
D, HB, LID = 64.0, 78.0, 13.0                     # jar diameter, body height, lid height (mm)
LABEL_W, LABEL_H, FRONT = 200.0, 42.0, 122.0      # wrap size; the front card's centre on the wrap
def contents(kind, w, h, rng):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32); x = (xx / w) * 2 - 1
    if kind == 'paste':
        base = np.array([38, 20, 10], np.float32); amber = np.array([150, 82, 30], np.float32)
        t = np.clip(np.abs(x) ** 6, 0, 1)[..., None] * 0.55 + (1 - yy / h)[..., None] * 0.08    # light through the thin edge
        img = base * (1 - t) + amber * t
        n = rng.random((h, w)) < 0.012; img[n] = img[n] * 0.35                                   # seeds
    else:
        img = np.ones((h, w, 3), np.float32) * np.array([92, 70, 52], np.float32)
        img += rng.normal(0, 7, (h, w, 1)); img *= (0.88 + 0.12 * (1 - np.abs(x) ** 2))[..., None]
    return img
def jar(label_png, kind, seed=3):
    rng = np.random.default_rng(seed); W = int(D * PX); H = int((HB + LID) * PX); R = D / 2
    lab = np.asarray(Image.open(label_png).convert('RGB')).astype(np.float32); lk = lab.shape[1] / LABEL_W
    img = np.zeros((H, W, 3), np.float32); body_top = int(LID * PX)
    c = contents(kind, W, H - body_top - int(6 * PX), rng)
    img[body_top + int(6 * PX):, :] = c                                       # filled to 6 mm under the shoulder
    img[body_top:body_top + int(6 * PX), :] = np.array([226, 222, 214])        # the empty glass under the lid
    # the label: each column of the jar shows the wrap at the angle it faces
    y0 = body_top + int((HB - LABEL_H) / 2 * PX + 4 * PX); hl = int(LABEL_H * PX)
    for col in range(W):
        xm = (col + 0.5) / PX - R; th = np.arcsin(np.clip(xm / R, -0.999, 0.999)); u = FRONT + th * R
        src = lab[:, int(np.clip(u * lk, 0, lab.shape[1] - 1))]
        src = np.asarray(Image.fromarray(src.astype(np.uint8)[:, None, :]).resize((1, hl), Image.LANCZOS))[:, 0]
        img[y0:y0 + hl, col] = src * (0.72 + 0.28 * np.cos(th))
    # glass: a soft highlight down the left, darker edges
    x = (np.arange(W) + 0.5) / W * 2 - 1
    shade = (0.82 + 0.18 * np.sqrt(np.clip(1 - x ** 2, 0, 1)))[None, :, None]; img[body_top:] *= shade[:, :, :]
    hi = np.exp(-((x + 0.62) / 0.06) ** 2)[None, :, None] * 70; img[body_top:] += hi
    img[:body_top] = np.array([46, 40, 36])                                   # the lid
    img[:body_top, :] *= (0.75 + 0.25 * np.sqrt(np.clip(1 - x ** 2, 0, 1)))[None, :, None]
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    m = Image.new('L', (W, H), 0); d = ImageDraw.Draw(m)
    d.rounded_rectangle((0, body_top, W - 1, H - 1), radius=int(5 * PX), fill=255); d.rounded_rectangle((int(2 * PX), 0, W - int(2 * PX), body_top + 4), radius=int(2 * PX), fill=255)
    out = Image.new('RGB', (W + 120, H + 120), (238, 232, 222)); sh = Image.new('L', out.size, 0)
    ImageDraw.Draw(sh).ellipse((40, H + 40, W + 80, H + 100), fill=110); sh = sh.filter(ImageFilter.GaussianBlur(14))
    out.paste((120, 105, 90), (0, 0), sh); out.paste(im, (60, 40), m); return out
