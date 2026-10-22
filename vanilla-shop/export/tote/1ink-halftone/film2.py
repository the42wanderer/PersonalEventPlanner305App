# One-ink tote stamp from the comic-halftone image: brush line work kept, every dot tint re-screened as one true
# halftone, the flower at her hands given its vanilla lip, lettering set, out to a 1-bit film at 270 mm wide.
import numpy as np, cv2, math
from PIL import Image, ImageDraw, ImageFont
from rescreen import load, analyse, halftone
F='/home/user/PersonalEventPlanner305App/vanilla-shop/fonts/'
FN='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/tote/fonts/'
g=load(); h0,w0=g.shape
S=2; ink2,tone2,dot2=analyse(g,S)                       # analysis at 2x the source
K=20.0; W=int(270*K); H=int(round(W*h0/w0)); f=W/w0     # film: 20 px/mm
# ---- separate line work from dots inside the tinted areas: dots are small blobs, lines are long or large shapes
inkb=(ink2>0).astype(np.uint8)
n,lab,st,_=cv2.connectedComponentsWithStats(inkb,8)
big=st[:,4]>=70*S*S; big[0]=False
elong=np.maximum(st[:,2],st[:,3])>=14*S; elong[0]=False
linecomp=(big|elong)[lab]
lines2=inkb.astype(bool)&(~dot2|linecomp)
dots2=inkb.astype(bool)&dot2&~linecomp
# tone of the tint from the dots alone, normalised at the region edges so tints don't fade near outlines
m=dot2.astype(np.float32); sig=3.0*S
tone=cv2.GaussianBlur(dots2.astype(np.float32),(0,0),sig)/np.maximum(cv2.GaussianBlur(m,(0,0),sig),1e-3)
tone=np.clip(tone*1.08,0,1)*m
# quantise lightly towards the four comic tints, the way shading sheets come, but keep the sky's smooth glow
q=np.array([0,0.12,0.27,0.45,0.68]); idx=np.abs(tone[...,None]-q).argmin(-1); tq=q[idx]
yy=np.arange(tone.shape[0])[:,None]/tone.shape[0]
sky=(yy<0.36)
tone=np.where(sky,tone,0.55*tone+0.45*tq)*m
# ---- up to film resolution
def up(a,interp=cv2.INTER_LINEAR): return cv2.resize(a.astype(np.float32),(W,H),interpolation=interp)
L=cv2.GaussianBlur(up(lines2),(0,0),f/S*0.55)>0.5        # smooth the line edges after the upscale
T=up(tone); M=up(m)>0.5
film=L|(halftone(T,K,pitch_mm=1.3,angle=45,min_dot=0.32)&M&~L)
orig=cv2.GaussianBlur(cv2.resize(g,(W,H),interpolation=cv2.INTER_CUBIC),(0,0),f*0.4)<0.5
keep=np.zeros((H,W),np.float32)
for (x0,y0,x1,y1) in ((585,488,705,600),(405,858,505,975)):          # her face, his face (source px)
    cv2.ellipse(keep,(int((x0+x1)/2*f),int((y0+y1)/2*f)),(int((x1-x0)/2*f),int((y1-y0)/2*f)),0,0,360,1,-1)
keep=cv2.GaussianBlur(keep,(0,0),3*f)>0.5
film=np.where(keep,orig,film)
# ---- the flower at her hands: add the rolled trumpet lip the vanilla flower has (source px, then to film)
def P(x,y): return (np.array([x,y])*f).round().astype(np.int32)
def poly(pts,fill=True,width=0):
    p=np.array([P(*q) for q in pts],np.int32)
    mk=np.zeros(film.shape,np.uint8)
    if fill: cv2.fillPoly(mk,[p],1,cv2.LINE_AA)
    else: cv2.polylines(mk,[p],False,1,int(width*K),cv2.LINE_AA)
    return mk.astype(bool)
def bez(p0,p1,p2,n=40):
    t=np.linspace(0,1,n)[:,None]; return (1-t)**2*p0+2*(1-t)*t*p1+t*t*p2
