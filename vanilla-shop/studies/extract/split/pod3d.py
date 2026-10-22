# Painterly pods with real form: each pod is a spine curve with a width profile. For every pixel inside it we take
# the signed position across the pod (-1 .. 1) from the nearest spine point, turn it into a tube normal, light it
# (wrapped diffuse + a narrow highlight that becomes the shine line), compress the light into a three-tone paint
# ramp, add faint lengthwise ridges, a contact shadow underneath, and depth-of-field blur.
import numpy as np, cv2
from scipy.spatial import cKDTree
from PIL import Image, ImageDraw
import draw
K=20; SS=2
def hx(c): return np.array([int(c[i:i+2],16) for i in (1,3,5)],np.float32)
def mix(a,b,t): return a+(b-a)*t
LIGHT=np.array([-0.55,-0.45,0.70]); LIGHT/=np.linalg.norm(LIGHT); HALF=LIGHT+np.array([0,0,1.]); HALF/=np.linalg.norm(HALF)
def pod_geom(pts,W,tip='round',curl=0.0,n=500):
    """spine through pts (mm); W half-width; tip 'round' or 'point'; curl bends the last 15% (deg, signed)"""
    sp=draw.cr(pts,60)
    if curl:
        k=int(len(sp)*0.85); d=sp[k]-sp[k-3]; a=np.arctan2(d[1],d[0]); seg=np.linalg.norm(np.diff(sp[k:],axis=0),axis=1)
        tail=[sp[k]]
        for i,s in enumerate(seg): a+=np.radians(curl)/len(seg); tail.append(tail[-1]+s*np.array([np.cos(a),np.sin(a)]))
        sp=np.vstack([sp[:k],np.array(tail)])
    L=np.concatenate([[0],np.cumsum(np.linalg.norm(np.diff(sp,axis=0),axis=1))]); u=np.linspace(0,L[-1],n)
    sp=np.stack([np.interp(u,L,sp[:,0]),np.interp(u,L,sp[:,1])],1); t=u/L[-1]
    w=np.where(t<0.05,0.35,np.where(t<0.16,0.35+(W-0.35)*np.sin(np.pi/2*(t-0.05)/0.11),W*(1+0.05*np.sin(np.pi*t))))
    if tip=='point': w=np.where(t>0.78,W*np.maximum(0.08,np.cos(np.pi/2*(t-0.78)/0.22))**0.85,w)
    else: w=np.where(t>0.9,W*np.sqrt(np.clip(1-((t-0.9)/0.1)**2,0.02,1)),w)
    d=np.gradient(sp,axis=0); d/=np.linalg.norm(d,axis=1,keepdims=True); nr=np.stack([-d[:,1],d[:,0]],1)
    poly=np.vstack([sp+nr*w[:,None],(sp-nr*w[:,None])[::-1]])
    return dict(sp=sp,t=t,w=w,nr=nr,poly=poly)
def render_pod(g,H,Wd,ox,pal,seed=0,ridge=0.07):
    """returns RGBA float image (H,Wd,4) of one pod"""
    m=Image.new('L',(Wd*SS,H*SS),0); ImageDraw.Draw(m).polygon([tuple((v+[ox,0])*K*SS/K) for v in g['poly']*K],fill=255)
    a=np.asarray(m.resize((Wd,H),Image.LANCZOS)).astype(np.float32)/255
    ys,xs=np.nonzero(a>0.002); P=np.stack([xs,ys],1).astype(np.float32)/K-np.array([ox,0])
    tree=cKDTree(g['sp']); _,idx=tree.query(P)
    c=g['sp'][idx]; nr=g['nr'][idx]; w=g['w'][idx]; t=g['t'][idx]
    s=np.clip(np.sum((P-c)*nr,1)/np.maximum(w,0.05),-1,1)
    rng=np.random.default_rng(seed)
    s2=s+ridge*np.sin(s*np.pi*2.6+seed)                      # faint lengthwise ridges
    nz=np.sqrt(np.clip(1-np.clip(s2,-1,1)**2,0,1)); N=np.stack([nr[:,0]*s2,nr[:,1]*s2,nz],1)
    N/=np.linalg.norm(N,axis=1,keepdims=True)
    dif=np.clip((N@LIGHT+0.12)/1.12,0,1)
    # highlight in the pod's own cross-section plane, so the shine runs as a line down its length
    hp=np.stack([nr@HALF[:2],np.full(len(s2),HALF[2])],1); hp/=np.linalg.norm(hp,axis=1,keepdims=True)
    spec=np.clip(s2*hp[:,0]+nz*hp[:,1],0,1)**30
    rim=np.clip(-(nr@LIGHT[:2])*s2,0,1)**3*0.25                 # a little bounced light on the shadow edge
    # slow blotchy variation along the pod, like uneven paint
    ph=rng.uniform(0,6.3,3); blot=0.05*np.sin(t*7+ph[0])+0.03*np.sin(t*17+ph[1])
    v=np.clip(dif+blot,0,1)
    sh,md,lt,sp_=(hx(pal[k]) for k in ('shadow','mid','light','spec'))
    col=np.where((v<0.5)[:,None],mix(sh,md,(v/0.5)[:,None]),mix(md,lt,((v-0.5)/0.5)[:,None]))
    col=mix(col,sp_,(spec*0.6)[:,None]); col=mix(col,md,rim[:,None])
    if pal.get('tip'):                                         # ripening at the tip
        tk=np.clip((t-0.8)/0.2,0,1)**1.5; col=mix(col,hx(pal['tip']),(tk*0.55)[:,None])
    out=np.zeros((H,Wd,4),np.float32); out[ys,xs,:3]=col; out[...,3]=a
    return out
def composite(base,pods,ox=0,grain=8,seed=1):
    """base: HxWx3 float. pods: list of (geom, pal, depth 0..1, blur_mm). Drawn back to front with contact shadows."""
    H,Wd=base.shape[:2]; img=base.copy()
    for i,(g,pal,dep,bl) in enumerate(sorted(pods,key=lambda q:q[2])):
        r=render_pod(g,H,Wd,ox,pal,seed=i)
        a=r[...,3]
        # contact shadow, a little down and right, soft
        shm=cv2.GaussianBlur(np.roll(np.roll(a,int(0.45*K),0),int(0.3*K),1),(0,0),0.7*K)*0.38
        img=img*(1-shm[...,None])+hx('#173320')*shm[...,None]
        if bl>0:
            sig=bl*K; premul=r[...,:3]*a[...,None]
            premul=cv2.GaussianBlur(premul,(0,0),sig); a=cv2.GaussianBlur(a,(0,0),sig)
            rgb=premul/np.maximum(a[...,None],1e-4)
        else: rgb=r[...,:3]
        img=img*(1-a[...,None])+rgb*a[...,None]
    if grain: img+=np.random.default_rng(seed).normal(0,1,img.shape[:2]).astype(np.float32)[...,None]*grain
    return img
FRONT=dict(shadow='#4A7A3C',mid='#9CC271',light='#D6EBA4',spec='#FBFEEE')
def depth_pal(dep,ground='#2F5A33',tip=None):
    g=hx(ground); f=(1-dep)*0.42
    p={k:'#%02X%02X%02X'%tuple(mix(hx(v),g,f).astype(int)) for k,v in FRONT.items()}
    if tip: p['tip']=tip
    return p
