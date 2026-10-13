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

// Plate dimensions are read from the JPEG header so the embed keeps its true aspect ratio.
const plateFile = path.join(dir, 'plates', 'de-alwis-vanilla.jpg');
const jpg = fs.readFileSync(plateFile);
function jpegSize(b) {
  let i = 2;
  while (i < b.length) {
    const marker = b[i + 1], len = b.readUInt16BE(i + 2);
    if (marker >= 0xC0 && marker <= 0xC3) return { h: b.readUInt16BE(i + 5), w: b.readUInt16BE(i + 7) };
    i += 2 + len;
  }
  throw new Error('Not a JPEG: ' + plateFile);
}
VS.setImages({ plate: { href: 'data:image/jpeg;base64,' + jpg.toString('base64'), ...jpegSize(jpg) } });

const out = path.join(dir, 'export');
fs.mkdirSync(out, { recursive: true });
for (const cw of Object.keys(VS.COLORWAYS)) {
  fs.writeFileSync(path.join(out, `natural-vanilla-tea_${cw}_dieline.svg`), VS.sheetSVG(cw, { paper: '#FFFFFF' }));
  fs.writeFileSync(path.join(out, `natural-vanilla-tea_${cw}_front.svg`), VS.faceSVG('front', cw));
}
console.log('Box (mm):', Object.fromEntries(Object.entries(VS.BOX).map(([k, v]) => [k, v.toFixed(2)])));
console.log('Wrote', fs.readdirSync(out).length, 'files to', out);
