# Copperplate-style engraving as vector, for foil and print separations.
#
# Every element is a parametric surface S(u, v) -> (x, y, z) on the page (mm, y down, z towards the viewer). Its
# normal, lit from the upper left, gives a darkness at every point; hatch lines follow the form (along a petal, round a
# pod, from the midrib of a leaf), swelling where it is dark, tapering and breaking where it is light, and crossed by a
# second family in the deepest shadow. Outlines thicken on the side away from the light. Forms are drawn back to front;
# each is cut back by the silhouettes in front of it plus a hairline gap, as an engraver separates overlapping forms.
# Everything comes out as filled polygons (shapely), so it separates cleanly into print and foil.
import numpy as np
from shapely.geometry import Polygon, MultiPolygon, Point, LineString
from shapely.ops import unary_union

LIGHT = np.array([-0.55, -0.72, 0.70]); LIGHT /= np.linalg.norm(LIGHT)
SHADOW2D = -LIGHT[:2] / np.linalg.norm(LIGHT[:2])          # the page direction away from the light

def smooth(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1); return t * t * (3 - 2 * t)

def catmull(pts, n=200):
    """a smooth curve through pts (Catmull-Rom, centripetal enough for drawing)"""
    P = np.asarray(pts, float); P = np.vstack([2 * P[0] - P[1], P, 2 * P[-1] - P[-2]]); out = []
    seg = len(P) - 3
    for i in range(seg):
        p0, p1, p2, p3 = P[i:i + 4]
        for t in np.linspace(0, 1, max(2, n // seg), endpoint=(i == seg - 1)):
            t2, t3 = t * t, t * t * t
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    return np.array(out)

def resample(c, n):
    d = np.r_[0, np.cumsum(np.linalg.norm(np.diff(c, axis=0), axis=1))]; s = np.linspace(0, d[-1], n)
    return np.stack([np.interp(s, d, c[:, 0]), np.interp(s, d, c[:, 1])], 1)

def frames(c):
    t = np.gradient(c, axis=0); t /= np.linalg.norm(t, axis=1, keepdims=True) + 1e-12
    return t, np.stack([-t[:, 1], t[:, 0]], 1)

def ribbon_poly(pts, w, taper=0.25):
    """a stroke of varying width as a polygon; widths taper to points at the ends over `taper` mm"""
    pts = np.asarray(pts, float); w = np.asarray(w, float).copy()
    if len(pts) < 2: return None
    seg = np.r_[0, np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))]
    if seg[-1] < 0.05: return None
    w *= np.minimum(1, np.minimum(seg, seg[-1] - seg) / taper + 0.15)
    _, nrm = frames(pts)
    L = pts + nrm * (w / 2)[:, None]; R = pts - nrm * (w / 2)[:, None]
    p = Polygon(np.vstack([L, R[::-1]]))
    return p if p.is_valid else p.buffer(0)

def strokes_from(pts, w, wcut=0.045, taper=0.3):
    """split a line where it is too light to cut, and turn each run into a polygon"""
    on = w >= wcut; out = []; i = 0; n = len(w)
    while i < n:
        if not on[i]: i += 1; continue
        j = i
        while j < n and on[j]: j += 1
        if j - i >= 2:
            p = ribbon_poly(pts[i:j], w[i:j], taper)
            if p is not None and not p.is_empty: out.append(p)
        i = j
    return out

