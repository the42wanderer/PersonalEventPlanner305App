# Ebony & Amber, black done the way the references do it: solid black at the heart, fading out into the paper.
import sys, numpy as np
from PIL import Image, ImageFilter
sys.path.insert(0,'/home/user/PersonalEventPlanner305App/vanilla-shop/brand/directions/bloom'); sys.path.insert(0,'/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/soap/b3')
import bloom
O='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/soap/b3/'
K=bloom.K; W,H=150,95; G=np.array([236,233,228],np.float32)
yy,xx=np.mgrid[0:H*K,0:W*K].astype(np.float32)/K
def finish(a,name):
    rng=np.random.default_rng(11); h,w=a.shape[:2]
    a=a+rng.normal(0,12,(h,w,1))+rng.normal(0,3,(h,w,3))
    tooth=np.asarray(Image.fromarray(rng.normal(128,40,(h,w)).clip(0,255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.6))).astype(np.float32)-128
    a=a+0.35*tooth[...,None]; Image.fromarray(a.clip(0,255).astype(np.uint8)).save(O+name)
def over(base,rgb,alpha): return base*(1-alpha[...,None])+np.asarray(rgb,np.float32)*alpha[...,None]
def flower(k,cx,cy,R,rot,edge,core,throat,blur):
    S=int(R*2.4); n=O+f'L-eb-{k}'; bloom.bloom(n,S,S,S/2,S/2,R,edge,core,throat,None,blur=blur,grain=0)
    im=Image.open(n+'.png').rotate(rot,resample=Image.BICUBIC); c=Image.new('RGBA',(W*K,H*K),(0,0,0,0))
    c.paste(im,(int((cx+7)*K-im.size[0]/2),int((cy+7)*K-im.size[1]/2))); a=np.asarray(c).astype(np.float32)/255
    return a[...,:3]*255,a[...,3]
base=np.ones((H*K,W*K,3),np.float32)*G
# 1. the flower inverted: black at the lip and throat, greying out to nothing at the petal tips; small one in amber
a=base.copy()
rgb,al=flower('1s',66,14,15,22,'#B5651E','#F4D3A2','#E0913A',2.2); a=a*(1-al[...,None])+rgb*al[...,None]
rgb,al=flower('1b',104,30,74,-30,'#B9B2AA','#0A0908','#0A0908',5.2); al=np.clip(al*1.25,0,1); a=a*(1-al[...,None])+rgb*al[...,None]
finish(a,'D-ebony-1.png')
# 2. two charcoal pebbles, large and small: a hard black body with a soft halo falling away on one side
def pebble(a,cx,cy,rx,ry,ang,dx,dy):
    t=np.radians(ang); X=(xx-cx)*np.cos(t)+(yy-cy)*np.sin(t); Y=-(xx-cx)*np.sin(t)+(yy-cy)*np.cos(t)
    def ell(sx,sy,ox,oy,soft):
        Xo=X-ox; Yo=Y-oy; d=np.sqrt((Xo/sx)**2+(Yo/sy)**2); return np.clip((1-d)/soft+0.5,0,1)
    halo=ell(rx*1.25,ry*1.25,dx,dy,0.9)**1.6*0.85; body=ell(rx,ry,0,0,0.14)
    m=np.maximum(halo,body)
    return over(a,(10,9,8),m)
a=base.copy(); a=pebble(a,108,36,27,21,-12,-5,-8); a=pebble(a,66,14,9,7,10,2,4); finish(a,'D-ebony-2.png')
# 3. a black sun: one soft radial mass, solid at the centre, fading out to paper; a small amber flower glowing at its rim
a=base.copy(); d=np.hypot(xx-110,(yy-34)*1.05); m=np.clip(1-(d-12)/50,0,1); m=m*m*(3-2*m); a=over(a,(10,9,8),m)
rgb,al=flower('3s',62,18,16,18,'#B5651E','#F7DDB0','#E0913A',2.4); a=a*(1-al[...,None])+rgb*al[...,None]
finish(a,'D-ebony-3.png')
print('ok')
