// 100 g pouch labels in the vine system: Natural Vanilla Tea and Vanilla & Cinnamon Tea.
// The arched outline follows the current labels; SIZE is a working size until the real one is confirmed.
// Usage: node tools/label.mjs  ->  export/labels/<name>.svg (+ .pdf via the render step)
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const opentype = require('opentype.js');
const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const font = (f) => opentype.loadSync(path.join(root, 'fonts', f));
const F = { display: font('fraunces-italic.ttf'), sans: font('geist-regular.ttf'), medium: font('geist-medium.ttf') };
const C = { ink: '#143A1D', soft: '#5C6F5F', line: '#143A1D' };
const n = (v, d = 3) => Math.round(v * 10 ** d) / 10 ** d;

const SIZE = { w: 70, h: 100, shoulder: 13 };   // mm; arch rises from the shoulders to the top edge
const BLEED = 3;

function width(f, s, sz, track = 0) {
  const g = f.stringToGlyphs(s), k = sz / f.unitsPerEm;
  return g.reduce((w, gl, i) => w + gl.advanceWidth * k + (i < g.length - 1 ? f.getKerningValue(gl, g[i + 1]) * k + track * sz : 0), 0);
}
function text(key, s, sz, x, y, o = {}) {
  const f = F[key], str = o.caps ? s.toUpperCase() : s, g = f.stringToGlyphs(str), k = sz / f.unitsPerEm;
  const w = width(f, str, sz, o.track || 0);
  let cx = o.anchor === 'end' ? x - w : o.anchor === 'middle' ? x - w / 2 : x, d = '';
  g.forEach((gl, i) => { d += gl.getPath(cx, y, sz).toPathData(3); cx += gl.advanceWidth * k + (i < g.length - 1 ? f.getKerningValue(gl, g[i + 1]) * k + (o.track || 0) * sz : 0); });
  return d ? `<path d="${d}" fill="${o.fill || C.ink}"/>` : '';
}
const label = (s, x, y, o = {}) => text('medium', s, o.size || 1.9, x, y, { caps: true, track: 0.14, ...o });
const svgMark = (f) => { const s = fs.readFileSync(path.join(root, 'brand', f), 'utf8'); return { vw: Number(s.match(/viewBox="0 0 ([\d.]+) ([\d.]+)/)[1]), vh: Number(s.match(/viewBox="0 0 [\d.]+ ([\d.]+)/)[1]), d: s.match(/ d="([^"]+)"/)[1] }; };
const LOGO = svgMark('vanilla-shop-logo.svg');
const logo = (x, y, w) => `<path fill="${C.ink}" fill-rule="evenodd" d="${LOGO.d}" transform="translate(${n(x)} ${n(y)}) scale(${n(w / LOGO.vw, 6)})"/>`;
const img = (f, x, y, w, h) => {
  const b = fs.readFileSync(path.join(root, 'plates', 'generated', f));
  const type = f.endsWith('.png') ? 'png' : 'jpeg';
  return `<image xlink:href="data:image/${type};base64,${b.toString('base64')}" x="${n(x)}" y="${n(y)}" width="${n(w)}" height="${n(h)}" preserveAspectRatio="none"/>`;
};

function ean13(code, x, y, fill = C.ink) {
  const L = ['0001101', '0011001', '0010011', '0111101', '0100011', '0110001', '0101111', '0111011', '0110111', '0001011'];
  const G = ['0100111', '0110011', '0011011', '0100001', '0011101', '0111001', '0000101', '0010001', '0001001', '0010111'];
  const R = ['1110010', '1100110', '1101100', '1000010', '1011100', '1001110', '1010000', '1000100', '1001000', '1110100'];
  const PARITY = ['LLLLLL', 'LLGLGG', 'LLGGLG', 'LLGGGL', 'LGLLGG', 'LGGLLG', 'LGGGLL', 'LGLGLG', 'LGLGGL', 'LGGLGL'];
  const dg = code.split('').map(Number);
  const check = (10 - dg.slice(0, 12).reduce((a, v, i) => a + v * (i % 2 ? 3 : 1), 0) % 10) % 10;
  if (dg.length !== 13 || check !== dg[12]) throw new Error('Invalid EAN-13: ' + code);
  let bits = '101', guards = [0, 1, 2];
  dg.slice(1, 7).forEach((d, i) => { bits += (PARITY[dg[0]][i] === 'L' ? L : G)[d]; });
  guards.push(bits.length + 1, bits.length + 3); bits += '01010';
  dg.slice(7).forEach((d) => { bits += R[d]; });
  guards.push(bits.length, bits.length + 2); bits += '101';
  const m = 0.264, qz = 11 * m, barH = 18.28, guardExtra = 1.32;
  let d = '';
  for (let i = 0; i < bits.length; i++) {
    if (bits[i] !== '1') continue;
    let j = i; while (bits[j + 1] === '1' && guards.includes(j + 1) === guards.includes(i)) j++;
    const h = barH + (guards.includes(i) ? guardExtra : 0);
    d += `M${n(x + qz + i * m)} ${n(y)}h${n((j - i + 1) * m)}v${n(h)}h${n(-(j - i + 1) * m)}Z`;
    i = j;
  }
  const sz = 2.2, ty = y + barH + 0.35 + sz * 0.72; // digits sit just under the short bars
  const digits = text('sans', code[0], sz, x + qz - 1.6 * m, ty, { anchor: 'end', fill, outline: true }) +
    text('sans', code.slice(1, 7), sz, x + qz + (3 + 21) * m, ty, { anchor: 'middle', fill, track: 0.06, outline: true }) +
    text('sans', code.slice(7), sz, x + qz + (50 + 21) * m, ty, { anchor: 'middle', fill, track: 0.06, outline: true });
  return `<path d="${d}" fill="${fill}"/>${digits}`;
}
const EAN_W = 113 * 0.264;


// Outline: shoulders at SIZE.shoulder, a soft arch to the top edge between them.
const outline = (inset = 0) => {
  const { w, h, shoulder: s } = SIZE, i = inset;
  return `M${n(i)} ${n(h - i)}V${n(s + i)}H${n(5 + i)}C${n(12)} ${n(1 + i)} ${n(w - 12)} ${n(1 + i)} ${n(w - 5 - i)} ${n(s + i)}H${n(w - i)}V${n(h - i)}Z`;
};

const LABELS = {
  'natural-vanilla-tea-100g': { ground: 'v6-label-ground-vanilla.jpg', over: 'Authentic Ceylon', lines: ['Vanilla', 'Tea'], under: 'with Natural Vanilla', gtin: '4796034220243' },
  'vanilla-cinnamon-tea-100g': { ground: 'v6-label-ground-cinnamon.jpg', over: 'Authentic Ceylon', lines: ['Vanilla &', 'Cinnamon Tea'], under: 'Vanilla and cinnamon blended with pure Ceylon tea', gtin: '4796034220250' },
};

function build(p) {
  const { w, h } = SIZE;
  const VINE = { file: 'v6-vine-2x.png', pw: 3808, ph: 1651 };
  const vw = 80, vh = vw * VINE.ph / VINE.pw;                 // the vine, wider than the label, cropped by it
  const sz = Math.min(11, 48 / width(F.display, p.lines[0], 1), 48 / width(F.display, p.lines[1], 1));
  const b1 = 26 + sz * 0.78, b2 = b1 + sz * 0.9;
  const out = [
    img(p.ground, -BLEED, -BLEED, w + 2 * BLEED, h + 2 * BLEED),
    img(VINE.file, 3, 45.5, vw, vh),
    logo(w / 2 - 6, 7.5, 12),
    label(p.over, w / 2, 23.6, { anchor: 'middle' }),
    text('display', p.lines[0], sz, w / 2, b1, { anchor: 'middle' }),
    text('display', p.lines[1], sz, w / 2, b2, { anchor: 'middle' }),
    text('sans', p.under, p.under.length > 30 ? 1.95 : 2.4, w / 2, b2 + 4.6, { anchor: 'middle' }),
  ];
  // Barcode on its own white tile (scanners want a light, even ground); batch fields and weight beside it.
  out.push(`<rect x="2.4" y="${h - 23.6}" width="31.4" height="21.6" rx="1" fill="#FFFFFF"/>`);
  out.push(ean13(p.gtin, 2.6, h - 22.6));
  [['MRP Rs.', 0], ['MFD', 1], ['EXP', 2], ['BTN', 3]].forEach(([k, i]) => {
    const y = h - 15.6 + i * 3.9;
    out.push(label(k, 38, y, { size: 1.7 }));
    out.push(`<path d="M${n(49)} ${n(y + 0.4)}H${n(w - 4)}" stroke="${C.line}" stroke-width="0.14"/>`);
  });
  out.push(text('display', '100 g', 4.6, w - 4, h - 19.6, { anchor: 'end' }));
  return `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="${w + 2 * BLEED}mm" height="${h + 2 * BLEED}mm" viewBox="${-BLEED} ${-BLEED} ${w + 2 * BLEED} ${h + 2 * BLEED}">` +
    `<defs><clipPath id="bleed"><path d="${outline(-BLEED)}"/></clipPath></defs>` +
    `<g id="Artwork" clip-path="url(#bleed)">${out.join('')}</g>` +
    `<path id="Cut_line" d="${outline()}" fill="none" stroke="#E4007C" stroke-width="0.2"/></svg>`;
}

const dir = path.join(root, 'export', 'labels');
fs.mkdirSync(dir, { recursive: true });
for (const [k, p] of Object.entries(LABELS)) fs.writeFileSync(path.join(dir, `${k}.svg`), build(p));
console.log('wrote', Object.keys(LABELS).join(', '));
