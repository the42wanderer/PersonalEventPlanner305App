# Four front-panel directions, each read off a structure on the bottle board. 120 x 70 mm strip, front centred at x 60.
import sys; sys.path.insert(0,'../w')
from kit import width, logo, txt, caps, rule, esc, css
import orchid
T='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/ext/d/'
W,H,CX=120,70,60
S={'01':dict(no='No. 01',name='Extract',kind='WITH ALCOHOL',dark='#4A120C',col='#B83A24',deep='#7E2414',light='#F6E2C6',paper='#F7EFDC'),
   '02':dict(no='No. 02',name='Extract',kind='ALCOHOL-FREE',dark='#4A2C08',col='#C98A22',deep='#8A5A10',light='#FBEFD4',paper='#F7EFDC'),
   '03':dict(no='No. 03',name='Syrup',kind='NATURAL SYRUP',dark='#16301C',col='#2F5A33',deep='#1F3F24',light='#E7EFCF',paper='#F7EFDC')}
def im(h,x,y,w,hh,extra=''): return f'<image href="file://{T}{h}" x="{x}" y="{y}" width="{w}" height="{hh}" preserveAspectRatio="none" {extra}/>'
def track_to(t,f,sz,target):
    w0=width(t,f,sz); return (target-w0)/(sz*max(len(t)-1,1))
def out(o,name,ml):
    s=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W*20}" height="{H*20}" viewBox="0 0 {W} {H}">'+''.join(o)+'</svg>'
    open(T+name+'.html','w').write(f'<html><head><style>{css}html,body{{margin:0}}</style></head><body>{s}</body></html>')

def bloom_front(k,ml='500 ML'):
    """Bloom pin and Nami Flow: one huge soft-focus flower fills the front; the name is a width-matched lockup on top of it."""
    s=S[k]; c=s['dark']
    o=[im(f'bl-{k}.png',0,0,W,H)]
    sz=27; wv=width('Vanilla','IS',sz); y=42.5
    o.append(txt('Vanilla',CX,y,sz,c,'IS','middle'))
    tr=track_to(s['name'].upper(),'RW',3.4,wv*0.58)
    o.append(caps(s['name'].upper(),CX,y+7.2,3.4,c,'middle',tr))
    o+=[caps(s['no'].upper(),CX-wv/2+1,8.2,1.9,c,'start',0.3), caps(ml,CX+wv/2-1,8.2,1.9,c,'end',0.3), logo(CX,8.6,8,c)]
    o.append(caps(s['kind'],CX,63.6,1.9,c,'middle',0.34))
    return o

def split_front(k,ml='500 ML'):
    """Nova: the front splits at the bottle's centre line. Left, a full-bleed colour field; right, a cream card set like a poster."""
    s=S[k]; c=s['dark']
    o=[f'<rect width="{W}" height="{H}" fill="{s["paper"]}"/>', f'<clipPath id="lh"><rect width="{CX}" height="{H}"/></clipPath>',
       f'<g clip-path="url(#lh)">{im(f"bi-{k}.png",0,0,W,H)}</g>']
    x0,x1=CX+5,CX+36; mx=(x0+x1)/2
    # corner brackets, as on Nova's card
    for (bx,by,dx,dy) in ((x0,7,1,1),(x1,7,-1,1),(x0,63,1,-1),(x1,63,-1,-1)):
        o.append(f'<path d="M{bx} {by+dy*3}V{by}H{bx+dx*3}" fill="none" stroke="{c}" stroke-width="0.3"/>')
    o.append(logo(mx,14.2,8.4,c))
    o+=[rule(x0+4,21.6,x1-4,21.6,c,0.2,0.6)]
    o+=[txt('Vanilla',mx,33,12.4,c,'IS','middle'), txt(s['name'],mx,43,12.4,c,'IS','middle')]
    o+=[caps(s['kind'],mx,48.6,1.85,s['deep'],'middle',0.3)]
    o+=[rule(x0+4,52.4,x1-4,52.4,c,0.2,0.6), txt('Pure Ceylon vanilla',mx,56.4,2.1,c,'G','middle'), caps(ml,mx,60.6,1.8,c,'middle',0.3)]
    o.append(txt(s['no'],CX-4,64.2,6.4,s['light'],'IS','end'))
    return o

