# Split, full wrap: colour half from the left panel to the bottle's centre, cream half from the centre round the right.
# 500 ml is the original 226 x 70 mm template; 200 and 100 ml are laid out for their own bottles (see SIZES.md).
import sys; sys.path.insert(0,'../w')
from kit import width, logo, txt, caps, rule, para, ean13, css
from content import SKU as C, MAKER
T='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/ext/d/'
W,H,CX=226,70,113; FX1=153; PAPER='#F7EFDC'
# wrap length = pi x bottle diameter (226 = pi x 72); 200/100 ml diameters and heights are estimates, see SIZES.md
SIZE={'500':dict(W=226,H=70,D=72),'200':dict(W=166,H=42,D=53),'100':dict(W=132,H=35,D=42)}
C['03']=dict(no='No. 03',l1='Vanilla',l2='Syrup',kind='NATURAL SYRUP',ean='4796034220083',mrp='12,500',
             story=C['01']['story'].split(' Steeped')[0]+' Made into a syrup for coffee, shakes and desserts.',
             rows=[('SPECIES','Vanilla planifolia'),('ORIGIN','Sri Lanka'),('BEST FOR','Coffee and shakes'),('USE','2 tsp per cup')])
SHORT='Grown in the hills of Kandy, Matale and Nuwara Eliya, where every vanilla flower is pollinated by hand.'
TAIL={'01':' Steeped in alcohol for the fullest flavour.','02':' Made without alcohol, for a gentler, rounder vanilla.'}
# prices: thevanillashop.lk and Glomark (100 ml); the syrup is sold in 500 ml only
PRICE={'01':{'500':'20,100','200':'8,000','100':'4,100'},'02':{'500':'17,000','200':'6,900','100':'3,500'},'03':{'500':'12,500'}}
# ingredients: the shop's own product pages (order still to be checked against the recipe); syrup is an estimate
EXTRA={'01':dict(ingr='Food-grade alcohol, natural vanilla bean extractives, purified water.',ingr_m='c',
                 store='Keep closed, cool and dark. Shake before use.',abv='35% VOL'),
       '02':dict(ingr='Purified water, vegetable glycerine, natural vanilla bean extractives.',ingr_m='c',
                 store='Keep closed, cool and dark. Shake before use.',abv=None),
       '03':dict(ingr='Cane sugar, purified water, natural vanilla extract, citric acid.',ingr_m='e',
                 store='Keep cool and dry. Refrigerate after opening.',abv=None)}
# nutrition: the current label's figures (USDA vanilla extract) plus energy worked out in SIZES.md.
# mark: 'c' = calculated or from the shop's listings (check), 'e' = estimate (confirm with production or a lab)
_ext=[('Energy','12 kcal','','c'),('Total fat','0 g','0%',''),('  Saturated','0 g','',''),('Cholesterol','0 mg','0%',''),
      ('Sodium','1 mg','0.04%',''),('Total carbohydrate','0.5 g','0.2%',''),('  Dietary fibre','0 g','',''),('  Sugars','0.5 g','',''),('Protein','0 g','0%','')]
NUT={'01':('PER TEASPOON, 5 ML','PER TSP, 5 ML',_ext),
     '02':('PER TEASPOON, 5 ML','PER TSP, 5 ML',[('Energy','6 kcal','','e')]+_ext[1:5]+[('Total carbohydrate','1.5 g','0.5%','e')]+_ext[6:8]+
           [('  Glycerine','1 g','','e'),_ext[8]]),
     '03':('PER 2 TEASPOONS, 10 ML','PER 2 TSP, 10 ML',[('Energy','31 kcal','','e'),('Total fat','0 g','0%','e'),('  Saturated','0 g','','e'),
           ('Cholesterol','0 mg','0%','e'),('Sodium','0 mg','0%','e'),('Total carbohydrate','8 g','3%','e'),('  Dietary fibre','0 g','','e'),
           ('  Sugars','8 g','','e'),('Protein','0 g','0%','e')])}
