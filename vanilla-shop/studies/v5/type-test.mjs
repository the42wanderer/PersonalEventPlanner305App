// Type test: the same dusk front (vine, gradient, logo, labels) with the name set in each candidate
// typeface, so the fonts are judged on the real artwork rather than on a specimen sheet.
// Fonts are read from local folders and outlined; none are committed.
// Usage: FONTSHARE_DIR=... GF_DIR=... node studies/v5/type-test.mjs  ->  studies/v5/out/type/<n>.svg
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const opentype = require('opentype.js');
const root = path.dirname(path.dirname(path.dirname(fileURLToPath(import.meta.url))));
const FS = process.env.FONTSHARE_DIR, GF = process.env.GF_DIR;
const fsh = (fam, file) => path.join(FS, fam, fs.readdirSync(path.join(FS, fam)).find((d) => d.endsWith('_Complete')), 'Fonts/OTF', file);
const load = (p) => { try { return opentype.loadSync(p); } catch { return null; } };

const W = 87.66, H = 84.74;
const CREAM = '#FBF6EC', ESPRESSO = '#1E1511';
const n = (v) => Math.round(v * 1000) / 1000;
function width(f, s, sz, track = 0) {
  const g = f.stringToGlyphs(s), k = sz / f.unitsPerEm;
  return g.reduce((w, gl, i) => w + gl.advanceWidth * k + (i < g.length - 1 ? f.getKerningValue(gl, g[i + 1]) * k + track * sz : 0), 0);
}
function text(f, s, sz, x, y, fill, o = {}) {
  const str = o.caps ? s.toUpperCase() : s, g = f.stringToGlyphs(str), k = sz / f.unitsPerEm;
  const w = width(f, str, sz, o.track || 0);
  let cx = o.anchor === 'end' ? x - w : x, d = '';
  g.forEach((gl, i) => { d += gl.getPath(cx, y, sz).toPathData(3); cx += gl.advanceWidth * k + (i < g.length - 1 ? f.getKerningValue(gl, g[i + 1]) * k + (o.track || 0) * sz : 0); });
  return `<path d="${d}" fill="${fill}"${o.opacity ? ` opacity="${o.opacity}"` : ''}/>`;
}
const sans = opentype.loadSync(fsh('general-sans', 'GeneralSans-Medium.otf'));
const label = (s, x, y, o = {}) => text(sans, s, 1.85, x, y, CREAM, { caps: true, track: 0.12, opacity: 0.9, ...o });
const logoSrc = fs.readFileSync(path.join(root, 'brand', 'vanilla-shop-logo.svg'), 'utf8');
const logo = (x, y, w, fill) => `<path fill="${fill}" fill-rule="evenodd" d="${logoSrc.match(/ d="([^"]+)"/)[1]}" transform="translate(${x} ${y}) scale(${n(w / Number(logoSrc.match(/viewBox="0 0 ([\d.]+)/)[1]))})"/>`;
const PLATE = path.join(root, 'studies', 'v5', 'out', 'plate-tea.png');
const VINE = path.join(root, 'plates', 'generated', 'v5-vine-cutout.webp');

