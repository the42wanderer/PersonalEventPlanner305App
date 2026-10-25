# Vanilla Tea, round 6: one big flat image + a white type band.
# Art: the same shapes (vanilla flower, buds, pods, vine leaves, Ceylon tea shoots), drawn large, cropped, flat, in one
# tonal teal family with the cream flower as the only light; no cast shadows, no soft rendering.
# Type: all of it lives on warm-white bands. 12-bag: a horizontal band across the foot, wrapping every side.
# 25-bag: too long and low for a horizontal band, so the band stands vertically at the front's end and wraps the corner
# as a white belt (front end, the whole brew side, the back's start); the rest of the box is image.
# Fonts: stand-ins until the Adobe Fonts project arrives: Zodiak for IvyPresto Display, Switzer for Neue Haas Unica.
import sys, json, math, re, numpy as np
from PIL import Image
S='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/'
sys.path.insert(0,S+'teasoap'); sys.path.insert(0,S+'teaart'); sys.path.insert(0,S+'ext/w')
sys.argv=sys.argv[:1]+sys.argv[1:]
import kit
NF=S+'newfonts/x/'
kit.FONTS.update({'DS':NF+'zodiak/Zodiak_Complete/Fonts/OTF/Zodiak-Light.otf','DR':NF+'zodiak/Zodiak_Complete/Fonts/OTF/Zodiak-Regular.otf',
                  'DI':NF+'zodiak/Zodiak_Complete/Fonts/OTF/Zodiak-LightItalic.otf',
                  'SN':NF+'switzer/Switzer_Complete/Fonts/OTF/Switzer-Regular.otf','SM':NF+'switzer/Switzer_Complete/Fonts/OTF/Switzer-Medium.otf'})
from kit import txt, rule, para, width, logo
import build as b
from build import hx, B, FOILG, lion
from build2 import shoot, vleaf, K
from build3 import BOX
from foliage2 import paint_flower, paint_pod, paint_vbud, Paint
import build5 as b5
from build5 import icon
O=b.O
css=''.join(f"@font-face{{font-family:{k};src:url(file://{v})}}" for k,v in kit.FONTS.items())
BG='#113C3A'; WHITE='#F6F3EC'; INK='#123B39'; SOFT='#4D6E6A'
FAR=('#174B47','#1B534E'); MID=('#1F5E57','#256A61','#2C7569'); NEAR=('#4C8E7C','#5E9D89','#78B19B'); VEIN='#A6D0BC'
EMB=open('/home/user/PersonalEventPlanner305App/vanilla-shop/brand/emblem/vanilla-shop-emblem-savor-the-calm_cream.svg').read()
EMB=EMB[EMB.index('>',EMB.index('<svg'))+1:EMB.rindex('</svg>')]

def canvas(fw,fh):
    W,H=fw+2*B,fh+2*B; return np.ones((int(H*K),int(W*K),3),np.float32)*hx(BG),Paint(W,H,seed=5)
def save(img,name): Image.fromarray(img.clip(0,255).astype(np.uint8)).save(O+name,quality=94)
def band(img,x0,y0,x1,y1):
    """the white band, a clean cut"""
    h,w=img.shape[:2]; X0,Y0,X1,Y1=[int(round((v+B)*K)) for v in (x0,y0,x1,y1)]
    img[max(Y0,0):min(Y1,h),max(X0,0):min(X1,w)]=hx(WHITE); return img
def flat_grain(img,seed):     # a whisper of print texture, no mottling
    rng=np.random.default_rng(seed); return img+rng.normal(0,2.2,img.shape[:2])[...,None]

# ---------------------------------------------------------------- the image: far vine leaves, mid tea, pods, near tea, flower
def scene(P,img,o,s,flower=True):
    """o: origin (mm, canvas coords incl. bleed); s: scale. One composition reused, cropped by each face"""
    X=lambda x,y:(o[0]+x*s,o[1]+y*s)
    vleaf(P,img,X(-30,70),-38,118*s,15*s,0.25,FAR[0]); vleaf(P,img,X(95,85),-128,110*s,14*s,-0.2,FAR[1])
    vleaf(P,img,X(10,-8),28,96*s,12*s,0.3,FAR[1]); vleaf(P,img,X(120,10),160,90*s,12*s,-0.25,FAR[0])
    shoot(P,img,X(-8,88),-62,78*s,0.35,30*s,MID,'#3F8577',11,1)
    shoot(P,img,X(102,92),-118,74*s,-0.3,28*s,MID,'#3F8577',12,-1)
    shoot(P,img,X(40,-12),82,60*s,0.3,26*s,MID,'#3F8577',13,1)
    paint_pod(P,img,X(-6,62),-14,104*s,3.2*s,0.12,0); paint_pod(P,img,X(-2,67),-21,92*s,2.8*s,0.08,0)
    shoot(P,img,X(18,95),-78,58*s,0.4,24*s,NEAR,VEIN,21,1)
    shoot(P,img,X(92,-10),118,52*s,-0.35,22*s,NEAR,VEIN,22,-1)
    paint_vbud(P,img,X(78,18),-50,9*s); paint_vbud(P,img,X(26,30),200,8*s)
    if flower: paint_flower(P,img,X(52,40),36,3.1*s)

