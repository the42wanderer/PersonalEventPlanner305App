# 2x2 board: front + How to brew, flat, all at one size; names outside the artwork
import sys, glob
from PIL import Image, ImageDraw, ImageFont
P='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/boxprev/'
V=[('1  Current Emerald','control, unchanged','estateemeraldside'),('2  Emerald & Apricot','rich green fields, warm sunset light','estateapricotside'),
   ('3  Jade & Citron','cooler, vivid, luminous yellow-green','estatecitronside'),('4  Forest & Ochre','earthy, warm, golden landscape','estateochreside')]
F=[p for p in glob.glob('/usr/share/fonts/**/*.ttf',recursive=True)]
big=ImageFont.truetype([p for p in F if p.endswith('DejaVuSans-Bold.ttf')][0],34); sm=ImageFont.truetype([p for p in F if p.endswith('DejaVuSans.ttf')][0],24)
H=640; tiles=[]
for name,sub,th in V:
    a=Image.open(P+th+'/3d-front.png').convert('RGB'); b=Image.open(P+th+'/3d-sideA.png').convert('RGB')
    a=a.resize((round(a.width*H/a.height),H),Image.LANCZOS); b=b.resize((round(b.width*H/b.height),H),Image.LANCZOS)
    t=Image.new('RGB',(a.width+b.width,H)); t.paste(a,(0,0)); t.paste(b,(a.width,0)); tiles.append((name,sub,t))
tw=max(t.width for *_,t in tiles); g=60; head=90
W=2*tw+3*g; Ht=2*(H+head)+3*g-20
bd=Image.new('RGB',(W,Ht),(234,229,220)); d=ImageDraw.Draw(bd)
for i,(name,sub,t) in enumerate(tiles):
    x=g+(i%2)*(tw+g); y=g-20+(i//2)*(H+head+g)
    d.text((x,y),name,fill=(36,30,26),font=big); d.text((x+2,y+46),sub,fill=(110,100,90),font=sm)
    bd.paste(t,(x,y+head))
bd.save(P+'board4.jpg',quality=93); bd.resize((W//6,Ht//6),Image.LANCZOS).save(P+'board4-thumb.png'); print(bd.size)
