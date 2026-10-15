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

const SIZE = { w: 70, h: 110, shoulder: 8.5 };  // mm, matched to the current label on the kraft pouch; arch rises from the shoulders to the top edge
const BLEED = 3;
// LABEL_GROUND picks the ground: cream (default), golden (the boxes'), or a tools/label_ground.py preset.
const GROUND = process.env.LABEL_GROUND || 'cream';
// Barcode bar height: 18.28 mm is full height at 80%; shortened to fit the label's foot strip.
const BAR_H = 10;

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
  const m = 0.264, qz = 11 * m, barH = BAR_H, guardExtra = 1.32;
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
  'natural-vanilla-tea-100g': { ground: 'v6-label-ground-vanilla.jpg', over: 'Authentic Ceylon', lines: ['Vanilla', 'Tea'], under: 'with Natural Vanilla', gtin: '4796034220243',
    // Upright vine: artwork bbox x 89-930, y 126-1438 px; climbs the right side beside the name.
    art: { file: 'v7-vine-upright.png', pw: 1024, ph: 1536, box: [89, 126, 930, 1438], at: [32, 11.5], height: 77 },
    weightUnder: true,
    deco: [{ at: [-1.5, 9.4], width: 21, flip: true, rotate: -6 }, { at: [-2.5, 66], width: 21, flip: true, rotate: -22 }] },
  'vanilla-cinnamon-tea-100g': { ground: 'v6-label-ground-cinnamon.jpg', over: 'Authentic Ceylon', lines: ['Vanilla &', 'Cinnamon Tea'], under: ['Vanilla and cinnamon blended', 'with pure Ceylon tea'], gtin: '4796034220250',
    // Vanilla pods, orchid and cinnamon quills: artwork bbox x 237-1331, y 263-802 px; across the foot.
    art: { file: 'v7-vanilla-cinnamon.png', pw: 1536, ph: 1024, box: [237, 263, 1331, 802], at: [3, 52.5], width: 66 },
    deco: [{ at: [-1.5, 9.4], width: 19, flip: true, rotate: -6 }, { at: [52.5, 9.4], width: 19, rotate: 6 }] },
};

// Place an artwork by its painted area (box, in source pixels): top-left at `at` (mm), sized by height or width.
function art(a) {
  const [x0, y0, x1, y1] = a.box, s = a.height ? a.height / (y1 - y0) : a.width / (x1 - x0);
  return img(a.file, a.at[0] - x0 * s, a.at[1] - y0 * s, a.pw * s, a.ph * s);
}

// Leaf sprig (v6-sprig.png: leaves span x 223-1447, y 168-927 px, stem cut at the right edge),
// tucked in at a label edge. flip puts the cut stem on the left; rotate turns it about its top-left.
const SPRIG = { file: 'v6-sprig.png', pw: 1448, ph: 1086, box: [223, 168, 1447, 927] };
function sprig(d) {
  const [x0, y0, x1] = SPRIG.box, s = d.width / (x1 - x0);
  const inner = img(SPRIG.file, -x0 * s, -y0 * s, SPRIG.pw * s, SPRIG.ph * s);
  const flip = d.flip ? `translate(${n(d.width)} 0) scale(-1 1)` : '';
  return `<g transform="translate(${n(d.at[0])} ${n(d.at[1])}) rotate(${d.rotate || 0}) ${flip}">${inner}</g>`;
}

