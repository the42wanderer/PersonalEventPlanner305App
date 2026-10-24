# Three art directions for the Vanilla Tea 25-bag carton, judged on one box. Long carton: front 175.9 mm, side 85.1 mm,
# height 85 mm, 3 mm bleed. The type layout is the generator's own, identical for all three.
#  A  Atmospheric: black-tea mahogany, one enormous flower in focus between an out-of-focus bloom behind and
#     out-of-focus pods in front: depth by planes, like a lens, not blur everywhere.
#  B  Graphic: deep tea-estate green, flat cut shapes in four inks, a low ochre sun, selective fine line detail.
#  C  The extract system: cream panel and a full-height teal field cropped hard, a tonal flower painted out of
#     the field's own colour, as on the extract labels.
import sys, os, math
sys.path.insert(0,'/home/user/PersonalEventPlanner305App/vanilla-shop/studies/extract/split')
sys.path.insert(0,'/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/teaart')
import numpy as np
from PIL import Image
import draw
from draw import Canvas, leaf, tepal, pod, bud, ribbon, trumpet, ellipse_ruffle, arc
from comp import flower, pods, mix
from blot2 import fbm
K=draw.K; BL=3; FW,SW,H=175.9,85.1,85; W=267; HH=91; f=FW+BL
O='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/teaart/cx/'
def rgb(c): return np.array([int(c[i:i+2],16) for i in (1,3,5)],np.float32)
def save(img,d,split=False):
    os.makedirs(O+d,exist_ok=True); out=np.asarray(img).clip(0,255).astype(np.uint8); fx=int((FW+BL)*K); sfx='-split' if split else ''
    for k in ('long','cube'):
        Image.fromarray(out[:,:int((FW+2*BL)*K)]).save(O+d+f'/{k}{sfx}-front.png'); Image.fromarray(out[:,fx:]).save(O+d+f'/{k}{sfx}-side.png')
def ground_tex(col,name,seed=4):
    g=np.ones((900,900,3),np.float32)*rgb(col); g*=1+0.025*fbm(900,900,40,seed)[...,None]; g+=np.random.default_rng(seed).normal(0,4,(900,900))[...,None]
    im=Image.fromarray(g.clip(0,255).astype(np.uint8)); im.save(O+name+'/paper.jpg',quality=92); im.save(O+name+'/paper-lid.jpg',quality=92)

def A():
    g='#3A1C14'; cv=Canvas(W,HH)
    far=dict(tep_core='#7C4A33',tep_edge='#5C3222',ground=g,lip_core='#8A5640',lip_edge='#6E412E',throat_core='#7C4A33',throat_edge='#5C3222')
    flower(cv,(104,30),130,3.3,far,blurs=(3.6,3.4,3.8))                                   # the bloom behind: out of focus
    cv.add([leaf((f+30,104),-122,92,16,0.3),leaf((f+70,100),-100,70,13,-0.2),leaf((f-80,104),-62,70,12,0.25)],'#552C1D','#43221A',2.6,alpha=0.9)
    hero=dict(tep_core='#FFF2DF',tep_edge='#DE9E6A',ground=g,lip_core='#FFF9EE',lip_edge='#F1C79E',throat_core='#F3BF55',throat_edge='#C8892C')
    flower(cv,(f-58,50),30,3.75,hero,blurs=(0.35,0.3,0.5))                                 # the hero, in focus
    p=dict(pod_core='#26130C',pod_edge='#120805')
    pods(cv,p,[((f-178,104),-9,185,4.6,0.1,1),((f-160,109),-14,170,4.0,0.06,-1)],1.9,sheen_col='#6A3826')  # pods in front: out of focus
    img=cv.render(g,grain=7,seed=21); save(img,'A'); ground_tex(g,'A')

def rough(poly,amt):
    """a cut / printed edge: a slight, irregular wander instead of a vector curve"""
    P=np.asarray(poly,float); n=len(P); r=np.random.default_rng(n)
    d=np.roll(P,-1,0)-np.roll(P,1,0); d/=np.linalg.norm(d,axis=1,keepdims=True)+1e-9; nr=np.stack([d[:,1],-d[:,0]],1)
    w=np.convolve(np.r_[r.normal(0,1,n),r.normal(0,1,6)],np.ones(5)/5,'same')[:n]
    return P+nr*(w*amt)[:,None]