PROOF=False
def mark(x,y,w,h,kind='e'):
    """proof only: magenta = estimate or unknown, to confirm; cyan = calculated or taken from the listings, to check"""
    if not PROOF or not kind: return ''
    return f'<rect x="{x-0.5:.2f}" y="{y:.2f}" width="{w+1:.2f}" height="{h:.2f}" fill="{"#FF2BA6" if kind=="e" else "#12B5EA"}" opacity="0.32" rx="0.4"/>'
def tbc(x,y,w,h): return mark(x,y,w,h,'e')
LOOK={'01':dict(dark='#4A120C',deep='#7E2414',on='#FBE7D2',on2='#F3B996'),
      '02':dict(dark='#4A2C08',deep='#8A5A10',on='#3B2108',on2='#5C3A0C'),
      '03':dict(dark='#16301C',deep='#1F3F24',on='#EAF2D6',on2='#B9D29C')}
def spoon(x,y,c):
    return (f'<g fill="none" stroke="{c}" stroke-width="0.3" stroke-linecap="round"><ellipse cx="{x}" cy="{y}" rx="1.9" ry="1.25"/>'
            f'<path d="M{x+1.9} {y}L{x+7.2} {y-0.5}"/></g>')
def cup(x,y,c):
    return (f'<g fill="none" stroke="{c}" stroke-width="0.3" stroke-linejoin="round"><path d="M{x-2.3} {y-1.8}H{x+2.3}L{x+1.8} {y+2}H{x-1.8}Z"/>'
            f'<path d="M{x+2.15} {y-1}q1.6 0 1.4 1.3q-0.2 1 -1.65 0.9"/><path d="M{x-0.6} {y-2.6}q0.5 -0.6 0 -1.2M{x+0.6} {y-2.6}q0.5 -0.6 0 -1.2"/></g>')
def icon(use,x,y,c,f=1):
    g=(cup if 'cup' in use else spoon)(x,y,c)
    return g if f==1 else f'<g transform="translate({x} {y}) scale({f}) translate({-x} {-y})">{g}</g>'
def front(k,cx,s,size):
    """the front card, right of the bottle's centre cx, at scale s of the 500 ml card; the net volume keeps its legal size"""
    st=C[k]; L=LOOK[k]; c=L['dark']; e=EXTRA[k]; o=[]
    cx0,cx1=cx+5*s,cx+36*s; mx=(cx0+cx1)/2; a=3*s
    for (bx,by,dx,dy) in ((cx0,7*s,1,1),(cx1,7*s,-1,1),(cx0,63*s,1,-1),(cx1,63*s,-1,-1)):
        o.append(f'<path d="M{bx:.2f} {by+dy*a:.2f}V{by:.2f}H{bx+dx*a:.2f}" fill="none" stroke="{c}" stroke-width="{max(0.3*s,0.22):.2f}"/>')
    o+=[logo(mx,14.2*s,8.4*s,c), rule(cx0+4*s,21.6*s,cx1-4*s,21.6*s,c,0.2,0.6),
        txt(st['l1'],mx,33*s,12.4*s,c,'IS','middle'), txt(st['l2'],mx,43*s,12.4*s,c,'IS','middle'),
        caps(st['kind'],mx,48.6*s,max(1.85*s,1.2),L['deep'],'middle',0.3 if s==1 else 0.22), rule(cx0+4*s,51.4*s,cx1-4*s,51.4*s,c,0.2,0.6)]
    # tagline, then the net volume: numerals at least 4 mm high on 500 ml, 3 mm on 200 and 100 ml
    ty,ny,ns,ts={'500':(55.2,61.4,5.4,2.0),'200':(33.1,37.3,4.0,1.35),'100':(27.8,31.7,4.0,1.3)}[size]
    tag='Made with Ceylon vanilla' if k=='03' else 'Pure Ceylon vanilla'
    if e['abv']:
        abv=' · '+e['abv'].replace('VOL','vol'); wt=width(tag+abv,'G',ts); wa=width(abv[3:],'G',ts)
        o+=[mark(mx+wt/2-wa,ty-ts*0.85,wa,ts*1.15), txt(tag+abv,mx,ty,ts,c,'G','middle')]
    else: o.append(txt(tag,mx,ty,ts,c,'G','middle'))
    o.append(txt(f'{size} ml',mx,ny,ns,c,'IS','middle'))
    o.append(txt(st['no'],cx-4*s,64.2*s,6.4*s,LOOK['01']['on'] if k!='02' else '#FFF6E2','IS','end'))
    return o
