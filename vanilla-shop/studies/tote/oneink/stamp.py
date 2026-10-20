# The tote stamp in one ink: an engraved Ceylon pictorial stamp, the vanilla vine breaking out of it.
# Art 270 x 337 mm. Everything is drawn here; nothing is generated.
import math, sys, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
from draw import cr, arc
from engrave import Form, Plate, paste, MIN_LINE, MIN_GAP
import spray
F='/home/user/PersonalEventPlanner305App/vanilla-shop/fonts/'
W,H=270,337
K=int(sys.argv[1]) if len(sys.argv)>1 else 16
# stamp geometry (mm)
PX0,PY0,PX1,PY1=14,12,232,326           # paper edge, at the perforations
FX0,FY0,FX1,FY1=23,21,223,317           # outer edge of the frame
WX0,WY0,WX1,WY1=31,64,215,278           # picture window
pl=Plate(W,H,K)
def rect(x0,y0,x1,y1): return np.array([[x0,y0],[x1,y0],[x1,y1],[x0,y1]],float)
def text(t,x,y,size,font,anchor='mm',ink=True,rotate=0,track=0):
    """set type straight into the plate: ink=True prints it, False knocks it out of a solid"""
    f=ImageFont.truetype(font if font.startswith('Noto') else F+font,int(size*K))
    if track:
        chars=list(t); ws=[f.getlength(c) for c in chars]; tw=sum(ws)+track*K*(len(chars)-1)
        im=Image.new('L',(int(tw+4*K),int(size*K*1.6)),0); d=ImageDraw.Draw(im); xx=2*K
        for c,w_ in zip(chars,ws): d.text((xx,im.size[1]/2),c,font=f,fill=255,anchor='lm'); xx+=w_+track*K
    else:
        bb=f.getbbox(t,anchor='lm'); im=Image.new('L',(int(bb[2]-bb[0]+4*K),int(size*K*1.8)),0)
        ImageDraw.Draw(im).text((2*K-bb[0],im.size[1]/2),t,font=f,fill=255,anchor='lm')
    if rotate: im=im.rotate(rotate,expand=True)
    a=np.asarray(im)>127; ys,xs=np.nonzero(a); a=a[ys.min():ys.max()+1,xs.min():xs.max()+1]
    h,w=a.shape; cx,cy=int(x*K),int(y*K)
    ox={'l':0,'m':w//2,'r':w}[anchor[0]]; oy={'t':0,'m':h//2,'b':h}[anchor[1]]
    reg=pl.ink[cy-oy:cy-oy+h,cx-ox:cx-ox+w]
    if ink: reg|=a
    else: reg&=~a
    return w/K,h/K
# ---------------------------------------------------------------- the picture: a hill-country vanilla garden
yy,xx=np.mgrid[0:pl.ink.shape[0],0:pl.ink.shape[1]].astype(np.float32)/K
win=(xx>WX0+14)&(xx<WX1)&(yy>WY0)&(yy<WY1)
def lines_h(region,pitch,tone_fn,phase=0.0,wave=None):
    """horizontal engraved lines over a region; tone_fn(x,y) sets the line width"""
    yv=yy if wave is None else yy-wave(xx)
    ph=np.mod((yv+phase)/pitch,1.0)-0.5; t=np.clip(tone_fn(xx,yy),0,1)
    lw=np.clip(t*pitch*1.05,0,pitch-MIN_GAP); lw=np.where(lw<MIN_LINE*0.8,0,np.maximum(lw,MIN_LINE))
    return region&(np.abs(ph)*pitch<lw/2)
def ridge(x,base,amps):
    y=np.full_like(x,base)
    for a,f,p in amps: y+=a*np.sin(x/f+p)
    return y
def lines_field(region,pitch,phase,tone):
    ph=np.mod(phase/pitch,1.0)-0.5; t=np.clip(tone,0,1)
    lw=np.clip(t*pitch*1.05,0,pitch-MIN_GAP); lw=np.where(lw<MIN_LINE*0.8,0,np.maximum(lw,MIN_LINE))
    return region&(np.abs(ph)*pitch<lw/2)
LS_R=WX0+13
pic=win.copy()
VX,VY=104,181                                     # vanishing point, on the horizon
# sky: level lines, darker towards the top, with long low clouds left as bare paper
sky=pic&(yy<VY+2)
clouds=np.zeros_like(sky)
for cx,cy,rx,ry in [(80,98,30,2.6),(118,104,22,1.8),(150,92,26,2.2),(66,124,18,1.6),(138,132,30,2.4),(98,146,16,1.4)]:
    clouds|=((xx-cx)/rx)**2+((yy-cy)/ry)**2<1
pl.ink|=lines_field(sky&~clouds,0.9,yy,0.66-0.52*np.clip((yy-WY0)/(VY-WY0),0,1)**0.7)
# hills: two ranges; lines follow each ridge at the crest and flatten out lower down; slopes facing left catch the light
def ridge(x,base,amps):
    y=np.full_like(x,base)
    for a_,f,p in amps: y=y+a_*np.sin(x/f+p)
    return y
for base,amps,tone in [(160,[(8,24,0.4),(3.5,10,1.6),(1.2,4,0.2)],0.3),(174,[(6,19,2.3),(3,8,0.5),(1,3.3,1.0)],0.5)]:
    top=ridge(xx,base,amps); reg=pic&(yy>=top)&(yy<VY+2)
    pl.ink&=~reg
    dx=np.gradient(ridge(xx[0],base,amps))[None,:]*K
    phase=yy-(top-base)*np.exp(-np.clip(yy-top,0,None)/9)
    pl.ink|=lines_field(reg,0.8,phase,tone+0.32*np.clip(dx,-1,1)+0.12*np.clip((yy-top)/10,0,1))
    pl.ink|=reg&(yy<top+0.45)
# the garden floor: furrows running to the vanishing point, fading out before the horizon
gr=pic&(yy>=VY+2)
pl.ink&=~gr
dep=np.clip((yy-VY)/(WY1-VY),0,1)
pl.ink|=lines_field(gr,1.3,(xx-VX)/np.maximum(yy-VY,0.5)*60,0.18+0.3*dep**0.8-0.2*(1-np.clip((yy-VY-2)/12,0,1)))
pl.ink|=pic&(yy>=VY+1.6)&(yy<VY+2.1)
# rows of lopped gliricidia posts in perspective, each with a vanilla vine looped over it
def post(x,y,h):
    s=h/44
    if h<7:
        pl.stroke([(x,y),(x,y-h)],max(0.3,0.9*s)); pl.stroke(arc((x,y-h),-90,h*0.25,0.0,3),0.3)
        for a_ in (-150,-120,-60,-30): pl.stroke(arc((x,y-h),a_,h*0.3,0.3,3),0.26)
        return
    trunk=Form(cr([(x,y),(x+0.8*s,y-h*0.45),(x-0.4*s,y-h*0.8),(x,y-h)],8),lambda t:(1.6-0.5*t)*s+0.1,tone=0.62,hatch='along',pitch=0.62,round_=1.0,hi=-0.4,outline=max(0.26,0.34*s),cross=0.8)
    pl.form(trunk)
    tip=np.array([x,y-h])
    for k,a_ in enumerate((-160,-138,-112,-90,-68,-42,-20)):
        sp=arc(tip,a_,(9+3*math.sin(k*2.1))*s,0.7*(1 if a_<-90 else -1),6); pl.stroke(sp,max(0.26,0.32*s))
        if s>0.35:
            for j in range(1,6):
                q=sp[int(j*(len(sp)-1)/6)]; d=sp[min(len(sp)-1,int(j*(len(sp)-1)/6)+2)]-q; n=np.array([-d[1],d[0]]); n/=np.linalg.norm(n)+1e-9
                for sg in (1,-1): pl.form(Form([q,q+n*sg*2.0*s+d*0.6],lambda t,s=s:0.55*s*math.sin(math.pi*min(t,0.999))+0.05,tone=0.3,outline=0.24,round_=0.3,cross=1))
    # vine: twining up the trunk, over the top, down in a swag
    up=np.array([(x+1.4*s*math.sin(k*1.3),y-h*k/10) for k in range(10)])
    sw=cr([(x+1*s,y-h*0.9),(x+5*s,y-h*1.04),(x+9*s,y-h*0.86),(x+10*s,y-h*0.55),(x+9*s,y-h*0.38)],10)
    pl.stroke(np.vstack([up,sw]),max(0.3,0.55*s))
    for j,tq in enumerate((0.2,0.45,0.7,0.95)):
        q=sw[int(tq*(len(sw)-1))]; ang=(-25 if j%2 else 205)
        pl.form(Form(arc(q,ang,8*s,0.4 if j%2 else -0.4,5),lambda t,s=s:2.0*s*math.sin(math.pi*min(t,0.999))**0.8+0.08,tone=0.58,pitch=0.6,round_=1.0,hi=-0.4,outline=0.26,cross=0.85))
    if s>0.45:
        q=sw[-1]
        for k in range(6): pl.form(Form(cr([q,q+np.array([(k-2.5)*0.8*s,7*s]),q+np.array([(k-2.5)*1.3*s,15*s])],6),lambda t,s=s:0.9*s*min(1,t*6)**0.6+0.05,tone=0.5,pitch=0.55,outline=0.26,round_=1.0,hi=-0.3,cross=0.8))
F_=150.0
for X in (-0.62,-0.18):
    for Z in (12,8,5.6,4.0,2.95,2.2):
        x=VX+F_*X/Z*1.0; y=VY+F_*0.62/Z
        if x<LS_R+6 or y>WY1+4: continue
        post(x,y,(y-VY)*1.55)
# ---------------------------------------------------------------- the stamp: paper edge, frame, lettering
def perforated(x0,y0,x1,y1,r=3.3,pitch=9.6):
    m=np.zeros(pl.ink.shape,np.uint8); cv2.fillPoly(m,[pl.px(rect(x0,y0,x1,y1))],1)
    for (a,b,c,d) in ((x0,y0,x1,y0),(x0,y1,x1,y1),(x0,y0,x0,y1),(x1,y0,x1,y1)):
        L=math.hypot(c-a,d-b); n=int(round(L/pitch)); st=L/n
        for i in range(n+1):
            cx,cy=a+(c-a)*i/n,b+(d-b)*i/n; cv2.circle(m,(int(cx*K),int(cy*K)),int(r*K),0,-1,cv2.LINE_AA)
    return m.astype(bool)
paper=perforated(PX0,PY0,PX1,PY1)
edge=paper^cv2.erode(paper.astype(np.uint8),cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(int(0.55*K)*2+1,)*2)).astype(bool)
# frame: solid ink between the frame edge and the window, the left strip and the caption box left as paper
frame=np.zeros(pl.ink.shape,bool); frame[int(FY0*K):int(FY1*K),int(FX0*K):int(FX1*K)]=True
frame[int(WY0*K):int(WY1*K),int(WX0*K):int(WX1*K)]=False
pl.ink|=frame
# a fine paper rule round the window and round the frame's outer edge
for (a,b,c,d,inset) in ((WX0,WY0,WX1,WY1,-1.6),(FX0,FY0,FX1,FY1,1.5)):
    pl.ink[cv2.rectangle(np.zeros(pl.ink.shape,np.uint8),(int((a+inset)*K),int((b+inset)*K)),(int((c-inset)*K),int((d-inset)*K)),1,max(1,int(0.5*K))).astype(bool)]=False
