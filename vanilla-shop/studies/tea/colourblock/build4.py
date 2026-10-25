# Vanilla Tea cartons, round 4: depth in the hill country from the rows themselves (far ranges in fine, sparse dots,
# the near slope in large ones); the brew side's wordmark set full-width in the system's wide caps; the 12-bag's
# flower larger and its top shoot reaching over the tear; NET WT. in the signature row; a teal lid with the botanical.
import sys, json, math, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
S='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/'
sys.path.insert(0,S+'teasoap'); sys.path.insert(0,S+'teaart')
import build as b
from build import logo, txt, caps, rule, lion, face, grain, hx, B
from build2 import shoot, vleaf, laid_on, CW, K
from build3 import BOX, washi, ridge
from foliage2 import paint_flower, paint_pod, paint_vbud, Paint
R='/home/user/PersonalEventPlanner305App/vanilla-shop'; O=b.O

def estate(h,w,x0,ranges,trees,seed=5):
    """Ceylon hill country as ink coverage: every range planted in contour rows of tea, the rows (and their bushes)
    shrinking with distance, so the dots themselves carry the depth. ranges back to front:
    (base, peaks, fill, row gap, bush size, ink)"""
    xs=np.arange(w,dtype=np.float32)/K+x0; yy=np.arange(h,dtype=np.float32)[:,None]/K
    owner=np.full((h,w),-1,np.int16); curves=[]
    for i,(base,peaks,*_) in enumerate(ranges):
        r=ridge(xs,base,peaks,seed+i,0.45 if i<len(ranges)-1 else 0.2); curves.append(r); owner[yy>=r[None,:]]=i
    cov=np.zeros((h,w),np.float32); ss=3
    for i,(base,peaks,fill,gap,dot,ink) in enumerate(ranges):
        mine=(owner==i); r=curves[i]
        im=Image.new('L',(w*ss,h*ss),0); dr=ImageDraw.Draw(im)
        for k in range(1,90):
            off=k*gap*(1+0.012*k); ph=(k*0.37)%1; step=max(1,int(dot*2.2*K))
            for j in range(0,w,step):
                jj=min(w-1,j+int(ph*step)); y=(r[jj]+off)*K*ss; x=jj*ss; rr=dot*K*ss*0.5
                dr.ellipse((x-rr*1.25,y-rr*0.85,x+rr*1.25,y+rr*0.85),fill=255)
        if i==len(ranges)-1:
            for (tx,th) in trees:                                            # shade trees on the near slope
                j=int((tx-x0)*K); y0=r[min(w-1,max(0,j))]+th*0.4; X=tx-x0
                dr.line([(X*K*ss,y0*K*ss),(X*K*ss,(y0-th)*K*ss)],fill=255,width=max(1,int(0.2*K*ss)))
                for q in range(5):
                    cy=y0-th+q*th*0.13; cw=th*(0.11+0.05*(q%2))
                    dr.ellipse(((X-cw)*K*ss,(cy-0.4)*K*ss,(X+cw)*K*ss,(cy+0.4)*K*ss),fill=255)
        dots=np.asarray(im.resize((w,h),Image.BOX)).astype(np.float32)/255
        cov=np.where(mine,np.maximum(fill,dots*ink),cov)
    return cov

def wordmark(img,text,x0,x1,base,col,wide=True):
    """the brew side's name: the system's wide caps, set to exactly the column's width, no crop"""
    f=R+'/fonts/archivo-expanded-medium.ttf'; tw=(x1-x0)*K
    fnt=ImageFont.truetype(f,400); bb=fnt.getbbox(text); sz=int(400*tw/(bb[2]-bb[0])); fnt=ImageFont.truetype(f,sz); bb=fnt.getbbox(text)
    im=Image.fromarray(img.clip(0,255).astype(np.uint8)); ImageDraw.Draw(im).text((x0*K-bb[0],base*K),text,font=fnt,fill=col,anchor='ls')
    return np.asarray(im).astype(np.float32)

