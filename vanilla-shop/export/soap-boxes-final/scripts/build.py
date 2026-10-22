# Full soap-box flats, approved "Bloom duo" design, on the current box's layout (Soap__packs.pdf), mm:
#   back panel x 28.4-164.1, y 0-81.3 (printed upside down) · top wall y 81.3-110.8 · front y 110.8-192.0
#   bottom wall y 192.0-221.5 · left wall x 0-28.4 · right wall x 164.1-190.3
# Writes, per soap: PRINT (CMYK art + text, foil areas left as paper), FOIL (the foil plate, solid black),
# PROOF (cut in magenta, folds in cyan, foil simulated, pink = text to check). Text and data are from the boxes on sale.
import sys, json
sys.path.insert(0,'/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/ext/w')
import kit
from kit import width, logo, txt, caps, rule, para, ean13, esc
R='/home/user/PersonalEventPlanner305App/vanilla-shop'
kit.FONTS.update({'NSi':R+'/fonts/noto-serif-sinhala.ttf','NTa':R+'/fonts/noto-serif-tamil.ttf','ISR':R+'/fonts/instrument-serif.ttf'})
css=''.join(f"@font-face{{font-family:{k};src:url(file://{v})}}" for k,v in kit.FONTS.items())
O='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/soap/full/'
B=3.0; SW,SH=190.3,221.5; FX0,FX1,FY0,FY1,FLY=28.4,164.1,110.8,192.0,81.3; M=12
FOILG=('<linearGradient id="foil" x1="0" y1="0" x2="1" y2="0.35"><stop offset="0" stop-color="#4E300A"/><stop offset="0.28" stop-color="#8E6420"/>'
       '<stop offset="0.46" stop-color="#C9A55A"/><stop offset="0.6" stop-color="#76521A"/><stop offset="0.85" stop-color="#A37A30"/><stop offset="1" stop-color="#4E300A"/></linearGradient>')
def chk(c12): return c12+str((10-sum(int(v)*(3 if i%2 else 1) for i,v in enumerate(c12))%10)%10)
PH_EAN=chk('200000000000')     # 2xx = in-store numbers, never a real product: an obvious placeholder
SOAP={
 'vanilla': dict(l2='Bathing Bar',desc='',ink='#5A3410',deep='#8A5A10',kind='BATHING BAR',
                 ean='4796034220069',mrp='1,200',tfm='70',mfd='01/09/2025',exp='30/08/2027',extra=None,
                 en='Rejuvenate your skin and spirit with The Vanilla Shop bathing bar.'),
 'rosette': dict(l2='Rose',desc='Vanilla & rose bathing bar',ink='#5A1426',deep='#9A3550',kind='VANILLA & ROSE BATHING BAR',
                 ean='4796034220076',mrp='1,300',tfm='63',mfd='02/04/2025',exp='01/04/2027',extra=('rose extract',True),
                 en='Rejuvenate your skin and spirit with The Vanilla Shop vanilla and rose bathing bar.'),
 'charcoal':dict(l2='Charcoal+',desc='Charcoal & vanilla bathing bar',ink='#141414',deep='#55504B',kind='CHARCOAL & VANILLA BATHING BAR',
                 ean=None,mrp='1,300',tfm=None,mfd=None,exp=None,extra=('charcoal',True),
                 en='Rejuvenate your skin and spirit with The Vanilla Shop vanilla and charcoal bathing bar.'),
 'aloe':    dict(l2='Aloe Vera',desc='Vanilla & aloe vera bathing bar',ink='#16301C',deep='#3F7A47',kind='VANILLA & ALOE VERA BATHING BAR',
                 ean=None,mrp='1,300',tfm=None,mfd=None,exp=None,extra=('aloe vera',False),
                 en='Rejuvenate your skin and spirit with The Vanilla Shop vanilla and aloe vera bathing bar.'),
}
EN_REST=(' It hydrates and protects your skin with the natural antioxidant benefits of vanilla and helps reduce fine lines, '
         'while its warm aroma soothes the senses and lifts your mood, leaving your skin soft, radiant and youthful. ')
