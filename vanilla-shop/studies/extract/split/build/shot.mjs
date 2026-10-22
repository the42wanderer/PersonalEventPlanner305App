import { createRequire } from 'module';
const require = createRequire('/opt/node-tools/node_modules/');
const { chromium } = require('playwright');
const [w,h,...files]=process.argv.slice(2); const b = await chromium.launch(); const p = await b.newPage({ viewport:{width:+w,height:+h} });
for (const f of files){ const src=f.endsWith('.svg')?f:f+'.html'; await p.goto('file://'+src); await p.waitForTimeout(400); await p.screenshot({path:f.replace(/\.(svg|html)$/,'')+'.png',omitBackground:true}); }
await b.close();
