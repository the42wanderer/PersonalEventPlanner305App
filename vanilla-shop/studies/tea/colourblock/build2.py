# Vanilla Tea, 25-bag carton, after the tea board (pins 5, 6, 10): colour-blocked like the bottle's split (cream |
# deep teal, wrapping the corner), the candles' giant cropped serif on the colour side, the soap's grid and caps on
# the cream, and a dense, flat, crisp botanical (vanilla flower, buds, cured pods, Ceylon tea shoots) on the band.
import sys, json, math, numpy as np
from PIL import Image, ImageDraw, ImageFont
S='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/'
sys.path.insert(0,S+'teasoap'); sys.path.insert(0,S+'teaart')
import build as b
from build import logo, txt, caps, rule, para, lion, face, grain, hx, FW, FH, SW, LH, B
import foliage2 as fo
from foliage2 import tealeaf, paint_flower, paint_pod, paint_vbud, Paint, LIGHT
from comp import mix
import draw
K=12; fo.K=K; draw.K=K
R='/home/user/PersonalEventPlanner305App/vanilla-shop'
O=b.O
SPLIT=96                                     # cream panel width on the front, mm (the bottle's split)
CW={'teal':dict(paper='#F3ECDC',band='#1D4F4D',word='#245E5B',ink='#163F3D',deep='#2F6E6A',lt='#F3ECDC',
                leaves=('#2C5B45','#4F7F5C','#7EA57A','#A9C79A'),pod='#3A2216')}
def flatleaf(P,img,p0,ang,L,W,bend,col,dark,vein,rng):
    """a tea leaf, flat and crisp: one colour, the shaded half a step darker, the veins drawn in a light line"""
    poly,sp,half,d,nrm,u,prof=tealeaf(p0,ang,L,W,bend,rng)
    P.over(img,poly,col,1.0,0.03); P.over(img,half,dark,1.0,0.03)
    P.over(img,draw.ribbon(sp[3:-4],lambda t,w=W*0.04:w*(1-0.7*t)+0.02),vein,0.8,0)
    n=len(sp)
    for k in (0.3,0.45,0.6,0.74):
        j=int(k*(n-1))
        for sg in (1,-1):
            e=sp[j]+nrm[j]*sg*prof[j]*0.8+d[j]*prof[j]*0.85
            P.over(img,draw.ribbon(draw.cr([sp[j],(sp[j]+e)/2+d[j]*prof[j]*0.12,e],6),lambda t,w=W*0.018:w*(1-t)+0.01),vein,0.55,0)
def shoot(P,img,p0,ang,L,bend,lmax,cols,vein,seed,flip=1):
    """a Ceylon tea shoot: alternate leaves down a stem, two young leaves and the bud at the tip"""
    rng=np.random.default_rng(seed); sp=draw.arc(p0,ang,L,bend,n=6); n=len(sp); d=np.gradient(sp,axis=0)
    P.over(img,draw.ribbon(sp,lambda t:lmax*0.03*(1-0.5*t)+0.05),cols[0],1.0,0)
    side=flip
    for i,t in enumerate((0.2,0.42,0.62,0.8)):
        j=int(t*(n-1)); da=math.degrees(math.atan2(d[j][1],d[j][0])); Ls=lmax*(1-0.4*t)*rng.uniform(0.85,1.05)
        c=cols[(i+seed)%len(cols)]; flatleaf(P,img,tuple(sp[j]),da+side*rng.uniform(38,58),Ls,Ls*0.3,side*0.25,c,mix(c,'#0E2A22',0.3),vein,rng); side=-side
    da=math.degrees(math.atan2(d[-1][1],d[-1][0]))
    for sg,f in ((1,0.36),(-1,0.3)):
        Ls=lmax*f; c=cols[-1]; flatleaf(P,img,tuple(sp[-4]),da+sg*26,Ls,Ls*0.3,sg*0.3,c,mix(c,'#0E2A22',0.25),vein,rng)
    P.over(img,draw.bud(tuple(sp[-1]),da,lmax*0.3,lmax*0.07,0.08),mix(cols[-1],'#FFFFFF',0.35),1.0,0)
def vleaf(P,img,p0,ang,L,W,bend,col):
    """the vanilla vine's own leaf: long, fleshy, smooth-edged, a soft sheen down the middle"""
    poly=draw.leaf(p0,ang,L,W,bend); sp=draw.leaf(p0,ang,L,W,bend,spine=True)
    P.over(img,poly,col,1.0,0.03); P.shade(img,poly,LIGHT*W*0.25,mix(col,'#000000',0.35),0.6)
    P.over(img,draw.ribbon(sp[2:-3],lambda t:W*0.12*math.sin(math.pi*t)+0.03),mix(col,'#FFFFFF',0.25),0.5,0)