EN_END={'aloe':'Choose it for smooth, soft, flawless skin.'}
SI_BODY=('අපගේ නිෂ්පාදනයේ ස්වාභාවික වැනිලාවල ඇති ප්‍රතිඔක්සිකාරක ගුණය මගින් ඔබේ සමෙහි තෙතමනය සහ තරුණ පෙනුම තවත් '
         'වැඩිදියුණු කරන්න. එහි ඇති උණුසුම් වැනිලා සුවඳ ඔබේ මනසද ප්‍රබෝධමත් කිරීමට උපකාරී වේ.')
TA_BODY=('The Vanilla Shop குளியல் பார் வயதான தோற்றத்தைக் குறைக்கும் (anti-aging) மற்றும் ஆன்டிஆக்ஸிடன்ட் நன்மைகளுடன் '
         'உங்கள் தோலை அருமையாகப் பராமரிக்கிறது. இதனால் தோல் நன்கு ஈரப்பதமாகவும், பாதுகாக்கப்பட்டும், மிருதுவாகவும், '
         'பிரகாசமாகவும் இருக்கும். இதன் இதமான, வெப்பமான மணம் உங்கள் உணர்வுகளை அமைதியாக்கி, மனநிலையை மேம்படுத்துகிறது.')
MODE='print'   # print | foil | proof
def mark(x,y,w,h): return f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="#FF2BA6" opacity="0.3" rx="0.4"/>' if MODE=='proof' else ''
def ink(c): return '#000' if MODE=='foil' else c
def show(): return MODE!='foil'           # everything but the foil is left off the foil plate
def foilfill(): return '#000' if MODE=='foil' else ('url(#foil)' if MODE=='proof' else 'none')
def front(s):
    c=s['ink']; x=12
    g=[]
    if show(): g.append(logo(x+9,16,18,c))
    rest=esc(' &' if s['l2']!='Bathing Bar' else '')
    g.append(f'<text x="{x-0.8}" y="44" font-family="ISR" font-size="21"><tspan fill="{foilfill()}">Vanilla</tspan>'
             +(f'<tspan fill="{c}">{rest}</tspan>' if show() else '')+'</text>')
    if show():
        l2=s['l2']; plus=l2.endswith('+')
        g.append(f'<text x="{x-0.8}" y="61" font-family="IS" font-size="21" fill="{c}">{esc(l2.rstrip("+"))}'
                 +('<tspan font-family="ISR" font-size="11" dx="0.8" dy="-8.5">+</tspan>' if plus else '')+'</text>')
        # the same two lines under every name: what it is (caps), then the farm line; 100% natural sits over the weight
        g.append(caps(s['kind'] if s['desc'] else '100% NATURAL',x,72.9,2.3,c,tr=0.13))
        if s['desc']: g.append(caps('100% NATURAL',124,72.9,2.3,c,'end',0.13))
        g.append(txt('Made with vanilla grown on our own farms.',x,77.6,4.1,c,'IS'))
        g.append(caps('NET WT. 100 g',124,77.6,4.4,c,'end',0))
    sx=(FX1-FX0)/136; sy=(FY1-FY0)/81
    return [f'<g transform="translate({FX0} {FY0}) scale({sx:.5f} {sy:.5f})">'+''.join(g)+'</g>']
import math
sys.path.insert(0,'/home/user/PersonalEventPlanner305App/vanilla-shop/brand/directions/bloom')
import orchid
def podmark(W):
    p=orchid.pod(W/2-9,5.6,W/2+9,4.4,1.5)                   # a small cured pod, in the same gold foil as "Vanilla"
    f=foilfill()
    return f'<path d="{p["body"]}" fill="{f}"/><path d="{p["curl"]}" fill="none" stroke="{f}" stroke-width="0.4" stroke-linecap="round"/>'
