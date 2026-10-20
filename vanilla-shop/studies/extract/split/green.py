# Three compositions for No. 03 with the lit pods (pod3d). Each returns an RGB image; W, H in mm, ox = panel offset.
import numpy as np
from PIL import Image
import draw, pod3d, comp
from draw import Canvas, leaf, stem, bud, ellipse_ruffle
from comp import PAL, mix, flower
P=PAL['03']; G='#2F5A33'
def back_layers(cv): return cv.render(G,grain=0,raw=True)
def finish(cv_front,img,seed):
    img=cv_front.render(G,grain=0,raw=True,base=img) if cv_front else img
    img+=np.random.default_rng(seed).normal(0,1,img.shape[:2]).astype(np.float32)[...,None]*8
    return Image.fromarray(img.clip(0,255).astype(np.uint8))
TIP='#EBD27A'
def podset(spec):
    """spec: (points, half-width, depth, tip, curl, blur)"""
    out=[]
    for pts,w,dep,tip,curl,bl in spec:
        g=pod3d.pod_geom(pts,w,tip,curl); out.append((g,pod3d.depth_pal(dep,G,TIP if dep>=0.95 else None),dep,bl))
    return out
# ---------- A: the hanging bunch (reference layout), refined
def optA(W=60,H=70,ox=0):
    s=60/1161; rp=lambda p:(p[0]*s,p[1]*s)
    cv=Canvas(W,H,ox)
    cv.add([leaf(rp((455,130)),116,50,8.6,0.14)],'#5C9656','#2E5C33',0.8,alpha=0.95,glow=0.9,halo=0.08)
    comp.sheen(cv,[leaf(rp((455,130)),116,50,8.6,0.14,spine=True)],0.35,'#7AB06E','#5C9656',0.8,0.35)
    ST=[[(462,0),(466,70),(458,128)],[(458,128),(440,160),(425,195)],[(458,128),(462,160),(460,185)],
        [(470,140),(505,200),(530,260),(560,285)],[(505,200),(530,280),(535,360)],[(458,128),(480,300),(493,560)],
        [(458,128),(470,400),(472,640)],[(470,90),(560,170),(640,300),(700,440)]]
    cv.add([stem([rp(q) for q in s_],0.8 if i==0 else 0.62) for i,s_ in enumerate(ST)],'#B4D290','#56864C',0.15,glow=1.0,halo=0.04)
    cv.add([ellipse_ruffle(rp(k),0.95,0.55,20,0.04,5) for k in [(458,128),(447,146),(505,200),(538,268)]],'#D2E6AE','#6E9C5C',0.15,halo=0.0)
    flower(cv,rp((805,300)),22,1.0,P,blurs=(0.35,0.3,0.6))
    img=back_layers(cv)
    R=lambda pts:[rp(q) for q in pts]
    pods=podset([(R([(472,640),(452,800),(432,975)]),1.8,0.1,'point',0,0.55),
                 (R([(535,360),(552,480),(575,650)]),1.85,0.25,'point',0,0.4),
                 (R([(493,560),(505,780),(545,960),(590,1095)]),2.2,0.45,'point',0,0.25),
                 (R([(425,195),(418,420),(392,650),(340,860)]),2.3,0.6,'point',0,0.12),
                 (R([(560,285),(630,430),(710,600),(768,765)]),2.3,0.75,'point',0,0.08),
                 (R([(460,185),(468,420),(560,720),(690,960),(765,1245)]),2.8,1.0,'point',0,0.0)])
    img=pod3d.composite(img,pods,ox,grain=0)
    return finish(None,img,13)
