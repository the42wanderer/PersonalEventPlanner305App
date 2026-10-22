# Four non-CGI ways to paint a pod. All share the pod shape (green.pod_shape) and, per pixel, its coordinates:
# s = position across the pod (-1 .. 1), t = position along it (0 .. 1), lit = how much that side faces the light.
import numpy as np, cv2
from scipy.spatial import cKDTree
from PIL import Image, ImageDraw
K=20; SS=2
def hx(c): return np.array([int(c[i:i+2],16) for i in (1,3,5)],np.float32)
L2=np.array([-0.6,-0.8]); L2/=np.linalg.norm(L2)
RAMP=dict(shadow='#5C9450',mid='#A9D082',light='#DAEEB0',hi='#F3FADF')
def ramp(dep,ground='#2F5A33'):
    f=(1-dep)*0.42; g=hx(ground); return {k:hx(v)+(g-hx(v))*f for k,v in RAMP.items()}
def noise2(h,w,scale,seed):
    """smooth value noise, roughly -1..1, feature size `scale` px"""
    r=np.random.default_rng(seed); sm=r.normal(0,1,(int(h/scale)+3,int(w/scale)+3)).astype(np.float32)
    n=cv2.resize(sm,(w,h),interpolation=cv2.INTER_CUBIC); return n/ (n.std()+1e-6)/2.5
class Pod:
    def __init__(s,sp,w,nr,H,W,ox):
        s.sp,s.w,s.nr=sp,w,nr; s.t=np.linspace(0,1,len(sp))
        poly=np.vstack([sp+nr*w[:,None],(sp-nr*w[:,None])[::-1]])+[ox,0]
        x0,y0=np.floor(poly.min(0)*K).astype(int)-260; x1,y1=np.ceil(poly.max(0)*K).astype(int)+260
        s.x0,s.y0=max(x0,0),max(y0,0); s.x1,s.y1=min(x1,W),min(y1,H)
        h,wd=s.y1-s.y0,s.x1-s.x0; s.h,s.wd=h,wd
        m=Image.new('L',(wd*SS,h*SS),0); ImageDraw.Draw(m).polygon([tuple(((v*K)-[s.x0,s.y0])*SS) for v in poly],fill=255)
        s.a=np.asarray(m.resize((wd,h),Image.LANCZOS)).astype(np.float32)/255
        yy,xx=np.mgrid[0:h,0:wd]; P=np.stack([(xx+s.x0)/K-ox,(yy+s.y0)/K],-1).reshape(-1,2)
        _,idx=cKDTree(sp).query(P); idx=idx.reshape(h,wd)
        c=sp[idx]; n_=nr[idx]; P=P.reshape(h,wd,2)
        s.s=np.clip(np.sum((P-c)*n_,-1)/np.maximum(w[idx],0.05),-1.2,1.2); s.tt=s.t[idx]
        s.lit=np.clip(s.s*(n_@L2),-1,1)             # +1 on the side facing the light
        s.ox=ox
def put(img,pod,rgb,alpha):
    sl=img[pod.y0:pod.y1,pod.x0:pod.x1]; sl[:]=sl*(1-alpha[...,None])+rgb*alpha[...,None]
def halo(img,pod,dep):
    a=cv2.GaussianBlur(cv2.dilate(pod.a,np.ones((9,9),np.uint8)),(0,0),0.45*K)*0.55*(0.4+0.6*dep)
    put(img,pod,np.broadcast_to(hx('#173320'),a.shape+(3,)),a)
def soften(rgb,a,mm):
    if mm<=0: return rgb,a
    pm=cv2.GaussianBlur(rgb*a[...,None],(0,0),mm*K); a2=cv2.GaussianBlur(a,(0,0),mm*K)
    return pm/np.maximum(a2[...,None],1e-4),a2
# ---- 1. gouache: a few flat shapes per pod
def gouache(img,pod,dep,seed):
    R=ramp(dep); n=noise2(pod.h,pod.wd,40,seed)*0.12
    v=pod.lit+n
    rgb=np.where((v>0.18)[...,None],R['light'],R['mid'])
    rgb=np.where((v<-0.55)[...,None],R['shadow'],rgb)
    dash=(np.abs(pod.lit-0.62+n*0.5)<0.09)&(pod.tt>0.18)&(pod.tt<0.78)
    rgb=np.where(dash[...,None],R['hi'],rgb)
    rgb=np.broadcast_to(rgb,pod.a.shape+(3,)).astype(np.float32)
    rgb=cv2.GaussianBlur(rgb,(0,0),0.12*K)
    rgb,a=soften(rgb,pod.a,0.08+(1-dep)*0.6); put(img,pod,rgb,a)
