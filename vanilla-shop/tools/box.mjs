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
  display: font('fraunces-italic.ttf'),   // product name and headings
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
function text(key, s, sz, x, y, o = {}) {
  const f = F[key], str = o.caps ? s.toUpperCase() : s, g = f.stringToGlyphs(str), k = sz / f.unitsPerEm;
  const w = width(f, str, sz, o.track || 0);
  let cx = o.anchor === 'end' ? x - w : o.anchor === 'middle' ? x - w / 2 : x, d = '';
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

  // Brewing, set as a short typographic table.
  sideA: (w, h) => {
    const rows = [
      ['Water', '150 ml', 'One tea bag in hot water'],
      ['Steep', '5 minutes', 'Then lift the bag out'],
      ['Or', 'Over ice', 'Let it cool and pour over ice'],
    ];
    const out = [paper(w, h), text('display', 'How to brew', 8, M, 17), hair(M, 22, w - M)];
    rows.forEach(([k, v, d], i) => {
      const y = 33 + i * 15;
      out.push(label(k, M, y - 1.2, { fill: C.soft }));
      out.push(text('display', v, 6.2, 27, y));
      out.push(text('sans', d, 2.25, 27, y + 4.4, { fill: C.soft }));
      out.push(hair(M, y + 8, w - M, 0.12));
    });
    out.push(label('2 g per tea bag', M, h - M, { fill: C.soft }));
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

  // Information panel.
  sideB: (w, h) => {
    const out = [paper(w, h), text('display', 'Naturally aromatic', 6.2, M, 15)];
    out.push(body(['A beautifully balanced infusion that celebrates the pure', 'essence of vanilla, creating a soothing, memorable', 'experience in every cup.'], M, 21.5, { size: 2.15, lead: 3.2 }));
    const rows = [
      ['Ingredients', ['To be confirmed before print']],
      ['Net weight', ['24 g (12 tea bags × 2 g)']],
      ['Packed for', ['The Vanilla Shop', '253 Koswatta Road, Battaramulla, Sri Lanka']],
      ['Storage', ['To be confirmed before print']],
    ];
    let y = 31.5;
    rows.forEach(([k, vals]) => {
      out.push(hair(M, y, w - M, 0.12));
      out.push(label(k, M, y + 3.4, { fill: C.soft }));
      vals.forEach((v, j) => out.push(text('sans', v, 2.15, 30, y + 3.4 + j * 2.9, { fill: v.startsWith('To be') ? C.soft : C.ink })));
      y += 4.6 + vals.length * 2.9;
    });
    out.push(hair(M, y, w - M, 0.12));
    const sy = h - M - 10;
    out.push(slot(M, sy, 17, 10, ['Agro Ventures', 'logo']));
    out.push(slot(w - M - 25, sy, 25, 10, ['EAN-13', 'barcode']));
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

  // Base: batch and date fields.
  bottom: (w, h) => {
    const cx = w / 2, out = [paper(w, h)];
    out.push(text('display', 'Vanilla Tea', 6, cx, h / 2 - 6, { anchor: 'middle' }));
    [['Batch', h / 2 + 6], ['Best before', h / 2 + 14]].forEach(([k, y]) => {
      out.push(label(k, cx - 20, y, { fill: C.soft }));
      out.push(hair(cx, y + 0.3, cx + 20, 0.15));
    });
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
    const sz = 21.5 / width(F.display, 'Vanilla', 1), base = 63.5, lead = 0.9;
    const hills = fs.readFileSync(path.join(root, 'plates', 'generated', 'v2-hills-front.jpg'));
    const hw = hills.readUInt16BE(hills.indexOf(Buffer.from([0xFF, 0xC0])) + 7), hh = hills.readUInt16BE(hills.indexOf(Buffer.from([0xFF, 0xC0])) + 5);
    const bandW = w + 6, bandH = bandW * hh / hw;
    const v2 = fs.readFileSync(path.join(root, 'plates', 'generated', 'v2-vanilla-tea.png'));
    const vw = v2.readUInt32BE(16), vh = v2.readUInt32BE(20), vs = 82 / vh;
    const tag = (x, y) => `<g fill="none" stroke="${C.ink}" stroke-width="0.3" stroke-linejoin="round">` +
      `<path d="M${n(x + 2)} ${n(y - 3.4)}q-1.6 1.6 0 3.4"/>` +
      `<path d="M${n(x)} ${n(y + 0.9)}l1 -1h2l1 1v4.6h-4Z"/><circle cx="${n(x + 2)}" cy="${n(y + 1)}" r="0.35"/></g>`;
    const lionSrc = fs.readFileSync(path.join(root, 'brand', 'ceylon-tea-lion.svg'), 'utf8');
    const lvw = Number(lionSrc.match(/viewBox="0 0 ([\d.]+)/)[1]);
    const lion = (x, y, lw) => `<path fill="#B8862B" fill-rule="evenodd" d="${lionSrc.match(/ d="([^"]+)"/)[1]}" transform="translate(${n(x)} ${n(y)}) scale(${n(lw / lvw, 6)})"/>`;
    return [
      paper(w, h),
      `<image href="data:image/jpeg;base64,${hills.toString('base64')}" width="${hw}" height="${hh}" transform="translate(-3 ${n(h + 1 - bandH)}) scale(${n(bandW / hw, 6)})"/>`,
      `<image href="data:image/png;base64,${v2.toString('base64')}" width="${vw}" height="${vh}" transform="translate(${n(w - 1 - vw * vs)} 1.5) scale(${n(vs, 6)})"/>`,
      logo(M, 7, 17.5),
      lion(M, 29, 11),
      label(over, M, base - sz * lead - sz * 0.78 - 1.6),
      text('display', 'Vanilla', sz, M - 0.3, base - sz * lead),
      text('display', 'Tea', sz, M - 0.3, base),
      text('sans', under, 2.2, M, base + 4.2, { fill: C.soft }),
      hair(M, 71, 28.5),
      tag(M, 72.8),
      label('12 tea bags \u00B7 24 g', M + 6, 76),
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
    const cw = cup.readUInt32BE(16), ch = cup.readUInt32BE(20), cs = 40 / cw, cx = w / 2;
    return [
      paper(w, h),
      `<image href="data:image/png;base64,${cup.toString('base64')}" width="${cw}" height="${ch}" transform="translate(${n(cx - 20)} 5) scale(${n(cs, 6)})"/>`,
      text('display', 'Vanilla was never plain.', 6.4, cx, 54, { anchor: 'middle' }),
      body(['The delicate sweetness of natural vanilla unfolds', 'through warm, comforting notes and a smooth,', 'mellow aroma.'], cx, 61.5, { anchor: 'middle', size: 2.3, lead: 3.4 }),
      hair(cx - 6, 72.5, cx + 6),
      label('Authentic Ceylon vanilla tea', cx, 77.7, { anchor: 'middle', fill: C.soft }),
    ].join('');
  },
};

// ---------------------------------------------------------------------------
// Output
function faceSVG(key) {
  const { w, h } = size(key);
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${n(w)}mm" height="${n(h)}mm" viewBox="0 0 ${n(w)} ${n(h)}">` +
    `<defs><clipPath id="c"><rect width="${n(w)}" height="${n(h)}"/></clipPath></defs><g clip-path="url(#c)">${faces[key](w, h)}</g></svg>`;
}
function sheetSVG() {
  let defs = '', art = '';
  for (const [key, { panel, region }] of Object.entries(PANELS)) {
    const { w, h } = size(key);
    defs += `<clipPath id="clip-${key}"><rect x="${region.x}" y="${region.y}" width="${n(region.w)}" height="${n(region.h)}"/></clipPath>`;
    art += `<g id="${key}" clip-path="url(#clip-${key})"><g transform="translate(${panel.x} ${panel.y}) scale(${n(MM, 6)})">${faces[key](w, h)}</g></g>`;
  }
  return `<svg xmlns="http://www.w3.org/2000/svg" width="1194.94pt" height="1052.97pt" viewBox="0 0 1194.94 1052.97">` +
    `<title>Natural Vanilla Tea – print sheet</title><defs>${defs}</defs><rect width="1194.94" height="1052.97" fill="#FFFFFF"/>` +
    `<g id="Artwork">${art}</g><g id="Dieline">${globalThis.VS_DIELINE}</g></svg>`;
}

const out = path.join(root, 'export', 'final');
fs.mkdirSync(out, { recursive: true });
for (const key of Object.keys(faces)) fs.writeFileSync(path.join(out, `face-${key}.svg`), faceSVG(key));
fs.writeFileSync(path.join(out, 'natural-vanilla-tea_print-sheet.svg'), sheetSVG());
console.log('wrote', fs.readdirSync(out).length, 'files to', out);
