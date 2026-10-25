# Vanilla Tea cartons, 25-bag (long) and 12-bag (cube), one system: the cream sheet torn over a deep teal band at the
# golden section, the candles' giant cropped serif on the brew side, the soap's grid and caps on the cream, the flat
# crisp botanical (vanilla flower, buds, cured pods, Ceylon tea shoots), and, faint on the cream, Ceylon hill country:
# blue mountain ranges with peaks, the near slope planted in rows of tea bushes, a few tall shade trees standing in it.
import sys, json, math, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
S='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/'
sys.path.insert(0,S+'teasoap'); sys.path.insert(0,S+'teaart')
import build as b
from build import logo, txt, caps, rule, lion, face, grain, hx, B
import build2 as b2
from build2 import shoot, vleaf, laid_on, CW, K
from foliage2 import paint_flower, paint_pod, paint_vbud, Paint
R='/home/user/PersonalEventPlanner305App/vanilla-shop'
O=b.O; GOLD=1.618
BOX={'long':dict(FW=175.9,FH=85.0,SW=85.1,LH=85.1,bags=25,net=50),
     'cube':dict(FW=87.6,FH=85.0,SW=84.6,LH=84.6,bags=12,net=24)}
for v in BOX.values(): v['SPLIT']=round(v['FW']/GOLD,1)

def washi(img,p,split,seed=21):
    """the cream sheet's edge is torn, not cut: a wandering deckle, fibres standing out of it, a faint shadow"""
    h,w=img.shape[:2]; rng=np.random.default_rng(seed)
    def wander(sig,amp): v=cv2.GaussianBlur(rng.normal(0,1,(h,1)).astype(np.float32),(1,0),sigmaX=0.1,sigmaY=sig*K)[:,0]; return v/(v.std()+1e-6)*amp
    xb=(B+split)+wander(7,1.6)+wander(1.2,0.45)+wander(0.25,0.12)
    d=np.arange(w,dtype=np.float32)[None,:]/K-xb[:,None]
    fib=cv2.GaussianBlur(rng.normal(0,1,(h,w)).astype(np.float32),(0,0),sigmaX=0.12*K,sigmaY=0.03*K); fib/=fib.std()
    fringe=np.clip((fib*0.5+0.55)-d/1.1,0,1)*(d>0)*(d<1.4)
    shadow=np.clip(1-(d-0.15)/1.6,0,1)*(d>0)*0.16
    out=img*(1-shadow[...,None]); a=np.clip((d<=0)*1.0+fringe*0.9,0,1)
    col=np.where((d>-0.5)[...,None],hx('#FBF8EF'),hx(p['paper']))
    return out*(1-a[...,None])+col*a[...,None], a

def ridge(xs,base,peaks,seed,jag=0.5):
    """a mountain line: peaks with steeper, uneven flanks and a little rocky noise, not a smooth wave"""
    r=np.full(xs.shape,base,np.float32)
    for (c,hgt,hw,skew) in peaks:
        u=(xs-c)/(hw*np.where(xs<c,1-skew,1+skew)); r=np.minimum(r,base-hgt*np.clip(1-np.abs(u),0,1)**1.35)
    n=cv2.GaussianBlur(np.random.default_rng(seed).normal(0,1,(1,xs.size)).astype(np.float32),(0,1),sigmaX=0.8*K,sigmaY=0.1)[0]
    return r+n/(n.std()+1e-6)*jag
