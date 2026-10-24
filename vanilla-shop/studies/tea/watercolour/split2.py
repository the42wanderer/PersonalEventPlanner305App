# Vanilla tea, Split refined (art-direction brief): one watercolour language for the whole tea range.
#  - layered depth: a crisper hero flower in front, a soft bloom and buds behind, leaves and pods between
#  - pigment gathers at the edges of each wash (as watercolour dries) instead of a digital glow
#  - pods: always the same pair of cured pods crossing low; flowers: always one hero, one soft echo
#  - the pattern on the cream (after Song Chao) is drawn from the same shapes as hairlines, and one vine runs out of
#    the teal and carries on in hairline across the cream: the only crossing of the boundary
import sys, math
sys.path.insert(0,'/home/user/PersonalEventPlanner305App/vanilla-shop/studies/extract/split')
sys.path.insert(0,'/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/teaart')
import numpy as np
from PIL import Image, ImageDraw
import draw
from draw import Canvas, leaf, pod, bud, stem, tepal, ellipse_ruffle
from comp import flower, mix, sheen
from teaflower import PAL
O='/home/user/PersonalEventPlanner305App/vanilla-shop/studies/tea/watercolour/split2/'
K=draw.K; B=3; PAPER=np.array([0xF6,0xEE,0xDC],np.float32)
TEAL=dict(PAL['teal']); TEAL['line']='#6E9A93'
CIN=dict(ground='#7C3D22',tep_core='#FFF6E8',tep_edge='#E9B48C',lip_core='#FFFAF0',lip_edge='#F6D9B8',throat_core='#F3C75E',throat_edge='#D69B3A',
         leaf_core='#A97A4C',leaf_edge='#4A2010',pod_core='#3A1C0E',pod_edge='#1C0E07',tea_core='#BFD48A',tea_edge='#3E5E2A',
         tbud_core='#EEF4D2',tbud_edge='#A9C27A',tstem='#93AE6C',line='#B48C6C',quill_core='#D98A4E',quill_edge='#7A3416')
class WC(Canvas):
    """every wash dries with pigment at its edge; less halo, so nothing glows"""
    def add(s,polys,core,edge,blur,depth=1.0,alpha=1.0,glow=1.0,centre=None,R=None,halo=0.12,wash=None):
        if wash is None: wash=(mix(edge,'#000000',0.18),0.32,0.32)
        super().add(polys,core,edge,blur,depth,alpha,glow,centre,R,halo,wash)
def flush(cv,p,base,ang,s,blur=0.7,alpha=1.0):
    a=math.radians(ang); P=lambda d,o=0:(base[0]+math.cos(a)*d*s-math.sin(a)*o*s, base[1]+math.sin(a)*d*s+math.cos(a)*o*s)
    tip=P(26); m1=P(9,0.8); m2=P(17,-0.6)
    cv.add([stem([base,m1,m2,tip],0.6*s)],mix(p['tstem'],'#FFFFFF',0.2),p['tstem'],blur*0.8,alpha=alpha)
    lv=[(m1,ang-62,19*s,5.6*s,-0.3),(m2,ang+52,15*s,4.6*s,0.28)]
    cv.add([leaf(*q) for q in lv],p['tea_core'],p['tea_edge'],blur,alpha=alpha,glow=1.1)
    sheen(cv,[leaf(*q,spine=True) for q in lv],0.38*s,mix(p['tea_core'],'#FFFFFF',0.4),p['tea_core'],blur,0.5*alpha)
    cv.add([bud(tip,ang-6,9*s,2.0*s,0.12)],p['tbud_core'],p['tbud_edge'],blur*0.8,alpha=alpha,glow=1.3)