// [label, source, upright file, second-line file, how the two lines are set]
const CANDIDATES = [
  ['Zodiak Bold + Italic', 'Fontshare', fsh('zodiak', 'Zodiak-Bold.otf'), fsh('zodiak', 'Zodiak-BoldItalic.otf')],
  ['Boska Black + Italic', 'Fontshare', fsh('boska', 'Boska-Black.otf'), fsh('boska', 'Boska-BlackItalic.otf')],
  ['Bespoke Serif Extrabold', 'Fontshare', fsh('bespoke-serif', 'BespokeSerif-Extrabold.otf'), fsh('bespoke-serif', 'BespokeSerif-ExtraboldItalic.otf')],
  ['Neco Black + Italic', 'Fontshare', fsh('neco', 'Neco-Black.otf'), fsh('neco', 'Neco-BlackItalic.otf')],
  ['Gambarino', 'Fontshare', fsh('gambarino', 'Gambarino-Regular.otf'), fsh('gambarino', 'Gambarino-Regular.otf')],
  ['Stardom', 'Fontshare', fsh('stardom', 'Stardom-Regular.otf'), fsh('stardom', 'Stardom-Regular.otf')],
  ['Melodrama Bold', 'Fontshare', fsh('melodrama', 'Melodrama-Bold.otf'), fsh('melodrama', 'Melodrama-Bold.otf')],
  ['Bonny Bold', 'Fontshare', fsh('bonny', 'Bonny-Bold.otf'), fsh('bonny', 'Bonny-Bold.otf')],
  ['Cabinet Grotesk Extrabold', 'Fontshare', fsh('cabinet-grotesk', 'CabinetGrotesk-Extrabold.otf'), fsh('cabinet-grotesk', 'CabinetGrotesk-Extrabold.otf')],
  ['Clash Display Semibold', 'Fontshare', fsh('clash-display', 'ClashDisplay-Semibold.otf'), fsh('clash-display', 'ClashDisplay-Semibold.otf')],
  ['Playfair Display Black (the website font)', 'Google', path.join(GF, 'playfair-display-latin-900-normal.woff'), path.join(GF, 'playfair-display-latin-900-italic.woff')],
  ['DM Serif Display', 'Google', path.join(GF, 'dm-serif-display-latin-400-normal.woff'), path.join(GF, 'dm-serif-display-latin-400-italic.woff')],
  ['Young Serif', 'Google', path.join(GF, 'young-serif-latin-400-normal.woff'), path.join(GF, 'young-serif-latin-400-normal.woff')],
  ['Zen Old Mincho Black', 'Google', path.join(GF, 'zen-old-mincho-latin-900-normal.woff'), path.join(GF, 'zen-old-mincho-latin-900-normal.woff')],
  ['Fraunces Black Italic', 'Google', path.join(root, 'fonts', 'fraunces-black-italic.ttf'), path.join(root, 'fonts', 'fraunces-black-italic.ttf')],
  ['Bricolage Grotesque Bold', 'Google', path.join(GF, 'bricolage-grotesque-latin-700-normal.woff'), path.join(GF, 'bricolage-grotesque-latin-700-normal.woff')],
];

const out = path.join(root, 'studies', 'v5', 'out', 'type');
fs.mkdirSync(out, { recursive: true });
const made = [];
CANDIDATES.forEach(([name, src, a, b], i) => {
  const fa = load(a), fb = load(b);
  if (!fa || !fb) { console.log('skip (missing font)', name); return; }
  // Same cap height for every face (narrow faces would otherwise grow tall), capped at 60 mm wide.
  const cap = (f) => (f.tables.os2?.sCapHeight || f.charToGlyph('H').getBoundingBox().y2) / f.unitsPerEm;
  const sz = Math.min(60 / width(fa, 'Vanilla', 1), 12.5 / cap(fa));
  const sz2 = Math.min(60 / width(fb, 'Tea', 1), 12.5 / cap(fb));
  const base2 = 73.2, base1 = base2 - 12.5 * 1.36;
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}mm" height="${H}mm" viewBox="0 0 ${W} ${H}">` +
    `<clipPath id="c"><rect width="${W}" height="${H}"/></clipPath><g clip-path="url(#c)">` +
    `<image href="file://${PLATE}" width="344.65" height="${H}" preserveAspectRatio="none"/>` +
    `<image href="file://${VINE}" x="-22" y="-9" width="182" height="${n(182 * 667 / 2000)}" preserveAspectRatio="none"/>` +
    logo(6.5, 6.5, 14, ESPRESSO) +
    text(fa, 'Vanilla', sz, 5.6, base1, CREAM) + text(fb, 'Tea', sz2, 5.6, base2, CREAM) +
    label('Ceylon tea with natural vanilla', 6.2, 79.8) + label('12 tea bags · 24 g', 81.4, 79.8, { anchor: 'end' }) +
    `</g></svg>`;
  const file = `${String(i + 1).padStart(2, '0')}.svg`;
  fs.writeFileSync(path.join(out, file), svg);
  made.push({ file, name, src });
});
fs.writeFileSync(path.join(out, 'index.json'), JSON.stringify(made, null, 1));
console.log('made', made.length);