def estate(h,w,x0,spec,seed=5):
    """Ceylon hill country, as ink coverage 0..1: far ranges as flat pale tone; the near slope in contour rows of
    tea bushes (small rounded dots), the rows stepping down the hill; slender shade trees standing among them"""
    xs=np.arange(w,dtype=np.float32)/K+x0; yy=np.arange(h,dtype=np.float32)[:,None]/K
    cov=np.zeros((h,w),np.float32)
    for i,(base,peaks,tone) in enumerate(spec['far']):                      # back to front, each covering the last
        r=ridge(xs,base,peaks,seed+i,0.45); m=(yy>=r[None,:]); cov[m]=tone
    base,peaks,tone=spec['near']; r=ridge(xs,base,peaks,seed+9,0.2); m=(yy>=r[None,:]); cov[m]=tone
    ss=3; im=Image.new('L',(w*ss,h*ss),0); dr=ImageDraw.Draw(im)
    gap,dot=spec.get('rows',(1.7,0.42))
    for k in range(1,60):                                                    # the rows: parallel to the crest, stepping down
        off=k*gap*(1+0.012*k); ph=(k*0.37)%1
        for j in range(0,w,max(1,int(dot*2.1*K))):
            jj=min(w-1,j+int(ph*dot*K)); y=(r[jj]+off)*K*ss; x=jj*ss; rr=dot*K*ss*0.5
            dr.ellipse((x-rr*1.25,y-rr*0.85,x+rr*1.25,y+rr*0.85),fill=255)
    for (tx,th) in spec['trees']:                                            # shade trees, tall and thin, as on every estate
        j=int((tx-x0)*K); y0=r[min(w-1,max(0,j))]+th*0.35; X=tx-x0
        dr.line([(X*K*ss,y0*K*ss),(X*K*ss,(y0-th)*K*ss)],fill=255,width=max(1,int(0.16*K*ss)))
        for q in range(5):
            cy=y0-th+q*th*0.13; cw=th*(0.1+0.04*(q%2));
            dr.ellipse(((X-cw)*K*ss,(cy-0.35)*K*ss,(X+cw)*K*ss,(cy+0.35)*K*ss),fill=255)
    lines=np.asarray(im.resize((w,h),Image.BOX)).astype(np.float32)/255
    cov=np.maximum(cov,lines*m*spec.get('ink',0.3))
    return cov

