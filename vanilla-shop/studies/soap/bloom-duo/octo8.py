# Bloom, pushed three ways, on the real box: a wrapped bar with the corners folded in (an octagon, ~9 mm chamfers).
import math
R='/home/user/PersonalEventPlanner305App/vanilla-shop'; S='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad'
O=S+'/soap/b2/'
FONT={'IS':R+'/fonts/instrument-serif-italic.ttf','G':R+'/fonts/geist-regular.ttf','AE':R+'/fonts/archivo-expanded-regular.ttf','ISR':R+'/fonts/instrument-serif.ttf','IV':S+'/candlefonts/ivy.otf','AL':R+'/fonts/archivo-expanded-light.ttf'}
CSS=''.join(f"@font-face{{font-family:{k};src:url(file://{v})}}" for k,v in FONT.items())
LOGO=__import__('re').search(r' d="([^"]+)"',open(R+'/brand/vanilla-shop-logo.svg').read()).group(1)
W,H,D,C=136,81,28,9.0
SOAPS={'vanilla':dict(small=None,big='Vanilla',kind='BATHING BAR',dk='#4A2C08',bgB='#D99327'),
       'rosette':dict(small='Vanilla &',big='Rosette',kind='VANILLA & ROSE BATHING BAR',dk='#5A1426',bgB='#CF5A76'),
       'ebony':dict(small='Ebony &',big='Amber',kind='CHARCOAL & VANILLA BATHING BAR',dk='#1F1B19',bgB='#1F1B19'),
       'aloe':dict(small='Vanilla &',big='Aloe Vera',kind='VANILLA & ALOE BATHING BAR',dk='#16301C',bgB='#3F7A47')}
ORDER=['vanilla','rosette','ebony','aloe']
FOIL2=('<linearGradient id="foil2" x1="0" y1="0" x2="1" y2="0.35"><stop offset="0" stop-color="#4E300A"/><stop offset="0.28" stop-color="#8E6420"/>'
       '<stop offset="0.46" stop-color="#C9A55A"/><stop offset="0.6" stop-color="#76521A"/><stop offset="0.85" stop-color="#A37A30"/><stop offset="1" stop-color="#4E300A"/></linearGradient>')
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
DEEP={'vanilla':'#A2650F','rosette':'#A3304C','ebony':'#2A2422','aloe':'#2E6636'}
WORDS={'vanilla':('VANILLA','BATHING BAR'),'rosette':('ROSETTE','VANILLA & ROSE BATHING BAR'),
       'ebony':('AMBER','EBONY & AMBER · CHARCOAL & VANILLA'),'aloe':('ALOE','VANILLA & ALOE VERA BATHING BAR')}
ML,MR=12.0,W-12.0; TRK=-0.012
def ink_w(word,size):
    b=_iv.getbbox(word); return (b[2]-b[0])/1000*size+TRK*size*(len(word)-1), b[0]/1000*size
# one size for the whole range: the widest word fills the measure exactly
SIZE=min((MR-ML)/ink_w(w,1)[0] for w,_ in WORDS.values())
def front_grid(scheme,k):
    word,line=WORDS[k]
    if scheme=='G': art=f'D-{k}'; hero=HERO[k][1]; small=HERO[k][1]; rule=HERO[k][1]
    else: art=f'L-{k}'; hero=DEEP[k]; small=SOAPS[k]['dk']; rule=SOAPS[k]['dk']
    _,lsb=ink_w(word,SIZE); base=61.5
    body=(f'<image href="file://{O}{art}.png" x="-7" y="-7" width="150" height="95" preserveAspectRatio="none"/>'
          + T(ML,11.6,1.7,'THE VANILLA SHOP','AE',small,tr=0.6)
          + T(ML-lsb,base,SIZE,word,'IV',hero,'start',TRK*SIZE)
          + f'<path d="M{ML} 66.4H{MR}" stroke="{rule}" stroke-width="0.18" opacity="0.6"/>'
          + T(ML,71.6,1.7,line,'AE',small,tr=0.6) + T(MR,71.6,1.7,'100% NATURAL  ·  100 G','AE',small,'end',0.6))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%"><defs><clipPath id="oc"><path d="{octa()}"/></clipPath></defs>'
            f'<g clip-path="url(#oc)">{body}</g></svg>')
