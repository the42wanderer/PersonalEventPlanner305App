# Client report: The Vanilla Shop rebrand, before and after. A4 landscape, rendered to PDF with Chromium.
import json
R='/home/user/PersonalEventPlanner305App/vanilla-shop'
S='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad'
O=S+'/report/'
F={'IS':R+'/fonts/instrument-serif-italic.ttf','ISR':R+'/fonts/instrument-serif.ttf','AE':R+'/fonts/archivo-expanded-regular.ttf',
   'AL':R+'/fonts/archivo-expanded-light.ttf','G':R+'/fonts/geist-regular.ttf','GM':R+'/fonts/geist-medium.ttf','IV':S+'/candlefonts/ivy.otf'}
css=''.join(f"@font-face{{font-family:{k};src:url(file://{v})}}" for k,v in F.items())
INK='#2A2017'; MUTE='#7A6B5A'; PAPER='#F4EEE3'; GOLD='#A37A30'
LOGO=__import__('re').search(r' d="([^"]+)"',open(R+'/brand/vanilla-shop-logo.svg').read()).group(1)
def logo(w,c=INK): return f'<svg viewBox="0 0 933 963" width="{w}mm" height="{w*963/933:.1f}mm"><path d="{LOGO}" fill="{c}" fill-rule="evenodd"/></svg>'
def img(p,style=''): return f'<img src="file://{p}" style="{style}">'
def page(n,body,bg=PAPER,dark=False):
    c='#F4EEE3' if dark else MUTE
    return (f'<section class="pg" style="background:{bg}">{body}'
            f'<div class="foot" style="color:{c}"><span>The Vanilla Shop · Rebrand 2026</span><span>{n:02d}</span></div></section>')
def head(kicker,title,sub=''):
    return (f'<div class="kick">{kicker}</div><h1>{title}</h1>'+(f'<p class="lede">{sub}</p>' if sub else ''))
def cube(k,w=34,h=36,d=34,ry=-34,rx=-16,pre='cd'):
    f=lambda n:f'file://{O}{pre}-{k}-{n}.jpg'
    return (f'<div class="scene" style="width:{w*1.9}mm;height:{h*1.75}mm"><div class="cube" style="transform:translate(-50%,-50%) rotateX({rx}deg) rotateY({ry}deg)">'
            f'<div class="face" style="width:{w}mm;height:{h}mm;background-image:url({f("front")});transform:translate(-50%,-50%) translateZ({d/2}mm)"></div>'
            f'<div class="face" style="width:{d}mm;height:{h}mm;background-image:url({f("side")});transform:translate(-50%,-50%) rotateY(90deg) translateZ({w/2}mm)"><i style="background:rgba(0,0,0,.22)"></i></div>'
            f'<div class="face" style="width:{w}mm;height:{d}mm;background-image:url({f("top")});transform:translate(-50%,-50%) rotateX(90deg) translateZ({h/2}mm)"><i style="background:rgba(255,255,255,.06)"></i></div>'
            f'</div><div class="shadow" style="width:{w*1.5}mm"></div></div>')