def art(k):
    p=CW[k]; W,H=B+FW+SW+B,FH+2*B; w,h=int(W*K),int(H*K)
    P=Paint(W,H,seed=3)
    img=np.ones((h,w,3),np.float32)*hx(p['paper'])
    x0=int((B+SPLIT)*K); img[:,x0:]=hx(p['band'])                       # the split: cream | teal, round the corner
    # the candles' move on the colour side: the name, huge and cropped, a step off the ground
    im=Image.fromarray(img.clip(0,255).astype(np.uint8)); dr=ImageDraw.Draw(im)
    fnt=ImageFont.truetype(R+'/fonts/instrument-serif.ttf',int(64*K))
    dr.text((int((B+FW+3)*K),int((B+FH-2)*K)),'Vanilla',font=fnt,fill=p['word'],anchor='ls')
    img=np.asarray(im).astype(np.float32)
    f=B+FW; L=p['leaves']
    vleaf(P,img,(B+SPLIT+4,B+92),-62,70,8.5,0.25,'#2A5240')                 # vine leaves, behind
    vleaf(P,img,(f+2,B+96),-118,64,7.5,-0.2,'#33604A')
    shoot(P,img,(f-3,B-4),134,56,0.3,25,L[1:],'#CFE0C2',3,1)               # Ceylon tea: one falling from the top corner,
    shoot(P,img,(B+SPLIT+10,B+97),-78,66,0.35,26,L,'#CFE0C2',5,1)          # one rising at the split,
    shoot(P,img,(f-4,B+97),-118,56,-0.25,24,L[1:],'#CFE0C2',8,-1)          # one at the corner,
    shoot(P,img,(f+SW-3,B+104),-100,44,0.25,21,L,'#CFE0C2',11,1)            # and one on the brew side, low
    paint_pod(P,img,(B+SPLIT-6,B+86),-17,86,2.3,0.12,0); paint_pod(P,img,(B+SPLIT-1,B+91),-24,78,2.0,0.08,0)
    paint_vbud(P,img,(f-24,B+20),-60,7.5); paint_vbud(P,img,(B+SPLIT+20,B+30),200,6.5)
    paint_flower(P,img,(f-44,B+46),38,2.75)
    img=grain(img,17); out=img.clip(0,255).astype(np.uint8)
    Image.fromarray(out[:,:int((FW+2*B)*K)]).save(O+f'{k}2-front.jpg',quality=94)
    Image.fromarray(out[:,int((FW+B)*K):]).save(O+f'{k}2-side.jpg',quality=94)
    for nm,(fw,fh) in {'lid':(FW,LH),'back':(FW,FH)}.items():
        a=np.ones((int((fh+2*B)*K),int((fw+2*B)*K),3),np.float32)*hx(p['paper']); a=grain(a,19)
        Image.fromarray(a.clip(0,255).astype(np.uint8)).save(O+f'{k}2-{nm}.jpg',quality=94)
def front(k):
    p=CW[k]; c=p['ink']; x=12; o=[]
    o.append(logo(x+9,16.5,18,c)); o.append(rule(x+21.5,9.5,x+21.5,23.5,c,0.2,0.45)); o.append(lion(x+25,10.6,17,c))
    o.append(f'<text x="{x-0.8}" y="47" font-family="ISR" font-size="23"><tspan fill="url(#foil)">Vanilla</tspan></text>')
    o.append(txt('Tea',x-0.8,66,23,c,'IS'))
    o.append(caps('CEYLON BLACK TEA WITH NATURAL VANILLA',x,76.4,1.95,c,tr=0.12))
    o.append(txt('Made with vanilla grown on our own farms.',x,81.2,4.2,c,'IS'))
    o.append(rule(SPLIT-6,8,SPLIT-6,FH-8,c,0.15,0.0))
    o.append(caps('NET WT. 50 g',SPLIT-9,16.4,3.6,c,'end',0)); o.append(caps('25 TEA BAGS',SPLIT-9,21.6,1.7,c,'end',0.2))
    return face(f'{k}2-F',FW,FH,f'{k}2-front.jpg',o)
def side(k):
    p=CW[k]; c=p['lt']; x=10; r=SW-10; o=[]
    o.append(txt('How to brew',x,15,6.4,c,'IS')); o.append(rule(x,18.6,r,18.6,c,0.2,0.6))
    for i,(nn,hd,t) in enumerate([('01','150 ML','One tea bag in freshly boiled water.'),('02','5 MINUTES','Steep, then lift the bag out.'),('03','OVER ICE','Let it cool and pour over ice.')]):
        y=25+i*8.6
        o.append(txt(nn,x,y+2.4,4.4,c,'ISR')); o.append(caps(hd,x+9,y,1.9,c,tr=0.16)); o.append(txt(t,x+9,y+3.4,2.1,c,'G'))
    o.append(rule(x,49.5,r,49.5,c,0.2,0.6))
    o.append(caps('25 TEA BAGS · 2 G EACH · NET WT. 50 g',x,53.6,1.6,c,tr=0.2))
    return face(f'{k}2-S',SW,FH,f'{k}2-side.jpg',o)
def lid(k):
    p=CW[k]; c=p['ink']; o=[]; cx=FW/2
    o.append(logo(cx,LH/2-6,22,c)); o.append(caps('AUTHENTIC CEYLON VANILLA TEA',cx,LH/2+12,2.2,c,'middle',0.3))
    o.append(rule(cx-40,LH/2+15.5,cx+40,LH/2+15.5,c,0.2,0.45)); o.append(caps('SAVOUR THE CALM',cx,LH/2+20,1.6,p['deep'],'middle',0.35))
    return face(f'{k}2-L',FW,LH,f'{k}2-lid.jpg',o)
if __name__=='__main__':
    man=[]
    for k in CW: art(k); man+=[front(k),side(k),lid(k)]
    json.dump(man,open(O+'faces2.json','w')); print('ok')
