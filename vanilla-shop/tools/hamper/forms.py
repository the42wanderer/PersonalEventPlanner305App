# Object-specific drawing for the hamper lid: each element is constructed from its own structure (a pod round its
# centreline, a leaf from its midrib and veins, a flower from overlapping tepals and a lip, a ribbon as a broad band),
# and engraved in a way that describes its material, not with one shared family of parallel curves.
#
# Production limits are settings, not constants: set them to the printer's ink and foil specifications.
import numpy as np
from shapely.geometry import Polygon, LineString
from shapely.ops import unary_union
from engrave import ribbon_poly, smooth, frames, to_path

SPEC = {
    'print': {'min_line': 0.08, 'min_gap': 0.10},   # mm: finest printable line, finest open gap between lines
    'foil':  {'min_line': 0.15, 'min_gap': 0.20},
}
LIGHT2D = np.array([-0.62, -0.78]); LIGHT2D /= np.linalg.norm(LIGHT2D)   # light from the upper left, on the page

def cubic(P0, P1, P2, P3, n=400):
    t = np.linspace(0, 1, n)[:, None]
    return (1 - t) ** 3 * P0 + 3 * (1 - t) ** 2 * t * P1 + 3 * (1 - t) * t ** 2 * P2 + t ** 3 * P3

def arclen_param(C):
    s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(C, axis=0), axis=1))]; return s / s[-1], s[-1]

def line(pts, w, layer='print', taper=0.4):
    """a stroke as a polygon, its width held at or above the layer's minimum line"""
    w = np.maximum(np.asarray(w, float), SPEC[layer]['min_line'])
    return ribbon_poly(np.asarray(pts, float), w, taper=taper)

class Pod:
    """a cured vanilla pod built round one centreline: a gentle cubic Bezier with a shallow bow. Both edges come from
    that centreline and its local perpendicular, edge(t) = C(t) +/- w(t) N(t), so the body keeps an even thickness. The
    stem end narrows to a short stalk with a rounded end; the tip tapers softly to a point."""
    def __init__(self, start, end, bow=0.06, width_frac=0.036, flip=1, n=500):
        a, b = np.array(start, float), np.array(end, float); d = b - a; L = np.linalg.norm(d); u = d / L
        nrm = np.array([-u[1], u[0]]) * flip
        # one cubic: the handles at a third and two thirds, pushed sideways for the bow (the far handle a little more,
        # so the tip end carries the slight turn)
        P1 = a + d / 3 + nrm * bow * L * 1.0; P2 = a + 2 * d / 3 + nrm * bow * L * 1.25
        self.C = cubic(a, P1, P2, b, n); self.t, self.L = arclen_param(self.C)
        self.T, self.N = frames(self.C)
        self.W = width_frac * self.L                                   # full body width
    def halfwidth(self, t):
        t = np.asarray(t, float); h = self.W / 2
        stem = 0.24
        # from the stalk the body widens gradually over its first third (one smooth rise, no shoulder), holds an even
        # thickness (a faint waist, no belly), and tapers softly to the tip over the last fifth
        rise = stem + (1 - stem) * smooth(-0.04, 0.36, t) ** 0.85
        body = 1 - 0.03 * np.sin(np.pi * np.clip((t - 0.30) / 0.50, 0, 1))
        tip = np.clip(1 - ((t - 0.80) / 0.20) ** 2.0, 0, 1) ** 0.55
        f = np.where(t < 0.36, rise, np.where(t < 0.80, body, tip))
        return h * f
    def edge(self, side, t=None):
        t = self.t if t is None else t
        C = np.stack([np.interp(t, self.t, self.C[:, k]) for k in (0, 1)], 1)
        N = np.stack([np.interp(t, self.t, self.N[:, k]) for k in (0, 1)], 1)
        return C + N * (side * self.halfwidth(t))[:, None]
    def outline(self):
        A = self.edge(+1); B = self.edge(-1)
        # the stalk's end, rounded: a half circle round C(0)
        r = self.halfwidth(0.0); c0 = self.C[0]; back = -self.T[0]; N0 = self.N[0]
        ths = np.linspace(np.pi, 0, 24)                       # from the -N edge round the back to the +N edge
        cap = np.array([c0 + r * (N0 * np.cos(th) + back * np.sin(th)) for th in ths])
        p = Polygon(np.vstack([A, B[::-1], cap]))
        return p if p.is_valid else p.buffer(0)
    def _at(self, t):
        C = np.stack([np.interp(t, self.t, self.C[:, k]) for k in (0, 1)], 1)
        N = np.stack([np.interp(t, self.t, self.N[:, k]) for k in (0, 1)], 1)
        return C, N
    def engrave(self, layer='print'):
        """the material: a solid shadow along the edge away from the light, tapering out towards both ends; a few
        longitudinal wrinkles following the centreline, closer and heavier towards that shadow, of different lengths, some
        stopping short; a narrow highlight on the lit side, broken where one wrinkle crosses it; the closed outline,
        heavier on the shadow side"""
        out = []; spec = SPEC[layer]
        mid = len(self.N) // 2
        dark = 1 if (self.N[mid] @ -LIGHT2D) > 0 else -1                             # the edge away from the light
        # the shadow band: from v = inner to the dark edge
        t = np.linspace(0.02, 0.985, 300); C, N = self._at(t); h = self.halfwidth(t)
        inner = 1 - 0.38 * smooth(0.04, 0.30, t) * (1 - smooth(0.78, 0.97, t))
        Eo = C + N * (dark * h)[:, None]; Ei = C + N * (dark * h * inner)[:, None]
        band = Polygon(np.vstack([Eo, Ei[::-1]])).buffer(0)
        if not band.is_empty: out.append(band)
        # wrinkles: (offset towards the dark side, start, end, weight 0..1, drift waves, phase)
        AMP = 0.025
        lines = [(-0.72, 0.30, 0.72, 0.35, 1.0, 0.3),
                 (-0.52, 0.12, 0.62, 0.45, 1.5, 1.1),
                 (-0.32, 0.56, 0.88, 0.50, 1.0, 2.0),          # crosses the highlight late: its break
                 (-0.13, 0.06, 0.93, 0.60, 1.5, 0.6),
                 (0.05, 0.10, 0.84, 0.75, 2.0, 2.4),
                 (0.21, 0.05, 0.95, 0.85, 1.5, 0.9),
                 (0.36, 0.16, 0.90, 1.00, 2.5, 1.7),
                 (0.49, 0.08, 0.80, 1.00, 1.0, 2.6)]
        offs = sorted([l[0] for l in lines] + [inner.min()])
        for v0, t0, t1, wt, waves, ph in lines:
            t = np.linspace(t0, t1, 240); C, N = self._at(t); h = self.halfwidth(t)
            v = v0 + AMP * np.sin(2 * np.pi * waves * (t - t0) / (t1 - t0) + ph)
            P = C + N * (dark * v * h)[:, None]
            k = offs.index(v0); gaps = [offs[k] - offs[k - 1] if k > 0 else 1, offs[k + 1] - offs[k] if k + 1 < len(offs) else 1]
            room = (min(gaps) - 2 * AMP) * h - spec['min_gap']                        # never closer than the minimum gap
            hl = np.exp(-((v + 0.36) / 0.09) ** 2)                                    # the highlight thins lines to nothing
            w = np.minimum(spec['min_line'] + 0.26 * wt * (1 - hl), room)
            w = np.where(w >= spec['min_line'], w, 0)
            out += [p for p in _runs(P, w, layer) if p is not None]
        # the closed outline (stalk end included), heavier on the shadow side
        B = np.asarray(self.outline().exterior.coords)
        tt, nn = frames(B)
        area = 0.5 * np.sum(B[:-1, 0] * B[1:, 1] - B[1:, 0] * B[:-1, 1]); outward = nn * (1 if area < 0 else -1)
        k = np.clip(outward @ -LIGHT2D, 0, 1)
        out.append(line(B, 0.14 + 0.18 * k, layer, taper=0.01))
        return out

