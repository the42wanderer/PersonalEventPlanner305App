# Concept A: the herbarium sheet. The wrap is one specimen sheet: the specimen taped at the centre,
# its determination slip under it, field notes, an accession barcode and a rubber-stamp batch box round the back.
import re
from PIL import Image
from kit import *
from content import *
PAPER='#F7F0DF'; CARD='#FFFBF2'; FX0,FX1=73,153
EMB=re.search(r'<g fill="[^"]*">(.*)</g>',open(R+'/brand/emblem/vanilla-shop-emblem-savor-the-calm_green.svg').read(),re.S).group(1)
SPEC={'01':dict(img='spec-01.png',tapes=[(0.22,0.84,-24),(0.70,0.62,18)]),
      '02':dict(img='spec-02.png',tapes=[(0.50,0.93,-8),(0.60,0.42,24)]),
      '03':dict(img='spec-03.png',tapes=[(0.86,0.52,62),(0.40,0.47,-18)])}
def tape(x,y,ang,col,w=11,h=2.7):
    # a gummed paper strip with slightly ragged ends
    j=[0,.35,-.25,.3,0]; l=' '.join(f'{-w/2+j[i]*0.6:.2f},{-h/2+i*h/4:.2f}' for i in range(5)); r=' '.join(f'{w/2-j[i]*0.6:.2f},{h/2-i*h/4:.2f}' for i in range(5))
    pts=l+' '+r
    return (f'<g transform="translate({x:.2f} {y:.2f}) rotate({ang})"><polygon points="{pts}" fill="#000" opacity="0.07" transform="translate(0.25 0.35)"/>'
            f'<polygon points="{pts}" fill="{col}" opacity="0.9"/></g>')
def stamp(cx,cy,d,col,ang=-14,op=0.78):
    s=d/250; return f'<g transform="translate({cx-d/2:.2f} {cy-d/2:.2f}) rotate({ang} {d/2} {d/2}) scale({s:.5f})" fill="{col}" opacity="{op}">{EMB}</g>'
def leader(lab_,val,x,y,w,sz,c,mid):
    # typewriter field line with a dotted leader
    lw_=width(lab_,'GMono',sz); vw=width(val,'G',sz*1.05)
    return [txt(lab_,x,y,sz,mid,'GMono'), txt(val,x+w,y,sz*1.05,c,'G','end'),
            f'<path d="M{x+lw_+1:.2f} {y-0.3:.2f}H{x+w-vw-1:.2f}" stroke="{c}" stroke-width="0.22" stroke-dasharray="0.05 0.7" stroke-linecap="round" opacity="0.6"/>']
