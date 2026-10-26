// Natural Vanilla Tea boxes: the vine set's painting, golden ground, diagram and lid sprigs, with the candle
// range's structure (ruled bars, spaced Roc Grotesk labels, sentence-case body) and a numbered brewing stepper.
// The name and panel headings are Instrument Serif Italic. Cube front: name high, logo bottom left.
// Long front: data columns on top, vine across the top right, the name along the foot, logo and lion bottom right.
// Output is Illustrator-ready SVG on the supplied dielines, type live, layers as in tools/candle.mjs.
// Usage: CANDLE_FONTS=/path node tools/tea_box.mjs [cube|long]
//   -> export/tea/<box>/vanilla-tea-<box>_EDITABLE.svg   (PREVIEW_DIR=... also writes <box>.html for a browser)
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { FONT as CFONT, MONO, esc, n, grainTile, root } from './candle.mjs';
const require = createRequire(import.meta.url);
const opentype = require('opentype.js');
await import(path.join(root, 'dieline.js'));
await import(path.join(root, 'dieline-long.js'));

// The name and the panel headings are in Instrument Serif Italic (free, OFL, in fonts/); labels and body
// text are the candle boxes' Roc Grotesk (Adobe Fonts, measured from CANDLE_FONTS, mapped by name).
const FONT = {
  title: { ps: 'InstrumentSerif-Italic', file: path.join(root, 'fonts', 'instrument-serif-italic.ttf') },
  roman: { ps: 'InstrumentSerif-Regular', file: path.join(root, 'fonts', 'instrument-serif.ttf') },
  wide: CFONT.wide, wideR: CFONT.wideR, body: CFONT.body,
};
FONT.title.ot = opentype.loadSync(FONT.title.file);
FONT.roman.ot = opentype.loadSync(FONT.roman.file);
const width = (f, s, sz, track = 0) => {
  const g = f.ot.stringToGlyphs(s), k = sz / f.ot.unitsPerEm;
  return g.reduce((w, gl) => w + gl.advanceWidth * k, 0) + track * Math.max(0, g.length - 1);
};
// TEA_THEME=green|espresso: a deep ground in cream ink, "Vanilla" in gold (the house foil), as on the candles and
// soaps; written to export/tea-<theme>/ so the golden-ground files stay as they are.
const THEMES = { green: { paper: '#1F3B2B', ink: '#F3E6C8' }, espresso: { paper: '#2A1B13', ink: '#F3E6C8' },
  // the extract labels' technique: a soft watercolour vanilla with Ceylon tea's two leaves and a bud, glowing out of
  // one colour (art from TEA_ART, made by studies/tea/watercolour/teaart.py; TEA_ART=studies/tea/watercolour); the realistic paintings are left off
  teal: { paper: '#2C6466', ink: '#F5EEDC', art: true }, tgreen: { paper: '#1F4732', ink: '#F5EEDC', art: true },
  // after the Japanese-tea board: cream paper, our engraving printed faintly all over (studies/tea/watercolour/cream.py),
  // the painted band along the front's foot; green ink, "Vanilla" in a deeper gold for a light ground
  // TEA_CREAM=shadow: no band; the name in the quiet middle; art from studies/tea/watercolour/shadow.py
  cream: { paper: '#F6EEDC', ink: '#1F4732', art: true, pattern: true, light: true },
  // the extract labels' Split on a box: cream left of the front, a teal block from SPLIT_AT wrapping onto the right
  // side with the watercolour flower across the fold (art from studies/tea/watercolour/split.py)
  split: { paper: '#F6EEDC', ink: '#1E4F50', art: true, light: true, split: { cube: 58, long: 92 } },
  splitcin: { paper: '#F6EEDC', ink: '#6B3420', art: true, light: true, split: { cube: 58, long: 92 }, suffix: '-cin', cin: true }, tgreen: { paper: '#1F4732', ink: '#F5EEDC', art: true },
  // after the Japanese-tea board: cream paper, our engraving printed faintly all over (studies/tea/watercolour/cream.py),
  // the painted band along the front's foot; green ink, "Vanilla" in a deeper gold for a light ground
  // TEA_CREAM=shadow: no band; the name in the quiet middle; art from studies/tea/watercolour/shadow.py
  cream: { paper: '#F6EEDC', ink: '#1F4732', art: true, pattern: true, light: true },
  // the extract labels' Split on a box: cream left of the front, a teal block from SPLIT_AT wrapping onto the right
  // side with the watercolour flower across the fold (art from studies/tea/watercolour/split.py)
  split: { paper: '#F6EEDC', ink: '#1E4F50', art: true, light: true, split: { cube: 58, long: 92 } },
  splitcin: { paper: '#F6EEDC', ink: '#6B3420', art: true, light: true, split: { cube: 58, long: 92 }, suffix: '-cin', cin: true }, amber: { paper: '#B0612A', ink: '#FFF4E4', art: true },
  // the painting soaked into aged cream paper like spilt tea (studies/tea/watercolour/carton/blotbox.py)
  blot: { paper: '#F4EBD6', ink: '#4F5E2C', art: true, light: true, blot: true, split: { cube: 58, long: 92 } },
  blotcin: { paper: '#F4EBD6', ink: '#6B3420', art: true, light: true, blot: true, split: { cube: 58, long: 92 }, suffix: '-cin', cin: true },
  // the pouch colours brought into the cream as one artwork (studies/tea/watercolour/carton/glow.py)
  // layered watercolour glazes, brand tea palette (studies/tea/watercolour/carton/blot2box.py)
  washteal: { paper: '#F6EEDC', ink: '#1E4F50', art: true, light: true, blot: true, split: { cube: 58, long: 92 } },
  wgreen: { paper: '#F6EEDC', ink: '#1F4A2C', art: true, light: true, blot: true, split: { cube: 58, long: 92 } },
  wsage: { paper: '#F6EEDC', ink: '#3E5A3C', art: true, light: true, blot: true, split: { cube: 58, long: 92 } },
  // three art directions judged on one carton (studies/tea/concepts/concepts.py)
  cA: { paper: '#3A1C14', ink: '#F3E6C8', art: true, blot: true, split: { cube: 58, long: 92 } },
  cB: { paper: '#1F3A2B', ink: '#F3E6C8', art: true, blot: true, split: { cube: 58, long: 92 } },
  cC: { paper: '#F6EEDC', ink: '#1E4F50', art: true, light: true, split: { cube: 58, long: 92 } },
  wash: { paper: '#F6EEDE', ink: '#1F4A2C', art: true, light: true, blot: true, split: { cube: 58, long: 92 } },
  glow: { paper: '#F6EEDC', ink: '#1E4F50', art: true, light: true, blot: true, split: { cube: 58, long: 92 } },
  glowcin: { paper: '#F6EEDC', ink: '#6B3420', art: true, light: true, blot: true, split: { cube: 58, long: 92 }, suffix: '-cin', cin: true },
  // The Estate: the grained tea-garden strip round the four walls on a cream ground, the lid the evening sky
  // (studies/tea/bandsystem/wrap.py writes the art into TEA_ART). Forest greens, or plum and orange.
  estate: { paper: '#F3E6BE', ink: '#142D25', art: true, light: true, estate: true },
  estateplum: { paper: '#F3E6BE', ink: '#3B1631', art: true, light: true, estate: true },
  // the alternative: no cream on How to brew; its land fades into the lid's plum and the steps are set in cream on it
  estateplumside: { paper: '#F3E6BE', ink: '#3B1631', art: true, light: true, estate: true, sidePlum: true } };