def _pod_negative(self, layer='print'):
    """a dark object engraved in reverse: the pod cut solid, its light cut into it as open lines that follow the
    centreline. A narrow highlight streak runs along the lit side, broken twice; light wrinkles of different lengths and
    spacing, most on the lit half, a couple faint on the shadow half. Open lines are at least the minimum gap wide; the
    ink left between them at least the minimum line."""
    spec = SPEC[layer]; body = self.outline()
    mid = len(self.N) // 2; dark = 1 if (self.N[mid] @ -LIGHT2D) > 0 else -1
    cuts = []
    # (offset towards the dark side, start, end, width mm, drift waves, phase); negative offsets are the lit half
    marks = [(-0.40, 0.16, 0.44, 0.30, 1.0, 0.4), (-0.40, 0.49, 0.71, 0.26, 1.0, 1.6), (-0.42, 0.76, 0.90, 0.20, 1.0, 2.2),   # the highlight, broken twice
             (-0.68, 0.24, 0.62, 0.14, 1.5, 0.8), (-0.62, 0.66, 0.86, 0.12, 1.0, 2.9),
             (-0.20, 0.10, 0.52, 0.13, 2.0, 1.3), (-0.14, 0.58, 0.92, 0.12, 1.5, 0.2),
             (0.02, 0.30, 0.78, 0.11, 2.0, 2.0),
             (0.30, 0.20, 0.55, 0.10, 1.0, 0.7), (0.40, 0.62, 0.84, 0.10, 1.0, 1.9)]
    for v0, t0, t1, wmm, waves, ph in marks:
        t = np.linspace(t0, t1, 200); C, N = self._at(t); h = self.halfwidth(t)
        v = v0 + 0.03 * np.sin(2 * np.pi * waves * (t - t0) / (t1 - t0) + ph)
        P = C + N * (dark * v * h)[:, None]
        w = np.maximum(wmm * np.clip(h / (self.W / 2), 0.3, 1), spec['min_gap'])     # narrower where the pod narrows
        p = ribbon_poly(P, w, taper=min(2.5, 0.25 * (t1 - t0) * self.L))
        if p is not None: cuts.append(p)
    g = body.difference(unary_union(cuts)) if cuts else body
    # keep the ink between cuts printable: drop slivers thinner than the minimum line
    g = g.buffer(-spec['min_line'] / 2).buffer(spec['min_line'] / 2)
    return [g.intersection(body)]
