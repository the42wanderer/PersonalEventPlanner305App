import numpy as np
from PIL import Image, ImageDraw, ImageFilter
PX=8  # px per mm
def lerp(a,b,t): return a+(b-a)*t
def bottle(label_png, ground, liquid, scale=1.0, lab_h=70, lab_y=58, neck_png=None):
    # 500 ml flask in mm: body radius 36, body height 128, shoulder dome, neck r 12 len 46, cap h 22
    R=38*scale; BH=92*scale; SH=30*scale; NR=12*scale; NL=46*scale; CH=19*scale
    Wmm=R*2+20; Hmm=BH+SH+NL+CH+16
    W,H=int(Wmm*PX),int(Hmm*PX); cx=W/2
    img=np.zeros((H,W,4),np.float32)
    y_base=H-8*PX; y_body_top=y_base-BH*PX; y_sh_top=y_body_top-SH*PX; y_neck_top=y_sh_top-NL*PX; y_cap_top=y_neck_top-CH*PX
    yy,xx=np.mgrid[0:H,0:W].astype(np.float32)
    # radius profile
    def radius(y):
        r=np.zeros_like(y)
        body=(y<=y_base)&(y>=y_body_top); r[body]=R*PX
        # rounded base corners
        bc=(y>y_base-6*PX*scale)&(y<=y_base); t=(y[bc]-(y_base-6*PX*scale))/(6*PX*scale); r[bc]=R*PX*np.sqrt(np.clip(1-t**2*0.35,0,1))
        sh=(y<y_body_top)&(y>=y_sh_top); t=(y_body_top-y[sh])/(y_body_top-y_sh_top)
        r[sh]=NR*PX+(R-NR)*PX*np.sqrt(np.clip(1-t**2,0,1))
        nk=(y<y_sh_top)&(y>=y_neck_top); r[nk]=NR*PX
        return r
    r=radius(yy[:,0])[:,None]
    inside=np.abs(xx-cx)<r
    u=np.clip((xx-cx)/np.maximum(r,1),-1,1)       # -1..1 across
    nz=np.sqrt(np.clip(1-u**2,0,1))
    # liquid: up to 6 mm into the shoulder
    liq_top=y_sh_top+3*PX*scale
    liq=inside&(yy>=liq_top)
    L=np.array(liquid,np.float32)/255
    shade=(0.55+0.45*nz)*(1-0.25*np.clip(u,0,1))
    col=np.where(liq[...,None], L*shade[...,None], np.array([0.80,0.82,0.80])*(0.85+0.15*nz)[...,None])
    a=np.where(liq,0.985,0.10+0.6*(1-nz)**4)
    img[...,:3]=np.where(inside[...,None],col,0); img[...,3]=np.where(inside,a,0)
    # label: cylinder mapping of the label image (front panel centred, ground elsewhere)
    lab=np.asarray(Image.open(label_png).convert('RGB')).astype(np.float32)/255
    lh_px=lab.shape[0]; lw_mm=lab.shape[1]/20; mm_per_px=lw_mm/lab.shape[1]
    g=np.array([int(ground[i:i+2],16) for i in (1,3,5)],np.float32)/255
    ly0=y_base-(lab_y+lab_h)*scale*PX*0+ (y_base-BH*PX)+ (BH-lab_h*scale-16*scale)*PX*0
    ly0=y_body_top+(BH-lab_h*scale)*PX*0.45; ly1=ly0+lab_h*scale*PX
    band=inside&(yy>=ly0)&(yy<ly1)&(yy<=y_base-4*PX)
    s_mm=np.arcsin(u)*R/scale   # arc length from centre in label mm (label is drawn at 500ml scale)
    lx=(s_mm+lw_mm/2)/mm_per_px; lyp=(yy-ly0)/(scale*PX)/mm_per_px
    curv=(1-nz)*2.2*PX  # slight smile of the label edges
    lyp=(yy-ly0-curv*0)/(scale*PX)/mm_per_px
    ix=np.clip(lx.astype(int),0,lab.shape[1]-1); iy=np.clip(lyp.astype(int),0,lab.shape[0]-1)
    labc=np.where(((lx>=0)&(lx<lab.shape[1]))[...,None], lab[iy,ix], g)
    lshade=(0.62+0.38*nz)*(1-0.18*np.clip(u,0,1))
    labc=labc*lshade[...,None]
    img[...,:3]=np.where(band[...,None],labc,img[...,:3]); img[...,3]=np.where(band,1,img[...,3])
    # neck strip, cylinder-mapped round the neck
    if neck_png:
        nk=np.asarray(Image.open(neck_png).convert('RGB')).astype(np.float32)/255
        nw_mm=nk.shape[1]/20; nh_mm=nk.shape[0]/20
        ny0=y_neck_top+(NL*0.32)*PX; ny1=ny0+nh_mm*scale*PX
        nb=(np.abs(xx-cx)<NR*PX+0.6*PX*scale)&(yy>=ny0)&(yy<ny1)
        un=np.clip((xx-cx)/(NR*PX+0.6*PX*scale),-1,1); nzn=np.sqrt(np.clip(1-un**2,0,1))
        sn=np.arcsin(un)*(NR+0.6*scale)/scale
        nx=np.clip(((sn+nw_mm/2)*20).astype(int),0,nk.shape[1]-1); nyy=np.clip(((yy-ny0)/(scale*PX)*20).astype(int),0,nk.shape[0]-1)
        nc=nk[nyy,nx]*((0.62+0.38*nzn)*(1-0.18*np.clip(un,0,1)))[...,None]
        img[...,:3]=np.where(nb[...,None],nc,img[...,:3]); img[...,3]=np.where(nb,1,img[...,3])
    # glass highlights
    hl=inside&(np.abs(u+0.55)<0.07)&(yy>y_neck_top+4*PX)
    k=np.where(band,0.12,0.4)[...,None]
    img[...,:3]=np.where(hl[...,None],img[...,:3]*(1-k)+k,img[...,:3])
    hl2=inside&(np.abs(u-0.72)<0.03)
    img[...,:3]=np.where(hl2[...,None],img[...,:3]*0.75+0.25,img[...,:3])
    # cap
    capin=(yy>=y_cap_top)&(yy<y_neck_top+1.5*PX)&(np.abs(xx-cx)<(NR+1.2*scale)*PX)
    uc=np.clip((xx-cx)/((NR+1.2*scale)*PX),-1,1); nc=np.sqrt(np.clip(1-uc**2,0,1))
    capc=(0.55+0.45*nc**0.6)[...,None]*np.array([0.78,0.78,0.80])+ (np.abs(uc+0.4)<0.08)[...,None]*0.15
    ribs=(np.sin(xx/(1.1*PX)*np.pi)>0.6)&(yy<y_cap_top+CH*PX*0.7)
    capc=capc*(1-0.08*ribs[...,None])
    img[...,:3]=np.where(capin[...,None],capc,img[...,:3]); img[...,3]=np.where(capin,1,img[...,3])
    out=Image.fromarray((img*255).clip(0,255).astype(np.uint8),'RGBA')
    # shadow
    sh=Image.new('RGBA',out.size,(0,0,0,0)); d=ImageDraw.Draw(sh)
    d.ellipse((cx-R*PX*1.05,y_base-4*PX,cx+R*PX*1.25,y_base+5*PX),fill=(40,25,15,110)); sh=sh.filter(ImageFilter.GaussianBlur(12))
    sh.alpha_composite(out); return sh