def pod_pair(cv,p,base,ang,L,w):
    """the range's pods: always two cured pods, crossing, the front one longer"""
    q=[(base,ang,L,w,0.12,1),((base[0]+6,base[1]+4),ang-9,L*0.9,w*0.85,0.08,-1)]
    cv.add([pod(*x) for x in q],p['pod_core'],p['pod_edge'],0.45,glow=0.9)
    sheen(cv,[pod(*x,spine=True)[3:-6]+np.array([0,-0.25*x[3]]) for x in q],0.28*w,mix(p['pod_core'],'#FFFFFF',0.35),p['pod_core'],0.4,0.55)
def quills(cv,p,base,ang,L,w):
    """two cinnamon quills: a rolled bark with its scroll end"""
    out=[]
    for i,(dx,dy,da,f) in enumerate(((0,0,0,1),(5,-4,7,0.86))):
        a=math.radians(ang+da); b=(base[0]+dx,base[1]+dy); e=(b[0]+math.cos(a)*L*f,b[1]+math.sin(a)*L*f)
        body=draw.ribbon(draw.cr([b,((b[0]+e[0])/2,(b[1]+e[1])/2),e],12),lambda t:w)
        cv.add([body],p['quill_core'],p['quill_edge'],0.4,glow=0.8)
        cv.add([ellipse_ruffle(e,w*1.05,w*0.8,ang+da,0.0,1)],mix(p['quill_core'],'#FFFFFF',0.25),p['quill_edge'],0.35)
        cv.add([draw.ribbon(draw.cr([b,e],10),lambda t:w*0.18)],mix(p['quill_edge'],'#000000',0.2),p['quill_edge'],0.3,alpha=0.6,wash=False)
def echo(cv,p,c,ang,s):
    """the soft echo behind the hero: a second bloom, out of focus"""
    flower(cv,c,ang,s,p,blurs=(0.85,0.75,0.95))
def vine(cv,p,pts,w=0.75):
    cv.add([stem(pts,w)],mix(p['tstem'],'#FFFFFF',0.1),p['tstem'],0.5)
# ------------------------------------------------------------------ hairline pattern (after Song Chao)
def outline_layer(Wmm,Hmm,shapes,col,width_mm=0.22,ss=2):
    im=Image.new('L',(int(Wmm*K*ss),int(Hmm*K*ss)),0); d=ImageDraw.Draw(im)
    for poly,closed in shapes:
        pts=[tuple(v) for v in np.asarray(poly)*K*ss]
        if closed: pts=pts+[pts[0]]
        d.line(pts,fill=255,width=max(1,int(width_mm*K*ss)),joint='curve')
    return np.asarray(im.resize((int(Wmm*K),int(Hmm*K)),Image.LANCZOS)).astype(np.float32)/255
def flower_lines(c,s,rot):
    spec=[(-97,16.5,2.0,0.26),(-160,14.8,1.85,-0.36),(-36,15.6,1.9,0.34),(126,13.2,1.75,0.30),(54,13.8,1.8,-0.32)]
    out=[(tepal(c,a+rot,L*s,W*s,b,0.012,i*0.9,0.2),True) for i,(a,L,W,b) in enumerate(spec)]
    m=(c[0]+math.cos(math.radians(40+rot))*6*s,c[1]+math.sin(math.radians(40+rot))*6*s)
    out.append((ellipse_ruffle(m,2.4*s,1.9*s,40+rot,0.12,9),True))
    return out