OLD=O+'old/'; SOAP=R+'/export/soap-boxes-final/'
P=[]
# 1 cover
P.append(page(1,f'''<div style="position:absolute;inset:0;display:grid;grid-template-columns:1fr 1.25fr">
<div style="padding:22mm 0 0 20mm">{logo(26)}<div class="kick" style="margin-top:28mm">Packaging &amp; brand review</div>
<div style="font:58pt/0.95 ISR;color:{INK};margin-top:4mm">From a shelf of<br><i style="font-family:IS">strangers</i><br>to one family.</div>
<p class="lede" style="width:100mm;margin-top:8mm">What we changed across the range, why, and where The Vanilla Shop stands now: extracts, tea, bath bars, candles and the tote.</p></div>
<div style="position:relative;background:#E7DFD2;overflow:hidden">{img(O+"soap-3d.jpg","position:absolute;width:150%;left:-25%;top:6%")}
{img(R+"/studies/v5/mockup-pair.jpg","position:absolute;width:118%;left:-9%;bottom:-6%")}</div></div>'''))
# 2 where we started
P.append(page(2,f'''<div class="pad">{head("01 · Where we started","Thirteen products, six visual languages.",
"The range as it appears on thevanillashop.lk today. Every product was designed on its own: white-and-gold bottle labels, yellow floral soap boxes, kraft pouches with paper stickers, cloth bags, a green tea box and a black floral hamper. Each one is fine by itself. Together, they don’t look like one shop.")}</div>
<div style="position:absolute;left:20mm;right:20mm;top:68mm;bottom:16mm;background:#fff;display:flex;align-items:center;justify-content:center">{img(R+"/research/current-range-website.jpg","max-width:96%;max-height:96%")}</div>'''))
# 3 diagnosis
items=[('No family resemblance','The logo appears in a black square, a gold square, a sticker and plain. Type, colour and illustration change from product to product, so a customer who loves the extract has no visual cue that the soap comes from the same people.'),
       ('Decoration over information','Ornate gold frames, busy all-over florals and small centred text. The product name is often the third thing you see.'),
       ('Text that undermines trust','Unfinished headlines (“…Bathing Bar by”), misspellings (“benifits”), inconsistent spellings of the shop’s own name, broken Tamil characters, and incomplete ingredient lists.'),
       ('Nothing says “our own farm”','The brand’s strongest story, vanilla grown on its own farms in Sri Lanka, was a line of small print rather than the reason to buy.')]
P.append(page(3,f'''<div class="pad">{head("02 · What wasn’t working","Good products, let down by their packs.")}
<div class="grid2" style="margin-top:12mm">{"".join(f'<div class="card"><div class="num">{i+1}</div><h3>{t}</h3><p>{d}</p></div>' for i,(t,d) in enumerate(items))}</div></div>'''))
# 4 approach
rows=[('Extracts','Home bakers, cooks; informed buyers','Purity, origin, how to use','Painted vanilla, numbered range, full information'),
      ('Tea','Tea drinkers, gifting, tourists','Ceylon, provenance, calm','Painted botanical on cream, Ceylon Tea lion, brewing guide'),
      ('Bath bars','Everyone, often on impulse','Pretty, gentle, which scent','Soft colour-coded bloom, big clear names, gold foil'),
      ('Candles','Everyone, mostly as a gift','Mood, a present that looks expensive','Deep colour, bold name, painted florals'),
      ('Tote','Fans, tourists','Heritage, craft, Sri Lanka','Engraved Ceylon scene, one ink')]
sig=[('The logo','On every product, never altered.'),('The vanilla flower','Somewhere on every pack, drawn to suit the line.'),
     ('Serif names','Product names in a serif; details in spaced capitals.'),('Printed, not digital','Warm grounds, grain and texture; no gloss.'),
     ('Our own farms','The origin claim on every pack.')]
P.append(page(4,f'''<div class="pad">{head("03 · The approach","One brand. Each line dressed for its own shelf.",
"Tea is bought by tea drinkers; soap is bought by everyone. Rather than force one look onto very different categories, each line got the look its shoppers expect, and all of them share five signals that carry the brand from one to the next.")}
<div style="display:grid;grid-template-columns:1.55fr 1fr;gap:12mm;margin-top:9mm">
<table><tr><th>Line</th><th>Who buys it</th><th>What it must say</th><th>How the design says it</th></tr>
{"".join(f'<tr><td class="ln">{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>' for a,b,c,d in rows)}</table>
<div><div class="kick" style="margin-bottom:3mm">Shared by every line</div>{"".join(f'<div class="sig"><b>{a}</b><span>{b}</span></div>' for a,b in sig)}</div></div></div>'''))
# 5 system
sw=[('Extracts',['#B3311E','#D79A2B','#3E6B3A','#F1E8D6']),('Tea',['#1F4A2C','#F6E7C2','#E8B9A0','#6A3B1E']),
    ('Bath bars',['#B5620F','#A8324E','#141414','#2F5A2D']),('Candles',['#7E1F25','#1C2350','#244A2A','#C9922A'])]
