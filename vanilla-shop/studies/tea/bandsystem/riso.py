# Vanilla Tea, 12-bag front: the Estate, re-rendered as a grained print. Same scene and layout as estate_front.py, but
# lit like a late-afternoon screenprint: plum shadows, rust and orange in the middle, butter in the light; every tone
# built from stochastic spray grain instead of a dot screen; ridge tops catching the light; the flower sharp, in
# front; dense rounded shade trees on the crests; a tea shoot at the lower right, cut by the cream's edge.
import os, sys, json, numpy as np, cv2
from PIL import Image, ImageDraw
S='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/'
sys.argv=sys.argv[:1]; sys.path.insert(0,S+'teasoap')
import build6 as b6, kit
from build6 import canvas, B, K, hx, lion
from build2 import shoot
from foliage2 import paint_flower, paint_vbud, trumpet
import draw as DR
import heat as H
import estate_front as EF
O=b6.O; FW,FH=EF.FW,EF.FH
def nz(h,w,sx,sy,seed):
    n=np.random.default_rng(seed).normal(0,1,(h,w)).astype(np.float32); n=cv2.GaussianBlur(n,(0,0),sigmaX=sx,sigmaY=sy); return n/(n.std()+1e-6)
def scene(h,w):
    """light, 0..1: a low sun behind the ranges; each ridge lit along its top and falling into shadow below"""
    xs=np.arange(w,dtype=np.float32)/K-B; ys=np.arange(h,dtype=np.float32)[:,None]/K-B; X=xs[None,:]
    sky=0.10+0.62*np.exp(-((ys-30)/11)**2)+0.10*np.exp(-((ys-30)/36)**2)+0.18*np.exp(-(((X-74)/26)**2+((ys-29)/9)**2))  # the sun's side brighter
    cloud=np.clip(nz(h,w,22*K,1.6*K,2),0,None)*np.exp(-((ys-17)/8)**2)*0.10                                     # long thin cloud bands
    L=np.broadcast_to(sky+cloud,(h,w)).copy()
    def hump(cs):
        r=np.full(xs.shape,99.0,np.float32)
        for c,top,hw in cs: r=np.minimum(r,top+(np.abs(xs-c)/hw)**1.8*(99-top)/6)
        return r
    def layer(crest,tone,rim,fall,mist=0.0,seed=0):
        nonlocal L; m=ys>=crest[None,:]; d=np.clip(ys-crest[None,:],0,None)
        v=tone+rim*np.exp(-d/fall)+0.025*nz(h,w,8*K,2*K,seed)                                    # lit top, shadowed base
        L=np.where(m,v,L)
        if mist: L=L+mist*np.exp(-((ys-crest[None,:]-2.4)/2.4)**2)*np.clip(0.6+0.5*nz(h,w,16*K,1.5*K,seed+1),0,1.2)
        return m
    far=np.minimum(hump([(8,27,26),(44,29,22),(96,28,30)]),28.5+np.abs(xs-80)**1.3*0.35-5.5)
    layer(far,0.46,0.20,2.0,0.10,1)
    layer(hump([(-6,31,20),(28,32,18),(62,33,16),(92,31,22)]),0.34,0.20,1.6,0.10,3)
    def hedges(m,crest,p0,amp,seed):
        nonlocal L; d=np.clip(ys-crest[None,:],0,None); per=p0*(1+0.05*d)
        ph=np.cumsum(1/np.maximum(per,0.3),axis=0)/K; f=ph-np.floor(ph)
        row=np.clip(1-np.abs(f-0.35)/0.42,0,1)**0.8                                               # each row lit on its upper face
        bush=0.75+0.25*np.cos(2*np.pi*(X/(per*1.2))+2.4*np.floor(ph))*(0.8+0.2*nz(h,w,1.2*K,1.2*K,seed))
        L=np.where(m,L+amp*row*bush,L)
    cA=hump([(56,33.5,30)]); mA=layer(cA,0.16,0.26,2.4,0.0,5); hedges(mA,cA,1.7,0.24,6)
    cB=hump([(6,37,20)]); mB=layer(cB,0.14,0.22,2.2,0.0,7); hedges(mB,cB,1.6,0.22,8)
    cN=EF.edge(xs)-8.5; mN=layer(cN,0.10,0.24,3.0,0.0,9); hedges(mN,cN,2.1,0.24,10)
    # shade trees: dense rounded clumps on the crests and in the hollows, dark, a warm rim on the sun side
    rng=np.random.default_rng(11); tm=Image.new('L',(w,h),0); rm=Image.new('L',(w,h),0)
    td,rd=ImageDraw.Draw(tm),ImageDraw.Draw(rm); P=lambda x,y:((x+B)*K,(y+B)*K)
    def clump(x0,crest,s):
        j=int(np.clip((x0+B)*K,0,w-1)); y0=crest[j]+0.3
        for q in range(rng.integers(8,13)):                                                               # a low, wide, bushy crown on the ground
            cx,cy=x0+rng.uniform(-1.3,1.3)*s,y0-s*rng.uniform(0.25,1.25); r=s*rng.uniform(0.3,0.5)
            td.ellipse([*P(cx-r,cy-r*0.85),*P(cx+r,cy+r*0.85)],fill=255)
            rd.ellipse([*P(cx-r+0.12*s,cy-r*0.85),*P(cx+r+0.12*s,cy+r*0.85)],fill=255)                  # the lit edge, toward the sun (right)
    for x0,s in ((36,0.9),(41,1.1),(45,0.8),(62,1.0),(67,0.8),(74,1.2)): clump(x0,cA,s)
    for x0,s in ((3,1.0),(10,0.8),(16,1.1)): clump(x0,cB,s)
    for x0,s in ((26,1.5),(52,1.3),(80,2.2),(85,1.8)): clump(x0,cN+0.6,s)
    t=np.asarray(tm).astype(np.float32)/255; r=np.asarray(rm).astype(np.float32)/255
    L=L*(1-t)+0.06*t+0.16*np.clip(r-t,0,1)                                                              # dark clumps, a rim of light
    return np.clip(L,0,1)
