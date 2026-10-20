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
        [(458,128),(470,400),(472,640)],[(470,90),(560,150),(640,230),(700,320)]]
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