def herb(k,ml='500 ML'):
    s=SKU[k]; c,mid=s['dark'],s['mid']; col=s['ribbon']; sp=SPEC[k]
    o=[f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']
    # ---- FRONT: specimen, tapes, slip, stamp
    im=Image.open(T+sp['img']); bw,bh=54,36.5; sc=min(bw/im.width,bh/im.height); iw,ih=im.width*sc,im.height*sc
    ix,iy=CX-iw/2,4.2+(bh-ih)/2+1.5
    o.append(img(sp['img'],ix,iy,iw,ih))
    for fx,fy,a in sp['tapes']: o.append(tape(ix+fx*iw,iy+fy*ih,a,col))
    o.append(stamp(CX+28.5,12.5,17,mid))
    sx0,sx1,sy0,sy1=CX-30,CX+30,42.2,67.4
    o+=[f'<rect x="{sx0+0.35}" y="{sy0+0.45}" width="{sx1-sx0}" height="{sy1-sy0}" fill="#000" opacity="0.06"/>',
        f'<rect x="{sx0}" y="{sy0}" width="{sx1-sx0}" height="{sy1-sy0}" fill="{CARD}"/>',
        f'<rect x="{sx0+1}" y="{sy0+1}" width="{sx1-sx0-2}" height="{sy1-sy0-2}" fill="none" stroke="{c}" stroke-width="0.35"/>',
        f'<rect x="{sx0+1.7}" y="{sy0+1.7}" width="{sx1-sx0-3.4}" height="{sy1-sy0-3.4}" fill="none" stroke="{c}" stroke-width="0.12"/>']
    o+=[txt(s['no'],sx0+3.6,sy0+6.1,4.2,c,'IS'), caps('THE VANILLA SHOP',CX,sy0+5.4,1.45,mid,'middle',0.3), caps(ml,sx1-3.6,sy0+5.4,1.6,c,'end',0.25),
        rule(sx0+3.2,sy0+7.6,sx1-3.2,sy0+7.6,c,0.15,0.6)]
    o.append(txt(f'{s["l1"]} {s["l2"]}',CX,sy0+15.4,9.6,c,'IS','middle'))
    o.append(caps(s['kind'],CX,sy0+19.3,1.75,mid,'middle',0.32))
    o.append(txt('Vanilla planifolia  ·  Sri Lanka',CX,sy0+22.4,1.6,c,'GMono','middle'))
    # ---- LEFT: field notes and entries, accession barcode, batch stamp
    lx0,lx1=6,FX0-6; lw=lx1-lx0
    o.append(caps('FIELD NOTES',lx0,6.2,1.55,mid))
    p,ye=para(s['story'],lx0,10,lw,1.75,2.5,c,'GMono'); o+=p
    y=ye+4.2
    for lab_,val in s['rows']: o+=leader(lab_.capitalize(),val,lx0,y,lw,1.75,c,mid); y+=2.9
    b,bw_=ean13(s['ean'],lx0+1.4,46.5,0.255,9.6,'#1A120C'); o+=b
    o.append(caps('ACC.',lx0,44.6,1.3,mid,tr=0.2))
    bx0=lx0+bw_+5; o.append(f'<rect x="{bx0}" y="45.2" width="{lx1-bx0}" height="14.2" rx="1.4" fill="none" stroke="{mid}" stroke-width="0.35" opacity="0.85"/>')
    for i,kk in enumerate(('MFD','EXP','BATCH')):
        yy=49.2+i*4.1; o+=[caps(kk,bx0+2,yy,1.35,mid,tr=0.2), rule(bx0+10,yy+0.4,lx1-2,yy+0.4,mid,0.15,0.6)]
    # ---- RIGHT: nutrition card, marks, maker, the range's colour chart
    rx0,rx1=FX1+6,W-6; rw=rx1-rx0
    o+=[f'<rect x="{rx0-1.6+0.3}" y="{3.4+0.4}" width="{rw+3.2}" height="31.6" fill="#000" opacity="0.05"/>',
        f'<rect x="{rx0-1.6}" y="3.4" width="{rw+3.2}" height="31.6" fill="{CARD}" stroke="{c}" stroke-width="0.15" stroke-opacity="0.5"/>']
    o+=[caps('NUTRITION  ·  PER TEASPOON, 5 ML',rx0,7,1.5,mid), caps('% DV',rx1,7,1.35,mid,'end')]
    y=8.4; o.append(rule(rx0,y,rx1,y,c,0.25,0.8))
    for name,amt,dv in NUTRITION:
        y+=2.75; ind=name.startswith('  ')
        o+=[txt(name.strip(),rx0+(2 if ind else 0),y,1.85,c), txt(amt,rx0+rw*0.62,y,1.85,c,'G','end'), txt(dv,rx1,y,1.85,c,'G','end')]
        o.append(rule(rx0,y+0.85,rx1,y+0.85,c,0.12,0.35))
    y=40.6
    for i,lab_ in enumerate(('USDA','EU','SGS')):
        cx=rx0+3.4+i*8; o+=[f'<circle cx="{cx}" cy="{y}" r="3.2" fill="none" stroke="{c}" stroke-width="0.2" stroke-dasharray="0.6 0.5" opacity="0.7"/>', caps(lab_,cx,y+0.55,1.2,c,'middle',0.1)]
    o+=[caps('PRODUCT OF SRI LANKA',rx1,y-1.2,1.35,mid,'end'), txt(f'MRP Rs. {s["mrp"]}',rx1,y+2.6,2.3,c,'GB','end')]
    y=48.4; o.append(caps('MANUFACTURED & MARKETED BY',rx0,y,1.3,mid)); y+=2.8
    for i,l in enumerate(MAKER): o.append(txt(l,rx0,y+i*2.3,1.7,c,'GB' if i==0 else 'G'))
    # colour chart, as on a digitised herbarium sheet: the three extracts, this one marked
    y=63.2; o.append(caps('THE RANGE',rx0,y+2.6,1.3,mid,tr=0.2)); x=rx0+14
    for kk,cc in (('01','#9E2F1C'),('02','#A06A14'),('03','#2F5A33')):
        o.append(f'<rect x="{x}" y="{y}" width="9" height="3.6" fill="{cc}"/>'); o.append(txt(f'No. {kk}',x+10.2,y+2.8,1.6,c,'G'))
        if kk==k: o.append(f'<rect x="{x-0.7}" y="{y-0.7}" width="10.4" height="5" fill="none" stroke="{c}" stroke-width="0.25"/>')
        x+=16.5
    o.append(img('grain.png',0,0,W,H,'opacity="0.45"'))
    return o
SKU['03']=dict(no='No. 03',l1='Vanilla',l2='Syrup',kind='NATURAL SYRUP',ean='4796034220083',mrp='12,500',art=None,dark='#16301C',mid='#3E6B3A',ribbon='#2F5A33',light='#E7EFCF',
               story=HISTORY+' Made into a syrup for coffee, shakes and desserts.',
               rows=[('SPECIES','Vanilla planifolia'),('ORIGIN','Sri Lanka'),('BEST FOR','Coffee and shakes'),('USE','2 tsp per cup')])
if __name__=='__main__':
    for k in ('01','02','03'):
        svg(herb(k),f'H-{k}')
        for ml in ('100','200'): svg(herb(k,ml+' ML'),f'H-{k}-{ml}')
    print('ok')