# ---------- B: the banana sweep: the bunch slanted right, crescent pods, one crossing the other way, two tips curled
def optB(W=60,H=70,ox=0):
    cv=Canvas(W,H,ox); X,Y=20,4
    cv.add([leaf((X+1,Y+2),112,46,8.0,0.25)],'#5C9656','#2E5C33',1.3,alpha=0.9,glow=0.9,halo=0.08)
    cv.add([stem([(X-8,-4),(X-3,1),(X,Y)],0.8)],'#B4D290','#56864C',0.15,glow=1.0)
    cv.add([ellipse_ruffle((X,Y),1.2,0.8,30,0.04,5)],'#D2E6AE','#6E9C5C',0.15,halo=0.0)
    img=back_layers(cv)
    def cres(dx_top,ang,L,bow,curve=1):
        a=np.radians(ang); d=np.array([np.sin(a),np.cos(a)]); n=np.array([d[1],-d[0]])*curve
        S=np.array([X+dx_top,Y+1.5]); E=S+d*L
        return [tuple(S),tuple(S+d*L*0.35+n*bow*0.8),tuple(S+d*L*0.7+n*bow),tuple(E)]
    pods=podset([(cres(-1.0,2,44,-2.4,-1),1.8,0.1,'round',-35,0.55),
                 (cres(0.5,46,40,3.0),1.8,0.2,'point',0,0.45),
                 (cres(-0.6,26,52,4.0),2.0,0.4,'point',0,0.25),
                 (cres(1.4,12,50,-2.8,-1),2.0,0.55,'point',0,0.18),
                 (cres(0.8,40,50,4.2),2.1,0.7,'round',80,0.1),
                 (cres(0.2,32,58,4.6),2.3,0.85,'point',0,0.05),
                 (cres(1.0,37,47,4.0),2.2,1.0,'point',0,0.0)])
    img=pod3d.composite(img,pods,ox,grain=0)
    cf=Canvas(W,H,ox); flower(cf,(44,14),28,1.35,P,blurs=(0.4,0.34,0.66))
    return finish(cf,img,14)
# ---------- C: No. 01's formula done properly: three huge pods cropped by the frame, sweeping diagonally, flower over them
def optC(W=60,H=70,ox=0):
    cv=Canvas(W,H,ox)
    cv.add([leaf((-4,8),28,60,11,0.25)],'#4E8A50','#2B5532',2.6,alpha=0.85,glow=0.9,halo=0.08)
    img=back_layers(cv)
    pods=podset([([(-6,30),(14,44),(36,58),(62,66)],3.2,0.35,'point',0,0.5),
                 ([(-8,12),(16,30),(40,50),(58,74)],3.7,0.7,'point',0,0.15),
                 ([(4,-6),(20,16),(34,40),(44,76)],4.0,1.0,'point',0,0.0)])
    img=pod3d.composite(img,pods,ox,grain=0)
    cf=Canvas(W,H,ox); flower(cf,(33,30),30,1.9,P,blurs=(0.42,0.36,0.7))
    return finish(cf,img,15)
# ---------- D: pods painted like the flower: airbrushed glow, a soft light line down the middle (like the tepals'
# midribs), a dark halo underneath for separation, rounded tips with a small nub. Shapes after the stamp: nearly
# straight, almost parallel, close-packed, the body swelling slightly; the leftmost only gently curved.
def hermite(top,tip,a0,a1,n=200):
    """one cubic between two ends with a set direction at each (degrees from straight down, + towards the right).
    With a0 <= a1 the curve turns one way only: a single clean arc, no wobble."""
    P0,P1=np.array(top,float),np.array(tip,float); L=np.linalg.norm(P1-P0)
    T0=np.array([np.sin(np.radians(a0)),np.cos(np.radians(a0))])*L; T1=np.array([np.sin(np.radians(a1)),np.cos(np.radians(a1))])*L
    t=np.linspace(0,1,n)[:,None]
    return (2*t**3-3*t**2+1)*P0+(t**3-2*t**2+t)*T0+(-2*t**3+3*t**2)*P1+(t**3-t**2)*T1
def pod_shape(pts,W,n=400):
    """a pod as an illustrator draws it: narrow out of the stalk, swelling to its widest about a third of the way
    down, a long gentle taper, then a blunt rounded end"""
    sp=pts if isinstance(pts,np.ndarray) else draw.cr(pts,60)
    L=np.concatenate([[0],np.cumsum(np.linalg.norm(np.diff(sp,axis=0),axis=1))]); u=np.linspace(0,L[-1],n)
    sp=np.stack([np.interp(u,L,sp[:,0]),np.interp(u,L,sp[:,1])],1); t=u/L[-1]
    w=np.where(t<0.08,0.3+(0.55*W-0.3)*t/0.08,
       np.where(t<0.35,W*(0.55+0.45*np.sin(np.pi/2*(t-0.08)/0.27)),W*(1-0.32*((t-0.35)/0.65)**1.6)))
    w=np.where(t>0.94,w*np.sqrt(np.clip(1-((t-0.94)/0.06)**2,0.03,1)),w)
    d=np.gradient(sp,axis=0); d/=np.linalg.norm(d,axis=1,keepdims=True); nr=np.stack([-d[:,1],d[:,0]],1)
    return sp,w,nr,d
