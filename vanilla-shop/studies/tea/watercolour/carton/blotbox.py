# Tea cartons, blot direction: the painting soaked into aged cream paper like spilt tea, low on the front and round the
# corner onto the right side; the left side, back and lid are the same aged paper, the lid with a faint tea ring.
import sys, math
sys.path.insert(0,'/home/user/PersonalEventPlanner305App/vanilla-shop/studies/extract/split')
sys.path.insert(0,'/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/teaart')
import numpy as np, cv2
from PIL import Image
import draw
from draw import leaf
from comp import flower, mix
from split2 import WC, flush, pod_pair, echo, quills
from blot import soak_in, aged_paper, blot_mask
O='/home/user/PersonalEventPlanner305App/vanilla-shop/studies/tea/watercolour/carton/blot/'
K=draw.K; B=3; PAPER=np.array([0xF4,0xEB,0xD6],np.float32)
base=dict(tep_core='#FFFDF6',lip_core='#FFFEF8',throat_core='#F3C75E',throat_edge='#D69B3A',pod_core='#4A2A16',pod_edge='#26150B',tbud_core='#F2F6E2',sheen=0.15)
GOLD=dict(base,ground='#DBB28C',tep_edge='#F0DCC6',lip_edge='#F7EBDC',leaf_core='#A3AC80',leaf_edge='#6A7048',tea_core='#99A877',tea_edge='#5E6E42',tbud_edge='#BCC49A',tstem='#929E70',tide='#A87452')
CIN=dict(base,ground='#CF9F86',tep_edge='#F0D6C6',lip_edge='#F7E8DC',leaf_core='#A3AC80',leaf_edge='#6A7048',tea_core='#99A877',tea_edge='#5E6E42',tbud_edge='#BCC49A',tstem='#929E70',
         quill_core='#C9844E',quill_edge='#7A3A18',tide='#9C5E44')
def long_art(p,cin):
    FW=175.9; f=FW+3
    def art(cv):
        cv.add([leaf((f+70,24),205,60,12,0.3)],mix(p['leaf_core'],p['ground'],0.5),p['leaf_edge'],2.4,alpha=0.6)
        echo(cv,p,(f+40,34),20,1.3)
        if cin: quills(cv,p,(f-72,84),-14,80,3.0)
        pod_pair(cv,p,(f-80,96),-14,130,2.9)
        flush(cv,p,(f+56,94),-106,1.5)
        flush(cv,p,(f-64,94),-76,1.25,blur=0.85)
        flower(cv,(f-36,56),40,2.35,p,blurs=(0.3,0.26,0.5))
    return art,[((f-30)*K,(B+64)*K,62*K,40*K),((f+36)*K,(B+56)*K,32*K,40*K),((f-86)*K,(B+84)*K,26*K,12*K),
                ((f-104)*K,(B+70)*K,2.4*K,2.1*K),((f-96)*K,(B+62)*K,1.3*K,1.2*K)]
def cube_art(p,cin):
    FW=87.6; f=FW+3
    def art(cv):
        cv.add([leaf((f+70,50),200,44,10,0.3)],mix(p['leaf_core'],p['ground'],0.5),p['leaf_edge'],2.4,alpha=0.6)
        echo(cv,p,(f+50,74),70,1.0)
        if cin: quills(cv,p,(f-58,86),-16,60,2.4)
        pod_pair(cv,p,(f-62,98),-18,96,2.5)
        flush(cv,p,(f+24,96),-100,1.1,blur=1.0,alpha=0.85)
        flush(cv,p,(f-48,96),-74,1.0,blur=0.85)
        flower(cv,(f-22,64),50,1.7,p,blurs=(0.3,0.26,0.5))
    return art,[((f-18)*K,(B+68)*K,34*K,28*K),((f+30)*K,(B+66)*K,30*K,30*K),((f-50)*K,(B+86)*K,16*K,9*K),
                ((f-58)*K,(B+74)*K,2.0*K,1.8*K)]
def build(name,p,FW,SW,mk,cin=False):
    art,blobs=mk(p,cin)
    cv=WC(int(round(B+FW+SW+B)),85+2*B); art(cv); img=cv.render(p['ground'],grain=0,raw=True)
    out=soak_in(img,PAPER,blobs,p['tide'],seed=3)
    fx=int((FW+B)*K)
    Image.fromarray(out[:,:int((FW+2*B)*K)].clip(0,255).astype(np.uint8)).save(O+f'{name}-front.png')
    Image.fromarray(out[:,fx:].clip(0,255).astype(np.uint8)).save(O+f'{name}-side.png')
def papers():
    """aged paper for the other faces, and the lid with a faint tea ring (as if a cup had stood on it)"""
    k=12; h=w=int(260*k)
    import blot; blot.K=k
    pap=aged_paper(h,w,PAPER,21); Image.fromarray(pap.clip(0,255).astype(np.uint8)).save(O+'paper.jpg',quality=92)
    yy,xx=np.mgrid[0:h,0:w].astype(np.float32)/k
    r=np.hypot(xx-130,yy-130); n=blot.fbm(h,w,int(20*k),5)
    ring=np.exp(-((r-37+2.5*n)/0.9)**2)*(0.5+0.5*np.clip(np.sin(np.arctan2(yy-130,xx-130)*1.0+1.3)+0.6,0,1))
    ring=cv2.GaussianBlur(ring,(0,0),0.4*k)*0.16
    tc=np.array([0xA8,0x74,0x52],np.float32); lid=pap*(1-ring[...,None])+tc*ring[...,None]
    Image.fromarray(lid.clip(0,255).astype(np.uint8)).save(O+'paper-lid.jpg',quality=92); blot.K=20
if __name__=='__main__':
    build('long',GOLD,175.9,85.1,long_art); build('cube',GOLD,87.6,84.6,cube_art); build('long-cin',CIN,175.9,85.1,long_art,True)
    papers(); print('ok')
