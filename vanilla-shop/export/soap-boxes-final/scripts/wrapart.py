# Artwork for the whole flat (back panel + wrap), at 12 px/mm with 3 mm bleed. Same flowers, veil and grain as the
# approved fronts (bloom-duo/duo.py), positioned in front-panel mm and carried over the walls of the wrap.
import sys, numpy as np
from PIL import Image, ImageFilter
sys.path.insert(0,'/home/user/PersonalEventPlanner305App/vanilla-shop/brand/directions/bloom')
import bloom
O='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/soap/full/'
KR=bloom.K; K=12; B=3.0; SW,SH=190.3,221.5; FX0,FY0,FX1,FY1,FLY=28.4,110.8,164.1,192.0,81.3
W,H=SW+2*B,SH+2*B; w,h=int(W*K),int(H*K)
CW={'vanilla':('#B5620F','#F8D79A','#D9822A','#F7EFDC'),
    'rosette':('#A8324E','#F8D3D6','#E08A6A','#F8EDE6'),
    'charcoal':('#060505','#958D85','#1E1B1A','#E4E2DE'),
    'aloe':   ('#2F5A2D','#CFE0A8','#C9A33A','#F2F1E2')}
LAY={'vanilla':((104,30,74,-14),(64,14,15,22)),'rosette':((108,34,72,10),(66,13,14,-26)),
     'charcoal':((102,28,76,-30),(64,14,15,6)),'aloe':((110,32,72,2),(66,14,15,-14))}
def hx(c): return np.array([int(c[i:i+2],16) for i in (1,3,5)],np.float32)
def layer(k,i,cx,cy,R,rot,blur):
    e,c,t,_=CW[k]; S=int(R*2.4); n=O+f'L-{k}-{i}'
    bloom.bloom(n,S,S,S/2,S/2,R,e,c,t,None,blur=blur,grain=0)
    im=Image.open(n+'.png').rotate(rot,resample=Image.BICUBIC); im=im.resize((int(im.size[0]*K/KR),)*2,Image.LANCZOS)
    X=(FX0+cx+B)*K; Y=(FY0+cy+B)*K
    return im,(int(X-im.size[0]/2),int(Y-im.size[1]/2))
def art(k):
    g=CW[k][3]; base=Image.new('RGBA',(w,h),tuple(int(v) for v in hx(g))+(255,))
    (b,s_)=LAY[k]
    sm,p=layer(k,'s',*s_,blur=2.2); base.paste(sm,p,sm)                 # the same passes as the approved fronts
    bg,p=layer(k,'b',*b,blur=5.2); base.paste(bg,p,bg); base.paste(bg,p,bg.getchannel('A').point(lambda v:int(v*0.5)))
    if k=='charcoal': base.paste(bg,p,bg.getchannel('A').point(lambda v:int(v*0.6)))
    a=np.asarray(base.convert('RGB')).astype(np.float32)
    yy,xx=np.mgrid[0:h,0:w].astype(np.float32)/K-B          # sheet mm
    # veil: plain paper behind the front's type, and quieter walls so their small text reads
    # the front's own veil, read at the nearest point of the front, then eased into each wall's level over ~12 mm
    fx=np.clip(xx,FX0,FX1)-FX0; fy=np.clip(yy,FY0,FY1)-FY0
    left=np.clip((88-fx)/50,0,1); left=left*left*(3-2*left); low=np.clip((fy-46)/32,0,1); low=low**1.4
    vf=np.maximum(left*0.82,low*0.86)
    topw=(yy<FY0)&(xx>=FX0)&(xx<=FX1); rightw=(xx>FX1)
    vw=np.where(yy<FLY,0.92,np.where(rightw,0.6,np.where(topw,0.72,0.78)))   # a faint ghost carries on over the back flap
    d=np.hypot(np.maximum(np.maximum(FX0-xx,xx-FX1),0),np.maximum(np.maximum(FY0-yy,yy-FY1),0))
    t=(d>0).astype(np.float32)          # each wall keeps its own level from the fold
    v=vf*(1-t)+vw*t
    a=a*(1-v[...,None])+hx(g)*v[...,None]
    # back panel: our engraved vanilla spray as a faint watermark in the soap's ink (about 9%), clipped to the back
    INK={'vanilla':'#5A3410','rosette':'#5A1426','charcoal':'#141414','aloe':'#16301C'}[k]
    sp=Image.open('/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/bw/spray-test.png').convert('L')
    m=Image.fromarray(255-np.asarray(sp)).rotate(-72,expand=True,resample=Image.BICUBIC)
    sc=150*K/max(m.size); m=m.resize((int(m.size[0]*sc),int(m.size[1]*sc)),Image.LANCZOS)
    Mk=Image.new('L',(w,h),0); Mk.paste(m,(int((FX0+84+B)*K-m.size[0]/2),int((40+B)*K-m.size[1]/2)))
    de=np.minimum(np.minimum(xx-FX0,FX1-xx),np.minimum(yy,FLY-yy)); ef=np.clip(de/14,0,1); ef=ef*ef*(3-2*ef)   # fade in from every edge
    rf=np.clip(1-np.hypot((xx-FX0-70)/80,(yy-40)/55),0,1)**0.7                                                  # and thin out from the middle
    wm=np.asarray(Mk).astype(np.float32)/255*ef*rf*0.11
    a=a*(1-wm[...,None])+hx(INK)*wm[...,None]
    rng=np.random.default_rng(11)
    mott=np.asarray(Image.fromarray(rng.normal(128,40,(h//36,w//36)).clip(0,255).astype(np.uint8)).resize((w,h),Image.BICUBIC)).astype(np.float32)-128
    a*=(1+0.008*mott/40)[...,None]
    a+=rng.normal(0,9,(h,w,1))+rng.normal(0,2.5,(h,w,3))
    tooth=np.asarray(Image.fromarray(rng.normal(128,40,(h,w)).clip(0,255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.0))).astype(np.float32)-128
    a+=0.3*tooth[...,None]
    Image.fromarray(a.clip(0,255).astype(np.uint8)).save(O+f'art-{k}.jpg',quality=93,subsampling=0)
for k in (sys.argv[1:] or CW): art(k); print(k)
