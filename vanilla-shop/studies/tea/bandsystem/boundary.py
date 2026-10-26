# The landscape/cream boundary of the 12-bag carton, as one function over the unfolded strip of the four walls:
# front -> How to brew side -> back -> other side, u from 0 (front's left edge) to P (back to the front), y down, in
# panel millimetres (H = panel height). Five anchors; between consecutive anchors the quintic smootherstep
# s(t) = 6t^5 - 15t^4 + 10t^3, so every join has matching first and second derivatives (both zero at the anchors).
# There is no anchor at the front/side fold: it falls inside the first segment. The whole curve is then raised by the
# smallest amount that keeps 0.04H between it and the ink of every glyph beneath it (TEXT_INK boxes from tea_box.mjs).
import json, numpy as np
import os
BOX = os.environ.get('BOX', 'cube')
if BOX == 'long':                                                  # the 25-bag carton: front and back twice as wide
    F, SA, BK, SB = 175.93, 85.13, 175.01, 84.49
    H = 84.70
else:
    F, SA, BK, SB = 87.65, 84.57, 87.58, 84.85                   # panel widths along the strip, from the cube dieline
    H = 84.74
P = F + SA + BK + SB
FOLDS = {'front|side': F, 'side|back': F + SA, 'back|side': F + SA + BK}
ORIGIN = {'front': 0.0, 'sideA': F, 'back': F + SA, 'sideB': F + SA + BK}
ANCHORS = [(0.0, 0.45 * H), (F + 0.25 * SA, 0.62 * H), (F + SA, 0.53 * H), (F + SA + BK, 0.53 * H), (P, 0.45 * H)]
# The long box's edge is one closed-form function of u, periodic in the perimeter P (so it meets itself at the glue
# flap with every derivative equal): two von Mises bumps on a level line,
#     y(u) = H * ( Y0 + A * v(u; MU, KAPPA) + A2 * v(u; MU2, KAPPA2) ),   v(u; m, k) = exp( k * ( cos(2 pi (u - m) / P) - 1 ) )
# Y0 the level over the name and the end panel; the first bump the front's valley, deepest (Y0 + A) at MU, KAPPA its
# width (half depth at P/(2 pi) * acos(1 - ln 2 / KAPPA) either side); the second a broad, shallow swell centred on the
# back, so the back keeps its hills as the cube's does. Smooth everywhere, no anchors.
VM = dict(Y0=float(os.environ.get('VM_Y0', 0.445)), A=float(os.environ.get('VM_A', 0.20)),
          KAPPA=float(os.environ.get('VM_K', 8.0)), MU=float(os.environ.get('VM_MU', 100.67)),
          A2=float(os.environ.get('VM_A2', 0.04)), KAPPA2=float(os.environ.get('VM_K2', 2.0)), MU2=F + SA + BK / 2)
CLEAR = 0.04 * H
def s5(t): return t * t * t * (10 - 15 * t + 6 * t * t)
def raw(u):
    if BOX == 'long':
        u = np.asarray(u, float)
        v = lambda m, k: np.exp(k * (np.cos(2 * np.pi * (u - m) / P) - 1))
        return H * (VM['Y0'] + VM['A'] * v(VM['MU'], VM['KAPPA']) + VM['A2'] * v(VM['MU2'], VM['KAPPA2']))
    u = np.mod(np.asarray(u, float), P); xa, ya = np.array(ANCHORS).T; y = np.empty_like(u)
    for i in range(len(ANCHORS) - 1):
        m = (u >= xa[i]) & (u <= xa[i + 1]); t = (u[m] - xa[i]) / (xa[i + 1] - xa[i])
        y[m] = ya[i] + (ya[i + 1] - ya[i]) * s5(t)
    return y
def lift(ink_json,skip=()):
    """the smallest uniform raise that gives every glyph in the cream 0.04H of clear space under the boundary"""
    need = 0.0
    for g in json.load(open(ink_json)):
        if g['panel'] not in ORIGIN or g['panel'] in skip: continue
        u = ORIGIN[g['panel']] + np.linspace(g['x0'], g['x1'], 24)
        need = max(need, CLEAR - (g['y0'] - raw(u).max()))
    return max(0.0, need)
DELTA = 0.0
def y(u): return raw(u) - DELTA