def sprig_lines(pts,rng,n_leaves,flowers=(),pods_at=(),flush_at=()):
    """a vine as hairlines: the stem, alternating vanilla leaves, the odd flower, hanging pods, a tea flush"""
    sp=draw.cr(pts,30); out=[(sp,False)]
    d=np.gradient(sp,axis=0); L=len(sp)
    for i in range(n_leaves):
        k=int((i+0.6)/n_leaves*(L-2)); a=math.degrees(math.atan2(d[k][1],d[k][0]))
        out.append((leaf(sp[k],a+(52 if i%2 else -52)+rng.uniform(-10,10),rng.uniform(13,19),rng.uniform(3.6,4.6),rng.uniform(-0.3,0.3)),True))
    for f,s,r in flowers: out+=flower_lines(sp[int(f*(L-1))],s,r)
    for f in pods_at:
        b=sp[int(f*(L-1))]
        for j in (0,1): out.append((pod((b[0]+j*3,b[1]),88-j*7,rng.uniform(26,34),1.3,0.06,1 if j else -1),True))
    for f,a in flush_at:
        b=sp[int(f*(L-1))]; s=1.0; A=math.radians(a); P=lambda t,o=0:(b[0]+math.cos(A)*t*s-math.sin(A)*o*s,b[1]+math.sin(A)*t*s+math.cos(A)*o*s)
        out+=[(draw.cr([b,P(9,0.8),P(17,-0.6),P(26)],10),False),(leaf(P(9,0.8),a-62,19,5.6,-0.3),True),(leaf(P(17,-0.6),a+52,15,4.6,0.28),True),(bud(P(26),a-6,9,2.0,0.12),True)]
    return out
def cream_area(Wmm,Hmm,shapes,linecol,quiet,seed):
    """cream with the hairline pattern, quieter behind the type"""
    img=np.ones((int(Hmm*K),int(Wmm*K),3),np.float32)*PAPER
    a=outline_layer(Wmm,Hmm,shapes,linecol)
    yy,xx=np.mgrid[0:img.shape[0],0:img.shape[1]].astype(np.float32)/K-B
    q=np.ones_like(a)
    for (x0,y0,x1,y1) in quiet:
        dx=np.maximum(np.maximum(x0-xx,xx-x1),0); dy=np.maximum(np.maximum(y0-yy,yy-y1),0)
        q=np.minimum(q,0.18+0.82*np.clip(np.hypot(dx,dy)/8,0,1))
    a=a*q*0.9
    lc=np.array([int(linecol[i:i+2],16) for i in (1,3,5)],np.float32)
    img=img*(1-a[...,None])+lc*a[...,None]
    img+=np.random.default_rng(seed).normal(0,3.2,img.shape[:2])[...,None]
    return img
# ------------------------------------------------------------------ boxes
def build_box(name,p,FW,split,SW,art,shapes,quiet):
    bw=FW-split; W=int(round(B+bw+SW+B)); H=85+2*B
    cv=WC(W,H); art(cv,bw)
    img=cv.render(p['ground'],grain=0,raw=True)
    img+=np.random.default_rng(5).normal(0,5,img.shape[:2])[...,None]
    fw=FW+2*B; front=cream_area(fw,H,shapes,p['line'],quiet,6)
    x0=int((split+B)*K); bwp=int(bw*K); fwp=front.shape[1]
    front[:,x0:]=img[:,B*K:B*K+(fwp-x0)]
    Image.fromarray(front.clip(0,255).astype(np.uint8)).save(O+f'{name}-split-front.png')
    Image.fromarray(img[:,B*K+bwp:].clip(0,255).astype(np.uint8)).save(O+f'{name}-split-side.png')
# all art coordinates: canvas mm (x includes 3 mm bleed; the fold sits at x = bw+3); pattern coordinates: front mm + 3
def long_art(p,cin=False):
    def art(cv,bw):
        f=bw+3
        cv.add([leaf((f+78,4),205,64,13,0.3)],mix(p['leaf_core'],p['ground'],0.55),p['leaf_edge'],2.4,alpha=0.75)
        echo(cv,p,(f+34,16),20,1.5)                                              # soft bloom behind, on the side, high
        vine(cv,p,[(-6,74),(14,64),(30,52),(44,46)])                              # the vine that runs out into the cream
        cv.add([leaf((14,64),-120,17,4.4,0.2),leaf((30,52),40,15,4.0,-0.2)],p['leaf_core'],p['leaf_edge'],0.8)
        if cin: quills(cv,p,(f-60,84),-16,70,3.4)
        pod_pair(cv,p,(f-70,96),-17,118,3.1)
        flush(cv,p,(f+66,92),-108,1.7)
        flush(cv,p,(10,94),-72,1.25,blur=0.9)
        flower(cv,(f-24,38),40,2.7,p,blurs=(0.3,0.26,0.5))                      # the hero, crisper
    return art