def stack_front(k,ml='500 ML'):
    """Kombucha's KOM/BU/CHA and Brooo: the word is the picture. VA/NIL/LA stacked to fill the front, a cured pod threaded through it."""
    s=S[k]; ink=s['light']; g=s['col']
    o=[f'<rect width="{W}" height="{H}" fill="{g}"/>']
    sz=23.5; lines=[('Va',30.6),('nil',48.4),('la',66.2)]
    letters=''.join(txt(t,CX+0.5,y,sz,ink,'IS','middle') for t,y in lines)
    p=orchid.pod(CX-27,58,CX+25,18,4.6,sag=0.06)
    pod=f'<path d="{p["body"]}" fill="#2A140A"/><path d="{p["curl"]}" fill="none" stroke="#2A140A" stroke-width="1.5" stroke-linecap="round"/>'
    # weave: the pod passes over Va and la and under nil
    o.append(letters); o.append(pod)
    o.append(f'<clipPath id="mid"><rect x="0" y="34.5" width="{W}" height="15.5"/></clipPath><g clip-path="url(#mid)">{txt("nil",CX+0.5,48.4,sz,ink,"IS","middle")}</g>')
    o.append(logo(CX,6.6,7.4,ink))
    vx_l,vx_r=CX-24,CX+24
    o.append(f'<g transform="translate({vx_l} 44) rotate(-90)">{caps(s["no"].upper()+"  ·  "+s["kind"],0,0,1.9,ink,"middle",0.34)}</g>')
    o.append(f'<g transform="translate({vx_r} 44) rotate(90)">{caps(s["name"].upper()+"  ·  "+ml,0,0,1.9,ink,"middle",0.34)}</g>')
    return o

def band_front(k,ml='500 ML'):
    """Oshlag: a lush painted band round the top of the bottle, a clean type field below with the contents written out."""
    s=S[k]; c=s['dark']; by=31
    ih=(W+8)*597/1774
    o=[f'<rect width="{W}" height="{H}" fill="#FBF7EE"/>', f'<clipPath id="bd"><rect width="{W}" height="{by}"/></clipPath>',
       f'<g clip-path="url(#bd)">{im(f"band-{k}.jpg",-4,by-ih+2,W+8,ih)}</g>', rule(0,by,W,by,c,0.35,0.9)]
    x0=CX-29
    o+=[txt('THE VANILLA SHOP',x0,by+7.6,3.7,c,'GB','start',0.04), rule(x0+40.4,by+3.2,x0+40.4,by+8.6,c,0.25,0.7),
        caps('CEYLON',x0+42.6,by+5.3,1.6,c,'start',0.25), caps(s['no'].upper(),x0+42.6,by+8.2,1.6,c,'start',0.25)]
    o+=[txt(f'Vanilla {s["name"]}',x0,by+17.6,8.6,s['deep'],'IS','start'), caps(s['kind'],x0,by+21.6,1.8,c,'start',0.3)]
    o.append(txt('hand-pollinated  ·  slow-cured',x0,by+25.4,1.7,c,'GMono','start'))
    o+=[rule(x0,by+27.6,x0+40,by+27.6,c,0.2,0.6), rule(x0+20,by+27.6,x0+20,by+32,c,0.2,0.6), rule(x0,by+32,x0+40,by+32,c,0.2,0.6),
        txt('Pure Ceylon',x0+1,by+30.6,1.9,c,'G'), txt(ml.lower(),x0+21,by+30.6,1.9,c,'G')]
    cx2,cy2=CX+22.5,by+20.4
    o+=[f'<circle cx="{cx2}" cy="{cy2}" r="6.4" fill="{s["col"]}"/>', logo(cx2,cy2,6.6,s['light'])]
    return o

if __name__=='__main__':
    for d,fn in (('bloom',bloom_front),('split',split_front),('stack',stack_front),('band',band_front)):
        for k in S:
            out(fn(k),f'F-{d}-{k}','500 ML')
    print('ok')
