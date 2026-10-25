# Vanilla Tea, 12-bag front: the heatmap glow, now a whole Ceylon tea garden. The scene is composed as light (the
# thermal ramp maps it): a dawn glow on the horizon, layered hill-country ridges paler with distance, mist in the
# valleys, an estate slope in contour rows of tea bushes, shade trees on a crest; the vanilla flower and a tea shoot in
# the foreground. The inner label carries the name in the range's type (Instrument Serif, Archivo Expanded caps).
import sys, json, numpy as np, cv2
from PIL import Image, ImageDraw
S='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/'
sys.argv=sys.argv[:1]; sys.path.insert(0,S+'teasoap')
import build6 as b6, kit
from build6 import canvas, B, BOX, K, hx, lion
from build2 import shoot
from build3 import ridge
from foliage2 import paint_flower, paint_vbud
import heat as H
O=b6.O
kit.FONTS.update({'ISR':'/home/user/PersonalEventPlanner305App/vanilla-shop/fonts/instrument-serif.ttf'})
b6.css=''.join(f"@font-face{{font-family:{a};src:url(file://{v})}}" for a,v in kit.FONTS.items())
d=BOX['cube']; FW,FH=d['FW'],d['FH']; cx=FW/2
def nz(h,w,sx,sy,seed):
    n=np.random.default_rng(seed).normal(0,1,(h,w)).astype(np.float32); n=cv2.GaussianBlur(n,(0,0),sigmaX=sx,sigmaY=sy); return n/(n.std()+1e-6)
def landscape(h,w):
    xs=np.arange(w,dtype=np.float32)/K-B; ys=np.arange(h,dtype=np.float32)[:,None]/K-B
    L=0.06+0.56*np.exp(-((ys-33)/11)**2)+0.06*np.exp(-((ys-33)/40)**2)                    # dawn glow on the horizon
    L=np.broadcast_to(L,(h,w)).copy()
    ridges=[(38,[(14,15,16,0.2),(46,11,14,-0.1),(80,17,15,0.15)],0.50),                   # far: pale in the haze
            (46,[(2,10,18,0.0),(36,14,16,0.25),(66,9,14,0.0),(96,12,14,0.1)],0.36),
            (54,[(24,12,20,0.1),(70,15,22,-0.2)],0.24)]
    for i,(base,peaks,tone) in enumerate(ridges):
        r=ridge(xs,base,peaks,40+i,0.35); m=ys>=r[None,:]
        L=np.where(m,tone+0.03*nz(h,w,6*K,2*K,50+i),L)
        mist=0.24*np.exp(-((ys-(r[None,:]+2.5))/2.2)**2)*np.clip(0.6+0.5*nz(h,w,14*K,1.5*K,60+i),0,1.2)   # mist hugging each ridge's foot
        L=L+mist*(i<2)
    # the estate: the near slope planted in contour rows of tea bushes
    crest=ridge(xs,62,[(40,10,40,0.2),(90,6,22,0)],70,0.0); slope=ys>=crest[None,:]
    depth=np.clip(ys-crest[None,:],0,None); period=1.6+0.09*depth                             # rows widen as they come near
    phase=np.cumsum(1/np.maximum(period,0.5),axis=0)/K
    rows=0.5+0.5*np.cos(2*np.pi*phase+0.15*nz(h,w,8*K,2*K,80))
    bush=0.75+0.25*np.cos(2*np.pi*(xs[None,:]/(1.3+0.06*depth))+3*phase)                    # the rows break into rounded bushes
    rows=rows*bush
    L=np.where(slope,0.12+0.24*rows**1.4+0.02*nz(h,w,2*K,2*K,81),L)
    # shade trees on the second ridge's crest: tall, thin, crowned
    im=Image.new('L',(w,h),0); dr=ImageDraw.Draw(im)
    r2=ridge(xs,46,[(2,10,18,0.0),(36,14,16,0.25),(66,9,14,0.0),(96,12,14,0.1)],41,0.35)
    for tx,th in ((30,9),(37,12),(44,8),(62,10),(74,7)):
        j=int((tx+B)*K); y0=r2[min(w-1,j)]+0.6; X=(tx+B)*K
        dr.line([(X,(y0+B)*K),(X,(y0-th*0.7+B)*K)],fill=255,width=int(0.3*K)); th=th*0.75
        for q,(wf,hf,dy) in enumerate(((0.62,0.7,0.0),(0.46,0.8,-1.0),(0.3,0.7,-1.9))):                            # a layered, spreading canopy
            dr.ellipse([X-th*wf*K,(y0-th+dy-hf+B)*K,X+th*wf*K,(y0-th+dy+hf+B)*K],fill=255)
    t=np.asarray(im).astype(np.float32)/255; L=L*(1-t)+0.16*t
    return np.clip(L,0,1)