def back(s,k):
    W=FX1-FX0
    if not show(): return [f'<g transform="translate({FX0+W} {FLY}) rotate(180)">'+podmark(W)+'</g>']
    c=s['ink']; d=s['deep']; o=[podmark(W)]
    o.append(txt('Nourish, rejuvenate and uplift.',W/2,13.5,7.0,c,'IS','middle'))
    o.append(rule(10,18.5,W-10,18.5,c,0.2,0.5))
    cw=37.5; xs=(9,9+cw+5.3,9+2*(cw+5.3)); y0=23.5
    o.append(caps('ENGLISH',xs[0],y0,1.3,d,tr=0.25)); o.append(txt('සිංහල',xs[1],y0+0.2,1.7,d,'NSi')); o.append(txt('தமிழ்',xs[2],y0+0.2,1.55,d,'NTa'))
    p,_=para(s['en']+EN_REST+EN_END.get(k,'Care for skin and spirit.'),xs[0],y0+4.4,cw,2.05,2.75,c); o+=p
    ph,yh=para('ඔබේ සමට සහ මනසට නැවුම් ප්‍රබෝධයක්',xs[1],y0+4.4,cw-1,1.95,2.7,c,'NSi'); o+=ph
    p,_=para(SI_BODY,xs[1],yh+3.2,cw,1.75,2.75,c,'NSi'); o+=p
    ph,yh=para('உங்கள் தோலுக்கும் மனதிற்கும் புத்துணர்ச்சி',xs[2],y0+4.4,cw,1.75,2.6,c,'NTa'); o+=ph
    p,ye=para(TA_BODY,xs[2],yh+3.2,cw,1.5,2.45,c,'NTa'); o+=[mark(xs[2]-0.5,y0+2.6,cw+1,ye-y0)]+p
    for x in (xs[1]-2.65,xs[2]-2.65): o.append(rule(x,y0-2,x,62,c,0.15,0.35))
    o.append(rule(10,66,W-10,66,c,0.2,0.5))
    o.append(caps('INGREDIENTS',10,71,1.35,d,tr=0.25))
    ex=s['extra']; ing='Vanilla planifolia bean extract, Vanilla planifolia bean powder, '+(ex[0]+', ' if ex else '')+'sodium palmate, sodium palm kernelate, glycerin.'
    p,ye=para(ing,31,71,W-41,1.85,2.5,c); o+=[mark(30.5,68.6,W-40,ye-71+3.4)]+p
    return [f'<g transform="translate({FX0+W} {FLY}) rotate(180)">'+''.join(o)+'</g>']
def top_wall(s):
    if not show(): return []
    c=s['ink']; cx=(FX0+FX1)/2; o=[]
    o.append(caps('BATHING BAR',cx-30,88.2,2.0,c,'middle',0.3))
    o.append(txt('බේතින් බාර්',cx,88.4,2.4,c,'NSi','middle'))
    o+=[mark(cx+19.5,85.6,21,3.6),txt('பாத்திங் பார்',cx+30,88.4,2.2,c,'NTa','middle')]
    for x in (cx-15,cx+15): o.append(rule(x,85.6,x,89.4,c,0.15,0.5))
    o.append(txt('Important: for external use only. Discontinue use if irritation occurs.',cx,93.6,2.05,c,'G','middle'))
    o.append(txt('බාහිර භාවිතය සඳහා පමණයි. අසාත්මිකතාවයක් ඇති වුවහොත් භාවිතය නවත්වන්න.',cx,97.5,1.85,c,'NSi','middle'))
    ta='வெளிப்புறப் பயன்பாட்டிற்கு மட்டும். ஒவ்வாமை ஏற்பட்டால் பயன்படுத்துவதை நிறுத்தவும்.'
    o+=[mark(cx-width(ta,'NTa',1.7)/2,99.2,width(ta,'NTa',1.7),3.2),txt(ta,cx,101.4,1.7,c,'NTa','middle')]
    t=f'Net wt. 100 g  ·  TFM {s["tfm"] or "__"}% when packed'
    if not s['tfm']: o.append(mark(cx-width(t,'GB',2.4)/2,104.4,width(t,'GB',2.4),3.0))
    o.append(txt(t,cx,106.6,2.4,c,'GB','middle'))
    return o
