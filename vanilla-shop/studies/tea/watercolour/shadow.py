# Vanilla tea, round five: no band. Cream paper, the engraving printed faintly (quiet behind the type, fuller at the
# right and foot), and the soft shadow of our vanilla vine and a tea flush falling across the box, as if afternoon
# light came through the plant: sharp where it is near, soft where it is far. Front-panel mm, 3 mm bleed.
import sys
sys.path.insert(0,'/home/user/PersonalEventPlanner305App/vanilla-shop/studies/extract/split')
sys.path.insert(0,'/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/teaart')
import numpy as np, cv2
from PIL import Image, ImageDraw
import draw
from cream import pattern, PAPER
O='/home/user/PersonalEventPlanner305App/vanilla-shop/studies/tea/watercolour/shadow/'
SP='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/bw/spray-test.png'
K=draw.K; B=3; SHADE=np.array([0x2A,0x4A,0x34],np.float32)
src=np.asarray(Image.open(SP).convert('L'))
sil=((255-src)>50).astype(np.uint8)*255
sil=cv2.morphologyEx(sil,cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(31,31)))     # hatching closed into solid shapes
sil=cv2.morphologyEx(sil,cv2.MORPH_OPEN,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)))
SIL=Image.fromarray(sil)
def tea_sil(d,base,ang,s,k):
    """a tea flush as a filled silhouette: stem, two leaves and a bud"""
    a=np.radians(ang); P=lambda t,o=0:(base[0]+np.cos(a)*t*s-np.sin(a)*o*s, base[1]+np.sin(a)*t*s+np.cos(a)*o*s)
    for poly in [draw.stem([P(0),P(9,0.8),P(17,-0.6),P(26)],0.7*s),draw.leaf(P(9,0.8),ang-62,19*s,5.6*s,-0.3),draw.leaf(P(17,-0.6),ang+52,15*s,4.6*s,0.28),draw.bud(P(26),ang-6,9*s,2.0*s,0.12)]:
        d.polygon([tuple(v) for v in (np.asarray(poly)+B)*k],fill=255)
def front(name,W,H,spray,flushes,quiet,glow):
    w,h=int(W*K),int(H*K)
    yy,xx=np.mgrid[0:h,0:w].astype(np.float32)/K-B
    pat=pattern(W,H); paper=np.ones_like(pat)*PAPER
    q=np.ones((h,w),np.float32)
    for (x0,y0,x1,y1) in quiet:                                   # quiet the print behind the type
        dx=np.maximum(np.maximum(x0-xx,xx-x1),0); dy=np.maximum(np.maximum(y0-yy,yy-y1),0)
        q=np.minimum(q,np.clip(np.hypot(dx,dy)/10,0,1))
    q=q*np.clip(0.35+0.65*((xx/W)*0.6+(yy/H)*0.4),0,1)             # fuller towards the right and the foot
    img=paper+(pat-paper)*q[...,None]
    # warm light pooling where the sun comes in
    g=np.clip(1-np.hypot(xx-glow[0],yy-glow[1])/glow[2],0,1)**1.5; img=img*(1+0.035*g[...,None])
    # the shadow: the vine (near, crisper) and the flushes (further, softer)
    M=Image.new('L',(w,h),0)
    (x,y,hm,rot,flip)=spray; s=SIL.transpose(Image.FLIP_LEFT_RIGHT) if flip else SIL
    s=s.resize((int(hm*2400/3400*K),int(hm*K)),Image.LANCZOS).rotate(rot,expand=True)
    M.paste(s,(int((x+B)*K-s.size[0]/2),int((y+B)*K-s.size[1]/2)),s)
    near=np.asarray(M).astype(np.float32)/255
    F=Image.new('L',(w,h),0); d=ImageDraw.Draw(F)
    for f in flushes: tea_sil(d,*f,K)
    far=np.asarray(F).astype(np.float32)/255
    # blur grows away from the top right (where the plant is closest to the box)
    t=np.clip(np.hypot(xx-W,yy+10)/ (W*0.9),0,1)
    n1=cv2.GaussianBlur(near,(0,0),0.5*K); n2=cv2.GaussianBlur(near,(0,0),2.2*K)
    a=(n1*(1-t)+n2*t)*0.26+cv2.GaussianBlur(far,(0,0),3.0*K)*0.17
    img=img*(1-a[...,None])+SHADE*a[...,None]
    img+=np.random.default_rng(3).normal(0,3.5,(h,w,1))
    Image.fromarray(img.clip(0,255).astype(np.uint8)).save(O+name)
# long, panel 176 x 85: signature top left, name across the middle left, the shadow falling from the top right
front('long-cream.png',182,91,spray=(138,30,120,-38,True),flushes=[((170,-8),118,2.4),((120,-10),70,1.9),((176,70),-150,2.0)],
      quiet=[(6,4,120,24),(4,36,124,70),(130,6,172,20)],glow=(150,10,90))
front('cube-cream.png',94,91,spray=(66,30,100,-34,True),flushes=[((90,-8),112,1.7),((92,64),-150,1.6)],
      quiet=[(5,4,52,22),(4,36,62,72),(52,6,84,18)],glow=(80,6,60))
print('ok')