Pod.engrave_negative = _pod_negative

def _runs(P, w, layer):
    """keep only stretches that are at least the minimum line; the rest are left open (highlights)"""
    ok = w >= SPEC[layer]['min_line'] * 0.999; out = []; i = 0
    while i < len(w):
        if not ok[i]: i += 1; continue
        j = i
        while j < len(w) and ok[j]: j += 1
        if j - i > 3: out.append(line(P[i:j], w[i:j], layer, taper=0.8))
        i = j
    return out

class Leaf:
    """a vanilla leaf built from its midrib: a short stalk, a gently bowed midrib (one cubic), the blade on either side
    of it from the local perpendicular, a little wider on one side, widest below the middle and drawn to a short point.
    Veins branch from the midrib at intervals and arch towards the tip, stopping short of the margin (an orchid's
    veins run long and curve, they do not fan out)."""
    def __init__(self, base, ang, L, W, bow=0.07, asym=0.12, flip=1, n=400):
        a = np.radians(ang); d = np.array([np.cos(a), np.sin(a)]); nrm = np.array([-d[1], d[0]]) * flip
        b = np.array(base, float); e = b + d * L
        self.C = cubic(b, b + d * L / 3 + nrm * bow * L, b + 2 * d * L / 3 + nrm * bow * L * 0.9, e, n)
        self.t, self.L = arclen_param(self.C); self.T, self.N = frames(self.C)
        self.W, self.asym, self.flip = W, asym, flip
    def halfwidth(self, t, side):
        """a thin stalk for the first 6%, then the blade: a rounded wedge to its widest at about 0.45, an even middle,
        drawn in to a true point (width 0 at the tip)"""
        t = np.asarray(t, float); h = self.W / 2
        stalk = 0.045 * self.W
        blade = smooth(0.04, 0.45, t) ** 0.62 * np.clip(1 - smooth(0.52, 1.0, t) ** 1.0, 0, 1) ** 0.62
        f = np.maximum(stalk / h * (1 - smooth(0.05, 0.16, t)), blade)
        return h * f * (1 + self.asym * side)
    def at(self, t):
        C = np.stack([np.interp(t, self.t, self.C[:, k]) for k in (0, 1)], -1)
        N = np.stack([np.interp(t, self.t, self.N[:, k]) for k in (0, 1)], -1)
        return C, N
    def point(self, t, v):
        """v in [-1, 1] across the blade (fraction of the half-width on that side)"""
        t = np.asarray(t, float); v = np.asarray(v, float); C, N = self.at(t)
        return C + N * (v * self.halfwidth(t, np.sign(v) + (v == 0)))[..., None]
    def outline(self):
        t = self.t
        A = self.point(t, np.ones_like(t)); B = self.point(t[::-1], -np.ones_like(t))
        r = 0.045 * self.W; c0 = self.C[0]; back = -self.T[0]; N0 = self.N[0]
        cap = np.array([c0 + r * (N0 * np.cos(th) + back * np.sin(th)) for th in np.linspace(np.pi, 0, 16)])   # the stalk's rounded end
        p = Polygon(np.vstack([A, B, cap])); return p if p.is_valid else p.buffer(0)

    def _vein_path(self, ti, side, D=0.26, v1=0.86, n=40):
        v = np.linspace(0.03, v1, n); t = ti + D * v ** 1.6
        return t, side * v
    def engrave(self, layer='print', nveins=5):
        spec = SPEC[layer]; out = []
        sides = (1, -1)
        mid = len(self.N) // 2
        dark_side = 1 if (self.N[mid] @ -LIGHT2D) > 0 else -1                # the half turned from the light
        # midrib: heavier at the stalk, fading towards the tip
        t = np.linspace(0.0, 0.93, 200); C, _ = self.at(t)
        out.append(line(C, 0.30 * (1 - t) + 0.08, layer, taper=1.0))
        # veins, alternating sides, branching from the midrib and arching to the tip
        tis = {s: np.linspace(0.12 + (0.04 if s == -1 else 0), 0.66, nveins) for s in sides}
        for s in sides:
            for ti in tis[s]:
                tt, vv = self._vein_path(ti, s); P = self.point(tt, vv)
                w = 0.17 * (1 - np.abs(vv)) ** 0.8 + 0.06
                out.append(line(P, w, layer, taper=0.8))
        # tone: the blade curls - darker beside the midrib on the lit half, towards the margin on the shadow half, more
        # at the base, and drifting along the length so the shade does not simply follow the midrib
        def tone(t, v):
            s = np.sign(v); a = np.abs(v)
            shadow = (s == dark_side)
            base = np.where(shadow, 0.42 + 0.30 * smooth(0.3, 1.0, a), 0.10 + 0.40 * np.exp(-a / 0.18))
            return np.clip(base + 0.16 * (1 - t) + 0.10 * np.sin(2 * np.pi * (1.1 * t + 0.25 * s)), 0, 1)
        # hatch between the veins, parallel to them
        for s in sides:
            ts = list(tis[s]) + [tis[s][-1] + (tis[s][-1] - tis[s][-2])]
            for i in range(len(ts) - 1):
                gap_t = ts[i + 1] - ts[i]
                k = max(2, int(gap_t * self.L * 0.55 / 0.55))                  # lines about 0.55 mm apart
                spacing = gap_t * self.L * 0.55 / (k + 1)
                for j in range(1, k + 1):
                    t0 = ts[i] + gap_t * j / (k + 1)
                    tt, vv = self._vein_path(t0, s, v1=0.92)
                    ok = tt < 0.97
                    tt, vv = tt[ok], vv[ok]
                    if len(tt) < 4: continue
                    P = self.point(tt, vv)
                    tn = tone(tt, vv)
                    w = np.where(tn > 0.28, spec['min_line'] + 0.26 * smooth(0.28, 1, tn), 0)
                    w = np.minimum(w, spacing - spec['min_gap'])
                    w = np.where(w >= spec['min_line'], w, 0)
                    out += [p for p in _runs(P, w, layer) if p is not None]
        # the outline, heavier on the shadow side
        B = np.asarray(self.outline().exterior.coords); tt, nn = frames(B)
        area = 0.5 * np.sum(B[:-1, 0] * B[1:, 1] - B[1:, 0] * B[:-1, 1]); outward = nn * (1 if area < 0 else -1)
        k = np.clip(outward @ -LIGHT2D, 0, 1)
        out.append(line(B, 0.14 + 0.20 * k, layer, taper=0.01))
        body = self.outline().buffer(0.2)
        return [p.intersection(body) for p in out if p is not None]