const THEME = THEMES[process.env.TEA_THEME] ? process.env.TEA_THEME : null;
const MM = 72 / 25.4, INK = THEME ? THEMES[THEME].ink : '#143A1D', PAPER = THEME ? THEMES[THEME].paper : '#F8E7C0';
const GOLD = 'url(#foil)';
const ART = THEME && THEMES[THEME].art ? (f) => path.join(process.env.TEA_ART, f) : null;
const R = (x0, y0, x1, y1) => ({ x: x0, y: y0, w: x1 - x0, h: y1 - y0 });
const G = (f) => path.join(root, 'plates', 'generated', f);
const data = (f) => `data:image/${f.endsWith('png') ? 'png' : 'jpeg'};base64,` + fs.readFileSync(f).toString('base64');
// All product and legal text is copied verbatim from the pack currently sold (Vanilla_Tea_P.pdf, 25 bags);
// nothing is added. The 12-bag cube uses the same wording with its own count and weight.
const DISTRIBUTOR = { intro: 'Marketed and Distributed by:', name: 'Agro Ventures Exports (Pvt) Ltd,', address: 'No.48, Sir Marcus Fernando Mawatha,\nColombo 07.', web: 'www.agroventuresexports.com', email: 'info@agroventuresexports.com', hotline: 'Hot Line: 011 2 187 287' };
// GTIN from the current 25-bag, 50 g pack. A new pack size needs its own GTIN from GS1 Sri Lanka.
const GTIN = '4796034220229';
const SHAPED = JSON.parse(fs.readFileSync(path.join(root, 'brand', 'shaped-labels.json'), 'utf8'));
const logoD = fs.readFileSync(path.join(root, 'brand', 'vanilla-shop-logo.svg'), 'utf8').match(/ d="([^"]+)"/)[1];
const LOGO_VB = Number(fs.readFileSync(path.join(root, 'brand', 'vanilla-shop-logo.svg'), 'utf8').match(/viewBox="0 0 ([\d.]+) ([\d.]+)/)[1]);
// The Ceylon Tea lion (Sri Lanka Tea Board quality mark, as on the current pack), one colour in the ink.
const LION = (() => { const s = fs.readFileSync(path.join(root, 'brand', 'ceylon-tea-lion.svg'), 'utf8'); const [vw, vh] = s.match(/viewBox="0 0 ([\d.]+) ([\d.]+)/).slice(1).map(Number); return { vw, vh, d: s.match(/ d="([^"]+)"/)[1] }; })();

const BOXES = {
  cube: {
    sheet: { w: 1194.94, h: 1052.97 }, dieline: globalThis.VS_DIELINE, pack: { bags: 12, net: 24 },
    panels: {
      front: { panel: R(145.46, 390.86, 393.94, 631.07), region: R(141.258, 391.242, 393.320, 630.828) },
      sideA: { panel: R(393.94, 390.86, 633.68, 631.07), region: R(393.035, 250.227, 634.207, 656.613) },
      back: { panel: R(633.68, 390.86, 881.95, 631.07), region: R(632.051, 391.246, 882.355, 630.699) },
      sideB: { panel: R(881.95, 390.86, 1122.45, 631.07), region: R(882.137, 250.227, 1123.309, 656.613) },
      top: { panel: R(145.50, 149.85, 393.53, 390.72), region: R(142.715, 89.582, 393.961, 390.723) },
      inner: { panel: R(145.50, 630.22, 393.53, 871.09), region: R(142.715, 628.051, 393.961, 929.191) },
      bottom: { panel: R(633.68, 631.07, 881.70, 870.00), region: R(629.184, 629.949, 881.703, 881.480) },
    },
    vine: { x: -6.4, y: -3, s: 0.0525 }, lidTurn: false,
  },
  long: {
    sheet: { w: 1642.42, h: 941.328 }, dieline: globalThis.VS_DIELINE_LONG, pack: { bags: 25, net: 50 },
    panels: {
      front: { panel: R(850.5, 382.8, 1349.2, 622.9), region: R(850.5, 374.3, 1349.2, 622.9) },
      sideA: { panel: R(1349.2, 382.8, 1590.5, 622.9), region: R(1349.2, 244.7, 1599, 775.1) },
      back: { panel: R(114.9, 382.8, 611, 622.9), region: R(114.9, 382.8, 611, 622.9) },
      sideB: { panel: R(611, 382.8, 850.5, 622.9), region: R(611, 244.7, 850.5, 775.1) },
      top: { panel: R(114.9, 142.3, 611, 382.8), region: R(106.4, 82.4, 612, 382.8) },
      inner: { panel: R(850.5, 622.9, 1349.2, 862.7), region: R(842, 622.9, 1357.7, 871.2) },
      bottom: { panel: R(114.9, 622.9, 611, 862.4), region: R(106.4, 622.9, 619.5, 922.3) },
    },
    vine: { x: 60, y: -24, s: 0.052 }, lidTurn: true,
  },
};

function build(boxKey) {
  const B = BOXES[boxKey], P = B.panels, pack = B.pack;
  const size = (k) => ({ w: P[k].panel.w / MM, h: P[k].panel.h / MM });
  const L = { Background: [], Ground: [], Painting: [], Name: [], Weave: [], Type: [], Barcode: [] };
  const EST = THEME && THEMES[THEME].estate;
  let defs = '', ringPath = '';
  // Face helpers: draw in mm from a panel's top-left; rot turns the face 180 degrees (a lid hinged at the back).
  const face = (k, rot = false) => {
    const p = P[k].panel, { w, h } = size(k);
    const X = (x) => n(rot ? p.x + (w - x) * MM : p.x + x * MM), Y = (y) => n(rot ? p.y + (h - y) * MM : p.y + y * MM), S = (v) => n(v * MM);
    const tr = (x, y) => rot ? ` transform="rotate(180 ${X(x)} ${Y(y)})"` : '';
    const text = (f, s, x, y, sz, o = {}) => {
      if (INK_BOXES) INK_BOXES.push(...inkBoxes(k, f, s, x, y, sz, o));
      const a = o.anchor ? ` text-anchor="${o.anchor}"` : '';
      return `<text x="${X(x)}" y="${Y(y)}" font-family="'${FONT[f].ps}'" font-size="${S(sz)}"${o.track ? ` letter-spacing="${S(o.track)}"` : ''} fill="${o.fill || INK}"${o.opacity ? ` opacity="${o.opacity}"` : ''}${a}${tr(x, y)}>${esc(s)}</text>`;
    };
    const para = (f, s, x, y, sz, wMax, lead, o = {}) => {
      const lines = [];
      for (const raw of s.split('\n')) {
        let cur = '';
        for (const word of raw.split(' ')) { const t = cur ? cur + ' ' + word : word; if (cur && width(FONT[f], t, sz, o.track || 0) > wMax) { lines.push(cur); cur = word; } else cur = t; }
        lines.push(cur);
      }
      return { h: lines.length * lead, svg: lines.map((l, i) => text(f, l, x, y + i * lead, sz, o)).join('') };
    };
    const rule = (x1, y1, x2, y2, op = 0.5) => `<path d="M${X(x1)} ${Y(y1)}L${X(x2)} ${Y(y2)}" stroke="${INK}" stroke-opacity="${op}" stroke-width="${S(0.18)}" fill="none"/>`;
    const caps = (s, x, y, o = {}) => text('wide', s, x, y, o.size || 2.05, { track: 0.3, ...o });
    const label = (s, x, y, o = {}) => text('wideR', s, x, y, o.size || 1.85, { track: 0.3, opacity: 0.7, ...o });
    const body = (s, x, y, wMax, o = {}) => para('body', s, x, y, o.size || 2.3, wMax, o.lead || 3.2, o);
    const logo = (cx, cy, lw) => `<path d="${logoD}" fill="${INK}" fill-rule="evenodd" transform="translate(${X(cx - lw / 2)} ${Y(cy - lw * 0.52)}) scale(${n(S(lw) / LOGO_VB, 6) * (rot ? -1 : 1)})"/>`;
    const icon = (key, x, y, s) => `<g fill="none" stroke="${INK}" stroke-width="0.42" stroke-linecap="round" stroke-linejoin="round" transform="translate(${X(x)} ${Y(y)}) scale(${n(S(s), 5)})">${ICON[key]}</g>`;
    const lion = (x, y, lw) => `<path id="Ceylon_Tea_lion" d="${LION.d}" fill="${INK}" fill-rule="evenodd" transform="translate(${X(x)} ${Y(y)}) scale(${n(S(lw) / LION.vw, 6)})"/>`;
    const img = (f, x, y, wmm, hmm) => `<image xlink:href="${data(f)}" x="${X(x)}" y="${Y(y)}" width="${S(wmm)}" height="${S(hmm)}" preserveAspectRatio="none"/>`;
    return { w, h, X, Y, S, text, para, rule, caps, label, body, logo, lion, icon, img };
  };

  // ---- grounds: paper colour on every panel and flap; the painted golden ground on the four walls
  for (const [k, { region }] of Object.entries(P)) L.Background.push(`<rect x="${region.x}" y="${region.y}" width="${n(region.w)}" height="${n(region.h)}" fill="${PAPER}"/>`);
  for (const k of ['front', 'sideA', 'back', 'sideB']) {
    const F = face(k), r = P[k].region, p = P[k].panel;
    defs += `<clipPath id="clip-${k}"><rect x="${n(Math.min(r.x, p.x) - (k === 'front' ? 3 * MM : 0))}" y="${n(p.y - 3 * MM)}" width="${n(Math.max(r.w, p.w) + (k === 'front' ? 3 * MM : 0))}" height="${n(p.h + 6 * MM)}"/></clipPath>`;
    if (!THEME) L.Ground.push(`<g clip-path="url(#clip-${k})">${F.img(G(`v6-ground-golden${boxKey === 'long' ? '-long' : ''}-${k}.jpg`), -3, -3, F.w + 6, F.h + 6)}</g>`);
  }

  if (ART && THEMES[THEME].blot) for (const k of ['back', 'sideB', 'top', 'bottom']) {
    const F = face(k), r = P[k].region;
    defs += `<clipPath id="clip-pap-${k}"><rect x="${r.x}" y="${r.y}" width="${n(r.w)}" height="${n(r.h)}"/></clipPath>`;
    L.Ground.push(`<g clip-path="url(#clip-pap-${k})">${F.img(ART(k === 'top' ? 'paper-lid.jpg' : 'paper.jpg'), (F.w - 260) / 2, (F.h - 260) / 2 - 2, 260, 260)}</g>`);
  }
  if (ART && THEMES[THEME].split) {
    const F = face('sideA'), r = P.sideA.panel;
    defs += `<clipPath id="clip-split-side"><rect x="${n(r.x)}" y="${n(r.y - 3 * MM)}" width="${n(r.w + 3 * MM)}" height="${n(r.h + 6 * MM)}"/></clipPath>`;
    L.Ground.push(`<g clip-path="url(#clip-split-side)">${F.img(ART(`${boxKey}${THEMES[THEME].suffix || ''}${THEMES[THEME].blot ? '' : '-split'}-side.png`), 0, -3, F.w + 3, F.h + 6)}</g>`);
  }
  if (ART && THEMES[THEME].pattern) for (const k of ['sideA', 'back', 'sideB', 'top', 'bottom']) {
    const F = face(k), r = P[k].region;
    defs += `<clipPath id="clip-pat-${k}"><rect x="${r.x}" y="${r.y}" width="${n(r.w)}" height="${n(r.h)}"/></clipPath>`;
    L.Ground.push(`<g clip-path="url(#clip-pat-${k})">${F.img(ART('pattern.jpg'), -40, -40, 260, 260)}</g>`);
  }
  if (EST) {
    // the four walls cut from one continuous strip (3 mm bleed each side), so the picture runs across the folds; the
    // lid's dark sky drawn over the front's top bleed and 3 mm past its other edges
    for (const k of ['front', 'sideA', 'back', 'sideB']) { const F = face(k); L.Ground.push(`<g clip-path="url(#clip-${k})">${F.img(ART(`est-${k}.jpg`), -3, -3, F.w + 6, F.h + 6)}</g>`); }
    const F = face('top'), p = P.top.panel;
    defs += `<clipPath id="clip-lid-art"><rect x="${n(p.x - 3 * MM)}" y="${n(p.y - 3 * MM)}" width="${n(p.w + 6 * MM)}" height="${n(p.h + 6 * MM)}"/></clipPath>`;
    L.Ground.push(`<g clip-path="url(#clip-lid-art)">${F.img(ART('est-lid.jpg'), -3, -3, F.w + 6, F.h + 6)}</g>`);
  }
  if (ART && !EST) { const F = face('front'); L.Ground.push(`<g clip-path="url(#clip-front)">${F.img(ART(THEMES[THEME].split ? `${boxKey}${THEMES[THEME].suffix || ''}${THEMES[THEME].blot ? '' : '-split'}-front.png` : `${boxKey}-${THEME}.png`), -3, -3, F.w + 6, F.h + 6)}</g>`); }
  // ---- painting: one placement for the vine across front and right side
  if (!ART) {
    const F = face('front'), V = B.vine, vine = F.img(G('v6-vine-faded.png'), V.x, V.y, 3808 * V.s, 1651 * V.s);
    const fa = P.front.panel, sa = P.sideA.panel;
    defs += `<clipPath id="clip-walls"><rect x="${n(fa.x - 3 * MM)}" y="${n(fa.y - 0.5 * MM)}" width="${n(sa.x + sa.w - fa.x + 3 * MM)}" height="${n(fa.h + 3.5 * MM)}"/></clipPath>`;
    L.Painting.push(`<g id="Vine" clip-path="url(#clip-walls)">${vine}</g>`);
  }
  // A panel heading in the serif italic sitting on a rule, at the height of the front's top bar, so the bars
  // read as one band round the box.
  const head = (F, s, x0, x1, right) => F.text('title', s, x0, 10.9, 6) + F.rule(x0, 12.8, x1, 12.8) + (right ? F.caps(right, x1, 10.4, { anchor: 'end', size: 1.85 }) : '');

  // ---- front
  if (!EST) {
    const F = face('front'), t = [];
    if (ART && THEMES[THEME].split) {
      // Cream left of the split: signature, pack line, the name stacked large, the plain-words line.
      const cube = boxKey === 'cube', x = cube ? 8 : 9, lw = cube ? 10 : 11, ln = cube ? 11.5 : 12.5, lnh = ln * LION.vh / LION.vw, ty = 6.5;
      t.push(F.logo(x + lw / 2, ty + lw * 0.52, lw), F.rule(x + lw + 3.5, ty, x + lw + 3.5, ty + lnh, 0.4), F.lion(x + lw + 7, ty, ln));
      // the pack line one cap-height under the signature; the name optically on the margin (italic overhang); the
      // plain-words line a fixed 7 mm under the last baseline, so the foot margin matches the top on both cartons
      t.push(F.caps('AUTHENTIC CEYLON', x, 22.5), F.caps(`${pack.bags} TEA BAGS · ${pack.net} G`, x, 26.3));
      if (THEMES[THEME].cin) {
        const sz = cube ? 13 : 17, b1 = cube ? 40 : 42;
        L.Name.push(F.text('title', 'Vanilla &', x - 1, b1, sz, { fill: GOLD }), F.text('title', 'Cinnamon', x - 1, b1 + 0.8 * sz, sz), F.text('title', 'Tea', x - 1, b1 + 1.6 * sz, sz));
        t.push(F.body('Vanilla and cinnamon blended\nwith pure Ceylon tea', x, b1 + 1.6 * sz + 7, 60, { size: cube ? 2.2 : 2.4, lead: 3.2 }).svg);
      } else {
        const sz = cube ? 16.5 : 23, b1 = cube ? 46 : 50;
        L.Name.push(F.text('title', 'Vanilla', x - 1.2, b1, sz, { fill: GOLD }), F.text('title', 'Tea', x - 1.2, b1 + 0.8 * sz, sz));
        t.push(F.body('Ceylon black tea\nwith natural vanilla', x, b1 + 0.8 * sz + 7, 44, { size: cube ? 2.3 : 2.5, lead: cube ? 3.2 : 3.4 }).svg);
      }
    } else if (ART && THEMES[THEME].pattern) {
      // The name large on the cream; the signature top left; the pack line top right; the band below is the picture.
      const cube = boxKey === 'cube', x = cube ? 8 : 9, rx = F.w - 8, lw = cube ? 10 : 11, ln = cube ? 11.5 : 12.5, lnh = ln * LION.vh / LION.vw, ty = 6.5;
      t.push(F.logo(x + lw / 2, ty + lw * 0.52, lw), F.rule(x + lw + 3.5, ty, x + lw + 3.5, ty + lnh, 0.4), F.lion(x + lw + 7, ty, ln));
      t.push(F.caps('AUTHENTIC CEYLON', rx, 10.6, { anchor: 'end' }), F.caps(`${pack.bags} TEA BAGS · ${pack.net} G`, rx, 14.4, { anchor: 'end' }));
      const shade = process.env.TEA_CREAM === 'shadow';   // no band: the name sits in the quiet middle, the line under it
      if (cube) {
        const sz = shade ? 18 : 16.5, b1 = shade ? 45 : 34;
        L.Name.push(F.text('title', 'Vanilla', 7, b1, sz, { fill: GOLD }), F.text('title', 'Tea', 7, b1 + 0.8 * sz, sz));
        if (shade) t.push(F.body('Ceylon black tea\nwith natural vanilla', 8, b1 + 0.8 * sz + 9, 40, { size: 2.4, lead: 3.3 }).svg);
        else t.push(F.body('Ceylon black tea\nwith natural vanilla', rx, 41, 30, { size: 2.3, lead: 3.2, anchor: 'end' }).svg);
      } else {
        const sz = shade ? 27 : 25, b = shade ? 53 : 40;
        L.Name.push(F.text('title', 'Vanilla', 8, b, sz, { fill: GOLD }), F.text('title', 'Tea', 8 + width(FONT.title, 'Vanilla ', sz), b, sz));
        if (shade) t.push(F.body('Ceylon black tea with natural vanilla', 9, b + 10, 80, { size: 2.6 }).svg);
        else t.push(F.body('Ceylon black tea\nwith natural vanilla', rx, 34.4, 40, { size: 2.5, lead: 3.4, anchor: 'end' }).svg);
      }
    } else if (ART && process.env.TEA_SIG === 'left') {
      // The signature (logo and lion) top left in place of the shop's name; the information under it; the name on the
      // foot rule bottom left; the whole right half left to the painting.
      const cube = boxKey === 'cube', x = cube ? 8 : 9, lw = cube ? 10 : 11, ln = cube ? 11.5 : 12.5, lnh = ln * LION.vh / LION.vw, ty = 6.5;
      t.push(F.logo(x + lw / 2, ty + lw * 0.52, lw), F.rule(x + lw + 3.5, ty, x + lw + 3.5, ty + lnh, 0.4), F.lion(x + lw + 7, ty, ln));
      if (cube) {
        t.push(F.rule(8, 21, 46, 21), F.caps('AUTHENTIC CEYLON', 8, 26.2), F.caps(`${pack.bags} TEA BAGS · ${pack.net} G`, 8, 30));
        t.push(F.body('Ceylon black tea\nwith natural vanilla', 8, 35.6, 40, { size: 2.4, lead: 3.3 }).svg);
        const sz = 19;
        L.Name.push(F.text('title', 'Vanilla', 7, F.h - 9 - 0.78 * sz, sz, { fill: GOLD }), F.text('title', 'Tea', 7, F.h - 9, sz));
      } else {
        t.push(F.caps('NO. 01', 96, 12, { anchor: 'end' }), F.rule(9, 21, 96, 21));
        t.push(F.label('BLEND', 9, 27.5), F.caps('CEYLON BLACK TEA', 9, 31.5), F.caps('NATURAL VANILLA', 9, 34.9));
        t.push(F.label('ORIGIN', 48, 27.5), F.caps('AUTHENTIC CEYLON', 48, 31.5));
        t.push(F.label('CONTENTS', 9, 40.9), F.caps(`${pack.bags} TEA BAGS · ${pack.net} G`, 9, 44.9));
        const sz = 26;
        L.Name.push(F.text('title', 'Vanilla', 8, F.h - 9, sz, { fill: GOLD }), F.text('title', 'Tea', 8 + width(FONT.title, 'Vanilla ', sz), F.h - 9, sz));
      }
      t.push(F.rule(cube ? 8 : 9, F.h - 5, cube ? 46 : 113, F.h - 5));
    } else if (ART) {
      // One layout for both boxes: information top left, the logo and the lion together top right as one signature,
      // the name on the foot rule bottom left, the drawing rising from the bottom right corner.
      const rx = F.w - 8, cube = boxKey === 'cube', ln = cube ? 11 : 12, lnh = ln * LION.vh / LION.vw, lw = cube ? 9.5 : 10, ty = 6.5;
      t.push(F.lion(rx - ln, ty, ln), F.rule(rx - ln - 3.5, ty, rx - ln - 3.5, ty + lnh, 0.4), F.logo(rx - ln - 7 - lw / 2, ty + lw * 0.52, lw));
      if (cube) {
        t.push(F.caps('AUTHENTIC CEYLON', 8, 10.4), F.caps(`${pack.bags} TEA BAGS · ${pack.net} G`, 8, 14.2), F.rule(8, 16.8, 46, 16.8));
        t.push(F.body('Ceylon black tea\nwith natural vanilla', 8, 22.4, 40, { size: 2.4, lead: 3.3 }).svg);
        const sz = 19;
        L.Name.push(F.text('title', 'Vanilla', 7, F.h - 9 - 0.78 * sz, sz, { fill: GOLD }), F.text('title', 'Tea', 7, F.h - 9, sz));
      } else {
        t.push(F.caps('THE VANILLA SHOP', 9, 12), F.caps('NO. 01', 96, 12, { anchor: 'end' }), F.rule(9, 15, 96, 15));
        t.push(F.label('BLEND', 9, 23), F.caps('CEYLON BLACK TEA', 9, 27), F.caps('NATURAL VANILLA', 9, 30.4));
        t.push(F.label('ORIGIN', 48, 23), F.caps('AUTHENTIC CEYLON', 48, 27));
        t.push(F.label('CONTENTS', 9, 36.4), F.caps(`${pack.bags} TEA BAGS · ${pack.net} G`, 9, 40.4));
        const sz = 26;
        L.Name.push(F.text('title', 'Vanilla', 8, F.h - 9, sz, { fill: GOLD }), F.text('title', 'Tea', 8 + width(FONT.title, 'Vanilla ', sz), F.h - 9, sz));
      }
      t.push(F.rule(cube ? 8 : 9, F.h - 5, cube ? 46 : 113, F.h - 5));
    } else if (boxKey === 'cube') {
      // Top bar; the name high, two lines; the product line; the logo bottom left on the same edge.
      const r = F.w - 8, sz = 20, asc = 0.72 * sz, top = 16.5, b1 = top + asc, b2 = b1 + 0.78 * sz;
      t.push(F.caps('AUTHENTIC CEYLON', 8, 10.4), F.caps(`${pack.bags} TEA BAGS · ${pack.net} G`, r, 10.4, { anchor: 'end' }), F.rule(8, 12.8, r, 12.8));
      L.Name.push(F.text('title', 'Vanilla', 7, b1, sz, THEME ? { fill: GOLD } : {}), F.text('title', 'Tea', 7, b2, sz));
      t.push(F.body('Ceylon black tea\nwith natural vanilla', 8, b2 + 8.8, 40, { size: 2.5, lead: 3.4 }).svg);
      // The lion top right, its top level with the name's capitals and its right edge on the bar's end.
      t.push(F.lion(r - 14, top, 14));
      const lw = 13.5;
      t.push(F.logo(8 + lw / 2, F.h - 7.5 - lw * 963 / 933 + lw * 0.52, lw));
    } else {
      // Ruled bar and data columns on top, the vine across the top right, the name along the foot.
      const bar = 96, sz = 26;
      t.push(F.caps('THE VANILLA SHOP', 9, 12), F.caps('NO. 01', bar, 12, { anchor: 'end' }), F.rule(9, 15, bar, 15));
      t.push(F.label('BLEND', 9, 23), F.caps('CEYLON BLACK TEA', 9, 27), F.caps('NATURAL VANILLA', 9, 30.4));
      t.push(F.label('ORIGIN', 48, 23), F.caps('AUTHENTIC CEYLON', 48, 27));
      t.push(F.label('CONTENTS', 9, 36.4), F.caps(`${pack.bags} TEA BAGS · ${pack.net} G`, 9, 40.4));
      if (THEME) L.Name.push(F.text('title', 'Vanilla', 8, F.h - 9, sz, { fill: GOLD }), F.text('title', 'Tea', 8 + width(FONT.title, 'Vanilla ', sz), F.h - 9, sz));
      else L.Name.push(F.text('title', 'Vanilla Tea', 8, F.h - 9, sz));
      // Bottom right, under the painting: the logo and the Ceylon Tea lion standing on the name's baseline,
      // split by a fine rule, the lion's right edge on the panel margin; the foot rule runs the full width.
      const base = F.h - 9, rx = F.w - 8, ln = 15, lnh = ln * LION.vh / LION.vw, lw = 14, lh = lw * 963 / 933;
      t.push(F.lion(rx - ln, base - lnh, ln), F.rule(rx - ln - 4.5, base - lnh, rx - ln - 4.5, base, 0.4));
      t.push(F.logo(rx - ln - 9 - lw / 2, base - lh + lw * 0.52, lw));
      t.push(F.rule(9, F.h - 5, rx, F.h - 5));
    }
    L.Type.push(`<g id="Front">${t.join('')}</g>`);
  }

  // ---- right side: how to brew as a numbered stepper; pack line at the foot
  if (!EST) {
    const F = face('sideA'), t = [], sx = boxKey === 'cube' ? 40 : 8, r = boxKey === 'cube' ? F.w - 8 : F.w - 30, sy = 18;
    if (boxKey === 'long' && !ART) L.Painting.push(F.img(G('v6-climb.png'), F.w - 2 - 612 * 0.035, F.h + 1.5 - 2000 * 0.035, 667 * 0.035, 2000 * 0.035));
    t.push(head(F, 'How to brew', sx, r));
    // Line icons in the same style as the contents panel, joined by a fine line.
    const steps = [['cup', '150 ML', 'One tea bag in hot water'], ['timer', '5 MINUTES', 'Then lift the bag out'], ['ice', 'OVER ICE', 'Let it cool, pour over ice']];
    const is = 6.6, gap = 14, tx = sx + is + 3;
    steps.forEach(([ic, h, d], i) => {
      const y = sy + i * gap;
      if (i) t.push(`<path d="M${F.X(sx + is / 2)} ${F.Y(y - gap + is + 1)}V${F.Y(y - 1)}" stroke="${INK}" stroke-opacity=".35" stroke-width="${F.S(0.22)}"/>`);
      t.push(F.icon(ic, sx, y, is / 10));
      t.push(F.text('wideR', h, tx, y + 2.6, 2.2, { track: 0.3 }), F.body(d, tx, y + 5.9, 30, { size: 2.1, lead: 2.9 }).svg);
    });
    const lift = boxKey === 'long' && ['wgreen', 'wsage'].includes(THEME) ? 8 : 0;   // clear of the pod tip at the fold
    t.push(F.rule(sx, F.h - 11.4 - lift, r, F.h - 11.4 - lift), F.caps(`${pack.bags} TEA BAGS · 2 G EACH · ${pack.net} G`, sx, F.h - 7.5 - lift, { size: 1.9 }));
    L.Type.push(`<g id="Side_How_to_brew">${ART && THEMES[THEME].split && !THEMES[THEME].blot ? t.join('').replaceAll(INK, '#F6EEDC') : t.join('')}</g>`);   // on the teal, the side's type turns cream
  }

  // ---- back: the line, then the labelled plate of vanilla
  const backPlate = (F, ox, w) => {
    const t = [], s = 56 / 1485, x0 = ox + w - 5 - 1000 * s, y0 = 19;
    const at = (px, py) => [x0 + px * s, y0 + py * s];
    if (!ART) L.Painting.push(F.img(G('v6-diagram-soft.png'), x0, y0, 1000 * s, 1485 * s));
    t.push(head(F, 'Vanilla was never plain.', ox + 8, ox + w - 8));
    if (ART) {   // no plate to label: the line alone, larger
      t.push(F.body('The delicate sweetness of natural vanilla unfolds through warm, comforting notes and a smooth, mellow aroma.', ox + 8, 21, w - 22, { size: 3.2, lead: 4.4 }).svg);
      return t.join('');
    }
    t.push(F.body('The delicate sweetness of natural vanilla unfolds through warm, comforting notes and a smooth, mellow aroma.', ox + 8, 19.6, 37, { size: 2.2, lead: 3.0 }).svg);
    [['VANILLA ORCHID', 'Hand-pollinated; open for one day', at(545, 330)],
      ['AERIAL ROOTS', 'The vine climbs by them', at(165, 560)],
      ['CEYLON TEA', 'Two leaves and a bud', at(330, 1065)],
      ['GREEN PODS', 'Ripen for about nine months', at(470, 980)],
      ['CURED POD', 'Sweated and dried for months', at(585, 1270)]].forEach(([k, note, [px, py]], i) => {
      const y = 46 + i * 6.8, lw = Math.max(width(FONT.wide, k, 1.75, 0.25), width(FONT.body, note, 2.0));
      t.push(F.text('wide', k, ox + 8, y, 1.75, { track: 0.25 }), F.text('body', note, ox + 8, y + 2.7, 2.0, { opacity: 0.85 }));
      const sx = ox + 8 + lw + 1.6, sy = y - 0.6;
      if (!ART) t.push(`<path d="M${F.X(sx)} ${F.Y(sy)}H${F.X(Math.min(px - 3, sx + 4))}L${F.X(px)} ${F.Y(py)}" fill="none" stroke="${INK}" stroke-width="${F.S(0.14)}"/><circle cx="${F.X(px)}" cy="${F.Y(py)}" r="${F.S(0.55)}" fill="${INK}"/>`);
    });
    return t.join('');
  };
  // Declarations are set at 1.5 mm letter height (x-height for body text, cap height for capitals), the Sri
  // Lankan 2026 minimum; see research/label-text-rules.md.
  const DECL = { body: 3.05, caps: 2.3, lead: 4.2 };
  // What's inside: the three icons, then the bag count and net weight as worded on the current pack.
  const inside = (F, ox, w) => {
    const t = [], r = ox + w - 8, cw = (w - 16) / 3;
    t.push(head(F, 'What’s inside', ox + 8, r));
    [['tea', 'CEYLON TEA'], ['pod', 'NATURAL VANILLA'], ['teabag', `${pack.bags} TEA BAGS`]].forEach(([ic, k], i) => {
      const cx = ox + 8 + cw * (i + 0.5);
      if (i) t.push(F.rule(ox + 8 + cw * i, 15.5, ox + 8 + cw * i, 27.5, 0.35));
      t.push(F.icon(ic, cx - 3.2, 15.6, 0.64), F.text('wide', k, cx, 26.2, 1.6, { track: 0.15, anchor: 'middle' }));
    });
    t.push(F.rule(ox + 8, 29.5, r, 29.5, 0.35));
    t.push(F.text('wideR', 'TEA BAGS', ox + 8, 35, DECL.caps, { track: 0.3, opacity: 0.75 }));
    t.push(F.body(`${pack.bags} tagged unbleached sachet tea bags`, ox + 8, 39.6, w - 16, { size: DECL.body, lead: DECL.lead }).svg);
    t.push(F.text('wideR', 'NET WEIGHT', ox + 8, 48, DECL.caps, { track: 0.3, opacity: 0.75 }));
    t.push(F.body(`${pack.net}g (2g x ${pack.bags})`, ox + 8, 52.6, w - 16, { size: DECL.body, lead: DECL.lead }).svg);
    return t.join('');
  };
  // Batch block (Sinhala, English, Tamil), barcode, distributor.
  const baseInfo = (F, ox, w) => {
    const t = [], r = ox + w - 8;
    t.push(head(F, 'Vanilla Tea', ox + 8, r, 'BATCH DETAILS'));
    [['කා.අ.', 'B.N.', 'தொகுதி இல'], ['නි.දි.', 'MFD.', 'பொ.செ திகதி'],
      ['කා.ඉ.දි.', 'EXP.', 'மு.திகதி'], ['උ.සි.මි.රු.', 'MRP. Rs.', 'விலைரூபா']].forEach(([si, en, ta], i) => {
      // English label on the line with the stamp line; Sinhala and Tamil together underneath.
      const y = 20.2 + i * 7.4, wsi = SHAPED[si].advance * 2.2;
      t.push(F.text('wideR', en, ox + 8, y, DECL.caps, { track: 0.25 }), shaped(F, si, 2.2, ox + 8, y + 3.6), shaped(F, ta, 2.0, ox + 8 + wsi + 2, y + 3.6));
      t.push(`<path d="M${F.X(ox + 21)} ${F.Y(y + 0.4)}H${F.X(ox + 42)}" stroke="${INK}" stroke-opacity=".6" stroke-width="${F.S(0.15)}" stroke-dasharray="${F.S(0.4)} ${F.S(0.4)}" fill="none"/>`);
    });
    L.Barcode.push(barcode(F, GTIN, r, 46));
    // Name and address are mandatory (1.5 mm); web, email and hotline are extra and set smaller.
    t.push(F.rule(ox + 8, 50.6, r, 50.6), F.body(DISTRIBUTOR.intro, ox + 8, 55.2, w - 16, { size: DECL.body }).svg);
    t.push(F.body(`${DISTRIBUTOR.name}\n${DISTRIBUTOR.address}`, ox + 8, 59.6, w - 16, { size: DECL.body, lead: DECL.lead }).svg);
    t.push(F.body(`${DISTRIBUTOR.web}\n${DISTRIBUTOR.email}\n${DISTRIBUTOR.hotline}`, ox + 8, 73, w - 16, { size: 2.2, lead: 3.0 }).svg);
    return t.join('');
  };

  // ---- the Estate: every wall on one 6 mm margin, the type in the cream under the curve (heights from wrap.py's
  // edge, at least 3 mm clear); headings in the serif italic, as the front's "Tea"; the lid the sky with the emblem
  // ring and logo in cream; the base cream with the batch block, barcode and distributor.
  function estatePanels() {
    const M = 6, CREAM = PAPER, cream = (s) => s.replaceAll(`fill="${INK}"`, `fill="${CREAM}"`).replaceAll(`stroke="${INK}"`, `stroke="${CREAM}"`);
    const hd = (F, s, x, y, wMax) => F.text('title', s, x, y, Math.min(7, wMax / width(FONT.title, s, 1)));
    {   // front: logo in the top-right corner; Vanilla over Tea, the facts beneath, the lion on the last baseline
      // the small lines at 1.75 mm, tracked tighter so they hold their own under the name; the gaps tightened to match,
      // so the name keeps its place under the curve
      const F = face('front'), base = F.h - M, t = [], sz = 17, cs = 1.75, d1 = base - 3.7, tb = d1 - 0.71 * cs - 3.2, vb = tb - 0.78 * sz, lw = 15, ln = 8.4;
      t.push(cream(F.logo(F.w - M - 927.6 * lw / 933 + lw / 2, M - 6.3 * lw / 933 + 0.52 * lw, lw)));      // ink box from brand/vanilla-shop-logo.svg
      L.Name.push(F.text('roman', 'Vanilla', M + 0.018 * sz, vb, sz, { fill: GOLD }), F.text('title', 'Tea', M, tb, sz));
      t.push(F.text('wideR', 'CEYLON BLACK TEA WITH NATURAL VANILLA', M, d1, cs, { track: 0.16 }));
      t.push(F.text('wideR', `${pack.bags} TEA BAGS  ·  NET WT. ${pack.net} g`, M, base, cs, { track: 0.16 }));
      t.push(F.lion(F.w - M - 1206 * ln / LION.vw, base - 890 * ln / LION.vw, ln));                         // ink box from the lion SVG
      L.Type.push(`<g id="Front">${t.join('')}</g>`);
    }
    {   // right side: how to brew, a column clear of the valley at the fold, the last line on the bottom margin
      // the column sits past the boundary's trough (a quarter into the panel), the heading 3.4 mm under the rising edge
      const SP = THEMES[THEME].sidePlum;
      const steps = [['cup', '150 ML', 'One tea bag in hot water'], ['timer', '5 MINUTES', 'Then lift the bag out'], ['ice', 'OVER ICE', 'Let it cool, pour over ice']];
      const F = face('sideA'), base = F.h - M, t = [];
      if (SP) {
        // the guide as one block centred between 12% margins (text still left-aligned): the heading, then three rows,
        // icons in one column centred on their two lines, the label (cap) over its explanation; rows spread evenly
        // from under the heading to the bottom margin. Sizes about 1.2x the cream-panel version.
        const mg = 0.12 * F.w, is = 6, gap = 3.2, ls = 2.8, lt = 0.25, bs = 2.6, lb = 2.0, eb = 4.8, hs = 7, hb = 54.6;   // label and explanation tight; rows apart
        const tw = Math.max(...steps.map(([, h, d]) => Math.max(width(FONT.wideR, h, ls, lt), width(FONT.body, d, bs))));
        const gw = Math.max(is + gap + tw, width(FONT.title, 'How to brew', hs)), x0 = mg + (F.w - 2 * mg - gw) / 2, tx = x0 + is + gap;
        const r1 = hb + 3.2, r3 = base - eb, pitch = (r3 - r1) / 2;
        t.push(F.text('title', 'How to brew', x0, hb, hs));
        steps.forEach(([ic, h, d], i) => {
          const y = r1 + i * pitch;
          t.push(F.icon(ic, x0, y + eb / 2 - is / 2, is / 10), F.text('wideR', h, tx, y + lb, ls, { track: lt }), F.text('body', d, tx, y + eb, bs));
        });
      } else {
        const x0 = 44, is = 5, pitch = 6.0, tx = x0 + is + 2.6; t.push(hd(F, 'How to brew', x0, 58.3, F.w - M - x0));
        const bs = Math.min(2.3, ...steps.map(([, , d]) => (F.w - M - tx) / width(FONT.body, d, 1)));   // body fits the column
        steps.forEach(([ic, h, d], i) => {
          const y = base - 4.8 - (2 - i) * pitch;
          t.push(F.icon(ic, x0, y - 0.2, is / 10), F.text('wideR', h, tx, y + 1.9, 1.7, { track: 0.3 }), F.text('body', d, tx, y + 4.8, bs));
        });
      }
      L.Type.push(`<g id="Side_How_to_brew">${SP ? cream(t.join('')) : t.join('')}</g>`);
    }
    {   // back: the line, the description, a closing line on the bottom margin
      const F = face('back'), base = F.h - M, t = [hd(F, 'Vanilla was never plain.', M, 56, F.w - 2 * M)];
      // a narrow paragraph broken by phrase; a clear pause; then the own-farms line on the bottom margin as the takeaway
      ['The delicate sweetness of natural vanilla', 'unfolds through warm, comforting notes', 'and a smooth, mellow aroma.'].forEach((l, i) => t.push(F.text('body', l, M, 61.4 + i * 3.75, 2.75)));
      t.push(F.text('title', 'Made with vanilla grown on our own farms.', M, base, 4.1));
      L.Type.push(`<g id="Back">${t.join('')}</g>`);
    }
    {   // left side: what's inside, the declarations at the 1.5 mm minimum (DECL), the net weight on the bottom margin
      const F = face('sideB'), base = F.h - M, t = [hd(F, 'What’s inside', M, 56, F.w - 2 * M)];
      t.push(F.text('wideR', 'TEA BAGS', M, 61.6, DECL.caps, { track: 0.3, opacity: 0.75 }), F.body(`${pack.bags} tagged unbleached sachet tea bags`, M, 66, F.w - 2 * M, { size: DECL.body, lead: DECL.lead }).svg);
      t.push(F.text('wideR', 'NET WEIGHT', M, base - 4.4, DECL.caps, { track: 0.3, opacity: 0.75 }), F.body(`${pack.net}g (2g x ${pack.bags})`, M, base, F.w - 2 * M, { size: DECL.body }).svg);
      L.Type.push(`<g id="Side_Whats_inside">${t.join('')}</g>`);
    }
    const Fo = face('bottom'); L.Type.push(`<g id="Base">${baseInfo(Fo, 0, Fo.w)}</g>`);
    {   // lid: the emblem ring and the logo in cream on the sky
      const F = face('top'), cx = F.w / 2, cy = F.h / 2, r = 22, ring = 'SAVOR THE CALM · AUTHENTIC CEYLON VANILLA TEA · ';
      const track = (2 * Math.PI * r - width(FONT.wide, ring, 2.5)) / ring.length;
      ringPath = `M${F.X(cx - r)} ${F.Y(cy)}A${F.S(r)} ${F.S(r)} 0 1 1 ${F.X(cx + r)} ${F.Y(cy)}A${F.S(r)} ${F.S(r)} 0 1 1 ${F.X(cx - r)} ${F.Y(cy)}`;
      defs += `<path id="ring" d="${ringPath}"/>`;
      L.Type.push(cream(`<g id="Lid"><circle cx="${F.X(cx)}" cy="${F.Y(cy)}" r="${F.S(25.6)}" fill="none" stroke="${INK}" stroke-opacity=".5" stroke-width="${F.S(0.18)}"/>` +
        `<circle cx="${F.X(cx)}" cy="${F.Y(cy)}" r="${F.S(18.6)}" fill="none" stroke="${INK}" stroke-opacity=".5" stroke-width="${F.S(0.18)}"/>` +
        `<text font-family="'${FONT.wide.ps}'" font-size="${F.S(2.5)}" letter-spacing="${F.S(track)}" fill="${INK}"><textPath xlink:href="#ring">${esc(ring)}</textPath></text>` +
        F.logo(cx, cy, 19) + '</g>'));
    }
  }
  if (EST) estatePanels();
  else if (boxKey === 'cube') {
    const Fb = face('back'); L.Type.push(`<g id="Back">${backPlate(Fb, 0, Fb.w)}</g>`);
    const Fs = face('sideB'); L.Type.push(`<g id="Side_Whats_inside">${inside(Fs, 0, Fs.w)}</g>`);
    const Fo = face('bottom'); L.Type.push(`<g id="Base">${baseInfo(Fo, 0, Fo.w)}</g>`);
  } else {
    const Fb = face('back'), half = 87.58;
    L.Type.push(`<g id="Back">${backPlate(Fb, 0, half)}${Fb.rule(half + 1.5, 18, half + 1.5, Fb.h - 10, 0.35)}${inside(Fb, half, Fb.w - half)}</g>`);
    const Fs = face('sideB'); L.Type.push(`<g id="Side_Batch_and_barcode">${baseInfo(Fs, 0, Fs.w)}</g>`);
    const Fo = face('bottom');
    L.Type.push(`<g id="Base">${Fo.logo(Fo.w / 2, Fo.h / 2 - 3, 24)}${Fo.caps('AUTHENTIC CEYLON VANILLA TEA', Fo.w / 2, Fo.h / 2 + 13, { anchor: 'middle' })}</g>`);
  }

  // ---- lid: two sprigs reaching in from opposite corners (from the vine set) frame the emblem ring (from the
  // candles). A long-box lid hangs off the back, so its whole group is turned to read from the front.
  if (!EST) {
    const F = face('top'), cx = F.w / 2, cy = F.h / 2 - 2, r = 22, ring = THEME && THEMES[THEME].cin ? 'SAVOR THE CALM · VANILLA & CINNAMON CEYLON TEA · ' : 'SAVOR THE CALM · AUTHENTIC CEYLON VANILLA TEA · ';
    const len = 2 * Math.PI * r, track = (len - width(FONT.wide, ring, 2.5)) / ring.length;
    ringPath = `M${F.X(cx - r)} ${F.Y(cy)}A${F.S(r)} ${F.S(r)} 0 1 1 ${F.X(cx + r)} ${F.Y(cy)}A${F.S(r)} ${F.S(r)} 0 1 1 ${F.X(cx - r)} ${F.Y(cy)}`;
    defs += `<path id="ring" d="${ringPath}"/>`;
    const ss = 0.024, sw = 1448 * ss, sh = 1086 * ss, p = P.top.panel, pcx = n(p.x + p.w / 2), pcy = n(p.y + p.h / 2);
    const sprig = F.img(G('v6-sprig.png'), F.w + 1.5 - sw, 1.5 - 168 * ss, sw, sh);
    defs += `<clipPath id="clip-lid"><rect x="${p.x}" y="${p.y}" width="${n(p.w)}" height="${n(p.h)}"/></clipPath>`;
    const turn = B.lidTurn ? ` transform="rotate(180 ${pcx} ${pcy})"` : '';
    if (!ART) L.Painting.push(`<g id="Lid_sprigs" clip-path="url(#clip-lid)"><g${turn}>${sprig}<g transform="rotate(180 ${pcx} ${pcy})">${sprig}</g></g></g>`);
    const fy = F.h - 8.6;
    L.Type.push(`<g id="Lid"${turn}><circle cx="${F.X(cx)}" cy="${F.Y(cy)}" r="${F.S(25.6)}" fill="none" stroke="${INK}" stroke-opacity=".5" stroke-width="${F.S(0.18)}"/>` +
      `<circle cx="${F.X(cx)}" cy="${F.Y(cy)}" r="${F.S(18.6)}" fill="none" stroke="${INK}" stroke-opacity=".5" stroke-width="${F.S(0.18)}"/>` +
      `<text font-family="'${FONT.wide.ps}'" font-size="${F.S(2.5)}" letter-spacing="${F.S(track)}" fill="${INK}"><textPath xlink:href="#ring">${esc(ring)}</textPath></text>` +
      F.logo(cx, cy, 19) + '</g>');
    if (B.lidTurn) ringPath = `M0 0`;   // the turned ring is inside a transformed group; no free guide path
  }

  if (EST) defs += '<linearGradient id="foil" x1="0" y1="0" x2="1" y2="0.3"><stop offset="0" stop-color="#8A6424"/><stop offset=".25" stop-color="#D9B465"/>' +
    '<stop offset=".5" stop-color="#A27A30"/><stop offset=".75" stop-color="#E6C77E"/><stop offset="1" stop-color="#946B28"/></linearGradient>';   // the front studies' gold
  else if (THEME && THEMES[THEME].light) defs += '<linearGradient id="foil" x1="0" y1="0" x2="1" y2="0.4"><stop offset="0" stop-color="#4A2C06"/><stop offset="0.3" stop-color="#8C5F1C"/>' +
    '<stop offset="0.5" stop-color="#5E3E0C"/><stop offset="0.75" stop-color="#9C7028"/><stop offset="1" stop-color="#4A2C06"/></linearGradient>';
  else if (THEME) defs += '<linearGradient id="foil" x1="0" y1="0" x2="1" y2="0.4"><stop offset="0" stop-color="#9A7230"/><stop offset="0.3" stop-color="#E9CB80"/>' +
    '<stop offset="0.5" stop-color="#B08336"/><stop offset="0.75" stop-color="#F2D995"/><stop offset="1" stop-color="#9A7230"/></linearGradient>';
  const tile = grainTile({ dpi: 600, clump: 0.5 });
  defs += `<pattern id="grain" patternUnits="userSpaceOnUse" width="${n(tile.mm * MM)}" height="${n(tile.mm * MM)}"><image xlink:href="${tile.href}" width="${n(tile.mm * MM)}" height="${n(tile.mm * MM)}"/></pattern>`;
  defs += `<clipPath id="clip-all">${Object.values(P).map(({ region: r }) => `<rect x="${r.x}" y="${r.y}" width="${n(r.w)}" height="${n(r.h)}"/>`).join('')}</clipPath>`;
  const g = (id, b) => `<g id="${id}">${b}</g>`;
  return `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="${B.sheet.w}pt" height="${B.sheet.h}pt" viewBox="0 0 ${B.sheet.w} ${B.sheet.h}">` +
    `<title>The Vanilla Shop: Natural Vanilla Tea, ${pack.bags} bags</title><defs>${defs}</defs>` +
    g('Background', L.Background.join('')) + g('Ground', L.Ground.join('')) + g('Painting', L.Painting.join('')) + g('Name', L.Name.join('')) + g('Weave', L.Weave.join('')) +
    g('Texture', `<rect width="${B.sheet.w}" height="${B.sheet.h}" fill="url(#grain)" opacity="${EST ? '.25' : '.55'}" clip-path="url(#clip-all)"/>`) +
    g('Type_and_Icons', L.Type.join('')) + g('Barcode', L.Barcode.join('')) +
    g('Lid_ring_path', `<path d="${ringPath}" fill="none" stroke="none"/>`) +
    g('Dieline', B.dieline.replace(/stroke="#B[0-9A-F]{5}"/g, 'stroke="#E4007C"')) + '</svg>';
}

function shaped(F, s, sz, x, y, op = 0.8) {
  const gl = SHAPED[s];
  if (!gl) throw new Error('Label not shaped: ' + s);
  return `<path d="${gl.d}" fill="${INK}" opacity="${op}" transform="translate(${F.X(x)} ${F.Y(y)}) scale(${n(F.S(sz), 5)})"/>`;
}

// Line icons on a 10 x 10 grid.
const ICON = {
  cup: '<path d="M1.6 4.2H7.2V6.6C7.2 8.2 6 9.2 4.4 9.2S1.6 8.2 1.6 6.6Z"/><path d="M7.2 5H8C8.9 5 9.2 5.6 9.2 6.2S8.9 7.4 8 7.4H7.1"/><path d="M3.4 1.2c-.6.7.6 1.2 0 2M5.4 1.2c-.6.7.6 1.2 0 2"/>',
  timer: '<circle cx="5" cy="5.6" r="3.5"/><path d="M5 5.6V3.5M5 5.6L6.6 6.6M4 1H6M5 1V2.1"/>',
  ice: '<path d="M2 1.6H8L7.2 9.2H2.8Z"/><rect x="3.3" y="4.6" width="1.6" height="1.6" transform="rotate(-12 4.1 5.4)"/><rect x="5.1" y="5.9" width="1.6" height="1.6" transform="rotate(10 5.9 6.7)"/><path d="M3 3.4H7"/>',
  tea: '<path d="M5 9.4V4.6"/><path d="M5 6.4C3 6.4 1.8 5 1.8 3.2C3.8 3.2 5 4.4 5 6.4Z"/><path d="M5 5.4C7 5.4 8.2 4 8.2 2.2C6.2 2.2 5 3.4 5 5.4Z"/><path d="M5 4.6C4.6 3.4 4.8 2 5.6 1"/>',
  pod: '<path d="M2.2 8.8C3.2 6 5.6 3 8.4 1.4C8.8 3.6 7.2 6.8 3.6 8.8Z"/><path d="M2.2 8.8L1.4 9.4M3.4 7.2C4.8 5.6 6.2 4 7.6 2.8"/>',
  teabag: '<path d="M3 4.4L4 3.4H6L7 4.4V9H3Z"/><circle cx="5" cy="4.2" r=".3"/><path d="M5 3.4V1.8M5 1.8C5.8 1.8 6.6 1.2 7.4 1.6"/><path d="M6.8 1.2H8.6V2.8H6.8Z"/>',
};

// EAN-13 (bars as one path, digits as outlines), 85% magnification, right-aligned at (right, top) in mm.
function barcode(F, code, right, top) {
  const Lc = ['0001101', '0011001', '0010011', '0111101', '0100011', '0110001', '0101111', '0111011', '0110111', '0001011'];
  const Gc = ['0100111', '0110011', '0011011', '0100001', '0011101', '0111001', '0000101', '0010001', '0001001', '0010111'];
  const Rc = ['1110010', '1100110', '1101100', '1000010', '1011100', '1001110', '1010000', '1000100', '1001000', '1110100'];
  const PAR = ['LLLLLL', 'LLGLGG', 'LLGGLG', 'LLGGGL', 'LGLLGG', 'LGGLLG', 'LGGGLL', 'LGLGLG', 'LGLGGL', 'LGGLGL'];
  const dg = code.split('').map(Number);
  if ((10 - dg.slice(0, 12).reduce((a, v, i) => a + v * (i % 2 ? 3 : 1), 0) % 10) % 10 !== dg[12]) throw new Error('Invalid EAN-13 ' + code);
  let bits = '101'; const gd = [0, 1, 2];
  dg.slice(1, 7).forEach((d, i) => { bits += (PAR[dg[0]][i] === 'L' ? Lc : Gc)[d]; });
  gd.push(bits.length + 1, bits.length + 3); bits += '01010';
  dg.slice(7).forEach((d) => { bits += Rc[d]; });
  gd.push(bits.length, bits.length + 2); bits += '101';
  const m = 0.28, barH = 22, q = 11 * m, W = (95 + 22) * m, x0 = right - W, y0 = top - barH - 3.2;
  let d = '';
  for (let i = 0; i < bits.length; i++) {
    if (bits[i] !== '1') continue;
    let j = i; while (bits[j + 1] === '1' && gd.includes(j + 1) === gd.includes(i)) j++;
    d += `M${F.X(x0 + q + i * m)} ${F.Y(y0)}h${F.S((j - i + 1) * m)}v${F.S(barH + (gd.includes(i) ? 1.4 : 0))}h${F.S(-(j - i + 1) * m)}Z`;
    i = j;
  }
  const ty = y0 + barH + 2.6, sz = 2.4;
  const dig = (s, x, anchor) => { const w = MONO.getAdvanceWidth(s, F.S(sz)); return MONO.getPath(s, anchor === 'end' ? F.X(x) - w : F.X(x) - w / 2, F.Y(ty), F.S(sz)).toPathData(3); };
  return `<g id="Barcode_${code}"><rect x="${F.X(x0 - 1.4)}" y="${F.Y(y0 - 1.4)}" width="${F.S(W + 2.8)}" height="${F.S(barH + 5.6)}" rx="${F.S(1)}" fill="#FFFFFF"/>` +
    `<path d="${d}" fill="#141414"/><path d="${dig(code[0], x0 + q - 1.2 * m, 'end') + dig(code.slice(1, 7), x0 + q + 24 * m) + dig(code.slice(7), x0 + q + 71 * m)}" fill="#141414"/></g>`;
}

// TEXT_INK=<file.json>: also write the ink box of every glyph set (panel, mm from the panel's top-left, y down), for
// checking the artwork's boundary against the real type
const INK_BOXES = process.env.TEXT_INK ? [] : null;
function inkBoxes(panel, f, s, x, y, sz, o) {
  const ot = FONT[f].ot, k = sz / ot.unitsPerEm, tr = o.track || 0, gl = ot.stringToGlyphs(s);
  const adv = gl.map((g) => g.advanceWidth * k), total = adv.reduce((a, v) => a + v, 0) + tr * Math.max(0, gl.length - 1);
  let cx = x - (o.anchor === 'middle' ? total / 2 : o.anchor === 'end' ? total : 0); const out = [];
  gl.forEach((g, i) => {
    const bb = g.getBoundingBox();
    if (bb.x2 > bb.x1) out.push({ panel, s, x0: cx + bb.x1 * k, x1: cx + bb.x2 * k, y0: y - bb.y2 * k, y1: y - bb.y1 * k });
    cx += adv[i] + tr;
  });
  return out;
}
const keys = process.argv[2] ? [process.argv[2]] : Object.keys(BOXES);
for (const k of keys) {
  const svg = build(k), dir = path.join(root, 'export', THEME ? `tea-${THEME}` : 'tea', k);
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, `vanilla-tea-${k}_EDITABLE.svg`), svg);
  if (INK_BOXES) fs.writeFileSync(process.env.TEXT_INK, JSON.stringify(INK_BOXES));
  if (process.env.PREVIEW_DIR) {
    const ff = Object.values(FONT).map((f) => `@font-face{font-family:'${f.ps}';src:url(file://${path.isAbsolute(f.file) ? f.file : path.join(process.env.CANDLE_FONTS, f.file)})}`).join('');
    fs.writeFileSync(path.join(process.env.PREVIEW_DIR, `tea-${k}.html`), `<html><head><meta charset="utf-8"><style>${ff}html,body{margin:0}</style></head><body>${svg}</body></html>`);
  }
  console.log('wrote', k, Math.round(svg.length / 1e5) / 10, 'MB');
}
