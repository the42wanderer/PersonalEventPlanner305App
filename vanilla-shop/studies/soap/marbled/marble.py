# Procedural marbling (ebru / marbled soap): colour bands combed and swirled by a warped flow, with fine veins and paper grain.
import numpy as np, cv2
from PIL import Image
def fbm(h,w,scale,oct,seed):
    r=np.random.default_rng(seed); out=np.zeros((h,w),np.float32); a=1; t=0
    for o in range(oct):
        s=max(2,int(scale/2**o)); g=r.standard_normal((h//s+3,w//s+3)).astype(np.float32)
        out+=a*cv2.resize(g,(w,h),interpolation=cv2.INTER_CUBIC)[:h,:w]; t+=a; a*=0.5
    return out/t
def hx(c): return np.array([int(c[i:i+2],16) for i in (1,3,5)],np.float32)
def marble(out,W,H,K,bands,vein,seed=1,calm=None,calm_col=None,grain=6,veins=False):
    h,w=int(H*K),int(W*K); yy,xx=np.mgrid[0:h,0:w].astype(np.float32)/K
    # flow: two passes of domain warping, then a comb (tine strokes) and a gentle swirl
    q1=fbm(h,w,int(70*K),3,seed); q2=fbm(h,w,int(70*K),3,seed+1)
    x1=xx+16*q1; y1=yy+11*q2
    r1=fbm(h,w,int(34*K),2,seed+2); r2=fbm(h,w,int(34*K),2,seed+3)
    x2=x1+4*r1; y2=y1+3*r2
    y2=y2+4.5*np.sin(x2/13.0)+1.2*np.sin(x2/4.1)                                    # comb drawn across
    cx,cy=W*0.72,H*0.32; dx,dy=x2-cx,y2-cy; rr=np.sqrt(dx*dx+dy*dy)+1e-3
    ang=2.4*np.exp(-rr/30); ca,sa=np.cos(ang),np.sin(ang)
    x3=cx+dx*ca-dy*sa; y3=cy+dx*sa+dy*ca                        # a swirl, as if a stylus was dragged round
    phase=(y3*0.042+0.004*x3)                               # band position
    n=len(bands); t=(phase%1.0)*n; i0=np.floor(t).astype(int)%n; f=t-np.floor(t)
    f=np.clip((f-0.3)/0.4,0,1); f=f*f*(3-2*f)                  # crisp-ish edges between bands, like paint on size
    P=np.stack([hx(c) for c in bands]); col=P[i0]*(1-f[...,None])+P[(i0+1)%n]*f[...,None]
    # veins: thin lines where a second, finer band field crosses zero
    v=np.abs(np.sin((phase*n+0.5)*np.pi))
    vm=np.clip(1-v/0.035,0,1)*0.7
    if veins: col=col*(1-vm[...,None])+hx(vein)*vm[...,None]
    col*=(1+0.06*fbm(h,w,int(6*K),3,seed+11))[...,None]           # pigment unevenness inside each band
    if calm is not None:                                         # a quieter zone where the type sits
        m=np.clip((yy-calm[0])/(calm[1]-calm[0]),0,1)[...,None]; m=m*m*(3-2*m)
        col=col*(1-m*0.82)+hx(calm_col)*m*0.82
    # paper: soft mottling, tooth and fine grain
    col*= (1+0.03*fbm(h,w,int(12*K),3,seed+7))[...,None]
    col+= np.random.default_rng(seed+9).normal(0,grain,(h,w,1))
    Image.fromarray(np.clip(col,0,255).astype(np.uint8)).save(out)
if __name__=='__main__':
    O='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/soap/b2/'
    P={'vanilla':(['#F4E2BC','#E8B65E','#F7ECD2','#C98A2E','#F1D7A0'],'#5A3414','#F3E4C2',3),
       'rosette':(['#F6DCDF','#E58BA0','#FBEDEE','#B9415F','#F0BCC7'],'#6A1A30','#F7E3E5',5),
       'ebony':(['#2A2522','#3D3531','#1B1715','#58463A','#2F2926'],'#D9A04A','#211C1A',7),
       'aloe':(['#DDEBCB','#86B98A','#EEF5E2','#3F7A47','#B9D9A8'],'#1E3F24','#E5F0D6',11)}
    for k,(b,v,c,sd) in P.items():
        marble(O+f'M-{k}.png',150,95,10,b,v,sd,veins=(k=='ebony'))
        marble(O+f'MC-{k}.png',150,95,10,b,v,sd,calm=(40,60),calm_col=c,veins=(k=='ebony'))
    print('ok')
