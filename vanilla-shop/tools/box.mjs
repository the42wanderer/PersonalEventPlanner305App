// Natural Vanilla Tea box — final artwork.
// Builds every face in millimetres (type outlined, illustration embedded) and the full print
// sheet on the supplied dieline (2.pdf artboard, cut/fold lines copied verbatim).
// Usage: node tools/box.mjs  ->  export/final/
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const opentype = require('opentype.js');
const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
await import(path.join(root, 'dieline.js'));

// ---------------------------------------------------------------------------
// System
const C = { paper: '#FEF8E9', ink: '#143A1D', soft: '#5C6F5F', line: '#143A1D' };
const M = 7; // outer margin on every face
const font = (f) => opentype.loadSync(path.join(root, 'fonts', f));
const F = {
  display: font('fraunces-italic.ttf'),   // headings
  upright: font('fraunces-display.ttf'),  // product name (upright, same family, for hierarchy)
  sans: font('geist-regular.ttf'),        // body copy
  medium: font('geist-medium.ttf'),       // small-caps labels
};
const ILLUSTRATION = 'plates/generated/gen3.png';
const n = (v, d = 3) => Math.round(v * 10 ** d) / 10 ** d;

// ---------------------------------------------------------------------------
// Dieline geometry (points, from 2.pdf). panel = fold to fold; region = artwork + bleed area.
const MM = 72 / 25.4;
const R = (x0, y0, x1, y1) => ({ x: x0, y: y0, w: x1 - x0, h: y1 - y0 });
const PANELS = {
  front:  { panel: R(145.46, 390.86, 393.94, 631.07),  region: R(141.258, 391.242, 393.320, 630.828) },
  sideA:  { panel: R(393.94, 390.86, 633.68, 631.07),  region: R(393.035, 250.227, 634.207, 656.613) },
  back:   { panel: R(633.68, 390.86, 881.95, 631.07),  region: R(632.051, 391.246, 882.355, 630.699) },
  sideB:  { panel: R(881.95, 390.86, 1122.45, 631.07), region: R(882.137, 250.227, 1123.309, 656.613) },
  top:    { panel: R(145.50, 149.85, 393.53, 390.72),  region: R(142.715, 89.582, 393.961, 390.723) },
  inner:  { panel: R(145.50, 630.22, 393.53, 871.09),  region: R(142.715, 628.051, 393.961, 929.191) },
  bottom: { panel: R(633.68, 631.07, 881.70, 870.00),  region: R(629.184, 629.949, 881.703, 881.480) },
};
// Face studies (e.g. frontTea) use the size of the face they replace.
const size = (k) => { const p = (PANELS[k] || PANELS[k.replace(/(Tea|V\d[a-z]?)$/, "")]).panel; return { w: p.w / MM, h: p.h / MM }; };

// ---------------------------------------------------------------------------
// Type (outlined with opentype.js)
function width(f, s, sz, track = 0) {
  const g = f.stringToGlyphs(s), k = sz / f.unitsPerEm;
  return g.reduce((w, gl, i) => w + gl.advanceWidth * k + (i < g.length - 1 ? f.getKerningValue(gl, g[i + 1]) * k + track * sz : 0), 0);
}
// In LIVE mode text is written as editable <text> (for the Illustrator file); otherwise as outlines.
// font-family lists the PostScript name first (what Illustrator matches) and the family name second.
let LIVE = false;
const FONT_NAMES = {
  display: { family: "'Fraunces144ptSuperSoftWonky-Italic', 'Fraunces 144pt SuperSoft Wonky'", style: 'italic' },
  upright: { family: "'Fraunces144ptSuperSoftWonky-SemiBold', 'Fraunces 144pt SuperSoft Wonky SemiBold'" },
  sans: { family: "'Geist-Regular', 'Geist'" },
  medium: { family: "'Geist-Medium', 'Geist Medium'" },
};
const esc = (t) => t.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
function text(key, s, sz, x, y, o = {}) {
  const f = F[key], str = o.caps ? s.toUpperCase() : s, g = f.stringToGlyphs(str), k = sz / f.unitsPerEm;
  const w = width(f, str, sz, o.track || 0);
  let cx = o.anchor === 'end' ? x - w : o.anchor === 'middle' ? x - w / 2 : x, d = '';
  if (LIVE && !o.outline && str.trim()) {
    const fn = FONT_NAMES[key];
    return `<text x="${n(cx)}" y="${n(y)}" font-family="${fn.family}"${fn.style ? ` font-style="${fn.style}"` : ''} font-size="${n(sz)}"` +
      `${o.track ? ` letter-spacing="${n(o.track * sz, 4)}"` : ''} fill="${o.fill || C.ink}"${o.opacity != null ? ` opacity="${o.opacity}"` : ''}>${esc(str)}</text>`;
  }
  g.forEach((gl, i) => {
    d += gl.getPath(cx, y, sz).toPathData(3);
    cx += gl.advanceWidth * k + (i < g.length - 1 ? f.getKerningValue(gl, g[i + 1]) * k + (o.track || 0) * sz : 0);
  });
  return d ? `<path d="${d}" fill="${o.fill || C.ink}"/>` : '';
}
const label = (s, x, y, o = {}) => text('medium', s, 1.9, x, y, { caps: true, track: 0.14, ...o });
const body = (lines, x, y, o = {}) => lines.map((l, i) => text('sans', l, o.size || 2.35, x, y + i * (o.lead || 3.5), o)).join('');
const hair = (x1, y, x2, w = 0.18) => `<path d="M${n(x1)} ${n(y)}H${n(x2)}" stroke="${C.line}" stroke-width="${w}"/>`;

