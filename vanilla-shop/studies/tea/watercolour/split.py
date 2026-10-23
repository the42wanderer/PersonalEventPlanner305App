# Vanilla tea, the extract labels' Split translated to a box: cream on the left of the front for the brand and the
# name; a deep teal block on the right that wraps the corner onto the side, holding the round-one watercolour flower
# (crossing the fold), a Ceylon tea flush and pods, on plain teal with grain.
import sys
sys.path.insert(0,'/home/user/PersonalEventPlanner305App/vanilla-shop/studies/extract/split')
sys.path.insert(0,'/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/teaart')
import numpy as np
from PIL import Image
import draw
from draw import Canvas, leaf
from comp import flower, mix
from teaflower import PAL, flush, pods
import cream
O='/home/user/PersonalEventPlanner305App/vanilla-shop/studies/tea/watercolour/split/'
K=draw.K; B=3; p=PAL['teal']; PAPER=np.array([0xF6,0xEE,0xDC],np.float32)
def tone_print(Wmm,Hmm):
    """the engraving, tone-on-tone: a shade lighter than the teal, very quiet"""
    cream.PAPER=np.array([0,0,0],np.float32); cream.LINE=np.array([255,255,255],np.float32); cream.FADE=1.0; cream.SPX,cream.SPY=0.9,0.95
    m=cream.pattern(Wmm,Hmm,h=78,seed=4)[...,0]/255      # 0..1 line mask
    return np.clip(m,0,1)
def build(box,FW,split,SW,art):
    """FW, SW: front and right-side panel widths (mm); split: where the teal starts on the front"""
    bw=FW-split; W=B+bw+SW+B; H=85+2*B
    cv=Canvas(int(round(W)),H); art(cv,bw)
    img=cv.render(p['ground'],grain=0,raw=True)
    img+=np.random.default_rng(5).normal(0,6,img.shape[:2])[...,None]
    fw=int((FW+2*B)*K); front=np.ones((H*K,fw,3),np.float32)*PAPER
    front+=np.random.default_rng(6).normal(0,3.5,front.shape[:2])[...,None]
    x0=int((split+B)*K); bwp=int(bw*K)
    front[:,x0:x0+bwp]=img[:,B*K:B*K+bwp]
    front[:,x0+bwp:]=img[:,B*K+bwp:B*K+bwp+(fw-x0-bwp)]                            # the bleed past the fold
    side=img[:,B*K+bwp:]
    Image.fromarray(front.clip(0,255).astype(np.uint8)).save(O+f'{box}-split-front.png')
    Image.fromarray(side.clip(0,255).astype(np.uint8)).save(O+f'{box}-split-side.png')
# coordinates below: x from the start of the teal block (the fold sits at x = bw), y from the panel top; the canvas
# helpers add the 3 mm bleed themselves
def long_art(cv,bw):      # block 84 on the front, the fold at x=84, side 85; brewing text on the side at x 8-56
    cv.add([leaf((bw+80,8),200,60,12,0.3)],mix(p['leaf_core'],p['ground'],0.5),p['leaf_edge'],2.6,alpha=0.8)
    flush(cv,p,(10,-6),70,1.4,blur=1.5,alpha=0.75)
    pods(cv,p,[((-4,92),-16,120,3.4,0.12,1),((8,98),-24,110,3.0,0.1,-1)])
    flush(cv,p,(bw+70,92),-112,1.8,blur=0.7)
    flush(cv,p,(6,92),-70,1.5,blur=0.75)
    flower(cv,(bw-24+3,36+3),40,2.75,p,blurs=(0.45,0.38,0.7))
def cube_art(cv,bw):      # block 30 on the front, side 85 with the brewing text at x 40-77
    cv.add([leaf((bw+80,70),200,50,10,0.3)],mix(p['leaf_core'],p['ground'],0.5),p['leaf_edge'],2.6,alpha=0.8)
    pods(cv,p,[((-4,94),-14,90,3.0,0.1,1)])
    flush(cv,p,(4,92),-72,1.4,blur=0.75)
    flush(cv,p,(bw+30,94),-100,1.2,blur=1.3,alpha=0.8)
    flower(cv,(bw+3+3,36+3),70,2.3,p,blurs=(0.42,0.36,0.65))
build('long',175.9,92,85.1,long_art)
build('cube',87.6,58,84.6,cube_art)
print('ok')
