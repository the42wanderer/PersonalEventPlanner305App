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
  frauncesBlack: font('fraunces-black-italic.ttf'), frauncesSoft: font('fraunces-display.ttf'),
  frauncesItalic: font('fraunces-italic.ttf'), gloock: font('gloock.ttf'),
  bodoniItalic: font('bodoni-moda-italic.ttf'), bodoni: font('bodoni-moda-bold.ttf'),
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

// Type studies: layout A with the logo and image No. 3; only the product-name face changes.
// Each face is sized so "Vanilla" fills the same 21.5 mm column width.
const typeStudy = (key, leading = 0.88, nudge = 0) => {
  const size = 21.5 / width(F[key], 'Vanilla', 1);
  const base = 73.6;
  return [
    art('gen3.png', W - 1.5, 2.5, 58, 81),
    logo(M, 7, 17.5),
    label('Natural', M, base - size * leading - size * 0.78 - 1.6),
    text(key, 'Vanilla', size, M - 0.3 + nudge, base - size * leading),
    text(key, 'Tea', size, M - 0.3 + nudge, base),
    hair(M, 76.6, 28.5),
    label('12 tea bags \u00B7 24 g', M, 80.2, { fill: C.soft }),
  ].join('');
};
for (const [k, key, lead] of [
  ['fraunces_soft', 'frauncesSoft', 0.9], ['fraunces_black_italic', 'frauncesBlack', 0.9],
  ['fraunces_italic', 'frauncesItalic', 0.9], ['bodoni_italic', 'bodoniItalic', 0.9],
  ['gloock', 'gloock', 0.9], ['bodoni', 'bodoni', 0.9],
]) studies['type_' + k] = () => typeStudy(key, lead);

// v3: bolder, clearer fronts (brief: obviously vanilla + tea, modern, approachable).
const GREEN = '#143A1D', CREAM = '#FEF8E9', SAGE = '#B9C7A2', GOLD = '#B8862B';
const lionSrc = fs.readFileSync(path.join(root, 'brand', 'ceylon-tea-lion.svg'), 'utf8');
const lion = (x, y, w, fill = GOLD) => {
  const vw = Number(lionSrc.match(/viewBox="0 0 ([\d.]+)/)[1]);
  return `<path fill="${fill}" fill-rule="evenodd" d="${lionSrc.match(/ d="([^"]+)"/)[1]}" transform="translate(${n(x)} ${n(y)}) scale(${n(w / vw, 6)})"/>`;
};
function plantImg(x, y, h) {
  const b = fs.readFileSync(path.join(root, 'plates', 'generated', 'v2-vanilla-tea.png'));
  const pw = b.readUInt32BE(16), ph = b.readUInt32BE(20), s = h / ph;
  return { svg: `<image href="data:image/png;base64,${b.toString('base64')}" width="${pw}" height="${ph}" transform="translate(${n(x)} ${n(y)}) scale(${n(s, 6)})"/>`, w: pw * s };
}
function hillsImg(x, y, w) {
  const b = fs.readFileSync(path.join(root, 'plates', 'generated', 'v3-hills-tile.jpg'));
  const sof = b.indexOf(Buffer.from([0xFF, 0xC0])), iw = b.readUInt16BE(sof + 7), ih = b.readUInt16BE(sof + 5);
  return { svg: `<image href="data:image/jpeg;base64,${b.toString('base64')}" width="${iw}" height="${ih}" preserveAspectRatio="none" transform="translate(${n(x)} ${n(y)}) scale(${n(w / iw, 6)})"/>`, h: w * ih / iw };
}
// Compact tea-tag icon, vertically centred on a label baseline y.
const tagIcon = (x, y, c) => `<g fill="none" stroke="${c}" stroke-width="0.28" stroke-linejoin="round"><path d="M${n(x)} ${n(y - 2.1)}l0.8 -0.8h1.6l0.8 0.8v3.5h-3.2Z"/><circle cx="${n(x + 1.6)}" cy="${n(y - 2)}" r="0.3"/></g>`;
const nameBlock = (x, base, sz, fill, sub) => [
  label('Authentic Ceylon', x, base - sz * 0.92 - sz * 0.72 - 2.6, { fill: sub }),
  text('frauncesItalic', 'Vanilla', sz, x - 0.4, base - sz * 0.92, { fill }),
  text('frauncesItalic', 'Tea', sz, x - 0.4, base, { fill }),
  text('sans', 'with Natural Vanilla', 2.3, x, base + 4.6, { fill: sub }),
].join('');

// A: cream top with the plant; a green band whose top edge is the tea hills; pod hangs into it.
studies.v3_band = () => {
  const plant = plantImg(0, 0, 0);
  const ph = 74, p = plantImg(W + 9 - 1000 * (74 / 1485), 1.5, ph);
  const hills = hillsImg(-4, 0, W + 8);
  const hy = 35.5, solid = hy + hills.h * 0.8;
  const sz = 28 / width(F.frauncesItalic, 'Vanilla', 1);
  return [
    hills.svg.replace('translate(-4 0)', `translate(-4 ${hy})`),
    `<linearGradient id="bandfade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${GREEN}" stop-opacity="0"/><stop offset="1" stop-color="${GREEN}"/></linearGradient>`,
    `<rect x="-5" y="${n(hy + hills.h * 0.35)}" width="${W + 10}" height="${n(solid - hy - hills.h * 0.35 + 0.2)}" fill="url(#bandfade)"/>`,
    `<rect x="-5" y="${n(solid)}" width="${W + 10}" height="${n(H - solid + 5)}" fill="${GREEN}"/>`,
    p.svg,
    logo(M, 7, 17.5),
    lion(M, 29.5, 8.5),
    nameBlock(M, 71, sz, CREAM, SAGE),
    tagIcon(M, 81, CREAM),
    label('12 tea bags · 24 g', M + 4.6, 81, { fill: CREAM }),
  ].join('');
};

// B: full green box, the plant on dark ground, big cream name.
studies.v3_green = () => {
  const ph = 80, p = plantImg(W + 8 - 1000 * (80 / 1485), 2.5, ph);
  const sz = 30 / width(F.frauncesItalic, 'Vanilla', 1);
  return [
    `<rect x="-5" y="-5" width="${W + 10}" height="${H + 10}" fill="${GREEN}"/>`,
    p.svg,
    logo(M, 7, 17.5, CREAM),
    lion(M, 29.5, 8.5),
    nameBlock(M, 70, sz, CREAM, SAGE),
    tagIcon(M, 80.5, CREAM),
    label('12 tea bags · 24 g', M + 4.6, 80.5, { fill: CREAM }),
  ].join('');
};

const out = path.join(root, 'studies', 'out');
fs.mkdirSync(out, { recursive: true });
for (const [k, fn] of Object.entries(studies)) fs.writeFileSync(path.join(out, `front_${k}.svg`), svg(fn()));
console.log('wrote', Object.keys(studies).join(', '));
