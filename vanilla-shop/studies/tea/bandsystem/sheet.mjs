// node sheet.mjs <html> <png> <pdf|-> : preview PNG at 2x, and a PDF at the artboard's true size (pt -> mm)
import { createRequire } from 'module'; import fs from 'fs';
const require = createRequire('/opt/node-tools/node_modules/'); const { chromium } = require('playwright');
const [html, png, pdf] = process.argv.slice(2);
const src = fs.readFileSync(html, 'utf8'); const [, w, h] = src.match(/<svg[^>]*width="([\d.]+)pt" height="([\d.]+)pt"/);
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: Math.ceil(+w), height: Math.ceil(+h) }, deviceScaleFactor: 2 });
await p.goto('file://' + html); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(500);
await p.addStyleTag({ content: 'svg{width:' + w + 'px;height:' + h + 'px;display:block}' });
await p.screenshot({ path: png, clip: { x: 0, y: 0, width: +w, height: +h } });
if (pdf && pdf !== '-') {
  await p.addStyleTag({ content: `@page{size:${(w * 25.4 / 72).toFixed(2)}mm ${(h * 25.4 / 72).toFixed(2)}mm;margin:0} svg{width:${(w * 25.4 / 72).toFixed(2)}mm;height:${(h * 25.4 / 72).toFixed(2)}mm}` });
  await p.pdf({ path: pdf, width: (w * 25.4 / 72).toFixed(2) + 'mm', height: (h * 25.4 / 72).toFixed(2) + 'mm', printBackground: true, preferCSSPageSize: true });
}
await b.close(); console.log('sheet', w, h, 'pt');
