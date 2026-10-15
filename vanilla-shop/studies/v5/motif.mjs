// v5 "one motif" studies: the same painted vanilla vine on every product, wrapping from the
// front round onto the side; only the gradient and the second word change per product.
// Builds each box as one continuous strip (front | sideA | back | sideB) so the vine and the
// gradient run across the folds, then the render step cuts the strip into faces.
// Draft type uses Fontshare fonts from a local folder (not committed; ITF FFL forbids redistribution).
// Usage: FONTSHARE_DIR=... node studies/v5/motif.mjs   ->  studies/v5/out/<design>-<product>/
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const opentype = require('opentype.js');
const root = path.dirname(path.dirname(path.dirname(fileURLToPath(import.meta.url))));
const here = path.join(root, 'studies', 'v5');
const FS = process.env.FONTSHARE_DIR;
const otf = (fam, file) => opentype.loadSync(path.join(FS, fam, fs.readdirSync(path.join(FS, fam)).find((d) => d.endsWith('_Complete')), 'Fonts/OTF', file));
const F = {
  zodiak: otf('zodiak', 'Zodiak-Bold.otf'), zodiakIt: otf('zodiak', 'Zodiak-BoldItalic.otf'),
  boska: otf('boska', 'Boska-Black.otf'), boskaIt: otf('boska', 'Boska-BlackItalic.otf'),
  sansBold: otf('general-sans', 'GeneralSans-Semibold.otf'), sans: otf('general-sans', 'GeneralSans-Medium.otf'),
};

// Box faces in mm, from the dieline. The strip runs front -> sideA -> back -> sideB.
const H = 84.74;
const FACES = { front: [0, 87.66], sideA: [87.66, 84.57], back: [172.23, 87.58], sideB: [259.81, 84.84] };
const STRIP_W = 344.65, TOP = [87.66, 84.57];
const C = { espresso: '#1E1511', cream: '#FBF6EC' };
const n = (v) => Math.round(v * 1000) / 1000;

function width(f, s, sz, track = 0) {
  const g = f.stringToGlyphs(s), k = sz / f.unitsPerEm;
  return g.reduce((w, gl, i) => w + gl.advanceWidth * k + (i < g.length - 1 ? f.getKerningValue(gl, g[i + 1]) * k + track * sz : 0), 0);
}
function text(f, s, sz, x, y, fill, o = {}) {
  const str = o.caps ? s.toUpperCase() : s, g = f.stringToGlyphs(str), k = sz / f.unitsPerEm;
  const w = width(f, str, sz, o.track || 0);
  let cx = o.anchor === 'end' ? x - w : o.anchor === 'middle' ? x - w / 2 : x, d = '';
  g.forEach((gl, i) => {
    d += gl.getPath(cx, y, sz).toPathData(3);
    cx += gl.advanceWidth * k + (i < g.length - 1 ? f.getKerningValue(gl, g[i + 1]) * k + (o.track || 0) * sz : 0);
  });
  return `<path d="${d}" fill="${fill}"${o.opacity ? ` opacity="${o.opacity}"` : ''}/>`;
}
// Size that makes a word exactly `w` mm wide.
const fit = (f, s, w, track = 0) => w / width(f, s, 1, track);
const label = (s, x, y, fill, o = {}) => text(F.sans, s, 1.85, x, y, fill, { caps: true, track: 0.12, ...o });
const logoSrc = fs.readFileSync(path.join(root, 'brand', 'vanilla-shop-logo.svg'), 'utf8');
const LOGO_VW = Number(logoSrc.match(/viewBox="0 0 ([\d.]+) ([\d.]+)/)[1]), LOGO_VH = Number(logoSrc.match(/viewBox="0 0 [\d.]+ ([\d.]+)/)[1]);
const logo = (x, y, w, fill) => `<path fill="${fill}" fill-rule="evenodd" d="${logoSrc.match(/ d="([^"]+)"/)[1]}" transform="translate(${n(x)} ${n(y)}) scale(${n(w / LOGO_VW)})"/>`;