# ---- 2. watercolour: wobbly wash, edge pooling, granulation, a glaze on the lit side
def watercolour(img,pod,dep,seed):
    R=ramp(dep)
    d_in=cv2.distanceTransform((pod.a>0.5).astype(np.uint8),cv2.DIST_L2,5)/K
    d_out=cv2.distanceTransform((pod.a<=0.5).astype(np.uint8),cv2.DIST_L2,5)/K
    sd=d_in-d_out+noise2(pod.h,pod.wd,30,seed)*0.1
    a=np.clip(sd/0.08+0.5,0,1)
    pool=np.exp(-np.clip(sd,0,None)/0.35)                  # pigment gathers at the drying edge
    gran=noise2(pod.h,pod.wd,2.2,seed+1)*0.5+noise2(pod.h,pod.wd,6,seed+2)*0.5
    rgb=R['mid']+(R['light']-R['mid'])*np.clip(0.45+0.35*pod.lit,0,1)[...,None]
    rgb=rgb+(R['shadow']-rgb)*(pool*0.4)[...,None]+gran[...,None]*6
    # second glaze, lighter, on the lit side, with its own wobbly edge
    g2=np.clip((pod.lit-0.2+noise2(pod.h,pod.wd,60,seed+3)*0.12)/0.12,0,1)*a
    rgb=rgb+(R['hi']-rgb)*(g2*0.55)[...,None]
    rgb,a=soften(rgb.astype(np.float32),a*0.95,(1-dep)*0.6); put(img,pod,rgb,a)
# ---- 3. brushstrokes laid along the pod
def strokes(img,pod,dep,seed):
    R=ramp(dep); rng=np.random.default_rng(seed)
    layer=np.zeros((pod.h,pod.wd,3),np.float32); cov=np.zeros((pod.h,pod.wd),np.float32)
    base=R['mid']; layer[:]=base; cov[:]=1
    sp,w,nr=pod.sp,pod.w,pod.nr; n=len(sp)
    for k in range(int(70+40*dep)):
        s0=rng.uniform(-0.9,0.9); ta=rng.uniform(0,0.85); tb=min(1,ta+rng.uniform(0.12,0.45))
        i0,i1=int(ta*(n-1)),int(tb*(n-1))
        if i1-i0<4: continue
        c=sp[i0:i1]+nr[i0:i1]*(w[i0:i1,None]*s0); bw=w[i0:i1]*rng.uniform(0.12,0.28)
        tt=np.linspace(0,1,i1-i0); bw=bw*np.sin(np.pi*tt)**0.5+0.02
        poly=np.vstack([c+nr[i0:i1]*bw[:,None],(c-nr[i0:i1]*bw[:,None])[::-1]])+[pod.ox,0]
        pts=((poly*K)-[pod.x0,pod.y0])*4
        m=np.zeros((pod.h*4//4*1,pod.wd),np.uint8)
        cv2.fillPoly(m,[np.round(pts).astype(np.int32)],255,lineType=cv2.LINE_AA,shift=2)
        lit=s0*(nr[(i0+i1)//2]@L2)
        v=np.clip(0.5+0.5*lit+rng.normal(0,0.12),0,1)
        col=np.where(v<0.5,R['shadow']+(R['mid']-R['shadow'])*v/0.5,R['mid']+(R['light']-R['mid'])*(v-0.5)/0.5)
        if lit>0.45 and rng.random()<0.35: col=R['hi']
        al=(m.astype(np.float32)/255)*rng.uniform(0.55,0.9)
        layer=layer*(1-al[...,None])+col*al[...,None]
    layer=cv2.GaussianBlur(layer,(0,0),0.05*K)
    rgb,a=soften(layer,pod.a,0.05+(1-dep)*0.6); put(img,pod,rgb,a)
# ---- 4. stipple: soft airbrushed base, light pigment as fine dots
def stipple(img,pod,dep,seed):
    R=ramp(dep); rng=np.random.default_rng(seed)
    v=np.clip(0.45+0.4*pod.lit-0.25*np.abs(pod.s)**3,0,1)
    base=R['shadow']+(R['mid']-R['shadow'])*v[...,None]
    dots=np.zeros(pod.a.shape,np.float32)
    ys,xs=np.nonzero(pod.a>0.5); keep=rng.random(len(ys))<0.03
    ys,xs=ys[keep],xs[keep]; pv=v[ys,xs]; keep=rng.random(len(ys))<pv**1.6
    for y,x,r in zip(ys[keep],xs[keep],rng.uniform(0.9,1.8,keep.sum())): cv2.circle(dots,(int(x),int(y)),int(r),1.0,-1,cv2.LINE_AA)
    dots=cv2.GaussianBlur(dots,(0,0),0.6)
    tone=R['light']+(R['hi']-R['light'])*np.clip(pod.lit,0,1)[...,None]
    rgb=base+(tone-base)*np.clip(dots*0.9+np.clip(v-0.6,0,1)*0.5,0,1)[...,None]
    rgb=cv2.GaussianBlur(rgb.astype(np.float32),(0,0),0.05*K)
    rgb,a=soften(rgb,pod.a,0.1+(1-dep)*0.6); put(img,pod,rgb,a)
STYLES=dict(gouache=gouache,watercolour=watercolour,strokes=strokes,stipple=stipple)
