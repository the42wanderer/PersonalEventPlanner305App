# Vanilla Tea cartons, round 5: branch 3.2 built in. The brew side and the back share one teal ground; "Vanilla Tea"
# in the italic runs margin to margin across both, on the 10 mm foot ("Tea" a tone lighter); and the botanical there is
# drawn in the same single tone, like shadows on the teal: tea shoots, the vanilla vine with its flower, pods at the foot.
import sys, json, math, numpy as np
from PIL import Image, ImageDraw, ImageFont
S='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/'
sys.path.insert(0,S+'teasoap'); sys.path.insert(0,S+'teaart')
import build as b
from build import logo, txt, caps, rule, para, lion, face, grain, hx, B
from build2 import shoot, vleaf, laid_on, CW, K
from build3 import BOX, washi
import build4 as b4
from build4 import estate
from foliage2 import paint_flower, paint_pod, paint_vbud, Paint
O=b.O; IS='/home/user/PersonalEventPlanner305App/vanilla-shop/fonts/instrument-serif-italic.ttf'
TEA_TONE='#2D6C68'
def fit(text,mm):
    f=ImageFont.truetype(IS,400); bb=f.getbbox(text); return ImageFont.truetype(IS,int(400*mm*K/(bb[2]-bb[0])))
def mask(h,w,text,fnt,x,y):
    m=Image.new('L',(w,h),0); bb=fnt.getbbox(text); ImageDraw.Draw(m).text((x*K-bb[0],y*K),text,font=fnt,fill=255,anchor='ls')
    return np.asarray(m).astype(np.float32)/255
def silhouette(h,w,paint):
    """paint the botanical, keep only its shape: one flat tone, like a shadow"""
    c0=np.zeros((h,w,3),np.float32); c1=np.full((h,w,3),255.0,np.float32); paint(c0); paint(c1)
    return np.clip(1-(c1-c0).mean(2)/255,0,1)
