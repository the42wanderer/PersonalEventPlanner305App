# Workshop: three ways to set the brewing method on the 25-bag brew side, over the same pour scene.
import sys, json
S='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/'
sys.path.insert(0,S+'teasoap'); sys.path.insert(0,S+'teaart')
sys.argv=['x']
import build5 as b5
from build5 import txt, caps, rule, face, icon, SHELF, TIP_X, CW
SW,FH=85.1,85.0; c=CW['teal']['lt']; LT2='#2D6C68'; BAND=CW['teal']['band']; x=10; R=SW-10
def head(o): o.append(txt('How to brew',x,16.5,7.0,c,'IS')); o.append(rule(x,SHELF,R,SHELF,c,0.22,0.6))
def A():
    """stepper: the stream continues as the line; metric | icon node | action"""
    o=[]; head(o); L=TIP_X
    o.append(rule(L,SHELF,L,76,c,0.25,0.7))
    rows=[('150 ml','cup',['One tea bag in','freshly boiled water.']),('5 min','timer',['Steep, then','lift the bag out.']),('over ice','ice',['Or let it cool','and pour over ice.'])]
    for i,(m,ic,ls) in enumerate(rows):
        y=46+i*12.2
        o.append(f'<circle cx="{L}" cy="{y}" r="3.9" fill="{BAND}" stroke="{c}" stroke-width="0.25"/>')
        o.append(icon(ic,L-2.6,y-2.8,5.2,c))
        o.append(txt(m,L-6,y+1.8,5.6,c,'IS','end'))
        for j,l in enumerate(ls): o.append(txt(l,L+6,y-0.6+j*3.3,2.45,c,'G'))
    return face('bw-A',SW,FH,'long5-side.jpg',o)
def B():
    """hero numerals: the candles' big type as the structure, the words small on top"""
    o=[]; head(o); cw=(R-x-8)/3
    cols=[('1','150 ML',['One tea bag,','freshly boiled','water.']),('2','5 MINUTES',['Steep, then','lift the bag','out.']),('3','OVER ICE',['Or let it cool','and pour over','ice.'])]
    for i,(n,hd,ls) in enumerate(cols):
        cx=x+i*(cw+4)
        o.append(txt(n,cx-1,74,30,LT2,'IS'))
        o.append(caps(hd,cx,49,2.1,c,tr=0.16)); o.append(rule(cx,51.2,cx+cw,51.2,c,0.18,0.5))
        for j,l in enumerate(ls): o.append(txt(l,cx,55.6+j*3.2,2.4,c,'G'))
    return face('bw-B',SW,FH,'long5-side.jpg',o)
def C():
    """editorial: the method as one sentence, the values pulled out in caps"""
    o=[]; head(o)
    K=lambda t:f'<tspan font-family="RW" font-size="2.5" letter-spacing="0.4">{t}</tspan>'
    lines=[f'One tea bag, {K("150 ML")} of',f'freshly boiled water and',f'{K("FIVE MINUTES")} of patience —',f'then lift it out. Or let it',f'cool, and pour it {K("OVER ICE")}.']
    for i,l in enumerate(lines): o.append(f'<text x="{x}" y="{46+i*6.2}" font-family="ISR" font-size="5.0" fill="{c}">{l}</text>')
    o.append(rule(x,79,x+18,79,c,0.22,0.6))
    return face('bw-C',SW,FH,'long5-side.jpg',o)
man=[A(),B(),C()]; json.dump(man,open(b5.O+'bw.json','w')); print('ok')