def B():
    g=rgb('#1F3A2B'); h,w=HH*K,W*K
    from foliage2 import Paint
    P=Paint(W,HH,seed=5); img=np.ones((h,w,3),np.float32)*g
    def disc(c,r,n=160): t=np.linspace(0,2*np.pi,n); return np.stack([c[0]+r*np.cos(t),c[1]+r*np.sin(t)],1)
    P.over(img,rough(disc((f-40,40),36,400),0.1),'#B98A3E',1.0,0.07)                                      # the low sun over the estate
    LV=[((f+24,102),-131,118,21,0.25,'#6E9A6C'),((f+8,100),-94,84,14,-0.15,'#A7C39A'),((f-34,100),-152,74,13,0.2,'#3E6B4A'),
        ((f+74,100),-100,62,11,0.15,'#6E9A6C'),((f+52,100),-120,46,9,0.1,'#3E6B4A')]
    for (p0,a,L,Wd,b,c) in LV:
        P.over(img,rough(leaf(p0,a,L,Wd,b),0.12),c,1.0,0.07)
    for (p0,a,L,Wd,b,c) in LV[:2]:                                                        # selective detail: veins on two leaves only
        sp=leaf(p0,a,L,Wd,b,spine=True); P.over(img,ribbon(sp[2:-3],lambda t:0.32*(1-0.6*t)+0.05),'#F3E8CF',0.75,0.0)
        d=np.gradient(sp,axis=0); d/=np.linalg.norm(d,axis=1,keepdims=True); n=np.stack([-d[:,1],d[:,0]],1)
        for k in (0.25,0.38,0.51,0.64,0.77):
            j=int(k*(len(sp)-1)); Lw=Wd*0.75*(1-0.4*k)
            for sg in (1,-1): P.over(img,ribbon(draw.cr([sp[j],sp[j]+d[j]*Lw*0.5+n[j]*sg*Lw*0.55,sp[j]+d[j]*Lw*1.1+n[j]*sg*Lw*0.9],8),lambda t:0.16*(1-t)+0.04),'#F3E8CF',0.55,0.0)
    for q in (((f-160,92),-12,150,2.3,0.22,0),((f-150,97),-19,136,2.0,0.16,0)):
        P.over(img,rough(pod(*q),0.08),'#3E2216',1.0,0.0)
        sp=pod(*q[:5],spine=True)
        for off in (-0.3,0.25): 
            d=np.gradient(sp,axis=0); d/=np.linalg.norm(d,axis=1,keepdims=True); n=np.stack([-d[:,1],d[:,0]],1)
            P.over(img,ribbon((sp+n*off*q[3])[3:-4],lambda t:0.09),'#6B4030',0.8,0.0)
    c=(f-52,44); s=3.2; spec=[(-97,16.5,2.0,0.26,0.0),(-160,14.8,1.85,-0.36,0.3),(-36,15.6,1.9,0.34,0.25),(126,13.2,1.75,0.30,0.4),(54,13.8,1.8,-0.32,0.35)]
    for i in (1,3,0,2,4):
        a,L,Wd,b,pin=spec[i]; a2=a+40*0.25; Lf=L*s*(0.8+0.2*abs(np.cos(np.radians(a2-40))))
        poly=tepal(c,a2,Lf,Wd*s,b,0.0,i*0.9,pin)
        P.over(img,poly,'#DCE3CC' if i in (1,3) else '#F5EDD8',1.0,0.0)
        P.shade(img,poly,np.array([0.8,0.8]),'#B9C6A6',0.8)
        sp=tepal(c,a2,Lf*0.8,Wd*s,b,spine=True); P.over(img,ribbon(sp,lambda t:0.18*np.sin(np.pi*t)+0.03),'#FFFFFF',0.9,0.0)
    tube,mouth,mc=trumpet(c,40,7.5*s,1.1*s,3.6*s,2.6*s,0.13)
    P.over(img,tube,'#EDE7D2',1.0,0.0); P.over(img,mouth,'#FFF8EA',1.0,0.0)
    dd=np.array([np.cos(np.radians(40)),np.sin(np.radians(40))])
    P.over(img,ellipse_ruffle(mc+dd*0.5*s,1.7*s,1.25*s,40,0.07,7),'#D9A23F',1.0,0.0)
    img*=(1+0.02*P.tooth)[...,None]; img+=np.random.default_rng(2).normal(0,2.2,(h,w))[...,None]
    save(img,'B'); ground_tex('#1F3A2B','B')

def C():
    g='#2C6466'; cv=Canvas(W,HH)
    echo=dict(tep_core='#6FA3A0',tep_edge='#4F8785',ground=g,lip_core='#7DAEAA',lip_edge='#64999A',throat_core='#8FA97E',throat_edge='#6E9070')
    flower(cv,(f+8,8),150,2.6,echo,blurs=(2.8,2.6,3.0))
    cv.add([leaf((f+40,104),-118,80,14,0.3),leaf((f-10,104),-80,60,11,-0.2),leaf((f+80,100),-104,56,10,0.2)],'#225558','#1B4749',1.3,alpha=0.95)
    p=dict(pod_core='#2B1710',pod_edge='#140A06')
    pods(cv,p,[((96,99),-18,92,2.9,0.12,1),((100,104),-25,84,2.5,0.08,-1)],0.55,sheen_col='#6B4A3A')
    hero=dict(tep_core='#F4F8F1',tep_edge='#97C6BF',ground=g,lip_core='#FFFDF6',lip_edge='#CFE4DA',throat_core='#EFC25C',throat_edge='#C9932E')
    flower(cv,(f-40,48),36,3.3,hero,blurs=(0.3,0.26,0.45))
    img=np.asarray(cv.render(g,grain=7,seed=23)).astype(np.float32)
    x=int((BL+92)*K); cream=np.ones((HH*K,x,3),np.float32)*rgb('#F6EEDC'); cream+=np.random.default_rng(1).normal(0,2.0,cream.shape[:2])[...,None]
    img[:,:x]=cream                                                                        # the extract labels' hard split
    save(img,'C',split=True)

if __name__=='__main__':
    {'A':A,'B':B,'C':C}[sys.argv[1]](); print('ok',sys.argv[1])
