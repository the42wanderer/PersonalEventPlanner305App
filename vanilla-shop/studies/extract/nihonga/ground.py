# Places a 2:1 painting at the foot of a 120 x 70 mm label strip (20 px/mm), extending its gradient up and sideways.
import sys, numpy as np
from PIL import Image, ImageFilter
def build(src, out, Ha=46, W=120, H=70, k=20):
    im=Image.open(src).convert('RGB'); a=np.asarray(im).astype(np.float32)
    hpx=int(Ha*k); wpx=int(im.width*hpx/im.height); art=np.asarray(im.resize((wpx,hpx),Image.LANCZOS)).astype(np.float32)
    # vertical profile from the outer 4% columns either side (the plant does not reach them)
    e=max(2,int(im.width*0.04)); prof=np.concatenate([a[:,:e],a[:,-e:]],1).mean(1)
    prof=np.asarray(Image.fromarray(prof[:,None,:].astype(np.uint8)).resize((1,hpx),Image.BILINEAR)).astype(np.float32)[:,0]
    Wp,Hp=W*k,H*k; can=np.zeros((Hp,Wp,3),np.float32)
    top=Hp-hpx; can[:top]=prof[0]; can[top:]=prof[:,None,:]
    x0=(Wp-wpx)//2; xs=np.arange(wpx)
    f=np.clip(np.minimum(xs,wpx-1-xs)/(0.06*wpx),0,1)[None,:,None]  # feather the art's side edges into the extension
    can[top:,max(x0,0):x0+wpx]=art[:,max(-x0,0):wpx-max(-x0,0) if x0<0 else wpx]*f+can[top:,max(x0,0):x0+wpx]*(1-f)
    n=np.random.default_rng(3).normal(0,1,(Hp,Wp)).astype(np.float32)*3.2  # grain, so the extension matches the painting
    mask=np.ones((Hp,Wp),np.float32); mask[top:,max(x0,0):x0+wpx]=1-f[0,:,0][None,:]
    can+= (n*mask)[...,None]
    Image.fromarray(can.clip(0,255).astype(np.uint8)).save(out,quality=94)
if __name__=='__main__': build(sys.argv[1],sys.argv[2],float(sys.argv[3]) if len(sys.argv)>3 else 46)
