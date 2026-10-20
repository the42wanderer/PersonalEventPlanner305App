# The vanilla spray in one ink: vine, leaves, two flowers, buds and a hanging pod bunch.
# Scale: 1 mm on the bag = about 2.5 mm of plant, so pods 70 mm long and 4 mm thick, flowers about 22 mm across.
import math, numpy as np
from draw import cr, arc
from engrave import Form, Plate
def hermite(top,tip,a0,a1,n=200):
    P0,P1=np.array(top,float),np.array(tip,float); L=np.linalg.norm(P1-P0)
    T0=np.array([math.sin(math.radians(a0)),math.cos(math.radians(a0))])*L; T1=np.array([math.sin(math.radians(a1)),math.cos(math.radians(a1))])*L
    t=np.linspace(0,1,n)[:,None]
    return (2*t**3-3*t**2+1)*P0+(t**3-2*t**2+t)*T0+(-2*t**3+3*t**2)*P1+(t**3-t**2)*T1
def podw(W):
    def f(t):
        if t<0.06: return 0.35+(0.6*W-0.35)*t/0.06
        if t<0.32: return W*(0.6+0.4*math.sin(math.pi/2*(t-0.06)/0.26))
        w=W*(1-0.3*((t-0.32)/0.68)**1.6)
        return w*math.sqrt(max(0.04,1-((t-0.93)/0.07)**2)) if t>0.93 else w
    return f
def leafw(W):  return lambda t: W*(math.sin(math.pi*min(t,0.999))**0.75)*(1-0.25*t)*min(1,0.25+t*5)+0.15
def tepw(W):   return lambda t: W*min(1,0.35+t*3)*(math.sin(math.pi*min(t,0.999)**0.8)**0.85)+0.12
def budw(W):   return lambda t: W*math.sin(math.pi*min(t,0.999)**0.65)**0.9+0.1
def leaf(base,ang,L,W,bend,tone=0.5,vein=0):
    return Form(arc(base,ang,L,bend,7),leafw(W),tone=tone,rib=True,pitch=0.8,round_=1.0,hi=-0.45,cross=0.78,
                hatch='vein' if vein else 'converge',vein=vein,outline=0.42)
def pod(top,tip,a0,a1,W=2.0,tone=0.55):
    return Form(hermite(top,tip,a0,a1),podw(W),tone=tone,pitch=0.66,round_=1.1,hi=-0.35,cross=0.7,tip_dark=0.2,outline=0.4)
def raceme(pl,node,specs,axis_end,W=2.0):
    """a bunch: a short curved axis from the node, each pod on its own stalk along it; specs=(attach t, tip, a0, a1, tone)"""
    ax=hermite(node,axis_end,-10,10,60)
    for t,tip,a0,a1,tone in specs:
        top=ax[int(t*59)]; pl.form(pod(top,tip,a0,a1,W,tone))
    pl.form(Form(ax,lambda t:1.0-0.3*t,tone=0.6,hatch='along',pitch=0.55,outline=0.36))
def flower(pl,node,a_ov,lip,s=1.0,mirror=1):
    """vanilla flower in three-quarter view, after the reference photo: a slim ovary out of the node; behind, five
    narrow tepals spread like a loose star; in front, the lip rolled into a trumpet with a frilled, flaring mouth"""
    ov=arc(node,a_ov,15*s,0.3*mirror,5); pl.form(Form(ov,lambda t:(0.75+0.45*t)*s,tone=0.5,hatch='along',pitch=0.6,outline=0.36))
    P=ov[-1]
    # tepals, absolute angles around the lip direction; (angle offset, length, half-width, bend, tone, in front?)
    spec=[(180+18*mirror,20,2.6,0.25*mirror,0.48,False),(-118*mirror,22,2.9,-0.3*mirror,0.36,False),(122*mirror,21,2.8,0.32*mirror,0.36,False),
          (-62*mirror,23,3.1,0.4*mirror,0.14,True),(64*mirror,22,3.0,-0.38*mirror,0.14,True)]
    def tep(da,L,W,b,tone):
        return Form(arc(P,lip+da,L*s,b,6),lambda t,W=W:W*s*min(1,0.3+t*3.2)*(math.sin(math.pi*min(t,0.999)**0.85)**0.9)*(1-0.12*math.sin(2*math.pi*t))+0.12,
                    tone=tone,pitch=0.7,round_=0.9,hi=-0.15*mirror,base_dark=0.35,tip_dark=0.12,cross=0.82,outline=0.4)
    for sp in spec:
        if not sp[5]: pl.form(tep(*sp[:5]))
    dd=np.array([math.cos(math.radians(lip)),math.sin(math.radians(lip))]); n=np.array([-dd[1],dd[0]])
    Ll=13*s
    pl.form(Form([P+dd*k*Ll/6 for k in range(7)],lambda t:(1.5+3.0*t**1.8)*s,tone=0.28,pitch=0.6,round_=1.1,hi=-0.4*mirror,cross=0.8,outline=0.42))
    m=P+dd*Ll; th=np.linspace(0,2*np.pi,300); rr=1+0.06*np.sin(7*th)+0.04*np.sin(13*th+1)
    rx,ry=2.6*s,5.4*s
    mouth=np.stack([rx*rr*np.cos(th),ry*rr*np.sin(th)],1); mouth=m+mouth[:,:1]*dd+mouth[:,1:]*n
    pl.knock(mouth)
    pl.form(Form([m-n*ry*0.72+dd*0.4,m+n*ry*0.72+dd*0.4],lambda t:rx*0.62*math.sin(math.pi*min(t,0.999))**0.55+0.1,tone=0.97,hatch='along',pitch=0.5,round_=0.2,hi=3,outline=0,solid=0.9))
    pl.stroke(mouth,0.44,True)
    for k in range(0,300,9):
        q=mouth[k]; pl.stroke([q,q+(m-q)*0.16],0.26)
    for sp in spec:
        if sp[5]: pl.form(tep(*sp[:5]))