def art(box,k='teal'):
    d=BOX[box]; FW,FH,SW,LH,SPLIT=d['FW'],d['FH'],d['SW'],d['LH'],d['SPLIT']
    p=CW[k]; W,H=B+FW+SW+B,FH+2*B; w,h=int(W*K),int(H*K); P=Paint(W,H,seed=3); f=B+FW; L=p['leaves']
    img=np.ones((h,w,3),np.float32)*hx(p['band'])
    img=wordmark(img,'VANILLA',f+10,f+SW-10,B+FH-7.5,p['word'])
    if box=='long':
        vleaf(P,img,(B+SPLIT+4,B+92),-62,70,8.5,0.25,'#2A5240'); vleaf(P,img,(f+2,B+96),-118,64,7.5,-0.2,'#33604A')
        shoot(P,img,(f-3,B-4),134,56,0.3,25,L[1:],'#CFE0C2',3,1); shoot(P,img,(B+SPLIT+10,B+97),-78,66,0.35,26,L,'#CFE0C2',5,1)
        shoot(P,img,(f-4,B+97),-118,56,-0.25,24,L[1:],'#CFE0C2',8,-1); shoot(P,img,(f+SW-3,B+104),-100,44,0.25,21,L,'#CFE0C2',11,1)
        over=lambda c:([paint_pod(P,c,*q) for q in [((B+SPLIT-14,B+86),-17,76,2.3,0.12,0),((B+SPLIT-9,B+91),-24,68,2.0,0.08,0)]],
                       [paint_vbud(P,c,*q) for q in [((f-20,B+20),-60,7.5),((B+SPLIT+12,B+30),200,6.5)]],paint_flower(P,c,(f-37,B+46),38,2.6))
    else:
        vleaf(P,img,(B+SPLIT+3,B+92),-64,52,6.5,0.25,'#2A5240'); vleaf(P,img,(f+2,B+96),-118,48,5.8,-0.2,'#33604A')
        shoot(P,img,(B+SPLIT+6,B+97),-80,50,0.35,19,L,'#CFE0C2',5,1)
        shoot(P,img,(f-3,B+97),-116,42,-0.25,18,L[1:],'#CFE0C2',8,-1); shoot(P,img,(f+SW-3,B+104),-100,36,0.25,16,L,'#CFE0C2',11,1)
        over=lambda c:(shoot(P,c,(f+6,B-3),158,52,0.35,19,L[1:],'#CFE0C2',3,1),                  # the top shoot reaches over the tear
                       [paint_pod(P,c,*q) for q in [((B+SPLIT-6,B+87),-19,34,1.6,0.12,0),((B+SPLIT-3,B+91),-27,30,1.4,0.08,0)]],
                       [paint_vbud(P,c,*q) for q in [((f-10,B+24),-60,5.5)]],paint_flower(P,c,(f-27,B+56),38,1.85))
    img,cream=washi(img,p,SPLIT)
    if box=='long':      # the hill country on the cream, between the name and the tear
        es=estate(h,w,-B,[(60,[(62,18,14,0.2),(84,30,13,-0.15),(110,22,16,0.1)],0.02,0.95,0.24,0.26),
                          (69,[(56,10,16,0.0),(100,17,15,0.25),(124,12,12,0.0)],0.025,1.25,0.31,0.3),
                          (84,[(92,22,20,0.2)],0.03,1.75,0.42,0.36)],trees=[(84,7.0),(94,8.5),(103,6.5)])
        xx=np.arange(w,dtype=np.float32)[None,:]/K-B; fx=np.clip((xx-46)/30,0,1); fx=fx*fx*(3-2*fx)
        A=es*fx*cream; img=img*(1-A[...,None])+hx(p['band'])*A[...,None]
    img=laid_on(img,over)
    img=grain(img,17); out=img.clip(0,255).astype(np.uint8)
    Image.fromarray(out[:,:int((FW+2*B)*K)]).save(O+f'{box}4-front.jpg',quality=94)
    Image.fromarray(out[:,int((FW+B)*K):]).save(O+f'{box}4-side.jpg',quality=94)
    # the lid: the band carried over the top, the botanical coming in from two corners, the name kept clear
    LW,LHH=FW+2*B,LH+2*B; P2=Paint(LW,LHH,seed=4); a=np.ones((int(LHH*K),int(LW*K),3),np.float32)*hx(p['band'])
    if box=='long':
        vleaf(P2,a,(B+FW+6,B+LH-6),-160,60,7.5,0.2,'#2A5240'); vleaf(P2,a,(B-6,B+8),20,52,6.5,-0.2,'#33604A')
        shoot(P2,a,(B+FW+5,B+LH+3),-150,62,0.3,24,L,'#CFE0C2',6,1); shoot(P2,a,(B-5,B+LH-4),-28,46,-0.25,21,L[1:],'#CFE0C2',9,-1)
        lo=lambda c:(shoot(P2,c,(B-5,B-2),24,50,0.3,22,L[1:],'#CFE0C2',4,1),paint_vbud(P2,c,(B+FW-24,B+16),-120,7),
                     paint_flower(P2,c,(B+FW-28,B+LH-22),210,2.3),paint_pod(P2,c,(B+FW-70,B+LH+2),-8,60,2.0,0.1,0))
    else:
        vleaf(P2,a,(B+FW+5,B+LH-5),-160,44,6,0.2,'#2A5240')
        shoot(P2,a,(B+FW+4,B+LH+3),-145,46,0.3,18,L,'#CFE0C2',6,1); shoot(P2,a,(B-4,B+LH-3),-30,34,-0.25,16,L[1:],'#CFE0C2',9,-1)
        lo=lambda c:(shoot(P2,c,(B-4,B-2),30,38,0.3,17,L[1:],'#CFE0C2',4,1),paint_flower(P2,c,(B+FW-6,B+LH-4),210,1.25))
    a=laid_on(a,lo); a=grain(a,19)
    Image.fromarray(a.clip(0,255).astype(np.uint8)).save(O+f'{box}4-lid.jpg',quality=94)

