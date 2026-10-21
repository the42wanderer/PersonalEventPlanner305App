import numpy as np, cv2, json
rng=np.random.default_rng(7)
S=3240/270.0                      # px per mm
BW,BH=int(381*S),int(406*S)       # bag body
def fbm(h,w,scale,oct=4,seed=0):
    r=np.random.default_rng(seed); out=np.zeros((h,w),np.float32); amp=1; tot=0
    for o in range(oct):
        s=max(2,int(scale/(2**o))); g=r.standard_normal((h//s+3,w//s+3)).astype(np.float32)
        out+=amp*cv2.resize(g,(w,h),interpolation=cv2.INTER_CUBIC)[:h,:w]; tot+=amp; amp*=0.5
    return out/tot
# ---- canvas cloth: plain weave (~1 mm threads), slubs, colour drift
y,x=np.mgrid[0:BH,0:BW].astype(np.float32)
P=S*0.85
warp=np.sin(2*np.pi*x/P+fbm(BH,BW,40,2,1)*1.5); weft=np.sin(2*np.pi*y/P+fbm(BH,BW,40,2,2)*1.5)
weave=0.5*warp*np.sign(weft)+0.5*weft*np.sign(np.sin(2*np.pi*x/(2*P)))
slub=cv2.GaussianBlur(np.clip(rng.standard_normal((BH,BW)).astype(np.float32)*(rng.random((BH,BW))>0.995),-3,3),(0,0),sigmaX=9,sigmaY=0.8)
tex=0.035*weave+0.25*slub+0.008*fbm(BH,BW,60,3,3)+0.02*rng.standard_normal((BH,BW)).astype(np.float32)
cloth=np.array([238,228,204],np.float32)/255
img=np.ones((BH,BW,3),np.float32)*cloth*(1+tex[...,None])
# ---- the one black ink
import sys
film=np.load(sys.argv[1] if len(sys.argv)>1 else 'worn.npy').astype(np.float32)
aw=int(270*S); ah=int(film.shape[0]*aw/film.shape[1]); ox=(BW-aw)//2; oy=int(48*S)
m=cv2.resize(film,(aw,ah),interpolation=cv2.INTER_AREA)
m=cv2.GaussianBlur(m,(0,0),0.9)                      # ink wicks into the fibres
full=np.zeros((BH,BW),np.float32); full[oy:oy+ah,ox:ox+aw]=m
fibre=np.clip(0.5+2.2*tex,0,1)
worn=np.clip(0.97+0.08*fbm(BH,BW,120,3,12),0.88,1)
a=full*np.clip(0.88+0.16*fibre,0,1)*worn
col=np.array((30,27,25),np.float32)/255
inked=col*(0.9+1.6*tex[...,None])+0.025          # black plastisol-free water-based ink: a soft, slightly lifted black
img=img*(1-a[...,None])+inked*a[...,None]
# ---- soft creases: a few broad folds from lying flat, gentle shading + small displacement
cr=np.zeros((BH,BW),np.float32)
for (cx_,ang,w_,amp) in [(0.35,0.25,0.10,1.0),(0.7,-0.15,0.07,-0.7),(0.55,1.35,0.12,0.6)]:
    d=( (x/BW-cx_)*np.cos(ang) - (y/BH-0.5)*np.sin(ang) )/w_
    cr+=amp*np.exp(-d*d)
cr+=0.04*fbm(BH,BW,900,1,41)
gy_,gx_=np.gradient(cv2.GaussianBlur(cr,(0,0),25))
shade=1+90*(gx_*0.5-gy_*0.85)
img*=np.clip(shade,0.93,1.04)[...,None]
mx=(x+gx_*900).astype(np.float32); my=(y+gy_*900).astype(np.float32)
img=cv2.remap(img,mx,my,cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)
# top hem: folded band with stitching
hem=int(30*S); img[:hem]*=0.97; img[hem-3:hem+2]*=0.9
for xx in range(int(8*S),BW-int(8*S),int(3.2*S)): cv2.line(img,(xx,hem-int(4*S)),(xx+int(1.8*S),hem-int(4*S)),(0.72,0.68,0.6),2)
img=np.clip(img,0,1)
# ---- scene: bag lying flat on a table, both handles laid up above it
W,H=BW+int(120*S),BH+int(280*S); bx,by=(W-BW)//2,int(215*S)
bg=np.ones((H,W,3),np.float32)*np.array([205,199,188],np.float32)/255
bg*=(1+0.004*fbm(H,W,30,2,99)+0.006*fbm(H,W,500,2,98))[...,None]
def strap(x1,x2,top,hw):
    lay=np.zeros((H,W),np.uint8); cx=(x1+x2)/2; rx=(x2-x1)/2
    pts=[(cx-rx*np.cos(t), by+int(12*S)-(by+int(12*S)-top)*np.sin(t)) for t in np.linspace(0,np.pi,90)]
    cv2.polylines(lay,[np.array(pts,np.int32)],False,255,hw,cv2.LINE_AA)
    lay[by:,:]=0
    return lay.astype(np.float32)/255
hw=int(25*S); x1,x2=bx+int(BW*0.29),bx+int(BW*0.71)
back=strap(x1+int(9*S),x2+int(9*S),by-int(178*S),hw); front=strap(x1,x2,by-int(170*S),hw)
for m_,dark in ((back,0.9),(front,1.0)):
    sh_=cv2.GaussianBlur(m_,(0,0),12); bg*=(1-0.22*np.roll(np.roll(sh_,10,0),7,1))[...,None]
    edge=np.clip(cv2.GaussianBlur(m_,(0,0),3)-cv2.GaussianBlur(cv2.erode(m_,np.ones((9,9))),(0,0),3),0,1)
    col=cloth*dark*(1+0.6*cv2.resize(tex,(W,H))[...,None])*(1-0.12*edge[...,None])
    bg=bg*(1-m_[...,None])+col*m_[...,None]
sh=np.zeros((H,W),np.float32); sh[by+10:by+BH+20,bx+8:bx+BW+16]=1; sh=cv2.GaussianBlur(sh,(0,0),24)
bg*=(1-0.3*sh)[...,None]
bg[by:by+BH,bx:bx+BW]=img
# strap ends sewn inside the hem: the stitched box-and-cross
st=(0.66,0.62,0.54)
for xc in (x1,x2):
    l,r_=xc-hw//2,xc+hw//2; t,b_=by+int(4*S),by+int(26*S)
    bg[by:b_+int(2*S),l:r_]*=0.985
    for p,q in (((l+6,t),(r_-6,t)),((r_-6,t),(r_-6,b_)),((r_-6,b_),(l+6,b_)),((l+6,b_),(l+6,t)),((l+6,t),(r_-6,b_)),((r_-6,t),(l+6,b_))):
        n_=int(np.hypot(q[0]-p[0],q[1]-p[1])//14)
        for k in range(n_):
            a0=k/n_; a1=(k+0.6)/n_
            cv2.line(bg,(int(p[0]+(q[0]-p[0])*a0),int(p[1]+(q[1]-p[1])*a0)),(int(p[0]+(q[0]-p[0])*a1),int(p[1]+(q[1]-p[1])*a1)),st,3,cv2.LINE_AA)
out=(np.clip(bg,0,1)*255).astype(np.uint8)
tag=sys.argv[2] if len(sys.argv)>2 else 'textured'
cv2.imwrite(f'mock-{tag}.jpg',cv2.cvtColor(cv2.resize(out,(1600,int(H*1600/W)),interpolation=cv2.INTER_AREA),cv2.COLOR_RGB2BGR),[cv2.IMWRITE_JPEG_QUALITY,90])
z=out[by+oy+int(150*S):by+oy+int(250*S), bx+ox+int(130*S):bx+ox+int(255*S)]
cv2.imwrite(f'mock-{tag}-detail.jpg',cv2.cvtColor(z,cv2.COLOR_RGB2BGR),[cv2.IMWRITE_JPEG_QUALITY,90])
print(W,H)
