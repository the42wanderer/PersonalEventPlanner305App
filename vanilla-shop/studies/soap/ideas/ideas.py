# Rough soap-box concepts as 3D box boards (CSS 3D, faces drawn as SVG in mm). Rough on purpose: idea, not finish.
import math, random
R='/home/user/PersonalEventPlanner305App/vanilla-shop'
S='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad'
O=S+'/soap/ideas/'
FONT={'IS':R+'/fonts/instrument-serif-italic.ttf','ISR':R+'/fonts/instrument-serif.ttf','G':R+'/fonts/geist-regular.ttf','GB':R+'/fonts/geist-bold.ttf',
      'AX':S+'/dlfont/archivo-x-black.ttf','AC':S+'/dlfont/archivo-c-black.ttf','AE':R+'/fonts/archivo-expanded-regular.ttf',
      'MK':S+'/dlfont/marker.ttf','CV':S+'/dlfont/caveat.ttf'}
CSS=''.join(f"@font-face{{font-family:{k};src:url(file://{v})}}" for k,v in FONT.items())
W,H,D=136,81,28              # box front w x h, depth (mm)
V={'vanilla':dict(name='Vanilla',sub='BATHING BAR',bg='#E7A93E',dk='#4A2C08',lt='#FBEBC4'),
   'rosette':dict(name='Rosette',sub='VANILLA & ROSE',bg='#E9899C',dk='#5A1426',lt='#FBE0E5'),
   'ebony':dict(name='Ebony & Amber',sub='CHARCOAL & VANILLA',bg='#262220',dk='#E0A048',lt='#F3D9A8'),
   'aloe':dict(name='Aloe Vera',sub='VANILLA & ALOE',bg='#4F8A55',dk='#16301C',lt='#E4F0CF')}
ORDER=['vanilla','rosette','ebony','aloe']
def svg(w,h,body,defs=''):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="100%" preserveAspectRatio="none"><defs>{defs}</defs>{body}</svg>'
def t(x,y,s,txt,f='G',c='#000',a='start',tr=0,extra=''):
    return f'<text x="{x}" y="{y}" font-family="{f}" font-size="{s}" fill="{c}" text-anchor="{a}" letter-spacing="{tr}" {extra}>{txt}</text>'
KRAFT=('<filter id="kr"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" seed="4"/>'
       '<feColorMatrix values="0 0 0 0 0.45  0 0 0 0 0.32  0 0 0 0 0.18  0 0 0 0.35 0"/><feComposite in2="SourceGraphic" operator="in"/></filter>')
def kraft(w,h,c='#C59F72'): return f'<rect width="{w}" height="{h}" fill="{c}"/><rect width="{w}" height="{h}" fill="{c}" filter="url(#kr)"/>'
def box(front,top,side,s=3.0,ry=-32,rx=-18,w=W,h=H,d=D):
    """one box, returned as an absolutely positionable div (centre-anchored)"""
    W_,H_,D_=w*s,h*s,d*s
    f=lambda inner,ww,hh,tr,shade: (f'<div style="position:absolute;left:{-ww/2}px;top:{-hh/2}px;width:{ww}px;height:{hh}px;transform:{tr};backface-visibility:hidden">'
                                     f'{inner}<div style="position:absolute;inset:0;background:rgba(0,0,0,{shade})"></div></div>')
    return (f'<div style="position:relative;transform-style:preserve-3d;transform:rotateX({rx}deg) rotateY({ry}deg)">'
            + f(front,W_,H_,f'translateZ({D_/2}px)',0)
            + f(f'<div style="position:absolute;inset:0;transform:none">{top}</div>',W_,D_,f'rotateX(90deg) translateZ({H_/2}px)',-0.0)
            + f(side,D_,H_,f'rotateY(90deg) translateZ({W_/2}px)',0.18)
            + f(side,D_,H_,f'rotateY(-90deg) translateZ({W_/2}px)',0.25)
            + '</div>')