def left_wall(s):
    if not show(): return []
    c=s['ink']; d=s['deep']
    g=[txt(f'MRP Rs. {s["mrp"]}',4,7.4,3.0,c,'GB')]
    code=s['ean'] or PH_EAN
    b,bw=ean13(code,5.2,10.4,0.25,8.2,'#1A120C'); g+=b
    if not s['ean']: g+=[caps('PLACEHOLDER BARCODE · REPLACE',4,25.6,1.25,'#C0007A',tr=0.15)]
    for i,(k,v) in enumerate((('MFD',s['mfd']),('EXP',s['exp']))):
        g+=[caps(k,36,14.6+i*4.2,1.4,d,tr=0.2),txt(v or '__/__/____',44.5,14.6+i*4.2,2.1,c)]
        if not v: g.append(mark(44,12.4+i*4.2,13,3))
    return [f'<g transform="translate(1.4 {FY1-3.5}) rotate(-90)">'+''.join(g)+'</g>']
def bottom_wall(s):
    if not show(): return []
    c=s['ink']; d=s['deep']; y=FY1; o=[logo(FX0+14,y+14.6,15,c)]
    x=FX0+28; o.append(caps('MARKETED BY',x,y+6.6,1.3,d,tr=0.25))
    for i,l in enumerate(['Agroventures Exports (Pvt) Ltd','No 48, Sir Marcus Fernando Mawatha, Colombo 07','info@agroventuresexports.com  ·  www.agroventuresexports.com','Hotline +94 11 218 7287  ·  +94 11 287 8766']):
        o.append(txt(l,x,y+9.9+i*2.45,1.85 if i else 1.95,c,'GB' if i==0 else 'G'))
    x2=FX0+96; o.append(caps('MANUFACTURED BY',x2,y+6.6,1.3,d,tr=0.25))
    for i,l in enumerate(['Galaxy Manufacturers (Pvt) Ltd','No 15, Raja Mawatha,','Ja-Ela, Sri Lanka']):
        o.append(txt(l,x2,y+9.9+i*2.45,1.95 if i==0 else 1.85,c,'GB' if i==0 else 'G'))
    o.append(rule(x2-3.5,y+5,x2-3.5,y+19,c,0.15,0.4))
    o.append(caps('PRODUCT OF SRI LANKA',x2,y+20.6,1.5,d,tr=0.25))
    return o
def right_wall(s):
    c=s['ink']; d=s['deep']; l2=s['l2']; amp='' if l2=='Bathing Bar' else ' &amp;'
    name=(f'<text x="0" y="0" font-family="ISR" font-size="7.4" text-anchor="middle"><tspan fill="{foilfill()}">Vanilla</tspan>'
          +(f'<tspan fill="{c}">{amp} </tspan><tspan font-family="IS" fill="{c}">{esc(l2)}</tspan>' if show() else
            f'<tspan fill="none">{amp} </tspan><tspan font-family="IS" fill="none">{esc(l2)}</tspan>')+'</text>')
    g=[name]+([caps(s['kind'],0,5.4,1.35,d,'middle',0.28)] if show() else [])
    return [f'<g transform="translate({(FX1+SW)/2-1.2} {(FY0+FY1)/2}) rotate(-90)">'+''.join(g)+'</g>']
