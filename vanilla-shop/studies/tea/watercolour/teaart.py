# Vanilla tea artwork in the extract labels' technique (studies/extract/split: draw.py, comp.py): a soft watercolour
# vanilla flower with Ceylon tea's two leaves and a bud and a cured pod, glowing out of one saturated colour.
import sys
sys.path.insert(0,'/home/user/PersonalEventPlanner305App/vanilla-shop/studies/extract/split')
import numpy as np, draw
from draw import Canvas, leaf, pod, bud, stem
from comp import flower, mix, sheen
O='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/teaart/'
PAL={'teal':dict(ground='#2C6466',tep_core='#F4FBF2',tep_edge='#8FC3B6',lip_core='#FBFDF4',lip_edge='#CDE6D8',throat_core='#F1C55E',throat_edge='#D49A3A',
                 leaf_core='#7DB59E',leaf_edge='#1F4D4C',pod_core='#3E2416',pod_edge='#1D1310',bud_core='#E2F1E4',bud_edge='#86BBA8',stem='#6FA593'),
     'amber':dict(ground='#B0612A',tep_core='#FFF3E0',tep_edge='#F0A86A',lip_core='#FFF8EC',lip_edge='#F9D3A6',throat_core='#F6C85A',throat_edge='#E0913A',
                 leaf_core='#E9A766',leaf_edge='#7A3A14',pod_core='#4A1F0C',pod_edge='#2A1107',bud_core='#FFE6C6',bud_edge='#EBA266',stem='#D98A4E')}
def tea_sprig(cv,p,base,ang,scale,blur):
    """two leaves and a bud on a short stem: the Ceylon tea flush"""
    s=scale; bx,by=base; a=np.radians(ang)
    tip=(bx+np.cos(a)*22*s,by+np.sin(a)*22*s); mid=(bx+np.cos(a)*11*s+2*s,by+np.sin(a)*11*s)
    cv.add([stem([base,mid,tip],0.55*s)],mix(p['stem'],'#FFFFFF',0.25),p['stem'],blur*0.8)
    lv=[(mid,ang-58,17*s,4.6*s,-0.35),((bx+np.cos(a)*17*s,by+np.sin(a)*17*s),ang+48,13*s,3.6*s,0.3)]
    cv.add([leaf(*q) for q in lv],p['leaf_core'],p['leaf_edge'],blur,glow=1.0)
    sheen(cv,[leaf(*q,spine=True) for q in lv],0.32*s,mix(p['leaf_core'],'#FFFFFF',0.35),p['leaf_core'],blur,0.5)
    cv.add([bud(tip,ang-8,8*s,1.7*s,0.15)],p['bud_core'],p['bud_edge'],blur*0.8,glow=1.2)
def compose(k,W,H,fc,fs,lip,sprig,pods_,back_leaf):
    p=PAL[k]; cv=Canvas(W,H,0)
    for q in back_leaf: cv.add([leaf(*q)],mix(p['leaf_core'],p['ground'],0.35),p['leaf_edge'],2.4,alpha=0.85)
    cv.add([pod(*q) for q in pods_],p['pod_core'],p['pod_edge'],0.6,glow=0.9)
    sheen(cv,[pod(*q,spine=True)[3:-6]+np.array([0,-0.25*q[3]]) for q in pods_],0.32*min(q[3] for q in pods_),mix(p['pod_core'],'#FFFFFF',0.35),p['pod_core'],0.55,0.55)
    tea_sprig(cv,p,*sprig)
    flower(cv,fc,lip,fs,p,blurs=(0.45,0.38,0.7))
    return cv.render(p['ground'],seed=21)
def long_front(k):    # 179 x 91: big and cropped top right; the name along the foot and the data top left stay on plain colour
    return compose(k,182,91,(136,34),3.1,35,((78,40),-42,2.3,0.9),
                   [((70,92),-14,140,4.4,0.16,1),((86,100),-22,128,3.8,0.1,-1)],[((176,100),-118,70,13,0.4)])
def cube_front(k):    # 92 x 91: the flower lower right, cropped by the edges; the tea flush rising behind it
    return compose(k,94,91,(64,62),2.55,150,((52,100),-78,2.0,0.9),
                   [((10,104),-26,120,3.8,0.16,1)],[((104,30),165,62,11,-0.3)])
if __name__=='__main__':
    for k in PAL:
        long_front(k).save(O+f'long-{k}.png'); cube_front(k).save(O+f'cube-{k}.png'); print(k)
