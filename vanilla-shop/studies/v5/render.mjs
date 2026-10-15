// Renders studies/v5/out/*.svg to PNG at 12 px/mm, then cuts each strip into box faces
// (out/<key>/face-*.jpg) for the 3D mock-up. Usage: node studies/v5/render.mjs [prefix]
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const out = path.join(path.dirname(fileURLToPath(import.meta.url)), 'out');
const PPM = 12, CSS_PER_MM = 96 / 25.4;
const only = process.argv[2] || '';
const files = fs.readdirSync(out).filter((f) => f.endsWith('.svg') && f.startsWith(only));
const browser = await chromium.launch();
for (const f of files) {
  const svg = fs.readFileSync(path.join(out, f), 'utf8');
  const [wmm, hmm] = svg.match(/width="([\d.]+)mm" height="([\d.]+)mm"/).slice(1).map(Number);
  const page = await browser.newPage({ viewport: { width: Math.ceil(wmm * CSS_PER_MM), height: Math.ceil(hmm * CSS_PER_MM) }, deviceScaleFactor: PPM / CSS_PER_MM });
  await page.goto('file://' + path.join(out, f));
  await page.waitForTimeout(300);
  await page.screenshot({ path: path.join(out, f.replace('.svg', '.png')), clip: { x: 0, y: 0, width: wmm * CSS_PER_MM, height: hmm * CSS_PER_MM } });
  await page.close();
}
await browser.close();
execFileSync('python3', ['-c', `
import json, os, sys
from PIL import Image
out = sys.argv[1]; only = sys.argv[2]; ppm = 12
L = json.load(open(os.path.join(out, 'faces.json')))
for f in sorted(os.listdir(out)):
    if not f.endswith('.png') or f.startswith('plate') or not f.startswith(only) or f.endswith('-top.png') or f.endswith('-bottom.png'):
        continue
    key = f[:-4]; d = os.path.join(out, key); os.makedirs(d, exist_ok=True)
    im = Image.open(os.path.join(out, f)).convert('RGB')
    for name, (x, w) in L['FACES'].items():
        im.crop((round(x * ppm), 0, round((x + w) * ppm), round(L['H'] * ppm))).save(os.path.join(d, 'face-%s.jpg' % name), quality=90)
    for side in ('top', 'bottom'):
        Image.open(os.path.join(out, key + '-' + side + '.png')).convert('RGB').save(os.path.join(d, 'face-%s.jpg' % side), quality=90)
`, out, only]);
console.log('rendered', files.length);
