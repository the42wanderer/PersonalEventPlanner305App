// Writes Illustrator-ready SVG print sheets (one per colourway) and PNG previews.
// Usage: npm install && npm run export
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const opentype = require('opentype.js');
const dir = path.dirname(path.dirname(fileURLToPath(import.meta.url)));

await import(path.join(dir, 'dieline.js'));
await import(path.join(dir, 'art.js'));
const VS = globalThis.VS;
const font = (f) => opentype.loadSync(path.join(dir, 'fonts', f));
VS.setFonts({
  display: font('fraunces-display.ttf'), italic: font('fraunces-italic.ttf'),
  sans: font('geist-medium.ttf'), bold: font('geist-bold.ttf'), mono: font('geist-mono.ttf'),
});

const out = path.join(dir, 'export');
fs.mkdirSync(out, { recursive: true });
for (const cw of Object.keys(VS.COLORWAYS)) {
  fs.writeFileSync(path.join(out, `natural-vanilla-tea_${cw}_dieline.svg`), VS.sheetSVG(cw, { paper: '#FFFFFF' }));
  fs.writeFileSync(path.join(out, `natural-vanilla-tea_${cw}_front.svg`), VS.faceSVG('front', cw));
}
console.log('Box (mm):', Object.fromEntries(Object.entries(VS.BOX).map(([k, v]) => [k, v.toFixed(2)])));
console.log('Wrote', fs.readdirSync(out).length, 'files to', out);
