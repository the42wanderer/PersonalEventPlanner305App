# Split, full wrap: colour half from the left panel to the bottle's centre, cream half from the centre round the right.
# Every fact comes from the labels now on sale (vanilla_labeels__final-01.pdf), with only the history line corrected;
# nothing is added that those labels don't carry. 200/100 ml sizes and prices are the only outside figures (see SIZES.md).
import sys; sys.path.insert(0,'../w')
from kit import width, logo, txt, caps, rule, para, ean13, css
from content import SKU as C, MAKER
T='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/ext/d/'
W,H,CX=226,70,113; FX1=153; PAPER='#F7EFDC'
# wrap length = pi x bottle diameter (226 = pi x 72); 200/100 ml diameters and heights are estimates, see SIZES.md
SIZE={'500':dict(W=226,H=70,D=72),'200':dict(W=166,H=42,D=53),'100':dict(W=132,H=35,D=42)}
C['03']=dict(no='No. 03',l1='Vanilla',l2='Syrup',kind='NATURAL SYRUP',ean='4796034220083',
             story=C['01']['story'].split(' Steeped')[0]+' Made into a syrup for sweet and savoury dishes.')
# "best for" is taken from each old label's own copy
BEST={'01':'Baking and desserts','02':'Desserts and beverages','03':'Sweet and savoury dishes'}
SHORT='Grown in the hills of Kandy, Matale and Nuwara Eliya, where every vanilla flower is pollinated by hand.'
TAIL={'01':' Steeped in alcohol for the fullest flavour.','02':' Made without alcohol, for a gentler, rounder vanilla.'}
# MRP: 500 ml from the old labels; 200 and 100 ml from the shop's product pages and Glomark (no old label to hand)
PRICE={'01':{'500':'20,000','200':'8,000','100':'4,100'},'02':{'500':'17,000','200':'6,900','100':'3,500'},'03':{'500':'12,500'}}
MFD,EXP='01/02/2025','31/01/2027'
# Sri Lanka's labelling regulations (in force 1 July 2026; research/label-text-rules.md): the common name in bold on the
# main panel in two languages, the third on any panel, each at least 3 mm high; the date of expiry in two languages.
# As on the tea boxes: English then Sinhala on the front card, Tamil on the colour side. Sizes are set so the letters
# without ascenders or descenders measure 3 mm (Noto Serif Sinhala Bold 0.59 em, Noto Serif Tamil Bold 0.57 em).
# The translations are ours: have a native Sinhala and Tamil reader check them on a printed proof.
NAME_SI={'01':'වැනිලා සාරය','02':'වැනිලා සාරය','03':'වැනිලා සිරප්'}
NAME_TA={'01':'வெனிலா சாறு','02':'வெனிலா சாறு','03':'வெனிலா சிரப்'}
SI,TA=5.2,5.3
# the batch fields in Sinhala and Tamil, word for word as on the Vanilla Tea pack on sale
DATE3=(('MFD','නි.දි.','பொ.செ திகதி'),('EXP','කා.ඉ.දි.','மு.திகதி'))
# the old labels' panel, the same on all three (its calories line has no figure, so it is left out)
NUT=[('Total fat','0 g','0%'),('  Saturated','0 g',''),('  Monounsaturated','0 g',''),('  Polyunsaturated','0 g',''),
     ('Cholesterol','0 mg','0%'),('Sodium','1 mg','0.04%'),('Total carbohydrate','0.5 g','0.2%'),('  Dietary fibre','0 g',''),
     ('  Sugars','0.5 g',''),('Protein','0 g','0%')]
PROOF=False
def mark(x,y,w,h,kind='e'):
    """proof only: magenta = still unknown, to confirm; cyan = from the listings, not the old labels, to check"""
    if not PROOF or not kind: return ''
    return f'<rect x="{x-0.5:.2f}" y="{y:.2f}" width="{w+1:.2f}" height="{h:.2f}" fill="{"#FF2BA6" if kind=="e" else "#12B5EA"}" opacity="0.32" rx="0.4"/>'
LOOK={'01':dict(dark='#4A120C',deep='#7E2414',on='#FBE7D2',on2='#F3B996'),
      '02':dict(dark='#4A2C08',deep='#8A5A10',on='#3B2108',on2='#5C3A0C'),
      '03':dict(dark='#16301C',deep='#1F3F24',on='#EAF2D6',on2='#B9D29C')}