def wrap(k,size='500'):
    """the 500 ml wrap, on the original 226 x 70 mm template"""
    s=C[k]; L=LOOK[k]; c=L['dark']; on=L['on']
    o=[f'<rect width="{W}" height="{H}" fill="{PAPER}"/>', f'<image href="file://{T}wart-{k}.png" width="{CX}" height="{H}" preserveAspectRatio="none"/>']
    # ---- colour side: brand line, story, how to use, the facts
    e=EXTRA[k]; x0,x1=7,57
    o.append(txt('Savor the calm.',x0,10.6,4.4,on,'IS'))
    p,ye=para(s['story'],x0,16.4,x1-x0,2.0,2.75,on); o+=p
    y=ye+4.8
    o.append(caps('HOW TO USE',x0,y,1.45,L['on2'],tr=0.3)); y+=2
    use=s['rows'][3][1]; best=s['rows'][2][1]
    o+=[rule(x0,y,x1,y,on,0.2,0.5)]
    o+=[tbc(x0+12,y+3.9,width(use,'IS',2.6),3.2),icon(use,x0+3.2,y+5.2,on), txt(use,x0+12.4,y+6.0,2.6,on,'IS'),
        rule(x0+26,y+1.5,x0+26,y+8.8,on,0.2,0.5), caps('BEST FOR',x0+28.5,y+4.0,1.35,L['on2'],tr=0.25), txt(best,x0+28.5,y+7.1,2.0,on)]
    y+=9.6; o.append(rule(x0,y,x1,y,on,0.2,0.5))
    o+=[caps('SPECIES',x0,y+3.6,1.35,L['on2'],tr=0.25), txt('Vanilla planifolia',x0,y+6.6,2.0,on),
        caps('ORIGIN',x0+28.5,y+3.6,1.35,L['on2'],tr=0.25), txt('Sri Lanka',x0+28.5,y+6.6,2.0,on)]
    y+=8.6; o.append(rule(x0,y,x1,y,on,0.2,0.5))
    o.append(caps('INGREDIENTS',x0,y+3.6,1.35,L['on2'],tr=0.25))
    pi,yi=para(e['ingr'],x0,y+6.4,24.5,1.75,2.3,on); o+=[mark(x0,y+4.9,24.5,yi-y-4.9+0.9,e['ingr_m'])]+pi
    o.append(caps('STORAGE',x0+28.5,y+3.6,1.35,L['on2'],tr=0.25))
    ps_,ys=para(e['store'],x0+28.5,y+6.4,x1-x0-28.5,1.75,2.3,on); o+=ps_
    o+=front(k,CX,1,'500')
    # ---- cream side: everything a shelf and a regulator need
    rx0,rx1=FX1+6,W-6; rw=rx1-rx0; per,_,rows=NUT[k]
    o+=[caps('NUTRITION  ·  '+per,rx0,7,1.5,L['deep'],tr=0.28 if len(per)<20 else 0.2), caps('% DV',rx1,7,1.35,L['deep'],'end')]
    y=8.4; o.append(rule(rx0,y,rx1,y,c,0.25,0.8)); step=2.7 if len(rows)<10 else 2.5
    for name,amt,dv,m in rows:
        y+=step; ind=name.startswith('  ')
        o.append(mark(rx0+rw*0.62-6,y-1.75,6,2.3,m))
        o+=[txt(name.strip(),rx0+(2 if ind else 0),y,1.85,c), txt(amt,rx0+rw*0.62,y,1.85,c,'G','end'), txt(dv,rx1,y,1.85,c,'G','end')]
        o.append(rule(rx0,y+0.85,rx1,y+0.85,c,0.12,0.35))
    y=38.0
    for i,lab_ in enumerate(('USDA','EU','SGS')):
        cx=rx0+3.2+i*7.6; o+=[tbc(cx-3.1,y-3.1,6.2,6.2),f'<circle cx="{cx}" cy="{y}" r="3" fill="none" stroke="{c}" stroke-width="0.2" stroke-dasharray="0.6 0.5" opacity="0.7"/>', caps(lab_,cx,y+0.5,1.15,c,'middle',0.1)]
    mrp=f'MRP Rs. {PRICE[k]["500"]}'; o+=[caps('PRODUCT OF SRI LANKA',rx1,y-1.1,1.35,L['deep'],'end'), mark(rx1-width(mrp,'GB',2.3),y+0.8,width(mrp,'GB',2.3),2.4,'c'), txt(mrp,rx1,y+2.6,2.3,c,'GB','end')]
    b,bw=ean13(s['ean'],rx0+1.2,44,0.25,8.6,'#1A120C'); o+=b
    bx=rx0+bw+5
    for i,kk in enumerate(('MFD','EXP','BATCH')):
        yy=45.6+i*3.6; o+=[caps(kk,bx,yy+1.6,1.3,L['deep'],tr=0.2), rule(bx+8.6,yy+2,rx1,yy+2,c,0.15,0.6)]
    y=58.2; o.append(caps('MANUFACTURED & MARKETED BY',rx0,y,1.25,L['deep'])); y+=2.6
    for i,l in enumerate(MAKER): o.append(txt(l,rx0,y+i*2.2,1.62,c,'GB' if i==0 else 'G'))
    return o