def buds(pl,node,dirs):
    for a,L in dirs:
        st=arc(node,a,L*0.5,0.3,4); pl.form(Form(st,lambda t:0.55,tone=0.5,hatch='along',pitch=0.55,outline=0.3))
        pl.form(Form(arc(st[-1],a+6,L*0.5,0.2,4),budw(1.5),tone=0.42,pitch=0.6,round_=1.0,hi=-0.4,cross=0.8,outline=0.34))
def build_stamp(pl):
    return stamp_spray(pl)
def build(pl):
    stem=Form(cr([(14,172),(24,140),(38,112),(50,84),(58,56),(66,30),(82,4)],20),lambda t:3.0-0.9*t,tone=0.55,hatch='along',pitch=0.62,round_=1.1,hi=-0.35,cross=0.72,outline=0.42)
    pl.form(leaf((50,84),-12,60,11,0.55,0.62,18)); pl.form(leaf((38,112),196,54,10,-0.6,0.62,18))
    pl.form(stem)
    pl.stroke(cr([(42,104),(34,112),(29,124),(27,140)],10),0.5)
    node=(55,72)
    raceme(pl,node,[(0.1,(36,140),-25,-5,0.7),(0.4,(60,156),-4,6,0.7),(0.7,(84,146),18,4,0.7),(0.9,(94,128),35,14,0.7),
                    (0.0,(30,126),-38,-12,0.5),(0.25,(46,152),-14,0,0.5),(0.5,(54,161),-6,4,0.5),(0.6,(68,155),6,-6,0.5),
                    (0.8,(77,148),12,0,0.5),(1.0,(87,138),24,6,0.5)],(64,84))
    pl.form(leaf((58,56),160,58,11,-0.45,0.5,18)); pl.form(leaf((66,30),-28,56,10.5,0.6,0.5,18))
    buds(pl,(63,38),[(-40,10),(-15,11),(10,9)])
    flower(pl,(66,30),-5,60,1.05,1)
    flower(pl,(40,106),190,120,1.0,-1)
if __name__=='__main__':
    pl=Plate(120,170,20); build(pl); pl.save('spray-test.png'); print('ok')

def stamp_spray(pl):
    """the vine laid out on the stamp itself (stamp mm): up from below the bottom edge, through the right of the picture,
    out over the frame at the top right; its bunch hangs over the bottom band clear of the caption"""
    S=1.3
    stem=Form(cr([(214,350),(207,310),(196,262),(190,215),(193,170),(204,128),(222,88),(246,46),(272,10)],24),lambda t:4.0-1.3*t,
              tone=0.55,hatch='along',pitch=0.7,round_=1.1,hi=-0.35,cross=0.72,outline=0.5)
    # leaves behind the stem
    pl.form(Form(arc((191,226),196,74,-0.5,7),leafw(14),tone=0.62,rib=True,pitch=0.85,round_=1.0,hi=-0.45,cross=0.78,hatch='vein',vein=18,outline=0.5))
    pl.form(Form(arc((205,126),218,70,0.45,7),leafw(13),tone=0.6,rib=True,pitch=0.85,round_=1.0,hi=-0.45,cross=0.78,hatch='vein',vein=18,outline=0.5))
    pl.form(stem)
    for r in (cr([(196,250),(184,258),(176,270),(172,288)],10),cr([(220,92),(232,100),(240,112)],8)): pl.stroke(r,0.6)
    # the bunch, from a node on the stem
    node=(196,200)
    raceme(pl,node,[(0.1,(178,282),-14,-3,0.7),(0.4,(204,300),-2,4,0.7),(0.7,(226,292),10,3,0.7),(0.95,(238,272),22,10,0.7),
                    (0.0,(172,268),-24,-8,0.5),(0.25,(190,296),-8,0,0.5),(0.5,(198,306),-3,3,0.5),(0.6,(212,300),4,-4,0.5),
                    (0.8,(222,292),9,0,0.5),(1.0,(232,282),16,5,0.5)],(206,212),2.6)
    # leaves in front, two of them crossing the frame
    pl.form(Form(arc((193,178),-14,78,0.55,7),leafw(14.5),tone=0.5,rib=True,pitch=0.85,round_=1.0,hi=-0.45,cross=0.78,hatch='vein',vein=18,outline=0.5))
    pl.form(Form(arc((228,80),-48,66,0.5,7),leafw(12.5),tone=0.5,rib=True,pitch=0.85,round_=1.0,hi=-0.45,cross=0.78,hatch='vein',vein=18,outline=0.5))
    pl.form(Form(arc((199,252),18,64,0.4,7),leafw(12),tone=0.52,rib=True,pitch=0.85,round_=1.0,hi=-0.45,cross=0.78,hatch='vein',vein=18,outline=0.5))
    buds(pl,(236,64),[(-120,13),(-150,14),(-175,12)])
    flower(pl,(240,58),-60,-110,1.45,1)
    flower(pl,(196,150),200,140,1.4,-1)
