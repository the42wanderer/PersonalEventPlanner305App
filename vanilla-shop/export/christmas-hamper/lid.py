# Christmas hamper lid, 365 x 227 mm top: one gold foil of vanilla line art on a deep matte ground.
# A vine garland with hanging pods across the top, the logo and "A Vanilla Christmas", and a row of
# Christmas trees drawn as vanilla vines, each topped with a vanilla flower for its star.
import sys, math, random
sys.path.insert(0,'/home/user/PersonalEventPlanner305App/vanilla-shop/brand/directions/bloom')
import orchid
R='/home/user/PersonalEventPlanner305App/vanilla-shop'
O='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/hamper/'
W,H=365,227
FONTS={'IS':R+'/fonts/instrument-serif-italic.ttf','ISR':R+'/fonts/instrument-serif.ttf','AE':R+'/fonts/archivo-expanded-regular.ttf'}
CSS=''.join(f"@font-face{{font-family:{k};src:url(file://{v})}}" for k,v in FONTS.items())
LOGO=__import__('re').search(r' d="([^"]+)"',open(R+'/brand/vanilla-shop-logo.svg').read()).group(1)
GROUND={'green':'#1E3B2A','red':'#7A1C22'}
FOILG=('<linearGradient id="g" x1="0" y1="0" x2="1" y2="0.6"><stop offset="0" stop-color="#8A6424"/><stop offset="0.25" stop-color="#E8C878"/>'
       '<stop offset="0.45" stop-color="#A57A2E"/><stop offset="0.7" stop-color="#F3DB97"/><stop offset="1" stop-color="#8E6526"/></linearGradient>')
rnd=random.Random(7)
def P(x,y): return f'{x:.2f} {y:.2f}'
def leaf(x,y,ang,L,w=0.42):
    a=math.radians(ang); d=(math.cos(a),math.sin(a)); p=(-d[1],d[0])
    t=(x+d[0]*L,y+d[1]*L); c1=(x+d[0]*L*0.45+p[0]*L*w,y+d[1]*L*0.45+p[1]*L*w); c2=(x+d[0]*L*0.45-p[0]*L*w,y+d[1]*L*0.45-p[1]*L*w)
    return f'<path d="M{P(x,y)}Q{P(*c1)} {P(*t)}Q{P(*c2)} {P(x,y)}Z"/><path d="M{P(x,y)}L{P(x+d[0]*L*0.82,y+d[1]*L*0.82)}" stroke-width="0.3"/>'
def bez(p0,p1,p2,p3,t):
    u=1-t; return (u**3*p0[0]+3*u*u*t*p1[0]+3*u*t*t*p2[0]+t**3*p3[0], u**3*p0[1]+3*u*u*t*p1[1]+3*u*t*t*p2[1]+t**3*p3[1])
def flower(cx,cy,R_,rot=0):
    f=orchid.flower(0,0,R_)
    return (f'<g transform="translate({cx:.2f} {cy:.2f}) rotate({rot})">'+''.join(f'<path d="{t}"/>' for t in f['tepals'])
            +f'<path d="{f["lip"]}"/><path d="{f["throat"]}" stroke-width="0.3"/></g>')
def pod(x,y,L,w=1.7):
    p=orchid.pod(x,y,x+0.6,y+L,w,hook=1.0,sag=0.05)
    return f'<path d="{p["body"]}"/><path d="{p["curl"]}"/><path d="{p["spine"]}" stroke-width="0.25"/>'
def spark(x,y,r):
    return f'<path d="M{P(x,y-r)}Q{P(x,y)} {P(x+r,y)}Q{P(x,y)} {P(x,y+r)}Q{P(x,y)} {P(x-r,y)}Q{P(x,y)} {P(x,y-r)}Z" fill="FILL" stroke="none"/>'
