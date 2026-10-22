# Ebony & Amber, round two. The flower in pure black that thins out to nothing towards the petal tips (no grey),
# 4: on its own with a small amber flower; 5: lit from behind by an amber glow, an eclipse.
import sys, numpy as np
from PIL import Image, ImageFilter
sys.path.insert(0,'/home/user/PersonalEventPlanner305App/vanilla-shop/brand/directions/bloom')
import bloom
O='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/soap/b3/'
K=bloom.K; W,H=150,95; G=np.array([236,233,228],np.float32)
yy,xx=np.mgrid[0:H*K,0:W*K].astype(np.float32)/K
def finish(a,name):
    rng=np.random.default_rng(11); h,w=a.shape[:2]
    a=a+rng.normal(0,12,(h,w,1))+rng.normal(0,3,(h,w,3))
    tooth=np.asarray(Image.fromarray(rng.normal(128,40,(h,w)).clip(0,255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.6))).astype(np.float32)-128
    Image.fromarray((a+0.35*tooth[...,None]).clip(0,255).astype(np.uint8)).save(O+name)
def place(im,cx,cy):
    c=Image.new('RGBA',(W*K,H*K),(0,0,0,0)); c.paste(im,(int((cx+7)*K-im.size[0]/2),int((cy+7)*K-im.size[1]/2)),im)
    a=np.asarray(c).astype(np.float32)/255; return a[...,:3]*255,a[...,3]
def black_flower(cx,cy,R,rot,blur,fall=1.6):
    S=int(R*2.4); n=O+'L-eb2'; bloom.bloom(n,S,S,S/2,S/2,R,'#000000','#000000','#000000',None,blur=blur,grain=0)
    a=np.asarray(Image.open(n+'.png')).astype(np.float32); y,x=np.mgrid[0:a.shape[0],0:a.shape[1]].astype(np.float32)/K
    r=np.hypot(x-S/2,y-S/2)/R; f=np.clip(1-r**fall,0,1)                       # solid at the heart, gone by the tips
    al=np.clip(a[...,3]/255*1.3,0,1)*f
    im=Image.fromarray(np.dstack([np.full(al.shape+(3,),9,np.float32),al*255]).astype(np.uint8),'RGBA').rotate(rot,resample=Image.BICUBIC)
    return place(im,cx,cy)
def amber_flower(cx,cy,R,rot):
    S=int(R*2.4); n=O+'L-eb2s'; bloom.bloom(n,S,S,S/2,S/2,R,'#B5651E','#F7DDB0','#E0913A',None,blur=2.3,grain=0)
    return place(Image.open(n+'.png').rotate(rot,resample=Image.BICUBIC),cx,cy)
def comp(a,rgb,al): return a*(1-al[...,None])+rgb*al[...,None]
B=black_flower(104,32,70,-30,4.4); S=amber_flower(66,14,15,22)
a=np.ones((H*K,W*K,3),np.float32)*G; a=comp(a,*S); a=comp(a,*B); finish(a,'D-ebony-4.png')
a=np.ones((H*K,W*K,3),np.float32)*G
d=np.hypot(xx-96,yy-26)/78; glow=np.clip(1-d,0,1)**1.3                      # amber light behind the flower
amb=np.array([214,130,46],np.float32); hot=np.array([246,196,120],np.float32)
a=comp(a,np.broadcast_to(amb,a.shape),glow*1.0); a=comp(a,np.broadcast_to(hot,a.shape),np.clip(1-d*1.8,0,1)**1.5*0.8)
a=comp(a,*B); finish(a,'D-ebony-5.png')
print('ok')