def place(x,y,inner): return f'<div style="position:absolute;left:{x}px;top:{y}px;transform-style:preserve-3d">{inner}</div>'
def board(name,title,blurb,scenes,bg='#EDE6DA',w=1800,h=1100):
    html=(f'<html><head><style>{CSS}html,body{{margin:0}}.b{{position:relative;width:{w}px;height:{h}px;background:{bg};overflow:hidden;perspective:2600px}}'
          f'.h{{position:absolute;left:60px;top:44px;font:52px IS;color:#2A2017}}.p{{position:absolute;left:62px;top:112px;width:1300px;font:21px/1.45 G;color:#4A4036}}</style></head>'
          f'<body><div class="b"><div class="h">{title}</div><div class="p">{blurb}</div>{"".join(scenes)}</div></body></html>')
    open(O+name+'.html','w').write(html)

# ---------------------------------------------------------------- 1. postage parcel
STAMP=R+'/export/tote/1ink-halftone/tote-stamp-halftone_FILM.png'
def stamp_parcel(k):
    v=V[k]; defs=KRAFT+(f'<filter id="tint{k}"><feColorMatrix values="0 0 0 0 {int(v["dk"][1:3],16)/255} 0 0 0 0 {int(v["dk"][3:5],16)/255} 0 0 0 0 {int(v["dk"][5:7],16)/255} -1 0 0 0 1"/></filter>'
                          f'<path id="pm{k}" d="M88 25 a17 17 0 1 1 0.01 0"/>')
    stripes=''.join(f'<path d="M{x} 0 l6 0 l-6 6 l-6 0z" fill="{"#C8352A" if i%2 else "#2A4A8C"}"/>' for i,x in enumerate(range(0,150,6)))
    body=kraft(W,H)+f'<g transform="translate(0 0)">{stripes}</g><g transform="translate(0 75)">{stripes}</g>'
    body+=(f'<rect x="88" y="12" width="40" height="52" fill="#F4EEDF"/><image href="file://{STAMP}" x="89" y="13" width="38" height="50" preserveAspectRatio="xMidYMid slice" filter="url(#tint{k})"/>'
           f'<g opacity="0.75" fill="none" stroke="{v["dk"]}" stroke-width="0.6"><circle cx="88" cy="42" r="17"/><circle cx="88" cy="42" r="12"/>'
           + ''.join(f'<path d="M100 {32+i*5} q6 -3 12 0 t12 0 t12 0"/>' for i in range(4)) + '</g>'
           + f'<text font-family="AE" font-size="2.6" fill="{v["dk"]}" opacity="0.8" letter-spacing="0.5"><textPath href="#pm{k}">HAND-POLLINATED · NEGOMBO · SRI LANKA ·</textPath></text>'
           + t(88,44,4,'14 OCT','AE',v['dk'],'middle',0.3,'opacity="0.8"')
           + t(10,24,13,v['name'],'IS','#2A1B10') + t(10,31,2.6,v['sub']+' · 100 g','AE','#2A1B10',tr=0.6)
           + t(10,46,6,'To:','CV','#1E2A5A') + f'<path d="M20 46.5H76M10 56.5H76" stroke="#2A1B10" stroke-width="0.25"/>'
           + t(10,63,6,'From:','CV','#1E2A5A') + f'<path d="M26 63.5H76" stroke="#2A1B10" stroke-width="0.25"/>'
           + t(22,45,5.5,'Amma','CV','#1E2A5A'))
    top=svg(W,D,kraft(W,D)+f'<g transform="translate(12 6) rotate(-4)"><rect width="62" height="15" fill="none" stroke="#C8352A" stroke-width="0.9" rx="1"/>'
            + t(31,7,4.6,'CONTAINS CALM','AX','#C8352A','middle',0.4) + t(31,12.3,2.6,'HANDLE GENTLY · DO NOT RUSH','AE','#C8352A','middle',0.4)+'</g>'
            + t(124,18,9,'The Vanilla Shop','IS','#2A1B10','end'),KRAFT)
    side=svg(D,H,kraft(D,H)+''.join(f'<path d="M0 {y} l{D} -8 v6 l-{D} 8z" fill="{"#C8352A" if i%2 else "#2A4A8C"}" opacity="0.9"/>' for i,y in enumerate(range(6,90,8)))[:0]
             + t(14,40,3,'PAR AVION','AE','#2A4A8C','middle',0.6,'transform="rotate(-90 14 40)"'),KRAFT)
    return box(svg(W,H,body,defs),top,side)