class Tepal:
    """a sepal or petal: a narrow claw at the base, widest past the middle, an acute tip; built round one cubic
    centreline from the flower's heart. Foreshortening narrows and shortens a part turned away; a twist turns the blade
    edge-on towards the tip (width x |cos(twist)|), so tips curl rather than all lying flat."""
    def __init__(self, c, ang, L, W, bend=0.1, twist=0.0, fore=1.0, n=300):
        a = np.radians(ang); d = np.array([np.cos(a), np.sin(a)]); nr = np.array([-d[1], d[0]])
        c = np.array(c, float); L = L * (0.75 + 0.25 * fore); e = c + d * L
        self.C = cubic(c, c + d * L / 3 + nr * bend * L * 0.4, c + 2 * d * L / 3 + nr * bend * L, e, n)
        self.t, self.L = arclen_param(self.C); self.T, self.N = frames(self.C)
        self.W = W * fore; self.twist = twist
    def halfwidth(self, t):
        t = np.asarray(t, float)
        # fleshy and oblong: broad already at the base (the bases overlap round the heart), widest from about 0.4 to
        # 0.65, then drawn to an acute tip
        f = (0.48 + 0.52 * smooth(0.0, 0.42, t)) * np.clip(1 - smooth(0.64, 1.0, t) ** 1.15, 0, 1) ** 0.7
        tw = np.abs(np.cos(np.radians(self.twist) * smooth(0.35, 1.0, t)))
        return self.W / 2 * f * (0.25 + 0.75 * tw)
    def at(self, t):
        return (np.stack([np.interp(t, self.t, self.C[:, k]) for k in (0, 1)], -1),
                np.stack([np.interp(t, self.t, self.N[:, k]) for k in (0, 1)], -1))
    def point(self, t, v):
        C, N = self.at(np.asarray(t, float)); return C + N * (np.asarray(v, float) * self.halfwidth(t))[..., None]
    def outline(self):
        t = self.t; A = self.point(t, np.ones_like(t)); B = self.point(t[::-1], -np.ones_like(t))
        p = Polygon(np.vstack([A, B])); return p if p.is_valid else p.buffer(0)

class Lip:
    """the vanilla orchid's lip in three-quarter view: a trumpet from the heart, wrapping the column, its mouth flared
    and frilled and turned towards the viewer. tube: from the heart to the mouth; mouth: a frilled ellipse."""
    def __init__(self, c, toward, length, mouth_rx, mouth_ry, rot, lobes=11, frill=0.07, r0=3.0):
        self.r0 = r0; self.c = np.array(c, float); a = np.radians(toward); self.d = np.array([np.cos(a), np.sin(a)])
        self.m = self.c + self.d * length; self.rx, self.ry, self.rot = mouth_rx, mouth_ry, np.radians(rot)
        self.lobes, self.frill = lobes, frill
    def rim(self, n=400, k=1.0):
        th = np.linspace(0, 2 * np.pi, n, endpoint=False)
        r = 1 + self.frill * np.sin(self.lobes * th) + 0.03 * np.sin(3 * th + 0.7)
        x, y = self.rx * k * r * np.cos(th), self.ry * k * r * np.sin(th)
        R = np.array([[np.cos(self.rot), -np.sin(self.rot)], [np.sin(self.rot), np.cos(self.rot)]])
        return self.m + np.column_stack([x, y]) @ R.T
    def tube(self):
        """the outer wall from the heart to the mouth: hull of a small circle at the heart and the rim"""
        from shapely.geometry import MultiPoint
        base = [self.c + self.r0 * np.array([np.cos(a), np.sin(a)]) for a in np.linspace(0, 2 * np.pi, 24)]
        return MultiPoint(list(map(tuple, base)) + list(map(tuple, self.rim(120)))).convex_hull
    def mouth(self):
        p = Polygon(self.rim()); return p if p.is_valid else p.buffer(0)
    def outline(self):
        return unary_union([self.tube(), self.mouth()])

