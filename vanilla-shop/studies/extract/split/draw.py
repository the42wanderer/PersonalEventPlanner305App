# Organic vanilla drawing kit: everything is built from curved spines with width profiles, so nothing is geometric.
import math, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFilter
K=20; SS=2                       # px per mm, supersampling
def cr(pts,n=24):
    """Catmull-Rom through points -> dense polyline"""
    P=[pts[0]]+list(pts)+[pts[-1]]; out=[]
    for i in range(1,len(P)-2):
        p0,p1,p2,p3=map(np.array,(P[i-1],P[i],P[i+1],P[i+2]))
        for t in np.linspace(0,1,n,endpoint=False):
            out.append(0.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t**3))
    out.append(np.array(P[-2])); return np.array(out)
def ribbon(spine,prof,wave=0.0,freq=6,phase=0.0):
    """polygon around a spine; prof(t) gives the half-width in mm; wave ruffles the edges"""
    s=np.asarray(spine,float); d=np.gradient(s,axis=0); d/=np.linalg.norm(d,axis=1,keepdims=True)+1e-9
    nrm=np.stack([-d[:,1],d[:,0]],1); n=len(s); t=np.linspace(0,1,n)
    w=np.array([prof(x) for x in t]); wv=1+wave*np.sin(freq*2*np.pi*t+phase)
    L=s+nrm*(w*wv)[:,None]; R=s-nrm*(w*(1+wave*np.sin(freq*2*np.pi*t+phase+1.7)))[:,None]
    return np.vstack([L,R[::-1]])
def arc(p0,ang,L,bend,n=5,twist=0.0):
    """points along a gently bending path from p0 at angle ang (deg) of length L; bend in radians over its length"""
    pts=[np.array(p0,float)]; a=math.radians(ang); step=L/(n-1)
    for i in range(1,n):
        a+=bend/(n-1)+twist*math.sin(i/(n-1)*math.pi)/(n-1); pts.append(pts[-1]+step*np.array([math.cos(a),math.sin(a)]))
    return cr(pts,16)
def tepal(p0,ang,L,W,bend,wave=0.05,ph=0.0,pinch=0.0,spine=False):
    sp=arc(p0,ang,L,bend)
    if spine: return sp
    # narrow at the base, widest about 40% along, a long drawn-out tip; pinch suggests a twist
    prof=lambda t: W*min(1,0.4+t*3.0)*(math.sin(math.pi*min(t,0.999)**0.78)**0.8)*(1-pinch*math.exp(-((t-0.62)/0.09)**2))+0.03
    return ribbon(sp,prof,wave,5,ph)
def leaf(p0,ang,L,W,bend,spine=False):
    sp=arc(p0,ang,L,bend)
    if spine: return sp
    prof=lambda t: W*(math.sin(math.pi*t)**0.8)*(1-0.3*t)+0.08; return ribbon(sp,prof,0.015,3)
def pod(p0,ang,L,W,bend,curl=1,spine=False):
    sp=arc(p0,ang,L,bend,7)
    if spine: return sp
    # curl the last bit into a small hook
    end=sp[-1]; d=sp[-1]-sp[-3]; a=math.atan2(d[1],d[0]); r=W*1.1
    hook=[end+np.array([math.cos(a+curl*k*0.5),math.sin(a+curl*k*0.5)])*r*k/7 for k in range(1,8)]
    sp=np.vstack([sp,np.cumsum([h-end for h in hook],axis=0)*0.35+end])
    prof=lambda t: W*(min(1,t*6))**0.6*(1-0.75*t**3)+0.12; return ribbon(sp,prof,0.02,9)
def bud(p0,ang,L,W,bend):
    sp=arc(p0,ang,L,bend); prof=lambda t: W*math.sin(math.pi*t**0.6)**0.9*(1-0.2*t)+0.05; return ribbon(sp,prof)
def stem(pts,w): return ribbon(cr(pts,20),lambda t:w*(1-0.4*t)+0.05)
def ellipse_ruffle(c,rx,ry,rot,amp,n,k=180):
    t=np.linspace(0,2*np.pi,k); r=1+amp*np.abs(np.sin(n*t/2))**1.6-amp*0.5
    x=rx*r*np.cos(t); y=ry*r*np.sin(t); a=math.radians(rot)
    return np.stack([c[0]+x*math.cos(a)-y*math.sin(a), c[1]+x*math.sin(a)+y*math.cos(a)],1)