board('1-postage-parcel','1 · Pollinated by hand: the soap as a parcel',
      'Kraft box, airmail edges, and our Ceylon stamp in each soap\'s ink. The postmark reads HAND-POLLINATED · NEGOMBO; the To / From lines turn it into a gift card. '
      'The lid says CONTAINS CALM · HANDLE GENTLY. Same world as the tote.',
      [place(300+i*410,660-(i%2)*50,stamp_parcel(k))  for i,k in enumerate(ORDER)])

# ---------------------------------------------------------------- 2. scratch and sniff
BLOOM=S+'/soap/new/SP-vanilla.png'
def sniff(big=False):
    defs=('<radialGradient id="gl" cx="35%" cy="30%" r="75%"><stop offset="0" stop-color="#fff" stop-opacity="0.9"/><stop offset="0.35" stop-color="#fff" stop-opacity="0.25"/>'
          '<stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient><path id="ring" d="M108 52 m-19 0 a19 19 0 1 1 38 0 a19 19 0 1 1 -38 0"/>'
          '<pattern id="dots" width="1.2" height="1.2" patternUnits="userSpaceOnUse"><circle cx="0.6" cy="0.6" r="0.28" fill="#fff" opacity="0.5"/></pattern>')
    front=(f'<svg viewBox="31.4 113.8 135.7 81.2" width="100%" height="100%" preserveAspectRatio="none"><image href="file://{BLOOM}" x="-3" y="-3" width="196.3" height="227.5"/></svg>')
    patch=svg(W,H,f'<circle cx="108" cy="52" r="16" fill="#E7B04A" opacity="0.35"/><circle cx="108" cy="52" r="16" fill="url(#dots)"/><circle cx="108" cy="52" r="16" fill="url(#gl)"/>'
              f'<circle cx="108" cy="52" r="16" fill="none" stroke="#4A2C08" stroke-width="0.3" stroke-dasharray="0.8 0.6"/>'
              f'<text font-family="AE" font-size="2.5" fill="#4A2C08" letter-spacing="0.9"><textPath href="#ring">SCRATCH · SNIFF · SAVOR THE CALM · SCRATCH · SNIFF ·</textPath></text>'
              + t(108,51,4.2,'scratch','CV','#4A2C08','middle') + t(108,56,4.2,'me ↓','CV','#4A2C08','middle'),defs)
    top=svg(W,D,f'<rect width="{W}" height="{D}" fill="#F7EFDC"/>'+t(W/2,17,3.2,'THIS BOX SMELLS OF REAL CEYLON VANILLA','AE','#4A2C08','middle',0.6))
    side=svg(D,H,f'<rect width="{D}" height="{H}" fill="#EBD3A0"/>')
    return box(f'<div style="position:absolute;inset:0">{front}</div><div style="position:absolute;inset:0">{patch}</div>',top,side,s=5.2 if big else 3.0,ry=-24)
board('2-scratch-and-sniff','2 · Smell the box',
      'A scratch-and-sniff vanilla varnish (micro-encapsulated fragrance) printed only on the circle. Shown on the Bloom box, but it sits on top of any idea. '
      'On a shelf of sealed soaps, ours is the one you can smell before you buy.',
      [place(900,660,sniff(True))])

# ---------------------------------------------------------------- 3. stack to spell
def spell(i,k):
    v=V[k]; word='SAVOR THE CALM'
    body=(f'<rect width="{W}" height="{H}" fill="{v["bg"]}"/>'
          f'<g transform="translate({-i*W} 0)">{t(6,60,47,word,"AX",v["lt"],"start",-1.2,"textLength=\""+str(4*W-12)+"\" lengthAdjust=\"spacingAndGlyphs\"")}</g>'
          + t(6,9,3,'THE VANILLA SHOP','AE',v['lt'],tr=0.7) + t(W-6,9,3,'100 g','AE',v['lt'],'end',0.7)
          + t(6,75,4.4,v['name'],'IS',v['lt']) + t(W-6,75,2.6,v['sub'],'AE',v['lt'],'end',0.6))
    top=svg(W,D,f'<rect width="{W}" height="{D}" fill="{v["bg"]}"/>'+t(W/2,20,16,str(i+1)+'/4','AX',v['lt'],'middle'))
    side=svg(D,H,f'<rect width="{D}" height="{H}" fill="{v["bg"]}"/>'+t(D/2,H/2,9,'SAVOR THE CALM'.split()[min(i,2)] if i<3 else '·','AX',v['lt'],'middle',0,f'transform="rotate(-90 {D/2} {H/2})"'))
    return box(svg(W,H,body),top,side,s=2.95,ry=-8,rx=-10)
