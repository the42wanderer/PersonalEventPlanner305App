// Candle boxes (90 x 90 x 95 mm, one per scent) laid out on the supplied dieline, as Illustrator-ready SVG.
// Type stays live text: the scent name in Instrument Serif (free, in fonts/), everything else in Roc Grotesk
// (Adobe Fonts), so it opens editable
// on a machine with those fonts active; the barcode digits and the logo are outlines.
// Layers: Background (ground colour, editable), Painting, Name, Weave (the plant over the name), Texture (tiled
// paper grain, under the small type), Type_and_Icons, Barcode, Dieline (cut and fold, magenta, do not print).
//
// Roc Grotesk is not in the repo. CANDLE_FONTS points at a folder with roc-wide-light.otf,
// roc-wide-regular.otf and roc-regular.otf, used only to measure lines and draw the preview.
// Usage: CANDLE_FONTS=/path node tools/candle.mjs [aura|zest|velvet|harmony]
//   -> export/candles/<scent>/vanilla-candle-<scent>_EDITABLE.svg  (PREVIEW_DIR=... also writes <scent>.html for a browser)
import fs from 'node:fs';
import path from 'node:path';
import zlib from 'node:zlib';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const opentype = require('opentype.js');
const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const DL = require(path.join(root, 'dieline-candle.cjs'));
const FD = process.env.CANDLE_FONTS;
if (!FD) throw new Error('Set CANDLE_FONTS to the folder with the candle fonts (see header).');

// Font name written into the file (what Illustrator looks for), the file used to measure it, and CSS weight.
const FONT = {
  name:  { ps: 'InstrumentSerif-Regular', file: path.join(root, 'fonts', 'instrument-serif.ttf') },   // free (OFL), in the repo
  wide:  { ps: 'RocGroteskWide-Light', file: 'roc-wide-light.otf' },
  wideR: { ps: 'RocGroteskWide-Regular', file: 'roc-wide-regular.otf' },
  body:  { ps: 'RocGrotesk-Regular', file: 'roc-regular.otf' },
};
for (const f of Object.values(FONT)) f.ot = opentype.loadSync(path.isAbsolute(f.file) ? f.file : path.join(FD, f.file));
const MONO = opentype.loadSync(path.join(root, 'fonts', 'geist-mono.ttf'));
const n = (v, d = 3) => Math.round(v * 10 ** d) / 10 ** d;
const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
const width = (f, s, sz, track = 0) => {
  const g = f.ot.stringToGlyphs(s), k = sz / f.ot.unitsPerEm;
  return g.reduce((w, gl) => w + gl.advanceWidth * k, 0) + track * Math.max(0, g.length - 1);
};

const SCENTS = {
  aura:    { name: 'AURA', no: 'NO. I', gtin: '4796034220311', ground: '#101A40', ink: '#A9B2EE', art: 'v9-candle-aura-boswellia.jpg',
             notes: ['FRANKINCENSE', 'EMBER', 'VANILLA'], mood: ['EVENING, STILL', 'SMOKE AND RESIN'], size: 46, weave: [[90, 0, 100, 101]] },
  zest:    { name: 'ZEST', no: 'NO. II', gtin: '4796034220328', ground: '#CA8813', ink: '#33410F', art: 'v9-candle-zest-tea.jpg',
             notes: ['GREEN TEA', 'ALOE', 'VANILLA'], mood: ['MORNING, CLEAR', 'FRESH AND GREEN'], size: 46, weave: [[72, 0, 118, 101]] },
  velvet:  { name: 'VELVET', no: 'NO. III', gtin: '4796034220281', ground: '#79171A', ink: '#F2A799', art: 'v9-candle-velvet-rose.jpg',
             notes: ['ENGLISH ROSE', 'GERANIUM', 'VANILLA'], mood: ['SOFT, ROMANTIC', 'A GARDEN AT DUSK'], size: 46, weave: [[99, 67, 16, 12], [114, 77, 17, 11]] },
  harmony: { name: 'HARMONY', no: 'NO. IV', gtin: '4796034220298', ground: '#204A2A', ink: '#D9A043', art: 'v9-candle-harmony-almond.jpg',
             notes: ['MILK', 'HONEY', 'VANILLA'], mood: ['WARM, UNHURRIED', 'MILK AND HONEY'], size: 46, weave: [[95, 55, 45, 20], [156, 46, 18, 20]] },
};
const SLOGAN = 'LIGHT IT SLOWLY · BREATHE IN · LET THE DAY SOFTEN · ';

