# More tea: the glow direction with depth of field. A crisp Ceylon tea shoot (two leaves and a bud) in focus in the
# foreground, light wrapping its edges; the vanilla flower out of focus behind; optional faint steam through the name.
import sys, json, numpy as np, cv2
from PIL import Image
S='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/'
sys.argv=sys.argv[:1]; sys.path.insert(0,S+'teasoap')
import build6 as b6, kit, draw
from build6 import canvas, B, BOX, K, hx
from build2 import shoot
import heat as H
O=b6.O
kit.FONTS.update({'ISR':'/home/user/PersonalEventPlanner305App/vanilla-shop/fonts/instrument-serif.ttf'})
b6.css=''.join(f"@font-face{{font-family:{a};src:url(file://{v})}}" for a,v in kit.FONTS.items())
d=BOX['cube']; FW,FH=d['FW'],d['FH']; cx=FW/2
LEAF=('<linearGradient id="leaf" x1="0" y1="0" x2="1" y2="0.3"><stop offset="0" stop-color="#9A7230"/><stop offset=".22" stop-color="#E9CB82"/>'
      '<stop offset=".45" stop-color="#B98D3F"/><stop offset=".7" stop-color="#F6E2A8"/><stop offset="1" stop-color="#A57B34"/></linearGradient>')
G={'cognac': (['#1C0C06','#391708','#5C2710','#934B1E','#D58A3E','#F6CC8A','#FFF7EA'],'#C46A2A','#F6EBDD',
              ('#5E2F12','#7C4019','#A35A24','#C97E3C'),'#F2C88A'),
   'emerald':(['#04140D','#082A1A','#0F4529','#1F6A40','#68A85E','#DCE29A','#FFFCEC'],'#2C9A5E','#EFF1E4',
              ('#174F30','#1F6841','#368A57','#62AA72'),'#D9EDB0')}
def gem_arr(src,ramp,halo):
    a=np.asarray(Image.open(O+src).convert('RGB')).astype(np.float32); h,w=a.shape[:2]
    L=(a@np.array([0.3,0.59,0.11],np.float32))/255
    Ls=cv2.GaussianBlur(L,(0,0),1.5*K); lo,hi=np.percentile(Ls,1),np.percentile(Ls,99.7); v=np.clip((Ls-lo)/(hi-lo),0,1)
    out=H.ramp(v*0.92,ramp)                                                                                 # the flower a touch dimmer: it is behind
    g=cv2.GaussianBlur(L,(0,0),9*K); g=np.clip((g-g.min())/(g.max()-g.min()+1e-6),0,1)**1.6
    out=255-(255-out)*(1-0.5*g[...,None]*hx(halo)/255)
    yy,xx=np.mgrid[0:h,0:w].astype(np.float32); r=np.hypot((xx-w/2)/(w*0.62),(yy-h/2)/(h*0.62))
    out*=(1-0.32*np.clip(r-0.55,0,1)**1.4)[...,None]
    return out
def tea_layer(cols,vein):
    """the crisp shoot, rendered alone; returns colour and alpha"""
    img,P=canvas(FW,FH); bg=img.copy()
    shoot(P,img,(B+2,B+FH+6),-58,64,0.45,24,cols,vein,7,1)
    al=np.clip(np.abs(img-bg).max(2)/40,0,1); return img,al
def steam(h,w):
    m=Image.new('L',(w*2,h*2),0); from PIL import ImageDraw; dr=ImageDraw.Draw(m)
    for x0,ph,amp in ((cx-9,0.0,3.2),(cx+4,1.9,2.6),(cx+14,3.4,2.2)):
        pts=[(B+x0+amp*np.sin(t*0.42+ph)+0.06*t*t*np.sin(ph),B+58-t) for t in np.linspace(0,46,80)]
        rib=draw.ribbon(pts,lambda u:0.55*(1-u)+0.12); dr.polygon([((x)*K*2,(y)*K*2) for x,y in rib],fill=255)
    m=np.asarray(m.resize((w,h),Image.LANCZOS)).astype(np.float32)/255
    m=cv2.GaussianBlur(m,(0,0),0.9*K); yy=np.arange(h,dtype=np.float32)[:,None]/K-B
    return m*np.clip((yy-8)/22,0,1)*np.clip((60-yy)/14,0,1)                                              # thin at both ends
def T(t,x,y,sz,c,f,a='middle',tr=0.0): return f'<text x="{x:.2f}" y="{y:.2f}" font-family="{f}" font-size="{sz}" letter-spacing="{sz*tr:.3f}" fill="{c}" text-anchor="{a}">{t}</text>'
man=[]
for k,(ramp,halo,cream,cols,vein) in G.items():
    base=gem_arr('pr2.jpg',ramp,halo); h,w=base.shape[:2]
    tc,ta=tea_layer(cols,vein)
    wrap=cv2.GaussianBlur(ta,(0,0),1.2*K)*(1-ta)                                                            # light wrapping the leaves' edges
    base=255-(255-base)*(1-0.55*wrap[...,None]*hx(vein)/255)
    out=base*(1-ta[...,None])+tc*ta[...,None]
    for sv in (False,True):
        o_=out.copy()
        if sv: s_=steam(h,w)*0.2; o_=o_*(1-s_[...,None])+hx(cream)*s_[...,None]
        o_+=np.random.default_rng(5).normal(0,2.6,(h,w))[...,None]
        nm=f'p4-{k}-{"steam" if sv else "leaf"}'; Image.fromarray(o_.clip(0,255).astype(np.uint8)).save(O+nm+'.jpg',quality=95)
        o=[f'<defs>{LEAF}</defs>',T('THE VANILLA SHOP',cx,10.5,1.5,cream,'RW',tr=0.5),
           T('VANILLA',cx,25,11.5,'url(#leaf)','ISR',tr=0.16), T('Tea',cx,34.2,7.2,cream,'IS'),
           T('CEYLON BLACK TEA WITH NATURAL VANILLA',cx,40,1.45,cream,'RW',tr=0.3),
           T('12 TEA BAGS',FW-8,FH-10,1.4,cream,'RW','end',0.3),T('NET WT. 24 g',FW-8,FH-6.5,1.4,cream,'RW','end',0.3)]
        man.append(b6.face(nm,FW,FH,nm+'.jpg',o))
json.dump(man,open(O+'p4.json','w')); print('ok')
