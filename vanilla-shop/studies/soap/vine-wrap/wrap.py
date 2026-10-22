# Soap wrap after real wrapped-bar packaging: the paper is an all-over pattern of our own vanilla vine painting
# (the tea-box art), toned into each soap's colours with grain; the type lives on a calm cream band.
import numpy as np, random
from PIL import Image, ImageFilter
G='/home/user/PersonalEventPlanner305App/vanilla-shop/plates/generated/'
O='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/soap/b2/'
SRC=['v6-vine.png','v7-vine-upright.png','v6-sprig.png','v7-vine-upright-b.png','v8-crop-vine-trail.png']
RAMP={'vanilla':('#5C3410','#C98A2E','#F6DFAE','#F1DDB5'),'rosette':('#5E1429','#C9607C','#F8D6DE','#F2D3D9'),
      'ebony':('#0E0C0B','#7A4E1A','#E2AE62','#1F1A18'),'aloe':('#163A1E','#5E9A66','#DDEDCB','#DAE8C7')}
def hx(c): return np.array([int(c[i:i+2],16) for i in (1,3,5)],np.float32)
def tone(im,dk,md,lt):
    a=np.asarray(im).astype(np.float32); L=(0.3*a[...,0]+0.59*a[...,1]+0.11*a[...,2])/255
    L=np.clip((L-0.12)/0.8,0,1)
    c=np.where(L[...,None]<0.5, hx(dk)+(hx(md)-hx(dk))*(L[...,None]/0.5), hx(md)+(hx(lt)-hx(md))*((L[...,None]-0.5)/0.5))
    return Image.fromarray(np.dstack([c,a[...,3]]).clip(0,255).astype(np.uint8),'RGBA')
def wrap(k,W=150,H=95,K=12,seed=4):
    dk,md,lt,gr=RAMP[k]; w,h=W*K,H*K
    base=Image.new('RGBA',(w,h),tuple(int(v) for v in hx(gr))+(255,))
    rnd=random.Random(seed)
    srcs=[tone(Image.open(G+f).convert('RGBA'),dk,md,lt) for f in SRC]
    # a loose half-drop repeat of sprays, varied in size and angle, as on a printed wrapping paper
    for row in range(-1,4):
        for col in range(-1,5):
            im=srcs[(row*3+col)%len(srcs)]
            s=rnd.uniform(0.9,1.1)*K*58/max(im.size)
            sp=im.resize((int(im.size[0]*s),int(im.size[1]*s)),Image.LANCZOS).rotate(rnd.uniform(-35,35)+(row%2)*180,expand=True,resample=Image.BICUBIC)
            x=int((col*50+(row%2)*25+rnd.uniform(-4,4))*K-sp.size[0]/2); y=int((row*36+rnd.uniform(-3,3))*K-sp.size[1]/2)
            base.alpha_composite(sp,(x,y)) if 0<=x and 0<=y and x+sp.size[0]<=w and y+sp.size[1]<=h else base.paste(sp,(x,y),sp)
    a=np.asarray(base.convert('RGB')).astype(np.float32)
    rng=np.random.default_rng(seed)
    mott=np.asarray(Image.fromarray((rng.normal(128,40,(h//90,w//90))).clip(0,255).astype(np.uint8)).resize((w,h),Image.BICUBIC)).astype(np.float32)-128
    a*= (1+0.012*mott/40)[...,None]; a+=rng.normal(0,6,(h,w,1))
    Image.fromarray(a.clip(0,255).astype(np.uint8)).save(O+f'W-{k}.png')
for k in RAMP: wrap(k)
print('ok')