def trumpet(base,ang,L,r0,rx,ry,ruffle=0.08):
    """the labellum: a tube from the column widening to a frilled mouth seen at an angle"""
    a=math.radians(ang); d=np.array([math.cos(a),math.sin(a)]); n=np.array([-d[1],d[0]])
    mouth_c=np.array(base)+d*L
    mouth=ellipse_ruffle(mouth_c,ry,rx,ang,ruffle,9)            # mouth faces along d, so its long axis runs across it
    tube=np.array([np.array(base)+n*r0, mouth_c+n*rx*0.95, mouth_c-n*rx*0.95, np.array(base)-n*r0])
    return tube, mouth, mouth_c
class Canvas:
    def __init__(s,W,H,ox=0): s.W,s.H,s.ox=W,H,ox; s.layers=[]
    def add(s,polys,core,edge,blur,depth=1.0,alpha=1.0,glow=1.0,centre=None,R=None,halo=0.35,wash=None):
        s.layers.append((polys if isinstance(polys,list) else [polys],core,edge,blur,alpha,glow,centre,R,halo,wash))
    def mask(s,polys):
        im=Image.new('L',(s.W*K*SS,s.H*K*SS),0); d=ImageDraw.Draw(im)
        for p in polys:
            wgt=1.0
            if isinstance(p,tuple) and len(p)==2 and np.isscalar(p[1]): p,wgt=p
            if wgt<=0.01: continue
            d.polygon([tuple(v) for v in ((np.asarray(p)+np.array([s.ox,0]))*K*SS)],fill=int(255*min(1,wgt)))
        return np.asarray(im.resize((s.W*K,s.H*K),Image.LANCZOS)).astype(np.float32)/255
    def render(s,ground,grain=8,seed=1,base=None,raw=False):
        g=np.array([int(ground[i:i+2],16) for i in (1,3,5)],np.float32)
        img=np.ones((s.H*K,s.W*K,3),np.float32)*g if base is None else base.copy()
        for polys,core,edge,blur,alpha,glow,centre,R,halo,wash in s.layers:
            m=s.mask(polys)
            # interior distance -> light core, saturated edge (the Bloom pin's petals)
            dist=cv2.distanceTransform((m>0.5).astype(np.uint8),cv2.DIST_L2,5)/K
            if centre is not None:
                yy,xx=np.mgrid[0:s.H*K,0:s.W*K].astype(np.float32)/K
                t=1-np.clip(np.hypot(xx-centre[0]-s.ox,yy-centre[1])/R,0,1)**(0.9*glow)
            else:
                dmax=max(dist.max(),0.01); t=np.clip(dist/(dmax*0.7),0,1)**(0.55/glow)
            cc=np.array([int(core[i:i+2],16) for i in (1,3,5)],np.float32); ec=np.array([int(edge[i:i+2],16) for i in (1,3,5)],np.float32)
            col=ec+(cc-ec)*t[...,None]
            sig=blur*K
            col=cv2.GaussianBlur(col,(0,0),sig*0.6+0.1)
            a=cv2.GaussianBlur(m,(0,0),sig+0.1)*alpha
            halo=cv2.GaussianBlur(m,(0,0),sig*2.8+1)*halo*alpha
            a=np.clip(a+halo*(1-a),0,1)
            img=img*(1-a[...,None])+col*a[...,None]
            if wash:
                # watercolour: pigment gathers at the edge of a wash as it dries
                er=cv2.erode((m>0.5).astype(np.uint8),np.ones((int(wash[1]*K)*2+1,)*2,np.uint8))
                ring=np.clip(m-er.astype(np.float32),0,1); ring=cv2.GaussianBlur(ring,(0,0),K*0.25)
                wc=np.array([int(wash[0][i:i+2],16) for i in (1,3,5)],np.float32); ra=ring*wash[2]
                img=img*(1-ra[...,None])+wc*ra[...,None]
        n=np.random.default_rng(seed).normal(0,1,img.shape[:2]).astype(np.float32)*grain
        img+=n[...,None]
        if raw: return img
        return Image.fromarray(img.clip(0,255).astype(np.uint8))

def green_pod(p0,ang,L,W,bend,curl=0):
    """a fresh green pod: a slim, slightly curved bean, round at the end, on a short stalk"""
    sp=arc(p0,ang,L,bend,6)
    prof=lambda t: (0.4 if t<0.06 else W*0.5*(1+0.25*math.sin(math.pi*min(1,(t-0.07)/0.93))) *math.sqrt(max(0,1-max(0,(t-0.9)/0.1)**2)))+0.05
    return ribbon(sp,prof)
