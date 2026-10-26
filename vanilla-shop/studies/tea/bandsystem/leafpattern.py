# A faint engraved tea-leaf pattern for the cream ground: the sprig's own leaf (tea_leaf: Camellia sinensis, pointed,
# finely serrated) as a pair on a short stem, drawn as line engraving (outline, midrib, side veins) and laid in a
# half-drop repeat, every other column mirrored, as heritage papers and tea tins are. Returns a coverage mask over the
# strip; wrap.py tints the cream with it, fading it in from below and away from the type.
import numpy as np, cv2
from PIL import Image, ImageDraw

SS = 4                                                                        # supersampling for the hairlines

def leaf_lines(p0, ang, L, rng=None, ratio=0.36, bend=0.06):
    """one tea leaf as engraving lines (mm): an elliptic, pointed blade (about 2.8:1, widest a little below the middle),
    a smooth outline, the midrib bowed slightly, and side veins that curve towards the tip and stop short of the margin"""
    n = 60; t = np.linspace(0, 1, n)
    a = np.radians(ang); fwd = np.array([np.cos(a), np.sin(a)]); nr = np.array([-fwd[1], fwd[0]])
    mid = p0 + np.outer(t * L, fwd) + np.outer(bend * L * np.sin(np.pi * t), nr)                  # the midrib, bowed
    w = ratio * L / 2 * np.sin(np.pi * np.clip(t, 0, 1)) ** 0.85 * (1 - 0.3 * t ** 1.6)            # half-width, pointed tip
    w[t < 0.04] = 0
    left = mid + np.outer(w, nr); right = mid - np.outer(w, nr)
    lines = [np.vstack([left, right[::-1]]), mid[2:-3]]
    for tv in np.linspace(0.2, 0.78, 6):                                                            # side veins
        j = int(tv * (n - 1)); wj = w[j]
        for sd in (1, -1):
            s0 = mid[j]; e = mid[min(n - 1, j + int(0.13 * n))] + sd * nr * wj * 0.78
            c = s0 + sd * nr * wj * 0.5 + fwd * L * 0.02
            q = np.linspace(0, 1, 6)[:, None]
            lines.append((1 - q) ** 2 * s0 + 2 * (1 - q) * q * c + q ** 2 * e)                   # a quadratic curve
    return lines

def motif(tea_leaf=None, mirror=False, seed=0):
    """two leaves splayed from the tip of a short bowed stem, base at (0,0); about 14 x 14 mm"""
    f = -1 if mirror else 1
    t = np.linspace(0, 1, 14)[:, None]
    stem = np.hstack([f * 0.9 * np.sin(t * 1.8), -4.6 * t]); tip = stem[-1]
    ls = [stem]
    ls += leaf_lines(tip, -90 + f * 34, 9.6)
    ls += leaf_lines(tip + np.array([0, 1.1]), -90 - f * 40, 7.4)
    return ls

def mask(tea_leaf, h, w, K, X0, B, pitch=(24.0, 28.0), lw=(0.14, 0.09), rot=12):
    """coverage (0..1, float32, h x w) of the pattern over the strip canvas; x in strip mm from X0, y in art mm from -B"""
    im = Image.new('L', (w * SS, h * SS), 0); dr = ImageDraw.Draw(im)
    px, py = pitch; k = K * SS
    cols = int((w / K) / px) + 3; rows = int((h / K) / py) + 3
    shapes = [motif(tea_leaf, m, s) for m, s in ((False, 1), (True, 2))]
    for c in range(-1, cols):
        m = c % 2; x = c * px + px / 2
        for r in range(-1, rows):
            y = r * py + (py / 2 if m else 0) + py * 0.55
            th = np.radians(rot if m else -rot); R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
            for i, seg in enumerate(shapes[m]):
                q = seg @ R.T + np.array([x, y])
                dr.line([tuple(v * k) for v in q], fill=255, width=max(1, int(round((lw[1] if len(seg) == 6 else lw[0]) * k))), joint='curve')
    a = np.asarray(im.resize((w, h), Image.LANCZOS)).astype(np.float32) / 255
    return a
