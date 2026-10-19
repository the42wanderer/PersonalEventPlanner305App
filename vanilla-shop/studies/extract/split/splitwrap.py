# Split, full wrap (226 x 70 mm): colour half from the left panel to the bottle's centre, cream half from the centre round the right.
import sys; sys.path.insert(0,'../w')
from kit import width, logo, txt, caps, rule, para, ean13, css
from content import SKU as C, NUTRITION, MAKER
T='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/ext/d/'
W,H,CX=226,70,113; FX1=153; PAPER='#F7EFDC'
C['03']=dict(no='No. 03',l1='Vanilla',l2='Syrup',kind='NATURAL SYRUP',ean='4796034220083',mrp='12,500',
             story=C['01']['story'].split(' Steeped')[0]+' Made into a syrup for coffee, shakes and desserts.',
             rows=[('SPECIES','Vanilla planifolia'),('ORIGIN','Sri Lanka'),('BEST FOR','Coffee and shakes'),('USE','2 tsp per cup')])
LOOK={'01':dict(dark='#4A120C',deep='#7E2414',on='#FBE7D2',on2='#F3B996'),
      '02':dict(dark='#4A2C08',deep='#8A5A10',on='#3B2108',on2='#5C3A0C'),
      '03':dict(dark='#16301C',deep='#1F3F24',on='#EAF2D6',on2='#B9D29C')}
def spoon(x,y,c):
    return (f'<g fill="none" stroke="{c}" stroke-width="0.3" stroke-linecap="round"><ellipse cx="{x}" cy="{y}" rx="1.9" ry="1.25"/>'
            f'<path d="M{x+1.9} {y}L{x+7.2} {y-0.5}"/></g>')
def cup(x,y,c):
    return (f'<g fill="none" stroke="{c}" stroke-width="0.3" stroke-linejoin="round"><path d="M{x-2.3} {y-1.8}H{x+2.3}L{x+1.8} {y+2}H{x-1.8}Z"/>'
            f'<path d="M{x+2.15} {y-1}q1.6 0 1.4 1.3q-0.2 1 -1.65 0.9"/><path d="M{x-0.6} {y-2.6}q0.5 -0.6 0 -1.2M{x+0.6} {y-2.6}q0.5 -0.6 0 -1.2"/></g>')
