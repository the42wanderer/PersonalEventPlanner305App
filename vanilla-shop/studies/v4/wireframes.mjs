// v4 direction wireframes on the real front panel (87.66 x 84.74 mm).
// Code-made parts are final-quality; grey hatched boxes mark generated assets still to come.
// Draft type uses Fontshare fonts from a local folder (not committed; ITF FFL forbids redistribution).
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const opentype = require('opentype.js');
const root = path.dirname(path.dirname(path.dirname(fileURLToPath(import.meta.url))));
const FS = process.env.FONTSHARE_DIR;
const F = {
  name: opentype.loadSync(path.join(FS, 'gambarino/Gambarino_Complete/Fonts/OTF/Gambarino-Regular.otf')),
  sans: opentype.loadSync(path.join(FS, 'general-sans/GeneralSans_Complete/Fonts/OTF/GeneralSans-Medium.otf')),
};
const W = 87.66, H = 84.74, M = 7;
const C = { espresso: '#1E1511', cream: '#FBF6EC', gold: '#C6A668', amber: '#C9832F', honey: '#E8B04B', tea: '#3E5B3A', sage: '#C9D2B4' };
const n = (v) => Math.round(v * 1000) / 1000;

function text(f, s, sz, x, y, fill, o = {}) {
  const str = o.caps ? s.toUpperCase() : s;
  const w = f.getAdvanceWidth(str, sz) + (o.track || 0) * sz * (str.length - 1);
  let cx = o.anchor === 'end' ? x - w : o.anchor === 'middle' ? x - w / 2 : x, d = '';
  for (const ch of str) { d += f.getPath(ch, cx, y, sz).toPathData(2); cx += f.getAdvanceWidth(ch, sz) + (o.track || 0) * sz; }
  return `<path d="${d}" fill="${fill}"${o.transform ? ` transform="${o.transform}"` : ''}/>`;
}
const label = (s, x, y, fill, o = {}) => text(F.sans, s, 1.9, x, y, fill, { caps: true, track: 0.12, ...o });
const logoSrc = fs.readFileSync(path.join(root, 'brand', 'vanilla-shop-logo.svg'), 'utf8');
const logo = (x, y, w, fill) => `<path fill="${fill}" fill-rule="evenodd" d="${logoSrc.match(/ d="([^"]+)"/)[1]}" transform="translate(${x} ${y}) scale(${n(w / Number(logoSrc.match(/viewBox="0 0 ([\d.]+)/)[1]))})"/>`;
// Placeholder for a generated asset: hatched box + spec label.
const slot = (x, y, w, h, lines, dark = false) => {
  const c = dark ? '#FFFFFF' : '#000000';
  return `<g opacity="0.55"><rect x="${x}" y="${y}" width="${w}" height="${h}" fill="url(#hatch${dark ? 'D' : ''})" stroke="${c}" stroke-width="0.25" stroke-dasharray="1 0.7"/>` +
    lines.map((l, i) => text(F.sans, l, 1.7, x + w / 2, y + h / 2 + (i - (lines.length - 1) / 2) * 2.5 + 0.6, c, { anchor: 'middle', caps: true, track: 0.06 })).join('') + '</g>';
};
const defs = `<defs><pattern id="hatch" width="2" height="2" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="2" height="2" fill="#00000010"/><path d="M0 0V2" stroke="#00000022" stroke-width="0.4"/></pattern>` +
  `<pattern id="hatchD" width="2" height="2" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="2" height="2" fill="#FFFFFF10"/><path d="M0 0V2" stroke="#FFFFFF33" stroke-width="0.4"/></pattern></defs>`;
const svg = (bg, body) => `<svg xmlns="http://www.w3.org/2000/svg" width="${W}mm" height="${H}mm" viewBox="0 0 ${W} ${H}">${defs}<clipPath id="p"><rect width="${W}" height="${H}"/></clipPath><g clip-path="url(#p)"><rect x="-5" y="-5" width="${W + 10}" height="${H + 10}" fill="${bg}"/>${body}</g></svg>`;

function rng(seed) { let t = seed >>> 0; return () => { t += 0x6D2B79F5; let r = Math.imul(t ^ (t >>> 15), 1 | t); r ^= r + Math.imul(r ^ (r >>> 7), 61 | r); return ((r ^ (r >>> 14)) >>> 0) / 4294967296; }; }

