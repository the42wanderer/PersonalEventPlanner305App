# three directions, one board: front + How to brew, flat, one size each; names outside the artwork
import glob
from PIL import Image, ImageDraw, ImageFont
P='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/boxprev/'
V=[('1  Emerald & Dusty Rose','emerald sky, a broad rose band, peach horizon','estaterose'),
   ('2  Celadon & Forest','a light landscape, pale celadon panel','estateceladon'),
   ('3  Chartreuse & Ink Green','bold yellow-green sky, ink-green fields','estatechartreuse')]
F=glob.glob('/usr/share/fonts/**/*.ttf',recursive=True)
big=ImageFont.truetype([p for p in F if p.endswith('DejaVuSans-Bold.ttf')][0],34); sm=ImageFont.truetype([p for p in F if p.endswith('DejaVuSans.ttf')][0],24)
H=600; tiles=[]
for name,sub,th in V:
    a=Image.open(P+th+'/3d-front.png').convert('RGB'); b=Image.open(P+th+'/3d-sideA.png').convert('RGB')
    a=a.resize((round(a.width*H/a.height),H),Image.LANCZOS); b=b.resize((round(b.width*H/b.height),H),Image.LANCZOS)
    t=Image.new('RGB',(a.width+b.width,H)); t.paste(a,(0,0)); t.paste(b,(a.width,0)); tiles.append((name,sub,t))
tw=max(t.width for *_,t in tiles); g=60; head=90
W=tw+2*g; Ht=3*(H+head)+4*g-40
bd=Image.new('RGB',(W,Ht),(234,229,220)); d=ImageDraw.Draw(bd)
for i,(name,sub,t) in enumerate(tiles):
    x=g; y=g-20+i*(H+head+g)
    d.text((x,y),name,fill=(36,30,26),font=big); d.text((x+2,y+46),sub,fill=(110,100,90),font=sm); bd.paste(t,(x,y+head))
bd.save(P+'board3.jpg',quality=93); bd.resize((W//7,Ht//7),Image.LANCZOS).save(P+'board3-thumb.png'); print(bd.size)
