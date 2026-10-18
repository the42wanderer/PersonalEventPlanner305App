// 100 g pouch labels in the vine system: Natural Vanilla Tea and Vanilla & Cinnamon Tea.
// The arched outline follows the current labels; SIZE is a working size until the real one is confirmed.
// Usage: node tools/label.mjs  ->  export/labels-final/<name>.svg  (the approved design: Dusk ground, woven name)
//        LABEL_GROUND=cream|golden|dusk|sage|lilac LABEL_TYPE=standard|woven|editorial|arched  ->  study variants
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const opentype = require('opentype.js');
const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const font = (f) => opentype.loadSync(path.join(root, 'fonts', f));
// The name in Instrument Serif Italic, as on the tea boxes; small type stays Geist (outlined, free).
const F = { display: font('instrument-serif-italic.ttf'), sans: font('geist-regular.ttf'), medium: font('geist-medium.ttf') };
const C = { ink: '#143A1D', soft: '#5C6F5F', line: '#143A1D' };
const n = (v, d = 3) => Math.round(v * 10 ** d) / 10 ** d;

const SIZE = { w: 70, h: 110, shoulder: 8.5 };  // mm, matched to the current label on the kraft pouch; arch rises from the shoulders to the top edge
const BLEED = 3;
// LABEL_GROUND picks the ground: cream, golden (the boxes'), or a tools/label_ground.py preset.
// With neither set, the approved final is built: Dusk ground, woven name.
const FINAL = !process.env.LABEL_GROUND && !process.env.LABEL_TYPE;
const GROUND = process.env.LABEL_GROUND || (FINAL ? 'dusk' : 'cream');
const TYPE = process.env.LABEL_TYPE || (FINAL ? 'woven' : 'standard');
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
const LION = svgMark('ceylon-tea-lion.svg');
const lion = (x, y, w) => `<path id="Ceylon_Tea_lion" fill="${C.ink}" fill-rule="evenodd" d="${LION.d}" transform="translate(${n(x)} ${n(y)}) scale(${n(w / LION.vw, 6)})"/>`;
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

// Pieces placed by their painted area: file, source size, box = painted bbox in source px.
const PIECE = {
  vine:     { file: 'v7-vine-upright-b.png', pw: 1024, ph: 1536, box: [89, 126, 930, 1438] },   // the cinnamon painting's vine without the quills, so both labels match leaf for leaf
  cinnamon: { file: 'v7-vanilla-cinnamon.png', pw: 1536, ph: 1024, box: [237, 263, 1331, 802] },
  vineCinnamon: { file: 'v7-vine-upright-cinnamon.png', pw: 1024, ph: 1536, box: [89, 126, 930, 1438] }, // the same vine (same framing), cinnamon quills at its base on the left
  teacup:   { file: 'v7-teacup.png', pw: 1254, ph: 1254, box: [153, 302, 1180, 1051] },
  tip:      { file: 'v8-crop-climb-tip.png', pw: 580, ph: 680, box: [76, 20, 523, 679] },       // back-panel tendril tip, stem cut at bottom
  trail:    { file: 'v8-crop-vine-trail.png', pw: 1219, ph: 859, box: [0, 367, 1047, 770] },    // the main vine's trailing leaves, cut at left
};
// Shared composition: name and weight on the left, the Ceylon Tea lion top right; the upright vine down the
// right (running on under the spec card); the tendril tip curling into the top-left corner and the
// vine's trailing leaves coming in from the left edge.
const COMMON = [
  { piece: 'tip', at: [-1, 12.2], height: 21, rotate: 90 },
  { piece: 'trail', at: [-1.5, 81], width: 30 },
  { piece: 'vine', at: [28, 12], height: 94 },
];
const LABELS = {
  'natural-vanilla-tea-100g': { ground: 'v6-label-ground-vanilla.jpg', over: 'Authentic Ceylon', flavour: ['Vanilla'], under: ['Ceylon black tea', 'with natural vanilla'], gtin: '4796034220243',
    pieces: COMMON },
  // Same layout; the vanilla-and-cinnamon painting sits over the vine's base. "Tea" moves up into
  // the descriptor so the name stays clear of the vine.
  'vanilla-cinnamon-tea-100g': { ground: 'v6-label-ground-cinnamon.jpg', over: 'Authentic Ceylon', flavour: ['Vanilla &', 'Cinnamon'], under: ['Vanilla and cinnamon', 'blended with pure', 'Ceylon tea'], gtin: '4796034220250',
    // The same vine with cinnamon quills painted in at its base.
    pieces: [COMMON[0], COMMON[1], { piece: 'vineCinnamon', at: [28, 12], height: 94 }] },
};

