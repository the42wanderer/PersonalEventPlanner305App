# Vanilla Tea, 12-bag front, as a Japanese woodblock print (moku-hanga): the same flat illustration separated into a
# few transparent inks on warm paper, the flower left as unprinted paper, wood grain in the colour, each block a hair
# out of register, and a bokashi (the printer's hand-wiped gradient) of indigo across the top carrying the name.
# Type: the range's own (Instrument Serif, Archivo Expanded caps); "VANILLA" in gold foil.
import sys, json, numpy as np, cv2
from PIL import Image
S='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/'
sys.argv=sys.argv[:1]; sys.path.insert(0,S+'teasoap')
import build6 as b6, kit
from build6 import canvas, scene, B, BOX, K, hx, lion
from kit import logo
from foliage2 import paint_flower
O=b6.O
kit.FONTS.update({'ISR':'/home/user/PersonalEventPlanner305App/vanilla-shop/fonts/instrument-serif.ttf'})
b6.css=''.join(f"@font-face{{font-family:{a};src:url(file://{v})}}" for a,v in kit.FONTS.items())
d=BOX['cube']; FW,FH=d['FW'],d['FH']; cx=FW/2
PAPER='#F2E8D5'
INKS={'ground':'#DDCBA8','far':'#C7B28C','dgreen':'#4E6A4B','lgreen':'#93A77C','pod':'#5A3926','gold':'#D9A33F','indigo':'#232F48'}
rng=np.random.default_rng(7)
def noise(h,w,sx,sy,seed):
    n=np.random.default_rng(seed).normal(0,1,(h,w)).astype(np.float32); n=cv2.GaussianBlur(n,(0,0),sigmaX=sx,sigmaY=sy); return n/(n.std()+1e-6)
def print_block(out,mask,ink,seed,grain=0.06,shift=2):
    h,w=mask.shape; dx,dy=np.random.default_rng(seed).integers(-shift,shift+1,2)
    m=np.roll(np.roll(mask,dy,0),dx,1)
    m=cv2.GaussianBlur(m,(0,0),0.9); m=np.clip((m-0.5+0.07*noise(h,w,2.5,2.5,seed+1))*2.2+0.5,0,1)   # a cut, slightly rough edge
    wood=noise(h,w,90,2.2,seed+2)                                                                    # the block's grain, along the length
    a=m*np.clip(0.9+grain*wood+0.03*noise(h,w,10,10,seed+3),0,1)
    return out*(1-a[...,None]*(1-hx(ink)/255))                                                         # transparent ink: multiply
def art():
    img,P=canvas(FW,FH); scene(P,img,(B-6,B+26),0.86,flower=False); paint_flower(P,img,(B+52,B+70),120,2.15)
    h,w=img.shape[:2]; r,g,b=img[...,0],img[...,1],img[...,2]; L=img.mean(2)
    bg=np.linalg.norm(img-hx('#113C3A'),axis=2)<20
    flower=L>205; gold=(r>175)&(b<150)&(g>120)&~flower
    pod=(r>g+6)&(r>b+6)&(L<150)&~gold
    leaf=~(bg|flower|gold|pod); far=leaf&(L<95); dg=leaf&(L>=95)&(L<150); lg=leaf&(L>=150)
    out=np.ones((h,w,3),np.float32)*hx(PAPER)
    fib=noise(h,w,0.6,0.6,11); out*=(1+0.018*fib)[...,None]                                          # paper fibre
    f=lambda m:m.astype(np.float32)
    out=print_block(out,f(~flower),INKS['ground'],21,0.012)                                            # a pale tea ground; the flower is the paper
    out=print_block(out,f(lg|dg),INKS['lgreen'],23)
    out=print_block(out,f(dg),INKS['dgreen'],24); out=print_block(out,f(pod),INKS['pod'],25); out=print_block(out,f(gold),INKS['gold'],26,0.08)
    yy=np.arange(h,dtype=np.float32)[:,None]/K-B; t=np.clip((50-yy)/30,0,1)**1.3; t=t*t*(3-2*t)            # bokashi: wiped from the top
    bok=np.broadcast_to(t,(h,w))*np.clip(1+0.02*noise(h,w,300,40,31),0,1.05)
    a=bok*np.clip(0.97+0.015*noise(h,w,160,8,32)+0.012*noise(h,w,3,3,33),0,1); out=out*(1-a[...,None]*(1-hx(INKS['indigo'])/255))
    Image.fromarray(out.clip(0,255).astype(np.uint8)).save(O+'hg-front.jpg',quality=95)
def T(t,x,y,sz,c,f,a='middle',tr=0.0): return f'<text x="{x:.2f}" y="{y:.2f}" font-family="{f}" font-size="{sz}" letter-spacing="{sz*tr:.3f}" fill="{c}" text-anchor="{a}">{t}</text>'
art()
CREAM='#F2E8D5'; GOLD='#C9A15A'; IND='#232F48'
o=[logo(cx,10.8,12,CREAM),
   T('VANILLA',cx,28.5,11,GOLD,'ISR',tr=0.16), T('Tea',cx,37,7,CREAM,'IS'),
   T('CEYLON BLACK TEA WITH NATURAL VANILLA',cx,41.6,1.4,CREAM,'RW',tr=0.3),
   lion(FW-13.5,5.2,8.5,CREAM),
   T('12 TEA BAGS',7,8.4,1.35,CREAM,'RW','start',0.3), T('NET WT. 24 g',7,11.4,1.35,CREAM,'RW','start',0.3)]
json.dump([b6.face('hg-front',FW,FH,'hg-front.jpg',o)],open(O+'hg.json','w')); print('ok')
