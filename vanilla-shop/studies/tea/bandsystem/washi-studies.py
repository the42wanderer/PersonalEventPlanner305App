# Vanilla Tea, 12-bag front, after artisanal / Japanese tea packaging: a light paper ground, the illustration as a soft
# bloom (coloured halo, light core, as the soaps), lots of air, a vertical line of capitals on the edge.
# Type is the range's own: Instrument Serif ("Vanilla" upright in gold foil, "Tea" italic), Archivo Expanded caps, Geist.
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
d=BOX['cube']; FW,FH=d['FW'],d['FH']
GROUNDS={'washi':  dict(paper='#F1EBDD',mid='#9DB08A',hot='#FBF7EC',ink='#1F3A2E',soft='#5E6F60'),
         'hojicha':dict(paper='#E3D3B8',mid='#B08A55',hot='#FAF1E0',ink='#3A2616',soft='#7A5E42'),
         'matcha': dict(paper='#E4E8D6',mid='#7F9C6B',hot='#FAF9EF',ink='#22362A',soft='#5B6E5A')}
def bloom_art(name,g):
    img,P=canvas(FW,FH); scene(P,img,(B+18,B-26),0.8,flower=False); paint_flower(P,img,(B+60,B+30),30,2.2)
    L=(img@np.array([0.3,0.59,0.11],np.float32))/255
    L=cv2.GaussianBlur(L,(0,0),1.5*K); lo,hi=np.percentile(L,2),np.percentile(L,99.8); v=np.clip((L-lo)/(hi-lo),0,1)
    p,m,h=hx(g['paper']),hx(g['mid']),hx(g['hot'])
    a=np.clip(v/0.55,0,1)[...,None]; b_=np.clip((v-0.55)/0.45,0,1)[...,None]
    out=p*(1-a)+m*a; out=out*(1-b_)+h*b_                                   # paper → coloured halo → light core
    out+=np.random.default_rng(3).normal(0,3.0,out.shape[:2])[...,None]
    Image.fromarray(out.clip(0,255).astype(np.uint8)).save(O+f'wa-{name}.jpg',quality=94)
def T(t,x,y,sz,c,f,a='start',tr=0.0,extra=''):
    return f'<text x="{x:.2f}" y="{y:.2f}" font-family="{f}" font-size="{sz}" letter-spacing="{sz*tr:.3f}" fill="{c}" text-anchor="{a}" {extra}>{t}</text>'
man=[]
for name,g in GROUNDS.items():
    bloom_art(name,g); c=g['ink']; x=8
    o=[logo(x+7,13,13,c), f'<path d="M{x+15.5} 7.5V18.5" stroke="{c}" stroke-width="0.18" opacity=".45"/>', lion(x+18.5,8.1,11.5,c),
       T('Vanilla',x-0.6,FH-30.5,17,'#A68237','ISR'),
       T('Tea',x-0.6,FH-15.5,17,c,'IS'),
       T('CEYLON BLACK TEA WITH NATURAL VANILLA',x,FH-9.4,1.55,c,'RW',tr=0.22),
       f'<path d="M{x} {FH-7}H{x+52}" stroke="{c}" stroke-width="0.15" opacity=".45"/>',
       T('12 TEA BAGS',x,FH-4.2,1.55,g['soft'],'RW',tr=0.22), T('NET WT. 24 g',x+52,FH-4.2,1.55,g['soft'],'RW','end',0.22),
       f'<g transform="translate({FW-5.2} {FH-8}) rotate(-90)">'+T('AUTHENTIC CEYLON  ·  SAVOUR THE CALM',0,0,1.5,g['soft'],'RW',tr=0.32)+'</g>']
    man.append(b6.face(f'wa-{name}',FW,FH,f'wa-{name}.jpg',o))
json.dump(man,open(O+'wa.json','w')); print('ok')
