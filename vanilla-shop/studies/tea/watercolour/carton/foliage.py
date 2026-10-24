# Vanilla Tea (Sage), foliage direction: tea branches in three depths (far pale, middle, near crisp) that thin out
# into the paper, the vanilla bloom, buds and pods in front. Painted crisp: anti-aliased edges (no blur, no halo),
# two-tone leaves, mottled pigment, granulation, transparent glazes that darken where they overlap, paper tooth.
import sys, os, math, shutil
sys.path.insert(0,'/home/user/PersonalEventPlanner305App/vanilla-shop/studies/extract/split')
sys.path.insert(0,'/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/teaart')
import numpy as np, cv2
from PIL import Image, ImageDraw
import draw
from draw import leaf, bud, ribbon, arc
from comp import flower, mix
from split2 import WC, pod_pair, serrate
from blot2 import paint_wash, lift, fbm, smooth
from greens import pal, C
K=draw.K; B=3; PAPER=np.array([0xF6,0xEE,0xDC],np.float32)
ROOT='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/teaart/'
def rgb(c): return np.array([int(c[i:i+2],16) for i in (1,3,5)],np.float32)

class Paint:
    def __init__(s,Wmm,Hmm,seed=1):
        s.W,s.H=int(Wmm*K),int(Hmm*K); s.rng=np.random.default_rng(seed)
        s.mott=fbm(s.H,s.W,int(4*K),seed+1)            # wet-in-wet: pigment never lies evenly
        s.gran=fbm(s.H,s.W,3,seed+2,2)                  # granulation, at the scale of the paper
        s.tooth=fbm(s.H,s.W,int(0.25*K),seed+3,2)       # cold-pressed paper
        s.layer=None
    def begin(s,fm): s.acc=np.ones((s.H,s.W,3),np.float32); s.cov=np.zeros((s.H,s.W),np.float32); s.fm=fm
    def at(s,poly):
        c=np.asarray(poly).mean(0); return float(s.fm[min(s.H-1,max(0,int(c[1]*K))),min(s.W-1,max(0,int(c[0]*K)))])
    def mask(s,poly):
        P=np.asarray(poly,float)*K; x0,y0=np.floor(P.min(0)).astype(int)-2; x1,y1=np.ceil(P.max(0)).astype(int)+2
        x0,y0=max(x0,0),max(y0,0); x1,y1=min(x1,s.W),min(y1,s.H)
        if x1<=x0 or y1<=y0: return None
        ss=3; im=Image.new('L',((x1-x0)*ss,(y1-y0)*ss),0)
        ImageDraw.Draw(im).polygon([tuple(v) for v in (P-[x0,y0])*ss],fill=255)
        m=np.asarray(im.resize((x1-x0,y1-y0),Image.BOX)).astype(np.float32)/255
        return m,(slice(y0,y1),slice(x0,x1))
    def glaze(s,poly,col,a=1.0,mott=0.10):
        """a transparent wash: multiplies into what is under it, so overlaps darken like real glazes"""
        r=s.mask(poly)
        if r is None: return
        m,sl=r; c=rgb(col)/PAPER
        f=1+mott*s.mott[sl]; al=m*a*np.clip(0.93+0.12*s.gran[sl]+0.05*s.tooth[sl],0,1.2)
        g=1-al[...,None]*(1-np.clip(c*f[...,None],0,1.0))
        s.acc[sl]*=g; s.cov[sl]=np.maximum(s.cov[sl],m*a)
    def leaf2(s,q,col,deep,a=1.0,rib=True,seed=0):
        """a two-tone tea leaf: the lit half and the shaded half meet at a crisp, paler midrib"""
        full=serrate(leaf(*q),q[3],seed,0.45); sp=leaf(*q,spine=True); n=len(sp)
        a=a*s.at(full)   # each leaf painted at one dilution: far ones thin, near ones strong
        if a<0.03: return
        s.glaze(full,col,a)
        s.glaze(np.vstack([full[:n],sp[::-1]]),mix('#FFFFFF',deep,0.35),a*0.9,0.14)
        if rib:
            vr=ribbon(sp[2:-3],lambda t,w=q[3]*0.035:w*(1-0.7*t)+0.02)
            s.lift_line(vr,0.45*a)
    def lift_line(s,poly,a):
        """lifting pigment back off with a damp brush: a paler line"""
        r=s.mask(poly)
        if r is None: return
        m,sl=r; s.acc[sl]=s.acc[sl]*(1-m[...,None]*a)+m[...,None]*a*np.maximum(s.acc[sl],0.97)
    def stem(s,sp,w,col,a):
        poly=ribbon(sp,lambda t:w*(1-0.6*t)+0.03); s.glaze(poly,col,a*s.at(poly),0.05)
    def merge(s,base,fade):
        """lay the finished layer on the picture, thinned by the fade (transparency, never blur)"""
        return base*s.acc