const VINE = path.join(root, 'plates', 'generated', 'v5-vine-cutout.webp');
const VINE_PX = [2000, 667];
// The vine, placed by its width in mm and its top-left corner in strip coordinates.
const vine = (v, extra = '') => `<image href="file://${VINE}" x="${n(v.x)}" y="${n(v.y)}" width="${n(v.w)}" height="${n(v.w * VINE_PX[1] / VINE_PX[0])}" preserveAspectRatio="none"${extra}/>`;

// Per-product gradients (top -> base) and copy. Sizes are only given where the website states them.
const PRODUCTS = {
  tea: { word: 'Tea', sub: 'Ceylon tea with natural vanilla', size: '12 tea bags · 24 g',
    stops: '0:#FCF1DA,0.34:#F8DA9C,0.56:#EFB977,0.78:#CB8E8A,1:#9A5F72', ink: '#4A2533' },
  extract: { word: 'Extract', sub: 'Pure vanilla, non-alcoholic', size: '100 ml',
    stops: '0:#F8E7C8,0.32:#E7B672,0.56:#B9733F,0.8:#6E3B26,1:#3A2018', ink: '#2A1610' },
  syrup: { word: 'Syrup', sub: 'Natural vanilla syrup', size: '500 ml',
    stops: '0:#FDF4DE,0.34:#FADB8C,0.6:#EFAF4C,0.82:#D3883A,1:#A9602A', ink: '#5A3214' },
  soap: { word: 'Soap', sub: 'Hand made vanilla soap', size: 'Hand made',
    stops: '0:#FCF7EE,0.36:#F3E6D6,0.62:#DCCAD4,0.84:#B8A0B9,1:#8E7593', ink: '#3E2E44' },
};

// Each design returns the strip body (in strip mm) given the product.
const DESIGNS = {
  // 1. Dusk: the gradient and vine wrap the corner; big two-line name in cream on the dusk foot.
  dusk: {
    bg: true,
    vine: { x: -22, y: -9, w: 182 },
    body(p) {
      const v = this.vine;
      const sz = fit(F.zodiak, 'Vanilla', 60);
      return [
        vine(v),
        logo(6.5, 6.5, 14, C.espresso),
        text(F.zodiak, 'Vanilla', sz, 5.6, 73.2 - sz * 0.84, C.cream),
        text(F.zodiakIt, p.word, sz, 5.6, 73.2, C.cream),
        label(p.sub, 6.2, 79.8, C.cream, { opacity: 0.9 }),
        label(p.size, 81.4, 79.8, C.cream, { anchor: 'end', opacity: 0.9 }),
      ].join('');
    },
  },
  // 2. Cream: the vine alone on the brand cream, no gradient; modern grotesk name in espresso.
  cream: {
    bg: false,
    vine: { x: -22, y: -9, w: 182 },
    body(p) {
      const sz = fit(F.sansBold, 'Vanilla', 60, -0.03);
      return [
        vine(this.vine),
        logo(6.5, 6.5, 14, C.espresso),
        text(F.sansBold, 'Vanilla', sz, 5.2, 79.4 - sz * 0.8, C.espresso, { track: -0.03 }),
        text(F.sansBold, p.word, sz, 5.2, 79.4, p.ink, { track: -0.03 }),
        label(p.sub, 81.6, 74.9, C.espresso, { anchor: 'end' }),
        label(p.size, 81.6, 79.4, '#6A5A50', { anchor: 'end' }),
      ].join('');
    },
  },
  // 3. Masthead: a giant "Vanilla" along the foot, the pods dipping in front of it; the product
  // word sits under the logo. The vine's cut-off stem fades out at the top instead of ending hard.
  masthead: {
    bg: true,
    vine: { x: -8, y: 14, w: 150 },
    body(p) {
      const v = this.vine, vh = v.w * VINE_PX[1] / VINE_PX[0];
      const sz = fit(F.boska, 'Vanilla', 84);
      return [
        `<linearGradient id="vf" x1="0" y1="${n(v.y)}" x2="0" y2="${n(v.y + vh * 0.2)}" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#000"/><stop offset="1" stop-color="#fff"/></linearGradient>`,
        `<mask id="vm" maskUnits="userSpaceOnUse" x="-50" y="-50" width="500" height="200"><rect x="-50" y="-50" width="500" height="200" fill="url(#vf)"/></mask>`,
        text(F.boska, 'Vanilla', sz, 1.8, 79.5, C.cream),
        `<g mask="url(#vm)">${vine(v)}</g>`,
        logo(6.5, 6.5, 12, C.espresso),
        text(F.boskaIt, p.word, 15, 6, 31.5, C.espresso),
        label(p.sub, 81.4, 9.4, C.espresso, { anchor: 'end' }),
        label(p.size, 81.4, 13.4, C.espresso, { anchor: 'end', opacity: 0.8 }),
      ].join('');
    },
  },
};

