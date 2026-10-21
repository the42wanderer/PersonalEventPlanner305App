# Re-screen the AI image: keep its brush line work, replace its uneven, mixed dot patterns with one true halftone
# (round dots on a 45-degree grid, fixed pitch), as a printed comic would have it.
import numpy as np, cv2
from PIL import Image
SRC='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/images/92.webp'
def load(): return np.asarray(Image.open(SRC).convert('L')).astype(np.float32)/255
def analyse(g, s=2):
    """g: source greyscale 0..1. Returns (ink, tone, dotted) at s x the source size."""
    h,w=g.shape; G=cv2.resize(g,(w*s,h*s),interpolation=cv2.INTER_CUBIC)
    ink=(G<0.5).astype(np.float32)
    # tone the dots stand for: ink coverage averaged over about two dot pitches
    tone=cv2.GaussianBlur(ink,(0,0),2.4*s)
    # dots vs lines: a dot field is unoriented, so its structure tensor has low coherence; lines are strongly oriented
    gx=cv2.Sobel(G,cv2.CV_32F,1,0,ksize=3); gy=cv2.Sobel(G,cv2.CV_32F,0,1,ksize=3)
    S=lambda a:cv2.GaussianBlur(a,(0,0),2.2*s)
    jxx,jyy,jxy=S(gx*gx),S(gy*gy),S(gx*gy)
    lam=np.sqrt((jxx-jyy)**2+4*jxy**2); coh=lam/(jxx+jyy+1e-6)
    # fine detail: how much the ink flips over a small distance (dots flip a lot, flat areas don't)
    busy=cv2.GaussianBlur(np.abs(ink-cv2.GaussianBlur(ink,(0,0),1.0*s)),(0,0),2.0*s)
    dotted=(coh<0.42)&(tone>0.04)&(tone<0.82)&(busy>0.12)
    dm=dotted.astype(np.uint8)
    dm=cv2.morphologyEx(dm,cv2.MORPH_OPEN,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3*s,3*s)))
    dm=cv2.morphologyEx(dm,cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5*s,5*s)))
    return ink, tone, dm.astype(bool)
def halftone(tone, K, pitch_mm=1.35, angle=45, min_dot=0.30):
    """round-dot AM screen. tone 0..1 (1 = solid). pitch in mm, K px per mm."""
    h,w=tone.shape; p=pitch_mm*K; a=np.radians(angle)
    yy,xx=np.mgrid[0:h,0:w].astype(np.float32)
    u=(xx*np.cos(a)+yy*np.sin(a))/p; v=(-xx*np.sin(a)+yy*np.cos(a))/p
    du=u-np.round(u); dv=v-np.round(v); d=np.sqrt(du*du+dv*dv)*p           # distance to the nearest dot centre, px
    # dot radius for a coverage t: pi r^2 / p^2 = t (round dots up to ~78%, then the cells join)
    t=np.clip(tone,0,1); r=np.sqrt(t/np.pi)*p
    r=np.where(t>0.78, p*(0.5+0.35*(t-0.78)/0.22), r)
    r=np.where(r<min_dot*K/2, 0, r)                                          # no dots that would not print
    out=d<r
    out|=t>0.93
    return out
if __name__=='__main__':
    g=load(); ink,tone,dot=analyse(g)
    vis=np.dstack([np.where(ink>0,40,235)]*3).astype(np.uint8); vis[dot]=(vis[dot]*0.5+np.array([255,60,160])*0.5).astype(np.uint8)
    Image.fromarray(vis).save('dotmask.png'); print('dotted %',round(dot.mean()*100,1))