board('3-stack-to-spell','3 · Stack to spell',
      'Each soap in its own loud colour, one giant line of type running across all four. One box on its own reads SAVO… and makes you look for the rest; '
      'the full set on a shelf (or in a gift pack) spells SAVOR THE CALM. The lids number the set 1/4 to 4/4.',
      [place(345+i*404,620,spell(i,k)) for i,k in enumerate(ORDER)])

# ---------------------------------------------------------------- 4. paper-cut, hand-numbered
def torn(x0,y0,x1,y1,seed):
    r=random.Random(seed); pts=[]
    for x in range(int(x0),int(x1)+1,2): pts.append((x,y0+r.uniform(-1.4,1.4)))
    for x in range(int(x1),int(x0)-1,-2): pts.append((x,y1+r.uniform(-1.4,1.4)))
    return 'M'+' L'.join(f'{a:.1f} {b:.1f}' for a,b in pts)+'Z'
SHAPES={'vanilla':'<path d="M18 62 C22 40 40 22 62 20 C70 19 76 24 74 31 C72 37 64 37 63 31" fill="none" stroke="{c}" stroke-width="7.5" stroke-linecap="round"/>',
        'rosette':'<path d="M44 44 m0 0 a4 4 0 1 1 6 3 a9 9 0 1 1 -14 -8 a15 15 0 1 1 24 14 a21 21 0 1 1 -31 -20" fill="none" stroke="{c}" stroke-width="5" stroke-linecap="round"/>',
        'ebony':'<path d="M22 50 C16 34 30 20 46 24 C60 16 76 28 70 44 C76 58 60 70 46 64 C32 72 18 64 22 50Z" fill="{c}"/><circle cx="40" cy="40" r="3" fill="#F2EBDD"/><circle cx="54" cy="50" r="2.2" fill="#F2EBDD"/><circle cx="46" cy="56" r="1.6" fill="#F2EBDD"/>',
        'aloe':'<path d="M44 70 C40 50 28 34 14 26 C32 30 42 42 46 56 C46 38 52 22 62 12 C58 30 56 46 52 66 C58 52 68 44 80 40 C68 50 60 60 56 72Z" fill="{c}"/>'}
def papercut(i,k):
    v=V[k]; c=v['bg'] if k!='ebony' else '#1D1A18'
    body=(kraft(W,H,'#D9C3A1')+f'<path d="{torn(30,6,W-10,H-6,i)}" fill="#F2EBDD"/>'
          + f'<g transform="translate(30 0) scale(0.95)">{SHAPES[k].format(c=c)}</g>'
          + t(94,26,7.2,v['name'].split(' ')[0].upper(),'AC','#1D1A18','start',0.1) + t(94,31.5,1.9,v['sub'],'AE','#1D1A18',tr=0.3)
          + t(94,46,6.2,f'Batch {7+i:02d}','MK','#1E2A5A') + t(94,54,5,'poured 14.10','MK','#1E2A5A')
          + t(94,68,1.9,'HANDMADE IN SRI LANKA · 100 g','AE','#1D1A18',tr=0.4))
    side=svg(D,H,kraft(D,H,'#D9C3A1'),KRAFT)
    top=svg(W,D,kraft(W,D,'#D9C3A1')+t(10,18,8,'The Vanilla Shop','IS','#2A1B10'),KRAFT)
    return box(svg(W,H,body,KRAFT),top,side,s=2.95,ry=-28)
board('4-paper-cut','4 · Paper-cut and hand-numbered',
      'Stock kraft boxes, one torn paper label per soap with a bold paper-cut shape (curled pod, rose spiral, charcoal lump, aloe spikes), '
      'and the batch and pour date written in marker at the shop. The cheapest to make, and it says handmade without trying.',
      [place(340+i*400,650-(i%2)*36,papercut(i,k)) for i,k in enumerate(ORDER)])

