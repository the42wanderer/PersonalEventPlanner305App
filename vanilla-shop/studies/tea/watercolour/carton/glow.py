# Tea cartons, round two of the cream layout: the pouch colours (teal, terracotta) brought into the lower right as one
# artwork with the botanicals. The colour is deepest behind the flower and towards the corner, and the transition into
# the cream is made by the plant itself: a vine, bud and leaves reach out and carry soft colour with them; everything
# fades over a long distance. Plain paper elsewhere (fine grain only); the lid is just the seal.
import sys, os
sys.path.insert(0,'/home/user/PersonalEventPlanner305App/vanilla-shop/studies/extract/split')
sys.path.insert(0,'/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/teaart')
import numpy as np, cv2
from PIL import Image
import draw
from draw import leaf, bud, stem
from comp import flower, mix, sheen
from split2 import WC, flush, pod_pair, echo, quills, TEAL, CIN
O='/home/user/PersonalEventPlanner305App/vanilla-shop/studies/tea/watercolour/carton/glow/'
K=draw.K; B=3; PAPER=np.array([0xF6,0xEE,0xDC],np.float32)
def smooth(a,b,x): t=np.clip((x-a)/(b-a),0,1); return t*t*(3-2*t)
def reach(cv,p,pts,leaves,budat):
    """a vine reaching out of the colour into the cream: stem, a few leaves, a bud at its tip (soft-edged, no outline)"""
    cv.nowash=True
    cv.add([stem(pts,0.7)],mix(p['tstem'],'#FFFFFF',0.15),p['tstem'],0.5)
    cv.add([leaf(*q) for q in leaves],p['leaf_core'],p['leaf_edge'],0.6)
    sheen(cv,[leaf(*q,spine=True) for q in leaves],0.3,mix(p['leaf_core'],'#FFFFFF',0.3),p['leaf_core'],0.6,0.35)
    cv.add([bud(*budat)],p['tbud_core'],p['tbud_edge'],0.5,glow=1.2); cv.nowash=False
def compose(name,p,FW,SW,art,centre,radii,corner):
    cache=O+name+'-paint.npy'
    if os.path.exists(cache): img=np.load(cache)
    else:
        cv=WC(int(round(B+FW+SW+B)),85+2*B); art(cv); img=cv.render(p['ground'],grain=0,raw=True); np.save(cache,img)
    h,w=img.shape[:2]; yy,xx=np.mgrid[0:h,0:w].astype(np.float32)/K-B
    g=np.array([int(p['ground'][i:i+2],16) for i in (1,3,5)],np.float32)
    # depth inside the colour: a touch lighter round the flower, deeper towards the corner
    dc=np.hypot((xx-corner[0])/90,(yy-corner[1])/70); img=img*(0.86+0.14*smooth(0.0,1.0,dc))[...,None]
    # the transition: a long, soft fall-off, extended by the plant reaching out
    d=np.hypot((xx-centre[0])/radii[0],(yy-centre[1])/radii[1]); R=1-smooth(0.40,1.08,d)
    el=np.clip((np.abs(img-g).sum(2)-26)/50,0,1)
    core=cv2.GaussianBlur(cv2.erode((el>0.6).astype(np.uint8),np.ones((int(0.9*K),)*2,np.uint8)).astype(np.float32),(0,0),0.45*K)   # interiors only, not the halo
    G=np.clip(cv2.GaussianBlur(cv2.dilate(el,np.ones((int(2*K),)*2,np.uint8)),(0,0),5*K)*1.5,0,1)*0.8
    M=np.clip(np.maximum(R,G),0,1); M=np.maximum(M,core*np.clip(M*3,0,1))        # the plant itself stays whole; its halo melts into the paper
    paper=np.ones_like(img)*PAPER
    out=paper*(1-M[...,None])+img*M[...,None]+np.random.default_rng(5).normal(0,3.4,(h,w))[...,None]
    fx=int((FW+B)*K)
    Image.fromarray(out[:,:int((FW+2*B)*K)].clip(0,255).astype(np.uint8)).save(O+f'{name}-front.png')
    Image.fromarray(out[:,fx:].clip(0,255).astype(np.uint8)).save(O+f'{name}-side.png')
def long_art(p,cin):
    FW=175.9; f=FW+3
    def art(cv):
        cv.add([leaf((f+60,8),205,70,14,0.3)],mix(p['leaf_core'],p['ground'],0.5),p['leaf_edge'],2.6,alpha=0.8)
        echo(cv,p,(f+36,30),20,1.4)
        reach(cv,p,[(f-30,58),(f-48,46),(f-66,38),(f-80,30),(f-88,20)],
              [((f-50,45),-150,16,4.0,0.25),((f-70,36),60,14,3.6,-0.2),((f-84,25),-170,11,3.0,0.2)],((f-88,20),-110,9,2.0,0.1))
        if cin: quills(cv,p,(f-74,84),-13,84,3.2)
        pod_pair(cv,p,(f-82,96),-13,132,3.0)
        flush(cv,p,(f+54,94),-106,1.6)
        flush(cv,p,(f-70,94),-80,1.3,blur=0.8)
        flower(cv,(f-34,56),40,2.4,p,blurs=(0.3,0.26,0.5))
    return art
def cube_art(p,cin):
    FW=87.6; f=FW+3
    def art(cv):
        cv.add([leaf((f+60,46),200,50,11,0.3)],mix(p['leaf_core'],p['ground'],0.5),p['leaf_edge'],2.4,alpha=0.8)
        echo(cv,p,(f+44,76),70,1.0)
        reach(cv,p,[(f-16,62),(f-12,48),(f-8,36),(f-12,24)],[((f-12,47),200,12,3.2,0.25),((f-9,35),-20,11,3.0,-0.2)],((f-12,24),-100,7,1.6,0.1))
        if cin: quills(cv,p,(f-60,88),-16,60,2.4)
        pod_pair(cv,p,(f-64,98),-17,98,2.5)
        flush(cv,p,(f+22,96),-100,1.1,blur=1.0,alpha=0.85)
        flush(cv,p,(f-50,96),-76,1.0,blur=0.8)
        flower(cv,(f-24,66),50,1.7,p,blurs=(0.3,0.26,0.5))
    return art
def papers():
    k=12; h=w=int(260*k)
    pap=np.ones((h,w,3),np.float32)*PAPER+np.random.default_rng(21).normal(0,3.2,(h,w))[...,None]
    im=Image.fromarray(pap.clip(0,255).astype(np.uint8)); im.save(O+'paper.jpg',quality=92); im.save(O+'paper-lid.jpg',quality=92)
if __name__=='__main__':
    compose('long',TEAL,175.9,85.1,long_art(TEAL,False),(150,74),(120,74),(190,100))
    compose('cube',TEAL,87.6,84.6,cube_art(TEAL,False),(80,76),(70,58),(100,100))
    compose('long-cin',CIN,175.9,85.1,long_art(CIN,True),(150,74),(120,74),(190,100))
    papers(); print('ok')
