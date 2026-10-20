# bottles at true relative size, front and back, for the three label sizes
import sys; sys.path.insert(0,'../n')
import numpy as np
from PIL import Image
from bottle3 import bottle
T='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/ext/d/'
GROUND={'01':'#B83A24','02':'#C98A22','03':'#2F5A33'}; LIQ={'01':(58,22,10),'02':(96,52,14),'03':(122,74,26)}
D={'500':72,'200':53,'100':42}; H={'500':70,'200':42,'100':35}
def turned(png,frac):
    im=np.asarray(Image.open(T+png).convert('RGBA')); sh=int(im.shape[1]*frac)
    Image.fromarray(np.roll(im,-sh,axis=1)).save(T+'_t.png'); return T+'_t.png'
def row(k,sizes,back=False):
    ims=[]
    for z in sizes:
        f=f'SW-{k}.png' if z=='500' else f'SW-{k}-{z}.png'
        lab=turned(f,0.5) if back else T+f
        ims.append(bottle(lab,GROUND[k],LIQ[k],scale=D[z]/76,lab_h=H[z],true=True))
    return ims
def board(groups,out,bg=(236,228,214)):
    ims=[i for g in groups for i in g]; gap=60
    Wt=sum(i.size[0] for i in ims)+gap*(len(ims)+1)+gap*2*(len(groups)-1); Ht=max(i.size[1] for i in ims)+2*gap
    B=Image.new('RGBA',(Wt,Ht),bg+(255,)); x=gap
    for g in groups:
        for i in g: B.alpha_composite(i,(x,Ht-gap-i.size[1])); x+=i.size[0]+gap
        x+=gap*2
    B.convert('RGB').save(out,quality=88); print(out,B.size)
board([row('01',['500','200','100']),row('02',['500','200','100']),row('03',['500'])],T+'sizes-front.jpg')
board([row('01',['500','200','100'],True),row('02',['500','200','100'],True),row('03',['500'],True)],T+'sizes-back.jpg')