def garland():
    o=[]
    for (p0,p1,p2,p3) in (((9.2,22),(75,62),(140,58),(182.5,34)),((182.5,34),(225,58),(290,62),(355.8,22))):
        o.append(f'<path d="M{P(*p0)}C{P(*p1)} {P(*p2)} {P(*p3)}" stroke-width="0.6"/>')
        # a second, thinner vine twisting round the first
        o.append(f'<path d="M{P(p0[0],p0[1]+2)}C{P(p1[0],p1[1]-6)} {P(p2[0],p2[1]+5)} {P(p3[0],p3[1]-2)}" stroke-width="0.35"/>')
        for i in range(1,14):
            t=i/14; x,y=bez(p0,p1,p2,p3,t); x2,y2=bez(p0,p1,p2,p3,t+0.01); ang=math.degrees(math.atan2(y2-y,x2-x))
            o.append(leaf(x,y,ang+(-55 if i%2 else 55),8.5))
            if i in (2,4,7,10,12):                       # pods hang from the vine like baubles
                L=rnd.uniform(6,16); o.append(f'<path d="M{P(x,y)}L{P(x+0.3,y+L)}" stroke-width="0.3"/>'); o.append(pod(x,y+L,22,2.3))
            if i in (5,9): o.append(flower(x,y-1,6.5,rnd.uniform(-30,30)))
    o.append(flower(182.5,33,8.5,0))
    return o
def tree(cx,base,h,w,kind):
    top=base-h; o=[f'<path d="M{P(cx-w/2,base)}L{P(cx,top)}L{P(cx+w/2,base)}" stroke-width="0.5"/>']
    if kind=='zig':                                   # a vine zig-zagging down the tree, with a leaf at each turn
        pts=[]; n=max(4,int(h/7.5))
        for i in range(n+1):
            t=0.12+0.86*i/n; y=top+h*t; half=w/2*t*0.86; x=cx+(half if i%2 else -half); pts.append((x,y))
        d='M'+P(*pts[0])+''.join(f'Q{P(cx,(pts[i][1]+pts[i+1][1])/2)} {P(*pts[i+1])}' for i in range(len(pts)-1))
        o.append(f'<path d="{d}" stroke-width="0.4"/>')
        for i,(x,y) in enumerate(pts[1:-1]): o.append(leaf(x,y,(200 if x<cx else -20)+rnd.uniform(-10,10),4.2))
    elif kind=='loop':                                # loops, like a ribbon wound round
        n=max(3,int(h/10)); d=''
        for i in range(n):
            t=0.2+0.78*i/n; y=top+h*t; half=w/2*t*0.8
            d+=f'M{P(cx-half,y)}C{P(cx-half*0.3,y-6)} {P(cx+half*0.3,y+6)} {P(cx+half,y)}'
        o.append(f'<path d="{d}" stroke-width="0.4"/>')
    elif kind=='pods':                                # pods hung on the branches
        for i in range(1,int(h/11)+1):
            t=i/(h/11+1); y=top+h*t; half=w/2*t
            o.append(f'<path d="M{P(cx-half*0.85,y)}L{P(cx+half*0.85,y)}" stroke-width="0.35"/>')
            for s in (-1,1):
                if half>6: o.append(pod(cx+s*half*0.5,y+0.6,min(9,4+half*0.3),1.1))
    elif kind=='dots':                                # a dotted tree, as in a woven print
        for i in range(2,int(h/3.2)):
            y=top+i*3.2; half=w/2*(y-top)/h*0.86
            for j in range(-int(half/3.2),int(half/3.2)+1): o.append(f'<circle cx="{cx+j*3.2+(1.6 if i%2 else 0):.2f}" cy="{y:.2f}" r="0.62" fill="FILL" stroke="none"/>')
    o.append(flower(cx,top-3.2,5.4 if h>50 else 4.2,0))
    return o
