# Bold type pairings on the 12-bag front (fonts free for commercial use: Fontshare FFL, Google OFL).
import sys, json
S='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/'
sys.argv=sys.argv[:1]; sys.path.insert(0,S+'teasoap')
import build6 as b6, kit
from kit import txt, rule, width, logo
from build6 import INK, B, BOX, BH, lion
N=S+'newfonts/x/'; R='/home/user/PersonalEventPlanner305App/vanilla-shop/fonts/'
P={'A':('Zodiak Extrabold + Switzer',N+'zodiak/Zodiak_Complete/Fonts/OTF/Zodiak-Extrabold.otf',N+'switzer/Switzer_Complete/Fonts/OTF/Switzer-Regular.otf',N+'switzer/Switzer_Complete/Fonts/OTF/Switzer-Semibold.otf'),
   'B':('Bespoke Serif Bold + Cabinet Grotesk',N+'bespoke-serif/BespokeSerif_Complete/Fonts/OTF/BespokeSerif-Bold.otf',N+'cabinet-grotesk/CabinetGrotesk_Complete/Fonts/OTF/CabinetGrotesk-Medium.otf',N+'cabinet-grotesk/CabinetGrotesk_Complete/Fonts/OTF/CabinetGrotesk-Bold.otf'),
   'C':('Gambarino + Clash Grotesk',N+'gambarino/Gambarino_Complete/Fonts/OTF/Gambarino-Regular.otf',N+'clash-grotesk/ClashGrotesk_Complete/Fonts/OTF/ClashGrotesk-Medium.otf',N+'clash-grotesk/ClashGrotesk_Complete/Fonts/OTF/ClashGrotesk-Semibold.otf'),
   'D':('Gloock + Switzer Bold',R+'gloock.ttf',N+'switzer/Switzer_Complete/Fonts/OTF/Switzer-Medium.otf',N+'switzer/Switzer_Complete/Fonts/OTF/Switzer-Bold.otf')}
d=BOX['cube']; FW,FH=d['FW'],d['FH']; top=FH-BH; man=[]
for k,(nm,disp,body,bold) in P.items():
    kit.FONTS.update({f'D{k}':disp,f'S{k}':body,f'B{k}':bold})
b6.css=''.join(f"@font-face{{font-family:{a};src:url(file://{v})}}" for a,v in kit.FONTS.items())
for k,(nm,*_) in P.items():
    o=[]; x=7; sz=min(12.5,(FW-26-x)/width('Vanilla Tea',f'D{k}',1))
    o.append(f'<text x="{x-0.4}" y="{top+12.4}" font-family="D{k}" font-size="{sz:.2f}"><tspan fill="url(#foil)">Vanilla</tspan><tspan fill="{INK}"> Tea</tspan></text>')
    o.append(txt('Ceylon black tea with natural vanilla',x,top+18.6,2.55,INK,f'S{k}'))
    o.append(rule(x,top+21.6,FW-27,top+21.6,INK,0.2,0.4))
    o.append(txt('12 TEA BAGS',x,top+25.4,2.1,INK,f'B{k}',tr=0.08)); o.append(txt('NET WT. 24 g',FW-27,top+25.4,2.1,INK,f'B{k}','end',0.08))
    o.append(rule(FW-22,top+5,FW-22,FH-5,INK,0.2,0.4)); o.append(logo(FW-11,top+10.5,13,INK)); o.append(lion(FW-17.3,top+17.4,12.6,INK))
    o.append(f'<rect x="{-B}" y="{-B}" width="{FW+2*B}" height="8" fill="#000" opacity=".55"/>'+txt(nm,2,2.6,2.6,'#fff',f'B{k}'))
    man.append(b6.face(f'fw-{k}',FW,FH,'c6-cube-front.jpg',o))
json.dump(man,open(b6.O+'fw.json','w')); print('ok')
