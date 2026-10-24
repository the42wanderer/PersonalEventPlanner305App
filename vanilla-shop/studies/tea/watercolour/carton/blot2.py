# Watercolour that fades the way watercolour does: several transparent glazes, each its own irregular blot, paler and
# wider outward; edges hard (with a tide line) where the paper was dry and feathered where it was wet; a second
# pigment bleeding in wet-in-wet; pigment granulating in the paper's tooth; glazes multiply the paper, never cover it.
import numpy as np, cv2
K=20
def fbm(h,w,cell,seed,oct=4):
    r=np.random.default_rng(seed); out=np.zeros((h,w),np.float32); a=1; t=0
    for o in range(oct):
        c=max(2,int(cell/2**o)); g=r.normal(0,1,(h//c+3,w//c+3)).astype(np.float32)
        out+=a*cv2.resize(g,(w,h),interpolation=cv2.INTER_CUBIC)[:h,:w]; t+=a; a*=0.5
    return out/t
def smooth(a,b,x): t=np.clip((x-a)/(b-a),0,1); return t*t*(3-2*t)
def rgb(c): return np.array([int(c[i:i+2],16) for i in (1,3,5)],np.float32)/255
def glaze(h,w,centres,scale,seed,wet_bias=0.0):
    """one wash: an irregular blot; returns (coverage 0..1, tide 0..1)"""
    yy,xx=np.mgrid[0:h,0:w].astype(np.float32)
    f=np.full((h,w),-9,np.float32)
    for (cx,cy,rx,ry) in centres: f=np.maximum(f,1-np.hypot((xx-cx)/(rx*scale),(yy-cy)/(ry*scale)))
    f+=0.20*fbm(h,w,int(30*K),seed)+0.06*fbm(h,w,int(6*K),seed+1)+0.015*fbm(h,w,int(0.9*K),seed+2,2)
    wet=smooth(-0.3,0.5,fbm(h,w,int(22*K),seed+3)+wet_bias)             # where the paper was wet, the edge feathers
    soft=0.012+0.20*wet
    cov=np.clip(0.5+f/(2*soft),0,1); cov=cov*cov*(3-2*cov)
    er=cv2.erode((cov>0.5).astype(np.uint8),cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(int(1.1*K),)*2)).astype(np.float32)
    tide=cv2.GaussianBlur(np.clip((cov>0.5).astype(np.float32)-er,0,1),(0,0),0.3*K)*(1-wet)
    inside=0.82+0.18*fbm(h,w,int(10*K),seed+4)                          # pigment settles unevenly
    return cov*inside,tide
def paint_wash(h,w,paper,layers,seed=1):
    """layers: (centres, scale, colour, strength, wet_bias); returns the paper with the glazes multiplied in"""
    img=np.ones((h,w,3),np.float32)*paper/255
    tooth=fbm(h,w,int(0.35*K),seed+50,2)
    for i,(centres,scale,col,stren,wb) in enumerate(layers):
        cov,tide=glaze(h,w,centres,scale,seed+10*i,wb)
        a=np.clip(cov*stren+tide*stren*0.55,0,1)
        a=a*(1+0.09*tooth)                                              # granulation in the tooth
        c=rgb(col); img=img*(1-a[...,None]*(1-c))                       # transparent: multiplies the paper
    return img*255

def lift(cv):
    """render the painting over black and over white: gives each element its true colour and transparency"""
    a=cv.render('#000000',grain=0,raw=True); b=cv.render('#FFFFFF',grain=0,raw=True)
    al=np.clip(1-(b-a).mean(2)/255,0,1)
    col=np.where(al[...,None]>1e-3,a/np.maximum(al[...,None],1e-3),0)
    return np.clip(col,0,255),al

def lift(cv):
    """render the painting over black and over white: gives each element its true colour and transparency"""
    a=cv.render('#000000',grain=0,raw=True); b=cv.render('#FFFFFF',grain=0,raw=True)
    al=np.clip(1-(b-a).mean(2)/255,0,1)
    col=np.where(al[...,None]>1e-3,a/np.maximum(al[...,None],1e-3),0)
    return np.clip(col,0,255),al
