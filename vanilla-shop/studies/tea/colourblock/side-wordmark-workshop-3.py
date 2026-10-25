# Workshop, branch 3: the italic name sitting on the brew side's foot and wrapping onto the back, grown five ways.
import sys, json, numpy as np
from PIL import Image, ImageDraw, ImageFont
S='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/'
sys.path.insert(0,S+'teasoap'); sys.path.insert(0,S+'teaart')
import workshop as ws
from workshop import brew, back, txt, B, css, SW, FW, FH, W, O, p, LT, WD
from build import grain, hx, FOILG
from build2 import shoot, laid_on, K
from foliage2 import Paint, paint_flower, paint_vbud
import draw
IS='/home/user/PersonalEventPlanner305App/vanilla-shop/fonts/instrument-serif-italic.ttf'
L=p['leaves']; BASE=B+FH-10; X0=B+8.5; RIGHT=B+W-10
def fit(text,target_mm):
    f=ImageFont.truetype(IS,400); bb=f.getbbox(text); s=int(400*target_mm*K/(bb[2]-bb[0])); return ImageFont.truetype(IS,s)
def word_mask(h,w,text,fnt,x,y):
    m=Image.new('L',(w,h),0); bb=fnt.getbbox(text); ImageDraw.Draw(m).text((x*K-bb[0],y*K),text,font=fnt,fill=255,anchor='ls')
    return np.asarray(m).astype(np.float32)/255
def canvas():
    h,w=int((FH+2*B)*K),int((W+2*B)*K); return np.ones((h,w,3),np.float32)*hx(p['band']),h,w
def put(img,m,col,a=1.0): return img*(1-m[...,None]*a)+hx(col)*m[...,None]*a
def save(img,name): img=grain(img,23); Image.fromarray(img.clip(0,255).astype(np.uint8)).save(O+name+'.jpg',quality=92)

def v0():   # the original 3, for reference
    img,h,w=canvas(); f=ImageFont.truetype(IS,int(48*K*1.0)); img=put(img,word_mask(h,w,'Vanilla',f,X0,BASE),WD); save(img,'w3-0')
def v1():   # margin to margin
    img,h,w=canvas(); f=fit('Vanilla',RIGHT-X0); img=put(img,word_mask(h,w,'Vanilla',f,X0,BASE),WD); save(img,'w3-1')
def v2():   # the full name, Tea a tone lighter
    img,h,w=canvas(); f=fit('Vanilla Tea',RIGHT-X0); bb=f.getbbox('Vanilla ')
    m1=word_mask(h,w,'Vanilla',f,X0,BASE); full=word_mask(h,w,'Vanilla Tea',f,X0,BASE); m2=np.clip(full-m1,0,1)
    img=put(img,m1,WD); img=put(img,m2,'#2D6C68'); save(img,'w3-2')
def v3():   # a tea shoot woven through the letters, a flower resting on the last a
    img,h,w=canvas(); P=Paint(W+2*B,FH+2*B,seed=6); f=fit('Vanilla',RIGHT-X0)
    shoot(P,img,(B+SW-34,B+FH+8),-14,140,-0.18,19,L,'#CFE0C2',4,1)            # behind the word, along the foot
    img=put(img,word_mask(h,w,'Vanilla',f,X0,BASE),WD)
    img=laid_on(img,lambda c:(shoot(P,c,(B+SW+96,B+FH+6),-30,46,0.3,16,L[1:],'#CFE0C2',7,-1),   # in front of it, below the rule
                              paint_flower(P,c,(RIGHT-6,BASE-8),200,1.15),paint_vbud(P,c,(RIGHT-24,BASE-14),-40,4.5)))
    save(img,'w3-3')