class Surface:
    """S(u, v) on [0,1] x [-1,1]; subclasses set S and the hatch families. Darkness d in [0,1] from the normal, plus
    any extra shade (occlusion near a base, a throat) the subclass adds in `shade`."""
    spacing = 0.52; wmax = 0.30; gamma = 1.1; d0 = 0.16; cross_at = 0.70
    contour_w = (0.16, 0.42)
    def S(self, u, v): raise NotImplementedError
    def shade(self, u, v): return 0.0
    def normal(self, u, v, e=1e-3):
        su = (self.S(u + e, v) - self.S(u - e, v)) / (2 * e); sv = (self.S(u, v + e) - self.S(u, v - e)) / (2 * e)
        N = np.cross(su, sv); N /= np.linalg.norm(N, axis=-1, keepdims=True) + 1e-12
        return np.where(N[..., 2:3] < 0, -N, N)
    def dark(self, u, v):
        # tone: a surface facing the viewer is a light mid-tone (0.42); turned to the light it clears to a highlight,
        # turned away it darkens. (N.L - Lz) is 0 when facing the viewer.
        N = self.normal(u, v)
        return np.clip(0.42 - 1.15 * (N @ LIGHT - LIGHT[2]) + self.shade(u, v), 0, 1)
    def width(self, d, wmax=None):
        wm = self.wmax if wmax is None else wmax
        return (0.06 + (wm - 0.06) * smooth(self.d0, 1.0, d) ** self.gamma) * (d > self.d0)
    def boundary(self, n=160):
        u = np.linspace(0, 1, n)
        a = self.S(u, np.full(n, -1.0)); b = self.S(u[::-1], np.full(n, 1.0))
        return np.vstack([a[:, :2], b[:, :2]])
    def outline(self):
        p = Polygon(self.boundary()); return p if p.is_valid else p.buffer(0)
    def families(self):
        """param-space polylines (k, t) -> (u, v) arrays; override"""
        return []
    def cross_families(self): return []
    def hatch(self):
        out = []
        for fam, cross in ((self.families(), False), (self.cross_families(), True)):
            for uv in fam:
                u, v = uv[:, 0], uv[:, 1]; P = self.S(u, v)[:, :2]; d = self.dark(u, v)
                w = self.width(d) if not cross else self.width(smooth(self.cross_at, 1, d) * 0.9 + 0.1 * (d > self.cross_at), self.wmax * 0.7) * (d > self.cross_at)
                out += strokes_from(P, w)
        return out
    def contour(self):
        B = self.boundary(); B = np.vstack([B, B[:1]])
        t, nrm = frames(B)
        # outward normal: the boundary runs round the shape; orient by the signed area
        area = 0.5 * np.sum(B[:-1, 0] * B[1:, 1] - B[1:, 0] * B[:-1, 1]); out = nrm * (1 if area < 0 else -1)
        k = np.clip(out @ SHADOW2D, 0, 1)
        w = self.contour_w[0] + (self.contour_w[1] - self.contour_w[0]) * k ** 1.2
        p = ribbon_poly(B, w, taper=0.01)
        return [p] if p is not None else []

def _arc_steps(fn, a0, a1, spacing, probe=0.0, n=400):
    """parameter values along a1..a0 so that consecutive lines are `spacing` mm apart, measured along fn(a) (page xy)"""
    a = np.linspace(a0, a1, n); P = fn(a, probe)[:, :2]
    s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))]
    k = np.arange(spacing * 0.5, s[-1], spacing)
    return np.interp(k, s, a)

