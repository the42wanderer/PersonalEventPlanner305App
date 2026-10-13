// Front-panel layout studies. Renders each study to SVG (mm units, type outlined).
// Usage: node studies/front-studies.mjs  ->  studies/out/*.svg
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const opentype = require('opentype.js');
const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const font = (f) => opentype.loadSync(path.join(root, 'fonts', f));
const F = {
  serif: font('instrument-serif.ttf'), italic: font('instrument-serif-italic.ttf'),
  sans: font('geist-regular.ttf'), medium: font('geist-medium.ttf'),
};

// Front panel, fold to fold (mm), measured from the supplied dieline.
const W = 87.66, H = 84.74, M = 7;
const C = { paper: '#FEF8E9', ink: '#143A1D', soft: '#5C6F5F', rule: '#143A1D' };

const n = (v, d = 3) => Math.round(v * 10 ** d) / 10 ** d;
function width(f, s, size, track = 0) {
  const g = f.stringToGlyphs(s), k = size / f.unitsPerEm;
  return g.reduce((w, gl, i) => w + gl.advanceWidth * k + (i < g.length - 1 ? f.getKerningValue(gl, g[i + 1]) * k + track * size : 0), 0);
}
function text(key, s, size, x, y, o = {}) {
  const f = F[key], g = f.stringToGlyphs(o.caps ? s.toUpperCase() : s), k = size / f.unitsPerEm;
  const w = width(f, o.caps ? s.toUpperCase() : s, size, o.track || 0);
  let cx = o.anchor === 'end' ? x - w : o.anchor === 'middle' ? x - w / 2 : x, d = '';
  g.forEach((gl, i) => {
    d += gl.getPath(cx, y, size).toPathData(3);
    cx += gl.advanceWidth * k + (i < g.length - 1 ? f.getKerningValue(gl, g[i + 1]) * k + (o.track || 0) * size : 0);
  });
  return `<path d="${d}" fill="${o.fill || C.ink}"${o.transform ? ` transform="${o.transform}"` : ''}/>`;
}
const hair = (x1, y, x2) => `<path d="M${n(x1)} ${n(y)}H${n(x2)}" stroke="${C.rule}" stroke-width="0.18"/>`;

const plateFile = path.join(root, 'plates', 'de-alwis-vanilla.png');
const jpg = fs.readFileSync(plateFile);
const PW = 912, PH = 1190; // plate pixels
const href = 'data:image/png;base64,' + jpg.toString('base64');
// Plate placed `w` mm wide at x, y; optional crop in plate fractions [x0, y0, x1, y1].
function plate(x, y, w, crop = [0, 0, 1, 1]) {
  const s = w / ((crop[2] - crop[0]) * PW);
  return `<image href="${href}" width="${PW}" height="${PH}" preserveAspectRatio="none" transform="translate(${n(x)} ${n(y)}) scale(${n(s, 6)}) translate(${n(-crop[0] * PW)} ${n(-crop[1] * PH)})"/>`;
}

const svg = (body) => `<svg xmlns="http://www.w3.org/2000/svg" width="${W}mm" height="${H}mm" viewBox="0 0 ${W} ${H}">` +
  `<defs><clipPath id="p"><rect width="${W}" height="${H}"/></clipPath></defs>` +
  `<g clip-path="url(#p)"><rect x="-5" y="-5" width="${W + 10}" height="${H + 10}" fill="${C.paper}"/>${body}</g></svg>`;

const label = (s, x, y, o = {}) => text('medium', s, 1.95, x, y, { caps: true, track: 0.14, ...o });

