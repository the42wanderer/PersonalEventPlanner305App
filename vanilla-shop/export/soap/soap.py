# Soap box, Bloom direction, on the current box's flat layout (Soap__packs.pdf), in mm:
#   back panel 28.4-164.1 x 0-81.3 (printed upside down, folds over the top wall)
#   top wall y 81.3-110.8 · front x 28.4-164.1, y 110.8-192.0 · bottom wall y 192.0-221.5
#   left wall x 0-28.4 · right wall x 164.1-190.3
import sys; sys.path.insert(0,'../w')
import kit
from kit import width, logo, txt, caps, rule, para, ean13
R='/home/user/PersonalEventPlanner305App/vanilla-shop'
kit.FONTS.update({'NSi':R+'/fonts/noto-serif-sinhala.ttf','NTa':R+'/fonts/noto-serif-tamil.ttf'})
css=''.join(f"@font-face{{font-family:{k};src:url(file://{v})}}" for k,v in kit.FONTS.items())
T='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/soap/new/'
B=3.0; SW,SH=190.3,221.5
FX0,FX1,FY0,FY1=28.4,164.1,110.8,192.0; FLY=81.3
PAPER='#F7EFDC'
SI_BODY=('අපගේ නිෂ්පාදනයේ ස්වාභාවික වැනිලාවල ඇති ප්‍රතිඔක්සිකාරක ගුණය මගින් ඔබේ සමෙහි තෙතමනය සහ තරුණ පෙනුම තවත් '
         'වැඩිදියුණු කරන්න. එහි ඇති උණුසුම් වැනිලා සුවඳ ඔබේ මනසද ප්‍රබෝධමත් කිරීමට උපකාරී වේ.')
TA_BODY=('The Vanilla Shop குளியல் பார் வயதான தோற்றத்தைக் குறைக்கும் (anti-aging) மற்றும் ஆன்டிஆக்ஸிடன்ட் நன்மைகளுடன் '
         'உங்கள் தோலை அருமையாகப் பராமரிக்கிறது. இதனால் தோல் நன்கு ஈரப்பதமாகவும், பாதுகாக்கப்பட்டும், மிருதுவாகவும், '
         'பிரகாசமாகவும் இருக்கும். இதன் இதமான, வெப்பமான மணம் உங்கள் உணர்வுகளை அமைதியாக்கி, மனநிலையை மேம்படுத்துகிறது.')
SOAP={
 'vanilla':dict(art='bloom-vanilla.jpg',dark='#4A2C08',deep='#8A5A10',
    big='Vanilla',small=None,kind='BATHING BAR',ean='4796034220069',mrp='1,200',tfm='70',mfd='01/09/2025',exp='30/08/2027',
    en='Rejuvenate your skin and spirit with The Vanilla Shop bathing bar.'),
 'rosette':dict(art='bloom-rosette.jpg',dark='#5A1426',deep='#9A3550',
    big='Rosette',small='Vanilla &',kind='VANILLA & ROSE BATHING BAR',ean='4796034220076',mrp='1,300',tfm='63',mfd='02/04/2025',exp='01/04/2027',
    en='Rejuvenate your skin and spirit with The Vanilla Shop vanilla and rose bathing bar.'),
}
EN_REST=(' It hydrates and protects your skin with the natural antioxidant benefits of vanilla and helps reduce fine lines, '
         'while its warm aroma soothes the senses and lifts your mood, leaving your skin soft, radiant and youthful. '
         'Care for skin and spirit.')
INGR='Vanilla planifolia bean extract, Vanilla planifolia bean powder, sodium palmate, sodium palm kernelate, glycerin.'
PROOF=False
def mark(x,y,w,h):
    return f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="#FF2BA6" opacity="0.3" rx="0.4"/>' if PROOF else ''
