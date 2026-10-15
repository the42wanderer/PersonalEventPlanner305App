// Long box (25 bags, about 176 x 84 mm front): two ways to carry the vine design across the wider front.
// A: type on the left half, the vine large on the right.  B: the vine across the whole front, type in its sky.
// Usage: node studies/v5/long-front.mjs  ->  studies/v5/out/long-A.svg, long-B.svg
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const opentype = require('opentype.js');
const root = path.dirname(path.dirname(path.dirname(fileURLToPath(import.meta.url))));
const font = (f) => opentype.loadSync(path.join(root, 'fonts', f));
const F = { display: font('fraunces-italic.ttf'), sans: font('geist-regular.ttf'), medium: font('geist-medium.ttf') };
const INK = '#143A1D', SOFT = '#5C6F5F', M = 9;
const W = 176, H = 84;
const n = (v) => Math.round(v * 1000) / 1000;

function width(f, s, sz, track = 0) {
  const g = f.stringToGlyphs(s), k = sz / f.unitsPerEm;
  return g.reduce((w, gl, i) => w + gl.advanceWidth * k + (i < g.length - 1 ? f.getKerningValue(gl, g[i + 1]) * k + track * sz : 0), 0);
}
function text(f, s, sz, x, y, o = {}) {
  const str = o.caps ? s.toUpperCase() : s, g = f.stringToGlyphs(str), k = sz / f.unitsPerEm;
  let cx = o.anchor === 'end' ? x - width(f, str, sz, o.track || 0) : x, d = '';
  g.forEach((gl, i) => { d += gl.getPath(cx, y, sz).toPathData(3); cx += gl.advanceWidth * k + (i < g.length - 1 ? f.getKerningValue(gl, g[i + 1]) * k + (o.track || 0) * sz : 0); });
  return `<path d="${d}" fill="${o.fill || INK}"/>`;
}
const label = (s, x, y, o = {}) => text(F.medium, s, 2.1, x, y, { caps: true, track: 0.14, ...o });
const svgPath = (f) => { const s = fs.readFileSync(path.join(root, 'brand', f), 'utf8'); return { vw: Number(s.match(/viewBox="0 0 ([\d.]+)/)[1]), d: s.match(/ d="([^"]+)"/)[1] }; };
const LOGO = svgPath('vanilla-shop-logo.svg'), LION = svgPath('ceylon-tea-lion.svg');
const mark = (m, fill, x, y, w) => `<path fill="${fill}" fill-rule="evenodd" d="${m.d}" transform="translate(${n(x)} ${n(y)}) scale(${n(w / m.vw)})"/>`;
const img = (f, x, y, s, pw, ph) => `<image href="file://${path.join(root, 'plates', 'generated', f)}" width="${pw}" height="${ph}" transform="translate(${n(x)} ${n(y)}) scale(${s})"/>`;
const ground = img('v6-ground-golden-strip.jpg', -3, -3, (W + 120) / 4208 * 1.0, 4208, 1089).replace(/scale\(([\d.]+)\)/, () => `scale(${n(350.65 / 4208)} ${n(90.74 / 1089)})`);
const vine = (x, y, s) => img('v6-vine-faded.png', x, y, s, 1904, 826);
const tag = (x, y) => `<g fill="none" stroke="${INK}" stroke-width="0.34" stroke-linejoin="round"><path d="M${n(x + 2)} ${n(y - 3.4)}q-1.6 1.6 0 3.4"/><path d="M${n(x)} ${n(y + 0.9)}l1 -1h2l1 1v4.6h-4Z"/><circle cx="${n(x + 2)}" cy="${n(y + 1)}" r="0.35"/></g>`;
const wrap = (body) => `<svg xmlns="http://www.w3.org/2000/svg" width="${W}mm" height="${H}mm" viewBox="0 0 ${W} ${H}"><clipPath id="c"><rect width="${W}" height="${H}"/></clipPath><g clip-path="url(#c)">${ground}${body}</g></svg>`;

const name = (sz, x, base, lead = 0.88) => [
  label('Authentic Ceylon', x, base - sz * lead - sz * 0.72 - 3.4),
  text(F.display, 'Vanilla', sz, x - 0.6, base - sz * lead),
  text(F.display, 'Tea', sz, x - 0.6, base),
  text(F.sans, 'with Natural Vanilla', 3, x, base + 6),
].join('');
const foot = [tag(M, 76.4), label('25 tea bags · 50 g', M + 6.2, 79.6)].join('');

const A = () => {
  const sz = 48 / width(F.display, 'Vanilla', 1);
  return wrap([vine(30, -2.4, 0.104), mark(LOGO, INK, M, 6, 13), mark(LION, '#9C6F1E', W - M - 12, 7.5, 12), name(sz, M, 54), foot].join(''));
};
const B = () => {
  const sz = 40 / width(F.display, 'Vanilla', 1);
  return wrap([vine(12, -4, 0.128), mark(LOGO, INK, M, 6, 13), mark(LION, '#9C6F1E', W - M - 12, 7.5, 12), name(sz, M, 45.5), foot].join(''));
};

const out = path.join(root, 'studies', 'v5', 'out');
fs.mkdirSync(out, { recursive: true });
fs.writeFileSync(path.join(out, 'long-A.svg'), A());
fs.writeFileSync(path.join(out, 'long-B.svg'), B());
console.log('wrote long-A.svg, long-B.svg');
