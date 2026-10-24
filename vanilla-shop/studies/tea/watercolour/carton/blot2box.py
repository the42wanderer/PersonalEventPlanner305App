# Vanilla Tea cartons (25 and 12 bags): the painting, crisp, lifted onto layered watercolour glazes that fade the way
# watercolour does; brand tea palette (peach #E8B9A0, deep green #1F4A2C, tea brown #6A3B1E, cream). The wash wraps
# the corner onto the right side; the back, left side and lid are the same paper, the lid with a faint tea ring.
import sys
sys.path.insert(0,'/home/user/PersonalEventPlanner305App/vanilla-shop/studies/extract/split')
sys.path.insert(0,'/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/teaart')
import numpy as np, cv2
from PIL import Image
import draw
from comp import flower
from split2 import WC, flush, pod_pair
from blot2 import paint_wash, lift, fbm
O='/home/user/PersonalEventPlanner305App/vanilla-shop/studies/tea/watercolour/carton/wash/'
K=draw.K; B=3; PAPER=np.array([0xF6,0xEE,0xDE],np.float32)
p=dict(tep_core='#FFFDF8',lip_core='#FFFEF9',throat_core='#F3C75E',throat_edge='#D69B3A',pod_core='#5A3420',pod_edge='#2E1A0E',tbud_core='#F3F6E6',sheen=0.15,
       ground='#E2A88C',tep_edge='#F4DCCB',lip_edge='#FAEDE2',leaf_core='#8FA98A',leaf_edge='#3E5E44',tea_core='#8DAE84',tea_edge='#3F6644',tbud_edge='#B5CBA6',tstem='#82A47C')
def build(name,FW,SW,art,layers):
    W=int(round(B+FW+SW+B)); cv=WC(W,85+2*B); cv.crisp=True; art(cv)
    col,al=lift(cv); h,w=al.shape
    wash=paint_wash(h,w,PAPER,layers,seed=3)
    out=wash*(1-al[...,None])+col*al[...,None]+np.random.default_rng(4).normal(0,2.6,(h,w))[...,None]
    fx=int((FW+B)*K)
    Image.fromarray(out[:,:int((FW+2*B)*K)].clip(0,255).astype(np.uint8)).save(O+f'{name}-front.png')
    Image.fromarray(out[:,fx:].clip(0,255).astype(np.uint8)).save(O+f'{name}-side.png')
C=lambda x,y,rx,ry:((B+x)*K,(B+y)*K,rx*K,ry*K)          # x, y in front mm (the side continues past FW)
def long_box():
    FW=175.9; f=FW+3
    def art(cv):
        pod_pair(cv,p,(f-80,96),-14,130,2.9)
        flush(cv,p,(f+50,94),-106,1.5,blur=0.2)
        flush(cv,p,(f-66,94),-78,1.25,blur=0.2)
        flush(cv,p,(f+26,60),-96,0.9,blur=0.2)
        flower(cv,(f-36,56),40,2.35,p,blurs=(0.1,0.08,0.22))
    layers=[([C(140,66,70,42),C(196,58,44,40),C(98,84,30,12)],1.0,'#F3DCCB',0.55,0.4),
            ([C(140,64,54,34),C(196,60,32,30)],1.0,'#EBC0A6',0.55,0.0),
            ([C(142,62,36,24),C(198,66,18,18)],1.0,'#E2A88C',0.6,-0.3),
            ([C(170,84,22,14),C(214,80,16,14)],1.0,'#A9C2A8',0.45,0.5),
            ([C(78,62,2.4,2.1),C(88,54,1.3,1.2)],1.0,'#E2A88C',0.6,-0.6)]
    build('long',FW,85.1,art,layers)
def cube_box():
    FW=87.6; f=FW+3
    def art(cv):
        pod_pair(cv,p,(f-62,98),-18,96,2.5)
        flush(cv,p,(f+24,96),-100,1.1,blur=0.2)
        flush(cv,p,(f-48,96),-74,1.0,blur=0.2)
        flower(cv,(f-22,64),50,1.7,p,blurs=(0.1,0.08,0.22))
    layers=[([C(70,70,50,40),C(116,62,34,34),C(32,88,24,10)],1.0,'#F3DCCB',0.55,0.4),
            ([C(68,68,38,30),C(116,64,24,24)],1.0,'#EBC0A6',0.55,0.0),
            ([C(68,66,26,22),C(118,70,14,14)],1.0,'#E2A88C',0.6,-0.3),
            ([C(90,84,18,12),C(128,82,12,10)],1.0,'#A9C2A8',0.45,0.5),
            ([C(30,60,2.0,1.8),C(40,52,1.2,1.1)],1.0,'#E2A88C',0.6,-0.6)]
    build('cube',FW,84.6,art,layers)
def papers():
    k=12; h=w=int(260*k)
    import blot2; blot2.K=k
    pap=np.ones((h,w,3),np.float32)*PAPER*(1+0.012*fbm(h,w,int(40*k),21)[...,None])+np.random.default_rng(21).normal(0,2.6,(h,w))[...,None]
    Image.fromarray(pap.clip(0,255).astype(np.uint8)).save(O+'paper.jpg',quality=94)
    yy,xx=np.mgrid[0:h,0:w].astype(np.float32)/k; r=np.hypot(xx-130,yy-130); n=fbm(h,w,int(20*k),5)
    ring=np.exp(-((r-37+2.5*n)/0.9)**2)*(0.5+0.5*np.clip(np.sin(np.arctan2(yy-130,xx-130)+1.3)+0.6,0,1))
    ring=cv2.GaussianBlur(ring,(0,0),0.4*k)*0.12
    tc=np.array([0xC8,0x8E,0x70],np.float32); lid=pap*(1-ring[...,None])+tc*ring[...,None]
    Image.fromarray(lid.clip(0,255).astype(np.uint8)).save(O+'paper-lid.jpg',quality=94); blot2.K=20
if __name__=='__main__':
    long_box(); cube_box(); papers(); print('ok')