def back(s,c,d):
    """the back panel, drawn upright in its own frame (136 x 81), then turned over onto the sheet"""
    W=FX1-FX0; o=[]
    o.append(txt('Nourish, rejuvenate and uplift.',W/2,13.5,7.0,c,'IS','middle'))
    o.append(rule(10,18.5,W-10,18.5,c,0.2,0.5))
    cw=37.5; xs=(9,9+cw+5.3,9+2*(cw+5.3)); y0=23.5
    o.append(caps('ENGLISH',xs[0],y0,1.3,d,tr=0.25)); o.append(txt('සිංහල',xs[1],y0+0.2,1.7,d,'NSi')); o.append(txt('தமிழ்',xs[2],y0+0.2,1.55,d,'NTa'))
    p,_=para(s['en']+EN_REST,xs[0],y0+4.4,cw,2.05,2.75,c); o+=p
    ph,yh=para('ඔබේ සමට සහ මනසට නැවුම් ප්‍රබෝධයක්',xs[1],y0+4.4,cw-1,1.95,2.7,c,'NSi'); o+=ph
    p,_=para(SI_BODY,xs[1],yh+3.2,cw,1.75,2.75,c,'NSi'); o+=p
    ph,yh=para('உங்கள் தோலுக்கும் மனதிற்கும் புத்துணர்ச்சி',xs[2],y0+4.4,cw,1.75,2.6,c,'NTa'); o+=ph
    p,ye=para(TA_BODY,xs[2],yh+3.2,cw,1.5,2.45,c,'NTa'); o+=[mark(xs[2]-0.5,y0+2.6,cw+1,ye-y0)]+p
    for x in (xs[1]-2.65,xs[2]-2.65): o.append(rule(x,y0-2,x,62,c,0.15,0.35))
    o.append(rule(10,66,W-10,66,c,0.2,0.5))
    o.append(caps('INGREDIENTS',10,71,1.35,d,tr=0.25))
    p,ye=para(INGR,31,71,W-41,1.85,2.5,c); o+=[mark(30.5,68.6,W-40,ye-71+3.4)]+p
    return f'<g transform="translate({FX0+W} {FLY}) rotate(180)">'+''.join(o)+'</g>'
def top_wall(s,c,d):
    cx=(FX0+FX1)/2; o=[]
    o.append(caps('BATHING BAR',cx-30,88.2,2.0,c,'middle',0.3))
    o.append(txt('බේතින් බාර්',cx,88.4,2.4,c,'NSi','middle'))
    o+=[mark(cx+19.5,85.6,21,3.6),txt('பாத்திங் பார்',cx+30,88.4,2.2,c,'NTa','middle')]
    for x in (cx-15,cx+15): o.append(rule(x,85.6,x,89.4,c,0.15,0.5))
    o.append(txt('Important: for external use only. Discontinue use if irritation occurs.',cx,93.6,2.05,c,'G','middle'))
    o.append(txt('බාහිර භාවිතය සඳහා පමණයි. අසාත්මිකතාවයක් ඇති වුවහොත් භාවිතය නවත්වන්න.',cx,97.5,1.85,c,'NSi','middle'))
    ta='வெளிப்புறப் பயன்பாட்டிற்கு மட்டும். ஒவ்வாமை ஏற்பட்டால் பயன்படுத்துவதை நிறுத்தவும்.'
    o+=[mark(cx-width(ta,'NTa',1.7)/2,99.2,width(ta,'NTa',1.7),3.2),txt(ta,cx,101.4,1.7,c,'NTa','middle')]
    o.append(txt(f'Net wt. 100 g  ·  TFM {s["tfm"]}% when packed',cx,106.6,2.4,c,'GB','middle'))
    return o
def left_wall(s,c,d):
    o=[f'<rect x="1.2" y="{FY0+1.5}" width="25.4" height="{FY1-FY0-3}" fill="{PAPER}" opacity="0.92" rx="1"/>']
    g=[txt(f'MRP Rs. {s["mrp"]}',4,7.4,3.0,c,'GB')]
    b,bw=ean13(s['ean'],5.2,10.4,0.25,8.2,'#1A120C'); g+=b
    for i,(k,v) in enumerate((('MFD',s['mfd']),('EXP',s['exp']))):
        g+=[caps(k,36,14.6+i*4.2,1.4,d,tr=0.2),txt(v,44.5,14.6+i*4.2,2.1,c)]
    return o+[f'<g transform="translate(1.4 {FY1-3.5}) rotate(-90)">'+''.join(g)+'</g>']