// Logo (traced vector), recoloured.
const logoSrc = fs.readFileSync(path.join(root, 'brand', 'vanilla-shop-logo.svg'), 'utf8');
const LOGO = { vw: Number(logoSrc.match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/)[1]), vh: Number(logoSrc.match(/viewBox="0 0 [\d.]+ ([\d.]+)"/)[1]), d: logoSrc.match(/ d="([^"]+)"/)[1] };
const logo = (x, y, w, fill = C.ink) => `<path fill="${fill}" fill-rule="evenodd" d="${LOGO.d}" transform="translate(${n(x)} ${n(y)}) scale(${n(w / LOGO.vw, 6)})"/>`;
const logoH = (w) => w * LOGO.vh / LOGO.vw;

// Illustration (transparent PNG), placed by its right edge and top, fitted inside maxW x maxH.
const png = fs.readFileSync(path.join(root, ILLUSTRATION));
const IMG = { w: png.readUInt32BE(16), h: png.readUInt32BE(20), href: 'data:image/png;base64,' + png.toString('base64') };
function illustration(right, top, maxW, maxH) {
  const s = Math.min(maxW / IMG.w, maxH / IMG.h);
  return `<image href="${IMG.href}" width="${IMG.w}" height="${IMG.h}" transform="translate(${n(right - IMG.w * s)} ${n(top)}) scale(${n(s, 6)})"/>`;
}

// Placeholder for artwork the client must supply (licensed marks, barcode).
function slot(x, y, w, h, lines) {
  return `<rect x="${n(x)}" y="${n(y)}" width="${n(w)}" height="${n(h)}" rx="0.8" fill="none" stroke="${C.soft}" stroke-width="0.2" stroke-dasharray="0.7 0.5"/>` +
    lines.map((l, i) => text('medium', l, 1.35, x + w / 2, y + h / 2 + 0.5 + (i - (lines.length - 1) / 2) * 1.9, { caps: true, track: 0.1, anchor: 'middle', fill: C.soft })).join('');
}

const paper = (w, h, bleed = 80) => `<rect x="${-bleed}" y="${-bleed}" width="${w + bleed * 2}" height="${h + bleed * 2}" fill="${C.paper}"/>`;

// Ceylon tea-hills band: one seamless tile repeated along the box, so the landscape runs
// continuously across the folds from the front, round the brewing side, to the back.
const hillsTile = fs.readFileSync(path.join(root, 'plates', 'generated', 'v3-hills-tile.jpg'));
const sof = hillsTile.indexOf(Buffer.from([0xFF, 0xC0]));
const HT = { w: hillsTile.readUInt16BE(sof + 7), h: hillsTile.readUInt16BE(sof + 5), href: 'data:image/jpeg;base64,' + hillsTile.toString('base64') };
const TILE_W = 115, TILE_H = TILE_W * HT.h / HT.w;
function hillsBand(key, w, h) {
  const wrapStart = { front: 0, sideA: size('front').w, back: size('front').w + size('sideA').w }[key];
  let out = '';
  for (let i = Math.floor(wrapStart / TILE_W) - 1; i * TILE_W - wrapStart < w + 5; i++) {
    out += `<image href="${HT.href}" width="${HT.w}" height="${HT.h}" preserveAspectRatio="none" transform="translate(${n(i * TILE_W - wrapStart)} ${n(h + 1.5 - TILE_H)}) scale(${n((TILE_W + 0.25) / HT.w, 6)} ${n(TILE_H / HT.h, 6)})"/>`; // 0.25 mm overlap hides the anti-aliased join
  }
  return out;
}
// Paper-coloured gradient over the band where type sits: opaque at `from`, clear at `to`.
function fadeBand(id, from, to, h) {
  const x0 = Math.min(from, to), x1 = Math.max(from, to), opaqueLeft = from < to;
  return `<linearGradient id="fade-${id}" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="${C.paper}" stop-opacity="${opaqueLeft ? 1 : 0}"/><stop offset="1" stop-color="${C.paper}" stop-opacity="${opaqueLeft ? 0 : 1}"/></linearGradient>` +
    `<rect x="${n(x0)}" y="${n(h - TILE_H - 2)}" width="${n(x1 - x0)}" height="${n(TILE_H + 6)}" fill="url(#fade-${id})"/>` +
    // Solid part overlaps the gradient by 0.4 mm so no anti-aliased seam shows where they meet.
    (opaqueLeft ? `<rect x="-10" y="${n(h - TILE_H - 2)}" width="${n(x0 + 10.4)}" height="${n(TILE_H + 6)}" fill="${C.paper}"/>`
                : `<rect x="${n(x1 - 0.4)}" y="${n(h - TILE_H - 2)}" width="20" height="${n(TILE_H + 6)}" fill="${C.paper}"/>`);
}