class Leaf(Surface):
    """a vanilla leaf: thick, elliptic with a short point, smooth margin, folded a little along the midrib and curled
    along its length. base (x,y), direction (deg), length, width, bow (fraction of L, + = to the left of travel)"""
    def __init__(self, base, ang, L, W, bow=0.08, fold=0.10, curl=0.18, tilt=0.0):
        self.b = np.array(base, float); a = np.radians(ang); self.d = np.array([np.cos(a), np.sin(a)]); self.n = np.array([-self.d[1], self.d[0]])
        self.L, self.W, self.bow, self.fold, self.curl, self.tilt = L, W, bow, fold, curl, tilt
    def hw(self, u):
        return self.W / 2 * np.sin(np.pi * np.clip(u, 0, 1) ** 0.85) ** 0.62 * (1 - 0.18 * u)
    def S(self, u, v):
        u = np.asarray(u, float); v = np.asarray(v, float)
        mid = self.b + np.outer(u * self.L, self.d) + np.outer(self.bow * self.L * np.sin(np.pi * u), self.n)
        tdir = self.d + np.outer(self.bow * np.pi * np.cos(np.pi * u), self.n) / 1.0
        tdir /= np.linalg.norm(tdir, axis=-1, keepdims=True); nn = np.stack([-tdir[:, 1], tdir[:, 0]], 1)
        h = self.hw(u); xy = mid + nn * (v * h)[:, None]
        z = -self.fold * np.abs(v) * h + self.curl * self.L * 0.25 * np.sin(np.pi * u) + self.tilt * v * h
        return np.column_stack([xy, z])
    def shade(self, u, v):
        return 0.08 * (1 - u) + 0.10 * np.exp(-np.abs(v) / 0.10) - 0.12 * smooth(0.8, 1, np.abs(v)) + 0.02 * np.sign(v)
    def families(self):
        out = []; a = 0.20
        for s in (1, -1):
            for u0 in _arc_steps(lambda uu, p: self.S(uu, np.full_like(uu, s * 0.5)), -0.25, 0.98, self.spacing * 1.05, n=300):
                t = np.linspace(0.04, 0.97, 30); u = np.clip(u0 + a * t, 0.015, 0.985); v = s * t
                out.append(np.column_stack([u, v]))
        return out
    def cross_families(self):
        out = []
        for vk in np.arange(-0.92, 0.93, 0.085):
            u = np.linspace(0.05, 0.95, 60); out.append(np.column_stack([u, np.full_like(u, vk)]))
        return out
    def midrib(self):
        u = np.linspace(0.02, 0.9, 80); P = self.S(u, np.zeros_like(u))[:, :2]
        return [ribbon_poly(P, 0.32 * (1 - u) + 0.06)]

class Petal(Surface):
    """an orchid tepal: from a centre, narrow-oblong with a soft point, cupped across and twisted a little"""
    spacing = 0.50; d0 = 0.20
    def __init__(self, c, ang, L, W, bend=0.1, cup=0.5, twist=0.3):
        self.c = np.array(c, float); a = np.radians(ang); self.d = np.array([np.cos(a), np.sin(a)]); self.n = np.array([-self.d[1], self.d[0]])
        self.L, self.W, self.bend, self.cup, self.twist = L, W, bend, cup, twist
    def hw(self, u):
        return self.W / 2 * (np.sin(np.pi * np.clip(0.08 + 0.92 * u, 0, 1) ** 0.8) ** 0.7) * (0.55 + 0.45 * smooth(0, 0.3, u))
    def S(self, u, v):
        u = np.asarray(u, float); v = np.asarray(v, float)
        mid = self.c + np.outer(u * self.L, self.d) + np.outer(self.bend * self.L * u * u, self.n)
        h = self.hw(u); ph = self.twist * u
        xy = mid + np.outer(v * h * np.cos(ph), self.n)
        z = self.cup * h * (1 - v * v) + v * h * np.sin(ph) + 2.0 * (1 - u)
        return np.column_stack([xy, z])
    def shade(self, u, v):
        return 0.30 * np.exp(-u / 0.16) + 0.05 * v
    def families(self):
        out = []
        for vk in _arc_steps(lambda vv, p: self.S(np.full_like(vv, 0.45), vv), -0.97, 0.97, self.spacing):
            u = np.linspace(0.0, 0.97, 50); v = np.full_like(u, vk) * (0.35 + 0.65 * smooth(0, 0.35, u))
            out.append(np.column_stack([u, v]))
        return out
    def cross_families(self):
        out = []
        for uk in _arc_steps(lambda uu, p: self.S(uu, np.zeros_like(uu)), 0.02, 0.6, self.spacing * 1.2, n=400):
            v = np.linspace(-0.95, 0.95, 30); out.append(np.column_stack([np.full_like(v, uk), v]))
        return out

