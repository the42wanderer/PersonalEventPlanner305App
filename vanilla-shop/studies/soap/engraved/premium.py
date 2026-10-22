# Premium pass: our vanilla painting at full quality on deep, muted grounds (siblings of the candles), grain over all.
import numpy as np
from PIL import Image, ImageEnhance
G='/home/user/PersonalEventPlanner305App/vanilla-shop/plates/generated/'
O='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/soap/b2/'
K=12; W,H=150,95                         # art canvas = front (136 x 81) + 7 mm round it
GROUND={'vanilla':'#5E3E22','rosette':'#6E3540','ebony':'#2D2A28','aloe':'#47563F'}
def hx(c): return tuple(int(c[i:i+2],16) for i in (1,3,5))
def put(base,f,w_mm,cx,cy,rot=0,dim=1.0,flip=False,tint=None,amt=0.0):
    im=Image.open(G+f).convert('RGBA')
    if flip: im=im.transpose(Image.FLIP_LEFT_RIGHT)
    s=w_mm*K/im.size[0]; im=im.resize((int(im.size[0]*s),int(im.size[1]*s)),Image.LANCZOS)
    if rot: im=im.rotate(rot,expand=True,resample=Image.BICUBIC)
    if dim!=1.0:
        rgb=ImageEnhance.Brightness(im.convert('RGB')).enhance(dim); rgb.putalpha(im.getchannel('A')); im=rgb
    if tint is not None and amt>0:
        a=np.asarray(im).astype(np.float32); g=np.array(hx(tint),np.float32)
        L=(0.3*a[...,0]+0.59*a[...,1]+0.11*a[...,2])[...,None]/255
        toned=g*(0.55+0.9*L)                                    # the painting re-lit in the ground's own hue
        a[...,:3]=a[...,:3]*(1-amt)+toned*amt; im=Image.fromarray(a.clip(0,255).astype(np.uint8),'RGBA')
    base.alpha_composite(im,(int((cx+7)*K-im.size[0]/2),int((cy+7)*K-im.size[1]/2)))
TINT={'vanilla':('#C08A4A',0.35),'rosette':('#C46A78',0.2),'ebony':('#9A8E84',0.45),'aloe':('#8FAE80',0.3)}
def art(k):
    base=Image.new('RGBA',(W*K,H*K),hx(GROUND[k])+(255,)); t,m=TINT[k]
    if k=='rosette':
        put(base,'v9-candle-velvet-plant.png',230,118,34)
        put(base,'v6-vine.png',200,124,74,rot=10,tint=t,amt=m)
    else:
        pos={'vanilla':(132,52,-12),'ebony':(136,58,-26),'aloe':(130,47,4)}[k]
        put(base,'v6-vine.png',260,pos[0],pos[1],rot=pos[2],tint=t,amt=m)
    a=np.asarray(base.convert('RGB')).astype(np.float32)
    rng=np.random.default_rng(5)
    yy,xx=np.mgrid[0:H*K,0:W*K]/K; v=np.clip(1-0.12*(((xx-W*0.7)/W)**2+((yy-H*0.4)/H)**2)*4,0.85,1)
    a*=v[...,None]; a+=rng.normal(0,7,a.shape[:2])[...,None]
    Image.fromarray(a.clip(0,255).astype(np.uint8)).save(O+f'PR-{k}.png')
for k in GROUND: art(k)
print('ok')