def soft_pods(cv,spec,ox=0):
    for pts,W,dep in sorted(spec,key=lambda q:q[2]):
        sp,w,nr,d=pod_shape(pts,W)
        poly=np.vstack([sp+nr*w[:,None],(sp-nr*w[:,None])[::-1]])
        bl=0.2+(1-dep)*0.7
        wh=w+0.4; halo=np.vstack([sp+nr*wh[:,None],(sp-nr*wh[:,None])[::-1]])
        cv.add([halo],'#183A20','#183A20',0.4+bl*0.4,alpha=0.6*(0.4+0.6*dep),halo=0.0)
        core=mix('#CDE3A2','#A9C98A',(1-dep)*0.5); edge=mix('#5A8D4A','#4A7C42',(1-dep)*0.5)
        cv.add([poly],core,edge,bl,glow=0.95,halo=0.04)
        n=len(sp); i0,i1=int(n*0.1),int(n*0.9)
        mid=sp[i0:i1]+nr[i0:i1]*(w[i0:i1,None]*0.22)
        cv.add([draw.ribbon(mid,lambda t,ww=W:ww*0.17*np.sin(np.pi*t)**0.7+0.03)],'#F4FADF',core,bl*0.9,alpha=0.55*(0.5+0.5*dep),halo=0.0)
        tip=sp[-1]-d[-1]*0.1
        cv.add([ellipse_ruffle(tuple(tip),W*0.3,W*0.24,0,0.03,5)],'#B5B860',edge,bl*0.7,alpha=0.75,halo=0.0)
def optD(W=60,H=70,ox=0):
    s=60/1161; rp=lambda p:(p[0]*s,p[1]*s); R=lambda pts:[rp(q) for q in pts]
    cv=Canvas(W,H,ox)
    cv.add([leaf(rp((455,130)),116,50,8.6,0.14)],'#5C9656','#2E5C33',1.0,alpha=0.9,glow=0.9,halo=0.08)
    ST=[[(462,0),(466,70),(458,128)],[(458,128),(445,160),(432,195)],[(458,128),(462,160),(462,185)],
        [(470,140),(505,200),(530,250),(552,280)],[(505,200),(522,270),(528,330)],[(470,90),(560,170),(640,300),(700,440)]]
    cv.add([stem([rp(q) for q in s_],0.8 if i==0 else 0.6) for i,s_ in enumerate(ST)],'#C2DC9E','#6E9C5C',0.35,glow=1.0,halo=0.04)
    cv.add([ellipse_ruffle(rp(k),0.95,0.55,20,0.04,5) for k in [(458,128),(447,146),(505,200),(528,262)]],'#DCEBBA','#7FAA66',0.3,halo=0.0)
    flower(cv,rp((805,300)),22,1.0,P,blurs=(0.42,0.36,0.72))
    soft_pods(cv,[(R([(476,600),(472,780),(460,960)]),2.0,0.1),
                  (R([(528,330),(540,470),(552,640),(560,780)]),2.1,0.3),
                  (R([(500,520),(510,720),(528,900),(548,1070)]),2.3,0.45),
                  (R([(432,195),(424,420),(410,640),(392,860)]),2.3,0.6),
                  (R([(552,280),(588,430),(622,580),(650,740)]),2.3,0.75),
                  (R([(462,185),(476,430),(516,720),(566,980),(604,1220)]),2.75,1.0)],ox)
    return cv.render(G,seed=16)
# ---------- E: the same composition, the pods painted by one of the four styles in podstyles.py
# each pod: top (px on the reference), tip (px), direction at the top, direction at the tip, half-width (mm), depth
POD_H=[((472,640),(446,975),-2,-6,1.85,0.1),((535,360),(572,650),4,10,1.9,0.25),
       ((493,560),(588,1095),2,18,2.05,0.45),((425,195),(392,860),-1,-6,2.05,0.6),
       ((560,285),(766,765),10,34,2.05,0.75),((460,185),(762,1245),-4,34,2.35,1.0)]