class Tube(Surface):
    """a round body along a curve: stem, vine or vanilla pod. r(u) radius profile; rings round it, optional ridges"""
    spacing = 0.50; d0 = 0.18
    def __init__(self, pts, r, ridges=0, n=240, ring=True, rprofile=None, lengthwise=False):
        self.c = resample(catmull(pts, n * 2), n); self.t, self.nn = frames(self.c)
        s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(self.c, axis=0), axis=1))]; self.s = s / s[-1]; self.len = s[-1]
        self.r0 = r; self.ridges = ridges; self.ring = ring and not lengthwise; self.lengthwise = lengthwise
        self.rp = rprofile or (lambda u: np.ones_like(u))
    def _at(self, u):
        u = np.clip(np.asarray(u, float), 0, 1)
        c = np.stack([np.interp(u, self.s, self.c[:, k]) for k in (0, 1)], -1)
        nn = np.stack([np.interp(u, self.s, self.nn[:, k]) for k in (0, 1)], -1); nn /= np.linalg.norm(nn, axis=-1, keepdims=True) + 1e-12
        t = np.stack([nn[..., 1], -nn[..., 0]], -1)
        return c, nn, t
    def S(self, u, v):
        u = np.asarray(u, float); v = np.clip(np.asarray(v, float), -1, 1)
        c, nn, t = self._at(u); r = self.r0 * self.rp(u)
        th = np.arcsin(v); xy = c + nn * (r * v)[..., None] + t * (r * (1 - np.cos(th)) * 0.18)[..., None]
        return np.concatenate([xy, (r * np.cos(th))[..., None]], -1)
    def families(self):
        out = []
        if self.ring:
            for uk in _arc_steps(lambda uu, p: self.S(uu, np.zeros_like(uu)), 0, 1, self.spacing, n=900):
                v = np.linspace(-0.99, 0.99, 24); out.append(np.column_stack([np.full_like(v, uk), v]))
        for vk in np.linspace(-0.7, 0.7, self.ridges) if self.ridges else []:
            u = np.linspace(0.02, 0.98, 200); out.append(np.column_stack([u, np.full_like(u, vk)]))
        if self.lengthwise:                                   # lines along the body, spaced across its widest girth
            n = max(3, int(1.9 * self.r0 / self.spacing))
            for vk in np.sin(np.linspace(-1.35, 1.35, n)):
                u = np.linspace(0.0, 1.0, 400); out.append(np.column_stack([u, np.full_like(u, vk)]))
        return out
    def cross_families(self):
        out = []
        if self.lengthwise:                                   # rings across the darkest side only
            for uk in _arc_steps(lambda uu, p: self.S(uu, np.zeros_like(uu)), 0, 1, self.spacing * 1.15, n=900):
                v = np.linspace(-0.99, 0.99, 24); out.append(np.column_stack([np.full_like(v, uk), v]))
            return out
        for vk in np.arange(0.15, 0.99, 0.16):
            u = np.linspace(0.0, 1.0, 200); out.append(np.column_stack([u, np.full_like(u, vk)]))
        return out