def fade(P,cx,cy,rx,ry,seed,cap=1.0,inner=0.5):
    yy,xx=np.mgrid[0:P.H,0:P.W].astype(np.float32)/K
    d=np.hypot((xx-cx)/rx,(yy-cy)/ry)+0.5*fbm(P.H,P.W,int(14*K),seed)+0.16*fbm(P.H,P.W,int(3*K),seed+1)
    return smooth(1.0,inner,d)*cap

def branch(P,p0,ang,L,bend,lmax,cols,deep,a,seed,rib=True,tip=True):
    rng=np.random.default_rng(seed)
    sp=arc(p0,ang,L,bend*1.6,n=6,twist=rng.uniform(-0.4,0.4))
    if rib: P.stem(sp[:int(len(sp)*0.93)],lmax*0.02,mix(cols[0],deep,0.55),a*0.7)
    d=np.gradient(sp,axis=0); k=max(3,int(L/lmax*3.2)); side=1
    for i,t in enumerate(np.linspace(0.16,0.9,k)):
        j=int(t*(len(sp)-1)); da=math.degrees(math.atan2(d[j][1],d[j][0]))
        Ls=lmax*(1-0.45*t)*rng.uniform(0.82,1.08)
        q=(tuple(sp[j]+rng.normal(0,0.5,2)),da+side*rng.uniform(30,72)+rng.normal(0,10),Ls,Ls*rng.uniform(0.29,0.33),side*rng.uniform(0.08,0.3))
        P.leaf2(q,cols[rng.integers(len(cols))],deep,a,rib,seed*31+i); side=-side
    if tip:
        da=math.degrees(math.atan2(d[-1][1],d[-1][0]))
        bp=bud(tuple(sp[-1]),da,lmax*0.42,lmax*0.11,0.1); P.glaze(bp,mix(cols[0],'#FFFFFF',0.25),a*P.at(bp))

BACK=['#C2CDAE','#B3C29E','#CBD3B8']; MID=['#97AC82','#86A070','#A5B78F']; FRONT=['#7A9668','#6C8A5C','#88A174']
DEEPB,DEEPM,DEEPF='#9DB08A','#5E7A4E','#3F5C38'
CREAM,CREAME='#F5EDD2','#D8C48C'

def paint(name,FW,SW,spec,O):
    W=B+FW+SW+B; H=85+2*B; f=FW+3
    P=Paint(W,H,seed=7); h,w=P.H,P.W
    base=paint_wash(h,w,PAPER,[(spec['haze'],1.0,'#E9EEDF',0.45,0.7)],seed=5)
    fr=spec['focal']; sd=spec['side']
    for lay,cols,deep,(sx,sy,cap),ribs in (('back',BACK,DEEPB,(1.25,1.2,0.75),False),('mid',MID,DEEPM,(1.05,1.0,0.78),True),('front',FRONT,DEEPF,(0.9,0.9,0.92),True)):
        fm=np.maximum(fade(P,fr[0],fr[1],fr[2]*sx,fr[3]*sy,11,cap),fade(P,sd[0],sd[1],sd[2]*sx,sd[3]*sy,13,cap*sd[4])); P.begin(fm)
        for i,(p0,ang,L,bend,lm) in enumerate(spec[lay]): branch(P,p0,ang,L,bend,lm,cols,deep,1.0,hash((name,lay,i))%9999,ribs)
        base=P.merge(base,fm)
    cv=WC(int(W)+1,H); cv.crisp=True; cv.cap=0.03; pod_pair(cv,spec['p'],*spec['pod'])
    for (p0,ang,L) in spec['vbuds']:   # vanilla buds, cream, on fine green stems
        sp=arc(p0,ang+180,L*0.9,0.2,n=4); cv.add([ribbon(sp,lambda t:0.32)],'#8FA77A','#6F8C5E',0.03,wash=())
        cv.add([bud(p0,ang,L,L*0.3,0.08)],CREAM,CREAME,0.03,glow=1.2,wash=())
    flower(cv,*spec['flower'],spec['p'],blurs=(0.04,0.03,0.05))
    col,al=lift(cv); al=al[:h,:w]; base=base*(1-al[...,None])+col[:h,:w]*al[...,None]
    base*= (1+0.012*P.tooth)[...,None]; base+=np.random.default_rng(3).normal(0,1.0,(h,w))[...,None]
    out=base.clip(0,255).astype(np.uint8); fx=int((FW+B)*K)
    Image.fromarray(out[:,:int((FW+2*B)*K)]).save(O+f'{name}-front.png'); Image.fromarray(out[:,fx:]).save(O+f'{name}-side.png')

