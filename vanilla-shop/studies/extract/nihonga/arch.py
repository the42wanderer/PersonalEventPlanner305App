# One wrap label, 226 x 80 mm, with the top edge cut into arches (a tall front arch, lower side arches for the data)
import re, sys
sys.path.insert(0,'.')
from ground import build
R='/home/user/PersonalEventPlanner305App/vanilla-shop'; CF='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/candlefonts'
T='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/ext/n/'
logoD=re.search(r' d="([^"]+)"',open(R+'/brand/vanilla-shop-logo.svg').read()).group(1)
W,H,CX=226,80,113
css=(f"@font-face{{font-family:IS;src:url(file://{R}/fonts/instrument-serif-italic.ttf)}}"
     f"@font-face{{font-family:RW;src:url(file://{CF}/roc-wide-regular.otf)}}@font-face{{font-family:RR;src:url(file://{CF}/roc-regular.otf)}}")
def caps(t,x,y,sz,c,a='middle',tr=0.3,op=1): return f'<text x="{x}" y="{y}" font-family="RW" font-size="{sz}" letter-spacing="{sz*tr:.2f}" fill="{c}" text-anchor="{a}" opacity="{op}">{t}</text>'
def body(t,x,y,sz,c,a='middle'): return f'<text x="{x}" y="{y}" font-family="RR" font-size="{sz}" fill="{c}" text-anchor="{a}">{t}</text>'
def logo(cx,cy,lw,c): s=lw/933; return f'<path d="{logoD}" fill="{c}" fill-rule="evenodd" transform="translate({cx-lw/2:.2f} {cy-963*s/2:.2f}) scale({s:.5f})"/>'
FR=dict(x0=85,x1=141,top=2)          # front arch, r = 28
SA=[(43,83),(143,183)]; ST=24         # side arches, r = 20, crown at y 24
SPRING=44
def outline(i=0):
    r=28-i; rs=20-i; fx0,fx1=FR['x0']+i,FR['x1']-i
    (a0,a1),(b0,b1)=SA
    return (f"M{i} {H-i}V{SPRING+i}H{a0+i}A{rs} {rs} 0 0 1 {a1-i} {SPRING+i}H{fx0}V{FR['top']+28}A{r} {r} 0 0 1 {fx1} {FR['top']+28}"
            f"V{SPRING+i}H{b0+i}A{rs} {rs} 0 0 1 {b1-i} {SPRING+i}H{W-i}V{H-i}Z")
def wrap(name,ground,c,mid,light,s,ml='500 ML'):
    o=[f'<clipPath id="cl"><path d="{outline()}"/></clipPath>',
       f'<g clip-path="url(#cl)"><image href="file://{T}{ground}" width="{W}" height="{H}" preserveAspectRatio="none"/></g>',
       f'<path d="{outline(1.6)}" fill="none" stroke="{mid}" stroke-width="0.25" opacity="0.85"/>',
       logo(CX,12.2,10,c),
       f'<text font-family="IS" font-size="13.5" fill="{c}" text-anchor="middle"><tspan x="{CX}" y="30">{s["l1"]}</tspan><tspan x="{CX}" y="41.6">{s["l2"]}</tspan></text>',
       caps(s['kind'],CX,46.6,2.1,mid,tr=0.32), caps(ml,CX,H-4.2,2.1,light,tr=0.32)]
    # side arches: the formula rows
    for (x0,x1),rows in zip(SA,s['rows']):
        cx=(x0+x1)/2; y=31.5
        for lab_,val in rows:
            o+=[caps(lab_,cx,y,1.55,mid,tr=0.3), body(val,cx,y+3.3,2.3,c)]; y+=7.6
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W*20}" height="{H*20}" viewBox="0 0 {W} {H}">'+''.join(o)+'</svg>'
    open(T+name+'.html','w').write(f'<html><head><style>{css}html,body{{margin:0;background:transparent}}</style></head><body>{svg}</body></html>')
SK={'01':dict(src='v01a.webp',c='#4A120C',mid='#A8361F',light='#F6E2C6',l1='Vanilla',l2='Extract',kind='WITH ALCOHOL',
              rows=[[('SPECIES','Vanilla planifolia'),('ORIGIN','Sri Lanka')],[('BEST FOR','Baking, custards'),('USE','1 tsp per cake')]]),
    '02':dict(src='v02.webp',c='#4A2C08',mid='#8A5A10',light='#F8ECD2',l1='Vanilla',l2='Extract',kind='ALCOHOL-FREE',
              rows=[[('SPECIES','Vanilla planifolia'),('ORIGIN','Sri Lanka')],[('BEST FOR','Desserts, drinks'),('USE','1 tsp per cake')]])}
if __name__=='__main__':
    for k,s in SK.items():
        build(s['src'],T+f'gw-{k}.jpg',Ha=44,W=W,H=H)
        wrap(f'arch-{k}',f'gw-{k}.jpg',s['c'],s['mid'],s['light'],s)
        for ml in ('100','200'): wrap(f'arch-{k}-{ml}',f'gw-{k}.jpg',s['c'],s['mid'],s['light'],s,ml+' ML')
    print('ok')