def bottom_wall(s,c,d):
    y=FY1; o=[f'<rect x="{FX0+2}" y="{y+2.2}" width="{FX1-FX0-4}" height="25" fill="{PAPER}" opacity="0.9" rx="1"/>']
    o.append(logo(FX0+14,y+14.6,15,c))
    x=FX0+28; o.append(caps('MARKETED BY',x,y+6.6,1.3,d,tr=0.25))
    for i,l in enumerate(['Agroventures Exports (Pvt) Ltd','No 48, Sir Marcus Fernando Mawatha, Colombo 07','info@agroventuresexports.com  ·  www.agroventuresexports.com','Hotline +94 11 218 7287  ·  +94 11 287 8766']):
        o.append(txt(l,x,y+9.9+i*2.45,1.85 if i else 1.95,c,'GB' if i==0 else 'G'))
    x2=FX0+96; o.append(caps('MANUFACTURED BY',x2,y+6.6,1.3,d,tr=0.25))
    for i,l in enumerate(['Galaxy Manufacturers (Pvt) Ltd','No 15, Raja Mawatha,','Ja-Ela, Sri Lanka']):
        o.append(txt(l,x2,y+9.9+i*2.45,1.95 if i==0 else 1.85,c,'GB' if i==0 else 'G'))
    o.append(rule(x2-3.5,y+5,x2-3.5,y+19,c,0.15,0.4))
    return o
def right_wall(s,c,d):
    name=(s['small']+' ' if s['small'] else '')+s['big']
    g=[txt(name,0,0,7.2,c,'IS','middle'),caps(s['kind'],0,5.2,1.35,d,'middle',0.28)]
    return [f'<g transform="translate({(FX1+SW)/2-1.2} {(FY0+FY1)/2}) rotate(-90)">'+''.join(g)+'</g>']
def front(s,c,d):
    o=[logo(FX0+13,FY0+11,12,c)]
    x=FX0+8
    if s['small']: o.append(txt(s['small'],x+1,FY0+33,8.5,c,'IS'))
    o.append(txt(s['big'],x-1,FY0+52 if s['small'] else FY0+47,23 if s['small'] else 25,c,'IS'))
    o.append(caps(s['kind'],x+0.5,FY0+(59.5 if s['small'] else 55),2.25 if s['small'] else 2.9,d,tr=0.3))
    o.append(txt('100% natural  ·  made exclusively with our own farmed vanilla',x+0.5,FY1-7.6,2.15,c))
    o.append(caps('PRODUCT OF SRI LANKA',x+0.5,FY1-3.6,1.5,d,tr=0.28))
    o.append(txt('100 g',FX1-7,FY1-4.2,5.2,c,'IS','end'))
    return o
def build(k):
    s=SOAP[k]; c=s['dark']; d=s['deep']
    o=[f'<rect x="{-B}" y="{-B}" width="{SW+2*B}" height="{SH+2*B}" fill="{PAPER}"/>',
       f'<svg x="{-B}" y="{FLY}" width="{SW+2*B}" height="{SH-FLY+B}" viewBox="0 {B} {SW+2*B} {SH-FLY+B}"><image href="file://{T}{s["art"]}" width="{SW+2*B}" height="{SH-FLY+2*B}" preserveAspectRatio="none"/></svg>']
    o.append(back(s,c,d)); o+=top_wall(s,c,d); o+=front(s,c,d); o+=left_wall(s,c,d); o+=bottom_wall(s,c,d); o+=right_wall(s,c,d)
    if PROOF:
        cut=f'M{FX0} 0H{FX1}V{FLY}H{SW}V{SH}H0V{FLY}H{FX0}Z'
        o.append(f'<path d="{cut}" fill="none" stroke="#EC008C" stroke-width="0.25"/>')
        for (a,b_,x2,y2) in ((0,FY0,SW,FY0),(0,FY1,SW,FY1),(FX0,FLY,FX0,SH),(FX1,FLY,FX1,SH),(FX0,FLY,FX1,FLY)):
            o.append(f'<path d="M{a} {b_}L{x2} {y2}" stroke="#00A0E0" stroke-width="0.2" stroke-dasharray="1.2 0.8"/>')
    return o
def save(o,name):
    s_=(f'<svg xmlns="http://www.w3.org/2000/svg" width="{(SW+2*B)*20:.0f}" height="{(SH+2*B)*20:.0f}" '
        f'viewBox="{-B} {-B} {SW+2*B} {SH+2*B}">'+''.join(o)+'</svg>')
    open(T+name+'.html','w').write(f'<html><head><style>{css}html,body{{margin:0}}</style></head><body>{s_}</body></html>')
if __name__=='__main__':
    PROOF='proof' in sys.argv
    for k in SOAP: save(build(k),('PR-' if PROOF else 'SP-')+k)
    print('ok',round((SW+2*B)*20),round((SH+2*B)*20))
