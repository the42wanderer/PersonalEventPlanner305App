# Vanilla Tea, 12-bag carton: the Estate artwork as one continuous strip round the four walls (left side, front, right
# side, back, in that order round the box), so the hills, the cream's curve, the flower and the tea shoot run across
# the folds. The front is the approved front: every element keeps its place in front-panel millimetres; the hills are
# extended either side. The cream's edge is one line round the box: the front's sweep, a valley at the front-right fold
# rising to a calm column on the right side, a gentle shoulder across the back, level along the left side into the
# front's high left edge. Also renders the lid ground (the evening sky, dark, a soft glow behind the emblem).
# Output, per palette: <TEA_ART>/est-<panel>.jpg with 3 mm bleed on every side, for tools/tea_box.mjs (TEA_THEME=estate*).
import os, sys, numpy as np, cv2
from PIL import Image, ImageDraw
S='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/'
sys.argv=sys.argv[:1]; sys.path.insert(0,S+'teasoap')
import riso as RS, estate_front as EF
from build6 import canvas, B, K, hx
from build2 import shoot
from foliage2 import paint_flower, paint_vbud, trumpet
import heat as H
import build2, foliage2
def tea_leaf(p0,ang,L,W,bend,rng):
    """foliage2.tealeaf, made more like Camellia sinensis for the sprig: about 30% narrower (2.5:1), the tip pointed
    (the sides run straighter into it), and fine regular forward-facing serrations instead of spiky teeth"""
    W=W*0.7; sp=foliage2.arc(p0,ang,L,bend,n=5); n=len(sp); t=np.linspace(0,1,n)
    u=np.clip((t-0.07)/0.93,0,1); sn=np.sin(np.pi*u)
    prof=W*sn**np.where(u>0.5,1.25,0.8)*(1-0.25*u**2)+0.03                  # widest just below the middle, acute tip
    prof=np.where(t<0.07,0.05*W+0.04,prof)                                   # the petiole
    teeth=np.mod(t*n/1.6+rng.uniform(),1.0)*0.045*W*((u>0.15)&(u<0.94))      # a fine saw, pointing to the tip
    d=np.gradient(sp,axis=0); d/=np.linalg.norm(d,axis=1,keepdims=True)+1e-9; nrm=np.stack([-d[:,1],d[:,0]],1)
    kl,kr=rng.uniform(0.92,1.0),rng.uniform(0.92,1.0)
    Ls=sp+nrm*(prof*kl+teeth)[:,None]; Rs=sp-nrm*(prof*kr+teeth)[:,None]
    shadeL=float(nrm[n//2]@foliage2.LIGHT)>0
    half=np.vstack([Ls,sp[::-1]]) if shadeL else np.vstack([Rs,sp[::-1]])
    return np.vstack([Ls,Rs[::-1]]),sp,half,d,nrm,u,prof
build2.tealeaf=tea_leaf                                                       # the sprig's shoot() draws with this
def tea_shoot(P,img,p0,ang,L,bend,lmax,cols,vein,seed,flip=1):
    """build2.shoot with the tip changed: no bud cluster, the stem ends in a pair of the same tea leaves"""
    import math
    rng=np.random.default_rng(seed); sp=foliage2.arc(p0,ang,L,bend,n=6); n=len(sp); d=np.gradient(sp,axis=0)
    P.over(img,build2.draw.ribbon(sp,lambda t:lmax*0.03*(1-0.5*t)+0.05),cols[0],1.0,0)
    side=flip
    for i,t in enumerate((0.2,0.42,0.62,0.8)):
        j=int(t*(n-1)); da=math.degrees(math.atan2(d[j][1],d[j][0])); Ls=lmax*(1-0.4*t)*rng.uniform(0.85,1.05)
        c=cols[(i+seed)%len(cols)]; build2.flatleaf(P,img,tuple(sp[j]),da+side*rng.uniform(38,58),Ls,Ls*0.3,side*0.25,c,build2.mix(c,'#0E2A22',0.3),vein,rng); side=-side
    da=math.degrees(math.atan2(d[-1][1],d[-1][0]))
    for sg,f in ((1,0.62),(-1,0.54)):                                            # the pair at the tip, a little smaller
        Ls=lmax*f; c=cols[-1]; build2.flatleaf(P,img,tuple(sp[-1]),da+sg*22,Ls,Ls*0.3,sg*0.2,c,build2.mix(c,'#0E2A22',0.25),vein,rng)
nz,grain=RS.nz,RS.grain
FH=EF.FH
# panel spans in box millimetres along the walls, measured from the cube dieline (research/source 2.pdf)
PAN={'sideB':(-84.85,0.0),'front':(0.0,87.65),'sideA':(87.65,172.22),'back':(172.22,259.80)}
X0,X1=PAN['sideB'][0]-B,PAN['back'][1]+B
LID=(87.65,84.97)
def bez(P,n=400):
    P=np.array(P,float); t=np.linspace(0,1,n)[:,None]
    return (1-t)**3*P[0]+3*(1-t)**2*t*P[1]+3*(1-t)*t**2*P[2]+t**3*P[3]
# The cream's edge: boundary.py's function over the unfolded strip (five anchors, quintic smootherstep between them,
# no anchor on the front/side fold), raised by the least amount that keeps 0.04H above the real type. Used only as a
# mask: the landscape is not warped to it. Strip x is box mm with the front at 0 and the other side at negative x.
import boundary as BD
BD.DELTA=BD.lift(os.path.join(S,'boxprev',os.environ.get('INK','ink.json')),('sideA',) if os.environ.get('SIDE_PLUM') else ())   # on the plum side no text sits under the edge
def edge(x):
    x=np.asarray(x,float); u=np.where(x<0,x+BD.P,x)
    yp=BD.y(u)                                                                                     # panel mm (height H)
    return (yp+B)*(FH+2*B)/(BD.H+2*B)-B                                                            # -> strip art mm (the art is FH tall)
def scene(h,w):
    """RS.scene, over the whole strip: the front's ranges, hills and trees where they were, more of the same either side"""
    xs=np.arange(w,dtype=np.float32)/K+X0; ys=np.arange(h,dtype=np.float32)[:,None]/K-B; X=xs[None,:]
    sky=0.10+0.62*np.exp(-((ys-30)/11)**2)+0.10*np.exp(-((ys-30)/36)**2)+0.18*np.exp(-(((X-74)/26)**2+((ys-29)/9)**2))
    cloud=np.clip(nz(h,w,22*K,1.6*K,2),0,None)*np.exp(-((ys-17)/8)**2)*0.10
    L=np.broadcast_to(sky+cloud,(h,w)).copy()
    def hump(cs):
        r=np.full(xs.shape,99.0,np.float32)
        for c,top,hw in cs: r=np.minimum(r,top+(np.abs(xs-c)/hw)**1.8*(99-top)/6)
        return r
    def layer(crest,tone,rim,fall,mist=0.0,seed=0):
        nonlocal L; m=ys>=crest[None,:]; d=np.clip(ys-crest[None,:],0,None)
        L=np.where(m,tone+rim*np.exp(-d/fall)+0.025*nz(h,w,8*K,2*K,seed),L)
        if mist: L=L+mist*np.exp(-((ys-crest[None,:]-2.4)/2.4)**2)*np.clip(0.6+0.5*nz(h,w,16*K,1.5*K,seed+1),0,1.2)
        return m
    peak=lambda c,lift:28.5+np.abs(xs-c)**1.3*0.35-lift
    far=np.minimum.reduce([hump([(8,27,26),(44,29,22),(96,28,30),(-70,28,26),(-32,27.5,24),(132,27,26),(168,29,22),(214,28,28),(250,27.5,24)]),
                           peak(80,5.5),peak(206,4.5),peak(-48,4.0)])
    layer(far,0.46,0.20,2.0,0.10,1)
    layer(hump([(-6,31,20),(28,32,18),(62,33,16),(92,31,22),(-76,31.5,20),(-40,32,18),(118,32,18),(150,31,20),(186,32.5,18),(226,31,20),(256,32,18)]),0.34,0.20,1.6,0.10,3)
    def hedges(m,crest,p0,amp,seed):
        """contour rows of tea, varied as a real estate is: the spacing changes along the hill, the rows bend a little,
        and here and there a planting patch where the rows give way to loose bushes"""
        nonlocal L; d=np.clip(ys-crest[None,:],0,None)
        per=p0*(1+0.05*d)*np.clip(1+0.45*nz(h,1,1.6*K,1,seed+40),0.5,1.9)                         # row-to-row spacing, the same across the hill
        ph=np.cumsum(1/np.maximum(per,0.3),axis=0)/K+0.9*nz(1,w,10*K,1,seed+41); f=ph-np.floor(ph)   # rows stay parallel, bending gently
        row=np.clip(1-np.abs(f-0.35)/0.42,0,1)**0.8
        bush=0.75+0.25*np.cos(2*np.pi*(X/(per*1.2))+2.4*np.floor(ph))*(0.8+0.2*nz(h,w,1.2*K,1.2*K,seed))
        patch=np.clip((nz(h,w,4.5*K,2.5*K,seed+42)-0.95)*2.0,0,1)                                  # ~17% of the slope
        loose=np.clip(0.35+0.65*nz(h,w,0.6*K,0.5*K,seed+43),0,1)**1.4                                # rounder, darker-gapped bushes than the rows
        L=np.where(m,L+amp*(row*bush*(1-patch)+0.75*loose*patch),L)
    cA=hump([(56,33.5,30),(140,34,28),(222,33.5,30),(-50,34,28)]); mA=layer(cA,0.16,0.26,2.4,0.0,5); hedges(mA,cA,1.7,0.24,6)
    cB=hump([(6,37,20),(190,37,18),(-64,37,18)]); mB=layer(cB,0.14,0.22,2.2,0.0,7); hedges(mB,cB,1.6,0.22,8)
    cN=edge(xs)-8.5; mN=layer(cN,0.10,0.24,3.0,0.0,9); hedges(mN,cN,2.1,0.24,10)
    rng=np.random.default_rng(11); tm=Image.new('L',(w,h),0); rm=Image.new('L',(w,h),0)
    td,rd=ImageDraw.Draw(tm),ImageDraw.Draw(rm); P=lambda x,y:((x-X0)*K,(y+B)*K)
    def clump(x0,crest,s):
        j=int(np.clip((x0-X0)*K,0,w-1)); y0=crest[j]+0.3
        for q in range(rng.integers(8,13)):
            cx,cy=x0+rng.uniform(-1.3,1.3)*s,y0-s*rng.uniform(0.25,1.25); r=s*rng.uniform(0.3,0.5)
            td.ellipse([*P(cx-r,cy-r*0.85),*P(cx+r,cy+r*0.85)],fill=255)
            rd.ellipse([*P(cx-r+0.12*s,cy-r*0.85),*P(cx+r+0.12*s,cy+r*0.85)],fill=255)
    for x0,s in ((36,0.9),(41,1.1),(45,0.8),(62,1.0),(67,0.8),(74,1.2)): clump(x0,cA,s)                     # the front's own trees first
    for x0,s in ((3,1.0),(10,0.8),(16,1.1)): clump(x0,cB,s)
    for x0,s in ((26,1.5),(52,1.3),(80,2.2),(85,1.8)): clump(x0,cN+0.6,s)
    for x0,s in ((128,0.9),(134,1.1),(146,0.8),(151,1.0),(212,1.0),(218,0.8),(229,1.1),(-58,0.9),(-52,1.1),(-41,0.8)): clump(x0,cA,s)
    for x0,s in ((184,0.9),(193,1.0),(-69,1.0),(-60,0.8)): clump(x0,cB,s)
    for x0,s in ((112,1.6),(158,1.4),(198,1.5),(244,1.7),(-28,1.5),(-74,1.4)): clump(x0,cN+0.6,s)
    for x0,dy,s in ((-66,3.5,0.8),(-38,5.0,0.7),(-12,4.0,0.9),(120,4.5,0.8),(141,3.0,0.7),(163,5.0,0.9),(188,4.0,0.8),
                    (207,5.5,0.7),(226,3.5,0.9),(252,4.5,0.8)): clump(x0,cN+dy,s)                          # shade trees standing in the rows
    t=np.asarray(tm).astype(np.float32)/255; r=np.asarray(rm).astype(np.float32)/255
    return np.clip(L*(1-t)+0.06*t+0.16*np.clip(r-t,0,1),0,1)
def foreground(h,w):
    def lay(fn):
        img,P=canvas(X1-X0-2*B,FH); bg=img.copy(); fn(P,img)
        a=np.clip(np.abs(img-bg).max(2)/30,0,1); return (img@np.array([0.3,0.59,0.11],np.float32))/255,a
    u=lambda x:x-X0                                                                                  # front mm -> strip canvas mm
    fl=lay(lambda P,c:(paint_flower(P,c,(u(11),B+9),30,2.35),paint_vbud(P,c,(u(34),B+6),-40,6)))
    sh=lay(lambda P,c:tea_shoot(P,c,(u(80),B+72),-100,46,                                             # two leaves and a bud, upright, between flower and logo; only the stem meets the edge
                              -0.35,15,('#2A3A2A','#3C5038','#5A6E4E','#8DA07A'),'#C9D6B4',9,1))
    return fl,sh
def lip_shadow(h,w):
    tube,mouth,_=trumpet((11-X0,B+9),30,7.5*2.35,1.1*2.35,3.6*2.35,2.6*2.35,0.13)
    def mask(polys):
        im=Image.new('L',(w,h),0); dr=ImageDraw.Draw(im)
        for poly in polys: dr.polygon([(x*K,y*K) for x,y in poly],fill=255)
        return np.asarray(im).astype(np.float32)/255
    lip=cv2.GaussianBlur(mask((tube,mouth)),(0,0),0.5*K); src=mask((mouth,))
    sh=cv2.GaussianBlur(np.roll(src,int(0.5*K),0),(0,0),1.5*K)
    return np.clip(sh*(1-0.6*lip)*1.6,0,1)
SIDE_PLUM=bool(os.environ.get('SIDE_PLUM'))
def render(ramp,fr,gam,cream):
    """RS.render over the strip, then the cream below the edge; returns the strip, uint8"""
    h,w=canvas(X1-X0-2*B,FH)[0].shape[:2]                                                         # the paint canvas's own size
    L=cv2.GaussianBlur(scene(h,w),(0,0),0.12*K); (Lf,af),(Ls,as_)=foreground(h,w)
    yy,xx=np.mgrid[0:h,0:w].astype(np.float32)/K; xx+=X0; yy-=B
    as_=cv2.GaussianBlur(as_,(0,0),0.06*K); m=(as_>0.5).astype(np.uint8); ins=cv2.distanceTransform(m,cv2.DIST_L2,5)/K
    q=Ls[as_>0.5]; ln=np.clip((Ls-np.percentile(q,5))/(np.percentile(q,99)-np.percentile(q,5)+1e-6),0,1)
    L=L*(1-as_)+(0.20+0.22*ln+0.42*np.exp(-ins/0.5))*as_                                              # a warmer midtone, a muted copper rim
    af=cv2.GaussianBlur(af,(0,0),0.06*K); m=(af>0.5).astype(np.uint8); ins=cv2.distanceTransform(m,cv2.DIST_L2,5)/K
    lo,hi=np.percentile(Lf[af>0.5],(3,99)); sh=np.clip((Lf-lo)/(hi-lo+1e-6),0,1)
    heart=np.exp(-(((xx-30)/17)**2+((yy-19)/15)**2))
    fv=np.clip(0.68+0.16*sh+0.22*heart-0.17*np.exp(-ins/0.8)-0.22*lip_shadow(h,w),0,1)
    if SIDE_PLUM:                                                                                   # How to brew: the hills across its top, then the
        g=np.clip((yy-29)/12,0,1); g=g*g*(3-2*g)*((xx>=PAN['sideA'][0])&(xx<=PAN['sideA'][1]))       # land eases into the lid's deep plum, rows and all
        L=L*(1-g)+0.08*g
    out=H.ramp(grain(L,0.075,21)**gam,ramp)
    fg=grain(fv,0.075,23); fo=H.ramp(fg,ramp) if fr is None else H.ramp(np.clip((fg-0.56)/0.44,0,1),fr)
    out=out*(1-af[...,None])+fo*af[...,None]
    out*=(1-0.06*np.clip(nz(h,w,40*K,40*K,5),0,1))[...,None]
    out+=np.random.default_rng(5).normal(0,3.0,(h,w))[...,None]
    cm=np.clip((yy[:,:1]-edge(xx[0])[None,:])*K/1.2+0.5,0,1)                                         # the cream, crisp edge
    if SIDE_PLUM: cm=cm*~((xx>=PAN['sideA'][0])&(xx<=PAN['sideA'][1]))                               # no cream on that side: the front's ends at the fold
    paper=hx(cream)*(1+0.012*np.random.default_rng(3).normal(0,1,(h,w)))[...,None]
    return (out*(1-cm[...,None])+paper*cm[...,None]).clip(0,255).astype(np.uint8)
def lid(ramp,gam):
    """the lid: the sky continued over the top, dark, a low glow behind the emblem; the same grain"""
    W,Hh=LID; h=int(round((Hh+2*B)*K)); w=int(round((W+2*B)*K))
    yy,xx=np.mgrid[0:h,0:w].astype(np.float32)/K-B
    L=0.07+0.12*np.exp(-(((xx-W/2)/30)**2+((yy-Hh/2)/30)**2))+0.03*np.clip(nz(h,w,22*K,1.6*K,31),0,None)
    out=H.ramp(grain(L,0.075,33)**gam,ramp); out+=np.random.default_rng(6).normal(0,3.0,(h,w))[...,None]
    return out.clip(0,255).astype(np.uint8)
if __name__=='__main__':
    ks=os.environ.get('PALETTES','forest plum').split()
    for k in ks:
        d=os.path.join(S,'teasoap','estate-art',k+('-sideplum' if SIDE_PLUM else '')); os.makedirs(d,exist_ok=True)
        gam={'forest':1.3,'ceylon':1.15}.get(k,1.0)
        st=render(RS.RAMPS[k],RS.FLOWER.get(k),gam,RS.CREAM[k]); Image.fromarray(st).save(os.path.join(d,'strip.jpg'),quality=93)
        for p,(a,b) in PAN.items():
            c0,c1=int(round((a-B-X0)*K)),int(round((b+B-X0)*K)); c0=max(c0,0); c1=min(c1,st.shape[1])
            Image.fromarray(st[:,c0:c1]).save(os.path.join(d,f'est-{p}.jpg'),quality=95)
        Image.fromarray(lid(RS.RAMPS[k],gam)).save(os.path.join(d,'est-lid.jpg'),quality=95)
        print('ok',k,st.shape)