// Place an artwork by its painted area (box, in source pixels): top-left at `at` (mm), sized by height or width.
function art(d) {
  const a = PIECE[d.piece], [x0, y0, x1, y1] = a.box, s = d.height ? d.height / (y1 - y0) : d.width / (x1 - x0);
  const inner = img(a.file, -x0 * s, -y0 * s, a.pw * s, a.ph * s);
  // rotate 90 turns the piece clockwise about its painted box's top-left, then shifts it back into place.
  const rot = d.rotate === 90 ? `translate(${n((y1 - y0) * s)} 0) rotate(90)` : d.flip ? `translate(${n((x1 - x0) * s)} 0) scale(-1 1)` : '';
  return `<g transform="translate(${n(d.at[0])} ${n(d.at[1])}) ${rot}">${inner}</g>`;
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

// Small capitals set along a circular arc (centre cx, cy; radius r), centred on the top of the circle.
function arcText(str, cx, cy, r, sz, track) {
  const f = F.medium, s = str.toUpperCase(), k = sz / f.unitsPerEm, g = f.stringToGlyphs(s);
  const adv = g.map((gl) => gl.advanceWidth * k + track * sz), total = adv.reduce((a, b) => a + b, 0) - track * sz;
  let pos = -total / 2, d = '';
  return g.map((gl, i) => {
    const mid = pos + adv[i] / 2 - track * sz / 2, th = mid / r;
    const x = cx + r * Math.sin(th), y = cy - r * Math.cos(th);
    pos += adv[i];
    const path = gl.getPath(-gl.advanceWidth * k / 2, 0, sz).toPathData(3);
    return path ? `<path d="${path}" fill="${C.ink}" transform="translate(${n(x)} ${n(y)}) rotate(${n(th * 180 / Math.PI, 2)})"/>` : '';
  }).join('');
}

// Shared name size across all labels: largest size (up to cap) at which every line fits maxW mm.
function rangeSize(cap, maxW, withTea) {
  let sz = cap;
  for (const q of Object.values(LABELS)) for (const l of withTea ? [...q.flavour, 'Tea'] : q.flavour) sz = Math.min(sz, maxW / width(F.display, l, 1));
  return sz;
}

function build(p) {
  const { w, h } = SIZE;
  const VINE = { file: 'v6-vine-2x.png', pw: 3808, ph: 1651 };
  // The painting large, bleeding off both sides: flower right of centre, pods running off the left.
  const vw = 128, vh = vw * VINE.ph / VINE.pw;
  const L = 7;                                                    // left text edge
  // TYPE picks the name treatment: standard, woven (a vine leaf grows over the name), editorial
  // (big italic over tracked capitals between rules), arched (the old tagline along the arch).
  const dy = TYPE === 'arched' ? 3.2 : 0;
  // Woven: the vine stays in place; with the narrower Instrument Serif the leaf tip just overlaps the last letter.
  const pieces = TYPE === 'woven' ? p.pieces.map((q) => (q.piece.startsWith('vine') ? { ...q, at: [q.at[0] - 0, q.at[1]] } : q)) : p.pieces;
  const out = [
    img(GROUND === 'cream' ? p.ground : p.ground.replace('label-ground-', `label-ground-${GROUND}-`), -BLEED, -BLEED, w + 2 * BLEED, h + 2 * BLEED),
    ...pieces.map(art),
    logo(w / 2 - 6.5, 6.5 + dy, 13),
    // The Ceylon Tea lion top right, as on the boxes: right edge on the bar's end, foot level with the logo's.
    lion(w - L - 12, 6.5 + dy + 13 * LOGO.vh / LOGO.vw - 12 * LION.vh / LION.vw, 12),
    // Ruled top bar, as on the boxes: origin left, net weight right.
    label(p.over, L, 24.4 + dy), label('100 g', w - L, 24.4 + dy, { anchor: 'end' }),
    `<path d="M${n(L)} ${n(26.4 + dy)}H${n(w - L)}" stroke="${C.ink}" stroke-opacity=".5" stroke-width="0.18"/>`,
  ];
  // The flavour changes per product; "Tea" is the constant, set the same way and size on every label.
  // One name size for the whole range: the size at which every label's longest line fits.
  let next;
  const lines = [...p.flavour, 'Tea'];
  if (TYPE === 'editorial') {
    const sz = rangeSize(16, 50, false), lead = sz * 0.86;
    let y = 27 + dy + sz * 0.74;
    p.flavour.forEach((l, i) => out.push(text('display', l, sz, L - 0.6, y + i * lead)));
    y += (p.flavour.length - 1) * lead;
    const cap = 'TEA', cy = y + 6.4, csz = 3.4, tr = 0.6, cw = width(F.medium, cap, csz, tr);
    out.push(`<path d="M${n(L)} ${n(cy - 1.2)}H${n(L + 6)}" stroke="${C.ink}" stroke-width="0.2"/>`);
    out.push(text('medium', cap, csz, L + 8, cy, { track: tr }));
    out.push(`<path d="M${n(L + 10 + cw)} ${n(cy - 1.2)}H${n(L + 16 + cw)}" stroke="${C.ink}" stroke-width="0.2"/>`);
    next = cy + 6;
  } else {
    // Woven sizes each label's name on its own (as large as its lines allow) so it crosses the vine:
    // the upper leaf's tip passes in front of the type, its body and the stem run behind it.
    const sz = TYPE === 'woven' ? Math.min(18, ...lines.map((l) => 57 / width(F.display, l, 1))) : rangeSize(12.5, 46, true), lead = sz * 0.88;
    const b1 = 29.5 + dy + sz * 0.72;
    lines.forEach((l, i) => out.push(text('display', l, sz, L - 0.5, b1 + i * lead)));
    next = b1 + (lines.length - 1) * lead + 5;
    if (TYPE === 'woven') {
      // Redraw only the tip of the upper-left leaf on top of the name (source px 385-520, 415-540), so the
      // leaf goes over one stroke and under the next: over-under, and every letter still reads.
      const v = pieces.find((q) => q.piece.startsWith('vine')), a = PIECE[v.piece], sc = v.height / (a.box[3] - a.box[1]);
      const mm = (px, py) => [v.at[0] + (px - a.box[0]) * sc, v.at[1] + (py - a.box[1]) * sc];
      const [x0, y0] = mm(385, 415), [x1, y1] = mm(520, 540);
      out.push(`<clipPath id="leaf"><rect x="${n(x0)}" y="${n(y0)}" width="${n(x1 - x0)}" height="${n(y1 - y0)}"/></clipPath><g clip-path="url(#leaf)">${art(v)}</g>`);
    }
  }
  out.push(...[].concat(p.under).map((u, i) => text('sans', u, 2.2, L, next + i * 3)));
  // Net weight sits in the top bar.
  if (TYPE === 'arched') out.push(arcText('Savor the calm with vanilla-infused tea', w / 2, 46.5, 38.6, 1.75, 0.16));
  // Spec card: one compact, outlined panel at the foot, aligned to the text column. Barcode on the
  // left, the batch fields as a small ruled table on the right; one padding all round.
  // The barcode is scaled to match the size on the current pouch (bars about 21 mm wide, roughly
  // 67% magnification; GS1 recommends at least 80%, so test-scan before print).
  const K = 0.84, pad = 1.6, M = 0.264;
  const barsW = 95 * M * K, bcH = (BAR_H + 2.6) * K;
  const ch = bcH + 2 * pad, cx = L - 1.5, cy = h - 5.2 - ch;
  const bx = cx + pad + 1.2;                                  // left edge of the bars (digit "4" sits in the gap)
  const divX = bx + barsW + pad, fx = divX + pad, lineX0 = fx + 7.4, lineLen = 11.5;
  const cw = lineX0 + lineLen + pad - cx;
  out.push(`<rect x="${n(cx)}" y="${n(cy)}" width="${n(cw)}" height="${n(ch)}" rx="1" fill="#FFFFFF" stroke="${C.ink}" stroke-opacity=".5" stroke-width="0.18"/>`);
  out.push(`<g transform="translate(${n(bx - 11 * M * K)} ${n(cy + pad)}) scale(${K})">${ean13(p.gtin, 0, 0)}</g>`);
  out.push(`<path d="M${n(divX)} ${n(cy + pad)}V${n(cy + ch - pad)}" stroke="${C.ink}" stroke-width="0.12"/>`);
  const rows = ['MRP Rs.', 'MFD', 'EXP', 'BTN'], top = cy + pad + 1.15, step = (ch - 2 * pad - 1.15) / (rows.length - 1);
  rows.forEach((k, i) => {
    const y = top + i * step;
    out.push(label(k, fx, y, { size: 1.35, fill: C.ink }));
    out.push(`<path d="M${n(lineX0)} ${n(y + 0.2)}H${n(lineX0 + lineLen)}" stroke="${C.soft}" stroke-width="0.1" stroke-dasharray="0.35 0.35"/>`);
  });
  return `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="${w + 2 * BLEED}mm" height="${h + 2 * BLEED}mm" viewBox="${-BLEED} ${-BLEED} ${w + 2 * BLEED} ${h + 2 * BLEED}">` +
    `<defs><clipPath id="bleed"><path d="${outline(-BLEED)}"/></clipPath></defs>` +
    `<g id="Artwork" clip-path="url(#bleed)">${out.join('')}</g>` +
    `<path id="Cut_line" d="${outline()}" fill="none" stroke="#E4007C" stroke-width="0.2"/></svg>`;
}

const dir = path.join(root, 'export', FINAL ? 'labels-final' : (GROUND === 'cream' ? 'labels' : `labels-${GROUND}`) + (TYPE === 'standard' ? '' : `-${TYPE}`));
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