// Line icons, one style across the box: 0.32 mm forest stroke, drawn in a ±5.5 mm box around 0,0.
const TINT = '#E9ECDC';
const STROKE = `fill="none" stroke="${C.ink}" stroke-width="0.32" stroke-linecap="round" stroke-linejoin="round"`;
const ICONS = {
  cup: `<path ${STROKE} d="M-5 4.3Q0 5.7 5 4.3"/>` +
    `<path ${STROKE} d="M-3.8 -1.2H3.2Q3.2 3.9 -0.3 3.9Q-3.8 3.9 -3.8 -1.2Z"/>` +
    `<path ${STROKE} d="M3.15 -0.3q2.1 0 2.1 1.3t-2.35 1.6"/>` +
    `<path ${STROKE} d="M1.3 -1.2L2.5 -4.1"/><rect ${STROKE} x="1.75" y="-5.95" width="1.7" height="1.9" rx="0.2" transform="rotate(12 2.6 -5)"/>` +
    `<path ${STROKE} d="M-2.1 -2.4q-0.8 -1 0 -2M-0.5 -2.4q-0.8 -1 0 -2"/>`,
  timer: `<path d="M0 0.7L0 -3.2A3.9 3.9 0 0 1 1.95 -2.68Z" fill="${C.ink}" opacity="0.18"/>` +
    `<circle ${STROKE} cx="0" cy="0.7" r="3.9"/><path ${STROKE} d="M-0.9 -4.6H0.9M0 -4.6V-3.2M3 -2.5l0.7 -0.7"/>` +
    `<path ${STROKE} d="M0 0.7L1.6 -2.1"/><circle cx="0" cy="0.7" r="0.35" fill="${C.ink}"/>` +
    `<path ${STROKE} d="M0 -2.6v0.5M3.3 0.7h-0.5M0 4v-0.5M-3.3 0.7h0.5"/>`,
  ice: `<path ${STROKE} d="M-3.1 -4.4L-2.4 4.6H2.4L3.1 -4.4"/><path ${STROKE} d="M-2.85 -1.1H2.85"/>` +
    `<rect ${STROKE} x="-2.3" y="-0.3" width="2.1" height="2.1" rx="0.3" transform="rotate(14 -1.25 0.75)"/>` +
    `<rect ${STROKE} x="0.1" y="1.6" width="1.9" height="1.9" rx="0.3" transform="rotate(-10 1.05 2.55)"/>` +
    `<path ${STROKE} d="M1 -1.1L2.3 -6.1"/>`,
  // Two leaves and a bud: how Ceylon tea is plucked.
  tea: `<path ${STROKE} d="M0 4.8C0 2 0.3 -0.5 0.6 -3.4"/>` +
    `<path ${STROKE} d="M0.6 -3.4C-0.4 -4 -0.3 -5.3 0.6 -5.8C1.5 -5.3 1.6 -4 0.6 -3.4Z"/>` +
    `<path ${STROKE} d="M0.3 -1C-1.4 -0.3 -3.8 -1 -4.4 -3.3C-2.2 -3.9 -0.4 -3 0.3 -1Z"/><path ${STROKE} d="M0.3 -1L-3.3 -2.9"/>` +
    `<path ${STROKE} d="M0.1 2.2C1.8 3.2 4.3 2.6 5 0.2C2.7 -0.5 0.8 0.3 0.1 2.2Z"/><path ${STROKE} d="M0.1 2.2L3.9 0.6"/>`,
  // The vanilla orchid: five narrow petals around the rolled, ruffled lip.
  pod: [-90, -18, 54, 126, 198].map((a) => `<path ${STROKE} d="M0 -1.2C0.95 -2.2 1 -3.9 0 -5.4C-1 -3.9 -0.95 -2.2 0 -1.2Z" transform="rotate(${a + 90})"/>`).join('') +
    `<circle ${STROKE} cx="0" cy="0" r="1.25"/><circle cx="0" cy="0" r="0.42" fill="${C.ink}"/>`,
  // A tea bag on its string.
  teabag: `<rect ${STROKE} x="-3.4" y="-1.2" width="5" height="6" rx="0.6"/><path ${STROKE} d="M-3.4 0.2H1.6"/>` +
    `<path ${STROKE} d="M-0.9 -1.2C-0.9 -3.6 1.2 -4.6 2.6 -3.4"/><rect ${STROKE} x="2.3" y="-4.2" width="2.4" height="2.8" rx="0.3" transform="rotate(-14 3.5 -2.8)"/>`,
};
const icon = (name, cx, cy, r = 6.3, scale = 1) =>
  `<circle cx="${n(cx)}" cy="${n(cy)}" r="${n(r)}" fill="${TINT}"/><g transform="translate(${n(cx)} ${n(cy)}) scale(${scale})">${ICONS[name]}</g>`;