# ---------------------------------------------------------------- 12-bag (cube): a horizontal band across the foot, all round
BH=29.0
def cube():
    d=BOX['cube']; FW,FH,SW,LH=d['FW'],d['FH'],d['SW'],d['LH']; top=FH-BH; out=[]
    img,P=canvas(FW+SW,FH); scene(P,img,(B-8,B-12),0.86)                                  # one image across the front and round the corner
    scene(P,img,(B+FW+4,B-22),0.72,flower=False); paint_vbud(P,img,(B+FW+44,B+20),-40,8); paint_flower(P,img,(B+FW+60,B+30),210,1.6)
    img=band(img,-B,top,FW+SW+B,FH+B); img=flat_grain(img,1)
    save(img[:,:int((FW+2*B)*K)],'c6-cube-front.jpg'); save(img[:,int((FW+B)*K):],'c6-cube-side.jpg')
    o=[]; x=7; sz=min(11.2,(FW-26-x)/(width('Vanilla Tea','DS',1)))
    o.append(f'<text x="{x-0.4}" y="{top+12.2}" font-family="DS" font-size="{sz:.2f}"><tspan fill="url(#foil)">Vanilla</tspan><tspan fill="{INK}"> Tea</tspan></text>')
    o.append(txt('Ceylon black tea with natural vanilla',x,top+18.4,2.45,INK,'SN'))
    o.append(rule(x,top+21.6,FW-27,top+21.6,INK,0.18,0.35))
    o.append(txt('12 tea bags',x,top+25.2,2.15,INK,'SM')); o.append(txt('Net wt. 24 g',FW-27,top+25.2,2.15,INK,'SM','end'))
    o.append(rule(FW-22,top+5,FW-22,FH-5,INK,0.18,0.35))
    o.append(logo(FW-11,top+10.5,13,INK)); o.append(lion(FW-17.3,top+17.4,12.6,INK))
    out.append(face('c6-cube-F',FW,FH,'c6-cube-front.jpg',o))
    o=[]; x=7; o.append(txt('How to brew',x,top+8.4,5.2,INK,'DS'))
    cw=(SW-14)/3
    for i,(ic,hd,ls) in enumerate([('cup','150 ml',['One tea bag,','boiled water.']),('timer','5 minutes',['Steep, then','lift it out.']),('ice','Over ice',['Let it cool,','pour on ice.'])]):
        cx=x+i*cw; o.append(icon(ic,cx-0.3,top+11.6,5.4,INK)); o.append(txt(hd,cx+7,top+14.2,2.3,INK,'SM'))
        for j,l in enumerate(ls): o.append(txt(l,cx+7,top+18.2+j*3.1,2.15,INK,'SN'))
    out.append(face('c6-cube-S',SW,FH,'c6-cube-side.jpg',o))
    img,P=canvas(FW,FH); scene(P,img,(B-30,B-16),0.86); img=band(img,-B,top,FW+B,FH+B); save(flat_grain(img,3),'c6-cube-back.jpg')
    o=[]; x=7; o.append(txt('Vanilla was never plain.',x,top+8.4,5.2,INK,'DS'))
    pp,_=para('The delicate sweetness of natural vanilla unfolds through warm, comforting notes and a smooth, mellow aroma. Twelve tagged, unbleached sachet tea bags.',x,top+13.6,FW-14,2.15,3.0,INK,'SN'); o+=pp
    out.append(face('c6-cube-B',FW,FH,'c6-cube-back.jpg',o))
    out.append(lidface('cube',FW,LH)); return out

