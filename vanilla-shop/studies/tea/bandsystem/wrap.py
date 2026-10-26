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
BOXK=os.environ.get('BOX','cube')
if BOXK=='long':    # the 25-bag carton (research dieline VS_DIELINE_LONG): front and back about twice as wide, same height
    PAN={'sideB':(-84.49,0.0),'front':(0.0,175.93),'sideA':(175.93,261.06),'back':(261.06,436.07)}
    LID=(175.01,84.84)
else:
    PAN={'sideB':(-84.85,0.0),'front':(0.0,87.65),'sideA':(87.65,172.22),'back':(172.22,259.80)}
    LID=(87.65,84.97)
X0,X1=PAN['sideB'][0]-B,PAN['back'][1]+B
# The landscape's furniture, placed for the cube in strip mm. The long box keeps every piece where it stands to what
# it belongs with: the front's left part (under the flower) as it is; the cube's peak, glow, sprig and their trees moved
# onto the front's centre line CM (tea_box.mjs centres the Sinhala name and the descriptor on it, boundary.py puts the
# valley there), so the sprig rises from the valley between the name and the facts; the right side moved with its fold;
# the back's pattern laid twice across the wider back; the front's right end given hills and trees of its own.
CM=float(os.environ.get('CM',100.67))                                                             # tea_box.mjs prints it
FILL_MID=CM>130          # with the group at the right end, the middle of the front gets the new hills instead
def place(items,extra=()):
    if BOXK!='long': return list(items)
    dC=CM-80; dF=PAN['front'][1]-87.65; dB=PAN['sideA'][1]-172.22; out=[]
    for it in items:
        x=it[0]
        if x<60: out.append(it)
        elif x<87.65: out.append((x+dC,)+tuple(it[1:]))
        elif x<=172.22: out.append((x+dF,)+tuple(it[1:]))
        else: out+= [(x+dB,)+tuple(it[1:]),(x+dB+87.58,)+tuple(it[1:])]
    return out+list(extra)
