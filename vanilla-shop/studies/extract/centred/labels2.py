# centred extract labels: front panel centred in a 120 x 70 mm strip (what shows round a 500 ml flask)
import re, sys
R='/home/user/PersonalEventPlanner305App/vanilla-shop'; CF='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/candlefonts'
T='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/ext/c/'
logoD=re.search(r' d="([^"]+)"',open(R+'/brand/vanilla-shop-logo.svg').read()).group(1)
W,H,CX=120,70,60
SKU={'alc':dict(no='No. 01',l1='Vanilla',l2='Extract',kind='WITH ALCOHOL'),
     'free':dict(no='No. 02',l1='Vanilla',l2='Extract',kind='ALCOHOL-FREE'),
     'syrup':dict(no='No. 03',l1='Vanilla',l2='Syrup',kind='NATURAL SYRUP')}
BOLD={'alc':('#B83A24','#F6E2C6'),'free':('#DFA23A','#3B2108'),'syrup':('#21402A','#E7EFCF')}
NECK={'tea':BOLD,'neck':BOLD,'pod':BOLD,'tone':{'alc':('#B4432C','#F6E8D4'),'free':('#B07818','#F8ECD2'),'syrup':('#4F7448','#EEF1DC')}}
NTXT={'alc':'PURE CEYLON VANILLA','free':'PURE CEYLON VANILLA','syrup':'MADE WITH CEYLON VANILLA'}
DIR={ # ground, art, ink, accent
 'tea':  lambda k:(f'g-tea-{k}.jpg','art-cluster.png','#143A1D',{'alc':'#9C3B25','free':'#94600F','syrup':'#3C6634'}[k]),
 'tone': lambda k:('g-cream.jpg',f'art-cluster-{k}.png',{'alc':'#5A1A10','free':'#5E3A0C','syrup':'#16301C'}[k],{'alc':'#B4432C','free':'#B07818','syrup':'#4F7448'}[k]),
 'neck': lambda k:('g-cream.jpg','art-cluster.png','#143A1D',{'alc':'#A8361F','free':'#9A6210','syrup':'#2F5A33'}[k]),
 'pod':  lambda k:('g-pod.jpg','art-cluster.png','#F3E6CC',{'alc':'#E9896A','free':'#E9B44C','syrup':'#AFC98F'}[k]),
}
css=(f"@font-face{{font-family:IS;src:url(file://{R}/fonts/instrument-serif-italic.ttf)}}"
     f"@font-face{{font-family:RW;src:url(file://{CF}/roc-wide-regular.otf)}}@font-face{{font-family:RR;src:url(file://{CF}/roc-regular.otf)}}")
def caps(t,x,y,sz,c,a='middle',tr=0.3,op=1): return f'<text x="{x}" y="{y}" font-family="RW" font-size="{sz}" letter-spacing="{sz*tr:.2f}" fill="{c}" text-anchor="{a}" opacity="{op}">{t}</text>'
def rule(x1,y1,x2,y2,c,w=0.22,op=0.7): return f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{c}" stroke-width="{w}" opacity="{op}"/>'
def logo(cx,cy,lw,c): s=lw/933; return f'<path d="{logoD}" fill="{c}" fill-rule="evenodd" transform="translate({cx-lw/2:.2f} {cy-963*s/2:.2f}) scale({s:.5f})"/>'
def img(f,x,y,w,h): return f'<image href="file://{T}{f}" x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="none"/>'
def front(d,k,ml='500 ML'):
    g,a,c,acc=DIR[d](k); s=SKU[k]; o=[img(g,0,0,W,H)]
    # header: logo centred between two rules
    o+=[logo(CX,9.6,9.5,c), rule(CX-31,10.4,CX-8,10.4,c), rule(CX+8,10.4,CX+31,10.4,c),
        caps('CEYLON',CX-31,8.7,2.05,c,'start'), caps(ml,CX+31,8.7,2.05,c,'end')]
    o.append(f'<text font-family="IS" font-size="14.5" fill="{c}" text-anchor="middle"><tspan x="{CX}" y="27.6">{s["l1"]}</tspan><tspan x="{CX}" y="40.4">{s["l2"]}</tspan></text>')
    o.append(caps(s['kind'],CX,46,2.15,acc,tr=0.32))
    aw=36; ah=aw*650/890; o.append(img(a,CX-aw/2,49.2,aw,ah))
    if d=='neck': o+=[f'<rect width="{W}" height="2.2" fill="{BOLD[k][0]}"/>',f'<rect y="{H-2.2}" width="{W}" height="2.2" fill="{BOLD[k][0]}"/>']
    return o
for d in DIR:
    for k in SKU:
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W*20}" height="{H*20}" viewBox="0 0 {W} {H}">'+''.join(front(d,k))+'</svg>'
        open(f'{T}lab-{d}-{k}.html','w').write(f'<html><head><style>{css}html,body{{margin:0}}</style></head><body>{svg}</body></html>')
        for ml in ('100','200'):
            svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W*20}" height="{H*20}" viewBox="0 0 {W} {H}">'+''.join(front(d,k,ml+' ML'))+'</svg>'
            open(f'{T}lab-{d}-{k}-{ml}.html','w').write(f'<html><head><style>{css}html,body{{margin:0}}</style></head><body>{svg}</body></html>')
def neck(d,k):
    g,t=NECK[d][k]; w,h=78,13
    o=[f'<rect width="{w}" height="{h}" fill="{g}"/>',rule(0,1.4,w,1.4,t,0.2,0.6),rule(0,h-1.4,w,h-1.4,t,0.2,0.6),f'<text x="{w/2}" y="{h/2+2.1}" font-family="IS" font-size="6.4" fill="{t}" text-anchor="middle">{SKU[k]["no"]}</text>',
       caps(NTXT[k],w/2-21,h/2+0.75,1.9,t,'end',0.3),caps(NTXT[k],w/2+21,h/2+0.75,1.9,t,'start',0.3)]
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w*20}" height="{h*20}" viewBox="0 0 {w} {h}">'+''.join(o)+'</svg>'
    open(f'{T}neck-{d}-{k}.html','w').write(f'<html><head><style>{css}html,body{{margin:0}}</style></head><body>{svg}</body></html>')
for d in DIR:
    for k in SKU: neck(d,k)
print('ok')
