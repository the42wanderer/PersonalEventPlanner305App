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
# Pods traced from Agro Ventures' own plantation photo (agroventuresexports.com, home/img3.JPG, read at 664 x 1000 px):
# each is its centre line from the node to the tip, its width in px, and its depth (0 back .. 1 front).
TRACE=[
 ([(352,216),(356,300),(368,400),(380,480),(386,553)],21,0.15),
 ([(346,216),(337,285),(340,380),(352,470),(358,548)],21,0.25),
 ([(355,218),(362,330),(371,432),(379,555)],20,0.10),
 ([(333,214),(303,242),(293,300),(298,382),(318,465)],22,0.45),
 ([(359,216),(376,320),(410,420),(446,520),(466,604)],24,0.55),
 ([(368,214),(395,290),(425,380),(458,470),(490,566)],24,0.65),
 ([(365,212),(390,282),(414,362),(440,442),(462,506)],23,0.75),
 ([(360,212),(375,290),(395,380),(415,450),(428,488)],24,0.85),
 ([(372,210),(402,262),(442,332),(490,422),(535,520)],24,0.95)]
REMNANT={4:[(466,604),(463,628),(461,652),(463,672)],7:[(428,488),(431,500),(436,508)]}   # dried flowers still on the tips
def traced_pod(pts,wpx,S,O):
    P=[(O[0]+(x-350)*S,O[1]+(y-212)*S) for x,y in pts]; sp=draw.cr(P,20); W=wpx*S/2*1.3
    def prof(t):
        w=W*min(1,0.35+t*5.5)*(1+0.06*np.sin(np.pi*t))
        if t>0.93: w*=np.sqrt(max(0,1-((t-0.93)/0.07)**2))*0.75+0.25
        return w+0.04
    return draw.ribbon(sp,prof), P[-1]
def comp03(W=60,H=70,ox=0):
    """No. 03, syrup: the bunch traced from Agro Ventures' own vine photo, drawn like Nos. 01 and 02:
    soft glow from light near the node to deeper tips, back pods softer, dried flowers on two tips, one flower open"""
    p=PAL['03']; cv=Canvas(W,H,ox)
    S=0.158; O=(25,2)                      # 400 px of bunch -> about 63 mm; node near the top edge
    cv.add([leaf((-6,74),-62,64,10.5,0.25)],'#4C8650','#24482A',2.4,alpha=0.9,glow=0.8)
    cv.add([stem([(O[0]-2,-6),(O[0],O[1]+0.5)],0.9)],mix(p['stem'],'#FFFFFF',0.15),p['stem'],0.9)
    light=(O[0]+4,O[1]+8)
    tips=[]
    for i,(pts,wpx,dep) in sorted(enumerate(TRACE),key=lambda q:q[1][2]):
        poly,tip=traced_pod(pts,wpx,S,O)
        core=mix('#C2DC9C','#86AE6C',(1-dep)*0.55); edge=mix('#557F4A','#3C6438',(1-dep)*0.6)
        cv.add([poly],core,edge,0.3+(1-dep)*0.7,alpha=1.0,glow=1.15,halo=0.04)
        if i in (5,8): cv.add([poly],'#F0CF66','#B9D48E',0.45,alpha=0.8,centre=tuple(tip),R=13,glow=0.8,halo=0.0)
        if i in REMNANT:
            R_=[(O[0]+(x-350)*S,O[1]+(y-212)*S) for x,y in REMNANT[i]]
            cv.add([draw.stem(R_,0.32)],'#8A6A3A','#5A4424',0.35,alpha=0.9)
    cv.add([ellipse_ruffle((O[0],O[1]+0.4),1.6,1.1,0,0.06,5)],mix(p['stem'],'#FFFFFF',0.2),p['stem'],0.6)
    flower(cv,(44,9),40,1.05,p,blurs=(0.5,0.42,0.8))
    return cv.render(p['ground'],seed=13)
if __name__=='__main__':
    import sys
    for k,f in (('01',comp01),('02',comp02),('03',comp03)):
        f().save(f'art-{k}.png'); print(k)
