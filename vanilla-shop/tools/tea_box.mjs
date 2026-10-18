// Natural Vanilla Tea boxes: the vine set's painting, golden ground, diagram and lid sprigs, with the candle
// range's structure (ruled bars, spaced Roc Grotesk labels, sentence-case body) and a numbered brewing stepper.
// The name and panel headings are Instrument Serif Italic. Cube front: name high, logo bottom left.
// Long front: data columns on top, vine across the top right, the name along the foot.
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
  wide: CFONT.wide, wideR: CFONT.wideR, body: CFONT.body,
};
FONT.title.ot = opentype.loadSync(FONT.title.file);
const width = (f, s, sz, track = 0) => {
  const g = f.ot.stringToGlyphs(s), k = sz / f.ot.unitsPerEm;
  return g.reduce((w, gl) => w + gl.advanceWidth * k, 0) + track * Math.max(0, g.length - 1);
};
const MM = 72 / 25.4, INK = '#143A1D', PAPER = '#F8E7C0';
const R = (x0, y0, x1, y1) => ({ x: x0, y: y0, w: x1 - x0, h: y1 - y0 });
const G = (f) => path.join(root, 'plates', 'generated', f);
const data = (f) => `data:image/${f.endsWith('png') ? 'png' : 'jpeg'};base64,` + fs.readFileSync(f).toString('base64');
const DISTRIBUTOR = { name: 'Agro Ventures Exports (Pvt) Ltd', address: 'No. 48, Sir Marcus Fernando Mawatha,\nColombo 07, Sri Lanka', web: 'www.agroventuresexports.com', email: 'info@agroventuresexports.com', hotline: '011 2 187 287' };
// GTIN from the current 25-bag, 50 g pack. A new pack size needs its own GTIN from GS1 Sri Lanka.
const GTIN = '4796034220229';
const SHAPED = JSON.parse(fs.readFileSync(path.join(root, 'brand', 'shaped-labels.json'), 'utf8'));
const logoD = fs.readFileSync(path.join(root, 'brand', 'vanilla-shop-logo.svg'), 'utf8').match(/ d="([^"]+)"/)[1];
const LOGO_VB = Number(fs.readFileSync(path.join(root, 'brand', 'vanilla-shop-logo.svg'), 'utf8').match(/viewBox="0 0 ([\d.]+) ([\d.]+)/)[1]);

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
  let defs = '', ringPath = '';
  // Face helpers: draw in mm from a panel's top-left; rot turns the face 180 degrees (a lid hinged at the back).
  const face = (k, rot = false) => {
    const p = P[k].panel, { w, h } = size(k);
    const X = (x) => n(rot ? p.x + (w - x) * MM : p.x + x * MM), Y = (y) => n(rot ? p.y + (h - y) * MM : p.y + y * MM), S = (v) => n(v * MM);
    const tr = (x, y) => rot ? ` transform="rotate(180 ${X(x)} ${Y(y)})"` : '';
    const text = (f, s, x, y, sz, o = {}) => {
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
    const oldIcon = (k, cx, cy, r, sc) => `<circle cx="${X(cx)}" cy="${Y(cy)}" r="${S(r)}" fill="#FFFBF2" fill-opacity=".55"/><g transform="translate(${X(cx)} ${Y(cy)}) scale(${n(S(sc), 5)})">${OLD_ICONS[k]}</g>`;
    const img = (f, x, y, wmm, hmm) => `<image xlink:href="${data(f)}" x="${X(x)}" y="${Y(y)}" width="${S(wmm)}" height="${S(hmm)}" preserveAspectRatio="none"/>`;
    return { w, h, X, Y, S, text, para, rule, caps, label, body, logo, icon, oldIcon, img };
  };

  // ---- grounds: paper colour on every panel and flap; the painted golden ground on the four walls
  for (const [k, { region }] of Object.entries(P)) L.Background.push(`<rect x="${region.x}" y="${region.y}" width="${n(region.w)}" height="${n(region.h)}" fill="${PAPER}"/>`);
  for (const k of ['front', 'sideA', 'back', 'sideB']) {
    const F = face(k), r = P[k].region, p = P[k].panel;
    defs += `<clipPath id="clip-${k}"><rect x="${n(Math.min(r.x, p.x) - (k === 'front' ? 3 * MM : 0))}" y="${n(p.y - 3 * MM)}" width="${n(Math.max(r.w, p.w) + (k === 'front' ? 3 * MM : 0))}" height="${n(p.h + 6 * MM)}"/></clipPath>`;
    L.Ground.push(`<g clip-path="url(#clip-${k})">${F.img(G(`v6-ground-golden${boxKey === 'long' ? '-long' : ''}-${k}.jpg`), -3, -3, F.w + 6, F.h + 6)}</g>`);
  }

  // ---- painting: one placement for the vine across front and right side
  {
    const F = face('front'), V = B.vine, vine = F.img(G('v6-vine-faded.png'), V.x, V.y, 3808 * V.s, 1651 * V.s);
    const fa = P.front.panel, sa = P.sideA.panel;
    defs += `<clipPath id="clip-walls"><rect x="${n(fa.x - 3 * MM)}" y="${n(fa.y - 0.5 * MM)}" width="${n(sa.x + sa.w - fa.x + 3 * MM)}" height="${n(fa.h + 3.5 * MM)}"/></clipPath>`;
    L.Painting.push(`<g id="Vine" clip-path="url(#clip-walls)">${vine}</g>`);
  }
  // A panel heading in the serif italic sitting on a rule, at the height of the front's top bar, so the bars
  // read as one band round the box.
  const head = (F, s, x0, x1, right) => F.text('title', s, x0, 10.9, 6) + F.rule(x0, 12.8, x1, 12.8) + (right ? F.caps(right, x1, 10.4, { anchor: 'end', size: 1.85 }) : '');

  // ---- front
  {
    const F = face('front'), t = [];
    if (boxKey === 'cube') {
      // Top bar; the name high, two lines; the product line; the logo bottom left on the same edge.
      const r = F.w - 8, sz = 20, asc = 0.72 * sz, top = 16.5, b1 = top + asc, b2 = b1 + 0.78 * sz;
      t.push(F.caps('AUTHENTIC CEYLON', 8, 10.4), F.caps(`${pack.bags} TEA BAGS · ${pack.net} G`, r, 10.4, { anchor: 'end' }), F.rule(8, 12.8, r, 12.8));
      L.Name.push(F.text('title', 'Vanilla', 7, b1, sz), F.text('title', 'Tea', 7, b2, sz));
      t.push(F.body('Ceylon black tea\nwith natural vanilla', 8, b2 + 8.8, 40, { size: 2.5, lead: 3.4 }).svg);
      const lw = 13.5;
      t.push(F.logo(8 + lw / 2, F.h - 7.5 - lw * 963 / 933 + lw * 0.52, lw));
    } else {
      // Ruled bar and data columns on top, the vine across the top right, the name along the foot.
      const bar = 96, sz = 26;
      t.push(F.caps('THE VANILLA SHOP', 9, 12), F.caps('NO. 01', bar, 12, { anchor: 'end' }), F.rule(9, 15, bar, 15));
      t.push(F.label('BLEND', 9, 23), F.caps('CEYLON BLACK TEA', 9, 27), F.caps('NATURAL VANILLA', 9, 30.4));
      t.push(F.label('ORIGIN', 48, 23), F.caps('AUTHENTIC CEYLON', 48, 27));
      t.push(F.label('CONTENTS', 9, 36.4), F.caps(`${pack.bags} TEA BAGS · ${pack.net} G`, 9, 40.4));
      L.Name.push(F.text('title', 'Vanilla Tea', 8, F.h - 9, sz));
      t.push(F.rule(9, F.h - 5, bar + 50, F.h - 5));
    }
    L.Type.push(`<g id="Front">${t.join('')}</g>`);
  }

  // ---- right side: how to brew as a numbered stepper; pack line at the foot
  {
    const F = face('sideA'), t = [], sx = boxKey === 'cube' ? 40 : 8, r = boxKey === 'cube' ? F.w - 8 : F.w - 30, sy = 18;
    if (boxKey === 'long') L.Painting.push(F.img(G('v6-climb.png'), F.w - 2 - 612 * 0.035, F.h + 1.5 - 2000 * 0.035, 667 * 0.035, 2000 * 0.035));
    t.push(head(F, 'How to brew', sx, r));
    // The vine set's three brewing icons on light discs, joined by a fine line between the discs.
    const steps = [['cup', '150 ML', 'One tea bag in hot water'], ['timer', '5 MINUTES', 'Then lift the bag out'], ['ice', 'OVER ICE', 'Let it cool, pour over ice']];
    const rD = 3.6, cxD = sx + rD, gap = 14;
    steps.forEach(([ic, h, d], i) => {
      const y = sy + i * gap, cy = y + rD;
      if (i) t.push(`<path d="M${F.X(cxD)} ${F.Y(cy - gap + rD + 0.8)}V${F.Y(cy - rD - 0.8)}" stroke="${INK}" stroke-opacity=".35" stroke-width="${F.S(0.22)}"/>`);
      t.push(F.oldIcon(ic, cxD, cy, rD, 0.5));
      t.push(F.text('wideR', h, sx + 2 * rD + 2.4, y + 2.6, 2.2, { track: 0.3 }), F.body(d, sx + 2 * rD + 2.4, y + 5.9, 30, { size: 2.1, lead: 2.9 }).svg);
    });
    t.push(F.rule(sx, F.h - 11.4, r, F.h - 11.4), F.caps(`${pack.bags} TEA BAGS · 2 G EACH · ${pack.net} G`, sx, F.h - 7.5, { size: 1.9 }));
    L.Type.push(`<g id="Side_How_to_brew">${t.join('')}</g>`);
  }

  // ---- back: the line, then the labelled plate of vanilla
  const backPlate = (F, ox, w) => {
    const t = [], s = 56 / 1485, x0 = ox + w - 5 - 1000 * s, y0 = 19;
    const at = (px, py) => [x0 + px * s, y0 + py * s];
    L.Painting.push(F.img(G('v6-diagram-soft.png'), x0, y0, 1000 * s, 1485 * s));
    t.push(head(F, 'Vanilla was never plain.', ox + 8, ox + w - 8));
    t.push(F.body('The delicate sweetness of natural vanilla unfolds through warm, comforting notes and a smooth, mellow aroma.', ox + 8, 19.6, 37, { size: 2.2, lead: 3.0 }).svg);
    [['VANILLA ORCHID', 'Hand-pollinated; open for one day', at(545, 330)],
      ['AERIAL ROOTS', 'The vine climbs by them', at(165, 560)],
      ['CEYLON TEA', 'Two leaves and a bud', at(330, 1065)],
      ['GREEN PODS', 'Ripen for about nine months', at(470, 980)],
      ['CURED POD', 'Sweated and dried for months', at(585, 1270)]].forEach(([k, note, [px, py]], i) => {
      const y = 46 + i * 6.8, lw = Math.max(width(FONT.wide, k, 1.75, 0.25), width(FONT.body, note, 2.0));
      t.push(F.text('wide', k, ox + 8, y, 1.75, { track: 0.25 }), F.text('body', note, ox + 8, y + 2.7, 2.0, { opacity: 0.85 }));
      const sx = ox + 8 + lw + 1.6, sy = y - 0.6;
      t.push(`<path d="M${F.X(sx)} ${F.Y(sy)}H${F.X(Math.min(px - 3, sx + 4))}L${F.X(px)} ${F.Y(py)}" fill="none" stroke="${INK}" stroke-width="${F.S(0.14)}"/><circle cx="${F.X(px)}" cy="${F.Y(py)}" r="${F.S(0.55)}" fill="${INK}"/>`);
    });
    return t.join('');
  };
  // What's inside: intro, three icons, details table.
  const inside = (F, ox, w, seeWhere) => {
    const t = [], r = ox + w - 8;
    t.push(head(F, 'What’s inside', ox + 8, r));
    t.push(F.body(`Ceylon black tea with natural vanilla, in ${pack.bags} tagged, unbleached tea bags of 2 g each.`, ox + 8, 19.6, w - 16).svg);
    const cw = (w - 16) / 3;
    t.push(F.rule(ox + 8, 28, r, 28));
    [['tea', 'CEYLON TEA'], ['pod', 'NATURAL VANILLA'], ['teabag', `${pack.bags} TEA BAGS`]].forEach(([ic, k], i) => {
      const cx = ox + 8 + cw * (i + 0.5);
      if (i) t.push(F.rule(ox + 8 + cw * i, 28, ox + 8 + cw * i, 42, 0.35));
      t.push(F.oldIcon(ic, cx, 33.6, 4.2, 0.66), F.text('wide', k, cx, 41.2, 1.6, { track: 0.15, anchor: 'middle' }));
    });
    let y = 45.5;
    for (const [k, v, soft] of [['INGREDIENTS', 'To be confirmed before print', true], ['NET WEIGHT', `${pack.net} g (${pack.bags} tea bags × 2 g)`], ['STORAGE', 'To be confirmed before print', true], ['DISTRIBUTOR', `${DISTRIBUTOR.name} — see ${seeWhere}`]]) {
      t.push(F.rule(ox + 8, y, r, y, 0.35), F.label(k, ox + 8, y + 3.6), F.body(v, ox + 30, y + 3.6, w - 38, { size: 2.15, opacity: soft ? 0.6 : 1 }).svg);
      y += 6.4 + (width(FONT.body, v, 2.15) > w - 38 ? 3.2 : 0);
    }
    t.push(F.rule(ox + 8, y, r, y, 0.35));
    return t.join('');
  };
  // Batch block (Sinhala, English, Tamil), barcode, distributor.
  const baseInfo = (F, ox, w) => {
    const t = [], r = ox + w - 8;
    t.push(head(F, 'Vanilla Tea', ox + 8, r, 'BATCH DETAILS'));
    [['කා.අ.', 'B.N.', 'தொகுதி இல'], ['නි.දි.', 'MFD.', 'பொ.செ திகதி'],
      ['කා.ඉ.දි.', 'EXP.', 'மு.திகதி'], ['උ.සි.මි.රු.', 'MRP RS.', 'விலை ரூபா']].forEach(([si, en, ta], i) => {
      const y = 21.4 + i * 8;
      t.push(shaped(F, si, 1.75, ox + 8, y - 2.5), F.text('wideR', en, ox + 8, y, 1.85, { track: 0.25 }), shaped(F, ta, 1.6, ox + 8, y + 2.3));
      t.push(`<path d="M${F.X(ox + 22)} ${F.Y(y + 0.6)}H${F.X(ox + 44)}" stroke="${INK}" stroke-opacity=".6" stroke-width="${F.S(0.15)}" stroke-dasharray="${F.S(0.4)} ${F.S(0.4)}" fill="none"/>`);
    });
    L.Barcode.push(barcode(F, GTIN, r, 46));
    t.push(F.rule(ox + 8, 55.5, r, 55.5), F.label('MARKETED AND DISTRIBUTED BY', ox + 8, 60));
    t.push(F.text('wideR', DISTRIBUTOR.name.toUpperCase(), ox + 8, 64.2, 1.95, { track: 0.2 }));
    t.push(F.body(DISTRIBUTOR.address, ox + 8, 68, (w - 16) / 2, { size: 2.1, lead: 2.9 }).svg);
    t.push(F.body(`${DISTRIBUTOR.web}\n${DISTRIBUTOR.email}\nHotline ${DISTRIBUTOR.hotline}`, ox + 8 + (w - 16) / 2 + 2, 68, (w - 16) / 2, { size: 2.1, lead: 2.9 }).svg);
    return t.join('');
  };

  if (boxKey === 'cube') {
    const Fb = face('back'); L.Type.push(`<g id="Back">${backPlate(Fb, 0, Fb.w)}</g>`);
    const Fs = face('sideB'); L.Type.push(`<g id="Side_Whats_inside">${inside(Fs, 0, Fs.w, 'base')}</g>`);
    const Fo = face('bottom'); L.Type.push(`<g id="Base">${baseInfo(Fo, 0, Fo.w)}</g>`);
  } else {
    const Fb = face('back'), half = 87.58;
    L.Type.push(`<g id="Back">${backPlate(Fb, 0, half)}${Fb.rule(half + 1.5, 18, half + 1.5, Fb.h - 10, 0.35)}${inside(Fb, half, Fb.w - half, 'side')}</g>`);
    const Fs = face('sideB'); L.Type.push(`<g id="Side_Batch_and_barcode">${baseInfo(Fs, 0, Fs.w)}</g>`);
    const Fo = face('bottom');
    L.Type.push(`<g id="Base">${Fo.logo(Fo.w / 2, Fo.h / 2 - 3, 24)}${Fo.caps('AUTHENTIC CEYLON VANILLA TEA', Fo.w / 2, Fo.h / 2 + 13, { anchor: 'middle' })}</g>`);
  }

  // ---- lid: two sprigs reaching in from opposite corners (from the vine set) frame the emblem ring (from the
  // candles). A long-box lid hangs off the back, so its whole group is turned to read from the front.
  {
    const F = face('top'), cx = F.w / 2, cy = F.h / 2 - 2, r = 22, ring = 'SAVOR THE CALM · AUTHENTIC CEYLON VANILLA TEA · ';
    const len = 2 * Math.PI * r, track = (len - width(FONT.wide, ring, 2.5)) / ring.length;
    ringPath = `M${F.X(cx - r)} ${F.Y(cy)}A${F.S(r)} ${F.S(r)} 0 1 1 ${F.X(cx + r)} ${F.Y(cy)}A${F.S(r)} ${F.S(r)} 0 1 1 ${F.X(cx - r)} ${F.Y(cy)}`;
    defs += `<path id="ring" d="${ringPath}"/>`;
    const ss = 0.024, sw = 1448 * ss, sh = 1086 * ss, p = P.top.panel, pcx = n(p.x + p.w / 2), pcy = n(p.y + p.h / 2);
    const sprig = F.img(G('v6-sprig.png'), F.w + 1.5 - sw, 1.5 - 168 * ss, sw, sh);
    defs += `<clipPath id="clip-lid"><rect x="${p.x}" y="${p.y}" width="${n(p.w)}" height="${n(p.h)}"/></clipPath>`;
    const turn = B.lidTurn ? ` transform="rotate(180 ${pcx} ${pcy})"` : '';
    L.Painting.push(`<g id="Lid_sprigs" clip-path="url(#clip-lid)"><g${turn}>${sprig}<g transform="rotate(180 ${pcx} ${pcy})">${sprig}</g></g></g>`);
    const fy = F.h - 8.6;
    L.Type.push(`<g id="Lid"${turn}><circle cx="${F.X(cx)}" cy="${F.Y(cy)}" r="${F.S(25.6)}" fill="none" stroke="${INK}" stroke-opacity=".5" stroke-width="${F.S(0.18)}"/>` +
      `<circle cx="${F.X(cx)}" cy="${F.Y(cy)}" r="${F.S(18.6)}" fill="none" stroke="${INK}" stroke-opacity=".5" stroke-width="${F.S(0.18)}"/>` +
      `<text font-family="'${FONT.wide.ps}'" font-size="${F.S(2.5)}" letter-spacing="${F.S(track)}" fill="${INK}"><textPath xlink:href="#ring">${esc(ring)}</textPath></text>` +
      F.logo(cx, cy, 19) + '</g>');
    if (B.lidTurn) ringPath = `M0 0`;   // the turned ring is inside a transformed group; no free guide path
  }

  const tile = grainTile({ dpi: 600, clump: 0.5 });
  defs += `<pattern id="grain" patternUnits="userSpaceOnUse" width="${n(tile.mm * MM)}" height="${n(tile.mm * MM)}"><image xlink:href="${tile.href}" width="${n(tile.mm * MM)}" height="${n(tile.mm * MM)}"/></pattern>`;
  defs += `<clipPath id="clip-all">${Object.values(P).map(({ region: r }) => `<rect x="${r.x}" y="${r.y}" width="${n(r.w)}" height="${n(r.h)}"/>`).join('')}</clipPath>`;
  const g = (id, b) => `<g id="${id}">${b}</g>`;
  return `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="${B.sheet.w}pt" height="${B.sheet.h}pt" viewBox="0 0 ${B.sheet.w} ${B.sheet.h}">` +
    `<title>The Vanilla Shop: Natural Vanilla Tea, ${pack.bags} bags</title><defs>${defs}</defs>` +
    g('Background', L.Background.join('')) + g('Ground', L.Ground.join('')) + g('Painting', L.Painting.join('')) + g('Name', L.Name.join('')) + g('Weave', L.Weave.join('')) +
    g('Texture', `<rect width="${B.sheet.w}" height="${B.sheet.h}" fill="url(#grain)" opacity=".55" clip-path="url(#clip-all)"/>`) +
    g('Type_and_Icons', L.Type.join('')) + g('Barcode', L.Barcode.join('')) +
    g('Lid_ring_path', `<path d="${ringPath}" fill="none" stroke="none"/>`) +
    g('Dieline', B.dieline.replace(/stroke="#B[0-9A-F]{5}"/g, 'stroke="#E4007C"')) + '</svg>';
}

function shaped(F, s, sz, x, y) {
  const gl = SHAPED[s];
  if (!gl) throw new Error('Label not shaped: ' + s);
  return `<path d="${gl.d}" fill="${INK}" opacity=".8" transform="translate(${F.X(x)} ${F.Y(y)}) scale(${n(F.S(sz), 5)})"/>`;
}

// The vine set's icons (tools/box.mjs), drawn round their centre, set on a light disc.
const STROKE = `fill="none" stroke="${INK}" stroke-width="0.32" stroke-linecap="round" stroke-linejoin="round"`;
const OLD_ICONS = {
  cup: `<path ${STROKE} d="M-5 4.3Q0 5.7 5 4.3"/><path ${STROKE} d="M-3.8 -1.2H3.2Q3.2 3.9 -0.3 3.9Q-3.8 3.9 -3.8 -1.2Z"/><path ${STROKE} d="M3.15 -0.3q2.1 0 2.1 1.3t-2.35 1.6"/>` +
    `<path ${STROKE} d="M1.3 -1.2L2.5 -4.1"/><rect ${STROKE} x="1.75" y="-5.95" width="1.7" height="1.9" rx="0.2" transform="rotate(12 2.6 -5)"/><path ${STROKE} d="M-2.1 -2.4q-0.8 -1 0 -2M-0.5 -2.4q-0.8 -1 0 -2"/>`,
  timer: `<path d="M0 0.7L0 -3.2A3.9 3.9 0 0 1 1.95 -2.68Z" fill="${INK}" opacity="0.18"/><circle ${STROKE} cx="0" cy="0.7" r="3.9"/><path ${STROKE} d="M-0.9 -4.6H0.9M0 -4.6V-3.2M3 -2.5l0.7 -0.7"/>` +
    `<path ${STROKE} d="M0 0.7L1.6 -2.1"/><circle cx="0" cy="0.7" r="0.35" fill="${INK}"/><path ${STROKE} d="M0 -2.6v0.5M3.3 0.7h-0.5M0 4v-0.5M-3.3 0.7h0.5"/>`,
  ice: `<path ${STROKE} d="M-3.1 -4.4L-2.4 4.6H2.4L3.1 -4.4"/><path ${STROKE} d="M-2.85 -1.1H2.85"/><rect ${STROKE} x="-2.3" y="-0.3" width="2.1" height="2.1" rx="0.3" transform="rotate(14 -1.25 0.75)"/>` +
    `<rect ${STROKE} x="0.1" y="1.6" width="1.9" height="1.9" rx="0.3" transform="rotate(-10 1.05 2.55)"/><path ${STROKE} d="M1 -1.1L2.3 -6.1"/>`,
  tea: `<path ${STROKE} d="M0 4.8C0 2 0.3 -0.5 0.6 -3.4"/><path ${STROKE} d="M0.6 -3.4C-0.4 -4 -0.3 -5.3 0.6 -5.8C1.5 -5.3 1.6 -4 0.6 -3.4Z"/>` +
    `<path ${STROKE} d="M0.3 -1C-1.4 -0.3 -3.8 -1 -4.4 -3.3C-2.2 -3.9 -0.4 -3 0.3 -1Z"/><path ${STROKE} d="M0.3 -1L-3.3 -2.9"/><path ${STROKE} d="M0.1 2.2C1.8 3.2 4.3 2.6 5 0.2C2.7 -0.5 0.8 0.3 0.1 2.2Z"/><path ${STROKE} d="M0.1 2.2L3.9 0.6"/>`,
  pod: [-90, -18, 54, 126, 198].map((a) => `<path ${STROKE} d="M0 -1.2C0.95 -2.2 1 -3.9 0 -5.4C-1 -3.9 -0.95 -2.2 0 -1.2Z" transform="rotate(${a + 90})"/>`).join('') +
    `<circle ${STROKE} cx="0" cy="0" r="1.25"/><circle cx="0" cy="0" r="0.42" fill="${INK}"/>`,
  teabag: `<rect ${STROKE} x="-3.4" y="-1.2" width="5" height="6" rx="0.6"/><path ${STROKE} d="M-3.4 0.2H1.6"/><path ${STROKE} d="M-0.9 -1.2C-0.9 -3.6 1.2 -4.6 2.6 -3.4"/><rect ${STROKE} x="2.3" y="-4.2" width="2.4" height="2.8" rx="0.3" transform="rotate(-14 3.5 -2.8)"/>`,
};

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

const keys = process.argv[2] ? [process.argv[2]] : Object.keys(BOXES);
for (const k of keys) {
  const svg = build(k), dir = path.join(root, 'export', 'tea', k);
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, `vanilla-tea-${k}_EDITABLE.svg`), svg);
  if (process.env.PREVIEW_DIR) {
    const ff = Object.values(FONT).map((f) => `@font-face{font-family:'${f.ps}';src:url(file://${path.isAbsolute(f.file) ? f.file : path.join(process.env.CANDLE_FONTS, f.file)})}`).join('');
    fs.writeFileSync(path.join(process.env.PREVIEW_DIR, `tea-${k}.html`), `<html><head><meta charset="utf-8"><style>${ff}html,body{margin:0}</style></head><body>${svg}</body></html>`);
  }
  console.log('wrote', k, Math.round(svg.length / 1e5) / 10, 'MB');
}