// Panels in sheet points, from the dieline. Faces are drawn in mm from each panel's top-left; K converts.
const K = 254.9 / 90;
const P = {
  back: [105.5, 379.6], left: [360.4, 379.6], front: [615.3, 379.6], right: [870.2, 379.6],
  lid: [615.4, 124.6], base: [105.2, 649.2],
};

function build(key) {
  const c = SCENTS[key];
  const ink = c.ink, line = ink, img = (f) => 'data:image/' + (f.endsWith('png') ? 'png' : 'jpeg') + ';base64,' + fs.readFileSync(f).toString('base64');
  const layers = { Painting: [], Name: [], Weave: [], Type_and_Icons: [], Barcode: [] };
  let defs = '', ringPath = '';
  // Face helpers: X/Y map face mm to sheet pt.
  const face = (p) => {
    const [ox, oy] = P[p], X = (x) => n(ox + x * K), Y = (y) => n(oy + y * K), S = (v) => n(v * K);
    const text = (f, s, x, y, sz, o = {}) => {
      const a = o.anchor === 'end' ? ' text-anchor="end"' : o.anchor === 'middle' ? ' text-anchor="middle"' : '';
      return `<text x="${X(x)}" y="${Y(y)}" font-family="'${FONT[f].ps}'" font-size="${S(sz)}"${o.track ? ` letter-spacing="${S(o.track)}"` : ''} fill="${o.fill || ink}"${o.opacity ? ` opacity="${o.opacity}"` : ''}${a}>${esc(s)}</text>`;
    };
    // Paragraph: wrapped to w mm, one <text> with a tspan per line (one editable block in Illustrator).
    const para = (f, s, x, y, sz, w, lead, o = {}) => {
      const lines = [];
      for (const raw of s.split('\n')) {
        let cur = '';
        for (const word of raw.split(' ')) {
          const t = cur ? cur + ' ' + word : word;
          if (cur && width(FONT[f], t, sz, o.track || 0) > w) { lines.push(cur); cur = word; } else cur = t;
        }
        lines.push(cur);
      }
      const a = o.anchor === 'middle' ? ' text-anchor="middle"' : '';
      return { h: lines.length * lead, svg: `<text font-family="'${FONT[f].ps}'" font-size="${S(sz)}"${o.track ? ` letter-spacing="${S(o.track)}"` : ''} fill="${o.fill || ink}"${o.opacity ? ` opacity="${o.opacity}"` : ''}${a}>` +
        lines.map((l, i) => `<tspan x="${X(x)}" y="${Y(y + i * lead)}">${esc(l)}</tspan>`).join('') + '</text>' };
    };
    const rule = (x1, y1, x2, y2, op = 0.55) => `<path d="M${X(x1)} ${Y(y1)}L${X(x2)} ${Y(y2)}" stroke="${line}" stroke-opacity="${op}" stroke-width="${S(0.18)}" fill="none"/>`;
    return { X, Y, S, text, para, rule };
  };
  const caps = (F, s, x, y, o = {}) => F.text('wide', s, x, y, o.size || 2.05, { track: 0.3, ...o });
  const label = (F, s, x, y) => F.text('wideR', s, x, y, 1.85, { track: 0.3, opacity: 0.7 });
  const logoSrc = fs.readFileSync(path.join(root, 'brand', 'vanilla-shop-logo-cream.svg'), 'utf8');
  const logoD = logoSrc.match(/ d="([^"]+)"/)[1], LVW = 933, LVH = 963;
  const logo = (F, cx, cy, w) => `<path d="${logoD}" fill="${ink}" fill-rule="evenodd" transform="translate(${n(F.X(cx - w / 2))} ${n(F.Y(cy - w * LVH / LVW / 2))}) scale(${n(F.S(w) / LVW, 6)})"/>`;

  // ---------------- front + right side (one strip, painting across both)
  {
    const F = face('front');
    const art = path.join(root, 'plates', 'generated', c.art);
    const H = 101, W = H * 1774 / 887;                     // painting scaled a touch past the panels for bleed
    const pimg = (href) => `<image xlink:href="${href}" x="${F.X(0)}" y="${F.Y(-3)}" width="${F.S(W)}" height="${F.S(H)}" preserveAspectRatio="none"/>`;
    defs += `<clipPath id="clip-strip"><rect x="${F.X(0)}" y="${F.Y(-1)}" width="${F.S(187)}" height="${F.S(99)}"/></clipPath>`;
    layers.Painting.push(`<g id="Painting_${key}" clip-path="url(#clip-strip)">${pimg(img(art))}</g>`);
    layers.Name.push(F.text('name', c.name, 7, 88, c.size, { track: -0.3 }));
    // Weave: the plant alone (ground knocked out), drawn over the name inside these rects.
    defs += `<clipPath id="clip-weave">${c.weave.map(([x, y, w, h]) => `<rect x="${F.X(x)}" y="${F.Y(y - 3)}" width="${F.S(w)}" height="${F.S(h)}"/>`).join('')}</clipPath>`;
    layers.Weave.push(`<g clip-path="url(#clip-weave)">${pimg(img(plantCutout(art, key)))}</g>`);
    const t = [];
    t.push(F.rule(9, 15, 81, 15), caps(F, 'THE VANILLA SHOP', 9, 12), caps(F, c.no, 81, 12, { anchor: 'end' }));
    t.push(label(F, 'NOTES', 9, 24), ...c.notes.map((s, i) => caps(F, s, 9, 28 + i * 3.4)));
    t.push(label(F, 'MOOD', 36, 24), ...c.mood.map((s, i) => caps(F, s, 36, 28 + i * 3.4)));
    t.push(...['VANILLA', 'SCENTED', 'CANDLE'].map((s, i) => caps(F, s, 81, 28 + i * 3.4 - 4, { anchor: 'end' })));
    t.push(F.rule(9, 40, 81, 40), F.rule(9, 91.5, 81, 91.5));
    layers.Type_and_Icons.push(`<g id="Front_type">${t.join('')}</g>`);
  }

  // ---------------- lid: the logo inside a ring of text
  {
    const F = face('lid'), r = 22, cx = 45, cy = 45;
    const len = 2 * Math.PI * r, base = width(FONT.wide, SLOGAN, 2.6), track = (len - base) / SLOGAN.length;
    ringPath = `M${F.X(cx - r)} ${F.Y(cy)}a${F.S(r)} ${F.S(r)} 0 1 1 ${F.S(2 * r)} 0a${F.S(r)} ${F.S(r)} 0 1 1 ${F.S(-2 * r)} 0`;
    defs += `<path id="ring-${key}" d="${ringPath}"/>`;
    layers.Type_and_Icons.push(`<g id="Lid">` +
      `<circle cx="${F.X(cx)}" cy="${F.Y(cy)}" r="${F.S(25.6)}" fill="none" stroke="${line}" stroke-opacity=".55" stroke-width="${F.S(0.18)}"/>` +
      `<circle cx="${F.X(cx)}" cy="${F.Y(cy)}" r="${F.S(18.6)}" fill="none" stroke="${line}" stroke-opacity=".55" stroke-width="${F.S(0.18)}"/>` +
      `<text font-family="'${FONT.wide.ps}'" font-size="${F.S(2.6)}" letter-spacing="${F.S(track)}" fill="${ink}"><textPath xlink:href="#ring-${key}">${esc(SLOGAN)}</textPath></text>` +
      logo(F, cx, cy, 19) + F.rule(9, 79.5, 81, 79.5) + caps(F, c.name, 9, 84) + caps(F, c.no, 81, 84, { anchor: 'end' }) + '</g>');
  }

  // ---------------- back: contents, cautions, safety icons
  {
    const F = face('back'), t = [];
    t.push(F.rule(9, 15, 81, 15), caps(F, 'THE VANILLA SHOP', 9, 12), caps(F, c.no, 81, 12, { anchor: 'end' }));
    t.push(F.text('wideR', 'LIGHT IT SLOWLY.', 9, 23.6, 3.6, { track: 0.5 }));
    let y = 31;
    for (const [k, s] of [
      ['CONTAINS', 'Vanilla oil, beeswax, stearic acid, paraffin wax, parfum.'],
      ['CAUTION', 'Store the candle away from direct sunlight. Keep it away from dust and dirt. Avoid lighting in windy areas.'],
      ['WARNING', 'Do not leave a burning candle unattended. Keep away from things that catch fire. Keep away from children and pets.'],
      ['FOR BEST RESULTS', 'Trim the wick to ¼ inch before use. Dispose of contents and container according to local regulations.'],
    ]) {
      t.push(label(F, k, 9, y));
      const p = F.para('body', s, 9, y + 3.6, 2.3, 72, 3.1);
      t.push(p.svg); y += 3.6 + p.h + 1.3;
    }
    t.push(iconRow(F, 75, ['warning', 'unattended', 'children', 'distance', 'flammable'],
      ['READ THE WARNINGS', 'NEVER LEAVE UNATTENDED', 'AWAY FROM CHILDREN, PETS', '7 CM APART', 'AWAY FROM FABRICS'], ink));
    layers.Type_and_Icons.push(`<g id="Back">${t.join('')}</g>`);
  }

  // ---------------- left side: care icons, distributor, barcode
  {
    const F = face('left'), t = [];
    t.push(F.rule(9, 15, 81, 15), caps(F, 'VANILLA SCENTED CANDLE', 9, 12), caps(F, c.name, 81, 12, { anchor: 'end' }));
    t.push(iconRow(F, 15, ['sun', 'wind', 'trim', 'dispose'], ['NO DIRECT SUN', 'NO DRAFTS', 'TRIM WICK ¼ IN', 'DISPOSE RESPONSIBLY'], ink, true));
    t.push(F.rule(9, 36.5, 81, 36.5), label(F, 'MARKETED AND DISTRIBUTED BY', 9, 41));
    t.push(F.para('body', 'Agro Ventures Exports (Pvt) Ltd\nNo. 48, Sir Marcus Fernando Mawatha\nColombo 07, Sri Lanka', 9, 45.5, 2.3, 72, 3.1).svg);
    t.push(F.para('body', 'www.agroventuresexports.com\ninfo@agroventuresexports.com\nHotline 011 2 187287', 9, 56.5, 2.3, 72, 3.1).svg);
    t.push(caps(F, c.no, 9, 82.2, { size: 1.8 }), caps(F, 'THE VANILLA SHOP', 9, 85.3, { size: 1.8 }));
    layers.Type_and_Icons.push(`<g id="Left_side">${t.join('')}</g>`);
    layers.Barcode.push(barcode(F, c.gtin, 81, 87));
  }

  // ---------------- base
  {
    const F = face('base');
    layers.Type_and_Icons.push(`<g id="Base">${logo(F, 45, 40, 16)}${caps(F, 'VANILLA SCENTED CANDLE', 45, 56, { anchor: 'middle' })}${caps(F, c.name + '  ·  ' + c.no, 45, 60, { anchor: 'middle' })}</g>`);
  }

  // ---------------- assemble
  const tile = grainTile();
  defs += `<pattern id="grain" patternUnits="userSpaceOnUse" width="${n(tile.mm * K)}" height="${n(tile.mm * K)}"><image xlink:href="${tile.href}" width="${n(tile.mm * K)}" height="${n(tile.mm * K)}"/></pattern>`;
  defs += `<clipPath id="clip-bleed"><path d="${DL.BLEED}"/></clipPath>`;
  const g = (id, body) => `<g id="${id}">${body}</g>`;
  return `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="${DL.W}pt" height="${DL.H}pt" viewBox="0 0 ${DL.W} ${DL.H}">` +
    `<title>The Vanilla Shop candle box: ${c.name}</title><defs>${defs}</defs>` +
    g('Background', `<path d="${DL.BLEED}" fill="${c.ground}"/>`) +
    g('Painting', layers.Painting.join('')) + g('Name', layers.Name.join('')) + g('Weave', layers.Weave.join('')) +
    // Grain sits over the painting and the big name but under the small type, icons and barcode, so they print crisp.
    g('Texture', `<rect x="0" y="0" width="${DL.W}" height="${DL.H}" fill="url(#grain)" clip-path="url(#clip-bleed)"/>`) +
    g('Type_and_Icons', layers.Type_and_Icons.join('')) + g('Barcode', layers.Barcode.join('')) +
    // An unstroked copy of the lid circle: Illustrator flattens imported text on a path, so this is there to
    // click with the Type on a Path tool if the slogan needs retyping.
    g('Lid_ring_path', `<path d="${ringPath}" fill="none" stroke="none"/>`) +
    g('Dieline', DL.LINES.map((d) => `<path d="${d}" fill="none" stroke="#E4007C" stroke-width="0.5"/>`).join('')) + '</svg>';
}

