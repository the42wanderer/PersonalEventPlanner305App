# Sowvital/Taini-style: our engraved vanilla in one ink, large and cropped, on a cream or soft colour ground, with grain.
import numpy as np
from PIL import Image
O='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/soap/b2/'
SP='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/bw/spray-test.png'
K=12; W,H=150,95
C={'vanilla':('#F1E7D3','#7A4E1E'),'rosette':('#D3A0A4','#FBF1EA'),'ebony':('#E3DDD3','#2E2A27'),'aloe':('#7E9B73','#F6F2E4')}
POS={'vanilla':(120,24,-14),'rosette':(116,24,-2),'ebony':(120,30,-20),'aloe':(112,22,10)}
def hx(c): return np.array([int(c[i:i+2],16) for i in (1,3,5)],np.float32)
sp=Image.open(SP).convert('L')
for k,(g,ink) in C.items():
    cx,cy,rot=POS[k]
    m=Image.fromarray((255-np.asarray(sp)).astype(np.uint8))           # ink = white in the mask
    s=150*K/m.size[1]; m=m.resize((int(m.size[0]*s),int(m.size[1]*s)),Image.LANCZOS).rotate(rot,expand=True,resample=Image.BICUBIC)
    M=Image.new('L',(W*K,H*K),0); M.paste(m,(int((cx+7)*K-m.size[0]/2),int((cy+7)*K-m.size[1]/2)))
    a=np.asarray(M).astype(np.float32)/255; a=np.clip((a-0.25)/0.5,0,1)
    col=hx(g)*(1-a[...,None])+hx(ink)*a[...,None]
    rng=np.random.default_rng(3); col+=rng.normal(0,6,a.shape)[...,None]
    Image.fromarray(col.clip(0,255).astype(np.uint8)).save(O+f'E-{k}.png')
print('ok')
