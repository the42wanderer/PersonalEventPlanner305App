# grounds and art crops for the centred directions
import numpy as np
from PIL import Image, ImageFilter
G='/home/user/PersonalEventPlanner305App/vanilla-shop/plates/generated/'
T='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/ext/c/'
W,H=120*20,70*20
def hx(c): return np.array([int(c[i:i+2],16) for i in (1,3,5)],np.float32)
def ground(name,tl,tr,bl,br,grain=5,seed=1):
    y,x=np.mgrid[0:H,0:W].astype(np.float32); u=x/W; v=y/H
    c=(hx(tl)*((1-u)*(1-v))[...,None]+hx(tr)*(u*(1-v))[...,None]+hx(bl)*((1-u)*v)[...,None]+hx(br)*(u*v)[...,None])
    # soft light patch behind the name, as on the tea boxes
    r=np.sqrt(((u-0.5)/0.35)**2+((v-0.42)/0.5)**2); c+=(1-np.clip(r,0,1))[...,None]**2*np.array([6,5,2])
    rng=np.random.default_rng(seed); n=rng.normal(0,1,(H,W)).astype(np.float32)
    n=np.asarray(Image.fromarray(((n*40)+128).clip(0,255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7))).astype(np.float32)-128
    c+=n[...,None]/40*grain
    Image.fromarray(c.clip(0,255).astype(np.uint8)).save(T+f'g-{name}.jpg',quality=92)
GR={'alc':('#F8EFD5','#F4DFC2','#EECBB2','#E2B39E'),'free':('#F7EDCF','#F2D196','#F6E5BE','#EFCB8C'),'syrup':('#F5F2DF','#ECEDD3','#DCE3C2','#CCD9B8')}
for k,v in GR.items(): ground('tea-'+k,*v)
ground('cream','#F6EEDA','#F3E8D1','#F1E5CC','#EEE0C4',4,2)
ground('pod','#33221A','#2E1E16','#2A1A12','#24160F',6,3)
# art: flower cluster of the upright vine, and the whole vine
v=Image.open(G+'v7-vine-upright.png').convert('RGBA')
v.crop((70,800,960,1450)).save(T+'art-cluster.png'); v.crop((60,110,990,1450)).save(T+'art-vine.png')
# tonal versions (one colour family on cream), RGBA kept
TONE={'alc':('#5A1A10','#B4432C','#F3E4CC'),'free':('#5E3A0C','#C98A2A','#F6E6C4'),'syrup':('#16301C','#4F7448','#E6EBCF')}
def tone(src,k):
    a=np.asarray(Image.open(T+src)).astype(np.float32)/255; L=a[...,:3]@np.array([0.3,0.59,0.11],np.float32)
    L=np.clip((L-0.15)/0.75,0,1)**0.95; d,m,l=(hx(c)/255 for c in TONE[k])
    rgb=np.where((L<0.5)[...,None], d+(m-d)*(L/0.5)[...,None], m+(l-m)*((L-0.5)/0.5)[...,None])
    out=np.dstack([rgb,a[...,3:]]); Image.fromarray((out*255).clip(0,255).astype(np.uint8),'RGBA').save(T+src.replace('.png',f'-{k}.png'))
for k in TONE:
    tone('art-cluster.png',k); tone('art-vine.png',k)
print('ok')
