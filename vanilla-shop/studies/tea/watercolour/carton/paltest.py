# Palette test: lighter tea grounds, closer to the cream's value, washed out over a wide distance (no edge).
import sys
sys.path.insert(0,'/home/user/PersonalEventPlanner305App/vanilla-shop/studies/extract/split')
sys.path.insert(0,'/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/teaart')
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import draw
from draw import leaf
from comp import flower, mix
from split2 import WC, flush, pod_pair, echo
K=draw.K; B=3; PAPER=np.array([0xF6,0xEE,0xDC],np.float32)
base=dict(tep_core='#FFFDF6',lip_core='#FFFEF8',throat_core='#F3C75E',throat_edge='#D69B3A',pod_core='#4A2A16',pod_edge='#26150B',tbud_core='#F2F6E2')
P={'celadon':dict(base,ground='#A9C6B4',tep_edge='#D3E4D6',lip_edge='#E6EFE4',leaf_core='#8DB39A',leaf_edge='#4E7A60',tea_core='#9CC48E',tea_edge='#4E7F4A',tbud_edge='#A9C99A',tstem='#7FA97A'),
   'matcha':dict(base,ground='#C3CC92',tep_edge='#E4E7C4',lip_edge='#F0F0D8',leaf_core='#A3B26A',leaf_edge='#5E6E2E',tea_core='#9DB860',tea_edge='#55712A',tbud_edge='#B9C98A',tstem='#8EA35A'),
   'tea-gold':dict(base,ground='#DDBF8E',tep_edge='#EFDDBE',lip_edge='#F6EBD6',leaf_core='#A9B67E',leaf_edge='#5F6E3A',tea_core='#9DB870',tea_edge='#577433',tbud_edge='#BCCB92',tstem='#93A866')}
def smooth(a,b,x): t=np.clip((x-a)/(b-a),0,1); return t*t*(3-2*t)
tiles=[]
for k,p in P.items():
    cv=WC(94,91)
    cv.add([leaf((96,40),200,46,10,0.3)],mix(p['leaf_core'],p['ground'],0.5),p['leaf_edge'],2.4,alpha=0.7)
    echo(cv,p,(88,22),20,1.0)
    pod_pair(cv,p,(30,98),-18,90,2.4)
    flush(cv,p,(42,96),-74,1.05,blur=0.85)
    flush(cv,p,(92,96),-104,1.0,blur=1.0,alpha=0.85)
    flower(cv,(64,62),50,1.75,p,blurs=(0.3,0.26,0.5))
    img=cv.render(p['ground'],grain=0,raw=True)
    h,w=img.shape[:2]; yy,xx=np.mgrid[0:h,0:w].astype(np.float32)/K-B
    d=np.hypot((xx-80)/70,(yy-82)/62)
    M=1-smooth(0.35,1.05,d)                                   # a long, soft fade: no edge to find
    out=PAPER*(1-M[...,None])+img*M[...,None]+np.random.default_rng(4).normal(0,3.5,(h,w))[...,None]
    im=Image.fromarray(out.clip(0,255).astype(np.uint8)); dr=ImageDraw.Draw(im)
    f1=ImageFont.truetype('/home/user/PersonalEventPlanner305App/vanilla-shop/fonts/instrument-serif-italic.ttf',int(16.5*K))
    f2=ImageFont.truetype('/home/user/PersonalEventPlanner305App/vanilla-shop/fonts/archivo-expanded-regular.ttf',int(2.2*K))
    dr.text((10*K,12*K),'AUTHENTIC CEYLON',font=f2,fill=(80,70,50))
    dr.text((10*K,20*K),'Vanilla',font=f1,fill=(140,95,30)); dr.text((10*K,33*K),'Tea',font=f1,fill=tuple(int(v) for v in np.array([int(p['leaf_edge'][i:i+2],16) for i in (1,3,5)])*0.75))
    dr.text((4*K,85*K),k.upper(),font=f2,fill=(60,60,60))
    tiles.append(im)
c=Image.new('RGB',(sum(t.width for t in tiles)+40,tiles[0].height),'#888'); x=0
for t in tiles: c.paste(t,(x,0)); x+=t.width+20
c.thumbnail((1700,700)); c.save('paltest.jpg',quality=85); print('ok')