FLOWER_AT=(37,23.5); FLOWER_S=1.55
def optE(style,W=60,H=70,ox=0):
    import podstyles as ps
    s=60/1161; rp=lambda p:(p[0]*s,p[1]*s)
    cv=Canvas(W,H,ox)
    cv.add([leaf(rp((455,130)),116,50,8.6,0.14)],'#5C9656','#2E5C33',1.0,alpha=0.9,glow=0.9,halo=0.08)
    ST=[[(462,0),(466,70),(458,128)],[(458,128),(440,160),(425,195)],[(458,128),(462,160),(460,185)],
        [(470,140),(505,200),(530,260),(560,285)],[(505,200),(530,280),(535,360)],[(458,128),(480,300),(493,560)],
        [(458,128),(470,400),(472,640)],[(470,90),(560,170),(640,300),(700,440)]]
    cv.add([stem([rp(q) for q in s_],0.8 if i==0 else 0.6) for i,s_ in enumerate(ST)],'#C2DC9E','#6E9C5C',0.16,glow=1.0,halo=0.04)
    cv.add([ellipse_ruffle(rp(k),0.95,0.55,20,0.04,5) for k in [(458,128),(447,146),(505,200),(538,268)]],'#DCEBBA','#7FAA66',0.12,halo=0.0)
    flower(cv,FLOWER_AT,22,FLOWER_S,P,blurs=(0.42,0.36,0.72))
    img=cv.render(G,grain=0,raw=True)
    import cv2
    under=np.zeros(img.shape[:2],np.float32)                 # coverage of the pods painted so far
    for i,(top,tip,a0,a1,Wd,dep) in enumerate(sorted(POD_H,key=lambda q:q[5])):
        sp,w,nr,d=pod_shape(hermite(rp(top),rp(tip),a0,a1),Wd)
        pod=ps.Pod(sp,w,nr,H*20,W*20,ox)
        ps.halo(img,pod,dep)
        # paint the pod on its own layer, then give it the flower's softness
        cap={}
        orig=ps.put; ps.put=lambda im,pd,rgb,a: cap.update(rgb=rgb.astype(np.float32),a=a.astype(np.float32))
        ps.STYLES[style](img,pod,dep,seed=i*7+3); ps.put=orig
        rgb,a=cap['rgb'],cap['a']
        sharp=0.2+(1-dep)*0.5; soft=sharp+0.3+(1-dep)*0.4          # mm, as the tepals (0.42) and back tepals
        r1,a1=ps.soften(rgb,a,sharp); r2,a2=ps.soften(rgb,a,soft)
        rng=np.random.default_rng(i+11); f0=rng.uniform(0.25,0.7); fw=rng.uniform(0.25,0.4)
        f=np.clip(np.exp(-((pod.tt-f0)/fw)**2)*(0.55+0.45*dep)*1.6,0,1)
        f=np.maximum(f,np.exp(-(pod.tt/0.13)**2)*(0.75+0.25*dep))                    # the attachment
        if dep>=0.55:                                                                # crisp where it crosses a pod
            ov=under[pod.y0:pod.y1,pod.x0:pod.x1]
            f=np.maximum(f,np.clip(ov*1.6,0,1)*0.9)
        f=cv2.GaussianBlur(f.astype(np.float32),(0,0),14)
        rr=r1*f[...,None]+r2*(1-f[...,None]); aa=a1*f+a2*(1-f)
        glow=cv2.GaussianBlur(a,(0,0),soft*2.8*20)*0.22*(0.5+0.5*dep)    # the faint glow past the edge
        lt=ps.ramp(dep)['light']
        orig(img,pod,np.broadcast_to(lt,glow.shape+(3,)).astype(np.float32),glow)
        orig(img,pod,rr,aa)
        u=under[pod.y0:pod.y1,pod.x0:pod.x1]; u[:]=np.maximum(u,a)
        tip=sp[-1]-d[-1]*0.1+[ox,0]; cv2_tip(img,tip,Wd*0.28,dep)
    img+=np.random.default_rng(16).normal(0,1,img.shape[:2]).astype(np.float32)[...,None]*8
    return Image.fromarray(img.clip(0,255).astype(np.uint8))
def cv2_tip(img,c,r,dep):
    import cv2
    m=np.zeros(img.shape[:2],np.float32); cv2.circle(m,(int(c[0]*20),int(c[1]*20)),int(r*20),1.0,-1,cv2.LINE_AA)
    m=cv2.GaussianBlur(m,(0,0),7+(1-dep)*10)*0.45
    img[:]=img*(1-m[...,None])+np.array([181,184,96],np.float32)*m[...,None]
