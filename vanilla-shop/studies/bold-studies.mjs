// Bolder front concepts: one strong idea each, with display type that has character.
// Usage: node studies/bold-studies.mjs  ->  studies/out/bold_*.svg
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const opentype = require('opentype.js');
const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const font = (f) => opentype.loadSync(path.join(root, 'fonts', f));
const F = {
  frauncesBlack: font('fraunces-black-italic.ttf'), gloock: font('gloock.ttf'),
  bodoniItalic: font('bodoni-moda-italic.ttf'), sans: font('geist-regular.ttf'), medium: font('geist-medium.ttf'),
};

const W = 87.66, H = 84.74;
const FOREST = '#143A1D', CREAM = '#FEF8E9', BUTTER = '#F1D98A';
const n = (v, d = 3) => Math.round(v * 10 ** d) / 10 ** d;

function width(f, s, size, track = 0) {
  const g = f.stringToGlyphs(s), k = size / f.unitsPerEm;
  return g.reduce((w, gl, i) => w + gl.advanceWidth * k + (i < g.length - 1 ? f.getKerningValue(gl, g[i + 1]) * k + track * size : 0), 0);
}
function text(key, s, size, x, y, o = {}) {
  const f = F[key], str = o.caps ? s.toUpperCase() : s, g = f.stringToGlyphs(str), k = size / f.unitsPerEm;
  const w = width(f, str, size, o.track || 0);
  let cx = o.anchor === 'end' ? x - w : o.anchor === 'middle' ? x - w / 2 : x, d = '';
  g.forEach((gl, i) => {
    d += gl.getPath(cx, y, size).toPathData(3);
    cx += gl.advanceWidth * k + (i < g.length - 1 ? f.getKerningValue(gl, g[i + 1]) * k + (o.track || 0) * size : 0);
  });
  return `<path d="${d}" fill="${o.fill}"${o.transform ? ` transform="${o.transform}"` : ''}/>`;
}
const label = (s, x, y, fill, o = {}) => text('medium', s, 1.9, x, y, { caps: true, track: 0.14, fill, ...o });

function logo(x, y, w, fill) {
  const src = fs.readFileSync(path.join(root, 'brand', 'vanilla-shop-logo.svg'), 'utf8');
  const vw = Number(src.match(/viewBox="0 0 ([\d.]+)/)[1]);
  const d = src.match(/ d="([^"]+)"/)[1];
  return `<path fill="${fill}" fill-rule="evenodd" d="${d}" transform="translate(${n(x)} ${n(y)}) scale(${n(w / vw, 6)})"/>`;
}

// Illustration placed by height; returns the SVG and its box so other layers can line up with it.
function plant(file, x, y, h, clip) {
  const b = fs.readFileSync(path.join(root, 'plates', 'generated', file));
  const pw = b.readUInt32BE(16), ph = b.readUInt32BE(20), s = h / ph;
  const img = `<image href="data:image/png;base64,${b.toString('base64')}" width="${pw}" height="${ph}" transform="translate(${n(x)} ${n(y)}) scale(${n(s, 6)})"/>`;
  return { svg: img, w: pw * s, h, x, y };
}

// Knockout: draw the artwork first as a thick outline in the background colour, then the
// artwork itself, so anything behind it (roots, leaves) stops cleanly short of it.
const knockout = (markup, bg, w = 1.1) =>
  markup.replace(/fill="[^"]+"/g, `fill="${bg}" stroke="${bg}" stroke-width="${w}" stroke-linejoin="round"`) + markup;

const svg = (bg, body) => `<svg xmlns="http://www.w3.org/2000/svg" width="${W}mm" height="${H}mm" viewBox="0 0 ${W} ${H}">` +
  `<defs><clipPath id="p"><rect width="${W}" height="${H}"/></clipPath></defs>` +
  `<g clip-path="url(#p)"><rect x="-5" y="-5" width="${W + 10}" height="${H + 10}" fill="${bg}"/>${body}</g></svg>`;

const concepts = {
  // 1. Masthead: a giant italic "Vanilla" across the foot of the box, the cured pod hanging in front of it.
  masthead: () => {
    const p = plant('gen3.png', 0, -7, 93);
    p.x = 40.5 - p.w * 0.5; // pod (at 0.5 of the image width) hangs in front of the "n", leaving both stems visible
    const placed = plant('gen3.png', p.x, -7, 93);
    const size = (W + 3) / (width(F.frauncesBlack, 'Vanilla', 1));
    const pod = [p.x + 0.43 * p.w, 50, 0.14 * p.w, 40];
    return svg(FOREST, [
      placed.svg,
      text('frauncesBlack', 'Vanilla', size, -1.6, 80.5, { fill: CREAM }),
      `<clipPath id="pod"><rect x="${n(pod[0])}" y="${pod[1]}" width="${n(pod[2])}" height="${pod[3]}"/></clipPath>`,
      `<g clip-path="url(#pod)">${placed.svg}</g>`,
      knockout(logo(6, 6, 14.5, CREAM) + label('Natural tea', 6, 28.5, CREAM) + label('12 bags · 24 g', 6, 32, '#B9C7A2'), FOREST),
    ].join(''));
  },

  // 2. Spine: the word runs huge up the left edge, cropped by the fold, on a custard-yellow box.
  spine: () => {
    const size = (H + 2) / width(F.gloock, 'Vanilla', 1);
    const p = plant('gen3.png', 0, 10, 76);
    const placed = plant('gen3.png', W + 1.5 - p.w, 10, 76);
    return svg(BUTTER, [
      text('gloock', 'Vanilla', size, 0, 0, { fill: FOREST, transform: `translate(19.2 ${n(H + 1)}) rotate(-90)` }),
      placed.svg,
      logo(24, 4.5, 13, FOREST),
      label('Natural tea', 24, 77.5, FOREST),
      label('12 bags · 24 g', 24, 81, FOREST),
    ].join(''));
  },

  // 3. Statement: the brand's own line, set big in a fashion italic, next to the plant.
  statement: () => {
    const p = plant('gen3.png', 0, 2, 72);
    const placed = plant('gen3.png', W + 0.5 - p.w, 2, 72);
    return svg(CREAM, [
      placed.svg,
      logo(6, 6, 14.5, FOREST),
      text('bodoniItalic', 'Never', 13, 5.4, 57.5, { fill: FOREST }),
      text('bodoniItalic', 'plain.', 13, 5.4, 69.5, { fill: FOREST }),
      `<path d="M6 74.6H32" stroke="${FOREST}" stroke-width="0.2"/>`,
      label('Natural vanilla tea', 6, 78.4, FOREST),
      label('12 bags · 24 g', 6, 81.6, '#5C6F5F'),
    ].join(''));
  },
};

const out = path.join(root, 'studies', 'out');
fs.mkdirSync(out, { recursive: true });
for (const [k, fn] of Object.entries(concepts)) fs.writeFileSync(path.join(out, `bold_${k}.svg`), fn());
console.log('wrote', Object.keys(concepts).join(', '));
