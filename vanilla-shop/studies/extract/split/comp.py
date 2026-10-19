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
def bunch_pod(o,spread,L,W,drift,seed,curve=0.0):
    """one green pod of a hanging bunch: a short stalk leaves the node outward, turns over, then the pod hangs"""
    ox,oy=o
    pts=[(ox,oy),(ox+spread*2.6,oy-2.4),(ox+spread*5.2,oy-1.4),(ox+spread*6.4+drift*0.15,oy+3.2),
         (ox+spread*6.9+drift*0.5+curve,oy+L*0.42),(ox+spread*7.1+drift*0.8+curve*1.4,oy+L*0.75),(ox+spread*7.0+drift+curve,oy+L)]
    sp=draw.cr(pts,22)
    def prof(t):
        if t<0.17: return 0.42
        if t<0.25: return 0.42+(W-0.42)*(0.5-0.5*np.cos(np.pi*(t-0.17)/0.08))
        w=W*(1+0.06*np.sin(np.pi*(t-0.25)/0.75))
        if t>0.94: w*=np.sqrt(max(0,1-((t-0.94)/0.06)**2))
        return w+0.03
    body=draw.ribbon(sp,prof,0.004,3,seed)
    rib=sp[int(len(sp)*0.27):int(len(sp)*0.93)]+np.array([-W*0.38,0])
    return body,rib,sp[-1]
def comp03(W=60,H=70,ox=0):
    """No. 03, syrup: a bunch of green pods hanging from one node, after real vines;
    three depths of pods, the back ones deeper and softer, a few tips ripening to gold"""
    p=PAL['03']; cv=Canvas(W,H,ox)
    node=(26,8.5)
    cv.add([leaf((node[0]+5,node[1]+2),64,52,9.6,-0.3)],'#4F8A4E','#1C3A22',1.1,glow=0.8,halo=0.15)
    sheen(cv,[leaf((node[0]+5,node[1]+2),64,52,9.6,-0.3,spine=True)],0.45,'#7FB070','#4F8A4E',1.1,0.5)
    leaves(cv,p,[((node[0]-2,node[1]-1),196,28,6.2,-0.4)],2.6,0.8)
    cv.add([stem([(-4,3),(12,6.5),(node[0],node[1]),(44,5),(66,3)],1.0)],mix(p['stem'],'#FFFFFF',0.1),p['stem'],1.2)
    rows=[  # (spread, length, half-width, drift, curve)
      ([(-1.7,40,1.5,-4.5,0.8),(-0.8,47,1.55,-2.2,-0.5),(0.6,45,1.55,1.4,0.6),(1.6,38,1.45,4.2,-0.6)],1.2,0.5),
      ([(-1.25,50,1.65,-3.4,-0.7),(-0.1,56,1.7,-0.6,0.5),(1.0,52,1.65,2.6,-0.4),(2.0,43,1.55,5.0,0.7)],0.7,0.22),
      ([(-0.55,54,1.8,-1.6,0.6),(0.5,57,1.85,1.2,-0.6),(1.45,48,1.75,3.6,0.4),(-1.6,45,1.7,-4.2,-0.5)],0.35,0.0)]
    gold=[]
    for ri,(row,blur,dark) in enumerate(rows):
        parts=[bunch_pod(node,s_,L,w,d,ri*10+i,cu) for i,(s_,L,w,d,cu) in enumerate(row)]
        core=mix(p['pod_core'],p['pod_edge'],dark); edge=mix(p['pod_edge'],p['ground'],dark*0.6)
        tones=[0.0,0.18,-0.12,0.1,-0.06]
        for i,q in enumerate(parts):         # each pod on its own, so it keeps its own rim; no two quite the same green
            tj=tones[i%len(tones)]; cc=mix(core,'#E4F0C0',tj) if tj>0 else mix(core,'#7FA866',-tj)
            cv.add([q[0]],cc,edge,blur,glow=0.65,halo=0.06)
            sheen(cv,[q[1]],0.42,'#EEF6D8',core,blur,0.5*(1-dark))
        if ri==2: gold=[(q[0],q[2]) for q in parts[:3]]
        if ri==1: gold.append((parts[1][0],parts[1][2]))
    # ripening: gold creeping up from the tip, faded into the green
    for poly,tipxy in gold:
        cv.add([poly],'#F2CF63',p['pod_core'],0.4,alpha=0.85,centre=tuple(tipxy),R=15,glow=0.7,halo=0.0)
    cv.add([ellipse_ruffle(node,1.3,1.0,0,0.05,5)],mix(p['stem'],'#FFFFFF',0.2),p['stem'],0.7)
    flower(cv,(46,17),40,0.8,p,blurs=(0.9,0.8,1.0))
    return cv.render(p['ground'],seed=13)
if __name__=='__main__':
    import sys
    for k,f in (('01',comp01),('02',comp02),('03',comp03)):
        f().save(f'art-{k}.png'); print(k)
