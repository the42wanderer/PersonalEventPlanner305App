# Vanilla Tea, 25-bag carton, built on the soap-box system (export/soap-boxes-final): tinted paper, the bloom duo
# (one huge soft orchid off the edge, one small one), the type sitting on the bloom with a paper veil behind it,
# "Vanilla" in foil over the variant word in italic, caps line + farm line + big NET WT., exposed hairline grid.
# Tea's own additions, from the bottle (the commercial version): the Ceylon Tea mark in the signature, the pack count.
# Long carton faces, mm: front 175.9 x 85, brew side 85.1 x 85, lid 175.9 x 85.1, back 175.9 x 85.
import sys, re, os, json, numpy as np
from PIL import Image, ImageFilter
S='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/'
R='/home/user/PersonalEventPlanner305App/vanilla-shop'
sys.path.insert(0,S+'ext/w'); sys.path.insert(0,R+'/brand/directions/bloom')
import kit
from kit import width, logo, txt, caps, rule, para, esc
import bloom
kit.FONTS.update({'ISR':R+'/fonts/instrument-serif.ttf'})
css=''.join(f"@font-face{{font-family:{k};src:url(file://{v})}}" for k,v in kit.FONTS.items())
O=S+'teasoap/'; KR=bloom.K; K=12; B=3.0
FW,FH,SW,LH=175.9,85.0,85.1,85.1
FOILG=('<linearGradient id="foil" x1="0" y1="0" x2="1" y2="0.35"><stop offset="0" stop-color="#4E300A"/><stop offset="0.28" stop-color="#8E6420"/>'
       '<stop offset="0.46" stop-color="#C9A55A"/><stop offset="0.6" stop-color="#76521A"/><stop offset="0.85" stop-color="#A37A30"/><stop offset="1" stop-color="#4E300A"/></linearGradient>')
LS=open(R+'/brand/ceylon-tea-lion.svg').read(); LV=[float(v) for v in re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)',LS).groups()]; LD=re.search(r' d="([^"]+)"',LS).group(1)
def lion(x,y,w,c): s=w/LV[0]; return f'<path d="{LD}" fill="{c}" fill-rule="evenodd" transform="translate({x:.2f} {y:.2f}) scale({s:.5f})"/>'
# colourways, as the soaps: (bloom edge, bloom core, throat, paper), ink, deep
CW={'teal':(('#1C5A57','#CFE7DF','#D8A84A','#EDF0E7'),'#123B39','#2F6E6A'),
    'tea': (('#5A2614','#F2D6BC','#D99A3E','#F3ECE2'),'#3A1A0E','#7A4528')}
def hx(c): return np.array([int(c[i:i+2],16) for i in (1,3,5)],np.float32)
def layer(k,i,R_,blur):
    e,c,t,_=CW[k][0]; Sz=int(R_*2.4); n=O+f'L-{k}-{i}'
    if not os.path.exists(n+'.png'): bloom.bloom(n,Sz,Sz,Sz/2,Sz/2,R_,e,c,t,None,blur=blur,grain=0)
    return Image.open(n+'.png')
def place(base,im,rot,cx,cy,alpha=1.0):
    im=im.rotate(rot,resample=Image.BICUBIC); im=im.resize((int(im.size[0]*K/KR),)*2,Image.LANCZOS)
    m=im.getchannel('A') if alpha>=1 else im.getchannel('A').point(lambda v:int(v*alpha))
    base.paste(im,(int(cx*K-im.size[0]/2),int(cy*K-im.size[1]/2)),m)