def marks(x,y,d,gap):
    """the old labels' three marks, USDA Organic, SGS and the EU organic leaf, d mm high, left to right from x; returns the right edge"""
    o=[]
    for f,w in (('usda',d),('sgs',d),('eu',d*1.5)):
        o.append(f'<image href="file://{T}{f}.png" x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{d:.2f}" preserveAspectRatio="xMidYMid meet"/>'); x+=w+gap
    return o,x-gap
def facts(k,x0,x1,r1,rh,cz,fz,c1,c2):
    """two rows of facts on the colour side: species and origin, then what it's best for and that it's natural"""
    L=LOOK[k]; on=L['on']; o=[]
    for i,(a,av,b,bv) in enumerate((('SPECIES','Vanilla planifolia','ORIGIN','Sri Lanka'),('BEST FOR',BEST[k],'PRODUCT','100% natural'))):
        y=r1+i*rh; o+=[rule(x0,y,x1,y,on,0.2 if cz>1.2 else 0.18,0.5),
            caps(a,x0,y+c1,cz,L['on2'],tr=0.25 if cz>1.2 else 0.22), txt(av,x0,y+c2,fz,on),
            caps(b,x0+(x1-x0)*0.57,y+c1,cz,L['on2'],tr=0.25 if cz>1.2 else 0.22), txt(bv,x0+(x1-x0)*0.57,y+c2,fz,on)]
    return o
def front(k,cx,s,size):
    """the front card, right of the bottle's centre cx, at scale s of the 500 ml card; the net volume keeps its legal size"""
    st=C[k]; L=LOOK[k]; c=L['dark']; o=[]
    cx0,cx1=cx+5*s,cx+36*s; mx=(cx0+cx1)/2; a=3*s
    for (bx,by,dx,dy) in (() if size=='100' else ((cx0,7*s,1,1),(cx1,7*s,-1,1),(cx0,63*s,1,-1),(cx1,63*s,-1,-1))):   # 100 ml: no room for the corners
        o.append(f'<path d="M{bx:.2f} {by+dy*a:.2f}V{by:.2f}H{bx+dx*a:.2f}" fill="none" stroke="{c}" stroke-width="{max(0.3*s,0.22):.2f}"/>')
    if size=='500':
        # English, then the Sinhala name on its own line under it; the stack tightened to make room, the lower rule
        # given up so "Premium quality" and the volume keep their places
        o+=[logo(mx,13.4,7.8,c), rule(cx0+4,20.2,cx1-4,20.2,c,0.2,0.6),
            txt(st['l1'],mx,30.4,11.4,c,'IS','middle'), txt(st['l2'],mx,39.6,11.4,c,'IS','middle'),
            txt(NAME_SI[k],mx,46.6+(1.0 if k=='03' else 0),SI,c,'SiB','middle'),      # clear of Syrup's descenders
            caps(st['kind'],mx,51.8+(0.5 if k=='03' else 0),1.85,L['deep'],'middle',0.3)]
        o+=[txt('Premium quality',mx,55.6,2.0,c,'G','middle'), txt('500 ml',mx,61.4,5.4,c,'IS','middle')]
    else:
        # 200 and 100 ml: the Sinhala name cannot shrink with the label (3 mm is the floor), so it is stacked in two
        # lines under the English, the English set at its own 3 mm floor (Instrument Serif x-height 0.51 em);
        # "Premium quality" and the rules give way. The logo stays on the 200 ml card; on the 100 ml it moves to
        # the colour side.
        w1,w2=NAME_SI[k].split(' ')
        y={'200':dict(lg=6.9,v=14.0,e=19.2,s1=25.0,s2=30.7,kd=33.7,ml=37.6),
           '100':dict(lg=None,v=8.1,e=13.3,s1=19.0,s2=24.7,kd=27.7,ml=31.9)}[size]
        if y['lg']: o.append(logo(mx,y['lg'],3.8,c))
        o+=[txt(st['l1'],mx,y['v'],6.2,c,'IS','middle'), txt(st['l2'],mx,y['e'],6.2,c,'IS','middle'),
            txt(w1,mx,y['s1'],SI,c,'SiB','middle'), txt(w2,mx,y['s2'],SI,c,'SiB','middle'),
            caps(st['kind'],mx,y['kd'],1.2,L['deep'],'middle',0.22), txt(f'{size} ml',mx,y['ml'],4.0,c,'IS','middle')]
    o.append(txt(st['no'],cx-4*s,64.2*s,6.4*s,LOOK['01']['on'] if k!='02' else '#FFF6E2','IS','end'))
    return o
