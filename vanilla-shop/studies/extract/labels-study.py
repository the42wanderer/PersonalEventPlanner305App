import re, json
R='/home/user/PersonalEventPlanner305App/vanilla-shop'; CF='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/candlefonts'
T='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/ext/lab'
logoD=re.search(r' d="([^"]+)"',open(R+'/brand/vanilla-shop-logo.svg').read()).group(1)
SKU={
 'alc':  dict(no='No. 01', l1='Vanilla', l2='Extract', kind='WITH ALCOHOL', desc=['Pure Ceylon vanilla','in a classic extract'], use='Baking and custards', dose='1 tsp per cake', g='#B83A24', ink='#F6E2C6', sub='#F2C9A4'),
 'free': dict(no='No. 02', l1='Vanilla', l2='Extract', kind='ALCOHOL-FREE', desc=['Pure Ceylon vanilla,','no alcohol'], use='Desserts and drinks', dose='1 tsp per cake', g='#E0A53A', ink='#3B2108', sub='#6A3E10'),
 'syrup':dict(no='No. 03', l1='Vanilla', l2='Syrup', kind='NATURAL SYRUP', desc=['Ceylon vanilla syrup','for coffee and shakes'], use='Coffee and shakes', dose='2 tsp per cup', g='#21402A', ink='#E7EFCF', sub='#B9CC98'),
}
W,H=80,70
css=(f"@font-face{{font-family:IS;src:url(file://{R}/fonts/instrument-serif-italic.ttf)}}"
     f"@font-face{{font-family:RW;src:url(file://{CF}/roc-wide-regular.otf)}}@font-face{{font-family:RWL;src:url(file://{CF}/roc-wide-light.otf)}}@font-face{{font-family:RR;src:url(file://{CF}/roc-regular.otf)}}")
def caps(t,x,y,sz,c,anchor='start',f='RW',tr=0.3,op=1):
    return f'<text x="{x}" y="{y}" font-family="{f}" font-size="{sz}" letter-spacing="{sz*tr:.2f}" fill="{c}" text-anchor="{anchor}" opacity="{op}">{t}</text>'
def rule(x1,y1,x2,y2,c,w=0.22,op=0.7): return f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{c}" stroke-width="{w}" opacity="{op}"/>'
def logo(cx,cy,lw,c): s=lw/933; return f'<path d="{logoD}" fill="{c}" fill-rule="evenodd" transform="translate({cx-lw/2:.2f} {cy-963*s/2:.2f}) scale({s:.5f})"/>'
def art(k,x,y,w): h=w*1651/3808; return f'<image href="file://{T}/tone-v6-vine-2x-{k}.png" x="{x}" y="{y}" width="{w}" height="{h:.2f}"/>'
def A(k):
    s=SKU[k]; c=s['ink']; o=[f'<rect width="{W}" height="{H}" fill="{s["g"]}"/>']
    o.append(art(k,20,10,118))
    o+= [caps('THE VANILLA SHOP',6,8.2,2.1,c), caps(s['no'],W-6,8.2,2.1,c,'end'), rule(6,10,W-6,10,c)]
    o.append(f'<text font-family="IS" font-size="17" fill="{c}"><tspan x="5.2" y="27">{s["l1"]}</tspan><tspan x="5.2" y="41">{s["l2"]}</tspan></text>')
    o.append(caps(s['kind'],6,48,2.3,c))
    o.append(f'<text font-family="RR" font-size="2.6" fill="{c}"><tspan x="6" y="52.4">{s["desc"][0]}</tspan><tspan x="6" y="55.8">{s["desc"][1]}</tspan></text>')
    o+= [rule(6,59.5,W-6,59.5,c), logo(11.5,64.6,9,c), caps('500 ML',W-6,65.6,2.4,c,'end')]
    return o
def AC(k):
    s=SKU[k]; c=s['ink']; o=[f'<rect width="{W}" height="{H}" fill="{s["g"]}"/>']
    # arch window with the art, apothecary style
    ax,ay,aw,ah=5,13,28,46
    o.append(f'<clipPath id="arch{k}"><path d="M{ax} {ay+ah}V{ay+aw/2}A{aw/2} {aw/2} 0 0 1 {ax+aw} {ay+aw/2}V{ay+ah}Z"/></clipPath>')
    o.append(f'<g clip-path="url(#arch{k})"><rect x="{ax}" y="{ay}" width="{aw}" height="{ah}" fill="{s["g"]}"/>{art(k,-14,ay+6,80)}</g>')
    o.append(f'<path d="M{ax} {ay+ah}V{ay+aw/2}A{aw/2} {aw/2} 0 0 1 {ax+aw} {ay+aw/2}V{ay+ah}Z" fill="none" stroke="{c}" stroke-width="0.3"/>')
    o+= [caps('THE VANILLA SHOP',5,8.2,2.1,c), caps(s['no'],W-5,8.2,2.1,c,'end'), rule(5,10,W-5,10,c)]
    x0=37
    o.append(f'<text font-family="IS" font-size="10.5" fill="{c}"><tspan x="{x0-0.5}" y="20.5">{s["l1"]}</tspan><tspan x="{x0-0.5}" y="29">{s["l2"]}</tspan></text>')
    o.append(caps(s['kind'],x0,34,2.1,c))
    rows=[('SPECIES','Vanilla planifolia'),('ORIGIN','Sri Lanka'),('BEST FOR',s['use']),('USE',s['dose'])]
    y=38
    for lab,val in rows:
        o.append(rule(x0,y,W-5,y,c,0.18,0.5)); o.append(caps(lab,x0,y+3.1,1.6,c,op=0.75)); o.append(f'<text x="{x0+15}" y="{y+3.2}" font-family="RR" font-size="2.3" fill="{c}">{val}</text>'); y+=4.6
    o.append(rule(x0,y,W-5,y,c,0.18,0.5))
    o+= [rule(5,61.5,W-5,61.5,c), caps('500 ML',5,66.4,2.4,c), logo(W-10,65.2,8,c)]
    o.append(logo((x0+W-5)/2+12,0,0,c) if False else '')
    return o
for k in SKU:
    for nm,fn in (('A',A),('AC',AC)):
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W*20}" height="{H*20}" viewBox="0 0 {W} {H}">'+''.join(fn(k))+'</svg>'
        open(f'{T}/lab-{nm}-{k}.svg','w').write(svg)
        open(f'{T}/lab-{nm}-{k}.html','w').write(f'<html><head><style>{css}html,body{{margin:0}}</style></head><body>{svg}</body></html>')
print('ok')