INKM={'vanilla':'#5A3412','rosette':'#6A1A30','ebony':'#E6B060','aloe':'#1E3F24'}
def front_marble(k,calm):
    word,line=WORDS[k]; ink=INKM[k]; _,lsb=ink_w(word,SIZE); base=64
    art='MC' if calm else 'M'
    body=(f'<image href="file://{O}{art}-{k}.png" x="-7" y="-7" width="150" height="95" preserveAspectRatio="none"/>'
          + T(ML-lsb,base,SIZE,word,'IV',ink,'start',TRK*SIZE)
          + f'<path d="M{ML} 68.2H{MR}" stroke="{ink}" stroke-width="0.25" opacity="0.8"/>'
          + T(ML,73.2,2.5,line,'AE',ink,tr=0.35) + T(MR,73.2,2.5,'100 G','AE',ink,'end',0.35)
          + T(ML,13.2,2.5,'THE VANILLA SHOP','AE',ink,tr=0.35) + T(MR,13.2,2.5,'100% NATURAL','AE',ink,'end',0.35))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%"><defs><clipPath id="oc"><path d="{octa()}"/></clipPath></defs>'
            f'<g clip-path="url(#oc)">{body}</g></svg>')
INFO={'vanilla':['VANILLA','BATHING','BAR'],'rosette':['VANILLA &','ROSE','BATHING BAR'],
      'ebony':['CHARCOAL &','VANILLA','BATHING BAR'],'aloe':['VANILLA &','ALOE VERA','BATHING BAR']}
def front_candle_layout(k):
    word,_=WORDS[k]; ink=INKM[k]; R0,R1=12,86          # the text block: left 12 mm to 78 mm, like the candle panel
    cs,lead=2.15,3.45                                  # small caps (light), leading
    caps=lambda t,x,y,a='start',op=1: f'<text x="{x}" y="{y}" font-family="AL" font-size="{cs}" fill="{ink}" text-anchor="{a}" letter-spacing="{cs*0.16:.3f}" opacity="{op}">{t}</text>'
    rule=lambda y: f'<path d="M{R0} {y}H{R1}" stroke="{ink}" stroke-width="0.16" opacity="0.55"/>'
    hs=27.6; _,lsb=ink_w(word,hs)
    b=[f'<image href="file://{O}MR-{k}.png" x="-7" y="-7" width="150" height="95" preserveAspectRatio="none"/>',
       caps('THE VANILLA SHOP',R0,13.4), caps('SRI LANKA',R1,13.4,'end'), rule(16.2),
       ]
    _al=ImageFont.truetype(FONT['AL'],1000)
    cw=lambda t: _al.getlength(t)/1000*cs+cs*0.16*(len(t)-1)
    c1=('MADE WITH',['OUR OWN','FARMED','VANILLA']); c2=('NET WT.',['100 G','100%','NATURAL']); c3=INFO[k]
    w1=max(cw(t) for t in [c1[0]]+c1[1]); w2=max(cw(t) for t in [c2[0]]+c2[1]); w3=max(cw(t) for t in c3)
    gap=(R1-R0-w1-w2-w3)/2; x2=R0+w1+gap
    b+=[caps(c1[0],R0,22.6,op=0.62)]+[caps(t,R0,22.6+(i+1)*lead) for i,t in enumerate(c1[1])]
    b+=[caps(c2[0],x2,22.6,op=0.62)]+[caps(t,x2,22.6+(i+1)*lead) for i,t in enumerate(c2[1])]
    b+=[caps(t,R1,22.6+(i+1)*lead,'end') for i,t in enumerate(c3)]
    b+=[rule(37.2), T(R0-lsb,65.2,hs,word,'IV',ink,'start',TRK*hs), rule(70.4)]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%"><defs><clipPath id="oc"><path d="{octa()}"/></clipPath></defs>'
            f'<g clip-path="url(#oc)">{"".join(b)}</g></svg>')
BAND={'vanilla':('No. 01','VANILLA','Pure vanilla','#4A2A0C'),'rosette':('No. 02','ROSETTE','Vanilla & rose','#561327'),
      'ebony':('No. 03','AMBER','Charcoal & vanilla','#1C1715'),'aloe':('No. 04','ALOE','Vanilla & aloe vera','#173A1F')}