// Quiet faces shared by every design: the side continues the vine, the back carries one line.
function restOfBox(d, p, ink) {
  const [bx, bw] = FACES.back, [sx, sw] = FACES.sideB, [ax] = FACES.sideA;
  return [
    label('Brew one bag in 200 ml just-boiled water · 3–4 minutes', ax + 6, 79.6, ink, { opacity: 0.85 }),
    logo(bx + bw / 2 - 11, 18, 22, ink),
    text(F.zodiakIt, 'Vanilla was never plain.', 6.2, bx + bw / 2, 48, ink, { anchor: 'middle' }),
    label('The Vanilla Shop · Battaramulla · Sri Lanka', bx + bw / 2, 76, ink, { anchor: 'middle', opacity: 0.8 }),
    text(F.zodiakIt, 'What’s inside', 5, sx + 7, 16, ink),
    ...['Ceylon black tea', 'Natural vanilla', '12 tea bags'].map((s, i) => label(s, sx + 7, 26 + i * 5, ink)),
  ].join('');
}

const out = path.join(here, 'out');
fs.mkdirSync(out, { recursive: true });
const plate = (key, stops, wmm, hmm) => {
  const f = path.join(out, `plate-${key}.png`);
  if (!fs.existsSync(f)) execFileSync('python3', [path.join(root, 'tools', 'gradient_plate.py'), f, wmm, hmm, '12', stops, '5']);
  return f;
};

const only = process.argv[2];
for (const [dk, d] of Object.entries(DESIGNS)) {
  for (const [pk, p] of Object.entries(PRODUCTS)) {
    const key = `${dk}-${pk}`;
    if (only && !key.startsWith(only)) continue;
    const bg = d.bg ? `<image href="file://${plate(pk, p.stops, STRIP_W, H)}" width="${STRIP_W}" height="${H}" preserveAspectRatio="none"/>` : `<rect width="${STRIP_W}" height="${H}" fill="${C.cream}"/>`;
    const ink = d.bg ? (pk === 'extract' ? C.cream : C.espresso) : C.espresso;
    const strip = `<svg xmlns="http://www.w3.org/2000/svg" width="${STRIP_W}mm" height="${H}mm" viewBox="0 0 ${STRIP_W} ${H}">` +
      `${bg}${d.body(p)}${restOfBox(d, p, ink)}</svg>`;
    fs.writeFileSync(path.join(out, `${key}.svg`), strip);
    // Top flap: the colour at the top of the gradient, with the logo.
    const topCol = d.bg ? p.stops.split(',')[0].split(':')[1] : C.cream;
    const baseCol = d.bg ? p.stops.split(',').at(-1).split(':')[1] : C.cream;
    fs.writeFileSync(path.join(out, `${key}-top.svg`), `<svg xmlns="http://www.w3.org/2000/svg" width="${TOP[0]}mm" height="${TOP[1]}mm" viewBox="0 0 ${TOP[0]} ${TOP[1]}"><rect width="${TOP[0]}" height="${TOP[1]}" fill="${topCol}"/>${logo(TOP[0] / 2 - 14, TOP[1] / 2 - 14 * LOGO_VH / LOGO_VW, 28, C.espresso)}</svg>`);
    fs.writeFileSync(path.join(out, `${key}-bottom.svg`), `<svg xmlns="http://www.w3.org/2000/svg" width="${TOP[0]}mm" height="${TOP[1]}mm" viewBox="0 0 ${TOP[0]} ${TOP[1]}"><rect width="${TOP[0]}" height="${TOP[1]}" fill="${baseCol}"/></svg>`);
  }
}
fs.writeFileSync(path.join(out, 'faces.json'), JSON.stringify({ FACES, H, STRIP_W, TOP }));
console.log('wrote', fs.readdirSync(out).filter((f) => f.endsWith('.svg')).length, 'svgs');
