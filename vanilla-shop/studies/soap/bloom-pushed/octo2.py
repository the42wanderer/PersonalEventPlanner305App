# Bloom, pushed three ways, on the real box: a wrapped bar with the corners folded in (an octagon, ~9 mm chamfers).
import math
R='/home/user/PersonalEventPlanner305App/vanilla-shop'; S='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad'
O=S+'/soap/b2/'
FONT={'IS':R+'/fonts/instrument-serif-italic.ttf','G':R+'/fonts/geist-regular.ttf','AE':R+'/fonts/archivo-expanded-regular.ttf','IV':S+'/candlefonts/ivy.otf'}
CSS=''.join(f"@font-face{{font-family:{k};src:url(file://{v})}}" for k,v in FONT.items())
LOGO=__import__('re').search(r' d="([^"]+)"',open(R+'/brand/vanilla-shop-logo.svg').read()).group(1)
W,H,D,C=136,81,28,9.0
SOAPS={'vanilla':dict(small=None,big='Vanilla',kind='BATHING BAR',dk='#4A2C08',bgB='#D99327'),
       'rosette':dict(small='Vanilla &',big='Rosette',kind='VANILLA & ROSE BATHING BAR',dk='#5A1426',bgB='#CF5A76'),
       'ebony':dict(small='Ebony &',big='Amber',kind='CHARCOAL & VANILLA BATHING BAR',dk='#1F1B19',bgB='#1F1B19'),
       'aloe':dict(small='Vanilla &',big='Aloe Vera',kind='VANILLA & ALOE BATHING BAR',dk='#16301C',bgB='#3F7A47')}
ORDER=['vanilla','rosette','ebony','aloe']
FOIL=('<linearGradient id="foil" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8A6424"/><stop offset="0.3" stop-color="#F6DE97"/>'
      '<stop offset="0.5" stop-color="#B98B3A"/><stop offset="0.72" stop-color="#FFF0BE"/><stop offset="1" stop-color="#93692A"/></linearGradient>')
def T(x,y,s,t,f='G',c='#000',a='start',tr=0): return f'<text x="{x}" y="{y}" font-family="{f}" font-size="{s}" fill="{c}" text-anchor="{a}" letter-spacing="{tr}">{t}</text>'
def logo(cx,cy,lw,c): s=lw/933; return f'<path d="{LOGO}" fill="{c}" fill-rule="evenodd" transform="translate({cx-lw/2:.2f} {cy-963*s/2:.2f}) scale({s:.5f})"/>'
def octa(inset=0):
    c=C+inset*0.4; x0,y0,x1,y1=inset,inset,W-inset,H-inset
    return f'M{x0+c} {y0}H{x1-c}L{x1} {y0+c}V{y1-c}L{x1-c} {y1}H{x0+c}L{x0} {y1-c}V{y0+c}Z'
HERO={'vanilla':('VANILLA','#FFE7B8','BATHING BAR'),'rosette':('ROSETTE','#FFD6E0','VANILLA & ROSE BATHING BAR'),
      'ebony':('AMBER','#F0BE72','EBONY & AMBER · CHARCOAL & VANILLA'),'aloe':('ALOE','#DCEFC6','VANILLA & ALOE VERA BATHING BAR')}
from PIL import ImageFont
_iv=ImageFont.truetype(FONT['IV'],1000)
def front_candle(k):
    s=SOAPS[k]; word,tint,line=HERO[k]; art=f'file://{O}D-{k}.png'
    wpe=_iv.getlength(word)/1000-0.012*(len(word)-1)     # width per unit size, with the candles' tight tracking
    size=min(112/wpe,29)
    body=(f'<image href="{art}" x="-7" y="-7" width="150" height="95" preserveAspectRatio="none"/>'
          + T(12,10.5,1.75,'THE VANILLA SHOP','AE',tint,tr=0.55)+T(W-12,10.5,1.75,'100 G','AE',tint,'end',0.55)
          + f'<path d="M12 12.6H{W-12}" stroke="{tint}" stroke-width="0.15" opacity="0.7"/>'
          + T(W/2,H-12.5,size,word,'IV',tint,'middle',-0.012*size)
          + f'<path d="M12 {H-9.4}H{W-12}" stroke="{tint}" stroke-width="0.15" opacity="0.7"/>'
          + T(12,H-6,1.7,line,'AE',tint,tr=0.5)+T(W-12,H-6,1.7,'100% NATURAL','AE',tint,'end',0.5)
          + logo(W/2,30,0,tint)[:0])
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%"><defs>{FOIL}<clipPath id="oc"><path d="{octa()}"/></clipPath></defs>'
            f'<g clip-path="url(#oc)">{body}</g></svg>')