// Product and legal details, taken from the pack currently sold in the shop (Vanilla_Tea_P.pdf).
const DISTRIBUTOR = {
  intro: 'Marketed and distributed by',
  name: 'Agro Ventures Exports (Pvt) Ltd',
  address: ['No. 48, Sir Marcus Fernando Mawatha,', 'Colombo 07, Sri Lanka'],
  web: 'www.agroventuresexports.com',
  email: 'info@agroventuresexports.com',
  hotline: '011 2 187 287',
};
// GTIN from the current 25-bag, 50 g pack. A new pack size needs its own GTIN from GS1 Sri Lanka.
const GTIN = '4796034220229';

// EAN-13 at 80% magnification: 0.264 mm modules, 11/7-module quiet zones, human-readable digits.
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

// Sinhala and Tamil labels, shaped by tools/shape_labels.py (HarfBuzz) and stored as outlines.
const SHAPED = JSON.parse(fs.readFileSync(path.join(root, 'brand', 'shaped-labels.json'), 'utf8'));
const shaped = (s, sz, x, y, fill = C.soft) => {
  const g = SHAPED[s];
  if (!g) throw new Error('Label not shaped: ' + s);
  return `<path d="${g.d}" fill="${fill}" transform="translate(${n(x)} ${n(y)}) scale(${n(sz, 4)})"/>`;
};

