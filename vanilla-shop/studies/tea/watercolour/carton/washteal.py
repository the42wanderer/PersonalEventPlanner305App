# Vanilla Tea cartons, translated from the frozen pouch: the pouch's teal and its painting, laid as layered watercolour
# glazes on the cream (no rectangle, no gradient). The painting uses the pouch palette and technique, a touch crisper.
import sys
sys.path.insert(0,'/home/user/PersonalEventPlanner305App/vanilla-shop/studies/extract/split')
sys.path.insert(0,'/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/teaart')
import numpy as np
from PIL import Image
import draw
from draw import leaf
from comp import flower, mix
from split2 import WC, flush, pod_pair, echo, TEAL
from blot2 import paint_wash, lift
O='/home/user/PersonalEventPlanner305App/vanilla-shop/studies/tea/watercolour/carton/washteal/'
K=draw.K; B=3; PAPER=np.array([0xF6,0xEE,0xDC],np.float32)
p=TEAL
def build(name,FW,SW,art,layers):
    W=int(round(B+FW+SW+B)); cv=WC(W,85+2*B); cv.crisp=True; cv.cap=0.22; art(cv)
    col,al=lift(cv); h,w=al.shape
    wash=paint_wash(h,w,PAPER,layers,seed=3)
    out=wash*(1-al[...,None])+col*al[...,None]+np.random.default_rng(4).normal(0,2.6,(h,w))[...,None]
    fx=int((FW+B)*K)
    Image.fromarray(out[:,:int((FW+2*B)*K)].clip(0,255).astype(np.uint8)).save(O+f'{name}-front.png')
    Image.fromarray(out[:,fx:].clip(0,255).astype(np.uint8)).save(O+f'{name}-side.png')
C=lambda x,y,rx,ry:((B+x)*K,(B+y)*K,rx*K,ry*K)
# glazes: very diluted teal outermost, then mid, then the pouch's own teal behind the flower (they multiply)
G1,G2,G3='#D5E4E1','#9EC0BC','#3F7C7C'
def long_box():
    FW=175.9; f=FW+3
    def art(cv):
        pod_pair(cv,p,(f-86,96),-15,136,3.0)
        flush(cv,p,(f-70,94),-78,1.35)
        flush(cv,p,(f+60,96),-104,1.3)
        flower(cv,(f-40,44),40,2.75,p,blurs=(0.3,0.26,0.5))
    layers=[([C(134,50,70,46),C(200,70,40,30),C(96,82,32,12)],1.0,G1,0.7,0.4),
            ([C(136,48,56,38),C(198,72,26,20)],1.0,G2,0.7,0.0),
            ([C(138,46,40,30),C(196,76,14,12)],1.0,G3,0.85,-0.3),
            ([C(82,64,2.4,2.1),C(92,57,1.3,1.2)],1.0,G2,0.8,-0.6)]
    build('long',FW,85.1,art,layers)
def cube_box():
    FW=87.6; f=FW+3
    def art(cv):
        pod_pair(cv,p,(f-64,98),-18,98,2.5)
        flush(cv,p,(f-50,96),-74,1.0)
        flush(cv,p,(f+30,98),-100,1.0)
        flower(cv,(f-22,62),50,1.8,p,blurs=(0.3,0.26,0.5))
    layers=[([C(68,68,50,40),C(116,74,30,22),C(30,88,24,10)],1.0,G1,0.7,0.4),
            ([C(68,66,38,30),C(116,76,18,14)],1.0,G2,0.7,0.0),
            ([C(68,64,27,22)],1.0,G3,0.85,-0.3),
            ([C(30,60,2.0,1.8),C(40,52,1.2,1.1)],1.0,G2,0.8,-0.6)]
    build('cube',FW,84.6,art,layers)
if __name__=='__main__':
    long_box(); cube_box()
    import shutil; shutil.copy(O+'../bw2/paper.jpg',O+'paper.jpg'); shutil.copy(O+'../bw2/paper.jpg',O+'paper-lid.jpg')   # plain lid
    print('ok')