def wrap(k,ml='500 ML'):
    s=C[k]; L=LOOK[k]; c=L['dark']; on=L['on']
    o=[f'<rect width="{W}" height="{H}" fill="{PAPER}"/>', f'<image href="file://{T}wart-{k}.png" width="{CX}" height="{H}" preserveAspectRatio="none"/>']
    # ---- colour side: story and how to use, set in the light ink
    x0,x1=7,57
    o.append(caps(f'{s["no"].upper()}  ·  {s["l1"].upper()} {s["l2"].upper()}  ·  {s["kind"]}',x0,8.2,1.5,L['on2'],tr=0.28))
    p,ye=para(s['story'],x0,13,x1-x0,2.05,2.8,on); o+=p
    y=ye+6.2
    o.append(caps('HOW TO USE',x0,y,1.5,L['on2'],tr=0.3)); y+=2.2
    use=s['rows'][3][1]; best=s['rows'][2][1]
    o+=[rule(x0,y,x1,y,on,0.2,0.5)]
    o+=[(cup if 'cup' in use else spoon)(x0+3.2,y+5.4,on), txt(use,x0+12.4,y+6.2,2.6,on,'IS'),
        rule(x0+26,y+1.6,x0+26,y+9.2,on,0.2,0.5), caps('BEST FOR',x0+28.5,y+4.2,1.4,L['on2'],tr=0.25), txt(best,x0+28.5,y+7.4,2.1,on)]
    y+=10.6; o.append(rule(x0,y,x1,y,on,0.2,0.5))
    o+=[caps('SPECIES',x0,y+4,1.4,L['on2'],tr=0.25), txt('Vanilla planifolia',x0,y+7.2,2.1,on),
        caps('ORIGIN',x0+28.5,y+4,1.4,L['on2'],tr=0.25), txt('Sri Lanka',x0+28.5,y+7.2,2.1,on)]
    o.append(txt('Savor the calm.',x0,H-5.2,4.4,on,'IS'))
    # ---- front card (the right half of the front)
    cx0,cx1=CX+5,CX+36; mx=(cx0+cx1)/2
    for (bx,by,dx,dy) in ((cx0,7,1,1),(cx1,7,-1,1),(cx0,63,1,-1),(cx1,63,-1,-1)):
        o.append(f'<path d="M{bx} {by+dy*3}V{by}H{bx+dx*3}" fill="none" stroke="{c}" stroke-width="0.3"/>')
    o+=[logo(mx,14.2,8.4,c), rule(cx0+4,21.6,cx1-4,21.6,c,0.2,0.6),
        txt(s['l1'],mx,33,12.4,c,'IS','middle'), txt(s['l2'],mx,43,12.4,c,'IS','middle'),
        caps(s['kind'],mx,48.6,1.85,L['deep'],'middle',0.3), rule(cx0+4,52.4,cx1-4,52.4,c,0.2,0.6),
        txt('Made with Ceylon vanilla' if k=='03' else 'Pure Ceylon vanilla',mx,56.4,2.1,c,'G','middle'), caps(ml,mx,60.6,1.8,c,'middle',0.3)]
    o.append(txt(s['no'],CX-4,64.2,6.4,LOOK['01']['on'] if k!='02' else '#FFF6E2','IS','end'))
    # ---- cream side: everything a shelf and a regulator need
    rx0,rx1=FX1+6,W-6; rw=rx1-rx0
    o+=[caps('NUTRITION  ·  PER TEASPOON, 5 ML',rx0,7,1.5,L['deep']), caps('% DV',rx1,7,1.35,L['deep'],'end')]
    y=8.4; o.append(rule(rx0,y,rx1,y,c,0.25,0.8))
    for name,amt,dv in NUTRITION:
        y+=2.7; ind=name.startswith('  ')
        o+=[txt(name.strip(),rx0+(2 if ind else 0),y,1.85,c), txt(amt,rx0+rw*0.62,y,1.85,c,'G','end'), txt(dv,rx1,y,1.85,c,'G','end')]
        o.append(rule(rx0,y+0.85,rx1,y+0.85,c,0.12,0.35))
    y=37.6
    for i,lab_ in enumerate(('USDA','EU','SGS')):
        cx=rx0+3.2+i*7.6; o+=[f'<circle cx="{cx}" cy="{y}" r="3" fill="none" stroke="{c}" stroke-width="0.2" stroke-dasharray="0.6 0.5" opacity="0.7"/>', caps(lab_,cx,y+0.5,1.15,c,'middle',0.1)]
    o+=[caps('PRODUCT OF SRI LANKA',rx1,y-1.1,1.35,L['deep'],'end'), txt(f'MRP Rs. {s["mrp"]}',rx1,y+2.6,2.3,c,'GB','end')]
    b,bw=ean13(s['ean'],rx0+1.2,44,0.25,8.6,'#1A120C'); o+=b
    bx=rx0+bw+5
    for i,kk in enumerate(('MFD','EXP','BATCH')):
        yy=45.6+i*3.6; o+=[caps(kk,bx,yy+1.6,1.3,L['deep'],tr=0.2), rule(bx+8.6,yy+2,rx1,yy+2,c,0.15,0.6)]
    y=58.2; o.append(caps('MANUFACTURED & MARKETED BY',rx0,y,1.25,L['deep'])); y+=2.6
    for i,l in enumerate(MAKER): o.append(txt(l,rx0,y+i*2.2,1.62,c,'GB' if i==0 else 'G'))
    return o
def save(o,name):
    s_=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W*20}" height="{H*20}" viewBox="0 0 {W} {H}">'+''.join(o)+'</svg>'
    open(T+name+'.html','w').write(f'<html><head><style>{css}html,body{{margin:0}}</style></head><body>{s_}</body></html>')
if __name__=='__main__':
    for k in ('01','02','03'):
        save(wrap(k),f'SW-{k}')
        for ml in ('100','200'): save(wrap(k,ml+' ML'),f'SW-{k}-{ml}')
    print('ok')
