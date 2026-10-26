# The landscape/cream boundary of the 12-bag carton, as one function over the unfolded strip of the four walls:
# front -> How to brew side -> back -> other side, u from 0 (front's left edge) to P (back to the front), y down, in
# panel millimetres (H = panel height). Five anchors; between consecutive anchors the quintic smootherstep
# s(t) = 6t^5 - 15t^4 + 10t^3, so every join has matching first and second derivatives (both zero at the anchors).
# There is no anchor at the front/side fold: it falls inside the first segment. The whole curve is then raised by the
# smallest amount that keeps 0.04H between it and the ink of every glyph beneath it (TEXT_INK boxes from tea_box.mjs).
import json, numpy as np
F, SA, BK, SB = 87.65, 84.57, 87.58, 84.85                       # panel widths along the strip, from the cube dieline
H = 84.74
P = F + SA + BK + SB
FOLDS = {'front|side': F, 'side|back': F + SA, 'back|side': F + SA + BK}
ORIGIN = {'front': 0.0, 'sideA': F, 'back': F + SA, 'sideB': F + SA + BK}
ANCHORS = [(0.0, 0.45 * H), (F + 0.25 * SA, 0.62 * H), (F + SA, 0.53 * H), (F + SA + BK, 0.53 * H), (P, 0.45 * H)]
CLEAR = 0.04 * H
def s5(t): return t * t * t * (10 - 15 * t + 6 * t * t)
def raw(u):
    u = np.mod(np.asarray(u, float), P); xa, ya = np.array(ANCHORS).T; y = np.empty_like(u)
    for i in range(len(ANCHORS) - 1):
        m = (u >= xa[i]) & (u <= xa[i + 1]); t = (u[m] - xa[i]) / (xa[i + 1] - xa[i])
        y[m] = ya[i] + (ya[i + 1] - ya[i]) * s5(t)
    return y
def lift(ink_json):
    """the smallest uniform raise that gives every glyph in the cream 0.04H of clear space under the boundary"""
    need = 0.0
    for g in json.load(open(ink_json)):
        if g['panel'] not in ORIGIN: continue
        u = ORIGIN[g['panel']] + np.linspace(g['x0'], g['x1'], 24)
        need = max(need, CLEAR - (g['y0'] - raw(u).max()))
    return max(0.0, need)
DELTA = 0.0
def y(u): return raw(u) - DELTA