SPRIG_X=80 if BOXK!='long' else CM
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
    gx=place([(74,)])[0][0]
    sky=0.10+0.62*np.exp(-((ys-30)/11)**2)+0.10*np.exp(-((ys-30)/36)**2)+0.18*np.exp(-(((X-gx)/26)**2+((ys-29)/9)**2))
    cloud=np.clip(nz(h,w,22*K,1.6*K,2),0,None)*np.exp(-((ys-17)/8)**2)*0.10
    L=np.broadcast_to(sky+cloud,(h,w)).copy()
    def hump(cs):
        r=np.full(xs.shape,99.0,np.float32)
        for c,top,hw in cs: r=np.minimum(r,top+(np.abs(xs-c)/hw)**1.8*(99-top)/6)
        return r
    global REG; REG=np.zeros((h,w),np.uint8); rid=[0]
    def layer(crest,tone,rim,fall,mist=0.0,seed=0):
        nonlocal L; m=ys>=crest[None,:]; d=np.clip(ys-crest[None,:],0,None); rid[0]+=1; REG[np.broadcast_to(m,(h,w))]=rid[0]
        L=np.where(m,tone+rim*np.exp(-d/fall)+0.025*nz(h,w,8*K,2*K,seed),L)
        if mist: L=L+mist*np.exp(-((ys-crest[None,:]-2.4)/2.4)**2)*np.clip(0.6+0.5*nz(h,w,16*K,1.5*K,seed+1),0,1.2)
        return m
    peak=lambda c,lift:28.5+np.abs(xs-c)**1.3*0.35-lift
    pk=[(80,5.5),(206,4.5),(-48,4.0)] if BOXK!='long' else [(CM,5.5),(206+88.84,4.5),(-48,4.0),(206+176.42,3.2)]
    far=np.minimum.reduce([hump(place([(8,27,26),(44,29,22),(96,28,30),(-70,28,26),(-32,27.5,24),(132,27,26),(168,29,22),(214,28,28),(250,27.5,24)],
                                      [(80,28,26),(116,27.5,24)] if FILL_MID else [(128,28,26),(158,27.5,24)])),*[peak(c,l) for c,l in pk]])
    layer(far,0.46,0.20,2.0,0.10,1)
    layer(hump(place([(-6,31,20),(28,32,18),(62,33,16),(92,31,22),(-76,31.5,20),(-40,32,18),(118,32,18),(150,31,20),(186,32.5,18),(226,31,20),(256,32,18)],
                     [(72,32,18),(104,31,20),(130,32.5,18)] if FILL_MID else [(124,32,18),(148,31,20),(170,32.5,18)])),0.34,0.20,1.6,0.10,3)
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
    cA=hump(place([(56,33.5,30),(140,34,28),(222,33.5,30),(-50,34,28)],[(108,34,28)] if FILL_MID else [(150,34,28)])); mA=layer(cA,0.16,0.26,2.4,0.0,5); hedges(mA,cA,1.7,0.24,6)
    cB=hump(place([(6,37,20),(190,37,18),(-64,37,18)],[(124,37,20)] if FILL_MID else [(164,37,20)])); mB=layer(cB,0.14,0.22,2.2,0.0,7); hedges(mB,cB,1.6,0.22,8)
    cN=edge(xs)-8.5
    if BOXK=='long': cN=np.maximum(cN,float(os.environ.get('NEAR_TOP',0)))   # where the cream rides high, the near rows stop short of the far hills
    mN=layer(cN,0.10,0.24,3.0,0.0,9); hedges(mN,cN,2.1,0.24,10)
    rng=np.random.default_rng(11); tm=Image.new('L',(w,h),0); rm=Image.new('L',(w,h),0)
    td,rd=ImageDraw.Draw(tm),ImageDraw.Draw(rm); P=lambda x,y:((x-X0)*K,(y+B)*K)
    tms={3:Image.new('L',(w,h),0),4:Image.new('L',(w,h),0),5:Image.new('L',(w,h),0)}                # the trees, by the hill they stand on
    def clump(x0,crest,s):
        j=int(np.clip((x0-X0)*K,0,w-1)); y0=crest[j]+0.3; tq=ImageDraw.Draw(tms[3 if crest is cA else 4 if crest is cB else 5])
        for q in range(rng.integers(8,13)):
            cx,cy=x0+rng.uniform(-1.3,1.3)*s,y0-s*rng.uniform(0.25,1.25); r=s*rng.uniform(0.3,0.5)
            td.ellipse([*P(cx-r,cy-r*0.85),*P(cx+r,cy+r*0.85)],fill=255); tq.ellipse([*P(cx-r,cy-r*0.85),*P(cx+r,cy+r*0.85)],fill=255)
            rd.ellipse([*P(cx-r+0.12*s,cy-r*0.85),*P(cx+r+0.12*s,cy+r*0.85)],fill=255)
    cN6=cN+0.6
    for x0,s in place(((36,0.9),(41,1.1),(45,0.8),(62,1.0),(67,0.8),(74,1.2)),((96,0.9),(101,1.1),(112,0.8)) if FILL_MID else ((134,0.9),(140,1.1),(146,0.8))): clump(x0,cA,s)   # the front's own trees first
    for x0,s in place(((3,1.0),(10,0.8),(16,1.1)),((118,0.9),(126,1.0)) if FILL_MID else ((158,0.9),(167,1.0))): clump(x0,cB,s)
    for x0,s in place(((26,1.5),(52,1.3),(80,2.2),(85,1.8)),((74,1.4),(104,1.6)) if FILL_MID else ((126,1.5),(150,1.3))): clump(x0,cN6,s)
    for x0,s in place(((128,0.9),(134,1.1),(146,0.8),(151,1.0),(212,1.0),(218,0.8),(229,1.1),(-58,0.9),(-52,1.1),(-41,0.8))): clump(x0,cA,s)
    for x0,s in place(((184,0.9),(193,1.0),(-69,1.0),(-60,0.8))): clump(x0,cB,s)
    for x0,s in place(((112,1.6),(158,1.4),(198,1.5),(244,1.7),(-28,1.5),(-74,1.4))): clump(x0,cN6,s)
    for x0,dy,s in place(((-66,3.5,0.8),(-38,5.0,0.7),(-12,4.0,0.9),(120,4.5,0.8),(141,3.0,0.7),(163,5.0,0.9),(188,4.0,0.8),
                    (207,5.5,0.7),(226,3.5,0.9),(252,4.5,0.8)),((88,4.0,0.8),(116,5.0,0.7),(134,3.5,0.9)) if FILL_MID else ((120,4.0,0.8),(140,5.0,0.7),(162,3.5,0.9))): clump(x0,cN+dy,s)   # shade trees standing in the rows
    t=np.asarray(tm).astype(np.float32)/255; r=np.asarray(rm).astype(np.float32)/255
    for q in (3,4,5): REG[np.asarray(tms[q])>127]=q
    return np.clip(L*(1-t)+0.06*t+0.16*np.clip(r-t,0,1),0,1)
