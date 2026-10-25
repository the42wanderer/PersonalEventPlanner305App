# Workshop: the name on the brew side, wrapping the corner onto the back, each version locked to the side's grid
# (10 mm margins, the brew rule at 18.6, the pack rule at 49.5, a 10 mm foot). 25-bag: side 85.1 + back 175.9 x 85.
import sys, json, numpy as np
from PIL import Image
S='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/'
sys.path.insert(0,S+'teasoap'); sys.path.insert(0,S+'ext/w')
import build as b
from build import txt, caps, rule, para, grain, hx, B, css
from build2 import CW
O=b.O; p=CW['teal']; LT=p['lt']; WD=p['word']
SW,FW,FH=85.1,175.9,85.0; W=SW+FW; K=8
def ground():
    a=np.ones((int((FH+2*B)*K),int((W+2*B)*K),3),np.float32)*hx(p['band']); a=grain(a,23)
    Image.fromarray(a.clip(0,255).astype(np.uint8)).save(O+'ws-ground.jpg',quality=92)
def brew(o,r=SW-10):
    x=10
    o.append(txt('How to brew',x,15,6.4,LT,'IS')); o.append(rule(x,18.6,r,18.6,LT,0.2,0.6))
    for i,(nn,hd,t) in enumerate([('01','150 ML','One tea bag in freshly boiled water.'),('02','5 MINUTES','Steep, then lift the bag out.'),('03','OVER ICE','Let it cool and pour over ice.')]):
        y=25+i*8.6; o.append(txt(nn,x,y+2.4,4.4,LT,'ISR')); o.append(caps(hd,x+9,y,1.9,LT,tr=0.16)); o.append(txt(t,x+9,y+3.4,2.1,LT,'G'))
    o.append(rule(x,49.5,r,49.5,LT,0.2,0.6)); o.append(caps('25 TEA BAGS · 2 G EACH · NET WT. 50 g',x,53.6,1.6,LT,tr=0.2))
def back(o,narrow=False):
    X=SW; W2=FW; o.append(txt('Vanilla was never plain.',X+10,15,6.4,LT,'IS')); o.append(rule(X+10,18.6,X+W2-10,18.6,LT,0.2,0.6))
    cw=46; xs=[X+10+i*(cw+9) for i in range(3)]; y0=25
    for xx,h_,t in zip(xs,('THE TEA',"WHAT'S INSIDE",'STORAGE'),
        ('The delicate sweetness of natural vanilla unfolds through warm, comforting notes and a smooth, mellow aroma.',
         '25 tagged, unbleached sachet tea bags of Ceylon black tea with natural vanilla.',
         'Keep in a cool, dry place, away from strong odours. Close the box after use.')):
        o.append(caps(h_,xx,y0,1.6,LT,tr=0.2)); pp,_=para(t,xx,y0+4.4,cw,2.1,3.0,LT); o+=pp
    for xx in xs[1:]: o.append(rule(xx-4.5,y0-2.4,xx-4.5,46,LT,0.15,0.4))
    o.append(rule(X+10,49.5,X+W2-10,49.5,LT,0.2,0.6))                       # the back's pack rule sits on the side's
def strip(name,word,note):
    o=[]; o.append(f'<image href="file://{O}ws-ground.jpg" x="{-B}" y="{-B}" width="{W+2*B}" height="{FH+2*B}" preserveAspectRatio="none"/>')
    o.append(f'<defs><clipPath id="cp"><rect x="{-B}" y="{-B}" width="{W+2*B}" height="{FH+2*B}"/></clipPath></defs><g clip-path="url(#cp)">'+''.join(word)+'</g>'); brew(o,SW-16 if name=='ws-5' else SW-10); back(o)
    o.append(f'<path d="M{SW} {-B}V{FH+B}" stroke="#FFFFFF" stroke-opacity=".25" stroke-width="0.2" stroke-dasharray="1 1"/>')   # the fold, for reference
    s=(f'<svg xmlns="http://www.w3.org/2000/svg" width="{(W+2*B)*K:.0f}" height="{(FH+2*B+14)*K:.0f}" viewBox="{-B} {-B} {W+2*B} {FH+2*B+14}">'
       f'<rect x="{-B}" y="{FH+B}" width="{W+2*B}" height="14" fill="#fff"/>'+''.join(o)+
       txt(note,0,FH+B+8.5,3.4,'#222','G')+'</svg>')
    open(O+name+'.html','w').write(f'<html><head><style>{css}html,body{{margin:0}}svg{{display:block}}</style></head><body>{s}</body></html>')
    return [O+name,int((W+2*B)*K),int((FH+2*B+14)*K)]
T=lambda s,x,y,sz,f,extra='': f'<text x="{x}" y="{y}" font-family="{f}" font-size="{sz}" {extra}>{s}</text>'
opts=[
 ('ws-1','1 · Serif, cropped by the foot, wrapping: left on the 10 mm margin, the baseline on the box edge, tone on teal',
  [T('Vanilla',9,FH+5,92,'ISR',f'fill="{WD}"')]),
 ('ws-2','2 · Wide caps tracked across both panels: cap top on the pack rule +7.5, baseline on the 10 mm foot, 10 mm in from each end',
  [T('VANILLA',10,FH-10,25.5,'RWM',f'fill="{WD}" textLength="{W-20}" lengthAdjust="spacing"')]),
 ('ws-3','3 · Italic serif, wrapping, sitting on the 10 mm foot, left on the margin — the name as on the front, at the scale of the candles',
  [T('Vanilla',8.5,FH-10,48,'IS',f'fill="{WD}"')]),
 ('ws-4','4 · Hairline serif outline, wrapping, baseline on the box edge: the word only drawn, never filled, cream at low strength',
  [T('Vanilla',9,FH+5,92,'ISR',f'fill="none" stroke="{LT}" stroke-opacity=".35" stroke-width="0.25"')]),
 ('ws-6','6 · Serif set exactly margin to margin across both panels, sitting on the 10 mm foot — option 2\'s discipline in the brand\'s serif',
  [T('Vanilla',10,FH-10,60,'ISR',f'fill="{WD}" textLength="{W-20}" lengthAdjust="spacingAndGlyphs"')]),
 ('ws-5','5 · Wide caps up the side only, in the right-hand margin column: from the foot to the brew rule, the column narrowed to suit',
  [f'<g transform="translate({SW-6.2} {FH-10}) rotate(-90)">'+T('VANILLA',0,0,8.2,'RWM',f'fill="{WD}" textLength="{FH-10-18.6}" lengthAdjust="spacing"')+'</g>']),
]
if __name__=='__main__':
    ground(); man=[strip(n,w,t) for n,t,w in opts]; json.dump(man,open(O+'ws.json','w')); print('ok')
