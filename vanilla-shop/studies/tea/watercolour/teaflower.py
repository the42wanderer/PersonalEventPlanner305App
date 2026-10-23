# Vanilla tea artwork, the watercolour flower (round one) refined: the flower stays the hero; Ceylon tea flushes,
# two leaves and a bud, frame it in the same technique; cured pods underneath. Composed round the shared front
# layout (information top left, logo and lion top right, the name on the foot rule bottom left).
# Front-panel mm; the canvas carries 3 mm bleed.
import sys
sys.path.insert(0,'/home/user/PersonalEventPlanner305App/vanilla-shop/studies/extract/split')
import numpy as np, draw
from draw import Canvas, leaf, pod, bud, stem
from comp import flower, mix, sheen
from PIL import Image
O='/home/user/PersonalEventPlanner305App/vanilla-shop/studies/tea/watercolour/flower-tea/'
B=3
PAL={'green':dict(ground='#1F4732',tep_core='#FFF9EC',tep_edge='#B3CFA0',lip_core='#FFFCF2',lip_edge='#E3EDCC',throat_core='#F3C75E',throat_edge='#D69B3A',
                  leaf_core='#6E9C6A',leaf_edge='#173A26',pod_core='#3E2416',pod_edge='#1D1310',
                  tea_core='#BEDC86',tea_edge='#2F6230',tbud_core='#EEF6D2',tbud_edge='#9CC47A',tstem='#8AB46C'),
     'teal':dict(ground='#2C6466',tep_core='#F4FBF2',tep_edge='#8FC3B6',lip_core='#FBFDF4',lip_edge='#CDE6D8',throat_core='#F1C55E',throat_edge='#D49A3A',
                  leaf_core='#7DB59E',leaf_edge='#1F4D4C',pod_core='#3E2416',pod_edge='#1D1310',
                  tea_core='#A9D3A0',tea_edge='#235A4E',tbud_core='#E6F4E2',tbud_edge='#8CC0A8',tstem='#7CB09A')}
def at(p): return (p[0]+B,p[1]+B)
def flush(cv,p,base,ang,s,blur=0.8,alpha=1.0):
    """a Ceylon tea flush: two leaves and a bud on a short stem, the leaves broad with a sheen down the midrib"""
    a=np.radians(ang); P=lambda d,o=0:(base[0]+np.cos(a)*d*s-np.sin(a)*o*s, base[1]+np.sin(a)*d*s+np.cos(a)*o*s)
    tip=P(26); m1=P(9,0.8); m2=P(17,-0.6)
    cv.add([stem([at(base),at(m1),at(m2),at(tip)],0.6*s)],mix(p['tstem'],'#FFFFFF',0.2),p['tstem'],blur*0.8,alpha=alpha)
    lv=[(at(m1),ang-62,19*s,5.6*s,-0.3),(at(m2),ang+52,15*s,4.6*s,0.28)]
    cv.add([leaf(*q) for q in lv],p['tea_core'],p['tea_edge'],blur,alpha=alpha,glow=1.1)
    sheen(cv,[leaf(*q,spine=True) for q in lv],0.38*s,mix(p['tea_core'],'#FFFFFF',0.4),p['tea_core'],blur,0.5*alpha)
    cv.add([bud(at(tip),ang-6,9*s,2.0*s,0.12)],p['tbud_core'],p['tbud_edge'],blur*0.8,alpha=alpha,glow=1.3)
def pods(cv,p,specs):
    q=[(at(s_[0]),*s_[1:]) for s_ in specs]
    cv.add([pod(*x) for x in q],p['pod_core'],p['pod_edge'],0.6,glow=0.9)
    sheen(cv,[pod(*x,spine=True)[3:-6]+np.array([0,-0.25*x[3]]) for x in q],0.8,mix(p['pod_core'],'#FFFFFF',0.35),p['pod_core'],0.55,0.55)
def finish(cv,p,name,c,r):
    img=cv.render(p['ground'],grain=0,raw=True)
    yy,xx=np.mgrid[0:img.shape[0],0:img.shape[1]].astype(np.float32)/draw.K-B
    g=np.clip(1-np.hypot(xx-c[0],yy-c[1])/r,0,1)**1.6; img=img*(1+0.12*g[...,None])
    img+=np.random.default_rng(21).normal(0,1,img.shape[:2]).astype(np.float32)[...,None]*8
    Image.fromarray(img.clip(0,255).astype(np.uint8)).save(O+name)
def long_front(k):   # panel 176 x 85: brand and information top left, name bottom left, the flower big top right
    p=PAL[k]; cv=Canvas(182,91); c=(138,33)
    cv.add([leaf(at((186,6)),160,66,13,0.3)],mix(p['leaf_core'],p['ground'],0.5),p['leaf_edge'],2.8,alpha=0.8)
    flush(cv,p,(100,-6),66,1.45,blur=1.6,alpha=0.75)           # a flush hanging in from the top edge, behind, soft
    pods(cv,p,[((96,94),-14,100,3.4,0.16,1),((106,100),-22,92,3.0,0.1,-1)])
    flush(cv,p,(176,94),-104,2.0,blur=0.7)                    # a flush rising from the bottom right, in front
    flower(cv,at(c),40,3.0,p,blurs=(0.45,0.38,0.7))
    finish(cv,p,f'long-{k}.png',c,64)
def cube_front(k):   # panel 88 x 85: the flower big top right, cropped by the top edge
    p=PAL[k]; cv=Canvas(94,91); c=(66,27)
    cv.add([leaf(at((98,58)),190,48,10,0.3)],mix(p['leaf_core'],p['ground'],0.5),p['leaf_edge'],2.6,alpha=0.75)
    pods(cv,p,[((42,96),-20,80,2.9,0.12,1)])
    flush(cv,p,(90,94),-104,1.6,blur=0.7)
    flower(cv,at(c),100,2.1,p,blurs=(0.42,0.36,0.65))
    finish(cv,p,f'cube-{k}.png',c,46)
if __name__=='__main__':
    for k in (sys.argv[1:] or PAL): long_front(k); cube_front(k); print(k)