# ---------------------------------------------------------------- 25-bag (long): a vertical band, wrapping the corner as a white belt
BW=58.0; BB=62.0
def long():
    d=BOX['long']; FW,FH,SW,LH=d['FW'],d['FH'],d['SW'],d['LH']; bx=FW-BW; out=[]
    img,P=canvas(FW,FH); scene(P,img,(B-6,B-6),1.0); img=band(img,bx,-B,FW+B,FH+B); save(flat_grain(img,4),'c6-long-front.jpg')
    o=[]; x=bx+7; r=FW-7
    o.append(logo(x+7.5,15,15,INK)); o.append(rule(x+17,8.5,x+17,22,INK,0.18,0.35)); o.append(lion(x+20.5,9.6,15,INK))
    o.append(f'<text x="{x-0.5}" y="45" font-family="DS" font-size="15.5" fill="url(#foil)">Vanilla</text>')
    o.append(txt('Tea',x-0.5,61,15.5,INK,'DS'))
    o.append(rule(x,66.5,r,66.5,INK,0.18,0.35))
    o.append(txt('Ceylon black tea with natural vanilla',x,71.4,2.35,INK,'SN'))
    o.append(txt('25 tea bags',x,77.6,2.25,INK,'SM')); o.append(txt('Net wt. 50 g',r,77.6,2.25,INK,'SM','end'))
    out.append(face('c6-long-F',FW,FH,'c6-long-front.jpg',o))
    img,_=canvas(SW,FH); img=band(img,-B,-B,SW+B,FH+B); save(flat_grain(img,5),'c6-long-side.jpg')
    o=[]; x=10; r=SW-10
    o.append(txt('How to brew',x,19,8.2,INK,'DS')); o.append(rule(x,24,r,24,INK,0.18,0.35))
    for i,(ic,hd,ls) in enumerate([('cup','150 ml',['One tea bag in freshly','boiled water.']),('timer','5 minutes',['Steep, then lift','the bag out.']),('ice','Over ice',['Let it cool and','pour over ice.'])]):
        y=30+i*13.2; o.append(icon(ic,x-0.4,y-0.6,8.4,INK)); o.append(txt(hd,x+12.5,y+2.6,2.9,INK,'SM'))
        for j,l in enumerate(ls): o.append(txt(l,x+12.5,y+6.8+j*3.5,2.75,INK,'SN'))
    o.append(rule(x,FH-12,r,FH-12,INK,0.18,0.35)); o.append(txt('25 tea bags · 2 g each · Net wt. 50 g',x,FH-7.6,2.1,SOFT,'SN'))
    out.append(face('c6-long-S',SW,FH,'c6-long-side.jpg',o))
    img,P=canvas(FW,FH); scene(P,img,(B+BB+8,B-30),1.15,flower=False); paint_flower(P,img,(B+FW-30,B+58),200,2.6); paint_vbud(P,img,(B+BB+40,B+18),-60,9)
    img=band(img,-B,-B,BB,FH+B); save(flat_grain(img,6),'c6-long-back.jpg')
    o=[]; x=10; r=BB-8
    o.append(txt('Vanilla was',x,19,8.2,INK,'DS')); o.append(txt('never plain.',x,28.4,8.2,INK,'DS')); o.append(rule(x,33.5,r,33.5,INK,0.18,0.35))
    y=39.5
    for hd,t in (('The tea','The delicate sweetness of natural vanilla unfolds through warm, comforting notes and a smooth, mellow aroma.'),
                 ('Inside','25 tagged, unbleached sachet tea bags of Ceylon black tea with natural vanilla.')):
        o.append(txt(hd,x,y,2.3,INK,'SM')); pp,ye=para(t,x,y+4,r-x,2.1,2.95,INK,'SN'); o+=pp; y=ye+6.5
    out.append(face('c6-long-B',FW,FH,'c6-long-back.jpg',o))
    out.append(lidface('long',FW,LH)); return out

def lidface(box,FW,LH):
    """the lid: the image's ground, quiet; the emblem, the box's seal"""
    img,P=canvas(FW,LH); save(flat_grain(img,7),f'c6-{box}-lid.jpg')
    dia=LH*0.62; sc=dia/250
    o=[f'<g transform="translate({FW/2-dia/2:.2f} {LH/2-dia/2:.2f}) scale({sc:.5f})">{EMB}</g>']
    return face(f'c6-{box}-L',FW,LH,f'c6-{box}-lid.jpg',o)
def face(name,fw,fh,bgimg,o):
    W,H=fw+2*B,fh+2*B
    s=(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W*K:.0f}" height="{H*K:.0f}" viewBox="{-B} {-B} {W} {H}"><defs>{FOILG}</defs>'
       f'<image href="file://{O}{bgimg}" x="{-B}" y="{-B}" width="{W}" height="{H}" preserveAspectRatio="none"/>'+''.join(o)+'</svg>')
    open(O+name+'.html','w').write(f'<html><head><style>{css}html,body{{margin:0}}svg{{display:block}}</style></head><body>{s}</body></html>')
    return [O+name,int(W*K),int(H*K)]
if __name__=='__main__':
    man=cube()+long(); json.dump(man,open(O+'faces6.json','w')); print('ok')