class Bell(Surface):
    """the vanilla orchid's lip: a trumpet from the flower's heart towards the viewer and down, flaring to a frilled
    mouth. Its outer, visible half is engraved with rings parallel to the mouth; the open mouth is drawn by Throat."""
    spacing = 0.46; d0 = 0.16
    def __init__(self, base, axis, length, r0, r1, frill=0.08, lobes=9):
        self.b = np.array(base, float); a = np.array(axis, float); self.a = a / np.linalg.norm(a)
        self.e1 = np.cross(self.a, [0, 0, 1.0]); self.e1 /= np.linalg.norm(self.e1); self.e2 = np.cross(self.a, self.e1)
        self.L, self.r0, self.r1, self.frill, self.lobes = length, r0, r1, frill, lobes
    def r(self, u, th):
        return (self.r0 + (self.r1 - self.r0) * np.clip(u, 0, 1) ** 1.9) * (1 + self.frill * smooth(0.75, 1, u) * np.sin(self.lobes * th))
    def P3(self, u, th):
        u = np.asarray(u, float); th = np.asarray(th, float)
        c = self.b[None] + np.outer(u * self.L, self.a) if u.ndim else self.b + u * self.L * self.a
        rr = self.r(u, th)
        return c + (rr * np.cos(th))[..., None] * self.e1 + (rr * np.sin(th))[..., None] * self.e2
    def S(self, u, v):
        # the half facing the viewer: theta round the side whose normal points to +z
        th = np.asarray(v, float) * np.pi / 2 + self._th0
        return self.P3(u, th)
    @property
    def _th0(self):
        # the angle whose radial direction points most towards the viewer
        return np.arctan2(self.e2[2], self.e1[2])
    def shade(self, u, v): return 0.12 * (1 - u)
    def families(self):
        out = []
        for uk in _arc_steps(lambda uu, p: self.S(uu, np.zeros_like(uu)), 0.0, 0.985, self.spacing, n=600):
            v = np.linspace(-0.98, 0.98, 60); out.append(np.column_stack([np.full_like(v, uk), v]))
        return out
    def rim(self, n=360):
        th = np.linspace(0, 2 * np.pi, n); return self.P3(np.ones_like(th), th)
    def boundary(self, n=160):
        u = np.linspace(0, 1, n); a = self.S(u, np.full(n, -1.0)); b = self.S(u[::-1], np.full(n, 1.0))
        rim = self.rim()[:, :2]
        return np.vstack([a[:, :2], b[:, :2]])
    def outline(self):
        body = Polygon(self.boundary()).buffer(0); mouth = Polygon(self.rim()[:, :2]).buffer(0)
        return unary_union([body, mouth])
    def throat(self):
        """the open mouth: radial strokes from its centre, dark within, lighter towards the frilled rim"""
        R = self.rim(); c = R[:, :2].mean(0); out = []
        for i in range(0, len(R), 3):
            p = R[i, :2]; t = np.linspace(0, 1, 30); P = c + np.outer(t, p - c)
            w = 0.05 + 0.22 * (1 - smooth(0.55, 1, t)) * (0.6 + 0.4 * np.cos(np.arctan2(*(p - c)[::-1]) + 2.4))
            out += strokes_from(P, w)
        return out
    def contour(self):
        out = super().contour(); R = self.rim()[:, :2]; R = np.vstack([R, R[:1]])
        out.append(ribbon_poly(R, np.full(len(R), 0.26), taper=0.01)); return [p for p in out if p is not None]

