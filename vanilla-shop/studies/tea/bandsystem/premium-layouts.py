# Three premium layout systems on the 12-bag front (87.6 x 85 mm), over the same flat image.
# Premium packaging conventions: light weights, spaced capitals, one quiet hero line, small supporting type, air.
# Fonts all free for commercial use (OFL / Fontshare FFL); files stay out of the repo.
import sys, json, numpy as np
S='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/'
sys.argv=sys.argv[:1]; sys.path.insert(0,S+'teasoap')
import build6 as b6, kit
from build6 import canvas, scene, save, flat_grain, band, B, BOX, INK, WHITE, lion, EMB, hx, K
from kit import logo
A=S+'ff2/'; N=S+'newfonts/x/'; R='/home/user/PersonalEventPlanner305App/vanilla-shop/fonts/'
kit.FONTS.update({'BOD':A+'bodoni-moda-400-normal.ttf','CAS':A+'libre-caslon-display-400.ttf','PF':A+'playfair-300-normal.ttf',
                  'PFI':A+'playfair-300-italic.ttf','NRI':A+'newsreader-300-italic.ttf','GS':N+'general-sans/GeneralSans_Complete/Fonts/OTF/GeneralSans-Medium.otf'})
b6.css=''.join(f"@font-face{{font-family:{a};src:url(file://{v})}}" for a,v in kit.FONTS.items())
CREAM='#F2ECDD'; GOLD='#B08A3E'
d=BOX['cube']; FW,FH=d['FW'],d['FH']; cx=FW/2
def T(t,x,y,sz,c,f,a='middle',tr=0.0,style=''):
    return f'<text x="{x:.2f}" y="{y:.2f}" font-family="{f}" font-size="{sz}" letter-spacing="{sz*tr:.3f}" fill="{c}" text-anchor="{a}" {style}>{t}</text>'
def hr(x1,y,x2,c,w=0.15,op=0.7): return f'<path d="M{x1:.2f} {y:.2f}H{x2:.2f}" stroke="{c}" stroke-width="{w}" opacity="{op}"/>'
man=[]
# 1 · Apothecary label: the image full bleed; one small framed cream label, everything inside it small and centred
img,P=canvas(FW,FH); scene(P,img,(B-8,B-14),0.86); save(flat_grain(img,1),'pr1.jpg')
lw,lh=54,30; lx,ly=cx-lw/2,FH-lh-9
o=[f'<rect x="{lx}" y="{ly}" width="{lw}" height="{lh}" fill="{CREAM}"/>',
   f'<rect x="{lx+1.4}" y="{ly+1.4}" width="{lw-2.8}" height="{lh-2.8}" fill="none" stroke="{INK}" stroke-width="0.15" opacity=".8"/>',
   T('THE VANILLA SHOP',cx,ly+6.4,1.45,INK,'GS',tr=0.42),
   T('VANILLA TEA',cx,ly+14.6,5.4,INK,'CAS',tr=0.16),
   T('Ceylon black tea with natural vanilla',cx,ly+19.6,2.5,INK,'NRI'),
   hr(cx-6,ly+22.4,cx+6,INK),
   T('12 TEA BAGS  ·  NET WT. 24 G',cx,ly+26.2,1.4,INK,'GS',tr=0.32)]
o.append(lion(FW-14.5,6,9.5,CREAM))
man.append(b6.face('pr1',FW,FH,'pr1.jpg',o))
# 2 · Maison: spaced capitals over the image, centred high; the house line at the foot; nothing heavy
img,P=canvas(FW,FH); scene(P,img,(B-6,B+26),0.86,flower=False)
from foliage2 import paint_flower
paint_flower(P,img,(B+52,B+70),120,2.15)
h=img.shape[0]; yy=np.arange(h)[:,None]/K; f=np.clip((44-yy)/26,0,1)**1.4*0.85             # the sky above the image kept clear
img=img*(1-f[...,None])+hx('#0F3533')*f[...,None]; save(flat_grain(img,2),'pr2.jpg')
o=[T('THE VANILLA SHOP',cx,10.5,1.5,CREAM,'GS',tr=0.5),
   T('VANILLA',cx,24.5,10.2,GOLD,'BOD',tr=0.2),
   T('TEA',cx,31.6,3.2,CREAM,'BOD',tr=0.9),
   T('Ceylon black tea with natural vanilla',cx,37.4,2.6,CREAM,'NRI'),
   T('12 TEA BAGS',8,FH-6.5,1.4,CREAM,'GS','start',0.32),T('NET WT. 24 G',FW-8,FH-6.5,1.4,CREAM,'GS','end',0.32)]
man.append(b6.face('pr2',FW,FH,'pr2.jpg',o))
# 3 · Refined band: a slimmer white band; light spaced capitals; the details as a quiet caption line
BH=22; top=FH-BH
img,P=canvas(FW,FH); scene(P,img,(B-8,B-6),0.86); img=band(img,-B,top,FW+B,FH+B); save(flat_grain(img,3),'pr3.jpg')
o=[T('VANILLA TEA',8,top+9.6,6.2,INK,'PF','start',0.14),
   T('Ceylon black tea with natural vanilla',8,top+14.6,2.55,INK,'NRI','start'),
   T('12 TEA BAGS  ·  NET WT. 24 G',8,top+18.8,1.35,INK,'GS','start',0.32),
   f'<path d="M{FW-21} {top+4.5}V{FH-4.5}" stroke="{INK}" stroke-width="0.15" opacity=".5"/>',
   logo(FW-10.8,top+8.4,11,INK), lion(FW-15.6,top+13.6,9.6,INK)]
man.append(b6.face('pr3',FW,FH,'pr3.jpg',o))
json.dump(man,open(b6.O+'pr.json','w')); print('ok')
