// Glass labels for the candles: 60 x 60 mm squares, two to an A4 sheet in the same places as the supplied
// sticker files (dielines/Candle Stickers *.pdf), with crop marks. Each label is a small version of the box
// front: the scent's painting, the logo, the number, the name and "Vanilla Scented Candle", in the box's colours.
// Type is live text with the Adobe Fonts names, as in tools/candle.mjs.
// Usage: CANDLE_FONTS=/path node tools/candle_label.mjs  ->  export/candles/labels/vanilla-candle-labels-<a>-<b>_EDITABLE.svg
import fs from 'node:fs';
import path from 'node:path';
import { SCENTS, FONT, width, esc, n, grainTile, root } from './candle.mjs';

const A4 = { w: 595.28, h: 841.89 };
const SIDE = 169.87, Y0 = 41.99, X0 = [88.81, 270.39];       // label squares on the sheet (pt), from the sticker PDF
const K = SIDE / 60, BLEED = 2;                                // the two labels sit 4.1 mm apart, so 2 mm bleed each
// Per scent: where the painting sits in the label (mm): the plant comes in from the right, as on the box front,
// leaving the left and the foot clear for the logo and the name.
const CROP = { aura: -36, zest: -32, velvet: -38, harmony: -30 };
const NAME_SIZE = 14;                                          // one size for all four (HARMONY just fits 52 mm)

const logoSrc = fs.readFileSync(path.join(root, 'brand', 'vanilla-shop-logo-cream.svg'), 'utf8');
const logoD = logoSrc.match(/ d="([^"]+)"/)[1];

function label(key, ox) {
  const c = SCENTS[key], ink = c.ink;
  const X = (x) => n(ox + x * K), Y = (y) => n(Y0 + y * K), S = (v) => n(v * K);
  const text = (f, s, x, y, sz, o = {}) => `<text x="${X(x)}" y="${Y(y)}" font-family="'${FONT[f].ps}'" font-size="${S(sz)}"` +
    `${o.track ? ` letter-spacing="${S(o.track)}"` : ''} fill="${ink}"${o.anchor ? ` text-anchor="${o.anchor}"` : ''}${o.opacity ? ` opacity="${o.opacity}"` : ''}>${esc(s)}</text>`;
  const rule = (x1, y1, x2, y2) => `<path d="M${X(x1)} ${Y(y1)}L${X(x2)} ${Y(y2)}" stroke="${ink}" stroke-opacity=".55" stroke-width="${S(0.15)}" fill="none"/>`;
  const H = 60 + 2 * BLEED, W = H * 1774 / 887, art = path.join(root, 'plates', 'generated', c.art);
  const id = `clip-${key}`;
  const data = (f) => 'data:image/jpeg;base64,' + fs.readFileSync(f).toString('base64');
  const lw = 10.5, lh = lw * 963 / 933;
  return {
    clip: `<clipPath id="${id}"><rect x="${X(-BLEED)}" y="${Y(-BLEED)}" width="${S(60 + 2 * BLEED)}" height="${S(60 + 2 * BLEED)}"/></clipPath>`,
    ground: `<rect x="${X(-BLEED)}" y="${Y(-BLEED)}" width="${S(60 + 2 * BLEED)}" height="${S(60 + 2 * BLEED)}" fill="${c.ground}"/>`,
    painting: `<g clip-path="url(#${id})"><image xlink:href="${data(art)}" x="${X(CROP[key])}" y="${Y(-BLEED)}" width="${S(W)}" height="${S(H)}" preserveAspectRatio="none"/></g>`,
    type: `<g id="Label_${key}">` +
      `<path d="${logoD}" fill="${ink}" fill-rule="evenodd" transform="translate(${X(4.5)} ${Y(4.5)}) scale(${n(S(lw) / 933, 6)})"/>` +
      text('wide', c.no, 55.5, 7.2, 1.75, { track: 0.22, anchor: 'end' }) +
      rule(4.5, 40.2, 55.5, 40.2) +
      text('name', c.name, 4.1, 52.6, NAME_SIZE, { track: -0.1 }) +
      text('wide', 'VANILLA SCENTED CANDLE', 4.5, 56.8, 1.75, { track: 0.22 }) +
      '</g>',
    marks: [[0, 0], [60, 0], [0, 60], [60, 60]].map(([x, y]) => {
      const dx = x ? 1 : -1, dy = y ? 1 : -1;
      return `<path d="M${X(x)} ${Y(y + dy * 2.5)}V${Y(y + dy * 15)}M${X(x + dx * 2.5)} ${Y(y)}H${X(x + dx * 15)}" stroke="#000" stroke-width="0.3" fill="none"/>`;
    }).join(''),
    cut: `<rect x="${X(0)}" y="${Y(0)}" width="${S(60)}" height="${S(60)}" fill="none" stroke="#E4007C" stroke-width="0.5"/>`,
    lh,
  };
}

function sheet(a, b) {
  const L = [label(a, X0[0]), label(b, X0[1])];
  const tile = grainTile({ dpi: 800, clump: 0.5 });          // finer still at label size
  const g = (id, body) => `<g id="${id}">${body}</g>`;
  return `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="${A4.w}pt" height="${A4.h}pt" viewBox="0 0 ${A4.w} ${A4.h}">` +
    `<title>The Vanilla Shop candle labels: ${SCENTS[a].name}, ${SCENTS[b].name}</title><defs>${L.map((l) => l.clip).join('')}` +
    `<pattern id="grain" patternUnits="userSpaceOnUse" width="${n(tile.mm * K)}" height="${n(tile.mm * K)}"><image xlink:href="${tile.href}" width="${n(tile.mm * K)}" height="${n(tile.mm * K)}"/></pattern>` +
    `<clipPath id="clip-labels">${L.map((l) => l.ground.replace(/ fill="[^"]+"/, '')).join('')}</clipPath></defs>` +
    `<rect id="Paper" width="${A4.w}" height="${A4.h}" fill="#FFFFFF"/>` +
    g('Background', L.map((l) => l.ground).join('')) + g('Painting', L.map((l) => l.painting).join('')) +
    g('Texture', `<rect width="${A4.w}" height="${A4.h}" fill="url(#grain)" clip-path="url(#clip-labels)"/>`) +
    g('Type', L.map((l) => l.type).join('')) +
    g('Crop_marks', L.map((l) => l.marks).join('')) + g('Cut_guide', L.map((l) => l.cut).join('')) + '</svg>';
}

const dir = path.join(root, 'export', 'candles', 'labels');
fs.mkdirSync(dir, { recursive: true });
for (const [a, b] of [['aura', 'zest'], ['velvet', 'harmony']]) {
  const svg = sheet(a, b), f = `vanilla-candle-labels-${a}-${b}`;
  fs.writeFileSync(path.join(dir, `${f}_EDITABLE.svg`), svg);
  if (process.env.PREVIEW_DIR) {
    const ff = Object.values(FONT).map((x) => `@font-face{font-family:'${x.ps}';src:url(file://${path.isAbsolute(x.file) ? x.file : path.join(process.env.CANDLE_FONTS, x.file)})}`).join('');
    fs.writeFileSync(path.join(process.env.PREVIEW_DIR, `${f}.html`), `<html><head><meta charset="utf-8"><style>${ff}html,body{margin:0}</style></head><body>${svg}</body></html>`);
  }
  console.log('wrote', f);
}
