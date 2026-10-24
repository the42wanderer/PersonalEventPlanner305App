import sys
sys.path.insert(0,'/home/user/PersonalEventPlanner305App/vanilla-shop/studies/extract/split')
sys.path.insert(0,'/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/teaart')
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
import draw
from draw import leaf
from comp import flower, mix
from split2 import WC, flush, pod_pair, echo
from blot2 import paint_wash, lift
K=draw.K; B=3; PAPER=np.array([0xF6,0xEE,0xDE],np.float32)
# brand tea palette: deep green #1F4A2C, cream #F6E7C2, peach #E8B9A0, tea brown #6A3B1E
PEACH=dict(tep_core='#FFFDF8',lip_core='#FFFEF9',throat_core='#F3C75E',throat_edge='#D69B3A',pod_core='#5A3420',pod_edge='#2E1A0E',tbud_core='#F3F6E6',sheen=0.15,
           ground='#E2A88C',tep_edge='#F4DCCB',lip_edge='#FAEDE2',leaf_core='#8FA98A',leaf_edge='#3E5E44',tea_core='#8DAE84',tea_edge='#3F6644',tbud_edge='#B5CBA6',tstem='#82A47C')
p=PEACH
cv=WC(94,91); cv.crisp=True
pod_pair(cv,p,(30,98),-18,90,2.4)
flush(cv,p,(42,96),-74,1.05,blur=0.25)
flush(cv,p,(92,96),-104,1.0,blur=0.3)
flower(cv,(64,62),50,1.75,p,blurs=(0.1,0.08,0.22))
col,al=lift(cv); h,w=al.shape
C=lambda x,y,rx,ry:((B+x)*K,(B+y)*K,rx*K,ry*K)
layers=[([C(72,70,52,44),C(98,36,20,26),C(30,88,26,12)],1.0,'#F3DCCB',0.55,0.4),      # outer, palest, mostly wet
        ([C(70,68,40,34),C(92,44,14,18)],1.0,'#EBC0A6',0.55,0.0),                     # middle peach
        ([C(68,66,28,24)],1.0,'#E2A88C',0.6,-0.3),                                     # inner, strongest, crisper
        ([C(90,82,18,14)],1.0,'#A9C2A8',0.45,0.5),                                    # green bleeding in, wet-in-wet
        ([C(26,60,2.2,2.0),C(36,51,1.3,1.2)],1.0,'#E2A88C',0.6,-0.6)]                  # two drops
wash=paint_wash(h,w,PAPER,layers,seed=3)
out=wash*(1-al[...,None])+col*al[...,None]+np.random.default_rng(4).normal(0,2.8,(h,w))[...,None]
im=Image.fromarray(out.clip(0,255).astype(np.uint8)); dr=ImageDraw.Draw(im)
f1=ImageFont.truetype('/home/user/PersonalEventPlanner305App/vanilla-shop/fonts/instrument-serif-italic.ttf',int(16.5*K))
f2=ImageFont.truetype('/home/user/PersonalEventPlanner305App/vanilla-shop/fonts/archivo-expanded-regular.ttf',int(2.2*K))
dr.text((10*K,12*K),'AUTHENTIC CEYLON',font=f2,fill=(60,70,55))
dr.text((10*K,20*K),'Vanilla',font=f1,fill=(130,86,26)); dr.text((10*K,33*K),'Tea',font=f1,fill=(0x1F,0x4A,0x2C))
im.save('b2test-full.png'); im.crop((int(30*K),int(30*K),int(94*K),int(91*K))).save('b2test-crop.jpg',quality=94); im.thumbnail((900,900)); im.save('b2test.jpg',quality=92); print('ok')