def build(k):
    s=SOAP[k]; o=[]
    if MODE=='foil': o.append(f'<rect x="{-B}" y="{-B}" width="{SW+2*B}" height="{SH+2*B}" fill="#fff"/>')
    else: o.append(f'<image href="file://{O}art-{k}.jpg" x="{-B}" y="{-B}" width="{SW+2*B}" height="{SH+2*B}" preserveAspectRatio="none"/>')
    o+=back(s,k)+top_wall(s)+front(s)+left_wall(s)+bottom_wall(s)+right_wall(s)
    if MODE=='proof':
        cut=f'M{FX0} 0H{FX1}V{FLY}H{SW}V{SH}H0V{FLY}H{FX0}Z'
        o.append(f'<path d="{cut}" fill="none" stroke="#EC008C" stroke-width="0.25"/>')
        for (a,b_,x2,y2) in ((0,FY0,SW,FY0),(0,FY1,SW,FY1),(FX0,FLY,FX0,SH),(FX1,FLY,FX1,SH),(FX0,FLY,FX1,FLY)):
            o.append(f'<path d="M{a} {b_}L{x2} {y2}" stroke="#00A0E0" stroke-width="0.2" stroke-dasharray="1.2 0.8"/>')
    return o
NAMES={'vanilla':'Vanilla Bathing Bar','rosette':'Vanilla & Rose','charcoal':'Vanilla & Charcoal+','aloe':'Vanilla & Aloe Vera'}
def page(k,o,name):
    PW,PH=SW+2*B+2*M,SH+2*B+2*M+6
    inner=(f'<svg xmlns="http://www.w3.org/2000/svg" style="position:absolute;left:{M}mm;top:{M}mm" width="{SW+2*B}mm" height="{SH+2*B}mm" '
           f'viewBox="{-B} {-B} {SW+2*B} {SH+2*B}"><defs>{FOILG}</defs>'+''.join(o)+'</svg>')
    cm=''
    ox,oy=M+B,M+B   # sheet origin on the page
    for (x,y,dx,dy) in ((FX0,0,0,-1),(FX1,0,0,-1),(0,FLY,-1,0),(SW,FLY,1,0),(0,SH,-1,0),(SW,SH,1,0),(0,SH,0,1),(SW,SH,0,1),(FX0,0,-1,0),(FX1,0,1,0)):
        X,Y=ox+x,oy+y
        cm+=f'<path d="M{X+dx*4:.2f} {Y+dy*4:.2f}L{X+dx*10:.2f} {Y+dy*10:.2f}" stroke="#000" stroke-width="0.12"/>'
    what={'print':'print file · CMYK · foil areas left unprinted, see FOIL plate','foil':'FOIL PLATE · gold foil · 100% = foil · register to the print file',
          'proof':'PROOF · magenta = cut, cyan dashes = folds, pink = text to check, foil simulated'}[MODE]
    cm+=f'<text x="{M}" y="{PH-6}" font-family="G" font-size="2.6" fill="#333">The Vanilla Shop  {esc(NAMES[k])} box · flat {SW} × {SH} mm · bleed {B:.0f} mm · {what}</text>'
    over=f'<svg xmlns="http://www.w3.org/2000/svg" style="position:absolute;left:0;top:0" width="{PW}mm" height="{PH}mm" viewBox="0 0 {PW} {PH}">{cm}</svg>'
    open(O+name+'.html','w').write(f'<html><head><style>{css}@page{{size:{PW}mm {PH}mm;margin:0}}html,body{{margin:0}}</style></head>'
        f'<body><div style="position:relative;width:{PW}mm;height:{PH}mm;background:#fff">{inner}{over}</div></body></html>')
    return [O+name,round(PW,1),round(PH,1)]
man=[]
for m in ('print','foil','proof'):
    MODE=m
    for k in SOAP: man.append(page(k,build(k),f'{k}_box_{m.upper()}'))
json.dump(man,open(O+'man.json','w')); print('ok',PH_EAN)