class Flower:
    """parts in drawing order, back to front: the two lateral sepals low behind, the dorsal sepal leaning back, the two
    petals spreading up and out in front of the sepals' bases, the lip in front of everything"""
    def __init__(self, c, R=40.0, rot=0.0):
        c = np.array(c, float); self.c = c
        def T(ang, Lf, Wf, bend, twist, fore): return Tepal(c, ang + rot, R * Lf, R * Wf, bend, twist, fore)
        # irregular spacing (not 72 degrees apart): the gaps open towards the lip
        self.parts = [
            ('sepal_l', T(150, 0.90, 0.27, -0.10, 25, 0.95)),
            ('sepal_r', T(22, 0.80, 0.25, 0.12, 45, 0.75)),     # turned away: shorter, narrower, twisted
            ('dorsal', T(-98, 0.96, 0.28, 0.10, 15, 0.92)),
            ('petal_l', T(-150, 0.88, 0.30, -0.15, 30, 1.00)),
            ('petal_r', T(-42, 0.80, 0.27, 0.14, 50, 0.80)),
        ]
        # the lip: a long funnel down and towards the viewer, its frilled mouth about half the flower's radius across
        a = np.radians(68 + rot)
        self.lip = Lip(c + 1.5 * np.array([np.cos(a), np.sin(a)]), 68 + rot, R * 0.52, R * 0.30, R * 0.23, rot + 30,
                       lobes=13, frill=0.06, r0=R * 0.13)
    def silhouette(self):
        return unary_union([p.outline() for _, p in self.parts] + [self.lip.outline()])
    def outline_drawing(self, layer='print', gap=0.4):
        """each part's outline, cut back where a part in front covers it (with a hairline gap)"""
        shapes = [p.outline() for _, p in self.parts] + [self.lip.tube(), self.lip.mouth()]
        out = []
        for i, s in enumerate(shapes):
            front = unary_union(shapes[i + 1:]).buffer(gap) if i + 1 < len(shapes) else None
            ring = s.exterior.buffer(0.14)
            out.append(ring.difference(front) if front is not None else ring)
        return out


# ---- the brand's own orchid: the vanilla flower on the tea cartons (studies/extract/split/draw.py, painted there by
# foliage2.paint_flower), rebuilt here as vector shapes with exactly its geometry, so the hamper engraves the same
# flower the range already shows.
import sys as _sys, os as _os, math as _math
_sys.path.insert(0, _os.path.join(_os.path.dirname(__file__), '..', '..', 'studies', 'extract', 'split'))
import draw as _draw

class BrandFlower:
    SPEC = [(-97, 16.5, 2.0, 0.26, 0.0), (-160, 14.8, 1.85, -0.36, 0.3), (-36, 15.6, 1.9, 0.34, 0.25),
            (126, 13.2, 1.75, 0.30, 0.4), (54, 13.8, 1.8, -0.32, 0.35)]     # angle, length, width, bend, pinch
    ORDER = [1, 3, 0, 2, 4]                                                # back tepals first
    BACK = {1, 3}
    def __init__(self, c, ang_lip=30, s=2.35):
        cx, cy = c; self.c = np.array(c, float); self.s = s; self.ang_lip = ang_lip
        self.tepals = []
        for i in self.ORDER:
            a, L, W, b, pin = self.SPEC[i]; a2 = a + ang_lip * 0.25
            Lf = L * s * (0.8 + 0.2 * abs(np.cos(np.radians(a2 - ang_lip))))
            poly = _draw.tepal((cx, cy), a2, Lf, W * s, b, 0.012, i * 0.9, pin)
            sp = np.asarray(_draw.tepal((cx, cy), a2, Lf * 0.82, W * s, b, spine=True))
            self.tepals.append(dict(i=i, poly=Polygon(poly).buffer(0), spine=sp, back=i in self.BACK, W=W * s))
        tube, mouth, mc = _draw.trumpet((cx, cy), ang_lip, 7.5 * s, 1.1 * s, 3.6 * s, 2.6 * s, 0.13)
        self.tube = Polygon(tube).buffer(0); self.mouth = Polygon(mouth).buffer(0); self.mc = np.asarray(mc)
        dd = np.array([np.cos(np.radians(ang_lip)), np.sin(np.radians(ang_lip))])
        self.throat = Polygon(_draw.ellipse_ruffle(self.mc + dd * 0.5 * s, 1.7 * s, 1.25 * s, ang_lip, 0.07, 7)).buffer(0)
    def shapes(self):
        """back to front"""
        return [t['poly'] for t in self.tepals] + [self.tube, self.mouth]
    def silhouette(self):
        return unary_union(self.shapes())
    def outline_drawing(self, gap=0.4, w=0.16):
        S = self.shapes(); out = []
        for i, s_ in enumerate(S):
            front = unary_union(S[i + 1:]).buffer(gap) if i + 1 < len(S) else None
            ring = s_.exterior.buffer(w / 2)
            out.append(ring.difference(front) if front is not None else ring)
        out.append(self.throat.exterior.buffer(w / 2))
        return out