class Band(Surface):
    """a ribbon: a band along a curve, twisting about it by phi(u); lengthwise lines"""
    spacing = 0.46; d0 = 0.16; wmax = 0.28
    def __init__(self, pts, width, phis, n=300):
        self.c = resample(catmull(pts, n * 2), n); self.t, self.nn = frames(self.c)
        s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(self.c, axis=0), axis=1))]; self.s = s / s[-1]
        self.w = width; ph = np.asarray(phis, float); self.phi = lambda u: np.interp(u, np.linspace(0, 1, len(ph)), ph)
    def S(self, u, v):
        u = np.clip(np.asarray(u, float), 0, 1); v = np.asarray(v, float)
        c = np.stack([np.interp(u, self.s, self.c[:, k]) for k in (0, 1)], -1)
        nn = np.stack([np.interp(u, self.s, self.nn[:, k]) for k in (0, 1)], -1); nn /= np.linalg.norm(nn, axis=-1, keepdims=True) + 1e-12
        ph = np.radians(self.phi(u)); hw = self.w / 2
        xy = c + nn * (v * hw * np.cos(ph))[..., None]
        return np.concatenate([xy, (v * hw * np.sin(ph))[..., None]], -1)
    def back(self, u):
        return np.cos(np.radians(self.phi(u))) < 0
    def shade(self, u, v):
        return 0.20 * self.back(u) + 0.12 * smooth(0.7, 1, np.abs(v))
    def families(self):
        out = []
        for vk in np.arange(-0.93, 0.94, 2 * self.spacing / self.w):
            u = np.linspace(0, 1, 500); out.append(np.column_stack([u, np.full_like(u, vk)]))
        return out
    def outline(self):
        u = np.linspace(0, 1, 500); quads = []
        A = self.S(u, -np.ones_like(u))[:, :2]; B = self.S(u, np.ones_like(u))[:, :2]
        for i in range(len(u) - 1):
            q = Polygon([A[i], A[i + 1], B[i + 1], B[i]])
            if q.area > 1e-6: quads.append(q.buffer(0.01))
        return unary_union(quads)
    def contour(self):
        u = np.linspace(0, 1, 500); out = []
        for vv in (-1, 1):
            P = self.S(u, np.full_like(u, vv))[:, :2]; _, nrm = frames(P)
            k = np.clip((nrm * vv) @ SHADOW2D, 0, 1)
            out.append(ribbon_poly(P, self.contour_w[0] + 0.18 * k, taper=0.2))
        return [p for p in out if p is not None]

class Berry:
    """a sphere: latitude rings round the axis that faces the light, the highlight left clean"""
    def __init__(self, c, r): self.c = np.array(c, float); self.r = r
    def outline(self): return Point(*self.c).buffer(self.r, 48)
    def hatch(self, spacing=0.46, wmax=0.29):
        out = []; ax = LIGHT
        for h in np.arange(-0.98, 0.9, spacing / self.r):
            # the circle of points on the sphere at height h along the light axis, projected
            th = np.linspace(0, 2 * np.pi, 120)
            e1 = np.cross(ax, [0, 0, 1.0]); e1 /= np.linalg.norm(e1); e2 = np.cross(ax, e1)
            rr = np.sqrt(max(0, 1 - h * h)); P3 = (h * ax)[None] + rr * (np.cos(th)[:, None] * e1 + np.sin(th)[:, None] * e2)
            vis = P3[:, 2] > 0.02
            d = np.clip(0.42 - 1.15 * (P3 @ LIGHT - LIGHT[2]), 0, 1)
            w = (0.06 + (wmax - 0.06) * smooth(0.16, 1, d) ** 1.1) * vis * (d > 0.16)
            out += strokes_from(self.c + P3[:, :2] * self.r, w)
        return out
    def contour(self):
        th = np.linspace(0, 2 * np.pi, 160); P = self.c + self.r * np.column_stack([np.cos(th), np.sin(th)])
        k = np.clip(np.column_stack([np.cos(th), np.sin(th)]) @ SHADOW2D, 0, 1)
        return [ribbon_poly(P, 0.14 + 0.32 * k, taper=0.01)]

def star(c, r, points=4, inner=0.18, rot=0):
    """a sparkle: concave-sided star"""
    out = []
    for i in range(points * 2):
        a = np.radians(rot) + np.pi * i / points; rr = r if i % 2 == 0 else r * inner
        out.append((c[0] + rr * np.sin(a), c[1] - rr * np.cos(a)))
    return Polygon(out)

def to_path(g, nd=3):
    """shapely geometry -> SVG path data (evenodd)"""
    if g is None or g.is_empty: return ''
    polys = [g] if isinstance(g, Polygon) else [p for p in getattr(g, 'geoms', []) if isinstance(p, Polygon)]
    f = lambda x: f'{x:.{nd}f}'
    out = []
    for p in polys:
        for ring in [p.exterior, *p.interiors]:
            c = np.asarray(ring.coords)
            if len(c) < 3: continue
            out.append('M' + 'L'.join(f'{f(x)} {f(y)}' for x, y in c) + 'Z')
    return ''.join(out)