P.append(page(5,f'''<div class="pad">{head("04 · The system","What every designer works from.")}
<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10mm;margin-top:9mm">
<div><div class="kick">Logo</div><div style="display:flex;gap:8mm;align-items:center;margin-top:4mm">{logo(24)}{logo(16,'#5A1426')}{logo(12,'#16301C')}</div>
<p class="small" style="margin-top:4mm">One mark, in the line’s darkest colour or in gold foil. Never boxed, framed or recoloured beyond that.</p>
<div class="kick" style="margin-top:9mm">Type</div>
<div style="font:30pt/1 ISR;color:{INK};margin-top:3mm">Vanilla <i style="font-family:IS">&amp; Rose</i></div><p class="small">Instrument Serif: product names</p>
<div style="font:9pt AE;letter-spacing:.25em;color:{INK};margin-top:4mm">100% NATURAL · SRI LANKA</div><p class="small">Archivo Expanded: details, in spaced capitals</p>
<div style="font:28pt/1 IV;color:{INK};margin-top:4mm">VELVET</div><p class="small">Ivy Presto: the candle line only</p></div>
<div><div class="kick">One flower, four ways</div><div class="flw">
{img(R+"/plates/generated/v6-vine.png")}<span>Painted · tea &amp; extracts</span>
{img(R+"/studies/soap/bloom-duo/art-rosette.jpg")}<span>Bloom · bath-bar fronts</span>
{img(S+"/bw/spray-test.png")}<span>Engraved · tote &amp; bath-bar backs</span>
{img(O+"cd-velvet-side.jpg")}<span>Florals · candles</span></div></div>
<div><div class="kick">Colour, by line</div>{"".join(f'<div style="margin-top:4mm"><div class="small" style="margin-bottom:1.5mm">{n}</div><div style="display:flex;gap:1.5mm">'+"".join(f'<div style="width:14mm;height:9mm;background:{c};border-radius:1mm"></div>' for c in cs)+'</div></div>' for n,cs in sw)}
<div style="margin-top:6mm;display:flex;gap:3mm;align-items:center"><div style="width:14mm;height:9mm;border-radius:1mm;background:linear-gradient(110deg,#4E300A,#C9A55A 45%,#76521A 60%,#A37A30)"></div><span class="small">Gold foil: “Vanilla”, the house signature</span></div></div></div></div>'''))
# 6 extracts
P.append(page(6,f'''<div class="pad">{head("05 · Vanilla extracts &amp; syrup","A numbered range you can read across the room.")}</div>
<div class="ba"><div class="b">{img(OLD+"alcoholic-vanilla-extracts.jpg","width:100%")}<div class="tag">Before</div></div>
<div class="a" style="background:#EDE7DC">{img(O+"extract-range.jpg","width:100%")}<div class="tag">After</div></div></div>
<div class="notes">{"".join(f'<div><b>{a}</b>{b}</div>' for a,b in [("Split label","Painted vanilla on one side, clean information on the other; the label reads at a glance."),("No. 01 · 02 · 03","Alcoholic extract, non-alcoholic extract and syrup become a collectable, numbered set, each with its own colour."),("Same information","Every fact from the old labels is kept, re-set to be readable; the history line was corrected."),("Print-ready","500, 200 and 100 ml labels and neck seals, with bleed and cut lines.")])}</div>'''))
# 7 tea
P.append(page(7,f'''<div class="pad">{head("06 · Natural vanilla tea","The kraft pouch stays. Everything on it changes.")}</div>
<div class="ba"><div class="b" style="display:flex;gap:3mm;align-items:center;justify-content:center;padding:0 4mm">{img(OLD+"vanilla_ceylon_tea_1.jpg","width:58%")}{img(O+"tea-box-old.jpg","width:34%")}</div>
<div class="a" style="display:grid;grid-template-columns:0.85fr 1.15fr;gap:3mm;padding:0 3mm;background:#F4F1EB;align-items:center">{img(O+"tea-pouches-new.jpg","width:100%")}{img(O+"tea-boxes-new.jpg","width:100%")}<div class="tag">After</div></div></div>
<div class="tagb">Before</div>
<div class="notes">{"".join(f'<div><b>{a}</b>{b}</div>' for a,b in [("Same kraft pouch","The 100 g stand-up pouch is kept; a new arched paper label replaces the sticker, for Vanilla Tea and Vanilla &amp; Cinnamon Tea."),("Boxes for gifting","A 25-bag and a 12-bag carton replace the green sachet box, in the same painted style as the pouch labels."),("Painted vanilla","Flower, vine and cured pods (and cinnamon quills), painted to match the extracts."),("Ceylon credentials","The Ceylon Tea lion and “Authentic Ceylon” on every pack; a brewing guide on the boxes.")])}</div>'''))
# 8 soaps
P.append(page(8,f'''<div class="pad">{head("07 · Bath bars","Same box, a completely different feeling.")}</div>
<div class="ba" style="grid-template-columns:1fr 1.35fr"><div class="b" style="display:grid;grid-template-columns:1fr 1fr;align-content:center">{"".join(img(OLD+f+"_1.jpg","width:100%") for f in ["vanilla","rosette","charcoal","aloe_vera"])}</div>
<div class="a" style="background:#E6E0D5;display:flex;align-items:center">{img(O+"soap-3d.jpg","width:112%;margin-left:-6%")}<div class="tag">After</div></div></div>
<div class="tagb">Before</div>
<div class="notes">{"".join(f'<div><b>{a}</b>{b}</div>' for a,b in [("Same die, same print","The folded octagon box is unchanged; only the artwork is new."),("Colour tells you which","Honey, rose, charcoal and aloe glow on a light, grainy paper; a shopper finds their scent instantly."),("“Vanilla” in gold foil","Every bar opens with the same foiled word, so the four read as one set."),("Clearer names","Vanilla Bathing Bar · Vanilla &amp; Rose · Vanilla &amp; Charcoal+ · Vanilla &amp; Aloe Vera.")])}</div>'''))
# 9 soap detail
P.append(page(9,f'''<div class="pad">{head("Bath bars · the details","Built to be picked up and turned over.")}</div>
<div style="position:absolute;left:20mm;right:20mm;top:52mm;bottom:18mm;display:grid;grid-template-columns:1.25fr 1fr;gap:8mm">
<div style="background:#E6E0D5;display:flex;align-items:center;justify-content:center">{img(SOAP+"fronts.png","width:100%")}</div>
<div style="display:grid;grid-template-rows:1fr auto;gap:5mm"><div style="background:#fff;display:flex;align-items:center;justify-content:center;overflow:hidden">{img(O+"soap-back-clean.jpg","width:100%")}</div>
<p class="small">The back carries the brand’s engraved vanilla as a faint watermark and a small gold-foil pod; the flower wraps over the walls. Text is in English, Sinhala and Tamil, set properly, with the typos of the old box corrected.</p></div></div>'''))
# 10 candles
P.append(page(10,f'''<div class="pad">{head("08 · Scented candles","Same box, a new identity for each mood.")}</div>
<div style="position:absolute;left:20mm;right:20mm;top:44mm;height:52mm;background:#fff;display:flex;justify-content:space-around;align-items:center">{"".join(cube(k,22,23,22,pre="old") for k in ["velvet","aura","harmony","zest"])}<div class="tag">Before</div></div>
<div style="position:absolute;left:20mm;right:20mm;top:100mm;height:60mm;background:#E2DACD;display:flex;justify-content:space-around;align-items:center">{"".join(cube(k,25,26,25) for k in ["velvet","aura","harmony","zest"])}<div class="tag">After</div></div>
<div class="notes" style="top:166mm">{"".join(f'<div><b>{a}</b>{b}</div>' for a,b in [("Same die","The 90 × 90 × 95 mm carton is unchanged; only the artwork is new."),("A name you can see","The old boxes showed a small script name on a colour sticker over a dark logo pattern. Now the name is the hero, across the corner of the box."),("Each mood its own world","Velvet, Aura, Harmony and Zest each get a deep colour and their own painted florals, so the set reads as a gift range."),("Full information","Notes and mood, safety icons, contents and maker details, set clearly on the sides.")])}</div>''',bg='#EAE3D7'))
# 11 tote
P.append(page(11,f'''<div style="position:absolute;inset:0;display:grid;grid-template-columns:1fr 1fr">
<div class="pad">{head("09 · The tote","The brand you carry out of the shop.","A one-ink screen print: an engraved Ceylon harvest scene inside a stamp, drawn as a comic-era halftone. One colour keeps it affordable to print and easy to reorder.")}</div>
<div style="background:#D9D2C4;display:flex;align-items:center;justify-content:center;overflow:hidden">{img(R+"/export/tote/1ink-halftone/tote-stamp-halftone_mockup.jpg","height:100%")}</div></div>'''))
# 12 line-up now
P.append(page(12,f'''<div class="pad">{head("10 · Where the brand is now","One shop, five lines, unmistakably related.")}</div>
<div style="position:absolute;left:14mm;right:14mm;top:50mm;bottom:16mm;display:grid;grid-template-columns:1.2fr 1fr 0.55fr;grid-template-rows:1fr 1fr;gap:4mm">
<div style="background:#EDE7DC;display:flex;align-items:center;overflow:hidden">{img(O+"extract-range.jpg","width:100%")}</div>
<div style="background:#F4F1EB;display:grid;grid-template-columns:0.85fr 1.15fr;gap:2mm;padding:0 2mm;align-items:center;overflow:hidden">{img(O+"tea-pouches-new.jpg","width:100%")}{img(O+"tea-boxes-new.jpg","width:100%")}</div>
<div style="grid-row:span 2;background:#D9D2C4;overflow:hidden;display:flex;justify-content:center">{img(R+"/export/tote/1ink-halftone/tote-stamp-halftone_mockup.jpg","height:100%")}</div>
<div style="background:#E6E0D5;display:flex;align-items:center;overflow:hidden">{img(O+"soap-3d.jpg","width:100%")}</div>
<div style="background:#EAE3D7;display:flex;justify-content:space-around;align-items:center;overflow:hidden">{"".join(cube(k,17,18,17) for k in ["velvet","aura","harmony","zest"])}</div></div>'''))
# 13 status
st=[('Ready for print','Extract labels: three sizes plus neck seals, with bleed and cut lines.','Bath bars: print, foil-plate and proof files for all four boxes.','Tote: one-ink print film.'),
    ('Ready to adapt','Tea: editable dielines and fronts.','Candles: editable box and label files for four scents.',''),
    ('To confirm before printing','Barcodes, dates and TFM for Charcoal+ and Aloe Vera; net weight of the bars (100 g or 114 g).','Full ingredient lists per product; a native-speaker check of Sinhala and Tamil; cosmetic claims against NMRA rules.','A physical foil proof and a check of every die against the printer’s.')]
