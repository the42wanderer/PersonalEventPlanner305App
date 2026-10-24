# The 100 g kraft stand-up pouch drawn flat under even, neutral light (no photo shadows), with the label at its
# measured place: pouch 100 x 170 mm, label 70 x 110 mm, label top 40 mm down.
import sys
sys.path.insert(0,'/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/teaart')
import numpy as np, cv2
from PIL import Image, ImageDraw
from blot2 import fbm
O=sys.argv[1]; k=8; W,H=100,170; w,h=W*k,H*k
rng=np.random.default_rng(2)
kraft=np.array([0xA9,0x84,0x5B],np.float32)
fib=cv2.GaussianBlur(rng.normal(0,1,(h,w)).astype(np.float32),(0,0),sigmaX=2.2,sigmaY=0.5)   # paper fibres
img=kraft*(1+0.045*fbm(h,w,60,3)[...,None]+0.035*fib[...,None]+0.02*rng.normal(0,1,(h,w))[...,None])
yy,xx=np.mgrid[0:h,0:w].astype(np.float32)
pillow=1-0.06*((np.abs(xx-w/2)/(w/2))**4)-0.05*np.clip((yy-0.86*h)/(0.14*h),0,1)**2           # a filled pouch: the edges turn away a little
img*=pillow[...,None]
m=Image.new('L',(w,h),0); d=ImageDraw.Draw(m); d.rounded_rectangle((0,0,w-1,h-1),radius=3*k,fill=255)
for y in (10*k,):  # tear notches
    d.polygon([(0,y-6),(10,y),(0,y+6)],fill=0); d.polygon([(w,y-6),(w-10,y),(w,y+6)],fill=0)
mask=np.asarray(m).astype(np.float32)/255
for y0,y1,f in ((0,6*k,0.93),(22*k,22*k+5,0.85),(22*k+5,22*k+10,1.05)):   # top seal, zip track
    img[y0:y1]*=f
crimp=(np.mod(xx[:6*k],10)<5)*0.04; img[:6*k]*=(1-crimp)[...,None]
gus=(yy>h-18*k)&(np.abs(xx-w/2)<w*0.5)&((yy-(h-18*k))>(((xx-w/2)/(w/2))**2)*12*k)          # the bottom gusset seam
img[gus]*=0.97
L=Image.open(O+'pouch-vanilla.png').convert('RGBA').resize((70*k,110*k),Image.LANCZOS); la=np.asarray(L).astype(np.float32)
x0,y0=15*k,40*k; a=la[...,3:]/255; img[y0:y0+110*k,x0:x0+70*k]=img[y0:y0+110*k,x0:x0+70*k]*(1-a)+la[...,:3]*pillow[y0:y0+110*k,x0:x0+70*k,None]*a
out=np.dstack([img.clip(0,255),mask*255]).astype(np.uint8)
Image.fromarray(out,'RGBA').save(O+'pouch-neutral.png'); print('ok')