def foreground(h,w):
    img,P=canvas(FW,FH); bg=img.copy()
    shoot(P,img,(B-4,B+FH+4),-66,58,0.45,22,('#6E8E66','#88A57A','#A3BC92','#C2D4AE'),'#E6EFD6',9,1)
    paint_flower(P,img,(B+11,B+9),30,2.35); paint_vbud(P,img,(B+34,B+6),-40,6)
    a=np.clip(np.abs(img-bg).max(2)/30,0,1); Lf=(img@np.array([0.3,0.59,0.11],np.float32))/255
    return Lf,a
def render(name,ramp):
    img,_=canvas(FW,FH); h,w=img.shape[:2]
    L=cv2.GaussianBlur(landscape(h,w),(0,0),0.5*K); Lf,a=foreground(h,w)
    Lf=cv2.GaussianBlur(Lf*a,(0,0),1.25*K); a=cv2.GaussianBlur(a,(0,0),1.25*K)                     # the near things softest: depth
    L=L*(1-a)+np.clip(Lf/np.maximum(a,1e-3)*1.05,0,1)*a
    out=H.ramp(np.clip(L,0,1)**1.05,ramp); out+=np.random.default_rng(5).normal(0,2.8,(h,w))[...,None]
    Image.fromarray(out.clip(0,255).astype(np.uint8)).save(O+name+'.jpg',quality=95)
def T(t,x,y,sz,c,f,a='middle',tr=0.0): return f'<text x="{x:.2f}" y="{y:.2f}" font-family="{f}" font-size="{sz}" letter-spacing="{sz*tr:.3f}" fill="{c}" text-anchor="{a}">{t}</text>'
man=[]
for rk in ('jade','amber'):
    ramp=H.RAMPS[rk]; nm=f'gd-{rk}'; render(nm,ramp); ink=ramp[1]; CREAM='#F6F1E4'
    lw,lh=56,33; lx,ly=cx-lw/2,FH-lh-8
    o=[f'<rect x="{lx}" y="{ly}" width="{lw}" height="{lh}" fill="{CREAM}"/>',
       f'<rect x="{lx+1.4}" y="{ly+1.4}" width="{lw-2.8}" height="{lh-2.8}" fill="none" stroke="{ink}" stroke-width="0.15" opacity=".75"/>',
       T('THE VANILLA SHOP',cx,ly+6.6,1.4,ink,'RW',tr=0.42),
       T('VANILLA TEA',cx,ly+15.2,6.2,ink,'ISR',tr=0.14),
       T('Ceylon black tea with natural vanilla',cx,ly+20.6,2.6,ink,'IS'),
       f'<path d="M{cx-6} {ly+23.4}H{cx+6}" stroke="{ink}" stroke-width="0.15" opacity=".6"/>',
       T('SINGLE ORIGIN  ·  HILL COUNTRY, SRI LANKA',cx,ly+26.8,1.3,ink,'RW',tr=0.26),
       T('12 TEA BAGS  ·  NET WT. 24 g',cx,ly+30.0,1.3,ink,'RW',tr=0.3),
       lion(FW-14.5,6,9.5,CREAM)]
    man.append(b6.face(nm,FW,FH,nm+'.jpg',o))
json.dump(man,open(O+'gd.json','w')); print('ok')
