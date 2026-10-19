import numpy as np, draw
from draw import Canvas, tepal, leaf, pod, bud, stem, trumpet, ellipse_ruffle
def mix(a,b,t):
    A=[int(a[i:i+2],16) for i in (1,3,5)]; B=[int(b[i:i+2],16) for i in (1,3,5)]
    return '#%02X%02X%02X'%tuple(int(x+(y-x)*t) for x,y in zip(A,B))
def flower(cv,c,ang_lip,scale,cols,blurs=(0.6,0.45,0.8),tilt=1.0):
    """an open vanilla flower seen at an angle: two back tepals softer and deeper, three front ones crisp,
    a light streak down each midrib, the frilled trumpet lip pointing ang_lip"""
    s=scale; cx,cy=c
    spec=[(-97,16.5,2.0,0.26,0.0),(-160,14.8,1.85,-0.36,0.3),(-36,15.6,1.9,0.34,0.25),(126,13.2,1.75,0.30,0.4),(54,13.8,1.8,-0.32,0.35)]
    back={1,3}; tp_b,tp_f,ribs=[],[],[]
    for i,(a,L,W,b,pin) in enumerate(spec):
        a2=a+ang_lip*0.25
        Lf=L*s*(0.8+0.2*abs(np.cos(np.radians(a2-ang_lip))))
        poly=tepal((cx,cy),a2,Lf,W*s,b,0.012,i*0.9,pin); (tp_b if i in back else tp_f).append(poly)
        sp=tepal((cx,cy),a2,Lf*0.82,W*s,b,spine=True)
        ribs.append(draw.ribbon(sp,lambda t,w=W*s:w*0.16*np.sin(np.pi*t)+0.02))
    deep=mix(cols['tep_edge'],cols['ground'],0.35)
    cv.add(tp_b,mix(cols['tep_core'],cols['tep_edge'],0.25),deep,blurs[0]*1.8,centre=(cx,cy),R=17*s)
    cv.add(tp_f,cols['tep_core'],cols['tep_edge'],blurs[0],centre=(cx,cy),R=17*s)
    cv.add(ribs,'#FFFFFF',cols['tep_core'],blurs[0]*0.8,alpha=0.55,centre=(cx,cy),R=15*s)
    tube,mouth,mc=trumpet((cx,cy),ang_lip,7.5*s,1.1*s,3.6*s,2.6*s,0.13)
    cv.add([tube],cols['lip_edge'],mix(cols['lip_edge'],cols['tep_edge'],0.4),blurs[1],glow=1.0)
    cv.add([mouth],cols['lip_core'],cols['lip_edge'],blurs[1]*0.8,glow=1.4)
    d=np.array([np.cos(np.radians(ang_lip)),np.sin(np.radians(ang_lip))])
    th=ellipse_ruffle(mc+d*0.5*s,1.7*s,1.25*s,ang_lip,0.07,7)
    cv.add([th],cols['throat_core'],cols['throat_edge'],blurs[2],alpha=0.9)
    cv.add([draw.stem([(cx,cy),(cx+d[0]*2.6*s,cy+d[1]*2.6*s)],0.45*s)],'#FFFFFF',cols['lip_core'],blurs[1],alpha=0.7)
PAL={'01':dict(ground='#B83A24',tep_core='#FFF0DC',tep_edge='#EE7F58',lip_core='#FFF6E8',lip_edge='#F7BE94',throat_core='#F6C25A',throat_edge='#E8903E',
               leaf_core='#E68560',leaf_edge='#A6311C',pod_core='#6A1A0E',pod_edge='#3C0B06',bud_core='#FCD6B8',bud_edge='#E57E59',stem='#C9583A'),
     '02':dict(ground='#C98A22',tep_core='#FFF8E6',tep_edge='#F2B45A',lip_core='#FFFBEF',lip_edge='#FBDDA2',throat_core='#F3A23C',throat_edge='#DB7E25',
               leaf_core='#EDBE62',leaf_edge='#A86A12',pod_core='#6A400C',pod_edge='#3E2406',bud_core='#FFEDC4',bud_edge='#EDB75A',stem='#D9A245'),
     '03':dict(ground='#2F5A33',tep_core='#F6F8E4',tep_edge='#9DC07E',lip_core='#FBFBEC',lip_edge='#D3E2B4',throat_core='#E8C35A',throat_edge='#C9A03A',
               leaf_core='#6E9C62',leaf_edge='#24482A',pod_core='#C6DFA0',pod_edge='#3F6B38',bud_core='#E3EDC6',bud_edge='#88AE73',stem='#5E8A55')}
def sheen(cv,spines,w,col,base,blur,alpha=0.5):
    cv.add([draw.ribbon(sp,lambda t,w=w:w*np.sin(np.pi*t)**0.7+0.02) for sp in spines],col,base,blur,alpha=alpha)
