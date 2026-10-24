# The 12-bag front as a blot test: tea-gold and celadon, painting soaked into aged paper.
import sys
sys.path.insert(0,'/home/user/PersonalEventPlanner305App/vanilla-shop/studies/extract/split')
sys.path.insert(0,'/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/teaart')
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import draw
from draw import leaf
from comp import flower, mix
from split2 import WC, flush, pod_pair, echo
from blot import soak_in
K=draw.K; B=3; PAPER=np.array([0xF4,0xEB,0xD6],np.float32)
base=dict(tep_core='#FFFDF6',lip_core='#FFFEF8',throat_core='#F3C75E',throat_edge='#D69B3A',pod_core='#4A2A16',pod_edge='#26150B',tbud_core='#F2F6E2')
P={'tea-gold':(dict(base,ground='#D9B784',tep_edge='#EFDDBE',lip_edge='#F6EBD6',leaf_core='#A9B67E',leaf_edge='#5F6E3A',tea_core='#9DB870',tea_edge='#577433',tbud_edge='#BCCB92',tstem='#93A866'),'#9A6A2C','#4F5E2C'),
   'celadon':(dict(base,ground='#A9C6B4',tep_edge='#D3E4D6',lip_edge='#E6EFE4',leaf_core='#8DB39A',leaf_edge='#4E7A60',tea_core='#9CC48E',tea_edge='#4E7F4A',tbud_edge='#A9C99A',tstem='#7FA97A'),'#5E8A74','#2F5A44')}
tiles=[]
for k,(p,tide,ink) in P.items():
    cv=WC(94,91)
    cv.add([leaf((96,40),200,46,10,0.3)],mix(p['leaf_core'],p['ground'],0.5),p['leaf_edge'],2.4,alpha=0.7)
    echo(cv,p,(86,30),20,1.0)
    pod_pair(cv,p,(30,98),-18,90,2.4)
    flush(cv,p,(42,96),-74,1.05,blur=0.85)
    flush(cv,p,(92,96),-104,1.0,blur=1.0,alpha=0.85)
    flower(cv,(64,62),50,1.75,p,blurs=(0.3,0.26,0.5))
    art=cv.render(p['ground'],grain=0,raw=True)
    blobs=[((B+70)*K,(B+66)*K,40*K,34*K),((B+92)*K,(B+40)*K,16*K,22*K),((B+36)*K,(B+84)*K,18*K,10*K),
           ((B+30)*K,(B+56)*K,2.2*K,2.0*K),((B+44)*K,(B+45)*K,1.3*K,1.2*K)]          # main soak, the spread, two drops
    out=soak_in(art,PAPER,blobs,tide,seed=3)
    im=Image.fromarray(out.clip(0,255).astype(np.uint8)); dr=ImageDraw.Draw(im)
    f1=ImageFont.truetype('/home/user/PersonalEventPlanner305App/vanilla-shop/fonts/instrument-serif-italic.ttf',int(16.5*K))
    f2=ImageFont.truetype('/home/user/PersonalEventPlanner305App/vanilla-shop/fonts/archivo-expanded-regular.ttf',int(2.2*K))
    dr.text((10*K,12*K),'AUTHENTIC CEYLON',font=f2,fill=(80,70,50))
    dr.text((10*K,20*K),'Vanilla',font=f1,fill=(130,86,26)); dr.text((10*K,33*K),'Tea',font=f1,fill=ink)
    dr.text((4*K,86*K),k.upper(),font=f2,fill=(60,60,60))
    tiles.append(im)
c=Image.new('RGB',(sum(t.width for t in tiles)+20,tiles[0].height),'#888'); x=0
for t in tiles: c.paste(t,(x,0)); x+=t.width+20
c.save('blottest-full.jpg',quality=90); c.thumbnail((1700,900)); c.save('blottest.jpg',quality=85); print('ok')