def teapot(h,w,cx,base,s=1.0,tilt=28):
    """a big teapot, one flat tone, tipped forward as if about to pour: round body, domed lid and knob, a long swan
    spout dipping left, a loop handle; the lid seam and a belly band cut out as fine lines, like the soap's watermark"""
    import draw
    ss=3; im=Image.new('L',(w*ss,h*ss),0); d=ImageDraw.Draw(im); P=lambda x,y:((cx+x*s)*K*ss,(base+y*s)*K*ss)
    t=np.linspace(0,2*np.pi,200); body=[P(23*np.cos(a),-17-16.5*np.sin(a)) for a in t]
    body=[(x,min(y,P(0,-1.2)[1])) for x,y in body]; d.polygon(body,fill=255)                  # flat-bottomed belly
    d.polygon([P(-14,-3.2),P(14,-3.2),P(11,0),P(-11,0)],fill=255)                             # the foot
    d.polygon([P(15*np.cos(a),-31.5-6.5*np.sin(a)) for a in np.linspace(0,np.pi,60)],fill=255)   # the lid
    d.ellipse([P(-2.6,-41.2),P(2.6,-36.4)],fill=255); d.polygon([P(-1.3,-37.4),P(1.3,-37.4),P(1.8,-36),P(-1.8,-36)],fill=255)
    rib=draw.ribbon(draw.cr([(-19,-12),(-28,-17),(-33,-27),(-38,-35)],16),lambda u:3.6*(1-u)+0.9)   # the spout
    d.polygon([P(x,y) for x,y in rib],fill=255)
    rib=draw.ribbon(draw.cr([(20,-27),(30,-31),(35,-22),(31,-12),(20,-8)],16),lambda u:1.9)       # the handle
    d.polygon([P(x,y) for x,y in rib],fill=255)
    lw=max(1,int(0.28*s*K*ss))
    d.line([P(15*np.cos(a),-31.5+0.6*np.sin(a)) for a in np.linspace(np.pi,2*np.pi,40)],fill=0,width=lw)   # lid seam
    for off in (-14.5,-13.3): d.line([P(x,off+1.8*np.sqrt(max(0,1-(x/23)**2))) for x in np.linspace(-22.2,22.2,60)],fill=0,width=max(1,lw//2))
    im=im.rotate(tilt,resample=Image.BICUBIC,center=P(-11,0))                                 # tipped on its front foot
    return np.asarray(im.resize((w,h),Image.BOX)).astype(np.float32)/255
def art(box,k='teal'):
    d=BOX[box]; FW,FH,SW,LH,SPLIT=d['FW'],d['FH'],d['SW'],d['LH'],d['SPLIT']; p=CW[k]; L=p['leaves']
    W,H=B+FW+SW+FW+B,FH+2*B; w,h=int(W*K),int(H*K); P=Paint(W,H,seed=3); f=B+FW; g=f+SW   # g: the fold onto the back
    img=np.ones((h,w,3),np.float32)*hx(p['band'])
    # the shadows on the brew side and back, in the word's tone
    def shade_paint(c):
        if box=='long':
            shoot(P,c,(g+FW+4,B-4),148,70,0.3,24,L,'#000000',22,-1)
            vleaf(P,c,(g+40,B+FH+6),-70,62,7,0.25,'#000000')
            paint_flower(P,c,(g+FW-46,B+30),210,2.2); paint_vbud(P,c,(g+FW-74,B+20),-120,7); paint_vbud(P,c,(g+FW-30,B+52),40,6)
        else:
            shoot(P,c,(g+FW+4,B-4),146,52,0.3,19,L,'#000000',22,-1)
            paint_flower(P,c,(g+FW-26,B+32),210,1.6); paint_vbud(P,c,(g+FW-46,B+22),-120,5.5)
    sh=silhouette(h,w,shade_paint); xx=np.arange(w,dtype=np.float32)[None,:]/K; sh*=(xx>f)
    sh=np.maximum(sh,teapot(h,w,g-11,B+46,0.82)*(xx>f))                         # beside the steps, pouring towards them, the handle round the fold
    img=img*(1-sh[...,None])+hx(p['word'])*sh[...,None]
    # Vanilla Tea, margin to margin across the brew side and the back, on the 10 mm foot
    fnt=fit('Vanilla Tea',(g+FW-10)-(f+10)); m1=mask(h,w,'Vanilla',fnt,f+10,B+FH-10); mall=mask(h,w,'Vanilla Tea',fnt,f+10,B+FH-10)
    img=img*(1-m1[...,None])+hx(p['word'])*m1[...,None]; m2=np.clip(mall-m1,0,1); img=img*(1-m2[...,None])+hx(TEA_TONE)*m2[...,None]
    # the front, as before
    if box=='long':
        vleaf(P,img,(B+SPLIT+4,B+92),-62,70,8.5,0.25,'#2A5240'); vleaf(P,img,(f+2,B+96),-118,64,7.5,-0.2,'#33604A')
        shoot(P,img,(f-3,B-4),134,56,0.3,25,L[1:],'#CFE0C2',3,1); shoot(P,img,(B+SPLIT+10,B+97),-78,66,0.35,26,L,'#CFE0C2',5,1)
        shoot(P,img,(f-4,B+97),-118,56,-0.25,24,L[1:],'#CFE0C2',8,-1)
        over=lambda c:([paint_pod(P,c,*q) for q in [((B+SPLIT-14,B+86),-17,76,2.3,0.12,0),((B+SPLIT-9,B+91),-24,68,2.0,0.08,0)]],
                       [paint_vbud(P,c,*q) for q in [((f-20,B+20),-60,7.5),((B+SPLIT+12,B+30),200,6.5)]],paint_flower(P,c,(f-37,B+46),38,2.6))
    else:
        vleaf(P,img,(B+SPLIT+3,B+92),-64,52,6.5,0.25,'#2A5240'); vleaf(P,img,(f+2,B+96),-118,48,5.8,-0.2,'#33604A')
        shoot(P,img,(B+SPLIT+6,B+97),-80,50,0.35,19,L,'#CFE0C2',5,1); shoot(P,img,(f-3,B+97),-116,42,-0.25,18,L[1:],'#CFE0C2',8,-1)
        over=lambda c:(shoot(P,c,(f+6,B-3),158,52,0.35,19,L[1:],'#CFE0C2',3,1),
                       [paint_pod(P,c,*q) for q in [((B+SPLIT-6,B+87),-19,34,1.6,0.12,0),((B+SPLIT-3,B+91),-27,30,1.4,0.08,0)]],
                       [paint_vbud(P,c,*q) for q in [((f-10,B+24),-60,5.5)]],paint_flower(P,c,(f-27,B+56),38,1.85))
    img,cream=washi(img,p,SPLIT)
    if box=='long':
        es=estate(h,w,-B,[(60,[(62,18,14,0.2),(84,30,13,-0.15),(110,22,16,0.1)],0.02,0.95,0.24,0.26),
                          (69,[(56,10,16,0.0),(100,17,15,0.25),(124,12,12,0.0)],0.025,1.25,0.31,0.3),
                          (84,[(92,22,20,0.2)],0.03,1.75,0.42,0.36)],trees=[(84,7.0),(94,8.5),(103,6.5)])
        xs=np.arange(w,dtype=np.float32)[None,:]/K-B; fx=np.clip((xs-46)/30,0,1); fx=fx*fx*(3-2*fx)
        A=es*fx*cream; img=img*(1-A[...,None])+hx(p['band'])*A[...,None]
    img=laid_on(img,over); img=grain(img,17); out=img.clip(0,255).astype(np.uint8)
    Image.fromarray(out[:,:int((FW+2*B)*K)]).save(O+f'{box}5-front.jpg',quality=94)
    Image.fromarray(out[:,int((FW+B)*K):int((FW+SW+2*B)*K)]).save(O+f'{box}5-side.jpg',quality=94)
    Image.fromarray(out[:,int((FW+SW+B)*K):]).save(O+f'{box}5-back.jpg',quality=94)
    b4.O=O; b4.art.__globals__  # lid stays as round 4
def back(box,k='teal'):
    d=BOX[box]; FW,FH=d['FW'],d['FH']; p=CW[k]; c=p['lt']; o=[]
    if box=='long':
        o.append(txt('Vanilla was never plain.',10,15,6.4,c,'IS')); o.append(rule(10,18.6,FW-10,18.6,c,0.2,0.6))
        cw=46; xs=[10+i*(cw+9) for i in range(3)]; y0=25
        cols=(('THE TEA','The delicate sweetness of natural vanilla unfolds through warm, comforting notes and a smooth, mellow aroma.'),
              ("WHAT'S INSIDE",'25 tagged, unbleached sachet tea bags of Ceylon black tea with natural vanilla.'),
              ('STORAGE','Keep in a cool, dry place, away from strong odours. Close the box after use.'))
    else:
        o.append(txt('Vanilla was never plain.',8,14,5.2,c,'IS')); o.append(rule(8,17.6,FW-8,17.6,c,0.2,0.6))
        cw=33; xs=[8,8+cw+5.6]; y0=24
        cols=(('THE TEA','The delicate sweetness of natural vanilla unfolds through warm, comforting notes and a smooth, mellow aroma.'),
              ("WHAT'S INSIDE",'12 tagged, unbleached sachet tea bags of Ceylon black tea with natural vanilla.'))
    for xx,(hd,t) in zip(xs,cols):
        o.append(caps(hd,xx,y0,1.6,c,tr=0.2)); pp,_=para(t,xx,y0+4.4,cw,2.1,3.0,c); o+=pp
    for xx in xs[1:]: o.append(rule(xx-(4.5 if box=='long' else 2.8),y0-2.4,xx-(4.5 if box=='long' else 2.8),46,c,0.15,0.4))
    o.append(rule(10 if box=='long' else 8,49.5,FW-(10 if box=='long' else 8),49.5,c,0.2,0.6))
    return face(f'{box}5-B',FW,FH,f'{box}5-back.jpg',o)
def front(box): r=b4.front(box); return rename(r,box,'F')
def side(box): r=b4.side(box); return rename(r,box,'S')
def rename(r,box,n):
    src=open(r[0]+'.html').read().replace(f'{box}4-front.jpg',f'{box}5-front.jpg').replace(f'{box}4-side.jpg',f'{box}5-side.jpg')
    nm=O+f'{box}5-{n}'; open(nm+'.html','w').write(src); return [nm,r[1],r[2]]

def lid_art(box,k='teal'):
    """the lid: one gesture in the shadow tone, a tea shoot sweeping from the front-left corner to a vanilla flower
    cropped by the far edge; nothing else"""
    d=BOX[box]; FW,LH=d['FW'],d['LH']; p=CW[k]; L=p['leaves']; s=1 if box=='long' else 0.62
    W,H=FW+2*B,LH+2*B; w,h=int(W*K),int(H*K); P=Paint(W,H,seed=9)
    a=np.ones((h,w,3),np.float32)*hx(p['band'])
    def g(c):
        shoot(P,c,(B-4,B+LH+4),-22,FW*0.95,-0.42,24*s+4,L,'#000000',31,1)
        vleaf(P,c,(B+FW*0.45,B+LH+6),-48,58*s+10,7*s+1.5,0.3,'#000000')
        paint_flower(P,c,(B+FW-20*s-6,B+18*s+4),205,2.5*s+0.5); paint_vbud(P,c,(B+FW-58*s-6,B+10*s+3),-100,7*s+1.5)
    sh=silhouette(h,w,g); a=a*(1-sh[...,None])+hx(p['word'])*sh[...,None]; a=grain(a,19)
    Image.fromarray(a.clip(0,255).astype(np.uint8)).save(O+f'{box}5-lid.jpg',quality=94)
def lid(box,k='teal'):
    d=BOX[box]; FW,LH=d['FW'],d['LH']; p=CW[k]; c=p['lt']; o=[]
    x=12 if box=='long' else 8; s=1 if box=='long' else 0.8; cy=LH/2-4
    o.append(logo(x+11*s,cy-8*s,22*s,c))                                     # left on the front's margin, as the column below
    o.append(caps('AUTHENTIC CEYLON VANILLA TEA',x,cy+10*s,2.1*s,c,tr=0.3)); o.append(rule(x,cy+13.4*s,x+76*s,cy+13.4*s,c,0.2,0.55))
    o.append(caps('SAVOUR THE CALM',x,cy+18*s,1.6*s,c,tr=0.35))
    return face(f'{box}5-L',FW,LH,f'{box}5-lid.jpg',o)


EMB=open('/home/user/PersonalEventPlanner305App/vanilla-shop/brand/emblem/vanilla-shop-emblem-savor-the-calm_cream.svg').read()
EMB=EMB[EMB.index('>',EMB.index('<svg'))+1:EMB.rindex('</svg>')]
def lid_art(box,k='teal'):
    """the lid: one gesture in the shadow tone behind the emblem: a tea shoot sweeping in from the front-left corner,
    a vanilla flower cropped by the far edge"""
    d=BOX[box]; FW,LH=d['FW'],d['LH']; p=CW[k]; L=p['leaves']; s=1 if box=='long' else 0.62
    W,H=FW+2*B,LH+2*B; w,h=int(W*K),int(H*K); P=Paint(W,H,seed=9)
    a=np.ones((h,w,3),np.float32)*hx(p['band'])
    def g(c):
        shoot(P,c,(B-4,B+LH+4),-24,FW*0.62,-0.35,24*s+4,L,'#000000',31,1)
        vleaf(P,c,(B+FW+6,B+LH*0.75),-170,58*s+12,7*s+1.5,0.3,'#000000')
        paint_flower(P,c,(B+FW-18*s-4,B+16*s+3),205,2.5*s+0.5); paint_vbud(P,c,(B+FW-52*s-6,B+8*s+3),-100,7*s+1.5)
    sh=silhouette(h,w,g); a=a*(1-sh[...,None])+hx(p['word'])*sh[...,None]; a=grain(a,19)
    Image.fromarray(a.clip(0,255).astype(np.uint8)).save(O+f'{box}5-lid.jpg',quality=94)
def lid(box,k='teal'):
    d=BOX[box]; FW,LH=d['FW'],d['LH']; dia=LH*0.66; sc=dia/250
    o=[f'<g transform="translate({FW/2-dia/2:.2f} {LH/2-dia/2:.2f}) scale({sc:.5f})">{EMB}</g>']   # the emblem, the box's seal
    return face(f'{box}5-L',FW,LH,f'{box}5-lid.jpg',o)

if __name__=='__main__':
    man=[]
    for box in (sys.argv[1:] or BOX): art(box); lid_art(box); man+=[front(box),side(box),back(box),lid(box)]
    json.dump(man,open(O+'faces5.json','w')); print('ok')