def front_band(k):
    no,word,desc,ink=BAND[k]; x0,x1=21,65; cx=(x0+x1)/2; cs=2.05
    _al=ImageFont.truetype(FONT['AL'],1000)
    caps=lambda t,y,sz=cs,op=1: f'<text x="{cx}" y="{y}" font-family="AL" font-size="{sz}" fill="{ink}" text-anchor="middle" letter-spacing="{sz*0.18:.3f}" opacity="{op}">{t}</text>'
    hs=7.6; ws=_iv.getlength(word)/1000*hs
    b=[f'<image href="file://{O}W-{k}.png" x="-7" y="-7" width="150" height="95" preserveAspectRatio="none"/>',
       f'<rect x="{x0}" y="-7" width="{x1-x0}" height="95" fill="#F8F0DF"/>',
       f'<rect x="{x0}" y="-7" width="{x1-x0}" height="95" fill="url(#gr)" opacity="0.5"/>',
       f'<path d="M{x0+1.6} -7V88M{x1-1.6} -7V88" stroke="url(#foil)" stroke-width="0.35"/>',
       logo(cx,15.5,12.5,ink),
       caps(no,27.2,op=0.75),
       f'<path d="M{cx-5} 30H{cx+5}" stroke="{ink}" stroke-width="0.18" opacity="0.6"/>',
       T(cx,42.5,hs,word,'IV',ink,'middle',-0.01*hs),
       f'<text x="{cx}" y="48.6" font-family="IS" font-size="3.6" fill="{ink}" text-anchor="middle">{desc}</text>',
       f'<path d="M{cx-5} 53H{cx+5}" stroke="{ink}" stroke-width="0.18" opacity="0.6"/>',
       caps('BATHING BAR',58.6), caps('MADE WITH OUR OWN',62.4,op=0.75), caps('FARMED VANILLA',65.4,op=0.75),
       caps('100% NATURAL  ·  100 G',72.2,op=0.75)]
    defs=FOIL+'<filter id="gn"><feTurbulence type="fractalNoise" baseFrequency="2.2" numOctaves="2" seed="3"/><feColorMatrix values="0 0 0 0 0.4 0 0 0 0 0.3 0 0 0 0 0.2 0 0 0 0.18 0"/></filter><pattern id="gr" width="20" height="20" patternUnits="userSpaceOnUse"><rect width="20" height="20" filter="url(#gn)"/></pattern>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%"><defs>{defs}<clipPath id="oc"><path d="{octa()}"/></clipPath></defs>'
            f'<g clip-path="url(#oc)">{"".join(b)}</g></svg>')
PG={'vanilla':'#5E3E22','rosette':'#6E3540','ebony':'#2D2A28','aloe':'#47563F'}
PNAME={'vanilla':('VANILLA','Pure vanilla bathing bar'),'rosette':('ROSETTE','Vanilla & rose bathing bar'),
       'ebony':('EBONY & AMBER','Charcoal & vanilla bathing bar'),'aloe':('ALOE VERA','Vanilla & aloe vera bathing bar')}
def front_premium(k):
    name,desc=PNAME[k]; cream='#F3E6CC'; x=12
    hs=8.6; lsb=_iv.getbbox(name)[0]/1000*hs
    b=[f'<image href="file://{O}PR-{k}.png" x="-7" y="-7" width="150" height="95" preserveAspectRatio="none"/>',
       logo(x+6.4,15,12.8,'url(#foil)'),
       T(x-lsb,36,hs,name,'IV','url(#foil)','start',-0.008*hs),
       f'<text x="{x}" y="42.4" font-family="IS" font-size="4.1" fill="{cream}">{desc}</text>',
       f'<text x="{x}" y="50.6" font-family="AL" font-size="2.15" fill="{cream}" letter-spacing="0.4" opacity="0.8">MADE WITH OUR OWN</text>',
       f'<text x="{x}" y="53.9" font-family="AL" font-size="2.15" fill="{cream}" letter-spacing="0.4" opacity="0.8">FARMED VANILLA</text>',
       f'<text x="{x}" y="72.8" font-family="IS" font-size="5" fill="url(#foil)">100 g</text>']
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%"><defs>{FOIL}<clipPath id="oc"><path d="{octa()}"/></clipPath></defs>'
            f'<g clip-path="url(#oc)">{"".join(b)}</g></svg>')
