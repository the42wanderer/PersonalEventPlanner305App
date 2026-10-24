# Vanilla Tea (Sage), refinement pass of the foliage direction. Same composition and palette; better execution:
# botanical tea leaves (petiole, elliptic blade, acute tip, fine teeth, uneven halves, lit from the top left),
# alternate leaves at irregular spacing, every leaf on a stem, "two leaves and a bud" at the tips, gentle overlaps
# (no muddy multiplying), text kept clear, and the flower and pods painted with the same brush: flat washes and
# crisp shadow shapes in the same sage, no airbrush, no gloss.
import sys, os, math, shutil
sys.path.insert(0,'/home/user/PersonalEventPlanner305App/vanilla-shop/studies/extract/split')
sys.path.insert(0,'/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/teaart')
import numpy as np
from PIL import Image, ImageDraw
import draw
from draw import bud, ribbon, arc, tepal, trumpet, ellipse_ruffle, pod
from comp import mix
from blot2 import paint_wash, fbm, smooth
K=draw.K; B=3; PAPER=np.array([0xF6,0xEE,0xDC],np.float32)
ROOT='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/teaart/'
def rgb(c): return np.array([int(c[i:i+2],16) for i in (1,3,5)],np.float32)
LIGHT=np.array([1.0,1.0])/math.sqrt(2)    # shade falls to the lower right

class Paint:
    def __init__(s,Wmm,Hmm,seed=1):
        s.W,s.H=int(Wmm*K),int(Hmm*K)
        s.mott=fbm(s.H,s.W,int(4*K),seed+1); s.gran=fbm(s.H,s.W,3,seed+2,2); s.tooth=fbm(s.H,s.W,int(0.25*K),seed+3,2)
        s.safe=[]
    # ---- rasterising
    def box(s,polys,pad=2):
        P=np.vstack([np.asarray(p,float) for p in polys])*K
        x0,y0=np.floor(P.min(0)).astype(int)-pad; x1,y1=np.ceil(P.max(0)).astype(int)+pad
        x0,y0,x1,y1=max(x0,0),max(y0,0),min(x1,s.W),min(y1,s.H)
        return None if x1<=x0 or y1<=y0 else (x0,y0,x1,y1)
    def m(s,poly,bx,ss=3):
        x0,y0,x1,y1=bx; im=Image.new('L',((x1-x0)*ss,(y1-y0)*ss),0)
        ImageDraw.Draw(im).polygon([tuple(v) for v in (np.asarray(poly,float)*K-[x0,y0])*ss],fill=255)
        return np.asarray(im.resize((x1-x0,y1-y0),Image.BOX)).astype(np.float32)/255
    def sl(s,bx): return (slice(bx[1],bx[3]),slice(bx[0],bx[2]))
    def tex(s,sl,g=0.12): return np.clip(0.93+g*s.gran[sl]+0.05*s.tooth[sl],0,1.2)
    # ---- where a shape may be strong: the fade (one dilution per shape) and the text panels
    def at(s,poly):
        c=np.asarray(poly).mean(0); v=float(s.fm[min(s.H-1,max(0,int(c[1]*K))),min(s.W-1,max(0,int(c[0]*K)))])
        for (x0,y0,x1,y1) in s.safe:
            if x0<=c[0]<=x1 and y0<=c[1]<=y1: v*=0.2
        return v
    def in_safe(s,poly):
        c=np.asarray(poly).mean(0); return any(x0<=c[0]<=x1 and y0<=c[1]<=y1 for (x0,y0,x1,y1) in s.safe)
    # ---- a layer of transparent glazes; overlaps inside a layer darken only a little (no mud)
    def begin(s,fm): s.acc=np.ones((s.H,s.W,3),np.float32); s.fm=fm
    def put(s,bx,g):
        a=s.acc[s.sl(bx)]; lo=np.minimum(a,g); hi=np.maximum(a,g); s.acc[s.sl(bx)]=lo*(1-0.3*(1-hi))
    def end(s,img): return img*s.acc
    def glaze_g(s,mask,col,a,sl,mott=0.05):
        c=rgb(col)/PAPER; f=1+mott*s.mott[sl]; al=mask*a*s.tex(sl)
        return 1-al[...,None]*(1-np.clip(c*f[...,None],0,1.0))
    # ---- opaque-ish paint (the flower, buds, pods) straight onto the picture
    def over(s,img,poly,col,a,mott=0.03):
        bx=s.box([poly]); 
        if bx is None: return
        sl=s.sl(bx); m=s.m(poly,bx)*a*np.clip(0.97+0.05*s.gran[sl],0,1); c=rgb(col)*(1+mott*s.mott[sl])[...,None]
        img[sl]=img[sl]*(1-m[...,None])+c*m[...,None]
    def shade(s,img,poly,shift,col,a,clip=None):
        """a crisp shadow shape: the part of a form that a copy of itself, nudged towards the light, does not cover"""
        bx=s.box([poly])
        if bx is None: return
        sl=s.sl(bx); m=s.m(poly,bx); m2=s.m(np.asarray(poly)-np.asarray(shift),bx); sh=np.clip(m-m2,0,1)
        if clip is not None: sh*=s.m(clip,bx)
        c=rgb(col)/255; al=sh*a*s.tex(sl,0.15)
        img[sl]=img[sl]*(1-al[...,None]*(1-c))
    def wash_in(s,img,poly,clip,col,a):
        bx=s.box([poly])
        if bx is None: return
        sl=s.sl(bx); al=s.m(poly,bx)*s.m(clip,bx)*a*s.tex(sl,0.15); c=rgb(col)/255
        img[sl]=img[sl]*(1-al[...,None]*(1-c))