def linear(rows):
    """the panel as one running line, for the 100 ml: 'Fat 0 g (saturated fat 0 g) · ...'"""
    nm={'Total fat':'Fat','Saturated':'saturated fat','Total carbohydrate':'Carbohydrate','Dietary fibre':'fibre'}
    g=[]
    for n,a,_,_ in rows:
        t=f'{nm.get(n.strip(),n.strip())} {a}'
        if n.startswith('  '): g[-1][1].append(t[0].lower()+t[1:])
        else: g.append((t,[]))
    return ' · '.join(t+(f' ({", ".join(sub)})' if sub else '') for t,sub in g)
def wrap_small(k,size):
    """200 and 100 ml: the same parts re-set for a shorter, narrower label; type stays at a readable size"""
    st=C[k]; L=LOOK[k]; c=L['dark']; on=L['on']; e=EXTRA[k]; Z=SIZE[size]; w,h=Z['W'],Z['H']; cx=w/2; s=h/70
    big=size=='200'
    o=[f'<rect width="{w}" height="{h}" fill="{PAPER}"/>', f'<image href="file://{T}wart-{k}-{size}.png" width="{cx}" height="{h}" preserveAspectRatio="none"/>']
    # ---- colour side
    x0,x1=(4.5,46) if big else (4,37)
    o.append(txt('Savor the calm.',x0,6.6 if big else 5.6,3.0 if big else 2.5,on,'IS'))
    fs,ld=(1.5,2.05) if big else (1.3,1.75)
    p,ye=para(SHORT+(TAIL.get(k,'') if big else ''),x0,10.2 if big else 8.6,x1-x0,fs,ld,on); o+=p
    y=ye+(2.4 if big else 2.2); o.append(rule(x0,y,x1,y,on,0.18,0.5))
    use=st['rows'][3][1]; best=st['rows'][2][1]
    if big:
        o+=[tbc(x0+8.8,y+2.9,width(use,'IS',2.1),2.6), icon(use,x0+2.6,y+3.7,on,0.8), txt(use,x0+9,y+4.6,2.1,on,'IS'),
            rule(x0+21,y+1.2,x0+21,y+6.2,on,0.18,0.5), caps('BEST FOR',x0+23,y+3.0,1.05,L['on2'],tr=0.22), txt(best,x0+23,y+5.6,1.5,on)]
        y+=7.4
    else:
        o+=[tbc(x0+7.3,y+2.6,width(use,'IS',1.8),2.3), icon(use,x0+2.2,y+3.3,on,0.65), txt(use,x0+7.5,y+4.1,1.8,on,'IS'),
            rule(x0+17,y+1.1,x0+17,y+5.4,on,0.18,0.5), caps('BEST FOR',x0+19,y+2.7,0.95,L['on2'],tr=0.2), txt(best,x0+19,y+5.0,1.3,on)]
        y+=6.4
    o.append(rule(x0,y,x1,y,on,0.18,0.5))
    cw,c2=(19.5,22) if big else (15.5,17)
    cz,fz,lz=(1.05,1.4,1.85) if big else (0.95,1.25,1.65)
    o+=[caps('INGREDIENTS',x0,y+2.8,cz,L['on2'],tr=0.22), caps('STORAGE',x0+c2,y+2.8,cz,L['on2'],tr=0.22)]
    pi,yi=para(e['ingr'],x0,y+5.0,cw,fz,lz,on); o+=[mark(x0,y+3.8,cw,yi-y-3.8+0.7,e['ingr_m'])]+pi
    ps_,_=para(e['store'],x0+c2,y+5.0,x1-x0-c2,fz,lz,on); o+=ps_
    o+=front(k,cx,s,size)
    # ---- cream side
    per=NUT[k][1]; rows=NUT[k][2]; mrp=f'MRP Rs. {PRICE[k][size]}'
    if big:
        rx0,rx1=111,162; ax1=135.5
        o+=[caps('NUTRITION',rx0,5.6,1.05,L['deep'],tr=0.2), txt(per,ax1,5.6,1.15,L['deep'],'G','end')]
        y=6.6; o.append(rule(rx0,y,ax1,y,c,0.22,0.8)); y+=0.15; step=2.15 if len(rows)>9 else 2.25
        for name,amt,dv,m in rows:
            y+=step; ind=name.startswith('  '); nm=name.strip().replace('Total carbohydrate','Carbohydrate')
            o+=[mark(rx0+14.6,y-1.3,4.2,1.75,m), txt(nm,rx0+(1.2 if ind else 0),y,1.4,c), txt(amt,rx0+18.6,y,1.4,c,'G','end'), txt(dv,ax1,y,1.4,c,'G','end'),
                rule(rx0,y+0.62,ax1,y+0.62,c,0.1,0.35)]
        bx0=139
        o+=[mark(rx1-width(mrp,'GB',1.8),4.2,width(mrp,'GB',1.8),1.9,'c'), txt(mrp,rx1,5.6,1.8,c,'GB','end')]
        b,bw=ean13(st['ean'],bx0+1.5,7.6,0.22,6.0,'#1A120C'); o+=[tbc(bx0+0.3,6.6,bw+2.5,10.4)]+b
        for i,kk in enumerate(('MFD','EXP','BATCH')):
            yy=18.6+i*2.75; o+=[caps(kk,bx0,yy,0.95,L['deep'],tr=0.2), rule(bx0+6.4,yy+0.3,rx1,yy+0.3,c,0.13,0.6)]
        for i,lab_ in enumerate(('USDA','EU','SGS')):
            ccx=bx0+2.1+i*5.0; o+=[tbc(ccx-2.1,25.9,4.2,4.2),f'<circle cx="{ccx}" cy="28" r="2.0" fill="none" stroke="{c}" stroke-width="0.16" stroke-dasharray="0.45 0.4" opacity="0.7"/>', caps(lab_,ccx,28.3,0.8,c,'middle',0.1)]
        y=32.2; o+=[caps('MANUFACTURED & MARKETED BY',rx0,y,0.95,L['deep'],tr=0.2), caps('PRODUCT OF SRI LANKA',rx1,y,0.95,L['deep'],'end',0.2)]
        for i,l in enumerate(MAKER): o.append(txt(l,rx0,y+2.2+i*1.7,1.3,c,'GB' if i==0 else 'G'))
    else:
        rx0,ax1,rx1=88.5,114,128
        o.append(caps('NUTRITION  ·  '+per,rx0,4.6,0.9,L['deep'],tr=0.18))
        lin=linear(rows)
        pl,yl=para(lin,rx0,6.7,ax1-rx0,1.15,1.5,c); o+=[mark(rx0,5.6,ax1-rx0,yl-5.6+0.6,'e' if k=='03' else 'c')]+pl
        y=yl+1.6; o.append(rule(rx0,y,ax1,y,c,0.18,0.6))
        o+=[mark(rx0,y+1.1,width(mrp,'GB',1.55),1.7,'c'), txt(mrp,rx0,y+2.5,1.55,c,'GB')]
        for i,kk in enumerate(('MFD','EXP','BATCH')):
            yy=y+5.0+i*2.4; o+=[caps(kk,rx0,yy,0.85,L['deep'],tr=0.18), rule(rx0+5.6,yy+0.3,rx0+13,yy+0.3,c,0.12,0.6)]
        for i,lab_ in enumerate(('USDA','EU','SGS')):
            ccx=rx0+16.6+i*3.8; o+=[tbc(ccx-1.75,y+5.6,3.5,3.5),f'<circle cx="{ccx:.2f}" cy="{y+7.35:.2f}" r="1.7" fill="none" stroke="{c}" stroke-width="0.14" stroke-dasharray="0.4 0.35" opacity="0.7"/>', caps(lab_,ccx,y+7.6,0.68,c,'middle',0.05)]
        y+=12.6
        mk=['Made by '+MAKER[0],'Level 26, East Tower, World Trade Center,','Echelon Square, Colombo, Sri Lanka','www.agroventuresexports.com','+94 11 287 8766']
        for i,l in enumerate(mk): o.append(txt(l,rx0,y+i*1.45,1.15,c,'GB' if i==0 else 'G'))
        # barcode in ladder orientation (bars across the bottle's axis), so it does not wrap round a 42 mm bottle
        b,bw=ean13(st['ean'],0,0,0.22,6.6,'#1A120C')
        o+=[tbc(117,3.6,9.6,25.2),f'<g transform="translate(118.6 28.2) rotate(-90)">'+''.join(b)+'</g>']
    return o