def foreground(h,w):
    """sharp, as two layers: the flower in front, upper left; a tea shoot rising at the lower right, cut by the cream"""
    def lay(fn):
        img,P=canvas(FW,FH); bg=img.copy(); fn(P,img)
        a=np.clip(np.abs(img-bg).max(2)/30,0,1); return (img@np.array([0.3,0.59,0.11],np.float32))/255,a
    fl=lay(lambda P,c:(paint_flower(P,c,(B+11,B+9),30,2.35),paint_vbud(P,c,(B+34,B+6),-40,6)))
    sh=lay(lambda P,c:shoot(P,c,(B+FW+5,B+FH-14),-128,46,-0.35,20,('#2A3A2A','#3C5038','#5A6E4E','#8DA07A'),'#C9D6B4',9,1))
    return fl,sh
def grain(v,amt,seed):
    """spray grain: fine clumped noise pushed through the tones, strongest in the middle of each gradient"""
    h,w=v.shape; g=0.65*nz(h,w,0.55,0.55,seed)+0.35*nz(h,w,1.4,1.4,seed+1)
    return np.clip(v+amt*g*(0.12+3.2*v*(1-v)),0,1)
def lip_shadow(h,w):
    """a soft occlusion on the petal under the lip's ruffled lower edge, so the two read as separate; cast straight down
    from the mouth only (never from the tube, whose straight side would show), wide and faint"""
    tube,mouth,_=trumpet((B+11,B+9),30,7.5*2.35,1.1*2.35,3.6*2.35,2.6*2.35,0.13)
    def mask(polys):
        im=Image.new('L',(w,h),0); dr=ImageDraw.Draw(im)
        for poly in polys: dr.polygon([(x*K,y*K) for x,y in poly],fill=255)
        return np.asarray(im).astype(np.float32)/255
    lip=cv2.GaussianBlur(mask((tube,mouth)),(0,0),0.5*K); src=mask((mouth,))
    sh=cv2.GaussianBlur(np.roll(src,int(0.5*K),0),(0,0),1.5*K)
    return np.clip(sh*(1-0.6*lip)*1.6,0,1)                                                        # creeping a little up the lip's underside