p=pal('#6E8C6A'); p.update(pod_core='#5E3E26',pod_edge='#3A2414',tep_edge='#E6EDE2')
def cube(O):
    FW,SW=87.6,84.6; f=FW+3
    spec=dict(p=p,focal=(f-18,58,40,36),side=(f+36,84,44,22,0.5),
        haze=[C(70,56,30,32),C(118,80,30,12)],
        back=[((f-10,99),-120,70,0.25,24),((f+6,99),-95,72,-0.15,24),((f-40,99),-70,60,0.3,22),((f+30,99),-115,62,0.2,22),((f+62,99),-100,52,0.1,20),((f-2,70),-150,40,0.2,20),((f-26,66),-118,34,0.3,18),((f+12,58),-128,36,0.2,18)],
        mid=[((f-14,99),-110,60,0.3,21),((f-48,99),-62,46,-0.2,19),((f+8,90),-140,48,0.15,19),((f+24,99),-100,40,0.1,17),((f-30,99),-90,50,0.15,19)],
        front=[((f-26,97),-125,40,0.25,16),((f-48,95),-70,30,-0.2,15),((f+2,97),-105,30,0.2,15)],
        pod=((f-62,88),-18,66,2.1),
        vbuds=[((f-8,42),-50,6.5),((f-44,66),200,5.5)],
        flower=((f-21,60),40,1.75))
    paint('cube',FW,SW,spec,O)
def long(O):
    FW,SW=175.9,85.1; f=FW+3
    spec=dict(p=p,focal=(f-48,50,66,46),side=(f+40,82,46,24,0.5),
        haze=[C(128,50,56,40),C(220,78,40,14)],
        back=[((f-20,99),-120,95,0.25,30),((f+8,99),-95,90,-0.15,30),((f-60,99),-65,80,0.3,28),((f+34,99),-115,80,0.2,28),((f+66,99),-100,60,0.1,24),((f-6,62),-155,55,0.2,26),((f-100,99),-50,60,0.2,24),((f-40,60),-112,46,0.3,24),((f+14,52),-128,48,0.2,22)],
        mid=[((f-26,99),-112,80,0.3,26),((f-74,99),-62,62,-0.2,24),((f+8,90),-142,62,0.15,24),((f+28,99),-100,52,0.1,22),((f-46,99),-92,66,0.15,24)],
        front=[((f-36,97),-126,52,0.25,20),((f-80,95),-68,40,-0.2,18),((f-6,97),-106,40,0.2,18)],
        pod=((f-118,90),-17,100,2.6),
        vbuds=[((f-34,32),-45,8.5),((f-92,58),205,7.5)],
        flower=((f-60,50),40,2.5))
    paint('long',FW,SW,spec,O)
if __name__=='__main__':
    O=ROOT+'fol/'; {'cube':cube,'long':long}[sys.argv[1]](O)
    shutil.copy(ROOT+'bw2/paper.jpg',O+'paper.jpg'); shutil.copy(ROOT+'bw2/paper.jpg',O+'paper-lid.jpg'); print('ok',sys.argv[1])