def save(o,name,w=W,h=H):
    s_=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w*20}" height="{h*20}" viewBox="0 0 {w} {h}">'+''.join(o)+'</svg>'
    open(T+name+'.html','w').write(f'<html><head><style>{css}html,body{{margin:0}}</style></head><body>{s_}</body></html>')
def small_art(k,size):
    """the 500 ml colour art scaled to the label height, set against the bottle's centre; the plain ground is reflected to fill"""
    from PIL import Image, ImageOps
    Z=SIZE[size]; s=Z['H']/70; im=Image.open(T+f'wart-{k}.png').convert('RGB')
    wpx,hpx=round(113*s*20),round(Z['H']*20); im=im.resize((wpx,hpx),Image.LANCZOS)
    full=round(Z['W']/2*20); pad=full-wpx; out=Image.new('RGB',(full,hpx))
    strip=ImageOps.mirror(im.crop((0,0,pad,hpx))); out.paste(strip,(0,0)); out.paste(im,(pad,0)); out.save(T+f'wart-{k}-{size}.png')
if __name__=='__main__':
    PROOF='proof' in sys.argv
    for k in ('01','02','03'):
        save(wrap(k),('PR-' if PROOF else 'SW-')+k)
        for size in PRICE[k]:
            if size=='500': continue
            small_art(k,size); Z=SIZE[size]; save(wrap_small(k,size),('PR-' if PROOF else 'SW-')+f'{k}-{size}',Z['W'],Z['H'])
    print('ok')