def fade(P,cx,cy,rx,ry,seed,cap=1.0,inner=0.5):
    yy,xx=np.mgrid[0:P.H,0:P.W].astype(np.float32)/K
    d=np.hypot((xx-cx)/rx,(yy-cy)/ry)+0.45*fbm(P.H,P.W,int(16*K),seed)
    return smooth(1.0,inner,d)*cap

def tealeaf(p0,ang,L,W,bend,rng):
    sp=arc(p0,ang,L,bend,n=5); n=len(sp); t=np.linspace(0,1,n)
    u=np.clip((t-0.07)/0.93,0,1)
    prof=W*np.sin(np.pi*u)**0.82*(1-0.28*u**1.6)+0.03
    prof=np.where(t<0.07,0.05*W+0.04,prof)                      # the petiole
    teeth=(np.mod(t*n/3.2+rng.uniform(),1.0)**2)*0.035*W*((u>0.18)&(u<0.96))
    d=np.gradient(sp,axis=0); d/=np.linalg.norm(d,axis=1,keepdims=True)+1e-9; nrm=np.stack([-d[:,1],d[:,0]],1)
    kl,kr=rng.uniform(0.88,1.0),rng.uniform(0.88,1.0)
    Ls=sp+nrm*(prof*kl+teeth)[:,None]; Rs=sp-nrm*(prof*kr+teeth)[:,None]
    shadeL=float(nrm[n//2]@LIGHT)>0
    half=np.vstack([Ls,sp[::-1]]) if shadeL else np.vstack([Rs,sp[::-1]])
    return np.vstack([Ls,Rs[::-1]]),sp,half,d,nrm,u,prof

def paint_leaf(P,p0,ang,L,W,bend,col,deep,a,rng,veins):
    poly,sp,half,d,nrm,u,prof=tealeaf(p0,ang,L,W,bend,rng)
    a=a*P.at(poly)
    if a<0.04: return
    bx=P.box([poly])
    if bx is None: return
    sl=P.sl(bx); mf=P.m(poly,bx)
    g=P.glaze_g(mf,col,a,sl)*P.glaze_g(P.m(half,bx),deep,a*0.55,sl,0.07)
    if veins:   # lifted out with a damp brush: the midrib, and on near leaves the side veins curving to the tip
        lines=[ribbon(sp[4:-4],lambda t,w=W*0.045:w*(1-0.7*t)+0.015)]
        if veins>1:
            n=len(sp)
            for k in (0.28,0.42,0.56,0.7):
                j=int(k*(n-1)); 
                for sg in (1,-1):
                    e=sp[j]+nrm[j]*sg*prof[j]*0.82+d[j]*prof[j]*0.9
                    lines.append(ribbon(draw.cr([sp[j],(sp[j]+e)/2+d[j]*prof[j]*0.15+nrm[j]*sg*prof[j]*0.1,e],6),lambda t,w=W*0.02:w*(1-t)+0.01))
        for i,ln in enumerate(lines):
            lm=P.m(ln,bx)*mf*(0.55 if i==0 else 0.28)
            g=g+(1-g)*lm[...,None]
    P.put(bx,g)

def branch(P,p0,ang,L,bend,lmax,cols,deep,seed,veins,tip):
    """a tea shoot: alternate leaves at irregular spacing, larger and older at the base, every leaf on the stem"""
    rng=np.random.default_rng(seed)
    sp=arc(p0,ang,L,bend,n=6,twist=rng.uniform(-0.3,0.3)); n=len(sp); d=np.gradient(sp,axis=0)
    ts=[]; t=rng.uniform(0.1,0.2)
    while t<0.86: ts.append(t); t+=rng.uniform(0.11,0.24)*(1.1-0.4*t)
    stemcol=mix(cols[0],deep,0.5)
    for j0,j1 in zip([0]+[int(x*(n-1)) for x in ts],[int(x*(n-1)) for x in ts]+[n-1]):   # the stem, segment by segment
        seg=sp[j0:j1+1]
        if len(seg)<2 or P.in_safe(seg): continue
        a=0.45*P.at(seg)
        if a<0.04: continue
        rib=ribbon(seg,lambda q,w=lmax*0.016*(1-0.5*j0/n):w+0.015); bx=P.box([rib])
        if bx: P.put(bx,P.glaze_g(P.m(rib,bx),stemcol,a,P.sl(bx),0.04))
    side=rng.choice([-1,1])
    for i,t in enumerate(ts):
        if rng.uniform()<0.12: side=-side; continue     # a leaf lost: the rhythm is never even
        j=int(t*(n-1)); da=math.degrees(math.atan2(d[j][1],d[j][0]))
        Ls=lmax*(1-0.42*t)*rng.uniform(0.7,1.12)
        paint_leaf(P,tuple(sp[j]),da+side*(rng.uniform(32,62)-18*t),Ls,Ls*rng.uniform(0.27,0.32),side*rng.uniform(0.05,0.35),
                   cols[rng.integers(len(cols))],deep,1.0,rng,veins)
        side=-side
    da=math.degrees(math.atan2(d[-1][1],d[-1][0]))
    if tip:   # two young leaves and the bud, on the stem's end
        for sg,f in ((1,0.34),(-1,0.27)):
            Ls=lmax*f; paint_leaf(P,tuple(sp[-4]),da+sg*28,Ls,Ls*0.3,sg*0.3,mix(cols[0],'#FFFFFF',0.1),deep,0.9,rng,1 if veins else 0)
        bp=bud(tuple(sp[-1]),da,lmax*0.3,lmax*0.065,0.08); a=0.9*P.at(bp); bx=P.box([bp])
        if bx and a>0.04: P.put(bx,P.glaze_g(P.m(bp,bx),mix(cols[0],'#FFFFFF',0.3),a,P.sl(bx)))
    else:
        paint_leaf(P,tuple(sp[-1]),da,lmax*0.4,lmax*0.12,0.1,cols[0],deep,1.0,rng,0)

# ---- the flower, painted with the same brush: flat washes, crisp sage shadows, lifted midribs
SH='#C3CEBC'; SH2='#AEBCA6'
def paint_flower(P,img,c,ang_lip,s):
    cx,cy=c; spec=[(-97,16.5,2.0,0.26,0.0),(-160,14.8,1.85,-0.36,0.3),(-36,15.6,1.9,0.34,0.25),(126,13.2,1.75,0.30,0.4),(54,13.8,1.8,-0.32,0.35)]
    back={1,3}; order=[1,3,0,2,4]
    hub=ellipse_ruffle((cx,cy),5.2*s,4.6*s,0,0.06,5); inner=ellipse_ruffle((cx,cy),10*s,9*s,20,0.08,5)
    for i in order:
        a,L,W,b,pin=spec[i]; a2=a+ang_lip*0.25; Lf=L*s*(0.8+0.2*abs(np.cos(np.radians(a2-ang_lip))))
        poly=tepal((cx,cy),a2,Lf,W*s,b,0.012,i*0.9,pin); sp=tepal((cx,cy),a2,Lf*0.82,W*s,b,spine=True)
        P.over(img,poly,'#F3F2E8' if i in back else '#FDFCF6',1.0)
        P.shade(img,poly,LIGHT*0.45*s,SH,0.5 if i in back else 0.38,clip=inner)                 # the turned edge in shadow
        P.wash_in(img,poly,hub,SH,0.35 if i in back else 0.22)                       # where the tepals meet the column
        rib=ribbon(sp,lambda t,w=W*s:w*0.12*np.sin(np.pi*t)+0.02); P.over(img,rib,'#FFFFFF',0.65)
    tube,mouth,mc=trumpet((cx,cy),ang_lip,7.5*s,1.1*s,3.6*s,2.6*s,0.13)
    P.over(img,tube,'#F8F6EE',1.0); P.shade(img,tube,LIGHT*0.6*s,SH,0.45)
    P.over(img,mouth,'#FFFEF8',1.0); P.shade(img,mouth,LIGHT*0.5*s,'#E4DDC4',0.55)
    dd=np.array([np.cos(np.radians(ang_lip)),np.sin(np.radians(ang_lip))])
    th=ellipse_ruffle(mc+dd*0.5*s,1.7*s,1.25*s,ang_lip,0.07,7)
    P.over(img,th,'#EFC25C',0.92,0.06); P.shade(img,th,-LIGHT*0.25*s,'#D49A3C',0.45)
    P.over(img,draw.stem([(cx,cy),(cx+dd[0]*2.6*s,cy+dd[1]*2.6*s)],0.4*s),'#FFFFFF',0.6)
def paint_vbud(P,img,p0,ang,L):
    sp=arc(p0,ang+180,L*0.9,0.2,n=4); st=ribbon(sp,lambda t:0.3)
    P.over(img,st,'#8EA47C',0.9); P.shade(img,st,LIGHT*0.15,SH2,0.4)
    b=bud(p0,ang,L,L*0.3,0.08); P.over(img,b,'#F3EBD0',1.0); P.shade(img,b,LIGHT*0.5,'#D7C694',0.6)
    P.over(img,bud(p0,ang,L*0.2,L*0.17,0.0),'#9DB38A',0.85)                        # the green calyx it grows from
def paint_pod(P,img,base,ang,L,w,bend,curl):
    """a cured vanilla pod: slender, near-black brown, matte, with fine lengthwise ridges"""
    poly=pod(base,ang,L,w,bend,curl); sp=pod(base,ang,L,w,bend,spine=True)
    P.over(img,poly,'#4A3122',0.97,0.12)
    P.shade(img,poly,-LIGHT*0.45*w,'#9C8A7E',0.55)                                  # the shadowed underside
    d=np.gradient(sp,axis=0); d/=np.linalg.norm(d,axis=1,keepdims=True)+1e-9; nrm=np.stack([-d[:,1],d[:,0]],1)
    t=np.linspace(0,1,len(sp)); prof=w*(np.minimum(1,t*6))**0.6*(1-0.75*t**3)
    rng=np.random.default_rng(int(L*10))
    for off,col,a in ((-0.45,'#7A5B44',0.35),(-0.1,'#2C1B12',0.35),(0.25,'#6B4C37',0.25),(0.55,'#2C1B12',0.3)):
        wob=np.convolve(rng.normal(0,0.06,len(sp)+6),np.ones(7)/7,'valid')[:len(sp)]
        line=sp+nrm*((off+wob)*prof)[:,None]
        P.over(img,ribbon(line[3:-3],lambda q,ww=w*0.06:ww+0.01),col,a)
    P.over(img,ribbon((sp+nrm*(-0.62*prof)[:,None])[6:-8],lambda q,ww=w*0.05:ww),'#8E7360',0.18)   # a dull, not glossy, highlight

BACK=['#C4CFB1','#B7C5A2','#CCD5BA']; MID=['#9AAE85','#8AA274','#A6B892']; FRONT=['#86A174','#7A9668','#92AA7F']
DEEPB,DEEPM,DEEPF='#A4B592','#667F55','#5A7550'
def paint(name,FW,SW,spec,O):
    W=B+FW+SW+B; H=85+2*B
    P=Paint(W,H,seed=7); P.safe=spec['safe']; h,w=P.H,P.W
    img=paint_wash(h,w,PAPER,[(spec['haze'],1.0,'#E9EEDF',0.4,0.7)],seed=5)
    fr=spec['focal']; sd=spec['side']
    for lay,cols,deep,(sx,sy,cap),veins,tip in (('back',BACK,DEEPB,(1.25,1.2,0.72),0,False),('mid',MID,DEEPM,(1.05,1.0,0.8),1,True),('front',FRONT,DEEPF,(0.9,0.9,0.92),2,True)):
        fm=np.maximum(fade(P,fr[0],fr[1],fr[2]*sx,fr[3]*sy,11,cap),fade(P,sd[0],sd[1],sd[2]*sx,sd[3]*sy,13,cap*sd[4])); P.begin(fm)
        for i,(p0,ang,L,bend,lm) in enumerate(spec[lay]): branch(P,p0,ang,L,bend,lm,cols,deep,1000+97*i+len(lay)*13+spec['seed'],veins,tip)
        img=P.end(img)
    for q in spec['pods']: paint_pod(P,img,*q)
    for q in spec['vbuds']: paint_vbud(P,img,*q)
    paint_flower(P,img,*spec['flower'])
    img*=(1+0.012*P.tooth)[...,None]; img+=np.random.default_rng(3).normal(0,1.0,(h,w))[...,None]
    out=img.clip(0,255).astype(np.uint8); fx=int((FW+B)*K)
    Image.fromarray(out[:,:int((FW+2*B)*K)]).save(O+f'{name}-front.png'); Image.fromarray(out[:,fx:]).save(O+f'{name}-side.png')
C=lambda x,y,rx,ry:((B+x)*K,(B+y)*K,rx*K,ry*K)
def cube(O):
    FW,SW=87.6,84.6; f=FW+3
    spec=dict(seed=1,focal=(f-18,58,40,36),side=(f+16,70,24,34,0.6),
        safe=[(8,10,57,70),(f+37,14,f+80,79)],
        haze=[C(70,56,30,32),C(118,80,30,12)],
        back=[((f-12,99),-118,68,0.3,24),((f+8,99),-96,64,-0.2,22),((f-44,99),-66,54,0.35,21),((f+40,99),-112,46,0.25,19),((f+2,72),-150,38,0.25,19)],
        mid=[((f-16,99),-108,58,0.35,21),((f-50,99),-58,42,-0.25,18),((f+10,92),-138,44,0.2,19),((f-32,99),-86,44,0.2,18)],
        front=[((f-26,97),-124,36,0.3,17),((f-50,95),-66,28,-0.25,15.5)],
        pods=[((f-62,88),-18,66,1.8,0.12,0),((f-56,92),-27,58,1.55,0.08,0)],
        vbuds=[((f-8,42),-50,6.5),((f-44,66),200,5.5)],
        flower=((f-21,60),40,1.75))
    paint('cube',FW,SW,spec,O)
def long(O):
    FW,SW=175.9,85.1; f=FW+3
    spec=dict(seed=2,focal=(f-48,50,66,46),side=(f+66,66,30,44,0.62),
        safe=[(8,10,78,83),(f+4,14,f+62,77)],
        haze=[C(128,50,56,40),C(220,78,40,14)],
        back=[((f-22,99),-118,92,0.3,30),((f+10,99),-96,84,-0.2,28),((f-64,99),-62,76,0.35,27),((f+44,99),-112,62,0.25,24),((f-4,64),-152,54,0.25,25),((f-104,99),-48,54,0.25,23),((f+72,99),-94,72,0.2,24)],
        mid=[((f-28,99),-110,78,0.35,26),((f-78,99),-60,60,-0.25,23),((f+10,92),-140,60,0.2,24),((f-50,99),-88,62,0.2,23),((f+78,99),-104,46,0.25,19)],
        front=[((f-38,97),-125,50,0.3,21),((f-84,95),-66,38,-0.25,19)],
        pods=[((f-118,90),-17,100,2.2,0.12,0),((f-110,94),-25,88,1.9,0.08,0)],
        vbuds=[((f-34,32),-45,8.5),((f-92,58),205,7.5)],
        flower=((f-60,50),40,2.5))
    paint('long',FW,SW,spec,O)
def label(O):
    """the 100 g kraft-pouch label (70 x 110 mm, arched top, 3 mm bleed): name in the cream above, the same
    painting below, thinning upward into the cream; proportions as the existing label"""
    W,H=76,116; P=Paint(W,H,seed=9); P.safe=[(6,4,70,60)]; h,w=P.H,P.W
    img=paint_wash(h,w,PAPER,[([C(36,84,26,22)],1.0,'#E9EEDF',0.4,0.7)],seed=6)
    for lay,cols,deep,cap,veins,tip,brs in (
        ('back',BACK,DEEPB,0.72,0,False,[((30,120),-104,58,0.3,19),((60,120),-118,50,0.25,18),((6,118),-62,46,0.3,17),((74,96),-150,34,0.2,16)]),
        ('mid',MID,DEEPM,0.8,1,True,[((40,120),-98,46,0.35,17),((14,120),-70,36,-0.25,15),((66,118),-122,40,0.2,15.5)]),
        ('front',FRONT,DEEPF,0.92,2,True,[((28,118),-112,30,0.3,14),((54,118),-80,24,-0.25,12.5)])):
        P.begin(fade(P,38,88,38*(1.25 if lay=='back' else 1.0),34*(1.2 if lay=='back' else 1.0),21,cap,0.5))
        for i,(p0,ang,L,bend,lm) in enumerate(brs): branch(P,p0,ang,L,bend,lm,cols,deep,500+31*i+len(lay),veins,tip)
        img=P.end(img)
    paint_pod(P,img,(4,104),-17,62,1.6,0.12,0); paint_pod(P,img,(8,108),-25,56,1.4,0.08,0)
    paint_vbud(P,img,(60,70),-55,5.5); paint_vbud(P,img,(18,84),205,4.8)
    paint_flower(P,img,(40,84),40,1.45)
    img*=(1+0.012*P.tooth)[...,None]; img+=np.random.default_rng(3).normal(0,1.0,(h,w))[...,None]
    Image.fromarray(img.clip(0,255).astype(np.uint8)).save(O+'label-vanilla.png')

if __name__=='__main__':
    O=ROOT+'fol2/'; {'cube':cube,'long':long,'label':label}[sys.argv[1]](O)
    shutil.copy(ROOT+'bw2/paper.jpg',O+'paper.jpg'); shutil.copy(ROOT+'bw2/paper.jpg',O+'paper-lid.jpg'); print('ok',sys.argv[1])