c=np.array([806.0,433.0]); tip=np.array([833.0,452.0]); ctrl=np.array([824.0,433.0])
spine=bez(c,ctrl,tip); dd=np.gradient(spine,axis=0); dd/=np.linalg.norm(dd,axis=1,keepdims=True); nr=np.stack([-dd[:,1],dd[:,0]],1)
wid=2.6+7.0*np.linspace(0,1,len(spine))**1.7
left=spine+nr*wid[:,None]; right=spine-nr*wid[:,None]
tube=list(left)+list(right[::-1])
d=dd[-1]; nrm=nr[-1]; mc=tip
th=np.linspace(0,2*np.pi,120); rng=np.random.default_rng(3); jit=1+0.13*np.abs(np.sin(5*th+0.6))+0.04*rng.standard_normal(120).cumsum()/8
mouth=[mc+d*(4.6*jit[i]*math.cos(t))+nrm*(10.2*jit[i]*math.sin(t)) for i,t in enumerate(th)]
inner=[mc+d*(2.2*math.cos(t)+0.9)+nrm*(5.6*math.sin(t)) for t in th]
tubeM=poly(tube); mouthM=poly(mouth)
film[tubeM|mouthM]=False
film|=poly(list(left),False,0.45)|poly(list(right),False,0.38)
film|=poly(mouth+[mouth[0]],False,0.42)
film|=poly(inner)
film|=poly(list(spine[8:-6]-nr[8:-6]*(wid[8:-6,None]*0.45)),False,0.28)    # one shading line along the underside
# ---- lettering in the empty boxes
def set_text(t,cx,cy,size_mm,font,track=0.0,rot=0.0,bold=5):
    fo=ImageFont.truetype(font,int(size_mm*K))
    chars=list(t) if track else [t]; ws=[fo.getlength(ch) for ch in chars]; tw=sum(ws)+track*K*(len(chars)-1)
    im=Image.new('L',(int(tw+8*K),int(size_mm*K*2.4)),0); dr=ImageDraw.Draw(im); x=4*K
    for ch,w_ in zip(chars,ws): dr.text((x,im.size[1]/2),ch,font=fo,fill=255,anchor='lm'); x+=w_+track*K
    if rot: im=im.rotate(rot,resample=Image.BICUBIC,expand=True)
    a=np.asarray(im)>127; ys,xs=np.nonzero(a); a=a[ys.min():ys.max()+1,xs.min():xs.max()+1]
    if bold: a=cv2.dilate(a.astype(np.uint8),cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(bold,bold))).astype(bool)
    hh,ww=a.shape; x0=int(cx-ww/2); y0=int(cy-hh/2); film[y0:y0+hh,x0:x0+ww]|=a
# the top banner is arched: its centre line runs through (173,169.5), (599,126.5), (1025,170) in source px
def arch(x): return 126.5+43.3*((x-599)/426)**2
def on_arch(t,xs,size,font,track=0.0,dy=0.0):
    slope=2*43.3*(xs-599)/426**2; ang=-math.degrees(math.atan(slope))
    cx,cy=P(xs,arch(xs)+dy); set_text(t,cx,cy,size,font,track,ang)
on_arch('CEYLON',599,13.0,F+'gloock.ttf',1.4,dy=2)
on_arch('ලංකා',305,7.4,FN+'NotoSerifSinhala.ttf',dy=1)
on_arch('இலங்கை',893,5.2,FN+'NotoSerifTamil.ttf',dy=2)
# value tablet x 128-298, y 1192-1325
cx,cy=P(213,1262); set_text('25',cx-int(2.2*K),cy,15,F+'gloock.ttf')
set_text('c',cx+int(6.6*K),cy-int(3.6*K),6.2,F+'gloock.ttf')
# caption box x 338-939, y 1240-1322
cx,cy=P(638.5,1270); set_text('THE VANILLA SHOP',cx,cy,7.2,F+'gloock.ttf',0.45)
cx,cy=P(638.5,1303); set_text('NEGOMBO',cx,cy,3.5,F+'geist-medium.ttf',2.2,bold=3)
# ---- clean for screen printing: no ink specks under 0.08 mm2, no paper holes under 0.06 mm2
def clean(mk,amin):
    n,lab,st,_=cv2.connectedComponentsWithStats(mk.astype(np.uint8),8); keep=st[:,4]>=amin*K*K; keep[0]=False; return keep[lab]
film=clean(film,0.08); film=~clean(~film,0.06)
np.save('ink2.npy',film)
Image.fromarray(np.where(film,0,255).astype(np.uint8)).convert('1').save('tote-stamp-halftone_FILM.png',dpi=(K*25.4,K*25.4))
print('film',W,H,'mm 270 x',round(H/K,1),'black %',round(film.mean()*100,1))