def pods(cv,p,specs,blur,glow=0.9,sheen_col=None):
    cv.add([pod(*s_) for s_ in specs],p['pod_core'],p['pod_edge'],blur,glow=glow)
    sheen(cv,[pod(*s_,spine=True)[3:-6]+np.array([0,-0.25*s_[3]]) for s_ in specs],0.32*min(s_[3] for s_ in specs),sheen_col or mix(p['pod_core'],'#FFFFFF',0.35),p['pod_core'],blur*0.9,0.55)
def leaves(cv,p,specs,blur,alpha=1.0):
    cv.add([leaf(*s_) for s_ in specs],p['leaf_core'],p['leaf_edge'],blur,alpha=alpha)
    sheen(cv,[leaf(*s_,spine=True) for s_ in specs],0.35,mix(p['leaf_core'],'#FFFFFF',0.3),p['leaf_core'],blur,0.45*alpha)
def comp01(W=60,H=70,ox=0):
    """No. 01, with alcohol: a big flower turned towards the card, two cured pods sweeping behind it"""
    p=PAL['01']; cv=Canvas(W,H,ox)
    leaves(cv,p,[((2,80),-60,48,8.5,0.55)],2.4,0.85)
    pods(cv,p,[((-8,68),-33,84,3.0,0.30,1),((2,82),-46,80,2.7,0.22,-1)],0.6)
    flower(cv,(29,34),26,2.05,p,blurs=(0.45,0.38,0.7))
    return cv.render(p['ground'],seed=11)
def comp02(W=60,H=70,ox=0):
    """No. 02, alcohol-free: the vine opening, a flower facing out and a spray of buds above"""
    p=PAL['02']; cv=Canvas(W,H,ox)
    leaves(cv,p,[((-6,64),-18,42,8.0,0.5),((66,76),-152,40,7.5,-0.5)],2.4,0.9)
    st=[(27,44),(33,31),(41,19),(50,8),(58,-2)]
    cv.add([stem(st,0.9)],mix(p['stem'],'#FFFFFF',0.25),p['stem'],0.6)
    cv.add([stem([(41,19),(36,15),(31,13)],0.45),stem([(46,13.5),(46,8),(44,3)],0.42),stem([(50,8),(55,6),(60,6)],0.4)],mix(p['stem'],'#FFFFFF',0.25),p['stem'],0.6)
    cv.add([bud((31,13),-168,12,2.6,-0.3),bud((44,3),-100,11,2.4,-0.25),bud((60,6),-5,11,2.3,0.3)],p['bud_core'],p['bud_edge'],0.55,glow=1.2)
    flower(cv,(25,45),86,1.8,p,blurs=(0.45,0.38,0.7))
    return cv.render(p['ground'],seed=12)
def bunch_pod(o,P):
    """one pod of a hanging bunch. P: dict with spread (sideways reach of the stalk), arch (how high it rises),
    L (length), W (half-width), drift (sideways travel of the hanging part), swing (S-curve), bulge (where it is fattest)"""
    ox,oy=o; s=P['spread']; d=P['drift']; sw=P['swing']
    reach=abs(s)*P['arch']
    pts=[(ox,oy),(ox+s*0.45,oy-reach*0.55),(ox+s*0.9,oy-reach*0.35),(ox+s*1.15,oy+2.6),
         (ox+s*1.2+d*0.35+sw,oy+P['L']*0.38),(ox+s*1.15+d*0.7-sw*0.6,oy+P['L']*0.72),(ox+s*1.1+d,oy+P['L'])]
    sp=draw.cr(pts,24); W=P['W']; bz=P['bulge']
    def prof(t):
        if t<0.15: return 0.4
        if t<0.24: return 0.4+(W*0.82-0.4)*(0.5-0.5*np.cos(np.pi*(t-0.15)/0.09))
        w=W*(0.82+0.24*np.exp(-((t-bz)/0.28)**2))
        if t>0.93: w*=np.sqrt(max(0,1-((t-0.93)/0.07)**2))*0.85+0.15*(1-(t-0.93)/0.07)
        return w+0.03
    body=draw.ribbon(sp,prof,0.005,3,P['L'])
    rib=sp[int(len(sp)*0.26):int(len(sp)*0.92)]+np.array([-W*0.36,0])
    return body,rib,sp[-1]
def make_bunch(seed=5,n=13):
    """a deterministic but irregular bunch: depth-sorted, uneven spacing, lengths, swings; two pods swing wide"""
    rng=np.random.default_rng(seed); pods=[]
    for i in range(n):
        s=rng.normal(0,4.2); s=np.sign(s)*min(abs(s)+0.8,9.5)
        pods.append(dict(spread=s,arch=rng.uniform(0.35,0.75),L=rng.uniform(33,58),W=rng.uniform(1.55,2.35),
                         drift=s*rng.uniform(0.15,0.7)+rng.normal(0,1.8),swing=rng.normal(0,0.35),bulge=rng.uniform(0.45,0.75),
                         depth=rng.uniform(0,1),tone=rng.uniform(-0.15,0.2)))
    # two pods that swing wide and cross, as in the photos
    pods.append(dict(spread=-11,arch=0.9,L=40,W=1.7,drift=-3,swing=0.4,bulge=0.6,depth=0.55,tone=0.05))
    pods.append(dict(spread=6,arch=0.5,L=50,W=1.85,drift=-8,swing=-0.3,bulge=0.55,depth=0.9,tone=0.12))
    return sorted(pods,key=lambda q:q['depth'])