def art(box,k='teal'):
    d=BOX[box]; FW,FH,SW,LH,SPLIT=d['FW'],d['FH'],d['SW'],d['LH'],d['SPLIT']
    p=CW[k]; W,H=B+FW+SW+B,FH+2*B; w,h=int(W*K),int(H*K); P=Paint(W,H,seed=3); f=B+FW; L=p['leaves']
    img=np.ones((h,w,3),np.float32)*hx(p['band'])
    im=Image.fromarray(img.clip(0,255).astype(np.uint8)); dr=ImageDraw.Draw(im)
    fnt=ImageFont.truetype(R+'/fonts/instrument-serif.ttf',int((64 if box=='long' else 60)*K))
    dr.text((int((f+3)*K),int((B+FH-2)*K)),'Vanilla',font=fnt,fill=p['word'],anchor='ls')
    img=np.asarray(im).astype(np.float32)
    if box=='long':
        vleaf(P,img,(B+SPLIT+4,B+92),-62,70,8.5,0.25,'#2A5240'); vleaf(P,img,(f+2,B+96),-118,64,7.5,-0.2,'#33604A')
        shoot(P,img,(f-3,B-4),134,56,0.3,25,L[1:],'#CFE0C2',3,1); shoot(P,img,(B+SPLIT+10,B+97),-78,66,0.35,26,L,'#CFE0C2',5,1)
        shoot(P,img,(f-4,B+97),-118,56,-0.25,24,L[1:],'#CFE0C2',8,-1); shoot(P,img,(f+SW-3,B+104),-100,44,0.25,21,L,'#CFE0C2',11,1)
        pods=[((B+SPLIT-14,B+86),-17,86,2.3,0.12,0),((B+SPLIT-9,B+91),-24,78,2.0,0.08,0)]
        buds=[((f-20,B+20),-60,7.5),((B+SPLIT+12,B+30),200,6.5)]; fl=((f-37,B+46),38,2.6)
    else:
        vleaf(P,img,(B+SPLIT+3,B+92),-64,52,6.5,0.25,'#2A5240'); vleaf(P,img,(f+2,B+96),-118,48,5.8,-0.2,'#33604A')
        shoot(P,img,(f-2,B-4),130,42,0.3,19,L[1:],'#CFE0C2',3,1); shoot(P,img,(B+SPLIT+6,B+97),-80,50,0.35,19,L,'#CFE0C2',5,1)
        shoot(P,img,(f-3,B+97),-116,42,-0.25,18,L[1:],'#CFE0C2',8,-1); shoot(P,img,(f+SW-3,B+104),-100,36,0.25,16,L,'#CFE0C2',11,1)
        pods=[((B+SPLIT-3,B+87),-19,40,1.6,0.12,0),((B+SPLIT,B+91),-27,36,1.4,0.08,0)]
        buds=[((f-12,B+18),-60,5.5),((B+SPLIT+8,B+28),200,5)]; fl=((f-20,B+52),38,1.6)
    img,cream=washi(img,p,SPLIT)
    if box=='long':      # the hill country on the cream, to the right of the name, running under the tear
        es=estate(h,w,-B,dict(far=[(62,[(62,18,14,0.2),(84,30,13,-0.15),(110,22,16,0.1)],0.05),
                                   (70,[(56,10,16,0.0),(98,17,15,0.25),(124,12,12,0.0)],0.08)],
                              near=(84,[(92,22,20,0.2)],0.035),trees=[(84,7.0),(94,8.5),(103,6.5)],ink=0.34))
        xx=np.arange(w,dtype=np.float32)[None,:]/K-B; fx=np.clip((xx-46)/30,0,1); fx=fx*fx*(3-2*fx)
        A=es*fx*cream; img=img*(1-A[...,None])+hx(p['band'])*A[...,None]
    img=laid_on(img,lambda c:([paint_pod(P,c,*q) for q in pods],[paint_vbud(P,c,*q) for q in buds],paint_flower(P,c,*fl)))
    img=grain(img,17); out=img.clip(0,255).astype(np.uint8)
    Image.fromarray(out[:,:int((FW+2*B)*K)]).save(O+f'{box}3-front.jpg',quality=94)
    Image.fromarray(out[:,int((FW+B)*K):]).save(O+f'{box}3-side.jpg',quality=94)
    a=np.ones((int((LH+2*B)*K),int((FW+2*B)*K),3),np.float32)*hx(p['paper']); hh2,ww2=a.shape[:2]
    sc=FW/175.9
    es=estate(hh2,ww2,-B,dict(far=[(LH-6,[(FW*0.2,16*sc+4,22*sc+6,0.2),(FW*0.78,20*sc+5,20*sc+6,-0.2)],0.045),
                                    (LH-2,[(FW*0.5,13*sc+3,24*sc+6,0.1),(FW*0.95,10*sc+3,14*sc+4,0)],0.07)],
                               near=(LH+6,[(FW*0.3,10*sc+3,30*sc+8,0.2),(FW*0.82,9*sc+3,24*sc+6,-0.2)],0.03),
                               trees=[(FW*0.22,6.5),(FW*0.36,7.5),(FW*0.8,6.8)],ink=0.28),seed=8)
    a=a*(1-es[...,None])+hx(p['band'])*es[...,None]; a=grain(a,19)
    Image.fromarray(a.clip(0,255).astype(np.uint8)).save(O+f'{box}3-lid.jpg',quality=94)