P.append(page(13,f'''<div class="pad">{head("11 · Status &amp; next steps","What’s done, and what the team finishes.")}
<div class="grid3" style="margin-top:10mm">{"".join(f'<div class="card"><h3>{t}</h3>'+"".join(f'<p>{x}</p>' for x in xs if x)+'</div>' for t,*xs in st)}</div>
<div style="position:absolute;right:20mm;bottom:20mm;display:flex;align-items:center;gap:5mm">{logo(14)}<span style="font:15pt IS;color:{INK}">Where every bean tells a story.</span></div></div>'''))
html=(f'<html><head><meta charset="utf-8"><style>{css}@page{{size:297mm 210mm;margin:0}}html,body{{margin:0}}'
 f'.pg{{position:relative;width:297mm;height:210mm;overflow:hidden;break-after:page;font-family:G;color:{INK}}}'
 f'.pad{{padding:16mm 20mm 0 20mm}}.kick{{font:7.2pt AE;letter-spacing:.28em;text-transform:uppercase;color:{GOLD}}}'
 f'h1{{font:34pt/1.02 ISR;margin:3mm 0 0;letter-spacing:-.01em}}h3{{font:15pt/1.15 ISR;margin:0 0 2mm}}'
 f'.lede{{font:10.5pt/1.5 G;color:{MUTE};max-width:200mm;margin:4mm 0 0}}.small{{font:8pt/1.45 G;color:{MUTE};margin:1mm 0 0}}'
 f'.foot{{position:absolute;left:20mm;right:20mm;bottom:7mm;display:flex;justify-content:space-between;font:6.5pt AE;letter-spacing:.2em;text-transform:uppercase}}'
 f'.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:7mm}}.grid3{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:7mm}}'
 f'.card{{background:#FBF8F2;border:0.3mm solid #E3D9C8;padding:7mm;border-radius:1.5mm}}.card p{{font:9pt/1.5 G;color:#4A3E31;margin:0 0 2mm}}'
 f'.num{{font:26pt IS;color:{GOLD};line-height:1;margin-bottom:2mm}}'
 f'table{{border-collapse:collapse;font:8.4pt/1.4 G;width:100%}}th{{font:6.5pt AE;letter-spacing:.2em;text-transform:uppercase;color:{GOLD};text-align:left;padding:0 3mm 2.5mm 0;border-bottom:0.3mm solid #CDBFA8}}'
 f'td{{padding:3mm 3mm 3mm 0;border-bottom:0.2mm solid #E3D9C8;vertical-align:top;color:#4A3E31}}td.ln{{font:13pt ISR;color:{INK}}}'
 f'.sig{{display:grid;grid-template-columns:34mm 1fr;padding:2.6mm 0;border-bottom:0.2mm solid #E3D9C8;font:8.6pt/1.4 G;color:#4A3E31}}.sig b{{font:12pt ISR;color:{INK};font-weight:normal}}'
 f'.flw{{display:grid;grid-template-columns:22mm 1fr;gap:2.5mm 4mm;align-items:center;margin-top:4mm}}.flw img{{width:22mm;height:22mm;object-fit:cover;border-radius:1mm;background:#fff}}.flw span{{font:8pt G;color:{MUTE}}}'
 f'.ba{{position:absolute;left:20mm;right:20mm;top:46mm;height:112mm;display:grid;grid-template-columns:1fr 1.5fr;gap:6mm}}'
 f'.ba>div{{position:relative;background:#fff;overflow:hidden;display:flex;align-items:center;justify-content:center}}'
 f'.tag,.tagb{{position:absolute;left:4mm;top:4mm;font:6.5pt AE;letter-spacing:.25em;text-transform:uppercase;background:{INK};color:#F4EEE3;padding:1.6mm 2.6mm;border-radius:.6mm}}'
 f'.tagb{{left:24mm;top:50mm}}'
 f'.notes{{position:absolute;left:20mm;right:20mm;top:163mm;display:grid;grid-template-columns:repeat(4,1fr);gap:6mm;font:8pt/1.45 G;color:#4A3E31}}.notes b{{display:block;font:11.5pt ISR;color:{INK};font-weight:normal;margin-bottom:1mm}}'
 f'.scene{{position:relative;perspective:260mm}}.cube{{position:absolute;left:50%;top:50%;transform-style:preserve-3d}}'
 f'.face{{position:absolute;left:0;top:0;background-size:100% 100%;backface-visibility:hidden}}.face i{{position:absolute;inset:0}}'
 f'.shadow{{position:absolute;left:50%;bottom:-2mm;height:7mm;transform:translateX(-50%);background:radial-gradient(closest-side,rgba(40,25,10,.28),transparent);z-index:-1}}'
 f'</style></head><body>{"".join(P)}</body></html>')
open(O+'report.html','w').write(html)
json.dump([[O+'report',297,210]],open(O+'man.json','w'))
print('pages',len(P))
