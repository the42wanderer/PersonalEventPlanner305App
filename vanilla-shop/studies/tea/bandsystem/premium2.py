# The premium direction kept (dark ground, the glowing bloom, spaced capitals, air), with the range's own type
# (Instrument Serif + Archivo Expanded caps) and four dark grounds from tea and Japanese craft instead of teal.
import sys, json, re
S='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/'
sys.argv=sys.argv[:1]; sys.path.insert(0,S+'teasoap')
import build6 as b6, kit
from build6 import B, BOX, lion
from kit import logo
import heat as H
O=b6.O
kit.FONTS.update({'ISR':'/home/user/PersonalEventPlanner305App/vanilla-shop/fonts/instrument-serif.ttf'})
b6.css=''.join(f"@font-face{{font-family:{a};src:url(file://{v})}}" for a,v in kit.FONTS.items())
d=BOX['cube']; FW,FH=d['FW'],d['FH']; cx=FW/2
G={'sumi':   (['#0E0C0A','#1B1814','#2E2A22','#5A4E38','#A88A56','#E6CF9A','#FFF6E2'],'#F1E8D6','#C29A55','Sumi ink'),
   'hojicha':(['#140C08','#24160E','#3D2616','#6E4526','#B57E45','#EBC88C','#FFF5E1'],'#F3E6D2','#C9975A','Hōjicha'),
   'matcha': (['#0D120B','#172014','#26341F','#4B6136','#93A866','#E2DDA0','#FFF8E6'],'#EEEBD8','#C2A35C','Deep matcha'),
   'aizome': (['#0A0E18','#141B2B','#213049','#3E5378','#8E9EB8','#E6D9B2','#FFF6E4'],'#ECE7DA','#C4A262','Aizome indigo')}
def T(t,x,y,sz,c,f,a='middle',tr=0.0): return f'<text x="{x:.2f}" y="{y:.2f}" font-family="{f}" font-size="{sz}" letter-spacing="{sz*tr:.3f}" fill="{c}" text-anchor="{a}">{t}</text>'
man=[]
for k,(ramp,cream,gold,nm) in G.items():
    H.heat('pr2.jpg',f'p2-{k}-2.jpg',ramp,sig=1.1,gamma=0.95); H.heat('pr1.jpg',f'p2-{k}-1.jpg',ramp,sig=1.1,gamma=0.95)
    # maison: name high and centred, the bloom rising beneath
    o=[T('THE VANILLA SHOP',cx,10.5,1.5,cream,'RW',tr=0.5),
       T('VANILLA',cx,25,11.5,gold,'ISR',tr=0.16),
       T('Tea',cx,34.2,7.2,cream,'IS'),
       T('CEYLON BLACK TEA WITH NATURAL VANILLA',cx,40,1.45,cream,'RW',tr=0.3),
       T('12 TEA BAGS',8,FH-6.5,1.4,cream,'RW','start',0.3),T('NET WT. 24 g',FW-8,FH-6.5,1.4,cream,'RW','end',0.3)]
    man.append(b6.face(f'p2-{k}-maison',FW,FH,f'p2-{k}-2.jpg',o))
    # label: a small framed cream label on the glow
    lw,lh=54,31; lx,ly=cx-lw/2,FH-lh-9; ink=ramp[1]
    o=[f'<rect x="{lx}" y="{ly}" width="{lw}" height="{lh}" fill="{cream}"/>',
       f'<rect x="{lx+1.4}" y="{ly+1.4}" width="{lw-2.8}" height="{lh-2.8}" fill="none" stroke="{ink}" stroke-width="0.15" opacity=".7"/>',
       T('THE VANILLA SHOP',cx,ly+6.5,1.4,ink,'RW',tr=0.42),
       T('VANILLA',cx,ly+15.2,7.0,gold,'ISR',tr=0.16), T('Tea',cx,ly+21.4,5.0,ink,'IS'),
       f'<path d="M{cx-6} {ly+23.6}H{cx+6}" stroke="{ink}" stroke-width="0.15" opacity=".6"/>',
       T('12 TEA BAGS  ·  NET WT. 24 g',cx,ly+27.2,1.35,ink,'RW',tr=0.3), lion(FW-14.5,6,9.5,cream)]
    man.append(b6.face(f'p2-{k}-label',FW,FH,f'p2-{k}-1.jpg',o))
json.dump(man,open(O+'p2.json','w')); print('ok')
