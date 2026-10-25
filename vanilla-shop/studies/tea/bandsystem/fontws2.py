# FondFont picks on the 12-bag front: Redaction (MoMA PS1 commission, OFL) and Hedvig Letters Serif (OFL),
# with Uncut Sans (OFL). Solid ink throughout (no fake foil gradient); "Vanilla" in flat gold = where the foil goes.
import sys, json
S='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/'
sys.argv=sys.argv[:1]; sys.path.insert(0,S+'teasoap')
import build6 as b6, kit
from kit import txt, rule, width, logo
from build6 import INK, B, BOX, BH, lion
F=S+'ff/'; GOLD='#A07A2C'
kit.FONTS.update({'RB':F+'redaction-700-normal.ttf','R35':F+'redaction-35-700-normal.ttf','HV':F+'hedvig-letters-serif-400-normal.ttf',
                  'UN':F+'uncut-sans-400-normal.ttf','UM':F+'uncut-sans-500-normal.ttf','UB':F+'uncut-sans-600-normal.ttf'})
b6.css=''.join(f"@font-face{{font-family:{a};src:url(file://{v})}}" for a,v in kit.FONTS.items())
d=BOX['cube']; FW,FH=d['FW'],d['FH']; top=FH-BH; man=[]
OPT=[('A','Redaction Bold + Uncut Sans','RB',False,0),('B','Redaction Bold, capitals + Uncut Sans','RB',True,0.06),
     ('C','Redaction 35 Bold (worn) + Uncut Sans','R35',False,0),('D','Hedvig Letters Serif + Uncut Sans','HV',False,0)]
for k,nm,f,caps,tr in OPT:
    o=[]; x=7; w1,w2=('VANILLA ','TEA') if caps else ('Vanilla ','Tea')
    sz=min(12.5,(FW-26-x)/(width(w1+w2,f,1)+tr*len(w1+w2)))
    o.append(f'<text x="{x-0.4}" y="{top+12.4}" font-family="{f}" font-size="{sz:.2f}" letter-spacing="{sz*tr:.3f}"><tspan fill="{GOLD}">{w1}</tspan><tspan fill="{INK}">{w2}</tspan></text>')
    o.append(txt('Ceylon black tea with natural vanilla',x,top+18.6,2.6,INK,'UN'))
    o.append(rule(x,top+21.6,FW-27,top+21.6,INK,0.2,0.4))
    o.append(txt('12 TEA BAGS',x,top+25.4,2.1,INK,'UB',tr=0.08)); o.append(txt('NET WT. 24 g',FW-27,top+25.4,2.1,INK,'UB','end',0.08))
    o.append(rule(FW-22,top+5,FW-22,FH-5,INK,0.2,0.4)); o.append(logo(FW-11,top+10.5,13,INK)); o.append(lion(FW-17.3,top+17.4,12.6,INK))
    o.append(f'<rect x="{-B}" y="{-B}" width="{FW+2*B}" height="8" fill="#000" opacity=".55"/>'+txt(k+' · '+nm,2,2.6,2.6,'#fff','UM'))
    man.append(b6.face(f'fw2-{k}',FW,FH,'c6-cube-front.jpg',o))
json.dump(man,open(b6.O+'fw2.json','w')); print('ok')