const studies = {
  // A: a narrow type column on the left, the painting running off the right edge onto the side.
  a_column: () => [
    plate(32, 1.5, 62),
    text('italic', 'The Vanilla Shop', 3.3, M, 12.5),
    text('sans', 'Painted in Ceylon by George De Alwis', 1.6, 0, 0, { fill: C.soft, transform: `translate(${M + 1.2} 49) rotate(-90)` }),
    label('Natural', M, 55.5),
    text('serif', 'Vanilla', 9.6, M - 0.3, 65.2),
    text('serif', 'Tea', 9.6, M - 0.3, 73.6),
    hair(M, 76.6, 28.5),
    label('12 tea bags \u00B7 24 g', M, 80.2, { fill: C.soft }),
  ].join(''),

  // B: specimen plate: the painting in a centred window, the name set beneath it.
  b_specimen: () => [
    label('The Vanilla Shop', W / 2, 10.5, { anchor: 'middle' }),
    plate(W / 2 - 22, 13, 44, [0.04, 0, 1, 0.84]),
    text('serif', 'Vanilla Tea', 9.6, W / 2, 73.2, { anchor: 'middle' }),
    label('Natural · 12 tea bags · 24 g', W / 2, 79.6, { anchor: 'middle', fill: C.soft }),
  ].join(''),

  // C: the painting large and cropped tight on the flowers; name small and confident top-left.
  c_close: () => [
    plate(-6, -16, 118, [0, 0, 1, 1]),
    text('italic', 'The Vanilla Shop', 3.9, M, 12.5),
    label('Natural', M, 66.5),
    text('serif', 'Vanilla Tea', 10.2, M - 0.4, 76.5),
    label('12 tea bags · 24 g', W - M, 76.5, { anchor: 'end', fill: C.soft }),
  ].join(''),
};

// Generated illustrations (trimmed cut-outs from tools/cutout.py), placed in layout A.
function pngSize(b) { return { w: b.readUInt32BE(16), h: b.readUInt32BE(20) }; }
function art(file, right, top, maxW, maxH) {
  const b = fs.readFileSync(path.join(root, 'plates', 'generated', file));
  const { w, h } = pngSize(b);
  const s = Math.min(maxW / w, maxH / h);
  return `<image href="data:image/png;base64,${b.toString('base64')}" width="${w}" height="${h}" transform="translate(${n(right - w * s)} ${n(top)}) scale(${n(s, 6)})"/>`;
}
const columnA = (image, caption) => [
  image,
  text('italic', 'The Vanilla Shop', 3.3, M, 12.5),
  text('sans', caption, 1.6, 0, 0, { fill: C.soft, transform: `translate(${M + 1.2} 49) rotate(-90)` }),
  label('Natural', M, 55.5),
  text('serif', 'Vanilla', 9.6, M - 0.3, 65.2),
  text('serif', 'Tea', 9.6, M - 0.3, 73.6),
  hair(M, 76.6, 28.5),
  label('12 tea bags \u00B7 24 g', M, 80.2, { fill: C.soft }),
].join('');
studies.gen1 = () => columnA(art('gen1-watercolour.png', W - 2, 3, 58, 80), 'Vanilla planifolia');
studies.gen2 = () => columnA(art('gen2.png', W - 1.5, 2.5, 58, 81), 'Vanilla planifolia');
studies.gen3 = () => columnA(art('gen3.png', W - 1.5, 2.5, 58, 81), 'Vanilla planifolia');

// Official logo (traced to vector by tools/trace_logo.py), recoloured to the brand ink.
function logo(x, y, w, fill = C.ink) {
  const src = fs.readFileSync(path.join(root, 'brand', 'vanilla-shop-logo.svg'), 'utf8');
  const [, vw, vh] = src.match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/).map(Number);
  const d = src.match(/ d="([^"]+)"/)[1];
  return `<path fill="${fill}" fill-rule="evenodd" d="${d}" transform="translate(${n(x)} ${n(y)}) scale(${n(w / vw, 6)})"/>`;
}
const columnLogo = (image, logoW = 17.5) => [
  image,
  logo(M, 7, logoW),
  label('Natural', M, 55.5),
  text('serif', 'Vanilla', 9.6, M - 0.3, 65.2),
  text('serif', 'Tea', 9.6, M - 0.3, 73.6),
  hair(M, 76.6, 28.5),
  label('12 tea bags \u00B7 24 g', M, 80.2, { fill: C.soft }),
].join('');
studies.logo_gen3 = () => columnLogo(art('gen3.png', W - 1.5, 2.5, 58, 81));
studies.logo_gen1 = () => columnLogo(art('gen1-watercolour.png', W - 2, 3, 58, 80));
studies.logo_gen2 = () => columnLogo(art('gen2.png', W - 1.5, 2.5, 58, 81));

const out = path.join(root, 'studies', 'out');
fs.mkdirSync(out, { recursive: true });
for (const [k, fn] of Object.entries(studies)) fs.writeFileSync(path.join(out, `front_${k}.svg`), svg(fn()));
console.log('wrote', Object.keys(studies).join(', '));