def trees():
    base=212; o=[f'<path d="M14 {base}H351" stroke-width="0.5"/>']
    back=[(44,70,34,'pods'),(98,84,40,'zig'),(152,74,36,'loop'),(213,74,36,'loop'),(267,84,40,'zig'),(321,70,34,'pods')]
    front=[(22,40,22,'dots'),(70,52,28,'loop'),(124,46,26,'dots'),(182.5,86,56,'dots'),(241,46,26,'dots'),(295,52,28,'loop'),(343,40,22,'dots')]
    for cx,h,w,k in back: o.append('<g stroke-width="0.3">'+''.join(tree(cx,base-4,h,w,k)).replace('stroke-width="0.5"','stroke-width="0.32"').replace('stroke-width="0.4"','stroke-width="0.28"')+'</g>')   # foil has no tints: the back row is finer, not fainter
    for cx,h,w,k in front: o+=tree(cx,base,h,w,k)
    for x in range(18,350,9):                        # a low line of vanilla leaves along the ground
        o.append(leaf(x+rnd.uniform(-2,2),base,rnd.choice((-120,-60,-100,-80)),rnd.uniform(3.5,6)))
    return o
def sky():
    o=[]; keep=[(108,80,257,116),(160,44,205,78)]               # keep clear of the logo and the title
    pts=[]
    while len(pts)<150:
        x,y=rnd.uniform(14,351),rnd.uniform(44,170)
        if any(a<x<c and b<y<d for a,b,c,d in keep): continue
        if any((x-u)**2+(y-v)**2<30 for u,v in pts): continue
        pts.append((x,y))
    for i,(x,y) in enumerate(pts):
        o.append(spark(x,y,rnd.uniform(1.0,2.2)) if i%3==0 else f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{rnd.uniform(0.45,0.85):.2f}" fill="FILL" stroke="none"/>')
    return o
def border():
    return [f'<rect x="7" y="7" width="{W-14}" height="{H-14}" stroke-width="0.6"/>',f'<rect x="9.2" y="9.2" width="{W-18.4}" height="{H-18.4}" stroke-width="0.3"/>']
def foil(fill):
    lines=''.join(garland()+trees()+sky()+border()).replace('FILL',fill)
    g=f'<g fill="none" stroke="{fill}" stroke-linecap="round" stroke-linejoin="round" stroke-width="0.45">'+lines+'</g>'
    s=1/933*26
    g+=f'<path d="{LOGO}" fill="{fill}" fill-rule="evenodd" transform="translate({182.5-13:.2f} {50:.2f}) scale({s:.5f})"/>'
    g+=f'<text x="182.5" y="101" text-anchor="middle" font-family="ISR" font-size="27" fill="{fill}">A Vanilla <tspan font-family="IS">Christmas</tspan></text>'
    g+=f'<text x="182.5" y="111.5" text-anchor="middle" font-family="AE" font-size="3.6" letter-spacing="1.3" fill="{fill}">FROM OUR FARMS IN SRI LANKA · 2026</text>'
    return g
def svg(colour,mode):
    # mode: 'mock' = foil simulated, 'print' = ground only (foil areas left for the foil), 'foil' = foil plate in black
    bg='#fff' if mode=='foil' else GROUND[colour]
    fill={'mock':'url(#g)','foil':'#000','print':'none'}[mode]
    body=f'<rect width="{W}" height="{H}" fill="{bg}"/>'
    if mode!='foil': body+=f'<rect width="{W}" height="{H}" fill="url(#grain)" opacity="0.5"/>'
    if mode!='print': body+=foil(fill)
    defs=(FOILG+'<filter id="n"><feTurbulence type="fractalNoise" baseFrequency="2.2" numOctaves="2" seed="3"/><feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.35 0"/></filter>'
          f'<pattern id="grain" width="{W}" height="{H}" patternUnits="userSpaceOnUse"><rect width="{W}" height="{H}" filter="url(#n)"/></pattern>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}mm" height="{H}mm"><defs>{defs}</defs>{body}</svg>'
def html(name,inner,w,h):
    open(O+name+'.html','w').write(f'<html><head><meta charset="utf-8"><style>{CSS}@page{{size:{w}mm {h}mm;margin:0}}html,body{{margin:0}}svg{{display:block;width:100vw;height:auto}}</style></head><body>{inner}</body></html>')
if __name__=='__main__':
    for c in GROUND:
        for m in ('mock','print','foil'): html(f'lid-{c}-{m}',svg(c,m),W,H)
    print('ok')
