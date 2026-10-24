# Six colour options for the Vanilla Tea carton, same watercolour and layout (12-bag front), to choose from.
import sys
sys.path.insert(0,'/home/user/PersonalEventPlanner305App/vanilla-shop/studies/extract/split')
sys.path.insert(0,'/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/teaart')
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import draw
from comp import flower, mix
from split2 import WC, flush, pod_pair
from blot2 import paint_wash, lift
K=draw.K; B=3; PAPER=np.array([0xF6,0xEE,0xDC],np.float32)
F='/home/user/PersonalEventPlanner305App/vanilla-shop/fonts/'
f1=ImageFont.truetype(F+'instrument-serif-italic.ttf',int(16.5*K)); f2=ImageFont.truetype(F+'archivo-expanded-regular.ttf',int(2.2*K)); f3=ImageFont.truetype(F+'archivo-expanded-regular.ttf',int(3.2*K))
def pal(ground,g1,g2,ink,leaf=('#8FB08A','#3E5E44'),tep='#E4EFE8'):
    return dict(tep_core='#FFFDF8',lip_core='#FFFEF9',throat_core='#F3C75E',throat_edge='#D69B3A',pod_core='#4A2A16',pod_edge='#26150B',tbud_core='#F3F6E6',
                ground=ground,tep_edge=tep,lip_edge='#F6F4EC',leaf_core=leaf[0],leaf_edge=leaf[1],tea_core=leaf[0],tea_edge=leaf[1],tbud_edge='#B5CBA6',tstem='#82A47C'),(g1,g2,ground),ink
OPTS=[('1  CEYLON GREEN',*pal('#2F5E3E','#D9E6D6','#9DBF9F','#1F4A2C')),          # brand tea deep green
      ('2  MIDNIGHT INDIGO',*pal('#2B3566','#DCDFEA','#9AA3C6','#1F2752',tep='#E2E5F2')),   # the Aura candle's blue
      ('3  CEYLON TEA RED',*pal('#8E3B2C','#F1DAD0','#D59A88','#6A2A1E',tep='#F6E2DA')),  # brewed black tea, extract red
      ('4  HONEY GOLD',*pal('#B98428','#F4E4C2','#E2BD72','#6A4A12',tep='#FBEFD8')),     # extract No. 02 gold
      ('5  SAGE',*pal('#6E8C6A','#E2EADB','#B4C8AC','#3E5A3C')),                           # soft, calm, tea leaf
      ('6  PLUM',*pal('#5E2C4A','#EADAE2','#B58CA4','#4A1E38',tep='#F2E4EC'))]           # a darker, gift-like option
C=lambda x,y,rx,ry:((B+x)*K,(B+y)*K,rx*K,ry*K)
tiles=[]
for name,p,(g1,g2,g3),ink in OPTS:
    cv=WC(94,91); cv.crisp=True; cv.cap=0.22
    pod_pair(cv,p,(26,98),-18,98,2.5); flush(cv,p,(40,96),-74,1.0); flush(cv,p,(94,98),-100,1.0)
    flower(cv,(68,62),50,1.8,p,blurs=(0.3,0.26,0.5))
    col,al=lift(cv); h,w=al.shape
    layers=[([C(68,68,50,40),C(30,88,24,10)],1.0,g1,0.7,0.4),([C(68,66,38,30)],1.0,g2,0.7,0.0),([C(68,64,27,22)],1.0,g3,0.85,-0.3),([C(30,60,2.0,1.8),C(40,52,1.2,1.1)],1.0,g2,0.8,-0.6)]
    out=paint_wash(h,w,PAPER,layers,seed=3)*(1-al[...,None])+col*al[...,None]
    im=Image.fromarray(out.clip(0,255).astype(np.uint8)); d=ImageDraw.Draw(im)
    d.text((10*K,12*K),'AUTHENTIC CEYLON',font=f2,fill=ink)
    d.text((10*K,20*K),'Vanilla',font=f1,fill=(130,86,26)); d.text((10*K,33*K),'Tea',font=f1,fill=ink)
    d.text((10*K,84*K),name,font=f3,fill=(40,40,40))
    im.thumbnail((560,560)); tiles.append(im)
w,h=tiles[0].size; c=Image.new('RGB',(w*3+40,h*2+20),'#9a958c')
for i,t in enumerate(tiles): c.paste(t,((i%3)*(w+20),(i//3)*(h+20)))
c.save('/home/user/PersonalEventPlanner305App/vanilla-shop/studies/tea/watercolour/carton/colour-options.jpg',quality=90); print('ok')
