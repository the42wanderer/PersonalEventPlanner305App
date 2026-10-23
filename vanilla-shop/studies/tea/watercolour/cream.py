# Vanilla tea, after the Japanese-tea board: a cream paper box with our engraved vanilla printed very faintly all over
# (the Song Chao faded print), and a deep tea-green band along the foot of the front holding the watercolour flower,
# Ceylon tea flushes and cured pods (the extract labels' technique). Front-panel mm, 3 mm bleed.
import sys
sys.path.insert(0,'/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/teaart')  # teaflower.py lives beside this file in the repo
sys.path.insert(0,'/home/user/PersonalEventPlanner305App/vanilla-shop/studies/extract/split')
import numpy as np
from PIL import Image
import draw
from draw import Canvas, leaf
from comp import flower, mix
from teaflower import PAL, flush, pods
O='/home/user/PersonalEventPlanner305App/vanilla-shop/studies/tea/watercolour/cream/'
SP='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/bw/spray-test.png'
K=draw.K; B=3; PAPER=np.array([0xF6,0xEE,0xDC],np.float32); LINE=np.array([0xA9,0xBE,0x9E],np.float32); FADE=0.30
p=PAL['green']
def pattern(Wmm,Hmm,k=K,h=72,seed=1):
    """the engraved spray, tiled in a loose half-drop, flipped every other one, as a pale sage line on cream"""
    w,hh=int(Wmm*k),int(Hmm*k); img=np.ones((hh,w,3),np.float32)*PAPER
    src=Image.open(SP).convert('L'); sw=int(h*2400/3400*k); sh=int(h*k)
    A=src.resize((sw,sh),Image.LANCZOS); Bf=A.transpose(Image.FLIP_LEFT_RIGHT)
    M=Image.new('L',(w,hh),255); rng=np.random.default_rng(seed)
    for r in range(-1,int(Hmm/(h*0.78))+2):
        for c in range(-1,int(Wmm/(h*0.66))+2):
            t=(A if (r*3+c)%2 else Bf).rotate(rng.uniform(-18,18),expand=True,fillcolor=255)
            x=int((c*h*0.66+(r%2)*h*0.33+rng.uniform(-6,6))*k); y=int((r*h*0.78+rng.uniform(-6,6))*k)
            M.paste(t,(x,y),Image.fromarray(((255-np.asarray(t))>30).astype(np.uint8)*255))
    a=1-np.asarray(M).astype(np.float32)/255; a=np.clip((a-0.15)/0.7,0,1)*FADE
    img=img*(1-a[...,None])+LINE*a[...,None]
    img+=np.random.default_rng(seed).normal(0,4,(hh,w,1))
    return img
def front(name,W,H,band,art):
    """cream with the faded print; the band from y=band (panel mm) to the foot, painted"""
    img=pattern(W,H)
    bh=int(H+B-(band+B)); cv=Canvas(int(W),bh)
    art(cv)
    b=cv.render(p['ground'],grain=6,seed=5,raw=True)
    y0=int((band+B)*K); img[y0:y0+b.shape[0],:b.shape[1]]=b[:img.shape[0]-y0]
    Image.fromarray(img.clip(0,255).astype(np.uint8)).save(O+name)
def at(x,y): return (x,y)       # band coordinates are already canvas mm (x includes the 3 mm bleed)
def long_art(cv):     # band 182 x 40 mm: the picture runs the full width
    cv.add([leaf((176,30),200,60,12,0.3)],mix(p['leaf_core'],p['ground'],0.5),p['leaf_edge'],2.6,alpha=0.8)
    flush(cv,p,(22,46),-74,1.35,blur=0.75)
    flush(cv,p,(70,48),-104,1.05,blur=1.2,alpha=0.8)
    pods(cv,p,[((40,48),-12,110,3.0,0.1,1),((52,52),-18,100,2.6,0.08,-1)])
    flush(cv,p,(174,46),-112,1.3,blur=0.7)
    flower(cv,(128,22),35,2.05,p,blurs=(0.45,0.38,0.7))
def cube_art(cv):     # band 94 x 36 mm
    cv.add([leaf((96,26),205,44,9,0.3)],mix(p['leaf_core'],p['ground'],0.5),p['leaf_edge'],2.4,alpha=0.8)
    pods(cv,p,[((8,44),-14,90,2.6,0.1,1)])
    flush(cv,p,(14,42),-72,1.05,blur=0.75)
    flush(cv,p,(90,42),-110,1.0,blur=0.7)
    flower(cv,(58,20),35,1.55,p,blurs=(0.42,0.36,0.65))
front('long-cream.png',182,91,48,long_art)
front('cube-cream.png',94,91,52,cube_art)
Image.fromarray(pattern(260,260,k=12,seed=2).clip(0,255).astype(np.uint8)).save(O+'pattern.jpg',quality=92)
print('ok')
