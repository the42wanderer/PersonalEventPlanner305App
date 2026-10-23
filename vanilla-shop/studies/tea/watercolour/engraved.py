# Vanilla tea artwork, round three: the brand's engraved vanilla spray (as on the soap backs and the tote) in fine
# cream line over a soft glow on teal: atmosphere underneath, one crisp drawing on top. Front-panel mm, +3 mm bleed.
import numpy as np
from PIL import Image, ImageFilter
SP='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/bw/spray-test.png'
O='/home/user/PersonalEventPlanner305App/vanilla-shop/studies/tea/watercolour/engraved/'
K=20; B=3
GROUND=np.array([0x2C,0x64,0x66],np.float32); LINE=np.array([0xF3,0xE6,0xC8],np.float32)
CREAM=np.array([0xE9,0xF0,0xDF],np.float32); WARM=np.array([0xE8,0xB0,0x62],np.float32)
src=Image.open(SP).convert('L'); src=src.transpose(Image.FLIP_LEFT_RIGHT)       # flipped: the stem enters bottom right
FR=[(0.30,0.21),(0.805,0.62)]                                                     # flowers, as fractions of the drawing
def art(name,W,H,left,top,hmm,pods):
    w,h=int(W*K),int(H*K)
    yy,xx=np.mgrid[0:h,0:w].astype(np.float32)/K-B
    wm=hmm*2400/3400
    img=np.ones((h,w,3),np.float32)*GROUND
    def glow(c,R,col,a):
        g=np.clip(1-np.hypot(xx-c[0],yy-c[1])/R,0,1)**1.8*a; return g[...,None]
    for fx,fy in FR:
        c=(left+fx*wm,top+fy*hmm); g=glow(c,hmm*0.33,CREAM,0.30); img=img*(1-g)+CREAM*g
    g=glow(pods,hmm*0.35,WARM,0.16); img=img*(1-g)+WARM*g
    vg=np.clip(np.hypot((xx-W*0.4)/W,(yy-H*0.5)/H)*1.4,0,1)**2*0.18; img*=(1-vg[...,None])        # a soft darkening at the edges
    m=src.resize((int(wm*K),int(hmm*K)),Image.LANCZOS)
    M=Image.new('L',(w,h),255); M.paste(m,(int((left+B)*K),int((top+B)*K)))
    a=1-np.asarray(M).astype(np.float32)/255; a=np.clip((a-0.15)/0.7,0,1)*0.92
    img=img*(1-a[...,None])+LINE*a[...,None]
    rng=np.random.default_rng(9); img+=rng.normal(0,6,(h,w,1))
    Image.fromarray(img.clip(0,255).astype(np.uint8)).save(O+name)
# long: panel 176 x 85; name bottom left to x 113, data top left to x 96, signature top right from x 139
art('long-teal.png',182,91,left=96,top=-12,hmm=100,pods=(134,55))
# cube: panel 88 x 85; info top left, signature top right, name stacked bottom left
art('cube-teal.png',94,91,left=51,top=25,hmm=62,pods=(73,62))
print('ok')