def foreground(h,w):
    def lay(fn):
        img,P=canvas(X1-X0-2*B,FH); bg=img.copy(); fn(P,img)
        a=np.clip(np.abs(img-bg).max(2)/30,0,1); return (img@np.array([0.3,0.59,0.11],np.float32))/255,a
    u=lambda x:x-X0                                                                                  # front mm -> strip canvas mm
    fl=lay(lambda P,c:(paint_flower(P,c,(u(11),B+9),30,2.35),paint_vbud(P,c,(u(34),B+6),-40,6)))
    sh=lay(lambda P,c:tea_shoot(P,c,(u(SPRIG_X),B+72),-100,46,                                             # two leaves and a bud, upright, between flower and logo; only the stem meets the edge
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
    ys=np.nonzero(src.max(1)>0.5)[0]; t=((np.arange(h,dtype=np.float32)-ys[0])/(ys[-1]-ys[0]))[:,None]   # 0 at the mouth's top, 1 at its foot
    up=np.clip((t-0.42)/0.38,0,1); up=up*up*(3-2*up)                                               # the shade reaches further up the mouth's
    return np.clip(sh*(1-0.6*lip*(1-0.75*up))*1.6,0,1)                                              # lower part, the top stays clean
def horn_shade(h,w):
    """the horn's underside against the petal behind it: a contact shade, not a cast shadow. Along the horn's edges
    that face down and away from the light (upper left), a slight shade on the petal just outside, falling off within
    about a millimetre, and a gentler one on the horn just inside, as its surface turns away; faded out towards the
    flower's heart so the centre stays clean"""
    tube,mouth,_=trumpet((11-X0,B+9),30,7.5*2.35,1.1*2.35,3.6*2.35,2.6*2.35,0.13)
    im=Image.new('L',(w,h),0); dr=ImageDraw.Draw(im)
    for poly in (tube,mouth): dr.polygon([(x*K,y*K) for x,y in poly],fill=255)
    m=(np.asarray(im)>127).astype(np.uint8)
    dout=cv2.distanceTransform(1-m,cv2.DIST_L2,5)/K; din=cv2.distanceTransform(m,cv2.DIST_L2,5)/K
    sm=cv2.GaussianBlur(m.astype(np.float32),(0,0),1.0*K); gy,gx=np.gradient(sm); g=np.hypot(gx,gy)+1e-6
    d=np.array([0.42,0.91]); face=np.clip((-gx*d[0]-gy*d[1])/g,0,1)**1.3                        # outward normal against the shade's way
    face=cv2.GaussianBlur(face.astype(np.float32),(0,0),0.6*K)
    base=np.array(tube[0]+tube[-1])/2 if len(tube)==4 else np.array(tube).mean(0)              # the tube's root, at the heart
    tip=np.array(mouth).mean(0); ax=tip-base; yy,xx=np.mgrid[0:h,0:w].astype(np.float32)/K
    t=np.clip(((xx-base[0])*ax[0]+(yy-base[1])*ax[1])/(ax@ax),0,1); along=np.clip((t-0.12)/0.3,0,1); along=along*along*(3-2*along)
    out=np.where(m==0,np.exp(-dout/0.75),0); inn=np.where(m==1,0.55*np.exp(-din/1.1),0)
    return (face*along*(out+inn)).astype(np.float32)
def pramp(v,cols):
    """H.ramp, or, when the stops are (position, colour) pairs, a gradient map with the stops where they are put"""
    if not isinstance(cols[0],tuple): return H.ramp(v,cols)
    pos=np.array([p for p,_ in cols]); rgb=np.array([hx(c) for _,c in cols]); v=np.clip(v,0,1)
    return np.stack([np.interp(v,pos,rgb[:,i]) for i in range(3)],-1)
SIDE_PLUM=bool(os.environ.get('SIDE_PLUM'))
def rgbf(c): return np.array(hx(c),np.float32)
def rramp(t,stops):
    pos=np.array([p for p,_ in stops]); rgb=np.array([hx(c) for _,c in stops])
    return np.stack([np.interp(np.clip(t,0,1),pos,rgb[:,i]) for i in range(3)],-1).astype(np.float32)
def direct(D,V0,Vp,af,as_,Ls,g,yy,xx):
    """art direction by region: the sky a colour gradient top to bottom (y in art mm), lit by the drawing's own light
    (its grain, cloud and glow kept as a brightness ratio against the sky's mean at that height); each hill layer its own
    ramp over its own range of light (rows, rims and shade kept); the trees with their hill; the sprig its own ramp;
    the How to brew side easing into its panel colour, the panel keeping the grain"""
    h,w=V0.shape; R=REG
    sk=(R==0)&(af<0.3); rows=np.array([np.median(V0[i][sk[i]]) if sk[i].sum()>20 else np.nan for i in range(h)])
    rows=np.where(np.isnan(rows),np.nanmax(rows),rows)
    ratio=np.clip(1+D.get('skyLight',1.3)*(V0-rows[:,None]),0.6,1.45)                             # the grain and glow at their own strength
    ysky=np.array([p for p,_ in D['sky']]); cy=rramp((yy[:,0]-ysky[0])/(ysky[-1]-ysky[0]),[((p-ysky[0])/(ysky[-1]-ysky[0]),c) for p,c in D['sky']])
    out=np.zeros((h,w,3),np.float32); wsum=np.zeros((h,w),np.float32)
    def put(mask,col):
        nonlocal out,wsum; m=cv2.GaussianBlur(mask.astype(np.float32),(0,0),0.12*K); out+=m[...,None]*col; wsum+=m
    put(R==0,cy[:,None,:]*ratio[...,None])
    for r in range(1,6):
        mk=R==r; q=V0[mk&(af<0.3)&(as_<0.3)]; lo,hi=np.percentile(q,(2,98)); put(mk,rramp((V0-lo)/(hi-lo+1e-6),D['hills'][r-1]))
    out/=np.maximum(wsum,1e-6)[...,None]
    q=Ls[as_>0.5]; lo,hi=np.percentile(q,(3,99)); sp=rramp((Ls-lo)/(hi-lo+1e-6),D['sprig'])
    out=out*(1-as_[...,None])+sp*as_[...,None]
    pc=rgbf(D['panel'])[None,None,:]*np.clip(Vp/0.055,0.6,1.5)[...,None]**D.get('panelGrain',0.35)
    return out*(1-g[...,None])+pc*g[...,None]
def render(ramp,fr,gam,cream,D=None):
    """RS.render over the strip, then the cream below the edge; returns the strip, uint8"""
    h,w=canvas(X1-X0-2*B,FH)[0].shape[:2]                                                         # the paint canvas's own size
    L=cv2.GaussianBlur(scene(h,w),(0,0),0.12*K); (Lf,af),(Ls,as_)=foreground(h,w)
    yy,xx=np.mgrid[0:h,0:w].astype(np.float32)/K; xx+=X0; yy-=B
    as_=cv2.GaussianBlur(as_,(0,0),0.06*K); m=(as_>0.5).astype(np.uint8); ins=cv2.distanceTransform(m,cv2.DIST_L2,5)/K
    q=Ls[as_>0.5]; ln=np.clip((Ls-np.percentile(q,5))/(np.percentile(q,99)-np.percentile(q,5)+1e-6),0,1)
    sprL=0.20+0.22*ln+0.42*np.exp(-ins/0.5); L=L*(1-as_)+sprL*as_                                              # a warmer midtone, a muted copper rim
    af=cv2.GaussianBlur(af,(0,0),0.06*K); m=(af>0.5).astype(np.uint8); ins=cv2.distanceTransform(m,cv2.DIST_L2,5)/K
    lo,hi=np.percentile(Lf[af>0.5],(3,99)); sh=np.clip((Lf-lo)/(hi-lo+1e-6),0,1)
    heart=np.exp(-(((xx-30)/17)**2+((yy-19)/15)**2))
    fv=np.clip(0.68+0.16*sh+0.22*heart-0.17*np.exp(-ins/0.8)-0.22*lip_shadow(h,w)-0.21*horn_shade(h,w),0,1)
    if D is not None: V0=grain(L,0.075,21)**gam
    g=np.zeros_like(L)
    if SIDE_PLUM:                                                                                   # How to brew: the hills across its top, then the
        g=np.clip((yy-29)/12,0,1); g=g*g*(3-2*g)*((xx>=PAN['sideA'][0])&(xx<=PAN['sideA'][1]))       # land eases into the lid's deep plum, rows and all
        L=L*(1-g)+0.08*g
    V=grain(L,0.075,21)**gam
    if os.environ.get('DUMP'): np.savez_compressed(os.environ['DUMP'],V=V.astype(np.float16),af=af.astype(np.float16),xx=xx[0],yy=yy[:,0])
    out=pramp(V,ramp) if D is None else None
    fg=grain(fv,0.075,23); fo=pramp(fg,ramp) if fr is None else H.ramp(np.clip((fg-0.56)/0.44,0,1),fr)
    if D is not None: out=direct(D,V0,V,af,as_,grain(sprL,0.075,24),g,yy,xx)
    out=out*(1-af[...,None])+fo*af[...,None]
    out*=(1-0.06*np.clip(nz(h,w,40*K,40*K,5),0,1))[...,None]
    out+=np.random.default_rng(5).normal(0,3.0,(h,w))[...,None]
    cm=np.clip((yy[:,:1]-edge(xx[0])[None,:])*K/1.2+0.5,0,1)                                         # the cream, crisp edge
    if SIDE_PLUM: cm=cm*~((xx>=PAN['sideA'][0])&(xx<=PAN['sideA'][1]))                               # no cream on that side: the front's ends at the fold
    paper=hx(cream)*(1+0.012*np.random.default_rng(3).normal(0,1,(h,w)))[...,None]
    return (out*(1-cm[...,None])+paper*cm[...,None]).clip(0,255).astype(np.uint8)
def lid(ramp,gam,D=None):
    """the lid: the sky continued over the top, dark, a low glow behind the emblem; the same grain (art-directed: the
    brewing panel's colour, the glow a little of the sky's)"""
    W,Hh=LID; h=int(round((Hh+2*B)*K)); w=int(round((W+2*B)*K))
    yy,xx=np.mgrid[0:h,0:w].astype(np.float32)/K-B
    L=0.07+0.12*np.exp(-(((xx-W/2)/30)**2+((yy-Hh/2)/30)**2))+0.03*np.clip(nz(h,w,22*K,1.6*K,31),0,None)
    Vl=grain(L,0.075,33)**gam
    if D is None: out=pramp(Vl,ramp)
    else:
        gl=np.clip((L-0.07)/0.12,0,1)[...,None]*D.get('lidGlow',0.25); pc=rgbf(D['panel'])*np.clip(Vl/0.055,0.6,1.5)[...,None]**D.get('panelGrain',0.35)
        out=pc*(1-gl)+rgbf(D['lidGlowCol'])*gl
    out+=np.random.default_rng(6).normal(0,3.0,(h,w))[...,None]
    return out.clip(0,255).astype(np.uint8)
if __name__=='__main__':
    ks=os.environ.get('PALETTES','forest plum').split()
    for k in ks:
        d=os.path.join(S,'teasoap','estate-art',k+('-sideplum' if SIDE_PLUM else '')+('-long' if BOXK=='long' else '')+os.environ.get('ART_SUFFIX','')); os.makedirs(d,exist_ok=True)
        gam={'forest':1.3,'ceylon':1.15,'evergreen':1.0,'emerald':1.15,'emeraldhoney':1.15,'apricot':1.15,'citron':1.15,'citronA':1.15,'citronB':1.15,'citronC':1.15,'ochre':1.15,'rose':1.15,'celadon':1.15,'chartreuse':1.15,'jade':1.15,'sage':1.1}.get(k,1.0)
        D=getattr(RS,'DIRS',{}).get(k); rp=RS.RAMPS.get(k,RS.RAMPS['emerald'])
        st=render(rp,RS.FLOWER.get(k,RS.FLOWER['emerald']),gam,RS.CREAM.get(k,D and D['cream']),D); Image.fromarray(st).save(os.path.join(d,'strip.jpg'),quality=93)
        for p,(a,b) in PAN.items():
            c0,c1=int(round((a-B-X0)*K)),int(round((b+B-X0)*K)); c0=max(c0,0); c1=min(c1,st.shape[1])
            Image.fromarray(st[:,c0:c1]).save(os.path.join(d,f'est-{p}.jpg'),quality=95)
        Image.fromarray(lid(rp,gam,D)).save(os.path.join(d,'est-lid.jpg'),quality=95)
        print('ok',k,st.shape)