def dates3(x,y,lead,sub,cz,fz,zs,zt,c,deep,vx):
    """MFD and EXP, the dates in bold at the Schedule II height (figures 1.5 mm), each field labelled in English on
    its line and in Sinhala and Tamil underneath"""
    o=[]
    for i,((en,si,ta),v) in enumerate(zip(DATE3,(MFD,EXP))):
        yy=y+i*lead
        o+=[caps(en,x,yy,cz,deep,tr=0.2), txt(v,x+vx,yy,fz,c,'GB'),
            txt(si,x,yy+sub,zs,deep,'SiS'), txt(ta,x+width(si,'SiS',zs)+1.2,yy+sub,zt,deep,'TaS')]
    return o
def dates(x,y,lead,cz,fz,c,deep,vx):
    o=[]
    for i,(kk,v) in enumerate((('MFD',MFD),('EXP',EXP))):
        yy=y+i*lead; o+=[caps(kk,x,yy,cz,deep,tr=0.2), txt(v,x+vx,yy,fz,c)]
    return o
def wrap(k,size='500'):
    """the 500 ml wrap, on the original template"""
    s=C[k]; L=LOOK[k]; c=L['dark']; on=L['on']
    o=[f'<rect width="{W}" height="{H}" fill="{PAPER}"/>', f'<image href="file://{T}wart-{k}.png" width="{CX}" height="{H}" preserveAspectRatio="none"/>']
    # ---- colour side: brand line, story, the facts
    x0,x1=7,57
    o.append(txt('Savor the calm.',x0,10.6,4.4,on,'IS'))
    p,ye=para(s['story'],x0,16.6,x1-x0,2.15,2.95,on); o+=p
    o.append(txt(NAME_TA[k],x0,44.0,TA,on,'TaB'))                      # the name in Tamil, the third language
    o+=facts(k,x0,x1,48.8,9.4,1.35,2.0,3.7,6.9)
    o+=front(k,CX,1,'500')
    # ---- cream side: nutrition, marks, price, barcode, dates, maker
    rx0,rx1=FX1+6,W-6; rw=rx1-rx0
    o+=[caps('NUTRITION  ·  PER TEASPOON',rx0,7,1.5,L['deep']), caps('% DV',rx1,7,1.35,L['deep'],'end')]
    y=8.4; o.append(rule(rx0,y,rx1,y,c,0.25,0.8))
    for name,amt,dv in NUT:
        y+=2.5; ind=name.startswith('  ')
        o+=[txt(name.strip(),rx0+(2 if ind else 0),y,1.8,c), txt(amt,rx0+rw*0.62,y,1.8,c,'G','end'), txt(dv,rx1,y,1.8,c,'G','end'),
            rule(rx0,y+0.8,rx1,y+0.8,c,0.12,0.35)]
    m,_=marks(rx0,35.6,5.6,1.8); o+=m
    mrp=f'MRP Rs. {PRICE[k]["500"]}'
    o+=[caps('PRODUCT OF SRI LANKA',rx1,37.3,1.35,L['deep'],'end'), txt(mrp,rx1,41.0,2.3,c,'GB','end')]
    b,bw=ean13(s['ean'],rx0+1.2,44,0.25,8.6,'#1A120C'); o+=b
    o+=dates3(rx0+bw+5,46.4,6.0,2.9,1.3,2.2,2.0,1.8,c,L['deep'],7.4)
    y=58.2; o.append(caps('MANUFACTURED & MARKETED BY',rx0,y,1.25,L['deep'])); y+=2.6
    for i,l in enumerate(MAKER): o.append(txt(l,rx0,y+i*2.2,1.62,c,'GB' if i==0 else 'G'))
    return o
def linear(rows):
    """the panel as one running line, for the 100 ml: 'Fat 0 g (saturated 0 g, ...) · ...'"""
    nm={'Total fat':'Fat','Total carbohydrate':'Carbohydrate','Dietary fibre':'fibre'}
    g=[]
    for n,a,_ in rows:
        t=f'{nm.get(n.strip(),n.strip())} {a}'
        if n.startswith('  '): g[-1][1].append(t[0].lower()+t[1:])
        else: g.append((t,[]))
    return ' · '.join(t+(f' ({", ".join(sub)})' if sub else '') for t,sub in g)