# ---------------------------------------------------------------- 5. characters
FACE={'vanilla':('<g fill="{lt}">'+''.join(f'<ellipse cx="68" cy="24" rx="7" ry="17" transform="rotate({a} 68 42)"/>' for a in (0,72,144,216,288))+'</g><circle cx="68" cy="42" r="12" fill="{bg2}"/>'
                 '<path d="M62 41 q2.5 2.5 5 0 M70 41 q2.5 2.5 5 0" stroke="{dk}" stroke-width="1.1" fill="none" stroke-linecap="round"/><path d="M65.5 47 q2.5 1.8 5 0" stroke="{dk}" stroke-width="1" fill="none" stroke-linecap="round"/>'
                 '<text x="84" y="22" font-family="MK" font-size="5" fill="{dk}">z z z</text>'),
      'rosette':('<circle cx="68" cy="42" r="21" fill="{lt}"/><path d="M68 42 m-3 0 a3 3 0 1 1 6 1 a7 7 0 1 1 -12 -4 a12 12 0 1 1 20 9" fill="none" stroke="{dk}" stroke-width="1.3" opacity="0.35"/>'
                 '<circle cx="60" cy="38" r="2" fill="{dk}"/><circle cx="76" cy="38" r="2" fill="{dk}"/><ellipse cx="56" cy="45" rx="4" ry="2.4" fill="#E2546E"/><ellipse cx="80" cy="45" rx="4" ry="2.4" fill="#E2546E"/>'
                 '<path d="M64 47 q4 3 8 0" stroke="{dk}" stroke-width="1.2" fill="none" stroke-linecap="round"/>'),
      'ebony':('<path d="M48 46 C44 30 58 20 70 24 C84 18 94 32 88 44 C94 58 80 66 68 62 C56 68 46 58 48 46Z" fill="#3A3532"/>'
               '<rect x="54" y="35" width="13" height="7" rx="2" fill="{lt}"/><rect x="71" y="35" width="13" height="7" rx="2" fill="{lt}"/><path d="M67 37h4" stroke="{lt}" stroke-width="1.2"/>'
               '<path d="M63 51 q6 2 12 -1" stroke="{lt}" stroke-width="1.2" fill="none" stroke-linecap="round"/>'),
      'aloe':('<path d="M68 68 C60 48 50 36 40 28 C56 30 64 40 68 52 C68 34 72 20 80 12 C78 30 76 44 74 60 C80 48 90 42 98 40 C88 48 80 58 76 68Z" fill="{lt}"/>'
              '<circle cx="66" cy="54" r="2" fill="{dk}"/><circle cx="76" cy="54" r="2" fill="{dk}"/><path d="M64 59 q7 6 14 0" stroke="{dk}" stroke-width="1.3" fill="none" stroke-linecap="round"/>')}
LINE={'vanilla':'SAVOR THE CALM','rosette':'BLUSH MODE','ebony':'COOL, DARK, HANDSOME','aloe':'FRESH OUT'}
def character(i,k):
    v=V[k]; lt='#FFF6E0' if k!='ebony' else '#F2A93B'; dk=v['dk'] if k!='ebony' else '#1A1716'
    body=(f'<rect width="{W}" height="{H}" fill="{v["bg"]}"/>'+'<g transform="translate(24 6)">'+FACE[k].format(lt=lt,dk=dk,bg2=v['bg'])+'</g>'
          + t(6,22,13,v['name'].split(' ')[0].upper(),'AC',lt,'start',0.2) + t(7,30,2.8,LINE[k],'AE',lt,tr=0.7)
          + t(6,74,2.6,'THE VANILLA SHOP · BATHING BAR · 100 g','AE',lt,tr=0.5))
    top=svg(W,D,f'<rect width="{W}" height="{D}" fill="{v["bg"]}"/>'+t(W/2,19,10,'hi.','MK',lt,'middle'))
    side=svg(D,H,f'<rect width="{D}" height="{H}" fill="{v["bg"]}"/>')
    return box(svg(W,H,body),top,side,s=2.95,ry=-26)
board('5-characters','5 · Characters',
      'Each soap gets a personality: a sleepy vanilla flower, a blushing rose, a charcoal in sunglasses, a grinning aloe. Flat, loud colours and big condensed type, '
      'from the Jooks / omm / Mayawell pins. The most shareable; better as a fun sub-line or gift set than as the main premium range.',
      [place(340+i*400,650-(i%2)*36,character(i,k)) for i,k in enumerate(ORDER)],bg='#F4EEE4')

