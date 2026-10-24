# The painting soaked into the paper like a watercolour blot / spilt tea: an irregular, slightly fibrous edge, a
# darker tide line where the pigment dried, uneven pigment with back-runs inside, a few satellite drops, and an aged
# paper mottle over everything.
import numpy as np, cv2
K=20
def fbm(h,w,cell,seed,oct=4):
    r=np.random.default_rng(seed); out=np.zeros((h,w),np.float32); a=1; t=0
    for o in range(oct):
        c=max(2,int(cell/2**o)); g=r.normal(0,1,(h//c+3,w//c+3)).astype(np.float32)
        out+=a*cv2.resize(g,(w,h),interpolation=cv2.INTER_CUBIC)[:h,:w]; t+=a; a*=0.5
    return out/t
def smooth(a,b,x): t=np.clip((x-a)/(b-a),0,1); return t*t*(3-2*t)
def blot_mask(h,w,blobs,seed=1):
    """blobs: (cx, cy, rx, ry) in px; returns (soak, tide, density)"""
    yy,xx=np.mgrid[0:h,0:w].astype(np.float32)
    f=np.full((h,w),-9,np.float32)
    for i,(cx,cy,rx,ry) in enumerate(blobs):
        f=np.maximum(f,1-np.hypot((xx-cx)/rx,(yy-cy)/ry))
    f+=0.22*fbm(h,w,int(28*K),seed)+0.06*fbm(h,w,int(5*K),seed+1)+0.018*fbm(h,w,int(0.8*K),seed+2,2)   # wandering, fibrous edge
    core=smooth(-0.015,0.015,f)
    er=cv2.erode((core>0.5).astype(np.uint8),cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(int(1.4*K),)*2)).astype(np.float32)
    tide=cv2.GaussianBlur(np.clip(core-er,0,1),(0,0),0.35*K)                                         # pigment dried at the rim
    bleed=cv2.GaussianBlur(core,(0,0),1.1*K)*(0.55+0.45*np.clip(fbm(h,w,int(0.6*K),seed+3,2)+0.5,0,1))
    soak=np.maximum(core,bleed*0.45)                                                                 # paper fibres drawing it out
    # inside: uneven pigment and a couple of lighter back-runs with their own faint edges
    dens=0.80+0.20*fbm(h,w,int(9*K),seed+4)
    br=fbm(h,w,int(16*K),seed+5); back=smooth(0.35,0.45,br)*core
    bedge=np.exp(-((br-0.40)/0.012)**2)*core*0.5
    dens=dens*(1-0.28*back)+0.0
    return soak,np.clip(tide+bedge*0.6,0,1),np.clip(dens,0,1)
def aged_paper(h,w,paper,seed=7):
    m=fbm(h,w,int(40*K),seed)*0.025+fbm(h,w,int(3*K),seed+1)*0.012
    img=np.ones((h,w,3),np.float32)*paper*(1+m[...,None])
    return img+np.random.default_rng(seed).normal(0,3.2,(h,w))[...,None]
def soak_in(art,paper,blobs,tide_col,seed=1):
    """art: the painting (same size); paper: rgb; returns the blot composite"""
    h,w=art.shape[:2]; soak,tide,dens=blot_mask(h,w,blobs,seed)
    base=aged_paper(h,w,paper,seed+10)
    # the ground soaks in unevenly; the painted elements (flower, leaves, pods) stay whole inside the blot
    gcol=np.median(art[::7,::7].reshape(-1,3),0)
    el=np.clip((np.abs(art-gcol).sum(2)-18)/40,0,1)
    a=np.maximum(soak*dens,el*np.clip(soak*1.6,0,1))[...,None]
    out=base*(1-a)+art*a
    tc=np.array([int(tide_col[i:i+2],16) for i in (1,3,5)],np.float32)
    t=(tide*0.55)[...,None]; out=out*(1-t)+tc*t
    return out
