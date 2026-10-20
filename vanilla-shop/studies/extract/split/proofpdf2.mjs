import { createRequire } from 'module';
const require = createRequire('/opt/node-tools/node_modules/');
const { chromium } = require('playwright'); const fs=require('fs');
const [out,label,...specs]=process.argv.slice(2);   // spec: file|W|H|caption
const T='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/ext/d/';
let html=`<html><head><style>@page{size:246mm 100mm;margin:0}html,body{margin:0;font-family:sans-serif}
.p{position:relative;width:246mm;height:100mm;page-break-after:always}img{position:absolute;left:7mm;top:7mm}
svg{position:absolute;left:0;top:0;width:246mm;height:100mm}.s{position:absolute;left:10mm;top:88mm;font-size:2.6mm;color:#333}
.k{display:inline-block;width:3mm;height:2mm;margin:0 1mm 0 4mm;vertical-align:-0.2mm;opacity:.5}</style></head><body>`;
for(const sp of specs){
  const [f,w,h,cap]=sp.split('|'); const W=+w,H=+h, x0=10,y0=10,x1=10+W,y1=10+H;
  const m=[[x0,y0],[x1,y0],[x0,y1],[x1,y1]].map(([x,y])=>{const dx=x==x0?-1:1,dy=y==y0?-1:1;
    return `<path d="M${x+dx*3} ${y}H${x+dx*9}M${x} ${y+dy*3}V${y+dy*9}" stroke="#000" stroke-width="0.15"/>`}).join('');
  html+=`<div class="p"><img src="file://${T}${f}" style="width:${W+6}mm;height:${H+6}mm"><svg viewBox="0 0 246 100">${m}</svg>
  <div class="s" style="top:${y1+10}mm">${cap} · trim ${W} × ${H} mm · bleed 3 mm · ${label}
  <span class="k" style="background:#FF2BA6"></span>estimate or unknown: confirm<span class="k" style="background:#12B5EA"></span>calculated or from the listings: check</div></div>`;}
html+='</body></html>'; fs.writeFileSync(T+'proofpdf.html',html);
const b=await chromium.launch(); const p=await b.newPage(); await p.goto('file://'+T+'proofpdf.html'); await p.waitForTimeout(1500);
await p.pdf({path:out,width:'246mm',height:'100mm',printBackground:true}); await b.close();