def render(name,ramp,fr=None,gam=1.0):
    img,_=canvas(FW,FH); h,w=img.shape[:2]
    L=cv2.GaussianBlur(scene(h,w),(0,0),0.12*K); (Lf,af),(Ls,as_)=foreground(h,w)
    yy,xx=np.mgrid[0:h,0:w].astype(np.float32)/K-B
    # the shoot: a dark silhouette, its leaves lit along the edges toward the sun
    as_=cv2.GaussianBlur(as_,(0,0),0.06*K); m=(as_>0.5).astype(np.uint8)
    ins=cv2.distanceTransform(m,cv2.DIST_L2,5)/K
    ln=np.clip((Ls-np.percentile(Ls[as_>0.5],5))/(np.percentile(Ls[as_>0.5],99)-np.percentile(Ls[as_>0.5],5)+1e-6),0,1)
    sv=0.05+0.20*ln**2+0.46*np.exp(-ins/0.32)                                                          # veins and rims catch the light
    L=L*(1-as_)+sv*as_
    # the flower: butter at the heart, warming to orange toward the tips and along every petal's edge, its own shading kept
    af=cv2.GaussianBlur(af,(0,0),0.06*K); m=(af>0.5).astype(np.uint8)
    ins=cv2.distanceTransform(m,cv2.DIST_L2,5)/K
    lo,hi=np.percentile(Lf[af>0.5],(3,99)); sh=np.clip((Lf-lo)/(hi-lo+1e-6),0,1)
    heart=np.exp(-(((xx-30)/17)**2+((yy-19)/15)**2))
    fv=0.68+0.16*sh+0.22*heart-0.17*np.exp(-ins/0.8)-0.22*lip_shadow(h,w)
    fv=np.clip(fv,0,1)
    v=grain(L,0.075,21)**gam; out=H.ramp(v,ramp)                                                  # gam>1: deeper darks, the light kept
    fg=grain(fv,0.075,23); fo=H.ramp(fg,ramp) if fr is None else H.ramp(np.clip((fg-0.56)/0.44,0,1),fr)   # the flower keeps its own warm light
    out=out*(1-af[...,None])+fo*af[...,None]
    out*=(1-0.06*np.clip(nz(h,w,40*K,40*K,5),0,1))[...,None]                                            # faint unevenness of a print
    out+=np.random.default_rng(5).normal(0,3.0,(h,w))[...,None]
    Image.fromarray(out.clip(0,255).astype(np.uint8)).save(O+name+'.jpg',quality=95)