// ---------------------------------------------------------------------------
// Faces
const faces = {
  // Logo top-left, product name bottom-left, the plant filling the right.
  frontV1: (w, h) => {
    const sz = 21.5 / width(F.display, 'Vanilla', 1), base = 73.6, lead = 0.9;
    return [
      paper(w, h),
      illustration(w - 1.5, 2.5, 58, 81),
      logo(M, 7, 17.5),
      label('Natural', M, base - sz * lead - sz * 0.78 - 1.6),
      text('display', 'Vanilla', sz, M - 0.3, base - sz * lead),
      text('display', 'Tea', sz, M - 0.3, base),
      hair(M, 76.6, 28.5),
      label('12 tea bags · 24 g', M, 80.2, { fill: C.soft }),
    ].join('');
  },

  // Brewing: three steps as aligned columns, each with a line icon, label, value and note.
  sideA: (w, h) => {
    const steps = [
      ['cup', 'Water', '150 ml', ['One tea bag in', 'hot water']],
      ['timer', 'Steep', '5 minutes', ['Then lift the', 'bag out']],
      ['ice', 'Or', 'Over ice', ['Let it cool and', 'pour over ice']],
    ];
    const colW = (w - 2 * M) / 3, top = 21;
    const out = [paper(w, h), hillsBand('sideA', w, h),
      text('display', 'How to brew', 8, M, 16.5),
      label('2 g per tea bag', w - M, 16.5, { fill: C.soft, anchor: 'end' }),
      hair(M, top, w - M)];
    steps.forEach(([name, k, v, note], i) => {
      const cx = M + colW * (i + 0.5);
      if (i > 0) out.push(`<path d="M${n(M + colW * i)} ${top + 5}V${top + 37}" stroke="${C.line}" stroke-width="0.12"/>`);
      out.push(icon(name, cx, top + 11));
      out.push(label(k, cx, top + 23, { fill: C.soft, anchor: 'middle' }));
      out.push(text('display', v, 4.9, cx, top + 30, { anchor: 'middle' }));
      note.forEach((l, j) => out.push(text('sans', l, 2.05, cx, top + 34.3 + j * 2.9, { fill: C.soft, anchor: 'middle' })));
    });
    return out.join('');
  },

  // Brand panel: logo, the line, the story.
  backV1: (w, h) => {
    const lw = 26, cx = w / 2;
    return [
      paper(w, h),
      logo(cx - lw / 2, 9, lw),
      text('display', 'Vanilla was', 7.4, cx, 45.5, { anchor: 'middle' }),
      text('display', 'never plain.', 7.4, cx, 53, { anchor: 'middle' }),
      body(['The delicate sweetness of natural vanilla unfolds', 'through warm, comforting notes and a smooth,', 'mellow aroma.'], cx, 61, { anchor: 'middle', size: 2.3, lead: 3.4 }),
      hair(cx - 6, 72.5, cx + 6),
      label('Natural vanilla tea · 12 bags · 24 g', cx, 77.7, { anchor: 'middle', fill: C.soft }),
    ].join('');
  },

  // Information panel: what is inside, then the details.
  sideB: (w, h) => {
    const out = [paper(w, h), text('display', 'What\u2019s inside', 6.2, M, 15)];
    out.push(body(['Ceylon black tea with natural vanilla, in 12 tagged,', 'unbleached tea bags of 2 g each.'], M, 21.6, { size: 2.15, lead: 3.1 }));
    const colW = (w - 2 * M) / 3;
    [['tea', 'Ceylon tea'], ['pod', 'Natural vanilla'], ['teabag', '12 tea bags']].forEach(([name, k], i) => {
      const cx = M + colW * (i + 0.5);
      out.push(icon(name, cx, 36.2, 4.6, 0.72));
      out.push(label(k, cx, 44.6, { anchor: 'middle' }));
    });
    const rows = [
      ['Ingredients', ['To be confirmed before print']],
      ['Net weight', ['24 g (12 tea bags \u00D7 2 g)']],
      ['Storage', ['To be confirmed before print']],
      ['Distributor', [DISTRIBUTOR.name + ' \u2014 see base']],
    ];
    let y = 48.6;
    rows.forEach(([k, vals]) => {
      out.push(hair(M, y, w - M, 0.12));
      out.push(label(k, M, y + 3.4, { fill: C.soft }));
      vals.forEach((v, j) => out.push(text('sans', v, 2.15, 30, y + 3.4 + j * 2.7, { fill: v.startsWith('To be') ? C.soft : C.ink })));
      y += 3.8 + vals.length * 2.7;
    });
    out.push(hair(M, y, w - M, 0.12));
    return out.join('');
  },

  // Top: the mark, centred.
  top: (w, h) => {
    const lw = 30;
    return [
      paper(w, h),
      logo(w / 2 - lw / 2, h / 2 - logoH(lw) / 2 - 4, lw),
      label('Authentic Ceylon vanilla tea', w / 2, h / 2 + logoH(lw) / 2 + 3, { anchor: 'middle', fill: C.soft }),
    ].join('');
  },

  // Base: trilingual batch block (stamped or inkjet-printed per batch), barcode, distributor.
  bottom: (w, h) => {
    const out = [paper(w, h)];
    const fields = [
      ['\u0D9A\u0DCF.\u0D85.', 'B.N.', '\u0BA4\u0BCA\u0B95\u0BC1\u0BA4\u0BBF \u0B87\u0BB2'],
      ['\u0DB1\u0DD2.\u0DAF\u0DD2.', 'MFD.', '\u0BAA\u0BCA.\u0B9A\u0BC6 \u0BA4\u0BBF\u0B95\u0BA4\u0BBF'],
      ['\u0D9A\u0DCF.\u0D89.\u0DAF\u0DD2.', 'EXP.', '\u0BAE\u0BC1.\u0BA4\u0BBF\u0B95\u0BA4\u0BBF'],
      ['\u0D8B.\u0DC3\u0DD2.\u0DB8\u0DD2.\u0DBB\u0DD4.', 'MRP Rs.', '\u0BB5\u0BBF\u0BB2\u0BC8 \u0BB0\u0BC2\u0BAA\u0BBE'],
    ];
    out.push(text('display', 'Vanilla Tea', 5.6, M, 13.5));
    out.push(hair(M, 17, w - M));
    fields.forEach(([si, en, ta], i) => {
      const y = 22.4 + i * 8;
      out.push(shaped(si, 1.75, M, y - 2.5));
      out.push(label(en, M, y, { fill: C.ink, caps: false }));
      out.push(shaped(ta, 1.6, M, y + 2.3));
      out.push(hair(M + 14, y + 0.6, M + 38, 0.15));
    });
    const bx = w - M - EAN_W + 1.5;
    out.push(ean13(GTIN, bx, 21));
    out.push(hair(M, 55.5, w - M));
    out.push(label(DISTRIBUTOR.intro, M, 60, { fill: C.soft }));
    out.push(text('medium', DISTRIBUTOR.name, 2.5, M, 64.2));
    out.push(body(DISTRIBUTOR.address, M, 67.8, { size: 2.1, lead: 2.9 }));
    out.push(body([DISTRIBUTOR.web, DISTRIBUTOR.email], w / 2 + 6, 67.8, { size: 2.1, lead: 2.9 }));
    out.push(text('medium', 'Hotline ' + DISTRIBUTOR.hotline, 2.3, w / 2 + 6, 64.2));
    return out.join('');
  },

  inner: (w, h) => paper(w, h),

  // Study: the same front with stronger tea cues (tea type, a tea-tag count, origin mark slot).
  frontTea: (w, h) => {
    const sz = 21.5 / width(F.display, 'Vanilla', 1), base = 67.8, lead = 0.9;
    const tag = (x, y) => `<g fill="none" stroke="${C.ink}" stroke-width="0.3" stroke-linejoin="round">` +
      `<path d="M${n(x + 2)} ${n(y - 3.4)}q-1.6 1.6 0 3.4"/>` +
      `<path d="M${n(x)} ${n(y + 0.9)}l1 -1h2l1 1v4.6h-4Z"/><circle cx="${n(x + 2)}" cy="${n(y + 1)}" r="0.35"/></g>`;
    return [
      paper(w, h),
      illustration(w - 1.5, 2.5, 58, 81),
      logo(M, 7, 17.5),
      slot(M, 29, 12, 9, ['Ceylon Tea', 'lion logo']),
      label('Ceylon black tea', M, base - sz * lead - sz * 0.78 - 1.6),
      text('display', 'Vanilla', sz, M - 0.3, base - sz * lead),
      text('display', 'Tea', sz, M - 0.3, base),
      text('sans', 'with natural vanilla', 2.2, M, base + 4.2, { fill: C.soft }),
      hair(M, 74.6, 28.5),
      tag(M, 76.4),
      label('12 tea bags \u00B7 24 g', M + 6, 79.6),
    ].join('');
  },

  // Study v2: new illustration (vanilla + tea sprig), Ceylon tea hills behind, lion mark, tea cues.
  // Naming reads top to bottom as one phrase: [over] Vanilla Tea, [under].
  frontV2: (w, h, over = 'Natural', under = 'Pure Ceylon black tea') => {
    const sz = 26 / width(F.display, 'Vanilla', 1), base = 64.5, lead = 0.92;
    const v2 = fs.readFileSync(path.join(root, 'plates', 'generated', 'v2-vanilla-tea.png'));
    const vw = v2.readUInt32BE(16), vh = v2.readUInt32BE(20), vs = 72 / vh;
    const tag = (x, y) => `<g fill="none" stroke="${C.ink}" stroke-width="0.3" stroke-linejoin="round">` +
      `<path d="M${n(x + 2)} ${n(y - 3.4)}q-1.6 1.6 0 3.4"/>` +
      `<path d="M${n(x)} ${n(y + 0.9)}l1 -1h2l1 1v4.6h-4Z"/><circle cx="${n(x + 2)}" cy="${n(y + 1)}" r="0.35"/></g>`;
    const lionSrc = fs.readFileSync(path.join(root, 'brand', 'ceylon-tea-lion.svg'), 'utf8');
    const lvw = Number(lionSrc.match(/viewBox="0 0 ([\d.]+)/)[1]);
    const lion = (x, y, lw) => `<path fill="#B8862B" fill-rule="evenodd" d="${lionSrc.match(/ d="([^"]+)"/)[1]}" transform="translate(${n(x)} ${n(y)}) scale(${n(lw / lvw, 6)})"/>`;
    return [
      paper(w, h),
      hillsBand('front', w, h),
      fadeBand('front', 35, 50, h),
      `<image href="data:image/png;base64,${v2.toString('base64')}" width="${vw}" height="${vh}" transform="translate(${n(w - 1.5 - vw * vs)} 3) scale(${n(vs, 6)})"/>`,
      logo(M, 7, 17.5),
      lion(M, 30, 8.5),
      label(over, M, base - sz * lead - sz * 0.72 - 2.4),
      text('display', 'Vanilla', sz, M - 0.4, base - sz * lead),
      text('display', 'Tea', sz, M - 0.4, base),
      text('sans', under, 2.3, M, base + 4.6, { fill: C.soft }),
      hair(M, 72.6, 33),
      tag(M, 74.4),
      label('12 tea bags \u00B7 24 g', M + 6, 77.6),
    ].join('');
  },

  // Approved: front and back for print.
  front: (w, h) => faces.frontV2(w, h, 'Authentic Ceylon', 'with Natural Vanilla'),
  back: (w, h) => faces.backV2(w, h),

  frontV2b: (w, h) => faces.frontV2(w, h, 'Ceylon', 'Black tea with natural vanilla'),
  frontV2c: (w, h) => faces.frontV2(w, h, 'Authentic Ceylon', 'Black tea, naturally flavoured'),

  // Study v2 back: the cup, the line, the story.
  backV2: (w, h) => {
    const cup = fs.readFileSync(path.join(root, 'plates', 'generated', 'v2-cup.png'));
    const cw = cup.readUInt32BE(16), ch = cup.readUInt32BE(20), cs = 38 / cw, cx = w / 2;
    return [
      paper(w, h),
      hillsBand('back', w, h),
      fadeBand('back', w - 4, w - 26, h),
      `<image href="data:image/png;base64,${cup.toString('base64')}" width="${cw}" height="${ch}" transform="translate(${n(cx - 19)} 3) scale(${n(cs, 6)})"/>`,
      text('display', 'Vanilla was never plain.', 6.4, cx, 48.5, { anchor: 'middle' }),
      body(['The delicate sweetness of natural vanilla unfolds', 'through warm, comforting notes and a smooth,', 'mellow aroma.'], cx, 55.5, { anchor: 'middle', size: 2.3, lead: 3.4 }),
    ].join('');
  },
};

// ---------------------------------------------------------------------------
// Variant "vine" (VARIANT=vine): the same box and copy, with the painted vanilla vine growing
// round it instead of the tea hills: flower and pods on the front, trailing on round the brewing
// side, a sprig on the lid and a tendril climbing the back. Writes to export/vine/.
const VARIANT = process.env.VARIANT || '';
if (VARIANT === 'vine') {
  const plate = (f) => {
    const b = fs.readFileSync(path.join(root, 'plates', 'generated', f));
    return { w: b.readUInt32BE(16), h: b.readUInt32BE(20), href: 'data:image/png;base64,' + b.toString('base64') };
  };
  // Firefly cut-outs of the v6 paintings (true masks, pixels untouched).
  const WRAP = plate('v6-vine.png'), SPRIG = plate('v6-sprig.png'), CLIMB = plate('v6-climb.png');
  const place = (p, x, y, s, flip = false) => `<image href="${p.href}" width="${p.w}" height="${p.h}" transform="translate(${n(x + (flip ? p.w * s : 0))} ${n(y)}) scale(${n(flip ? -s : s, 6)} ${n(s, 6)})"/>`;
  // One placement for the whole wrap, in mm from the front's left edge; each face shows its slice.
  const V = { x: -13.4, y: -2.6, s: 0.105 };
  const wrapAt = (key) => ({ front: 0, sideA: size('front').w }[key]);
  const vineWrap = (key) => place(WRAP, V.x - wrapAt(key), V.y, V.s);

  faces.front = (w, h) => {
    const sz = 30 / width(F.display, 'Vanilla', 1), base = 45.2, lead = 0.9;
    return [
      paper(w, h),
      vineWrap('front'),
      logo(M, 6.5, 13),
      label('Authentic Ceylon', M, base - sz * lead - sz * 0.72 - 2.4),
      text('display', 'Vanilla', sz, M - 0.4, base - sz * lead),
      text('display', 'Tea', sz, M - 0.4, base),
      text('sans', 'with Natural Vanilla', 2.5, M, base + 5),
      label('12 tea bags · 24 g', M, 79.8),
    ].join('');
  };

  // Brewing steps stacked in one column on the right; the vine fills the left and the foot.
  faces.sideA = (w, h) => {
    const x = 33, steps = [['150 ml', 'One tea bag in hot water'], ['5 minutes', 'Then lift the bag out'], ['Over ice', 'Let it cool and pour over ice']];
    const out = [paper(w, h), vineWrap('sideA'), text('display', 'How to brew', 6.4, x, 14.5), hair(x, 17.6, w - M)];
    steps.forEach(([v, note], i) => {
      const y = 25 + i * 9;
      out.push(text('display', v, 4.4, x, y));
      out.push(text('sans', note, 2.05, x, y + 3.4, { fill: C.soft }));
    });
    out.push(label('2 g per tea bag', w - M, 79.8, { anchor: 'end', fill: C.soft }));
    return out.join('');
  };

  // The line and the story, left-aligned; the tendril climbs the right edge from the base.
  faces.back = (w, h) => {
    const s = 0.039; // tendril artwork: leaves span x 71-612 px, stem cut at the bottom edge
    return [
      paper(w, h),
      place(CLIMB, w - 2 - 612 * s, h + 1.5 - CLIMB.h * s, s),
      text('display', 'Vanilla was', 7.4, M, 19),
      text('display', 'never plain.', 7.4, M, 26.8),
      body(['The delicate sweetness of natural', 'vanilla unfolds through warm,', 'comforting notes and a smooth,', 'mellow aroma.'], M, 35, { size: 2.3, lead: 3.4 }),
      hair(M, 74.6, 28.5),
      label('Natural vanilla tea \u00B7 12 bags \u00B7 24 g', M, 79.8, { fill: C.soft }),
    ].join('');
  };

  // Lid: the mark, with a sprig reaching in from the back corner.
  faces.top = (w, h) => {
    const lw = 28, s = 0.026; // sprig artwork: leaves from y 168 px, stem cut at the right edge
    return [
      paper(w, h),
      place(SPRIG, w + 1.5 - SPRIG.w * s, 2 - 168 * s, s),
      logo(w / 2 - lw / 2, h / 2 - logoH(lw) / 2 - 3, lw),
      label('Authentic Ceylon vanilla tea', w / 2, h / 2 + logoH(lw) / 2 + 3.5, { anchor: 'middle', fill: C.soft }),
    ].join('');
  };
}

// ---------------------------------------------------------------------------
// Output
function faceSVG(key) {
  const { w, h } = size(key);
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${n(w)}mm" height="${n(h)}mm" viewBox="0 0 ${n(w)} ${n(h)}">` +
    `<defs><clipPath id="c"><rect width="${n(w)}" height="${n(h)}"/></clipPath></defs><g clip-path="url(#c)">${faces[key](w, h)}</g></svg>`;
}
// Group names as they appear in Illustrator's Layers panel.
const GROUP_NAMES = { front: 'Front', sideA: 'Side_How_to_brew', back: 'Back', sideB: 'Side_Whats_inside', top: 'Top', inner: 'Inner_flap', bottom: 'Base' };
// Illustrator only reads embedded images from xlink:href; with plain href it treats them as missing links.
const forIllustrator = (svg) => svg
  .replace('<svg xmlns="http://www.w3.org/2000/svg"', '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"')
  .replace(/<image href=/g, '<image xlink:href=');
function sheetSVG() {
  let defs = '', art = '';
  for (const [key, { panel, region }] of Object.entries(PANELS)) {
    const { w, h } = size(key);
    defs += `<clipPath id="clip-${key}"><rect x="${region.x}" y="${region.y}" width="${n(region.w)}" height="${n(region.h)}"/></clipPath>`;
    art += `<g id="${GROUP_NAMES[key]}" clip-path="url(#clip-${key})"><g transform="translate(${panel.x} ${panel.y}) scale(${n(MM, 6)})">${faces[key](w, h)}</g></g>`;
  }
  return forIllustrator(`<svg xmlns="http://www.w3.org/2000/svg" width="1194.94pt" height="1052.97pt" viewBox="0 0 1194.94 1052.97">` +
    `<title>Natural Vanilla Tea – print sheet</title><defs>${defs}</defs><rect id="Background" width="1194.94" height="1052.97" fill="#FFFFFF"/>` +
    `<g id="Artwork">${art}</g><g id="Dieline">${globalThis.VS_DIELINE}</g></svg>`);
}

const STEM = VARIANT ? `natural-vanilla-tea-${VARIANT}` : 'natural-vanilla-tea';
const out = path.join(root, 'export', VARIANT || 'final');
fs.mkdirSync(out, { recursive: true });
const FINAL = ['front', 'sideA', 'back', 'sideB', 'top', 'inner', 'bottom'];
for (const key of VARIANT ? FINAL : Object.keys(faces)) fs.writeFileSync(path.join(out, `face-${key}.svg`), faceSVG(key));
fs.writeFileSync(path.join(out, `${STEM}_print-sheet.svg`), sheetSVG());
console.log('wrote', fs.readdirSync(out).length, 'files to', out);

// Editable version for Illustrator: same artwork, but type stays live text.
// Sinhala/Tamil labels, the barcode and the logos stay as outlines.
LIVE = true;
const editable = path.join(root, 'export', VARIANT ? `${VARIANT}-editable` : 'editable');
fs.mkdirSync(path.join(editable, 'fonts'), { recursive: true });
fs.writeFileSync(path.join(editable, `${STEM}_EDITABLE.svg`), sheetSVG());
for (const f of ['fraunces-italic.ttf', 'fraunces-display.ttf', 'geist-regular.ttf', 'geist-medium.ttf']) {
  fs.copyFileSync(path.join(root, 'fonts', f), path.join(editable, 'fonts', f));
}
LIVE = false;
console.log('wrote editable SVG and fonts to', editable);
