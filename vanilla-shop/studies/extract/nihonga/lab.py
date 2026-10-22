import re, sys
R='/home/user/PersonalEventPlanner305App/vanilla-shop'; CF='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/candlefonts'
T='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/ext/n/'
logoD=re.search(r' d="([^"]+)"',open(R+'/brand/vanilla-shop-logo.svg').read()).group(1)
W,H,CX=120,70,60
css=(f"@font-face{{font-family:IS;src:url(file://{R}/fonts/instrument-serif-italic.ttf)}}"
     f"@font-face{{font-family:RW;src:url(file://{CF}/roc-wide-regular.otf)}}")
def caps(t,x,y,sz,c,a='middle',tr=0.3): return f'<text x="{x}" y="{y}" font-family="RW" font-size="{sz}" letter-spacing="{sz*tr:.2f}" fill="{c}" text-anchor="{a}">{t}</text>'
def rule(x1,y1,x2,y2,c,w=0.22,op=0.7): return f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{c}" stroke-width="{w}" opacity="{op}"/>'
def logo(cx,cy,lw,c): s=lw/933; return f'<path d="{logoD}" fill="{c}" fill-rule="evenodd" transform="translate({cx-lw/2:.2f} {cy-963*s/2:.2f}) scale({s:.5f})"/>'
def page(name,ground,c,acc,l1,l2,kind,ml='500 ML'):
    o=[f'<image href="file://{T}{ground}" width="{W}" height="{H}" preserveAspectRatio="none"/>',
       logo(CX,9.6,9.5,c), rule(CX-31,10.4,CX-8,10.4,c), rule(CX+8,10.4,CX+31,10.4,c),
       caps('CEYLON',CX-31,8.7,2.05,c,'start'), caps(ml,CX+31,8.7,2.05,c,'end'),
       f'<text font-family="IS" font-size="13.5" fill="{c}" text-anchor="middle"><tspan x="{CX}" y="24.2">{l1}</tspan><tspan x="{CX}" y="36">{l2}</tspan></text>',
       caps(kind,CX,41.2,2.15,acc,tr=0.32)]
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W*20}" height="{H*20}" viewBox="0 0 {W} {H}">'+''.join(o)+'</svg>'
    open(T+name+'.html','w').write(f'<html><head><style>{css}html,body{{margin:0}}</style></head><body>{svg}</body></html>')
def neck(name,g,t,txt):
    w,h=78,13
    o=[f'<rect width="{w}" height="{h}" fill="{g}"/>',rule(0,1.4,w,1.4,t,0.2,0.6),rule(0,h-1.4,w,h-1.4,t,0.2,0.6),
       f'<text x="{w/2}" y="{h/2+2.1}" font-family="IS" font-size="6.4" fill="{t}" text-anchor="middle">{txt}</text>',
       caps('PURE CEYLON VANILLA',w/2-21,h/2+0.75,1.9,t,'end'),caps('PURE CEYLON VANILLA',w/2+21,h/2+0.75,1.9,t,'start')]
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w*20}" height="{h*20}" viewBox="0 0 {w} {h}">'+''.join(o)+'</svg>'
    open(T+name+'.html','w').write(f'<html><head><style>{css}html,body{{margin:0}}</style></head><body>{svg}</body></html>')
for v in ('a','b'):
    page(f'lab-01{v}',f'g-01{v}.jpg','#4A120C','#A8361F','Vanilla','Extract','WITH ALCOHOL')
    page(f'lab-01{v}-100',f'g-01{v}.jpg','#4A120C','#A8361F','Vanilla','Extract','WITH ALCOHOL','100 ML')
    page(f'lab-01{v}-200',f'g-01{v}.jpg','#4A120C','#A8361F','Vanilla','Extract','WITH ALCOHOL','200 ML')
neck('neck-01','#B83A24','#F6E8D4','No. 01')