# the left strip inside the window
LS=(WX0+0.0,WX0+12.5)
pl.ink[int(WY0*K):int(WY1*K),int(LS[0]*K):int(LS[1]*K)]=False
pl.ink[int(WY0*K):int(WY1*K),int(LS[1]*K):int((LS[1]+0.5)*K)]=True
text('VANILLA PLANIFOLIA',(LS[0]+LS[1])/2,(WY0+WY1)/2,6.0,'gloock.ttf',rotate=90,track=0.9)
# top band: CEYLON with the Sinhala and Tamil names
w_,_=text('CEYLON',FX0+14,42.5,23,'gloock.ttf','lm',ink=False,track=1.0)
text('ලංකා',FX0+14+w_+7,36.5,9.5,'NotoSerifSinhala.ttf','lm',ink=False)
text('இலங்கை',FX0+14+w_+7,50.5,6.2,'NotoSerifTamil.ttf','lm',ink=False)
# bottom band: the value tablet and the caption box
TB=(FX0+6,WY1+5,FX0+40,FY1-6)
pl.ink[cv2.rectangle(np.zeros(pl.ink.shape,np.uint8),(int(TB[0]*K),int(TB[1]*K)),(int(TB[2]*K),int(TB[3]*K)),1,max(1,int(0.5*K))).astype(bool)]=False
text('25',(TB[0]+TB[2])/2-3,(TB[1]+TB[3])/2+0.5,20,'gloock.ttf',ink=False)
text('c',(TB[0]+TB[2])/2+10.5,(TB[1]+TB[3])/2-5.5,8,'gloock.ttf',ink=False)
CB=(TB[2]+5,WY1+5,FX1-48,FY1-6)
pl.ink[int(CB[1]*K):int(CB[3]*K),int(CB[0]*K):int(CB[2]*K)]=False
pl.ink[cv2.rectangle(np.zeros(pl.ink.shape,np.uint8),(int((CB[0]+1.6)*K),int((CB[1]+1.6)*K)),(int((CB[2]-1.6)*K),int((CB[3]-1.6)*K)),1,max(1,int(0.4*K))).astype(bool)]=True
text('THE VANILLA SHOP',(CB[0]+CB[2])/2,CB[1]+10.5,8.6,'gloock.ttf',track=0.25)
text('NEGOMBO',(CB[0]+CB[2])/2,CB[1]+22,5.6,'gloock.ttf',track=2.4)
pl.ink|=edge
# ---------------------------------------------------------------- the vine, breaking out over the right of the stamp
sp=Plate(W,H,K); spray.stamp_spray(sp)
paste(pl,sp,0,0,halo=0.8)
pl.save(f'stamp-K{K}.png')
print('ok', pl.ink.shape)
