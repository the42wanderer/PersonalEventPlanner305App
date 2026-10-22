# One-ink engraving: every form is a spine with a half-width, and its tone is built from lines that follow the form,
# swelling where it turns from the light, the way a burin engraver shades. Output is a 1-bit film (ink = True).
import math, numpy as np, cv2
from scipy.spatial import cKDTree
LIGHT=np.array([-0.55,-0.83])   # light from the upper left (page y runs down)
MIN_LINE=0.24; MIN_GAP=0.24      # mm: thinner lines or gaps would not survive a screen on canvas

def resample(sp,n):
    sp=np.asarray(sp,float); L=np.concatenate([[0],np.cumsum(np.linalg.norm(np.diff(sp,axis=0),axis=1))])
    u=np.linspace(0,L[-1],n); return np.stack([np.interp(u,L,sp[:,0]),np.interp(u,L,sp[:,1])],1), L[-1]

class Form:
    """a shape drawn round a spine. w: half-width (mm) per spine point, or a function of t in 0..1.
    tone: overall darkness 0..1. hatch: 'along' (lines follow the spine) or 'converge' (lines meet at the ends).
    rib: leave a pale line down the middle (a leaf's midrib). hi: where the highlight sits across (-1..1)."""
    def __init__(s,spine,w,tone=0.5,hatch='converge',pitch=0.72,rib=False,hi=-0.35,cross=0.72,outline=0.36,
                 round_=1.0,tip_dark=0.0,base_dark=0.0,shade=None,vein=35,solid=0.93):
        s.sp,s.len=resample(spine,400); t=np.linspace(0,1,len(s.sp))
        s.w=np.array([w(x) for x in t]) if callable(w) else np.interp(t,np.linspace(0,1,len(w)),w)
        d=np.gradient(s.sp,axis=0); d/=np.linalg.norm(d,axis=1,keepdims=True)+1e-9; s.d=d
        s.nr=np.stack([-d[:,1],d[:,0]],1)
        s.tone,s.hatch,s.pitch,s.rib,s.hi,s.cross,s.outline,s.round=tone,hatch,pitch,rib,hi,cross,outline,round_
        s.tip_dark,s.base_dark,s.shade_fn,s.vein,s.solid=tip_dark,base_dark,shade,vein,solid
        L=s.sp+s.nr*s.w[:,None]; R=s.sp-s.nr*s.w[:,None]; s.poly=np.vstack([L,R[::-1]])
    def bbox(s,pad=1.0):
        return s.poly.min(0)-pad, s.poly.max(0)+pad