def grain(a,seed):
    h,w=a.shape[:2]; rng=np.random.default_rng(seed)
    mott=np.asarray(Image.fromarray(rng.normal(128,40,(h//36+1,w//36+1)).clip(0,255).astype(np.uint8)).resize((w,h),Image.BICUBIC)).astype(np.float32)-128
    a*=(1+0.008*mott/40)[...,None]; a+=rng.normal(0,9,(h,w,1))+rng.normal(0,2.5,(h,w,3))
    tooth=np.asarray(Image.fromarray(rng.normal(128,40,(h,w)).clip(0,255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.0))).astype(np.float32)-128
    return a+0.3*tooth[...,None]
def art(k):
    """front + brew side as one strip so the bloom wraps the corner; lid and back carry a faint ghost of it"""
    g=CW[k][0][3]; W,H=B+FW+SW+B,FH+2*B; w,h=int(W*K),int(H*K)
    base=Image.new('RGBA',(w,h),tuple(int(v) for v in hx(g))+(255,))
    place(base,layer(k,'s',17,2.2),22,B+106,B+14)                              # the small one, top, near the name
    bg=layer(k,'b',82,5.2); place(base,bg,-10,B+134,B+38); place(base,bg,-10,B+134,B+38,0.5)   # the huge one, round the corner
    a=np.asarray(base.convert('RGB')).astype(np.float32)
    yy,xx=np.mgrid[0:h,0:w].astype(np.float32)/K-B
    fx=np.clip(xx,0,FW); fy=np.clip(yy,0,FH)
    left=np.clip((100-fx)/58,0,1); left=left*left*(3-2*left); low=np.clip((fy-52)/28,0,1)**1.4
    vf=np.maximum(left*0.82,low*0.86)                                         # the soap's veil: paper behind the type
    vs=np.clip((xx-FW)/10,0,1)*0.62                                            # the brew side quieter, as the soap's walls
    v=np.where(xx>FW,np.maximum(vs,low*0.86),vf)
    a=a*(1-v[...,None])+hx(g)*v[...,None]
    a=grain(a,11); out=a.clip(0,255).astype(np.uint8)
    Image.fromarray(out[:,:int((FW+2*B)*K)]).save(O+f'{k}-front.jpg',quality=94)
    Image.fromarray(out[:,int((FW+B)*K):]).save(O+f'{k}-side.jpg',quality=94)
    for nm,(fw,fh,cx,cy,R_,rot,veil) in {'lid':(FW,LH,FW*0.74,LH*0.6,70,30,0.8),'back':(FW,FH,FW*0.18,FH*0.3,60,-40,0.86)}.items():
        ww,hh=int((fw+2*B)*K),int((fh+2*B)*K); b2=Image.new('RGBA',(ww,hh),tuple(int(v) for v in hx(g))+(255,))
        L=layer(k,'b',82,5.2); sz=int(L.size[0]*R_/82); place(b2,L.resize((sz,sz),Image.LANCZOS),rot,B+cx,B+cy)
        a=np.asarray(b2.convert('RGB')).astype(np.float32); a=a*(1-veil)+hx(g)*veil; a=grain(a,13)
        Image.fromarray(a.clip(0,255).astype(np.uint8)).save(O+f'{k}-{nm}.jpg',quality=94)

def face(name,fw,fh,bgimg,o):
    W,H=fw+2*B,fh+2*B
    s=(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W*K:.0f}" height="{H*K:.0f}" viewBox="{-B} {-B} {W} {H}"><defs>{FOILG}</defs>'
       f'<image href="file://{O}{bgimg}" x="{-B}" y="{-B}" width="{W}" height="{H}" preserveAspectRatio="none"/>'+''.join(o)+'</svg>')
    open(O+name+'.html','w').write(f'<html><head><style>{css}html,body{{margin:0}}svg{{display:block}}</style></head><body>{s}</body></html>')
    return [O+name,int(W*K),int(H*K)]
def front(k):
    c,d=CW[k][1],CW[k][2]; x=12; o=[]
    o.append(logo(x+9,16.5,18,c))
    o.append(rule(x+21.5,9.5,x+21.5,23.5,c,0.2,0.45)); o.append(lion(x+25,10.6,17,c))       # tea's certification, as on every Ceylon pack
    o.append(f'<text x="{x-0.8}" y="47" font-family="ISR" font-size="23"><tspan fill="url(#foil)">Vanilla</tspan></text>')
    o.append(txt('Tea',x-0.8,66,23,c,'IS'))
    o.append(caps('CEYLON BLACK TEA WITH NATURAL VANILLA',x,76.4,2.3,c,tr=0.13))
    o.append(caps('25 TEA BAGS',FW-12,76.4,2.3,c,'end',0.13))
    o.append(txt('Made with vanilla grown on our own farms.',x,81.2,4.2,c,'IS'))
    o.append(caps('NET WT. 50 g',FW-12,81.2,4.6,c,'end',0))
    return face(f'{k}-F',FW,FH,f'{k}-front.jpg',o)
def side(k):
    c,d=CW[k][1],CW[k][2]; x=10; r=SW-10; o=[]
    o.append(txt('How to brew',x,17,7.0,c,'IS')); o.append(rule(x,21,r,21,c,0.2,0.5))
    steps=[('01','150 ML','One tea bag in freshly boiled water.'),('02','5 MINUTES','Steep, then lift the bag out.'),('03','OVER ICE','Let it cool and pour over ice.')]
    for i,(nn,h,t) in enumerate(steps):
        y=29+i*14.5
        o.append(txt(nn,x,y+3.2,7.0,d,'ISR')); o.append(caps(h,x+13,y,2.3,c,tr=0.16)); o.append(txt(t,x+13,y+4.4,2.4,c,'G'))
        o.append(rule(x,y+8.2,r,y+8.2,c,0.15,0.35))
    o.append(rule(x,FH-14,r,FH-14,c,0.2,0.5))
    o.append(caps('25 TEA BAGS · 2 G EACH',x,FH-9.5,1.9,c,tr=0.2)); o.append(caps('NET WT. 50 g',r,FH-9.5,1.9,c,'end',0.2))
    o.append(caps('PRODUCT OF SRI LANKA',x,FH-5.6,1.5,d,tr=0.25))
    return face(f'{k}-S',SW,FH,f'{k}-side.jpg',o)
def lid(k):
    c,d=CW[k][1],CW[k][2]; o=[]; cx=FW/2
    o.append(logo(cx,LH/2-6,22,c))
    o.append(caps('AUTHENTIC CEYLON VANILLA TEA',cx,LH/2+12,2.2,c,'middle',0.3))
    o.append(rule(cx-40,LH/2+15.5,cx+40,LH/2+15.5,c,0.2,0.45))
    o.append(caps('SAVOUR THE CALM',cx,LH/2+20,1.6,d,'middle',0.35))
    return face(f'{k}-L',FW,LH,f'{k}-lid.jpg',o)
def back(k):
    c,d=CW[k][1],CW[k][2]; W=FW; o=[]
    o.append(txt('Vanilla was never plain.',W/2,15,7.4,c,'IS','middle')); o.append(rule(10,20.5,W-10,20.5,c,0.2,0.5))
    cw=48; xs=(10,10+cw+8,10+2*(cw+8)); y0=27
    o.append(caps('THE TEA',xs[0],y0,1.4,d,tr=0.25)); o.append(caps("WHAT'S INSIDE",xs[1],y0,1.4,d,tr=0.25)); o.append(caps('STORAGE',xs[2],y0,1.4,d,tr=0.25))
    p,_=para('The delicate sweetness of natural vanilla unfolds through warm, comforting notes and a smooth, mellow aroma.',xs[0],y0+4.6,cw,2.3,3.2,c); o+=p
    p,_=para('25 tagged, unbleached sachet tea bags of Ceylon black tea with natural vanilla.',xs[1],y0+4.6,cw,2.3,3.2,c); o+=p
    p,_=para('Keep in a cool, dry place, away from strong odours. Close the box after use.',xs[2],y0+4.6,cw,2.3,3.2,c); o+=p
    for xx in (xs[1]-4,xs[2]-4): o.append(rule(xx,y0-2.5,xx,58,c,0.15,0.35))
    o.append(rule(10,64,W-10,64,c,0.2,0.5))
    o.append(caps('MARKETED BY',10,70,1.3,d,tr=0.25))
    for i,l in enumerate(['Agroventures Exports (Pvt) Ltd','No 48, Sir Marcus Fernando Mawatha, Colombo 07','www.agroventuresexports.com  ·  Hotline +94 11 218 7287']):
        o.append(txt(l,10,73.4+i*2.6,1.95 if i else 2.05,c,'GB' if i==0 else 'G'))
    o.append(logo(W-20,73,15,c))
    return face(f'{k}-B',FW,FH,f'{k}-back.jpg',o)
if __name__=='__main__':
    man=[]
    for k in sys.argv[1:] or CW:
        art(k); man+=[front(k),side(k),lid(k),back(k)]
    json.dump(man,open(O+'faces.json','w')); print('ok')
