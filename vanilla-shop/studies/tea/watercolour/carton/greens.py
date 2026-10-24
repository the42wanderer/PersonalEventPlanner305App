# Vanilla Tea cartons in the two greens (Ceylon Green, Sage): the washteal layout, with the How to brew side
# laid entirely in the same layered watercolour (no panel edge inside the side; it runs off the folds).
import sys, shutil
sys.path.insert(0,'/home/user/PersonalEventPlanner305App/vanilla-shop/studies/extract/split')
sys.path.insert(0,'/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/teaart')
import numpy as np
from PIL import Image
import draw
from comp import flower, mix
from split2 import WC, flush, pod_pair
from blot2 import paint_wash, lift
K=draw.K; B=3; PAPER=np.array([0xF6,0xEE,0xDC],np.float32)
ROOT='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/teaart/'
def pal(ground):
    lc=mix('#7C9663',ground,0.22); le=mix('#3E5530',ground,0.22); tip=mix('#9AA466',ground,0.2)
    return dict(tep_core='#FFFDF8',lip_core='#FFFEF9',throat_core='#F3C75E',throat_edge='#D69B3A',pod_core='#4A2A16',pod_edge='#26150B',tbud_core=mix('#E4EBD2',ground,0.1),
                ground=ground,tep_edge='#E4EFE8',lip_edge='#F6F4EC',leaf_core=lc,leaf_edge=le,tea_core=lc,tea_edge=le,tea_tip=tip,veins=True,
                tbud_edge=mix('#9DB083',ground,0.2),tstem=mix('#7E965E',ground,0.2))
OPTS={'green':('#2F5E3E','#D9E6D6','#9DBF9F'),'sage':('#6E8C6A','#E2EADB','#B4C8AC')}
C=lambda x,y,rx,ry:((B+x)*K,(B+y)*K,rx*K,ry*K)
def side_layers(FW,SW,g1,g2):
    # the brew side: a full pale glaze that runs past both folds, a second glaze pooled unevenly over it
    c=FW+SW/2
    return [([C(c,42,SW*0.82,70)],1.0,g1,0.8,0.5),
            ([C(c+SW*0.12,24,SW*0.42,22),C(c-SW*0.15,66,SW*0.38,24)],1.0,g2,0.42,0.6)]
def build(O,name,FW,SW,art,layers):
    W=int(round(B+FW+SW+B)); cv=WC(W,85+2*B); cv.crisp=True; cv.cap=0.22; art(cv)
    col,al=lift(cv); h,w=al.shape
    wash=paint_wash(h,w,PAPER,layers,seed=3)
    out=wash*(1-al[...,None])+col*al[...,None]+np.random.default_rng(4).normal(0,2.6,(h,w))[...,None]
    fx=int((FW+B)*K)
    Image.fromarray(out[:,:int((FW+2*B)*K)].clip(0,255).astype(np.uint8)).save(O+f'{name}-front.png')
    Image.fromarray(out[:,fx:].clip(0,255).astype(np.uint8)).save(O+f'{name}-side.png')
def run(key):
    ground,G1,G2=OPTS[key]; G3=ground; p=pal(ground); O=ROOT+f'w-{key}/'
    import os; os.makedirs(O,exist_ok=True)
    FW,SW=175.9,85.1; f=FW+3
    def art(cv):
        pod_pair(cv,p,(f-86,96),-15,98,3.0)   # stops at the fold: the brew steps stay clear; flush(cv,p,(f-70,94),-78,1.35); flush(cv,p,(f+60,96),-104,1.3)
        flower(cv,(f-40,44),40,2.75,p,blurs=(0.3,0.26,0.5))
    build(O,'long',FW,SW,art,side_layers(FW,SW,G1,G2)+[([C(134,50,70,46),C(96,82,32,12)],1.0,G1,0.7,0.4),
            ([C(136,48,56,38),C(198,72,26,20)],1.0,G2,0.7,0.0),([C(138,46,40,30),C(234,86,12,8)],1.0,G3,0.85,-0.3),
            ([C(82,64,2.4,2.1),C(92,57,1.3,1.2)],1.0,G2,0.8,-0.6)])
    if ONLY=='long': return
    FW,SW=87.6,84.6; f=FW+3
    def art(cv):
        pod_pair(cv,p,(f-64,98),-18,98,2.5); flush(cv,p,(f-50,96),-74,1.0); flush(cv,p,(f+30,98),-100,1.0)
        flower(cv,(f-22,62),50,1.8,p,blurs=(0.3,0.26,0.5))
    build(O,'cube',FW,SW,art,side_layers(FW,SW,G1,G2)+[([C(68,68,50,40),C(30,88,24,10)],1.0,G1,0.7,0.4),
            ([C(68,66,38,30),C(116,76,18,14)],1.0,G2,0.7,0.0),([C(68,64,27,22)],1.0,G3,0.85,-0.3),
            ([C(30,60,2.0,1.8),C(40,52,1.2,1.1)],1.0,G2,0.8,-0.6)])
    shutil.copy(ROOT+'bw2/paper.jpg',O+'paper.jpg'); shutil.copy(ROOT+'bw2/paper.jpg',O+'paper-lid.jpg')
if __name__=='__main__': ONLY=sys.argv[2] if len(sys.argv)>2 else ''; run(sys.argv[1]); print('ok',sys.argv[1])