class Plate:
    def __init__(s,W,H,K=20):
        s.W,s.H,s.K=W,H,K; s.ink=np.zeros((int(H*K),int(W*K)),bool); s.cover=np.zeros_like(s.ink)
    def px(s,p): return (np.asarray(p)*s.K).round().astype(np.int32)
    def mask_poly(s,poly,x0,y0,w,h):
        m=np.zeros((h,w),np.uint8); cv2.fillPoly(m,[((np.asarray(poly)*s.K)-[x0,y0]).round().astype(np.int32)],1,cv2.LINE_8); return m.astype(bool)
    def knock(s,poly):
        """paper inside a shape: whatever is behind it disappears"""
        m=np.zeros(s.ink.shape,np.uint8); cv2.fillPoly(m,[s.px(poly)],1); m=m.astype(bool); s.ink[m]=False; s.cover|=m
    def stroke(s,pts,width,closed=False):
        m=np.zeros(s.ink.shape,np.uint8)
        cv2.polylines(m,[s.px(pts)],closed,1,max(1,int(round(width*s.K))),cv2.LINE_AA); s.ink|=m.astype(bool); s.cover|=m.astype(bool)
    def fill(s,poly):
        m=np.zeros(s.ink.shape,np.uint8); cv2.fillPoly(m,[s.px(poly)],1); s.ink|=m.astype(bool); s.cover|=m.astype(bool)
    def form(s,f):
        K=s.K; (a,b)=f.bbox(); x0,y0=max(0,int(a[0]*K)),max(0,int(a[1]*K)); x1,y1=min(s.ink.shape[1],int(b[0]*K)+1),min(s.ink.shape[0],int(b[1]*K)+1)
        if x1<=x0 or y1<=y0: return
        w,h=x1-x0,y1-y0; inside=s.mask_poly(f.poly,x0,y0,w,h)
        ys,xs=np.nonzero(inside); P=np.stack([(xs+x0+0.5)/K,(ys+y0+0.5)/K],1)
        i=cKDTree(f.sp).query(P)[1]; off=np.einsum('ij,ij->i',P-f.sp[i],f.nr[i])
        v=np.clip(off/(f.w[i]+1e-6),-1,1); u=i/(len(f.sp)-1); arcl=u*f.len
        # tone: a rounded form, lit from the upper left, darker towards its turning edges
        facing=np.einsum('ij,j->i',f.nr[i],LIGHT)        # how the +v side faces the light
        sh=f.tone+0.42*f.round*(-v*facing)+0.28*f.round*np.abs(v)**2.5
        sh+=f.tip_dark*np.clip((u-0.75)/0.25,0,1)**1.5+f.base_dark*np.clip((0.2-u)/0.2,0,1)
        sh-=0.55*np.exp(-((v-f.hi)/0.16)**2)*f.round*(f.tone<0.85)          # the highlight band
        if f.shade_fn is not None: sh=f.shade_fn(u,v,sh)
        sh=np.clip(sh,0,1)
        # line family along the form
        if f.hatch=='along': d=off
        elif f.hatch=='vein': d=arcl*math.cos(math.radians(f.vein))-np.abs(off)*math.sin(math.radians(f.vein))
        else: d=v*f.w.max()
        p=f.pitch; ph=np.mod(d/p,1.0)-0.5; dist=np.abs(ph)*p
        lw=np.clip(sh*p*1.05,0,p-MIN_GAP); lw=np.where(lw<MIN_LINE*0.8,0,np.maximum(lw,MIN_LINE))
        ink=(dist<lw/2)|(sh>f.solid)
        # cross-hatching in the deepest shade
        if f.cross<1:
            q=p*1.15; ph2=np.mod(arcl/q,1.0)-0.5; lw2=np.clip((sh-f.cross)/(1-f.cross)*q*1.1,0,q-MIN_GAP)
            lw2=np.where(lw2<MIN_LINE*0.8,0,np.maximum(lw2,MIN_LINE)); ink|=np.abs(ph2)*q<lw2/2
        if f.rib: ink&=~((np.abs(v)<0.07+0.0*u)&(u>0.04)&(u<0.92))
        tile=np.zeros((h,w),bool); tile[ys,xs]=ink
        s.ink[y0:y1,x0:x1][inside]=False; s.ink[y0:y1,x0:x1]|=tile; s.cover[y0:y1,x0:x1]|=inside
        if f.outline: s.stroke(f.poly,f.outline,True)
        if f.rib: s.stroke(f.sp[int(len(f.sp)*0.03):int(len(f.sp)*0.9)],0.26)
    def save(s,path,paper=(241,233,214),ink=(20,18,16)):
        from PIL import Image
        a=np.where(s.ink[...,None],np.array(ink,np.uint8),np.array(paper,np.uint8)); Image.fromarray(a).save(path)

def paste(dst,src,x,y,halo=0.7):
    """lay a separately drawn plate onto dst at (x, y) mm (same K), clearing a thin paper margin round it"""
    K=dst.K; X,Y=int(round(x*K)),int(round(y*K)); h,w=src.ink.shape
    a0,b0=max(0,-Y),max(0,-X); a1,b1=min(h,dst.ink.shape[0]-Y),min(w,dst.ink.shape[1]-X)
    cov=src.cover[a0:a1,b0:b1].astype(np.uint8)
    if halo: r=int(round(halo*K)); cov=cv2.dilate(cov,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2*r+1,2*r+1)))
    reg=(slice(Y+a0,Y+a1),slice(X+b0,X+b1))
    dst.ink[reg]=(dst.ink[reg]&~cov.astype(bool))|src.ink[a0:a1,b0:b1]; dst.cover[reg]|=cov.astype(bool)