# ---------------------------------------------------------------- 6. inside the bar
def hatch(path,ang,gap,c,clip):
    return (f'<clipPath id="{clip}"><path d="{path}"/></clipPath><g clip-path="url(#{clip})" stroke="{c}" stroke-width="0.35">'
            + ''.join(f'<path d="M{-50+i*gap} -20 l120 120" transform="rotate({ang} 60 40)"/>' for i in range(0,int(240/gap)))+'</g>')
def inside(i,k):
    v=V[k]; c=v['dk'] if k!='ebony' else '#2A2422'; paper='#F6F1E6'
    if k=='vanilla':
        art=('<path d="M14 40 C40 18 90 16 122 34 C90 26 40 30 14 40Z" fill="none" stroke="{c}" stroke-width="0.9"/>'
             '<path d="M14 42 C40 62 90 64 122 46 C90 54 40 52 14 42Z" fill="none" stroke="{c}" stroke-width="0.9"/>'
             + ''.join(f'<circle cx="{30+j*2.9+((j*7)%3)}" cy="{40+((j*13)%5)-2}" r="0.55" fill="{{c}}"/>' for j in range(30))
             + hatch('M14 40 C40 18 90 16 122 34 C90 26 40 30 14 40Z',20,1.3,'{c}',f'h1{i}'))
        word,sub='Vanilla,','split open.'
    elif k=='rosette':
        art=''.join(f'<path d="M{68-r} 40 a{r} {r*0.8} 0 0 1 {2*r} 0" fill="none" stroke="{{c}}" stroke-width="0.8" transform="rotate({j*47} 68 40)"/>' for j,r in enumerate(range(3,30,3)))
        word,sub='Rose,','from above.'
    elif k=='ebony':
        art=('<path d="M40 46 C36 28 54 18 70 22 C88 16 100 32 94 46 C100 60 82 68 68 64 C52 70 38 60 40 46Z" fill="none" stroke="{c}" stroke-width="0.9"/>'
             + hatch('M40 46 C36 28 54 18 70 22 C88 16 100 32 94 46 C100 60 82 68 68 64 C52 70 38 60 40 46Z',-30,1.1,'{c}',f'h2{i}')
             + ''.join(f'<circle cx="{50+(j*17)%40}" cy="{30+(j*11)%28}" r="{1+(j%3)*0.6}" fill="#F6F1E6" stroke="{{c}}" stroke-width="0.4"/>' for j in range(12)))
        word,sub='Charcoal,','up close.'
    else:
        art=('<path d="M24 52 C40 20 96 20 112 52 C96 40 40 40 24 52Z" fill="none" stroke="{c}" stroke-width="0.9"/>'
             '<path d="M34 49 C48 30 88 30 102 49 C88 41 48 41 34 49Z" fill="none" stroke="{c}" stroke-width="0.6"/>'
             + hatch('M24 52 C40 20 96 20 112 52 C96 40 40 40 24 52Z',60,1.2,'{c}',f'h3{i}'))
        word,sub='Aloe,','cut across.'
    body=(f'<rect width="{W}" height="{H}" fill="{paper}"/><g transform="translate(0 4)">{art.format(c=c)}</g>'
          + t(8,16,9,word,'IS',c) + t(8,23,6,sub,'IS',c) + t(8,74,2.4,'THE VANILLA SHOP · '+v['sub']+' BATHING BAR · 100 g','AE',c,tr=0.45))
    top=svg(W,D,f'<rect width="{W}" height="{D}" fill="{paper}"/>'+t(W/2,17,3,v['sub'],'AE',c,'middle',0.8))
    side=svg(D,H,f'<rect width="{D}" height="{H}" fill="{v["bg"]}"/>')
    return box(svg(W,H,body),top,side,s=2.95,ry=-28)
board('6-inside-the-bar','6 · Inside the bar',
      'The ingredient opened up and drawn big in one engraved colour, like the Sowvital and Taini pins: a split vanilla pod spilling seeds, a rose from above, '
      'charcoal up close, aloe cut across. Calm and premium, with a clear "what\'s in it". The coloured side panel tells them apart on a shelf.',
      [place(340+i*400,650-(i%2)*36,inside(i,k)) for i,k in enumerate(ORDER)])