def _bf_engrave(self, layer='print', spacing=0.48):
    """returns (hatch, outlines): the flower's own engraving. Tepals: strokes from the heart along each tepal's spine,
    fanned with its width, dense at the heart and along the edge turned from the light, fading to the tip, a clear
    channel down the midrib. The lip's tube: rings round it. The mouth: contours following the frill in to a dark
    throat."""
    spec = SPEC[layer]; hatch = []
    S = self.shapes()
    for ti, tp in enumerate(self.tepals):
        sp = tp['spine']; n = len(sp)
        front = unary_union(S[ti + 1:]).buffer(0.4)                              # what lies in front of this tepal
        poly = tp['poly'].buffer(-0.12).difference(front)
        T, Nn = frames(sp); t = np.linspace(0, 1, n)
        prof = np.minimum(1, 0.4 + t * 3.0) * np.sin(np.pi * np.minimum(t, 0.999) ** 0.78) ** 0.8   # draw.tepal's own profile
        Wd = tp['W']
        dark_side = 1 if (Nn[n // 2] @ -LIGHT2D) > 0 else -1
        k = int(Wd / spacing)
        for j in range(-k, k + 1):
            v = j / max(k, 1)                                                    # -1 .. 1 across
            if abs(v) < 0.10: continue                                           # the midrib stays clear
            P = sp + Nn * (v * Wd * prof * 1.05)[:, None]
            side = np.sign(v) * dark_side                                        # +1 on the shaded half
            heart = np.exp(-t / 0.20) * smooth(0.04, 0.12, t)                    # where the tepals meet the column
            edge = smooth(0.45, 1.0, abs(v)) * (side > 0)                         # the turned edge in shadow
            tone = 0.08 + 0.75 * heart + 0.45 * edge * (1 - smooth(0.6, 1.0, t)) + (0.12 if tp['back'] else 0)
            w = np.where(tone > 0.22, spec['min_line'] + 0.22 * smooth(0.22, 1, tone), 0)
            w = np.minimum(w, spacing * 1.05 * prof.max() - spec['min_gap'])
            w = np.where(w >= spec['min_line'], w, 0)
            w = np.where(t < 0.10, 0, w)                                          # strokes start clear of the very centre
            for p in _runs(P, w, layer):
                if p is not None: hatch.append(p.intersection(poly))
    # the tube: rings round it from the heart to the mouth, heavier on the shadow side
    a = np.radians(self.ang_lip); d = np.array([np.cos(a), np.sin(a)]); nn = np.array([-d[1], d[0]])
    L = 7.5 * self.s
    for u in np.arange(0.12, 0.98, spacing * 1.1 / L):
        c = self.c + d * L * u; half = (1.1 * self.s + (3.6 * self.s * 0.95 - 1.1 * self.s) * u) * 1.1
        v = np.linspace(-1, 1, 30); P = c + np.outer(v * half, nn) + np.outer(0.18 * half * (1 - v ** 2), d)
        sh = np.clip((nn @ -LIGHT2D) * v, 0, 1)
        w = np.where(sh > 0.15, spec['min_line'] + 0.20 * sh, 0)
        for p in _runs(P, w, layer):
            if p is not None: hatch.append(p.intersection(self.tube.difference(self.mouth.buffer(0.3))))
    # the mouth: contours following the frill inwards, then the throat dark
    for k_ in np.arange(0.92, 0.45, -0.075):
        R = np.asarray(_draw.ellipse_ruffle(self.mc, 2.6 * self.s * k_, 3.6 * self.s * k_, self.ang_lip, 0.13, 9))
        R = np.vstack([R, R[:1]])
        rel = R - self.mc; sh = np.clip((rel / (np.linalg.norm(rel, axis=1, keepdims=True) + 1e-9)) @ -LIGHT2D, 0, 1)
        w = np.where(sh > 0.2, spec['min_line'] + 0.16 * sh * (1.2 - k_), 0)
        for p in _runs(R, w, layer):
            if p is not None: hatch.append(p.intersection(self.mouth))
    # the throat seen at an angle: contours receding into the tube, each deeper one shifted back along it and
    # heavier; arcs on the far inner wall, closing to full rings only in the dark depth
    depth = 3.0 * self.s
    for k_ in np.arange(0.80, 0.10, -0.06):
        ctr = self.mc - d * (0.80 - k_) * depth
        R = np.asarray(_draw.ellipse_ruffle(ctr, 2.6 * self.s * k_, 3.6 * self.s * k_, self.ang_lip, 0.13 * k_, 9)); R = np.vstack([R, R[:1]])
        rel = R - ctr; rel /= np.linalg.norm(rel, axis=1, keepdims=True) + 1e-9
        far = smooth(-0.35, 0.25, rel @ -d)                                      # the far wall
        deep = 1 - k_ / 0.8
        w = spec['min_line'] + 0.24 * deep ** 0.8
        w = np.where((far > 0.5) | (k_ < 0.3), w, 0)
        for p in _runs(R, np.where(w > 0, np.maximum(w, spec['min_line']), 0), layer):
            if p is not None: hatch.append(p.intersection(self.mouth))
    return hatch, self.outline_drawing(w=0.22)
BrandFlower.engrave_parts = _bf_engrave
BrandFlower.engrave = lambda self, layer='print': sum(self.engrave_parts(layer), [])


class Ribbon:
    """a satin ribbon: one smooth centreline (through the given points), a constant width, and a twist phi(s) about the
    centreline (degrees, interpolated smoothly between the given values). Each edge is C(s) +/- W/2 cos(phi) N(s): where
    cos(phi) is near 0 the band turns edge-on, where it changes sign its back shows. Drawn in short pieces in order along
    its length; a later stretch that crosses an earlier one lies in front of it, the earlier one cut back."""
    def __init__(self, pts, W, phis, n=900, piece=4.0, notch=(False, True)):
        from engrave import catmull, resample
        self.notch = notch
        self.C = resample(catmull(pts, n * 2), n); self.t, self.L = arclen_param(self.C)
        self.T, self.N = frames(self.C); self.W = W
        ph = np.asarray(phis, float); u = np.linspace(0, 1, len(ph))
        # a smooth twist profile through the given values (monotone cubic-ish via smoothstep blending)
        def phi(t):
            t = np.asarray(t, float); i = np.clip(np.searchsorted(u, t) - 1, 0, len(u) - 2)
            a = (t - u[i]) / (u[i + 1] - u[i]); a = a * a * (3 - 2 * a)
            return ph[i] + (ph[i + 1] - ph[i]) * a
        self.phi = phi; self.piece = piece
    def edges(self, t):
        C = np.stack([np.interp(t, self.t, self.C[:, k]) for k in (0, 1)], -1)
        N = np.stack([np.interp(t, self.t, self.N[:, k]) for k in (0, 1)], -1)
        c = np.cos(np.radians(self.phi(t)))
        return C + N * (self.W / 2 * c)[:, None], C - N * (self.W / 2 * c)[:, None], c
    def _notch(self, end):
        """a swallowtail cut at the start (0) or end (1): a V taken out of the band's end"""
        t = 1.0 if end else 0.0; A, Bb, _ = self.edges(np.array([t])); C = (A[0] + Bb[0]) / 2
        T = np.array([np.interp(t, self.t, self.T[:, k]) for k in (0, 1)]) * (1 if end else -1)
        return Polygon([A[0] + T * 2, C - T * 0.55 * self.W, Bb[0] + T * 2])
    def pieces(self):
        """(t0, t1, polygon) for short stretches along the ribbon"""
        n = max(8, int(self.L / self.piece)); ts = np.linspace(0, 1, n + 1); out = []
        cuts = [self._notch(e) for e, on in zip((0, 1), self.notch) if on]
        for a, b in zip(ts[:-1], ts[1:]):
            t = np.linspace(a, b, 24); A, Bb, _ = self.edges(t)
            p = Polygon(np.vstack([A, Bb[::-1]])).buffer(0.02)
            for c in cuts: p = p.difference(c)
            out.append((a, b, p))
        return out
    def visible(self, gap=0.45):
        """each piece minus the later pieces that cross over it (not its neighbours)"""
        P = self.pieces(); out = []
        for i, (a, b, p) in enumerate(P):
            later = [q for j, (_, _, q) in enumerate(P) if j > i + 2 and q.intersects(p)]
            vis = p.difference(unary_union(later).buffer(gap)) if later else p
            out.append((a, b, vis))
        return out
    def outline(self):
        return unary_union([p for _, _, p in self.pieces()])
    def silhouette(self):
        return unary_union([v for _, _, v in self.visible()])


class FoldRibbon:
    """a satin ribbon that changes direction by folding: flat stretches, each a band of constant width round its own
    smooth centreline, joined at folds. At a fold the crease runs through the fold point along d1 + d2 (reflecting the
    band across it turns the incoming direction d1 into the outgoing d2); both stretches are trimmed there, and the
    outgoing one, its back now showing, lies on top. Faces alternate front/back at each fold. Ends: swallowtail."""
    def __init__(self, segments, W, notch=(True, True), gap=0.45):
        from engrave import catmull, resample
        self.W, self.gap = W, gap; self.segs = []
        for pts in segments:
            C = resample(catmull(pts, 400), 300); T, N = frames(C); self.segs.append(dict(C=C, T=T, N=N))
        self.notch = notch
    def _band(self, C, N):
        A = C + N * self.W / 2; B = C - N * self.W / 2
        return Polygon(np.vstack([A, B[::-1]])).buffer(0)
    def faces(self):
        """(polygon, face) per stretch, back to front, already trimmed at the creases"""
        out = []; S = self.segs
        for i, s in enumerate(S):
            C, T, N = s['C'], s['T'], s['N']
            # extend beyond any fold end so the crease cut is clean
            ext0 = np.array([C[0] - T[0] * self.W * 1.5]) if i > 0 else np.empty((0, 2))
            ext1 = np.array([C[-1] + T[-1] * self.W * 1.5]) if i < len(S) - 1 else np.empty((0, 2))
            CC = np.vstack([ext0, C, ext1]); TT, NN = frames(CC)
            p = self._band(CC, NN)
            for j, (F, d1, d2) in enumerate(self.folds()):
                if j not in (i - 1, i): continue
                c = d1 + d2; c /= np.linalg.norm(c) + 1e-12
                side = np.sign(c[0] * (-d1[1]) - c[1] * (-d1[0])) or 1           # the side both stretches lie on
                nrm = np.array([-c[1], c[0]]) * side
                half = Polygon([F - c * 500, F + c * 500, F + c * 500 + nrm * 500, F - c * 500 + nrm * 500])
                p = p.intersection(half)
            if i == 0 and self.notch[0]: p = p.difference(self._notch(C[0], -T[0], N[0]))
            if i == len(S) - 1 and self.notch[1]: p = p.difference(self._notch(C[-1], T[-1], N[-1]))
            out.append((p, 'front' if i % 2 == 0 else 'back'))
        return out
    def _notch(self, C, T, N):
        A = C + N * self.W / 2; B = C - N * self.W / 2
        return Polygon([A + T * 2, C - T * 0.55 * self.W, B + T * 2])
    def folds(self):
        S = self.segs
        return [(S[i]['C'][-1], S[i]['T'][-1], S[i + 1]['T'][0]) for i in range(len(S) - 1)]
    def visible(self):
        F = self.faces(); out = []
        for i, (p, face) in enumerate(F):
            front = unary_union([q for q, _ in F[i + 1:]]) if i + 1 < len(F) else None
            out.append((p.difference(front.buffer(self.gap)) if front is not None else p, face))
        return out
    def silhouette(self):
        return unary_union([p for p, _ in self.visible()])

def _fr_engrave(self, layer='foil', spacing=0.62):
    """for a foil ribbon: the visible faces as solid foil, with lines cut out of it (garnet showing) running along
    the band. Front faces stay bright, cut only towards their curling edges; back faces carry more; both deepen
    towards each crease, where the satin turns. Cuts are at least the foil's minimum gap; the foil between them at
    least its minimum line. Returns the foil geometry."""
    spec = SPEC[layer]; F = self.folds(); out = []
    for i, ((vis, face), s) in enumerate(zip(self.visible(), self.segs)):
        C, T, N = s['C'], s['T'], s['N']
        ext0 = np.array([C[0] - T[0] * self.W * 1.5]) if i > 0 else np.empty((0, 2))
        ext1 = np.array([C[-1] + T[-1] * self.W * 1.5]) if i < len(self.segs) - 1 else np.empty((0, 2))
        CC = np.vstack([ext0, C, ext1]); TT, NN = frames(CC)
        cuts = []
        for v in np.arange(-0.96, 0.97, 2 * spacing / self.W):
            P = CC + NN * (v * self.W / 2)
            dcrease = np.min([np.linalg.norm(P - f[0], axis=1) for f in F], axis=0) if F else np.full(len(P), 99.0)
            near = np.clip(1 - dcrease / (1.6 * self.W), 0, 1) ** 1.5
            edge = smooth(0.62, 1.0, abs(v))
            tone = (0.10 if face == 'front' else 0.34) + 0.45 * edge + 0.60 * near
            w = np.where(tone > 0.30, spec['min_gap'] + (spacing - spec['min_line'] - spec['min_gap']) * smooth(0.30, 1.0, tone), 0)
            cuts += [p for p in _runs_w(P, w, spec['min_gap']) if p is not None]
        g = vis.difference(unary_union(cuts)) if cuts else vis
        g = g.buffer(-spec['min_line'] / 2).buffer(spec['min_line'] / 2).intersection(vis)
        out.append(drop_specks(g, spec['min_line']))
    return out
FoldRibbon.engrave = _fr_engrave

def _runs_w(P, w, wmin):
    ok = w >= wmin * 0.999; out = []; i = 0
    while i < len(w):
        if not ok[i]: i += 1; continue
        j = i
        while j < len(w) and ok[j]: j += 1
        if j - i > 3: out.append(ribbon_poly(P[i:j], w[i:j], taper=1.0))
        i = j
    return out

def drop_specks(g, min_line):
    """remove fragments too small to hold (foil or ink): anything under about four times the minimum line squared"""
    from shapely.geometry import MultiPolygon
    parts = [g] if isinstance(g, Polygon) else list(getattr(g, 'geoms', []))
    keep = [p for p in parts if isinstance(p, Polygon) and p.area > 4 * min_line * min_line]
    return unary_union(keep) if keep else Polygon()