// ---------------- icons: 10 x 10 line drawings, placed in a ruled row with captions under each
function iconPaths(k) {
  const candle = (x, y, h = 4.4, w = 1.6) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx=".2"/><path d="M${x + w / 2} ${y - 2.3}c.75 .8 .65 1.6 0 1.9c-.65 -.3 -.75 -1.1 0 -1.9z"/>`;
  const cross = (x1, y1, x2, y2) => `<path d="M${x1} ${y1}L${x2} ${y2}M${x2} ${y1}L${x1} ${y2}"/>`;
  return {
    warning: '<path d="M5 1.1L9.3 8.7H.7Z"/><path d="M5 3.9V6.1"/><circle cx="5" cy="7.3" r=".22"/>',
    unattended: candle(1.6, 4.4) + '<path d="M5.6 3.6V9M5.6 6.4H8.6V9"/><path d="M.9 9.4L9.4 .9"/>',
    children: '<circle cx="2.6" cy="1.9" r="1.05"/><path d="M.9 5.6c0-1.1.7-1.9 1.7-1.9s1.7.8 1.7 1.9"/><circle cx="2.6" cy="8" r="1.15"/><path d="M1.75 7.3L1.8 6.1L2.45 6.85M3.45 7.3L3.4 6.1L2.75 6.85"/>' + candle(6.6, 4.6) + cross(5.9, 4.2, 8.9, 9.2),
    distance: candle(1, 4.6, 4.4, 1.4) + candle(7.6, 4.6, 4.4, 1.4) + '<path d="M3.2 6.6H6.8M3.9 5.9L3.2 6.6L3.9 7.3M6.1 5.9L6.8 6.6L6.1 7.3"/>',
    flammable: '<path d="M.8 1H5.4M1.4 1c.5 2.4-.3 4.6.3 8M2.7 1c.5 2.4-.3 4.6.3 8M4 1c.5 2.4-.3 4.6.3 8"/>' + candle(7, 4.6) + cross(6.2, 4.2, 9.3, 9.2),
    sun: '<circle cx="5" cy="5" r="1.7"/><path d="M5 1.2V2.3M5 7.7V8.8M1.2 5H2.3M7.7 5H8.8M2.3 2.3L3.1 3.1M6.9 6.9L7.7 7.7M7.7 2.3L6.9 3.1M3.1 6.9L2.3 7.7"/><path d="M1.3 8.7L8.7 1.3"/>',
    wind: '<path d="M.9 3.6H6.2c1.4 0 1.4-2 .1-2-.6 0-.9.4-.9.8M.9 5.4H8c1.4 0 1.4 2 .1 2-.6 0-.9-.4-.9-.8M.9 7.2H4.6"/><path d="M1 9.3L9.3 1"/>',
    trim: '<circle cx="2.3" cy="7.6" r="1.1"/><circle cx="4.6" cy="8.6" r="1.1"/><path d="M3.1 6.8L8.4 1.6M5.3 7.8L6.9 3.6"/><path d="M8.6 5.2V8.6"/>',
    dispose: '<path d="M2 3H8M3.9 3V1.9H6.1V3M2.7 3L3.2 9H6.8L7.3 3M4.3 4.6V7.6M5.7 4.6V7.6"/>',
  }[k];
}
function iconRow(F, top, keys, caps, ink, shareTopRule = false) {
  const x0 = 9, w = 72, cw = w / keys.length, is = 8.4, out = [];
  if (!shareTopRule) out.push(F.rule(x0, top, x0 + w, top));
  keys.forEach((k, i) => {
    const cx = x0 + cw * (i + 0.5), s = is / 10;
    if (i) out.push(F.rule(x0 + cw * i, top, x0 + cw * i, top + 15.5, 0.35));
    out.push(`<g fill="none" stroke="${ink}" stroke-width="0.42" stroke-linecap="round" stroke-linejoin="round" transform="translate(${F.X(cx - is / 2)} ${F.Y(top + 2)}) scale(${n(F.S(s), 5)})">${iconPaths(k).replace(/<circle cx="5" cy="7.3" r=".22"\/>/, `<circle cx="5" cy="7.3" r=".22" fill="${ink}"/>`)}</g>`);
    out.push(F.para('wide', caps[i], cx, top + 12.2, 1.45, cw - 1.2, 1.9, { track: 0.1, anchor: 'middle' }).svg);
  });
  return out.join('');
}

// ---------------- EAN-13: bars as one path, digits as outlines (no font needed at the printer)
function barcode(F, code, right, bottom) {
  const L = ['0001101', '0011001', '0010011', '0111101', '0100011', '0110001', '0101111', '0111011', '0110111', '0001011'];
  const G = ['0100111', '0110011', '0011011', '0100001', '0011101', '0111001', '0000101', '0010001', '0001001', '0010111'];
  const R = ['1110010', '1100110', '1101100', '1000010', '1011100', '1001110', '1010000', '1000100', '1001000', '1110100'];
  const PAR = ['LLLLLL', 'LLGLGG', 'LLGGLG', 'LLGGGL', 'LGLLGG', 'LGGLLG', 'LGGGLL', 'LGLGLG', 'LGLGGL', 'LGGLGL'];
  const dg = code.split('').map(Number);
  if ((10 - dg.slice(0, 12).reduce((a, v, i) => a + v * (i % 2 ? 3 : 1), 0) % 10) % 10 !== dg[12]) throw new Error('Invalid EAN-13 ' + code);
  let bits = '101'; const gd = [0, 1, 2];
  dg.slice(1, 7).forEach((d, i) => { bits += (PAR[dg[0]][i] === 'L' ? L : G)[d]; });
  gd.push(bits.length + 1, bits.length + 3); bits += '01010';
  dg.slice(7).forEach((d) => { bits += R[d]; });
  gd.push(bits.length, bits.length + 2); bits += '101';
  const m = 0.29, barH = 15, q = 11 * m, W = (95 + 22) * m, Hh = barH + 3.2, pad = 1.6;
  const x0 = right - W - 2 * pad + pad, y0 = bottom - Hh - pad;           // bars' box origin (mm)
  let d = '';
  for (let i = 0; i < bits.length; i++) {
    if (bits[i] !== '1') continue;
    let j = i; while (bits[j + 1] === '1' && gd.includes(j + 1) === gd.includes(i)) j++;
    const h = barH + (gd.includes(i) ? 1.4 : 0);
    d += `M${F.X(x0 + q + i * m)} ${F.Y(y0)}h${F.S((j - i + 1) * m)}v${F.S(h)}h${F.S(-(j - i + 1) * m)}Z`;
    i = j;
  }
  const sz = 2.4, ty = y0 + barH + 2.6;
  const digits = (s, x, anchor) => {
    const w = MONO.getAdvanceWidth(s, F.S(sz));
    const sx = anchor === 'end' ? F.X(x) - w : F.X(x) - w / 2;
    return MONO.getPath(s, sx, F.Y(ty), F.S(sz)).toPathData(3);
  };
  const ink = '#141414';
  return `<g id="Barcode_${code}"><rect x="${F.X(x0 - pad)}" y="${F.Y(y0 - pad)}" width="${F.S(W + 2 * pad)}" height="${F.S(Hh + 2 * pad - 0.6)}" rx="${F.S(1)}" fill="#F6F0E4"/>` +
    `<path d="${d}" fill="${ink}"/><path d="${digits(code[0], x0 + q - 1.2 * m, 'end') + digits(code.slice(1, 7), x0 + q + 24 * m) + digits(code.slice(7), x0 + q + 71 * m)}" fill="${ink}"/></g>`;
}

// ---------------- raster helpers (PNG writer, plant cut-out, grain tile)
function png(w, h, rgba) {
  const raw = Buffer.alloc((w * 4 + 1) * h);
  for (let y = 0; y < h; y++) { raw[y * (w * 4 + 1)] = 0; rgba.copy(raw, y * (w * 4 + 1) + 1, y * w * 4, (y + 1) * w * 4); }
  const crc = (b) => { let c = ~0; for (const x of b) { c ^= x; for (let k = 0; k < 8; k++) c = (c >>> 1) ^ (0xEDB88320 & -(c & 1)); } return ~c >>> 0; };
  const chunk = (t, d) => { const l = Buffer.alloc(4); l.writeUInt32BE(d.length); const td = Buffer.concat([Buffer.from(t), d]); const c = Buffer.alloc(4); c.writeUInt32BE(crc(td)); return Buffer.concat([l, td, c]); };
  const ih = Buffer.alloc(13); ih.writeUInt32BE(w, 0); ih.writeUInt32BE(h, 4); ih[8] = 8; ih[9] = 6;
  return Buffer.concat([Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]), chunk('IHDR', ih), chunk('IDAT', zlib.deflateSync(raw, { level: 9 })), chunk('IEND', Buffer.alloc(0))]);
}
// The plant cut-outs are made by tools/candle_plant.py (ground colour keyed out) into plates/generated.
function plantCutout(art, key) {
  const f = path.join(root, 'plates', 'generated', `v9-candle-${key}-plant.png`);
  if (!fs.existsSync(f)) throw new Error('Missing ' + f + ' (run tools/candle_plant.py)');
  return f;
}
// Seamless grain: light and dark specks with alpha, 512 px over 43.35 mm (300 dpi), tiled across the sheet.
// dpi sets the speck size (600 = finer than the eye reads as dots at label size); clump adds paper tooth.
function grainTile({ dpi = 600, clump = 0.7 } = {}) {
  const N = 512; let s = 7;
  const rnd = () => { s = (s * 16807) % 2147483647; return s / 2147483647; };
  const a = new Float32Array(N * N).map(() => rnd() + rnd() + rnd() - 1.5);
  const b = new Float32Array(N * N);                                     // wrap-around blur for clumps
  for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) {
    let v = 0; for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) v += a[((y + dy + N) % N) * N + (x + dx + N) % N];
    b[y * N + x] = v / 9;
  }
  const px = Buffer.alloc(N * N * 4);
  for (let i = 0; i < N * N; i++) {
    const v = b[i] * clump * 1.6 + a[i] * 0.45;                           // clumped tooth + fine grain
    const light = v > 0, al = Math.min(255, Math.abs(v) * 85);
    px[i * 4] = px[i * 4 + 1] = px[i * 4 + 2] = light ? 255 : 0; px[i * 4 + 3] = n(al * (light ? 0.55 : 0.8), 0);
  }
  return { mm: N / dpi * 25.4, href: 'data:image/png;base64,' + png(N, N, px).toString('base64') };
}

// ---------------- output
export { SCENTS, FONT, MONO, width, esc, n, grainTile, root };

// Run as a script (not when imported by tools/candle_label.mjs).
if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const keys = process.argv[2] ? [process.argv[2]] : Object.keys(SCENTS);
  for (const key of keys) {
    const svg = build(key);
    const dir = path.join(root, 'export', 'candles', key);
    fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(path.join(dir, `vanilla-candle-${key}_EDITABLE.svg`), svg);
    // Browser preview (PREVIEW_DIR, outside the repo): the same SVG with the font names mapped to the local files.
    if (process.env.PREVIEW_DIR) {
      const ff = Object.values(FONT).map((f) => `@font-face{font-family:'${f.ps}';src:url(file://${path.isAbsolute(f.file) ? f.file : path.join(FD, f.file)})}`).join('');
      fs.writeFileSync(path.join(process.env.PREVIEW_DIR, `${key}.html`), `<html><head><meta charset="utf-8"><style>${ff}html,body{margin:0}</style></head><body>${svg}</body></html>`);
    }
    console.log('wrote', key, Math.round(svg.length / 1e6 * 10) / 10, 'MB');
  }
}
