# One-ink tote stamp: the Sunburst artwork cleaned to a 1-bit film at 600 dpi, with the lettering set in the empty boxes.
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
SRC='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/images/90.webp'
F='/home/user/PersonalEventPlanner305App/vanilla-shop/fonts/'
FN='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/tote/fonts/'
WMM=270.0
src=np.asarray(Image.open(SRC).convert('L')).astype(np.float32)
h0,w0=src.shape; K=24.0                                   # px per mm (610 dpi)
W,H=int(WMM*K),int(WMM*K*h0/w0); f=W/w0
# smooth upscale, then threshold: clean edges with no stair steps
up=cv2.resize(src,(W,H),interpolation=cv2.INTER_CUBIC)
up=cv2.GaussianBlur(up,(0,0),f*0.45)
ink=up<128
# clean-up for screen printing: drop specks of ink under 0.25 mm2, fill paper holes under 0.15 mm2
def clean(m,amin):
    n,lab,st,_=cv2.connectedComponentsWithStats(m.astype(np.uint8),8)
    keep=st[:,4]>=amin*K*K; keep[0]=False
    return keep[lab]
ink=clean(ink,0.25); ink=~clean(~ink,0.15)
def P(x,y): return x*f,y*f                                # source px -> film px
def set_text(t,cx,cy,size_mm,font,track=0.0,anchor='mm'):
    fo=ImageFont.truetype(font,int(size_mm*K))
    chars=list(t) if track else [t]; ws=[fo.getlength(c) for c in chars]; tw=sum(ws)+track*K*(len(chars)-1)
    im=Image.new('L',(int(tw+8*K),int(size_mm*K*2.2)),0); d=ImageDraw.Draw(im); x=4*K
    for c,w_ in zip(chars,ws): d.text((x,im.size[1]/2),c,font=fo,fill=255,anchor='lm'); x+=w_+track*K
    a=np.asarray(im)>127; ys,xs=np.nonzero(a); a=a[ys.min():ys.max()+1,xs.min():xs.max()+1]
    h,w=a.shape; x0=int(cx-(w/2 if anchor[0]=='m' else 0 if anchor[0]=='l' else w)); y0=int(cy-h/2)
    a=cv2.dilate(a.astype(np.uint8),cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))).astype(bool)   # a touch bolder, to sit with the cut lines
    ink[y0:y0+h,x0:x0+w]|=a
    return w/K,h/K
# top banner (source x 229-1367, y 140-232 at its centre): CEYLON, with the Sinhala and Tamil names either side
bx0,by0=P(229,140); bx1,by1=P(1367,232); bcx,bcy=(bx0+bx1)/2,(by0+by1)/2+0.3*K
set_text('CEYLON',bcx,bcy,13.5,F+'gloock.ttf',track=1.6)
set_text('ලංකා',bx0+(bcx-bx0)*0.30,bcy,7.6,FN+'NotoSerifSinhala.ttf')
set_text('இலங்கை',bx1-(bx1-bcx)*0.30,bcy+0.4*K,5.4,FN+'NotoSerifTamil.ttf')
# value tablet (x 178-379, y 1592-1760)
tx0,ty0=P(178,1592); tx1,ty1=P(379,1760); tcx,tcy=(tx0+tx1)/2,(ty0+ty1)/2
w25,_=set_text('25',tcx-2.0*K,tcy+0.6*K,16,F+'gloock.ttf')
set_text('c',tcx-2.0*K+w25*K/2+2.6*K,tcy-3.4*K,6.5,F+'gloock.ttf')
# caption box (x 435-1205, y 1627-1735)
cx0,cy0=P(435,1627); cx1,cy1=P(1252,1735); ccx=(cx0+cx1)/2
set_text('THE VANILLA SHOP',ccx,cy0+(cy1-cy0)*0.40,7.6,F+'gloock.ttf',track=0.45)
set_text('NEGOMBO',ccx,cy0+(cy1-cy0)*0.78,3.6,F+'geist-medium.ttf',track=2.2)
np.save('ink.npy',ink)
Image.fromarray(np.where(ink,0,255).astype(np.uint8)).convert('1').save('tote-stamp-1ink_FILM.png',dpi=(K*25.4,K*25.4))
print('film',W,H,'mm',WMM,round(H/K,1),'black %',round(ink.mean()*100,1))

# optional: the same film with a worn, hand-pulled texture built into the ink, sized so every speck still prints
def fbm(h,w,scale,oct=4,seed=0):
    r=np.random.default_rng(seed); out=np.zeros((h,w),np.float32); amp=1; tot=0
    for o in range(oct):
        s_=max(2,int(scale/(2**o))); g=r.standard_normal((h//s_+3,w//s_+3)).astype(np.float32)
        out+=amp*cv2.resize(g,(w,h),interpolation=cv2.INTER_CUBIC)[:h,:w]; tot+=amp; amp*=0.5
    return out/tot
rng=np.random.default_rng(11)
wear=fbm(H,W,int(18*K),4,3)                                   # broad patches where the squeegee ran light
grain=fbm(H,W,int(0.9*K),2,4)                                 # fine grain, about 0.5 mm
holes=(wear>0.62)&(grain>0.35)
pins=cv2.dilate((rng.random((H,W))>0.99996).astype(np.uint8),cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(9,9))).astype(bool)
solid=cv2.erode(ink.astype(np.uint8),cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(int(0.6*K),)*2)).astype(bool)   # only inside wide black areas
worn=ink&~((holes|pins)&solid)
worn=clean(worn,0.25); worn=~clean(~worn,0.12)
Image.fromarray(np.where(worn,0,255).astype(np.uint8)).convert('1').save('tote-stamp-1ink_FILM-textured.png',dpi=(K*25.4,K*25.4))
np.save('worn.npy',worn)
print('textured: black %',round(worn.mean()*100,1))