def wrap_small(k,size):
    """200 and 100 ml: the same parts re-set for a shorter, narrower label; type stays at a readable size"""
    st=C[k]; L=LOOK[k]; c=L['dark']; on=L['on']; Z=SIZE[size]; w,h=Z['W'],Z['H']; cx=w/2; s=h/70
    big=size=='200'
    o=[f'<rect width="{w}" height="{h}" fill="{PAPER}"/>', f'<image href="file://{T}wart-{k}-{size}.png" width="{cx}" height="{h}" preserveAspectRatio="none"/>']
    # ---- colour side
    x0,x1=(4.5,46) if big else (4,37)
    if big:
        o.append(txt('Savor the calm.',x0,6.6,3.0,on,'IS'))
        p,ye=para(SHORT+TAIL.get(k,''),x0,10.4,x1-x0,1.55,2.1,on); o+=p
        o.append(txt(NAME_TA[k],x0,21.0,TA,on,'TaB'))                     # the name in Tamil, one line
    else:
        # the logo comes over from the front card; the Tamil name, stacked, takes the story's place
        o+=[logo(x0+3.2,5.0,5.6,on), txt('Savor the calm.',x0+8.4,6.6,2.5,on,'IS')]
        t1,t2=NAME_TA[k].split(' ')
        o+=[txt(t1,x0,12.0,TA,on,'TaB'), txt(t2,x0,17.4,TA,on,'TaB')]
    o+=facts(k,x0,x1,24.6,7.2,1.05,1.5,2.9,5.5) if big else facts(k,x0,x1,19.6,6.6,0.95,1.3,2.6,5.0)
    o+=front(k,cx,s,size)
    # ---- cream side
    mrp=f'MRP Rs. {PRICE[k][size]}'
    if big:
        rx0,rx1=111,162; ax1=135.5
        o+=[caps('NUTRITION',rx0,5.6,1.05,L['deep'],tr=0.2), txt('PER TSP',ax1,5.6,1.15,L['deep'],'G','end')]
        y=6.6; o.append(rule(rx0,y,ax1,y,c,0.22,0.8)); y+=0.15
        for name,amt,dv in NUT:
            y+=2.15; ind=name.startswith('  '); nm=name.strip().replace('Total carbohydrate','Carbohydrate')
            o+=[txt(nm,rx0+(1.2 if ind else 0),y,1.35,c), txt(amt,rx0+18.6,y,1.35,c,'G','end'), txt(dv,ax1,y,1.35,c,'G','end'),
                rule(rx0,y+0.62,ax1,y+0.62,c,0.1,0.35)]
        bx0=139
        o+=[mark(rx1-width(mrp,'GB',1.8),4.2,width(mrp,'GB',1.8),1.9,'c'), txt(mrp,rx1,5.6,1.8,c,'GB','end')]
        b,bw=ean13(st['ean'],bx0+1.5,7.6,0.22,6.0,'#1A120C'); o+=[mark(bx0+0.3,6.6,bw+2.5,10.4)]+b
        o+=dates3(bx0,19.4,4.6,2.1,0.95,1.9,1.7,1.5,c,L['deep'],5.2)
        m,_=marks(bx0,27.4,3.6,1.1); o+=m
        y=32.2; o+=[caps('MANUFACTURED & MARKETED BY',rx0,y,0.95,L['deep'],tr=0.2), caps('PRODUCT OF SRI LANKA',rx1,y,0.95,L['deep'],'end',0.2)]
        for i,l in enumerate(MAKER): o.append(txt(l,rx0,y+2.2+i*1.7,1.3,c,'GB' if i==0 else 'G'))
    else:
        rx0,ax1,rx1=88.5,114,128
        o.append(caps('NUTRITION  ·  PER TSP',rx0,4.6,0.9,L['deep'],tr=0.18))
        pl,yl=para(linear(NUT),rx0,6.7,ax1-rx0,1.15,1.5,c); o+=pl
        y=yl+1.6; o.append(rule(rx0,y,ax1,y,c,0.18,0.6))
        o+=[mark(rx0,y+1.1,width(mrp,'GB',1.55),1.7,'c'), txt(mrp,rx0,y+2.5,1.55,c,'GB')]
        o+=dates3(rx0,y+5.6,4.5,2.0,0.85,1.9,1.6,1.4,c,L['deep'],4.6)
        m,_=marks(rx0+16.2,y+5.0,2.6,0.6); o+=m
        y+=13.7
        mk=['Made by '+MAKER[0],'Level 26, East Tower, World Trade Center,','Echelon Square, Colombo, Sri Lanka','www.agroventuresexports.com','+94 11 287 8766']
        for i,l in enumerate(mk): o.append(txt(l,rx0,y+i*1.42,1.15,c,'GB' if i==0 else 'G'))
        # barcode in ladder orientation (bars across the bottle's axis), so it does not wrap round a 42 mm bottle
        b,bw=ean13(st['ean'],0,0,0.22,6.6,'#1A120C')
        o+=[mark(117,3.6,9.6,25.2),f'<g transform="translate(118.6 28.2) rotate(-90)">'+''.join(b)+'</g>']
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
