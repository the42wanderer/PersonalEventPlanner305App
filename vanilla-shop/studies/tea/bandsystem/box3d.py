# 3D views of the 12-bag carton from the flat print preview: faces cropped at the dieline's panel rectangles
import sys
from PIL import Image
S='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/'
pl=sys.argv[1]; LONG=len(sys.argv)>2 and sys.argv[2]=='long'; d=S+f'boxprev/{pl}/'; im=Image.open(d+'flat.png').convert('RGB')
if LONG:   # the 25-bag carton: the lid hinges at the back, so its face turns half round on the box
    k=im.width/1642.42
    P={'front':(850.5,382.8,1349.2,622.9),'sideA':(1349.2,382.8,1590.5,622.9),'back':(114.9,382.8,611,622.9),
       'sideB':(611,382.8,850.5,622.9),'top':(114.9,142.3,611,382.8)}
else:
    k=im.width/1194.94      # px per pt
    P={'front':(145.46,390.86,393.94,631.07),'sideA':(393.94,390.86,633.68,631.07),'back':(633.68,390.86,881.95,631.07),
       'sideB':(881.95,390.86,1122.45,631.07),'top':(145.50,149.85,393.53,390.72)}
for f,(x0,y0,x1,y1) in P.items():
    c=im.crop((round(x0*k)+4,round(y0*k)+4,round(x1*k)-4,round(y1*k)-4))
    (c.rotate(180) if LONG and f=='top' else c).save(d+f'3d-{f}.png')
s=4.6 if LONG else 6.4; W,H,D=(175.93,84.70,85.13) if LONG else (87.65,84.74,84.57); W,H,D=W*s,H*s,D*s
def face(f,w,h,tr): return f'<div style="position:absolute;left:{-w/2}px;top:{-h}px;width:{w}px;height:{h}px;background:url(file://{d}3d-{f}.png) center/100% 100%;transform:{tr}"></div>'
def cube(x,y,ry):
    fs=[face('front',W,H,f'translateZ({D/2}px)'),face('sideA',D,H,f'rotateY(90deg) translateZ({W/2}px)'),face('back',W,H,f'rotateY(180deg) translateZ({D/2}px)'),
        face('sideB',D,H,f'rotateY(-90deg) translateZ({W/2}px)'),
        f'<div style="position:absolute;left:{-W/2}px;top:{-D/2}px;width:{W}px;height:{D}px;background:url(file://{d}3d-top.png) center/100% 100%;transform:translateY({-H}px) rotateX(90deg)"></div>']
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;transform-style:preserve-3d;transform:rotateX(-18deg) rotateY({ry}deg)">'
            f'<div style="position:absolute;transform-style:preserve-3d">{"".join(fs)}</div></div>')
html=('<html><head><meta charset="utf-8"><style>html,body{margin:0}</style></head><body><div style="position:relative;width:1900px;height:1050px;background:#E6E0D5;overflow:hidden;perspective:5200px">'
      '<div style="position:absolute;left:120px;right:120px;top:830px;height:200px;background:radial-gradient(closest-side,rgba(40,25,10,.22),transparent)"></div>'
      +(cube(560,820,-24)+cube(1380,820,156) if LONG else cube(520,850,-30)+cube(1400,850,150))+'</div></body></html>')
open(d+'3d.html','w').write(html); print(d+'3d')