EC={'vanilla':('#F1E7D3','#7A4E1E'),'rosette':('#D3A0A4','#FBF1EA'),'ebony':('#E3DDD3','#2E2A27'),'aloe':('#7E9B73','#F6F2E4')}
EN={'vanilla':('Pure','Vanilla'),'rosette':('Vanilla &','Rose'),'ebony':('Ebony &','Amber'),'aloe':('Vanilla &','Aloe Vera')}
ES={'vanilla':'Bathing bar','rosette':'Vanilla & rose bathing bar','ebony':'Charcoal & vanilla bathing bar','aloe':'Vanilla & aloe vera bathing bar'}
DK={'vanilla':'#5A3410','rosette':'#5A1426','ebony':'#141414','aloe':'#16301C'}
DG={'vanilla':'#F7EFDC','rosette':'#F8EDE6','ebony':'#E4E2DE','aloe':'#F2F1E2'}
def front_engr(k,art=None):
    g,ink=EC[k]; l1,l2=EN[k]; x=12
    if art: g,ink=DG[k],DK[k]
    cap=lambda t,y,op=1: f'<text x="{x}" y="{y}" font-family="AL" font-size="2.2" fill="{ink}" letter-spacing="0.42" opacity="{op}">{t}</text>'
    b=[f'<image href="file://{art or O+'E-'+k+'.png'}" x="-7" y="-7" width="150" height="95" preserveAspectRatio="none"/>',
       f'<text x="{x-0.4}" y="24" font-family="ISR" font-size="12.5" fill="{ink}">{l1}</text>',
       f'<text x="{x-0.4}" y="35.5" font-family="IS" font-size="12.5" fill="{ink}">{l2}</text>',
       logo(x+4.6,52,9.2,ink),
       cap('THE VANILLA SHOP',61.2),
       f'<text x="{x}" y="65.6" font-family="IS" font-size="3.4" fill="{ink}">{ES[k]}</text>',
       cap('MADE WITH OUR OWN',69.6,0.8), cap('FARMED VANILLA',72.6,0.8), cap('NET WT. 100 G',75.6,0.8)]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%"><defs><clipPath id="oc"><path d="{octa()}"/></clipPath></defs>'
            f'<g clip-path="url(#oc)">{"".join(b)}</g></svg>')
FN={'vanilla':('Vanilla','Bathing Bar'),'rosette':('Vanilla &','Rosette'),'ebony':('Vanilla &','Charcoal+'),'aloe':('Vanilla &','Aloe Vera')}
FD={'vanilla':'','rosette':'Vanilla & rose bathing bar','ebony':'Charcoal & vanilla bathing bar','aloe':'Vanilla & aloe vera bathing bar'}
def front_bloom(k,art=None):
    # Type sized to a hierarchy you can read at arm's length on a shelf: name ~60 pt, logo 18 mm, descriptor ~13 pt,
    # small caps ~6.5 pt, net weight ~12.5 pt (digits ~3.2 mm, the usual minimum for a front panel of this size).
    g,ink=DG[k],DK[k]; l1,l2=FN[k]; x=12
    art=art or f'D-{k}.png'
    b=[f'<image href="file:///tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/soap/b3/{art}" x="-7" y="-7" width="150" height="95" preserveAspectRatio="none"/>',
       logo(x+9,16,18,ink),
       f'<text x="{x-0.8}" y="44" font-family="ISR" font-size="21" fill="url(#foil2)">Vanilla<tspan fill="{ink}">{l1[7:]}</tspan></text>',
       f'<text x="{x-0.8}" y="61" font-family="IS" font-size="21" fill="{ink}">{l2.rstrip("+")}'+('<tspan font-family="ISR" font-size="11" dx="0.8" dy="-8.5">+</tspan>' if l2.endswith('+') else '')+'</text>',
       (f'<text x="{x}" y="67.8" font-family="IS" font-size="5.2" fill="{ink}">{FD[k]}</text>' if k!='vanilla' else ''),
       f'<text x="{x}" y="72.9" font-family="AE" font-size="2.3" fill="{ink}" letter-spacing="0.3">100% NATURAL · PRODUCT OF SRI LANKA</text>',
       f'<text x="{x}" y="77.6" font-family="IS" font-size="4.1" fill="{ink}">Made with vanilla grown on our own farms.</text>',
       f'<text x="124" y="77.6" font-family="AE" font-size="4.4" fill="{ink}" text-anchor="end">NET WT. 100 g</text>']
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%"><defs>{FOIL2}<clipPath id="oc"><path d="{octa()}"/></clipPath></defs>'
            f'<g clip-path="url(#oc)">{"".join(b)}</g></svg>')