FLOWER={'emeraldhoney':['#B9874A','#D8AA68','#EBC98C','#F5E4B3','#FCF3D6'],'evergreen':['#B9874A','#D8AA68','#EBC98C','#F5E4B3','#FCF3D6'],'emerald':['#B9874A','#D8AA68','#EBC98C','#F5E4B3','#FCF3D6'],'jade':['#B9874A','#D8AA68','#EBC98C','#F5E4B3','#FCF3D6'],'sage':['#B9874A','#D8AA68','#EBC98C','#F5E4B3','#FCF3D6'],'forest':['#B9874A','#D8AA68','#EBC98C','#F5E4B3','#FCF3D6'],'ceylon':['#B9874A','#D8AA68','#EBC98C','#F5E4B3','#FCF3D6']}   # warm honey in the shade, never khaki
# evergreen: the stops given as positions down the sky (0, 35, 62, 78, 91, 100%), converted to the light the sky
# actually has at those heights in this scene (it brightens steeply near the horizon): so the glow is honey, its
# peak cream, the chartreuse a narrow step, and the tea rows (light 0.1-0.4) stay evergreen to moss
RAMPS={'evergreen':[(0,'#082C23'),(.26,'#14513A'),(.46,'#537A42'),(.64,'#A8B96B'),(.78,'#E6CC89'),(.88,'#FFF0C8'),(1,'#FFF0C8')],   # measured: upper sky ~0.33 stays evergreen-emerald
       'emeraldhoney':['#06180F','#0D2E1D','#17482C','#2F6B3C','#7C9A4A','#DAAE5C','#F7D894','#FEF0CC'],   # emerald, only its horizon light warmed to pale honey (same luminance, so same band width)
       'emerald':['#06180F','#0D2E1D','#17482C','#2F6B3C','#7C9A4A','#D2B45C','#F2DC98','#FCF1CF'],   # deep emerald, golden light
       'jade':['#0B1F18','#14382A','#1F5A3E','#4E8A5A','#9DBB6E','#DCD892','#F6EFC6'],               # bottle green to jade, lime-gold glow
       'sage':['#17221D','#26372F','#3E5448','#677D69','#9FAF92','#D3D7B6','#F2EED6'],               # misty highland sage
       'ceylon':['#0F1E17','#1E3527','#3D4F2E','#7A6A35','#B5813A','#DDA65A','#F2D08F','#FBEBC4'],   # tea-leaf greens to brewed amber
       'brew':['#1A0F0A','#2E1A10','#4E2C17','#7C4521','#AD6A2F','#D6964F','#EDC388','#FAE6C2'],     # a cup of black tea
       'forest':['#142D25','#30513A','#71804A','#B3A663','#E3CD8D','#F5E7B6'],'plum':['#1C0B1A','#341530','#57203A','#86333B','#BC5A38','#E58A4C','#F5B872','#FCE3A6'],
       'green':['#08171A','#0F2A2C','#17433F','#2C6455','#6F8E62','#C99A5C','#EFC487','#FBEACB']}
INK={'emeraldhoney':'#0D2E1D','evergreen':'#0C3326','emerald':'#0D2E1D','jade':'#14382A','sage':'#26372F','ceylon':'#1E3527','brew':'#2E1A10','forest':'#142D25','plum':'#3B1631','green':'#163F3D'}; CREAM={'emeraldhoney':'#F3E6BE','evergreen':'#F3E6BE','emerald':'#F3E6BE','jade':'#F3E6BE','sage':'#F2EED6','ceylon':'#F3E6BE','brew':'#F3E6BE','forest':'#F3E6BE','plum':'#F3E6BE','green':'#F4EEDF'}
if __name__=='__main__':
    man=[]
    for k in ('forest','plum'):
        ramp=RAMPS[k]; render(f'rs-{k}-art',ramp,FLOWER.get(k),1.3 if k=='forest' else 1.0); EF.CREAM=CREAM[k]; EF.GREEN=INK[k]; EF.compose(f'rs-{k}-art.jpg',f'rs-{k}.jpg')
        man.append(b6.face(f'rs-{k}',FW,FH,f'rs-{k}.jpg',EF.overlay(top=True)))
    json.dump(man,open(O+'rs.json','w')); print('ok')

# four-way board: each of the art director's six colours set on the tone it names (deepest = the brewing panel's
# tone 0.055, upper sky, midtones, the transition, the horizon glow 0.6-0.8, the brightest light held to the top)
RAMPS['apricot']=[(0, '#07251F'), (0.055, '#092E26'), (0.19, '#073C38'), (0.38, '#176347'), (0.52, '#9B9950'), (0.63, '#E7AE70'), (0.88, '#F8DFAC'), (1, '#F8DFAC')]
FLOWER['apricot']=FLOWER['emerald']; INK['apricot']='#092E26'; CREAM['apricot']='#F3E6BE'
RAMPS['citron']=[(0, '#052B26'), (0.055, '#07352F'), (0.17, '#064C45'), (0.41, '#238064'), (0.62, '#82AC63'), (0.8, '#D5D98B'), (0.94, '#F5EDC4'), (1, '#F5EDC4')]
FLOWER['citron']=['#8F955A','#B7B97C','#D8D7A2','#EFECCB','#FCF9E6'];   # vanilla's own pale green-ivory: cool olive shade, ivory light
INK['citron']='#07352F'; CREAM['citron']='#F3E6BE'
RAMPS['ochre']=[(0, '#1A261B'), (0.055, '#202F22'), (0.2, '#344831'), (0.38, '#687747'), (0.54, '#B39A51'), (0.69, '#E3BD79'), (0.9, '#FAE4B7'), (1, '#FAE4B7')]
FLOWER['ochre']=FLOWER['emerald']; INK['ochre']='#202F22'; CREAM['ochre']='#F3E6BE'