def tidy_pod(top,dx,L,W,lean,curl=0.0,spine=False):
    """a slender botanical-plate pod: leaves the shared stalk narrow, a long even body, and either a rounded tip
    or, when curl != 0, a tip that hooks round like a banana's but more so (curl = total turn in degrees, signed)"""
    x0,y0=top
    pts=[(x0,y0),(x0+dx*0.35,y0+L*0.18),(x0+dx*0.8+lean*0.3,y0+L*0.45),(x0+dx+lean*0.7,y0+L*0.75),(x0+dx*1.05+lean,y0+L)]
    sp=draw.cr(pts,24)
    if curl:
        d=sp[-1]-sp[-4]; a=np.arctan2(d[1],d[0]); step=np.linalg.norm(d)/3*0.9; tail=[sp[-1]]
        step=1.45
        for k in range(1,25):
            a+=np.radians(curl)/24*(0.55+0.9*k/24); step*=0.935; tail.append(tail[-1]+step*np.array([np.cos(a),np.sin(a)]))
        sp=np.vstack([sp,np.array(tail[1:])])
    if spine: return sp
    n=len(sp); body_end=24*4/ n if curl else 1.0
    def prof(t):
        w=W*min(1,(t/0.22))**0.75 if t<0.22 else W*(1+0.04*np.sin(np.pi*(t-0.22)/0.78))
        if curl:
            if t>0.74: w*=max(0.2,1-((t-0.74)/0.26)**1.1*0.82)
        elif t>0.9: w*=np.sqrt(max(0,1-((t-0.9)/0.1)**2))
        return w+0.05
    return draw.ribbon(sp,prof)
def ridges(sp,W,light,dark):
    """faint lines running the length of the bean: one pale ridge, one shallow groove"""
    s=sp[int(len(sp)*0.24):int(len(sp)*0.9)]
    d=np.gradient(s,axis=0); d/=np.linalg.norm(d,axis=1,keepdims=True)+1e-9; nrm=np.stack([-d[:,1],d[:,0]],1)
    out=[]
    for off,col,a,w in ((-0.38,light,0.7,0.17),(0.2,dark,0.55,0.14),(0.6,light,0.4,0.11)):
        out.append((draw.ribbon(s+nrm*W*off,lambda t,w=w:w*np.sin(np.pi*t)**0.4+0.02),col,a))
    return out
def comp03(W=60,H=70,ox=0):
    """No. 03, syrup: hand-placed pods (podpaths.py) painted like Nos. 01 and 02: slender pods hanging almost
    parallel from one node, two curling up at the end like a banana, faint ridges along each bean,
    one broad leaf behind, the flower and a bud above"""
    import podpaths as pp
    p=PAL['03']; cv=Canvas(W,H,ox); X,Y=pp.TOP
    cv.add([leaf((X+2,Y+4),56,52,10.0,-0.15)],'#6AA463','#2A5230',0.9,alpha=1.0,glow=0.9,halo=0.1)
    cv.add([stem([(X-7,-3),(X-3,3),(X,Y)],0.7)],mix(p['stem'],'#FFFFFF',0.15),p['stem'],0.8)
    for i,(P,w,dep) in enumerate(sorted(pp.PODS,key=lambda q:q[2])):
        poly,cl=pp.outline(P,w)
        # a watercolour wash, like the petals: pale near the node, deepening to green at the tip, translucent
        pale=mix('#F1F7DC','#CFE2AE',(1-dep)*0.5); deep=mix('#A9CC8A','#7FA868',(1-dep)*0.55); bl=0.28+(1-dep)*0.4
        L_=float(np.sum(np.linalg.norm(np.diff(cl,axis=0),axis=1)))
        cv.add([poly],pale,deep,bl,alpha=0.9,centre=(X,Y-2),R=L_*1.05,glow=0.8,halo=0.02,
               wash=(mix(deep,'#3E6A3C',0.4),0.4,0.38))
        for poly_r,col,a_ in ridges(cl,w,mix(pale,'#FFFFFF',0.4),deep):
            cv.add([poly_r],col,col,bl*1.1,alpha=a_*0.35*(0.5+0.5*dep),halo=0.0)
        if dep>=1.0:
            cv.add([poly],'#F0D47A','#B8D48E',0.6,alpha=0.6,centre=tuple(cl[-1]),R=13,glow=0.8,halo=0.0)
    cv.add([bud((X-3,2),-130,11,2.3,-0.25)],p['bud_core'],p['bud_edge'],0.6,glow=1.2)
    flower(cv,(13,10),20,1.1,p,blurs=(0.45,0.38,0.75))
    return cv.render(p['ground'],seed=13)
if __name__=='__main__':
    import sys
    for k,f in (('01',comp01),('02',comp02),('03',comp03)):
        f().save(f'art-{k}.png'); print(k)
