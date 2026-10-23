# Vanilla tea artwork, round two: a cup of Ceylon tea seen from above, a vanilla flower floating on it, the tea flush
# and cured pods beside it, all in the extract labels' watercolour technique on one teal ground. Coordinates are
# front-panel mm; the canvas carries 3 mm bleed, so everything is shifted by +3.
import sys
sys.path.insert(0,'/home/user/PersonalEventPlanner305App/vanilla-shop/studies/extract/split')
import numpy as np, draw
from draw import Canvas, leaf, pod, bud, stem, ellipse_ruffle
from comp import flower, mix, sheen
from teaart import PAL, tea_sprig
O='/home/user/PersonalEventPlanner305App/vanilla-shop/studies/tea/watercolour/cup/'
B=3
TEA=dict(core='#F0B566',edge='#8A4518')
def at(p): return (p[0]+B,p[1]+B)
def disc(c,r,n=180): return ellipse_ruffle(at(c),r,r,0,0.0,1,n)
def cup(cv,p,c,R,saucer):
    """saucer, handle, rim and the tea, from above; a soft light on the tea"""
    cv.add([disc(c,saucer)],mix('#F4F8F2',p['ground'],0.25),mix(p['tep_edge'],p['ground'],0.35),0.9,alpha=0.75,glow=0.8,halo=0.2)
    cv.add([disc(c,saucer*0.62)],mix('#FFFFFF',p['ground'],0.35),mix(p['tep_edge'],p['ground'],0.5),0.6,alpha=0.35,halo=0.0)
    a=np.radians(-28); h0=(c[0]+np.cos(a)*R*0.95,c[1]+np.sin(a)*R*0.95); h1=(c[0]+np.cos(a)*(R+9),c[1]+np.sin(a)*(R+9))
    cv.add([draw.ribbon(draw.cr([at(h0),at(((h0[0]+h1[0])/2+1.5,(h0[1]+h1[1])/2-1)),at(h1)],16),lambda t:1.6+0.6*np.sin(np.pi*t))],'#FCFAF3',mix(p['tep_edge'],'#FFFFFF',0.4),0.4,halo=0.1)
    cv.add([disc(c,R)],'#FDFBF5',mix(p['tep_edge'],'#FFFFFF',0.3),0.35,glow=1.3,halo=0.25)
    cv.add([disc(c,R*0.86)],TEA['core'],TEA['edge'],0.45,centre=at((c[0]-R*0.15,c[1]-R*0.2)),R=R*1.1,glow=0.9,halo=0.0)
    hl=draw.ribbon(draw.cr([at((c[0]-R*0.72,c[1]+R*0.1)),at((c[0]-R*0.55,c[1]-R*0.45)),at((c[0]-R*0.15,c[1]-R*0.7))],20),lambda t:R*0.05*np.sin(np.pi*t)**0.7+0.05)
    cv.add([hl],'#FFF6E2',TEA['core'],0.45,alpha=0.55,halo=0.0)
def loose(cv,p,pts,rng):
    """a few loose dried tea leaves, small and curled"""
    polys=[leaf(at(q),rng.uniform(0,360),rng.uniform(3.2,5.2),rng.uniform(0.9,1.4),rng.uniform(-0.6,0.6)) for q in pts]
    cv.add(polys,'#5A3A22','#2A1A10',0.25,glow=0.9,halo=0.05)
def finish(cv,p,name,W,H,glowc,glowr):
    img=cv.render(p['ground'],grain=0,raw=True)
    yy,xx=np.mgrid[0:img.shape[0],0:img.shape[1]].astype(np.float32)/draw.K
    g=np.clip(1-np.hypot(xx-glowc[0]-B,yy-glowc[1]-B)/glowr,0,1)**1.6
    img=img*(1+0.10*g[...,None])                                  # a little light pooling round the cup
    img+=np.random.default_rng(21).normal(0,1,img.shape[:2]).astype(np.float32)[...,None]*8
    from PIL import Image
    Image.fromarray(img.clip(0,255).astype(np.uint8)).save(O+name)
def long_front(k='teal'):        # panel 176 x 85: data top left, name along the foot, logo and lion bottom right
    p=PAL[k]; cv=Canvas(182,91); rng=np.random.default_rng(3); c=(142,25)
    cv.add([leaf(at((182,-6)),148,58,11,0.3)],mix(p['leaf_core'],p['ground'],0.45),p['leaf_edge'],2.4,alpha=0.8)
    cup(cv,p,c,26,38)
    tea_sprig(cv,p,at((112,46)),-128,1.35,0.85)
    pods_=[(at((132,86)),-28,70,2.9,0.14,1),(at((140,92)),-36,64,2.5,0.1,-1)]
    cv.add([pod(*q) for q in pods_],p['pod_core'],p['pod_edge'],0.55,glow=0.9)
    sheen(cv,[pod(*q,spine=True)[3:-6]+np.array([0,-0.25*q[3]]) for q in pods_],0.8,mix(p['pod_core'],'#FFFFFF',0.35),p['pod_core'],0.5,0.55)
    # loose(cv,p,[(108,58),(114,64),(121,57),(176,58),(170,66),(103,50)],rng)
    flower(cv,at((140,24)),55,1.45,p,blurs=(0.4,0.34,0.65))
    finish(cv,p,f'long-{k}.png',182,91,c,60)
def cube_front(k='teal'):        # panel 88 x 85: name high left, lion top right, logo bottom left
    p=PAL[k]; cv=Canvas(94,91); rng=np.random.default_rng(4); c=(66,61)
    cv.add([leaf(at((96,18)),150,40,8,0.3)],mix(p['leaf_core'],p['ground'],0.45),p['leaf_edge'],2.2,alpha=0.75)
    cup(cv,p,c,19,28)
    tea_sprig(cv,p,at((78,44)),-78,1.0,0.8)
    pods_=[(at((36,92)),-18,66,2.4,0.12,1)]
    cv.add([pod(*q) for q in pods_],p['pod_core'],p['pod_edge'],0.55,glow=0.9)
    sheen(cv,[pod(*q,spine=True)[3:-6]+np.array([0,-0.25*q[3]]) for q in pods_],0.7,mix(p['pod_core'],'#FFFFFF',0.35),p['pod_core'],0.5,0.55)
    # loose(cv,p,[(44,74),(50,81),(40,80),(87,38)],rng)
    flower(cv,at((65,60)),55,1.05,p,blurs=(0.38,0.32,0.6))
    finish(cv,p,f'cube-{k}.png',94,91,c,45)
if __name__=='__main__':
    long_front(); cube_front(); print('ok')
