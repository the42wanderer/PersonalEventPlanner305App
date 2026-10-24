# Tea cartons, composed for a box (the pouch stays as it is). Same painting, type and colours as the pouch.
#  A "wash": a mostly cream front; the painting sits low right in a soft teal wash that dissolves into the cream,
#     drying with a pigment edge, and runs round the corner onto the solid teal side.
#  B "window": the painting in a bounded window on the cream front, arched like the pouch label.
# Front-panel mm with 3 mm bleed; the fold is at x = FW.
import sys, math
sys.path.insert(0,'/home/user/PersonalEventPlanner305App/vanilla-shop/studies/extract/split')
sys.path.insert(0,'/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/teaart')
import numpy as np, cv2
from PIL import Image, ImageDraw
import draw
from draw import leaf
from comp import flower, mix
from split2 import WC, flush, pod_pair, echo, vine, quills, TEAL, CIN
O='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/teaart/ct/'
K=draw.K; B=3; PAPER=np.array([0xF6,0xEE,0xDC],np.float32)
def hx(c): return np.array([int(c[i:i+2],16) for i in (1,3,5)],np.float32)
def smooth(a,b,x): t=np.clip((x-a)/(b-a),0,1); return t*t*(3-2*t)
def paint(p,FW,SW,art):
    cv=WC(int(round(B+FW+SW+B)),85+2*B); art(cv); img=cv.render(p['ground'],grain=0,raw=True)
    return img+np.random.default_rng(5).normal(0,5,img.shape[:2])[...,None]
def paper(h,w,seed): return np.ones((h,w,3),np.float32)*PAPER+np.random.default_rng(seed).normal(0,3.2,(h,w))[...,None]
def wash_front(name,p,img,FW,cx,cy,rx,ry):
    H=85; h,w=img.shape[0],int((FW+2*B)*K)
    yy,xx=np.mgrid[0:h,0:w].astype(np.float32)/K-B
    rng=np.random.default_rng(9)
    n=cv2.resize(rng.normal(0,1,(h//60+2,w//60+2)).astype(np.float32),(w,h),interpolation=cv2.INTER_CUBIC)
    n=cv2.GaussianBlur(n,(0,0),K*3)
    d=np.hypot((xx-cx)/rx,(yy-cy)/ry)+0.05*n/ (np.abs(n).max()+1e-6)
    M=1-smooth(0.72,1.0,d)                                                       # a soft dissolve into the cream
    ring=np.exp(-((d-0.93)/0.025)**2)*0.10                                       # a faint line of pigment where the wash dried
    front=paper(h,w,6)
    art=img[:,:w]
    out=front*(1-M[...,None])+art*M[...,None]
    out=out*(1-ring[...,None])+hx(p['ground'])*0.8*ring[...,None]
    Image.fromarray(out.clip(0,255).astype(np.uint8)).save(O+name)
def window_front(name,p,img,FW,box,arch):
    """the painting in an arched window (the pouch label's shape), with a fine inner rule"""
    h,w=img.shape[0],int((FW+2*B)*K); x0,y0,x1,y1=box; s=arch
    m=Image.new('L',(w*2,h*2),0); d=ImageDraw.Draw(m)
    P=lambda x,y:((x+B)*K*2,(y+B)*K*2)
    pts=[P(x0,y1),P(x0,y0+s)]
    for i in range(41):
        t=i/40; x=x0+(x1-x0)*t; y=y0+s-s*math.sin(math.pi*t)**0.7; pts.append(P(x,y))
    pts+=[P(x1,y0+s),P(x1,y1)]
    d.polygon(pts,fill=255); M=np.asarray(m.resize((w,h),Image.LANCZOS)).astype(np.float32)/255
    out=paper(h,w,6)*(1-M[...,None])+img[:,:w]*M[...,None]
    Image.fromarray(out.clip(0,255).astype(np.uint8)).save(O+name)
def side(name,img,FW): Image.fromarray(img[:,int((FW+B)*K):].clip(0,255).astype(np.uint8)).save(O+name)
# compositions in canvas mm (front mm + 3); the fold at FW+3
def long_art(p,cin=False):
    FW=175.9; f=FW+3
    def art(cv):
        cv.add([leaf((f+80,10),205,64,13,0.3)],mix(p['leaf_core'],p['ground'],0.55),p['leaf_edge'],2.4,alpha=0.75)
        echo(cv,p,(f+40,20),20,1.4)
        if cin: quills(cv,p,(f-70,82),-14,80,3.2)
        pod_pair(cv,p,(f-78,96),-15,128,3.0)
        flush(cv,p,(f+60,94),-108,1.6)
        flush(cv,p,(f-60,92),-78,1.3,blur=0.85)
        cv.add([leaf((f-14,74),-140,20,5,0.2)],p['leaf_core'],p['leaf_edge'],0.8)
        flower(cv,(f-34,52),40,2.45,p,blurs=(0.3,0.26,0.5))
    return art
def cube_art(p):
    FW=87.6; f=FW+3
    def art(cv):
        cv.add([leaf((f+80,58),200,46,10,0.3)],mix(p['leaf_core'],p['ground'],0.55),p['leaf_edge'],2.4,alpha=0.75)
        echo(cv,p,(f+60,80),70,1.1)
        pod_pair(cv,p,(f-60,98),-18,96,2.6)
        flush(cv,p,(f+26,96),-100,1.15,blur=1.0,alpha=0.85)
        flush(cv,p,(f-50,94),-74,1.05,blur=0.85)
        flower(cv,(f-24,64),50,1.8,p,blurs=(0.3,0.26,0.5))
    return art
if __name__=='__main__':
    for name,p,FW,SW,art,wash,win in (
        ('long',TEAL,175.9,85.1,long_art(TEAL),(160,72,98,66),((96,13,166,78),12)),
        ('long-cin',CIN,175.9,85.1,long_art(CIN,True),(160,72,98,66),((96,13,166,78),12)),
        ('cube',TEAL,87.6,84.6,cube_art(TEAL),(80,82,62,54),((8,44,79.6,79),8))):
        import os
        cache=O+name+'-paint.npy'
        img=np.load(cache) if os.path.exists(cache) else paint(p,FW,SW,art); np.save(cache,img)
        wash_front(f'{name}-A-front.png',p,img,FW,*wash)
        window_front(f'{name}-B-front.png',p,img,FW,*win)
        side(f'{name}-side.png',img,FW)
        print(name)