# ---------------------------------------------------------------- 7. matchbox drawer
def drawer():
    v=V['vanilla']; s=4.0
    sleeve_f=svg(W,H,f'<rect width="{W}" height="{H}" fill="{v["bg"]}"/>'+t(10,40,22,'Vanilla','IS',v['dk'])+t(11,50,3,'BATHING BAR · PULL GENTLY →','AE',v['dk'],tr=0.6))
    sleeve_t=svg(W,D,f'<rect width="{W}" height="{D}" fill="{v["bg"]}"/>'+t(W/2,17,3,'THE VANILLA SHOP','AE',v['dk'],'middle',0.8))
    sleeve_s=svg(D,H,f'<rect width="{D}" height="{H}" fill="{v["bg"]}"/>')
    inner=svg(W,H,f'<rect width="{W}" height="{H}" fill="#F7EFDC"/><rect x="20" y="16" width="70" height="46" rx="12" fill="#F3E3BC" stroke="#D9BE84" stroke-width="0.6"/>'
              + t(55,42,5,'(the soap)','CV','#A08050','middle')
              + t(96,22,4.2,'Every vanilla','IS',v['dk']) + t(96,28,4.2,'flower opens for','IS',v['dk']) + t(96,34,4.2,'one morning.','IS',v['dk'])
              + t(96,44,4.2,'Someone was','IS',v['dk']) + t(96,50,4.2,'there to catch it.','IS',v['dk']))
    dr_f=svg(D-2,H-2,f'<rect width="{D}" height="{H}" fill="#F7EFDC"/>')
    W_,H_,D_=W*s,H*s,D*s
    # the drawer seen from above (its inside), slid out to the right of the sleeve
    return (f'<div style="position:relative;transform-style:preserve-3d;transform:rotateX(-58deg) rotateY(-18deg)">'
            f'<div style="position:absolute;left:{-W_/2+W_*0.55}px;top:{-H_/2}px;width:{W_}px;height:{H_}px;transform:rotateX(90deg) translateZ({-D_*0.0}px) translateY(0px)">{inner}</div>'
            f'<div style="position:absolute;left:{-W_/2}px;top:{-H_/2}px;width:{W_}px;height:{D_}px;transform:translateZ({H_/2}px) rotateX(0deg)">{sleeve_t}</div>'
            '</div>')
# simpler and clearer: a flat-lay diagram of the sleeve and the drawer pulled half out
def drawer_flat():
    v=V['vanilla']; s=5.0
    sleeve=svg(W,H,f'<rect width="{W}" height="{H}" fill="{v["bg"]}"/>'+t(10,42,24,'Vanilla','IS',v['dk'])+t(11,52,3.2,'BATHING BAR · PULL GENTLY →','AE',v['dk'],tr=0.6)
               + t(10,74,2.6,'THE VANILLA SHOP · 100 g','AE',v['dk'],tr=0.6))
    tray=svg(W,H,f'<rect width="{W}" height="{H}" fill="#F7EFDC" stroke="#CDB98F" stroke-width="1.2"/><rect x="10" y="14" width="66" height="50" rx="13" fill="#F1DEB0" stroke="#D2B67C" stroke-width="0.6"/>'
             + t(43,42,5,'(the soap)','CV','#A08050','middle')
             + t(84,24,4.6,'Every vanilla','IS',v['dk']) + t(84,30.5,4.6,'flower opens for','IS',v['dk']) + t(84,37,4.6,'one morning.','IS',v['dk'])
             + t(84,47,4.6,'Someone was','IS',v['dk']) + t(84,53.5,4.6,'there to catch it.','IS',v['dk']) + t(84,64,4,'— savor the calm','CV',v['dk']))
    return (f'<div style="position:absolute;left:260px;top:300px;width:{W*s}px;height:{H*s}px;transform:rotate(-6deg);box-shadow:0 30px 60px rgba(0,0,0,.25)">{tray}</div>'
            f'<div style="position:absolute;left:20px;top:330px;width:{W*s}px;height:{H*s}px;transform:rotate(-6deg);box-shadow:0 30px 60px rgba(0,0,0,.3)">{sleeve}</div>')
board('7-matchbox-drawer','7 · Extra: the matchbox drawer',
      'Same card, folded as a sleeve and a sliding tray. Pull the tray and the inside is printed: the soap sits next to a line about the one-morning flower. '
      'An unboxing moment for the price of a different die. Works with any of the ideas above.',
      [f'<div style="position:absolute;left:180px;top:120px">{drawer_flat()}</div>'],bg='#E9E2D6',h=1100)
print('ok')