def v4():   # the word as a window onto tea leaves, tone on tone
    img,h,w=canvas(); f=fit('Vanilla',RIGHT-X0); m=word_mask(h,w,'Vanilla',f,X0,BASE)
    field=np.ones_like(img)*hx('#245E5B'); P=Paint(W+2*B,FH+2*B,seed=8); rng=np.random.default_rng(3)
    cols=('#3A8277','#1B4E4A','#4A9083','#2E6E66')
    for i in range(26):
        shoot(P,field,(B+rng.uniform(-10,W+10),B+FH+8),rng.uniform(-130,-50),rng.uniform(40,90),rng.uniform(-0.4,0.4),rng.uniform(14,22),cols,'#3F8077',i,1)
    img=img*(1-m[...,None])+field*m[...,None]; save(img,'w3-4')
def v5():   # tone, with the soap's gold stroke under it (the swash is drawn in the SVG, in foil)
    img,h,w=canvas(); f=fit('Vanilla',RIGHT-X0); img=put(img,word_mask(h,w,'Vanilla',f,X0,BASE),WD); save(img,'w3-5')
def swash():
    pts=[(SW+40,FH-5.2),(SW+80,FH-6.6),(SW+120,FH-6.0),(SW+150,FH-7.4),(SW+164,FH-9.8)]
    sp=draw.cr(pts,14); rib=draw.ribbon(sp,lambda t:1.15*(t**0.5)*(1-t)**0.35+0.04)
    d='M'+' L'.join(f'{x:.2f} {y:.2f}' for x,y in rib)+'Z'
    return f'<path d="{d}" fill="url(#foil)"/>'

def v6():   # the original size, its right end set on the back's second column rule
    img,h,w=canvas(); f=fit('Vanilla',(B+SW+10+2*(46+9)-4.5)-X0); img=put(img,word_mask(h,w,'Vanilla',f,X0,BASE),WD); save(img,'w3-6')
def strip(name,bg,note,extra=''):
    o=[f'<defs>{FOILG}</defs><image href="file://{O}{bg}.jpg" x="{-B}" y="{-B}" width="{W+2*B}" height="{FH+2*B}" preserveAspectRatio="none"/>',extra]
    brew(o); back(o)
    o.append(f'<path d="M{SW} {-B}V{FH+B}" stroke="#FFFFFF" stroke-opacity=".25" stroke-width="0.2" stroke-dasharray="1 1"/>')
    k=8; s=(f'<svg xmlns="http://www.w3.org/2000/svg" width="{(W+2*B)*k:.0f}" height="{(FH+2*B+14)*k:.0f}" viewBox="{-B} {-B} {W+2*B} {FH+2*B+14}">'
            f'<rect x="{-B}" y="{FH+B}" width="{W+2*B}" height="14" fill="#fff"/>'+''.join(o)+txt(note,0,FH+B+8.5,3.4,'#222','G')+'</svg>')
    open(O+name+'.html','w').write(f'<html><head><style>{css}html,body{{margin:0}}svg{{display:block}}</style></head><body>{s}</body></html>')
    return [O+name,int((W+2*B)*k),int((FH+2*B+14)*k)]
if __name__=='__main__':
    for f in (v0,v1,v2,v3,v4,v5,v6): f()
    man=[strip('w3s-0','w3-0','3 · the original: italic on the foot, from the margin'),
         strip('w3s-1','w3-1','3.1 · margin to margin: the italic sized to end on the back\'s right margin'),
         strip('w3s-2','w3-2','3.2 · the full name, Vanilla Tea, margin to margin; Tea a tone lighter'),
         strip('w3s-3','w3-3','3.3 · a tea shoot woven through the letters, behind and in front; a flower resting on the last a'),
         strip('w3s-4','w3-4','3.4 · the word as a window onto tea leaves, tone on tone'),
         strip('w3s-5','w3-5','3.5 · the soap\'s gold stroke under the word, in foil',swash()),
         strip('w3s-6','w3-6','3.6 · the original\'s scale, its right end set on the back\'s second column rule')]
    json.dump(man,open(O+'w3.json','w')); print('ok')