def front(opt,k):
    if opt=='D': return front_candle(k)
    s=SOAPS[k]; art=f'file://{O}{opt}-{k}.png'
    body=f'<image href="{art}" x="-7" y="-7" width="150" height="95" preserveAspectRatio="none"/>'
    if opt=='A':     # cream bloom, everything that matters in gold foil
        ink=s['dk']; sub=s['dk']
        body+=f'<path d="{octa(3.2)}" fill="none" stroke="url(#foil)" stroke-width="0.55"/><path d="{octa(4.4)}" fill="none" stroke="url(#foil)" stroke-width="0.2"/>'
    elif opt=='B':   # bloom on the soap's own colour
        ink='#FFF4DE'; sub='#FFF4DE'
    else:            # the flower so close it becomes the whole box
        ink=s['dk']; sub=s['dk']
    lg='url(#foil)' if opt in 'AB' else s['dk']
    x=12; ny=48 if s['small'] else 44
    if opt=='C':
        body+=logo(19,15,10,lg)+(T(x,58,5.5,s['small'],'IS',ink) if s['small'] else '')+T(x,69 if s['small'] else 66,13,s['big'],'IS',ink)+T(x+0.5,74.2,1.7,s['kind'],'AE',sub,tr=0.45)
    else:
        body+=logo(20,16,11,lg)
        if s['small']: body+=T(x+0.5,ny-15.5,6.5,s['small'],'IS',ink)
        body+=T(x,ny,17 if len(s['big'])<8 else 13.5,s['big'],'IS',ink)+T(x+0.6,ny+6.4,1.9,s['kind'],'AE',sub if opt=='A' else ink,tr=0.5)
        body+=T(x+0.6,H-11,1.8,'100% natural · made exclusively with our own farmed vanilla','G',sub)+T(W-12,H-10.6,4.4,'100 g','IS',sub,'end')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%"><defs>{FOIL}<clipPath id="oc"><path d="{octa()}"/></clipPath></defs>'
            f'<g clip-path="url(#oc)">{body}</g></svg>')
def wallcol(opt,k): return SOAPS[k]['bgB'] if opt in 'BD' else '#F1E6CF'
def box(opt,k,s=3.0,ry=-24,rx=-14):
    pts=[(C,0),(W-C,0),(W,C),(W,H-C),(W-C,H),(C,H),(0,H-C),(0,C)]
    pts=[(x-W/2,y-H/2) for x,y in pts]
    faces=''
    shade=[0.0,0.06,0.16,0.22,0.3,0.3,0.22,0.06]
    for i in range(8):
        (px,py),(qx,qy)=pts[i],pts[(i+1)%8]; L=math.hypot(qx-px,qy-py); a=math.degrees(math.atan2(qy-py,qx-px))
        mx,my=(px+qx)/2*s,(py+qy)/2*s; col=wallcol(opt,k); dk=SOAPS[k]['dk'] if opt not in 'BD' else '#FFF4DE'
        txt=(f'<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font:{1.9*s}px AE;letter-spacing:{0.5*s}px;color:{dk};opacity:.8">THE VANILLA SHOP · {SOAPS[k]["kind"]}</div>' if i==0 else '')
        faces+=(f'<div style="position:absolute;left:{-L*s/2}px;top:{-D*s/2}px;width:{L*s}px;height:{D*s}px;background:{col};'
                f'transform:translate3d({mx}px,{my}px,0) rotateZ({a}deg) rotateX(-90deg)">{txt}<div style="position:absolute;inset:0;background:rgba(0,0,0,{shade[i]})"></div></div>')
    fr=(f'<div style="position:absolute;left:{-W*s/2}px;top:{-H*s/2}px;width:{W*s}px;height:{H*s}px;transform:translateZ({D*s/2}px)">{front(opt,k)}</div>')
    return f'<div style="position:relative;transform-style:preserve-3d;transform:rotateX({rx}deg) rotateY({ry}deg)">{faces}{fr}</div>'
def board(name,title,blurb,opt,bg):
    sc=''.join(f'<div style="position:absolute;left:{250+i*430}px;top:{560-(i%2)*30}px;transform-style:preserve-3d">{box(opt,k)}</div>' for i,k in enumerate(ORDER))
    big=f'<div style="position:absolute;left:1360px;top:250px;transform-style:preserve-3d">{""}</div>'
    html=(f'<html><head><style>{CSS}html,body{{margin:0}}.b{{position:relative;width:1800px;height:900px;background:{bg};overflow:hidden;perspective:2600px}}'
          f'.h{{position:absolute;left:60px;top:44px;font:52px IS;color:#2A2017}}.p{{position:absolute;left:62px;top:112px;width:1500px;font:21px/1.45 G;color:#4A4036}}</style></head>'
          f'<body><div class="b"><div class="h">{title}</div><div class="p">{blurb}</div>{sc}</div></body></html>')
    open(O+name+'.html','w').write(html)
board('D-candle-type','B · Bloom on colour, with the candles\' type',
      'The soap\'s name set like the candles: one word in Ivy Presto Bold capitals, tightly spaced, as wide as the box, in a light tint of its colour. '
      'The flower glows above it; hairline rules and small spaced capitals frame it, as on the candle boxes.','D','#E9E3D8')
html=open(O+'D-candle-type.html').read()
hero=''.join(f'<div style="position:absolute;left:{560+i*700}px;top:470px;transform-style:preserve-3d">{box("D",k,s=4.6,ry=-20,rx=-12)}</div>' for i,k in enumerate(['vanilla','ebony']))
a=html.index('<div class="h">'); b=html.index('</div></body>')
open(O+'D-closeup.html','w').write(html[:a]+hero+html[b:].replace('</div></body>','</div></body>',1))
print('ok')