def front(box,k='teal'):
    d=BOX[box]; FW,FH,SPLIT=d['FW'],d['FH'],d['SPLIT']; p=CW[k]; c=p['ink']; o=[]
    if box=='long':
        x=12
        o.append(logo(x+9,16.5,18,c)); o.append(rule(x+21.5,9.5,x+21.5,23.5,c,0.2,0.45)); o.append(lion(x+25,10.6,17,c))
        o.append(f'<text x="{x-0.8}" y="47" font-family="ISR" font-size="23"><tspan fill="url(#foil)">Vanilla</tspan></text>')
        o.append(txt('Tea',x-0.8,66,23,c,'IS'))
        o.append(caps('CEYLON BLACK TEA WITH NATURAL VANILLA',x,76.4,1.95,c,tr=0.12))
        o.append(txt('Made with vanilla grown on our own farms.',x,81.2,4.2,c,'IS'))
        o.append(caps(f'NET WT. {d["net"]} g',SPLIT-9,16.4,3.6,c,'end',0)); o.append(caps(f'{d["bags"]} TEA BAGS',SPLIT-9,21.6,1.7,c,'end',0.2))
    else:
        x=8
        o.append(logo(x+7,13.5,14,c)); o.append(rule(x+16.5,8,x+16.5,19,c,0.2,0.45)); o.append(lion(x+19.5,8.6,13,c))
        o.append(f'<text x="{x-0.6}" y="38" font-family="ISR" font-size="17"><tspan fill="url(#foil)">Vanilla</tspan></text>')
        o.append(txt('Tea',x-0.6,52.5,17,c,'IS'))
        o.append(caps('CEYLON BLACK TEA',x,61.5,1.7,c,tr=0.12)); o.append(caps('WITH NATURAL VANILLA',x,64.6,1.7,c,tr=0.12))
        o.append(txt('Made with vanilla grown',x,70.6,3.1,c,'IS')); o.append(txt('on our own farms.',x,74.2,3.1,c,'IS'))
        o.append(rule(x,77.4,SPLIT-6,77.4,c,0.15,0.4))
        o.append(caps(f'NET WT. {d["net"]} g',x,81.6,2.5,c,tr=0.02)); o.append(caps(f'{d["bags"]} TEA BAGS',SPLIT-6,81.6,1.5,c,'end',0.2))
    return face(f'{box}3-F',FW,FH,f'{box}3-front.jpg',o)
def side(box,k='teal'):
    d=BOX[box]; SW,FH=d['SW'],d['FH']; p=CW[k]; c=p['lt']; x=10; r=SW-10; o=[]
    o.append(txt('How to brew',x,15,6.4,c,'IS')); o.append(rule(x,18.6,r,18.6,c,0.2,0.6))
    for i,(nn,hd,t) in enumerate([('01','150 ML','One tea bag in freshly boiled water.'),('02','5 MINUTES','Steep, then lift the bag out.'),('03','OVER ICE','Let it cool and pour over ice.')]):
        y=25+i*8.6
        o.append(txt(nn,x,y+2.4,4.4,c,'ISR')); o.append(caps(hd,x+9,y,1.9,c,tr=0.16)); o.append(txt(t,x+9,y+3.4,2.1,c,'G'))
    o.append(rule(x,49.5,r,49.5,c,0.2,0.6))
    o.append(caps(f'{d["bags"]} TEA BAGS · 2 G EACH · NET WT. {d["net"]} g',x,53.6,1.6,c,tr=0.2))
    return face(f'{box}3-S',SW,FH,f'{box}3-side.jpg',o)
def lid(box,k='teal'):
    d=BOX[box]; FW,LH=d['FW'],d['LH']; p=CW[k]; c=p['ink']; o=[]; cx=FW/2; s=1 if box=='long' else 0.8
    o.append(logo(cx,LH/2-12,22*s,c)); o.append(caps('AUTHENTIC CEYLON VANILLA TEA',cx,LH/2+5,2.2*s,c,'middle',0.3))
    o.append(rule(cx-40*s,LH/2+8.5,cx+40*s,LH/2+8.5,c,0.2,0.45)); o.append(caps('SAVOUR THE CALM',cx,LH/2+13,1.6*s,p['deep'],'middle',0.35))
    return face(f'{box}3-L',FW,LH,f'{box}3-lid.jpg',o)
if __name__=='__main__':
    man=[]
    for box in (sys.argv[1:] or BOX): art(box); man+=[front(box),side(box),lid(box)]
    json.dump(man,open(O+'faces3.json','w')); print('ok')
