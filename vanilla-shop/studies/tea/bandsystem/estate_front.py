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
def edge(x):
    """face-mm y of the cream's top edge: level under the type, the near hill sweeping down on the right"""
    return 46.0-0.8*np.sin((x+6)/14)+12.5*ss((x-56)/32)
def compose(src,dst):
    a=np.asarray(Image.open(O+src).convert('RGB')).astype(np.float32); h,w=a.shape[:2]
    xs=np.arange(w,dtype=np.float32)/K-B; ys=np.arange(h,dtype=np.float32)[:,None]/K-B
    m=np.clip((ys-edge(xs)[None,:])*K/1.2+0.5,0,1)                                                # crisp, anti-aliased
    paper=hx(CREAM)*(1+0.012*np.random.default_rng(3).normal(0,1,(h,w)))[...,None]
    out=a*(1-m[...,None])+paper*m[...,None]
    Image.fromarray(out.clip(0,255).astype(np.uint8)).save(O+dst,quality=95)
def T(t,x,y,sz,c,f,a='start',tr=0.0): return f'<text x="{x:.2f}" y="{y:.2f}" font-family="{f}" font-size="{sz}" letter-spacing="{sz*tr:.3f}" fill="{c}" text-anchor="{a}">{t}</text>'
def overlay(x=8):
    return [f'<defs>{LEAF}</defs>', logo(x+4.6,51.6,9.2,GREEN),
            f'<text x="{x-0.3}" y="72" font-size="17"><tspan font-family="ISR" fill="url(#leaf)">Vanilla</tspan><tspan font-family="IS" fill="{GREEN}"> Tea</tspan></text>',
            T('CEYLON BLACK TEA WITH NATURAL VANILLA',x,77.2,1.45,GREEN,'RW',tr=0.24),
            T('12 TEA BAGS  ·  NET WT. 24 g',x,80.5,1.45,GREEN,'RW',tr=0.24),
            lion(FW-14.6,72.2,7.2,GREEN)]
if __name__=='__main__':
    compose('gd-dawn.jpg','ef-front.jpg')
    json.dump([b6.face('ef-front',FW,FH,'ef-front.jpg',overlay())],open(O+'ef.json','w')); print('ok')
