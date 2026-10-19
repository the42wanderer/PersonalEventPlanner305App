# Soft-focus orchid "bloom": the vector flower rasterised, blurred and coloured from a glowing centre to a deep edge, with grain.
import io, os, numpy as np, subprocess, json
from PIL import Image, ImageFilter
import orchid
K=20  # px per mm
def mask_svg(paths,W,H):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W*K}" height="{H*K}" viewBox="0 0 {W} {H}"><rect width="{W}" height="{H}" fill="#000"/>'+''.join(f'<path d="{p}" fill="#fff"/>' for p in paths)+'</svg>'
def raster(svg,name):
    name=os.path.abspath(name)
    open(name+'.svg','w').write(svg); subprocess.run(['node','shot.mjs',str(int(svg.split('width="')[1].split('"')[0])),str(int(svg.split('height="')[1].split('"')[0])),name+'.svg'],check=True)
    return np.asarray(Image.open(name+'.png').convert('L')).astype(np.float32)/255
def hx(c): return np.array([int(c[i:i+2],16) for i in (1,3,5)],np.float32)
def bloom(name,W,H,cx,cy,R,edge,core,throat,ground=None,blur=2.4,grain=7,pods=None,podcol=None):
    f=orchid.flower(cx,cy,R)
    M=raster(mask_svg(f['tepals']+[f['tube'],f['lip']],W,H),name+'-m')
    Lp=raster(mask_svg([f['tube'],f['lip']],W,H),name+'-l')
    Th=raster(mask_svg([f['throat']],W,H),name+'-t')
    sig=blur*K
    m8=Image.fromarray((M*255).astype(np.uint8))
    Mb=0.55*np.asarray(m8.filter(ImageFilter.GaussianBlur(sig*2.2))).astype(np.float32)/255+0.75*np.asarray(m8.filter(ImageFilter.GaussianBlur(sig*0.55))).astype(np.float32)/255
    Lb=np.asarray(Image.fromarray((Lp*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(sig*0.6))).astype(np.float32)/255
    Tb=np.asarray(Image.fromarray((Th*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(sig*0.5))).astype(np.float32)/255
    yy,xx=np.mgrid[0:H*K,0:W*K].astype(np.float32)/K
    t=np.clip(np.hypot(xx-cx,yy-cy)/R,0,1)**0.9
    col=hx(core)+(hx(edge)-hx(core))*t[...,None]
    col=col*(1-Lb[...,None]*0.85)+hx(core)*Lb[...,None]*0.85          # the lip glows light
    col=col*(1-Tb[...,None]*0.7)+hx(throat)*Tb[...,None]*0.7
    a=np.clip(Mb*1.15,0,1)
    if ground is None: out=np.dstack([col,a*255])
    else:
        g=hx(ground); rgb=g*(1-a[...,None])+col*a[...,None]; out=np.dstack([rgb,np.full(a.shape,255,np.float32)])
    n=np.random.default_rng(7).normal(0,1,a.shape).astype(np.float32)*grain
    out[...,:3]+=n[...,None]
    Image.fromarray(out.clip(0,255).astype(np.uint8),'RGBA').save(name+'.png')