def front(opt,k):
    if opt=='E': return front_engr(k)
    if opt=='F': return front_bloom(k)
    if opt in ('F1','F2','F3','F4','F5'): return front_bloom('ebony','D-ebony-'+opt[1]+'.png')
    if opt=='F0': return front_engr(k,'/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/soap/b3/D-'+k+'.png')
    if opt=='R': return front_premium(k)
    if opt=='Q': return front_band(k)
    if opt=='P': return front_candle_layout(k)
    if opt in 'MN': return front_marble(k,opt=='N')
    if opt in 'GL': return front_grid(opt,k)
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
WALLM2={'vanilla':'#F1DDB5','rosette':'#F2D3D9','ebony':'#E8E1D6','aloe':'#DAE8C7'}
WALLM={'vanilla':'#E8B65E','rosette':'#E58BA0','ebony':'#2A2522','aloe':'#86B98A'}
def wallcol(opt,k):
    if opt=='E': return EC[k][0]
    if opt=='F': return DG[k]
    if opt=='R': return PG[k]
    if opt=='Q': return WALLM2[k]
    return WALLM[k] if opt in 'MNP' else (SOAPS[k]['bgB'] if opt in 'BDG' else '#F1E6CF')
def box(opt,k,s=3.0,ry=-24,rx=-14):
    pts=[(C,0),(W-C,0),(W,C),(W,H-C),(W-C,H),(C,H),(0,H-C),(0,C)]
    pts=[(x-W/2,y-H/2) for x,y in pts]
    faces=''
    shade=[0.0,0.06,0.16,0.22,0.3,0.3,0.22,0.06]
    for i in range(8):
        (px,py),(qx,qy)=pts[i],pts[(i+1)%8]; L=math.hypot(qx-px,qy-py); a=math.degrees(math.atan2(qy-py,qx-px))
        mx,my=(px+qx)/2*s,(py+qy)/2*s; col=wallcol(opt,k); dk=EC[k][1] if opt=='E' else '#E9D3A0' if opt=='R' else BAND[k][3] if opt=='Q' else (INKM[k] if opt in 'MNPQ' else (SOAPS[k]['dk'] if opt not in 'BDG' else '#FFF4DE'))
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

def page(name,title,blurb,opt,bg):
    sc=''.join(f'<div style="position:absolute;left:{250+i*430}px;top:{520}px;transform-style:preserve-3d">{box(opt,k,ry=-22,rx=-12)}</div>' for i,k in enumerate(ORDER))
    html=(f'<html><head><style>{CSS}html,body{{margin:0}}.b{{position:relative;width:1800px;height:820px;background:{bg};overflow:hidden;perspective:2600px}}'
          f'.h{{position:absolute;left:60px;top:44px;font:52px IS;color:#2A2017}}.p{{position:absolute;left:62px;top:112px;width:1500px;font:21px/1.45 G;color:#4A4036}}</style></head>'
          f'<body><div class="b"><div class="h">{title}</div><div class="p">{blurb}</div>{sc}</div></body></html>')
    open(O+name+'.html','w').write(html)
def flat(name,opt,bg):
    cells=''.join(f'<div style="position:absolute;left:{60+(i%2)*860}px;top:{60+(i//2)*500}px;width:816px;height:486px;filter:drop-shadow(0 18px 30px rgba(0,0,0,.18))">{front(opt,k)}</div>' for i,k in enumerate(ORDER))
    open(O+name+'.html','w').write(f'<html><head><style>{CSS}html,body{{margin:0}}</style></head><body><div style="position:relative;width:1740px;height:1080px;background:{bg}">{cells}</div></body></html>')





page('E-engraved','After the board: engraved vanilla, one ink, colour-blocked','As on the Sowvital, Taini and Lomenai pins: our vanilla drawn in line engraving in a single ink, large and cropped by the box; cream and soft-colour boxes alternating; the name in serif, mixed case; a small details block.','E','#E6E0D5')
flat('E-flat','E','#E6E0D5')
page('F-bloom-duo','Bloom, two flowers','One vanilla flower large and cropped off the box, a second one small, out of the way of the type; soft watercolour glow, heavier blur and grain than the post.','F','#E6E0D5')
flat('F-flat','F','#E6E0D5')
print('ok')

def sheet(name,items,bg='#E6E0D5'):
    cells=''.join(f'<div style="position:absolute;left:{40+(i%2)*850}px;top:{40+(i//2)*510}px;width:816px;height:486px;filter:drop-shadow(0 10px 18px rgba(0,0,0,.18))">{front(o,k)}</div>' for i,(o,k) in enumerate(items))
    rows=(len(items)+1)//2
    open(O+name+'.html','w').write(f'<html><head><style>{CSS}html,body{{margin:0}}</style></head><body><div style="position:relative;width:1740px;height:{40+rows*510}px;background:{bg}">{cells}</div></body></html>')
sheet('F-ebony-options',[('F4','ebony'),('F5','ebony'),('F1','ebony'),('F','vanilla')])