def front(box,k='teal'):
    d=BOX[box]; FW,FH,SPLIT=d['FW'],d['FH'],d['SPLIT']; p=CW[k]; c=p['ink']; o=[]
    if box=='long':
        x=12
        o.append(logo(x+9,16.5,18,c)); o.append(rule(x+21.5,9.5,x+21.5,23.5,c,0.2,0.45)); o.append(lion(x+25,10.6,17,c))
        o.append(rule(x+46,9.5,x+46,23.5,c,0.2,0.45))                     # the signature row's third cell: what's in the box
        o.append(caps(f'NET WT. {d["net"]} g',x+50,15.6,3.1,c,tr=0.02)); o.append(caps(f'{d["bags"]} TEA BAGS · 2 G EACH',x+50,21.4,1.6,c,tr=0.2))
        o.append(f'<text x="{x-0.8}" y="47" font-family="ISR" font-size="23"><tspan fill="url(#foil)">Vanilla</tspan></text>')
        o.append(txt('Tea',x-0.8,66,23,c,'IS'))
        o.append(caps('CEYLON BLACK TEA WITH NATURAL VANILLA',x,76.4,1.95,c,tr=0.12))
        o.append(txt('Made with vanilla grown on our own farms.',x,81.2,4.2,c,'IS'))
    else:
        x=8
        o.append(logo(x+7,13.5,14,c)); o.append(rule(x+16.5,8,x+16.5,19,c,0.2,0.45)); o.append(lion(x+19.5,8.6,13,c))
        o.append(f'<text x="{x-0.6}" y="38" font-family="ISR" font-size="17"><tspan fill="url(#foil)">Vanilla</tspan></text>')
        o.append(txt('Tea',x-0.6,52.5,17,c,'IS'))
        o.append(caps('CEYLON BLACK TEA',x,61.5,1.7,c,tr=0.12)); o.append(caps('WITH NATURAL VANILLA',x,64.6,1.7,c,tr=0.12))
        o.append(txt('Made with vanilla grown',x,70.6,3.1,c,'IS')); o.append(txt('on our own farms.',x,74.2,3.1,c,'IS'))
        o.append(rule(x,77.4,SPLIT-6,77.4,c,0.15,0.4))
        o.append(caps(f'NET WT. {d["net"]} g',x,81.6,2.5,c,tr=0.02)); o.append(caps(f'{d["bags"]} TEA BAGS',SPLIT-6,81.6,1.5,c,'end',0.2))
    return face(f'{box}4-F',FW,FH,f'{box}4-front.jpg',o)
def side(box,k='teal'):
    d=BOX[box]; SW,FH=d['SW'],d['FH']; p=CW[k]; c=p['lt']; x=10; r=SW-10; o=[]
    o.append(txt('How to brew',x,15,6.4,c,'IS')); o.append(rule(x,18.6,r,18.6,c,0.2,0.6))
    for i,(nn,hd,t) in enumerate([('01','150 ML','One tea bag in freshly boiled water.'),('02','5 MINUTES','Steep, then lift the bag out.'),('03','OVER ICE','Let it cool and pour over ice.')]):
        y=25+i*8.6
        o.append(txt(nn,x,y+2.4,4.4,c,'ISR')); o.append(caps(hd,x+9,y,1.9,c,tr=0.16)); o.append(txt(t,x+9,y+3.4,2.1,c,'G'))
    o.append(rule(x,49.5,r,49.5,c,0.2,0.6))
    o.append(caps(f'{d["bags"]} TEA BAGS · 2 G EACH · NET WT. {d["net"]} g',x,53.6,1.6,c,tr=0.2))
    return face(f'{box}4-S',SW,FH,f'{box}4-side.jpg',o)
def lid(box,k='teal'):
    d=BOX[box]; FW,LH=d['FW'],d['LH']; p=CW[k]; c=p['lt']; o=[]; cx=FW/2; s=1 if box=='long' else 0.8
    o.append(logo(cx,LH/2-10,22*s,c)); o.append(caps('AUTHENTIC CEYLON VANILLA TEA',cx,LH/2+7,2.2*s,c,'middle',0.3))
    o.append(rule(cx-38*s,LH/2+10.5,cx+38*s,LH/2+10.5,c,0.2,0.5)); o.append(caps('SAVOUR THE CALM',cx,LH/2+15,1.6*s,c,'middle',0.35))
    return face(f'{box}4-L',FW,LH,f'{box}4-lid.jpg',o)
if __name__=='__main__':
    man=[]
    for box in (sys.argv[1:] or BOX): art(box); man+=[front(box),side(box),lid(box)]
    json.dump(man,open(O+'faces4.json','w')); print('ok')