# Three broad art directions, by region rather than by tone: 'sky' is a gradient top to bottom (art mm; the horizon is
# near 27-30), 'hills' one ramp per layer (far range, second range, mid hill, near hill, front fields) over that layer's
# own light, 'sprig' the tea shoot, 'panel' the How to brew side and the lid. The orchid keeps FLOWER['emerald'].
DIRS={
 'rose':{   # emerald sky, a broad dusty-rose band (a third of the sky), pale peach at the horizon; rose-brown far hills
  'sky':[(-3,'#0B3229'),(2.5,'#103F35'),(6,'#2E4A42'),(9,'#7D6C66'),(12,'#B8877F'),(14,'#C58F88'),(20.5,'#CC9789'),(25,'#F3CFAC'),(30,'#F7DCBC')],
  'hills':[[(0,'#6E4C4A'),(.5,'#9A746C'),(1,'#D2A994')],[(0,'#4C3B3B'),(.5,'#6F5752'),(1,'#A68578')],
           [(0,'#0A2A22'),(.45,'#1C5444'),(1,'#7E9E80')],[(0,'#061E18'),(.5,'#134437'),(1,'#447A64')],[(0,'#061E18'),(.5,'#134437'),(1,'#447A64')]],
  'sprig':[(0,'#0B2E25'),(.5,'#2C6250'),(1,'#A9C2A8')],'panel':'#0F3B31','lidGlowCol':'#5E5A52','cream':'#F3E6BE'},
 'celadon':{   # a light landscape: pale celadon sky, ivory horizon, sage far hills, the dark forest only in front
  'sky':[(-3,'#B6CCA6'),(6,'#C3D5B2'),(14,'#CCDABA'),(21,'#DFE3C6'),(26,'#F2E9CD'),(30,'#F6EFD8')],'skyLight':0.9,
  'hills':[[(0,'#86A07A'),(.5,'#97B089'),(1,'#C3D2B0')],[(0,'#6E8C67'),(.5,'#819D77'),(1,'#AFC29D')],
           [(0,'#365F4A'),(.45,'#517A5E'),(1,'#9DB792')],[(0,'#12352A'),(.5,'#214F3A'),(1,'#527E61')],[(0,'#12352A'),(.5,'#214F3A'),(1,'#527E61')]],
  'sprig':[(0,'#163C2E'),(.5,'#36654B'),(1,'#A3BE9A')],'panel':'#CBDABB','panelGrain':0.12,'lidGlowCol':'#E6EAD2','cream':'#F3E6BE'},
 'chartreuse':{   # a bold yellow-green sky over the whole upper art, butter yellow at the horizon, olive middle hills, ink-green front
  'sky':[(-3,'#A9BE3F'),(6,'#B7C94B'),(15,'#C2CF57'),(20,'#D8D97C'),(24.5,'#EFE0A0'),(30,'#F3E7B4')],'skyLight':1.0,
  'hills':[[(0,'#5E6F38'),(.5,'#728447'),(1,'#A3AF62')],[(0,'#475733'),(.5,'#5B6C3D'),(1,'#88964F')],
           [(0,'#0E2F27'),(.45,'#214A37'),(1,'#5F7B45')],[(0,'#06191A'),(.5,'#102F29'),(1,'#2F5442')],[(0,'#06191A'),(.5,'#102F29'),(1,'#2F5442')]],
  'sprig':[(0,'#0B2924'),(.5,'#285A43'),(1,'#B3C66C')],'panel':'#102F29','lidGlowCol':'#3C5A2E','cream':'#F5EFD9'}}