function build(p) {
  const { w, h } = SIZE;
  const VINE = { file: 'v6-vine-2x.png', pw: 3808, ph: 1651 };
  // The painting large, bleeding off both sides: flower right of centre, pods running off the left.
  const vw = 128, vh = vw * VINE.ph / VINE.pw;
  const L = 7;                                                    // left text edge
  const sz = Math.min(12.5, 54 / width(F.display, p.lines[0], 1), 54 / width(F.display, p.lines[1], 1));
  const b1 = 27 + sz * 0.74, b2 = b1 + sz * 0.88;
  const out = [
    img(GROUND === 'cream' ? p.ground : p.ground.replace('label-ground-', `label-ground-${GROUND}-`), -BLEED, -BLEED, w + 2 * BLEED, h + 2 * BLEED),
    ...(p.deco || []).map(sprig),
    art(p.art),
    logo(w / 2 - 6.5, 6.5, 13),
    label(p.over, L, 25.2),
    text('display', p.lines[0], sz, L - 0.5, b1),
    text('display', p.lines[1], sz, L - 0.5, b2),
    ...[].concat(p.under).map((u, i) => text('sans', u, 2.2, L, b2 + 5 + i * 3)),
  ];
  // Net weight on the line with "Authentic Ceylon", right-aligned.
  if (p.weightUnder) out.push(text('display', '100 g', 4.6, L, b2 + 13.5));
  else out.push(text('display', '100 g', 4.4, w - L, 25.6, { anchor: 'end' }));
  // Spec card: one compact, outlined panel at the foot, aligned to the text column. Barcode on the
  // left, the batch fields as a small ruled table on the right, a hairline between them.
  const cw = 58, ch = 15.2, cx = L - 1.5, cy = h - 5.2 - ch;
  out.push(`<rect x="${n(cx)}" y="${n(cy)}" width="${cw}" height="${ch}" rx="1.4" fill="#FFFFFF" stroke="${C.ink}" stroke-width="0.22"/>`);
  out.push(ean13(p.gtin, cx + 0.2, cy + 1.3));
  const fx = cx + 32.2;
  out.push(`<path d="M${n(fx - 1.6)} ${n(cy + 2)}V${n(cy + ch - 2)}" stroke="${C.ink}" stroke-width="0.12"/>`);
  [['MRP Rs.', 0], ['MFD', 1], ['EXP', 2], ['BTN', 3]].forEach(([k, i]) => {
    const y = cy + 3.9 + i * 3.25;
    out.push(label(k, fx, y, { size: 1.45, fill: C.ink }));
    out.push(`<path d="M${n(fx + 8.4)} ${n(y + 0.25)}H${n(cx + cw - 2)}" stroke="${C.soft}" stroke-width="0.1" stroke-dasharray="0.35 0.35"/>`);
  });
  return `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="${w + 2 * BLEED}mm" height="${h + 2 * BLEED}mm" viewBox="${-BLEED} ${-BLEED} ${w + 2 * BLEED} ${h + 2 * BLEED}">` +
    `<defs><clipPath id="bleed"><path d="${outline(-BLEED)}"/></clipPath></defs>` +
    `<g id="Artwork" clip-path="url(#bleed)">${out.join('')}</g>` +
    `<path id="Keyline" d="${outline(2.2)}" fill="none" stroke="${C.ink}" stroke-width="0.25"/>` +
    `<path id="Cut_line" d="${outline()}" fill="none" stroke="#E4007C" stroke-width="0.2"/></svg>`;
}

const dir = path.join(root, 'export', GROUND === 'cream' ? 'labels' : `labels-${GROUND}`);
fs.mkdirSync(dir, { recursive: true });
for (const [k, p] of Object.entries(LABELS)) {
  const svg = build(p);
  fs.writeFileSync(path.join(dir, `${k}.svg`), svg);
  // Preview: trimmed to the cut line, no bleed or cut path (for mock-ups).
  const { w, h } = SIZE;
  fs.writeFileSync(path.join(dir, `${k}_preview.svg`), svg
    .replace(/width="[\d.]+mm" height="[\d.]+mm" viewBox="[^"]+"/, `width="${w}mm" height="${h}mm" viewBox="0 0 ${w} ${h}"`)
    .replace(/<path d="[^"]+"\/><\/clipPath>/, `<path d="${outline()}"/></clipPath>`)
    .replace(/<path id="Cut_line"[^>]+\/>/, ''));
}
console.log('wrote', Object.keys(LABELS).join(', '));
