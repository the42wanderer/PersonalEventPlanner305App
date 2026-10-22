import { createRequire } from 'module';
const require = createRequire('/opt/node-tools/node_modules/');
const { chromium } = require('playwright'); const fs=require('fs');
const man=JSON.parse(fs.readFileSync(process.argv[2]));
const b=await chromium.launch(); const p=await b.newPage();
for (const [f,w,h] of man){ await p.goto('file://'+f+'.html'); await p.waitForTimeout(700);
  await p.pdf({path:f+'.pdf',width:w+'mm',height:h+'mm',printBackground:true}); }
await b.close();
