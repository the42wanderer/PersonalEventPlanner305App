# Vanilla Tea, 12-bag front, integrated: the Estate landscape over the upper part of the box, a warm cream ground
# running to the bottom and side edges (no floating label, no frame), its top edge the contour of the near hill, which
# dips into the cream on the right. Logo, then the name large and left-aligned, then description and weight.
import sys, json, numpy as np, cv2
from PIL import Image
S='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/'
sys.argv=sys.argv[:1]; sys.path.insert(0,S+'teasoap')
import build6 as b6, kit
from build6 import B, BOX, K, hx, lion
from kit import logo
O=b6.O
kit.FONTS.update({'ISR':'/home/user/PersonalEventPlanner305App/vanilla-shop/fonts/instrument-serif.ttf'})
b6.css=''.join(f"@font-face{{font-family:{a};src:url(file://{v})}}" for a,v in kit.FONTS.items())
d=BOX['cube']; FW,FH=d['FW'],d['FH']
GREEN='#163F3D'; CREAM='#F4EEDF'
LEAF=('<linearGradient id="leaf" x1="0" y1="0" x2="1" y2="0.3"><stop offset="0" stop-color="#8A6424"/><stop offset=".25" stop-color="#D9B465"/>'
      '<stop offset=".5" stop-color="#A27A30"/><stop offset=".75" stop-color="#E6C77E"/><stop offset="1" stop-color="#946B28"/></linearGradient>')
def ss(t): t=np.clip(t,0,1); return t*t*(3-2*t)
EDGE=np.array([(-3,45.5),(30,42.5),(52,51),(90.6,62.5)])                                       # one cubic sweep, like a hill's shoulder
_t=np.linspace(0,1,600)[:,None]; _c=(1-_t)**3*EDGE[0]+3*(1-_t)**2*_t*EDGE[1]+3*(1-_t)*_t**2*EDGE[2]+_t**3*EDGE[3]
def edge(x):
    """face-mm y of the cream's top edge: high and level under the logo, falling away smoothly to the right"""
    return np.interp(x,_c[:,0],_c[:,1])
def compose(src,dst):
    a=np.asarray(Image.open(O+src).convert('RGB')).astype(np.float32); h,w=a.shape[:2]
    xs=np.arange(w,dtype=np.float32)/K-B; ys=np.arange(h,dtype=np.float32)[:,None]/K-B
    m=np.clip((ys-edge(xs)[None,:])*K/1.2+0.5,0,1)                                                # crisp, anti-aliased
    paper=hx(CREAM)*(1+0.012*np.random.default_rng(3).normal(0,1,(h,w)))[...,None]
    out=a*(1-m[...,None])+paper*m[...,None]
    Image.fromarray(out.clip(0,255).astype(np.uint8)).save(O+dst,quality=95)
def T(t,x,y,sz,c,f,a='start',tr=0.0): return f'<text x="{x:.2f}" y="{y:.2f}" font-family="{f}" font-size="{sz}" letter-spacing="{sz*tr:.3f}" fill="{c}" text-anchor="{a}">{t}</text>'
def overlay(x=8):
    return [f'<defs>{LEAF}</defs>', logo(x+4.1,52.6,8.2,GREEN),
            f'<text x="{x-0.3}" y="72.5" font-size="16"><tspan font-family="ISR" fill="url(#leaf)">Vanilla</tspan><tspan font-family="IS" fill="{GREEN}"> Tea</tspan></text>',
            T('CEYLON BLACK TEA WITH NATURAL VANILLA',x,77.4,1.45,GREEN,'RW',tr=0.24),
            T('12 TEA BAGS  ·  NET WT. 24 g',x,80.6,1.45,GREEN,'RW',tr=0.24),
            lion(FW-14.6,71.6,7.2,GREEN)]
if __name__=='__main__':
    import os; os.environ['NOSHOOT']='1'; import garden as G
    G.NEAR=lambda xs: edge(xs)-8.5                                                                  # the near hill's rows run with the edge
    G.render('ef-art',G.RAMPS['dawn']); compose('ef-art.jpg','ef-front.jpg')
    json.dump([b6.face('ef-front',FW,FH,'ef-front.jpg',overlay())],open(O+'ef.json','w')); print('ok')
