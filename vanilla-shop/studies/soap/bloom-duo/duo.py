# Bloom, two flowers: one large and cropped, one small, set on a diagonal; softer blur and heavier grain than the original.
import sys, numpy as np
from PIL import Image, ImageFilter
sys.path.insert(0,'/home/user/PersonalEventPlanner305App/vanilla-shop/brand/directions/bloom')
import bloom
O='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/soap/b3/'
K=bloom.K; W,H=150,95                       # front 136 x 81 + 7 mm round it
CW={'vanilla':('#B5620F','#F8D79A','#D9822A','#F7EFDC'),
    'rosette':('#A8324E','#F8D3D6','#E08A6A','#F8EDE6'),
    'ebony':  ('#8E3A1A','#F3CFA2','#E0913A','#E4E2DE'),
    'aloe':   ('#2F5A2D','#CFE0A8','#C9A33A','#F2F1E2')}
# (cx, cy, R, rotation) for the big and the small flower, in front mm
LAY={'vanilla':((104,30,74,-14),(64,14,15,22)),
     'rosette':((108,34,72,10),(66,13,14,-26)),
     'ebony':  ((102,28,76,-30),(64,14,15,6)),
     'aloe':   ((110,32,72,2),(66,14,15,-14))}
def layer(k,i,cx,cy,R,rot,blur):
    e,c,t,_=CW[k]; S=int(R*2.4)                      # draw on its own square, then rotate into place
    n=O+f'L-{k}-{i}'; bloom.bloom(n,S,S,S/2,S/2,R,e,c,t,None,blur=blur,grain=0)
    im=Image.open(n+'.png').rotate(rot,resample=Image.BICUBIC)
    return im,(int((cx+7)*K-im.size[0]/2),int((cy+7)*K-im.size[1]/2))
def hx(c): return np.array([int(c[i:i+2],16) for i in (1,3,5)],np.float32)
for k in (sys.argv[1:] or CW):
    g=CW[k][3]; base=Image.new('RGBA',(W*K,H*K),tuple(int(v) for v in hx(g))+(255,))
    (b,s)=LAY[k]
    sm,p=layer(k,"s",*s,blur=2.2); base.alpha_composite(sm,p) if False else base.paste(sm,p,sm)
    bg,p=layer(k,"b",*b,blur=5.2); base.paste(bg,p,bg); base.paste(bg,p,bg.getchannel("A").point(lambda v:int(v*0.5)))   # a second pass deepens the colour
    # a wide halo of the whole picture laid back over it, so the light bleeds like wet paint
    a=np.asarray(base.convert('RGB')).astype(np.float32); h,w=a.shape[:2]
    rng=np.random.default_rng(11)
    mott=np.asarray(Image.fromarray(rng.normal(128,40,(h//60,w//60)).clip(0,255).astype(np.uint8)).resize((w,h),Image.BICUBIC)).astype(np.float32)-128
    a*=(1+0.008*mott/40)[...,None]                               # paper mottling
    a+=rng.normal(0,11,(h,w,1))+rng.normal(0,3,(h,w,3))          # heavy fine mono grain, a little colour in it
    tooth=np.asarray(Image.fromarray(rng.normal(128,40,(h,w)).clip(0,255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.6))).astype(np.float32)-128
    a+=0.35*tooth[...,None]                                      # and a coarser tooth under it
    Image.fromarray(a.clip(0,255).astype(np.uint8)).save(O+f'D-{k}.png')
print('ok')