// Grain plume: fine stochastic dots whose density follows a soft rising, swaying column (the aroma).
// Colour shifts from amber at the cup to honey higher up; density thins towards the top and edges.
function plume(cx, base, top, maxW, count, seed) {
  const rand = rng(seed), layers = { [C.amber]: '', [C.honey]: '', [C.gold]: '' };
  for (let i = 0; i < count; i++) {
    const t = Math.pow(rand(), 0.85);
    const y = base - t * (base - top);
    const sway = Math.sin(t * 4.2) * 4 * t + Math.sin(t * 9.5) * 1.2 * t;
    const half = maxW / 2 * (0.32 + 0.68 * Math.sin(Math.min(1, t * 1.25) * Math.PI / 2));
    const g = (rand() + rand() + rand()) / 3 * 2 - 1;          // soft, centre-weighted spread
    const keep = (1 - Math.pow(t, 1.8)) * (1 - Math.pow(Math.abs(g), 2.4));
    if (rand() > keep) continue;
    const x = cx + sway + g * half, r = 0.07 + rand() * 0.07;
    const col = t < 0.28 + rand() * 0.2 ? C.amber : (rand() < 0.75 ? C.honey : C.gold);
    layers[col] += `M${n(x - r)} ${n(y)}a${n(r)} ${n(r)} 0 1 0 ${n(2 * r)} 0a${n(r)} ${n(r)} 0 1 0 ${n(-2 * r)} 0`;
  }
  return Object.entries(layers).map(([c, d]) => `<path d="${d}" fill="${c}"/>`).join('');
}
// Dappled shade mood preview: blurred vanilla-leaf (long oval) shadows.
function dapple(seed) {
  const rand = rng(seed); let s = '<filter id="soft"><feGaussianBlur stdDeviation="1.1"/></filter><g filter="url(#soft)" fill="#2E3A24" opacity="0.32">';
  for (let i = 0; i < 26; i++) {
    const x = rand() * (W + 20) - 10, y = rand() * (H + 10) - 5, a = rand() * 180, L = 14 + rand() * 12;
    s += `<ellipse cx="${n(x)}" cy="${n(y)}" rx="${n(L / 2)}" ry="${n(L * 0.18)}" transform="rotate(${n(a)} ${n(x)} ${n(y)})"/>`;
  }
  return s + '</g>';
}

const name = (x, y, sz, fill) => text(F.name, 'Vanilla Tea', sz, x, y, fill);
const sizeFor = (w) => w / F.name.getAdvanceWidth('Vanilla Tea', 1);

const designs = {
  // 1. AROMA: a grain plume of warm vanilla tones rising from a cup; one real cured pod rests across the cup.
  aroma: () => {
    const sz = sizeFor(W - 2 * M);
    return svg(C.cream, [
      plume(W / 2 + 1, 64, 21, 46, 60000, 7),
      `<path d="M${n(W / 2 - 13)} 63.5h28q-1.2 13.5 -14 13.5t-14 -13.5Z" fill="${C.espresso}"/>`,
      `<ellipse cx="${n(W / 2 + 1)}" cy="63.6" rx="13.6" ry="1.5" fill="${C.amber}"/>`,
      slot(W / 2 - 25, 57.5, 52, 7, ['Photo: cured vanilla pod', 'across the cup rim']),
      name(M, 18, sz, C.espresso),
      logo(M, H - 14.5, 12, C.espresso),
      label('Ceylon black tea', W - M, H - 10.2, C.espresso, { anchor: 'end' }),
      label('with natural vanilla', W - M, H - 7.2, C.espresso, { anchor: 'end' }),
    ].join(''));
  },
  // 2. OBJECT ON COLOUR: real pod and tea sprig, crossed, hard daylight, oversized, on a flat tea-green field.
  object: () => {
    const sz = sizeFor(W - 2 * M);
    return svg(C.tea, [
      slot(-6, 14, W + 12, 52, ['Photo: cured vanilla pod + tea sprig', 'crossed, hard sun, cast shadow', 'on flat #3E5B3A, bleeds off both sides'], true),
      name(M, H - 9, sz, C.cream),
      logo(M, 6, 12, C.cream),
      label('Ceylon black tea with natural vanilla', W - M, 10, C.cream, { anchor: 'end' }),
      label('12 tea bags · 24 g', W - M, 13, C.sage, { anchor: 'end' }),
    ].join(''));
  },
  // 3. SHADE GARDEN: afternoon light through vanilla leaves across the whole box; a glass of tea and a pod.
  shade: () => {
    const sz = sizeFor(W - 2 * M);
    return svg('#EFE4CC', [
      dapple(11),
      slot(W - 42, 28, 38, 40, ['Photo, full bleed 2:1:', 'glass of tea + pod in', 'vanilla-leaf shade', '(mood preview behind)']),
      name(M, 18, sz, C.espresso),
      logo(M, H - 14.5, 12, C.espresso),
      label('Ceylon black tea', M + 15, H - 10.2, C.espresso),
      label('with natural vanilla', M + 15, H - 7.2, C.espresso),
    ].join(''));
  },
};
const out = path.join(root, 'studies', 'v4');
for (const [k, fn] of Object.entries(designs)) fs.writeFileSync(path.join(out, `front_${k}.svg`), fn());
console.log('wrote', Object.keys(designs).join(', '));