def long_shapes(rng,split):
    return (sprig_lines([(split+3+8,77),(split-12,70),(split-40,74),(split-66,82),(split-90,76)],rng,6,flowers=[(0.72,0.75,15)],pods_at=[(0.45,)][:0],flush_at=[(1.0,-150)])
            +sprig_lines([(split-4,-6),(split-22,6),(split-30,16)],rng,2,flowers=[(1.0,0.6,-20)]))
def cube_art(p):
    def art(cv,bw):
        f=bw+3
        cv.add([leaf((f+82,60),200,46,10,0.3)],mix(p['leaf_core'],p['ground'],0.55),p['leaf_edge'],2.4,alpha=0.75)
        echo(cv,p,(f+62,80),70,1.2)                                               # soft bloom low on the side, under the steps
        vine(cv,p,[(-6,80),(6,72),(18,64)])
        cv.add([leaf((6,72),-115,14,3.8,0.2)],p['leaf_core'],p['leaf_edge'],0.8)
        pod_pair(cv,p,(-10,98),-20,92,2.7)
        flush(cv,p,(f+30,96),-100,1.2,blur=1.1,alpha=0.85)
        flower(cv,(f+1,38),70,2.2,p,blurs=(0.3,0.26,0.5))
    return art
def cube_shapes(rng,split):
    return sprig_lines([(split+3+4,83),(split-10,76),(split-30,80),(split-52,86)],rng,4,flowers=[(0.85,0.55,10)],flush_at=[(0.98,-140)])
# ------------------------------------------------------------------ pouch labels (70 x 110, arched)
def label(name,p,cin=False):
    W,H=70+2*B,110+2*B; band=60
    cv=WC(W,H-band); 
    cv.add([leaf((74,8),200,40,9,0.3)],mix(p['leaf_core'],p['ground'],0.55),p['leaf_edge'],2.2,alpha=0.75)
    echo(cv,p,(62,10),20,1.0)
    vine(cv,p,[(8,-4),(12,8),(20,18)])
    if cin: quills(cv,p,(4,40),-14,50,2.6)
    pod_pair(cv,p,(-4,58),-18,76,2.4)
    flush(cv,p,(70,58),-112,1.2)
    flower(cv,(30,26),45,1.75,p,blurs=(0.3,0.26,0.5))
    art=cv.render(p['ground'],grain=0,raw=True); art+=np.random.default_rng(7).normal(0,5,art.shape[:2])[...,None]
    rng=np.random.default_rng(3)
    shapes=sprig_lines([(11,band+3),(9,band-10),(14,band-24),(8,band-40),(16,band-52)],rng,5,flowers=[(0.7,0.6,30)])
    img=cream_area(W,H,shapes,p['line'],[(4,4,72,58)],8)
    y0=(band+B)*K; img[y0:]=art[B*K:B*K+img.shape[0]-y0]
    Image.fromarray(img.clip(0,255).astype(np.uint8)).save(O+name)
if __name__=='__main__':
    rng=np.random.default_rng(11)
    build_box('long',TEAL,175.9,92,85.1,long_art(TEAL),long_shapes(rng,92),[(4,3,90,34),(4,36,90,82)])
    build_box('cube',TEAL,87.6,58,84.6,cube_art(TEAL),cube_shapes(np.random.default_rng(12),58),[(3,3,56,32),(3,34,56,78)])
    build_box('long-cin',CIN,175.9,92,85.1,long_art(CIN,True),long_shapes(np.random.default_rng(13),92),[(4,3,90,34),(4,36,90,82)])
    label('label-vanilla.png',TEAL); label('label-cinnamon.png',CIN,True)
    print('ok')
