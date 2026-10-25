# The glow direction, from coal to gem: jewel-toned grounds with colour in the shadows, a wide coloured halo so the light
# seems to come from inside the box, a soft vignette, pearl highlights, and a bright gold-leaf foil for VANILLA.
import sys, json, numpy as np, cv2
from PIL import Image
S='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/'
sys.argv=sys.argv[:1]; sys.path.insert(0,S+'teasoap')
import build6 as b6, kit
from build6 import B, BOX, K, hx, lion
import heat as H
O=b6.O
kit.FONTS.update({'ISR':'/home/user/PersonalEventPlanner305App/vanilla-shop/fonts/instrument-serif.ttf'})
b6.css=''.join(f"@font-face{{font-family:{a};src:url(file://{v})}}" for a,v in kit.FONTS.items())
d=BOX['cube']; FW,FH=d['FW'],d['FH']; cx=FW/2
LEAF=('<linearGradient id="leaf" x1="0" y1="0" x2="1" y2="0.3"><stop offset="0" stop-color="#9A7230"/><stop offset=".22" stop-color="#E9CB82"/>'
      '<stop offset=".45" stop-color="#B98D3F"/><stop offset=".7" stop-color="#F6E2A8"/><stop offset="1" stop-color="#A57B34"/></linearGradient>')
G={'cognac':  (['#1C0C06','#391708','#5C2710','#934B1E','#D58A3E','#F6CC8A','#FFF7EA'],'#C46A2A','#F6EBDD','Cognac (hōjicha)'),
   'emerald': (['#04140D','#082A1A','#0F4529','#1F6A40','#68A85E','#DCE29A','#FFFCEC'],'#2C9A5E','#EFF1E4','Emerald (matcha)'),
   'sapphire':(['#060C24','#0C1A48','#162E70','#2C52A2','#86A2D8','#ECE0BC','#FFF9EC'],'#3B68C8','#EEEADF','Sapphire (aizome)'),
   'obsidian':(['#100E10','#211B1D','#372B28','#62503E','#B4915F','#F0DBAA','#FFF9EC'],'#9A7444','#F3ECDF','Obsidian (sumi)')}
def gem(src,dst,ramp,halo):
    a=np.asarray(Image.open(O+src).convert('RGB')).astype(np.float32); h,w=a.shape[:2]
    L=(a@np.array([0.3,0.59,0.11],np.float32))/255
    Ls=cv2.GaussianBlur(L,(0,0),1.1*K); lo,hi=np.percentile(Ls,1),np.percentile(Ls,99.7); v=np.clip((Ls-lo)/(hi-lo),0,1)**0.95
    out=H.ramp(v,ramp)
    g=cv2.GaussianBlur(L,(0,0),9*K); g=np.clip((g-g.min())/(g.max()-g.min()+1e-6),0,1)**1.6          # the wide inner light
    hc=hx(halo)/255; out=255-(255-out)*(1-0.55*g[...,None]*hc)                                            # screen the halo in
    yy,xx=np.mgrid[0:h,0:w].astype(np.float32); r=np.hypot((xx-w/2)/(w*0.62),(yy-h/2)/(h*0.62))
    out*=(1-0.32*np.clip(r-0.55,0,1)**1.4)[...,None]                                                      # vignette
    pearl=np.clip((v-0.88)/0.12,0,1)[...,None]; out=out*(1-0.35*pearl)+np.array([255,253,248])*0.35*pearl  # pearl highlights
    out+=np.random.default_rng(5).normal(0,2.6,(h,w))[...,None]
    Image.fromarray(out.clip(0,255).astype(np.uint8)).save(O+dst,quality=95)
def T(t,x,y,sz,c,f,a='middle',tr=0.0): return f'<text x="{x:.2f}" y="{y:.2f}" font-family="{f}" font-size="{sz}" letter-spacing="{sz*tr:.3f}" fill="{c}" text-anchor="{a}">{t}</text>'
man=[]
for k,(ramp,halo,cream,nm) in G.items():
    gem('pr2.jpg',f'p3-{k}-2.jpg',ramp,halo); gem('pr1.jpg',f'p3-{k}-1.jpg',ramp,halo)
    o=[f'<defs>{LEAF}</defs>',T('THE VANILLA SHOP',cx,10.5,1.5,cream,'RW',tr=0.5),
       T('VANILLA',cx,25,11.5,'url(#leaf)','ISR',tr=0.16), T('Tea',cx,34.2,7.2,cream,'IS'),
       T('CEYLON BLACK TEA WITH NATURAL VANILLA',cx,40,1.45,cream,'RW',tr=0.3),
       T('12 TEA BAGS',8,FH-6.5,1.4,cream,'RW','start',0.3),T('NET WT. 24 g',FW-8,FH-6.5,1.4,cream,'RW','end',0.3)]
    man.append(b6.face(f'p3-{k}-maison',FW,FH,f'p3-{k}-2.jpg',o))
    lw,lh=54,31; lx,ly=cx-lw/2,FH-lh-9; ink=ramp[1]
    o=[f'<defs>{LEAF}</defs>',f'<rect x="{lx}" y="{ly}" width="{lw}" height="{lh}" fill="{cream}"/>',
       f'<rect x="{lx+1.4}" y="{ly+1.4}" width="{lw-2.8}" height="{lh-2.8}" fill="none" stroke="url(#leaf)" stroke-width="0.25"/>',
       T('THE VANILLA SHOP',cx,ly+6.5,1.4,ink,'RW',tr=0.42),
       T('VANILLA',cx,ly+15.2,7.0,'url(#leaf)','ISR',tr=0.16), T('Tea',cx,ly+21.4,5.0,ink,'IS'),
       f'<path d="M{cx-6} {ly+23.6}H{cx+6}" stroke="{ink}" stroke-width="0.15" opacity=".6"/>',
       T('12 TEA BAGS  ·  NET WT. 24 g',cx,ly+27.2,1.35,ink,'RW',tr=0.3), lion(FW-14.5,6,9.5,cream)]
    man.append(b6.face(f'p3-{k}-label',FW,FH,f'p3-{k}-1.jpg',o))
json.dump(man,open(O+'p3.json','w')); print('ok')
