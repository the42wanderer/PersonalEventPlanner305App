# Heatmap treatment: the flat image blurred, its brightness mapped through a thermal ramp; type stays crisp on top.
import sys, json, re, numpy as np, cv2
from PIL import Image
S='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/'
sys.argv=sys.argv[:1]; sys.path.insert(0,S+'teasoap')
import build6 as b6
from build6 import K, hx
O=b6.O
RAMPS={'jade':['#071F1F','#0E3A38','#165A52','#2E8270','#7DB58C','#E3C46A','#FFF3D8'],     # deep teal → jade → citrine → vanilla cream
       'amber':['#0A1E1D','#123A36','#3C4A2E','#8A5A24','#D08A3A','#F2C878','#FFF6E2']}     # teal-black → tea brown → amber → cream
def ramp(v,cols):
    c=np.array([hx(x) for x in cols]); t=np.clip(v,0,1)*(len(cols)-1); i=np.minimum(t.astype(int),len(cols)-2); f=(t-i)[...,None]
    return c[i]*(1-f)+c[i+1]*f
def heat(src,dst,cols,sig=2.4,gamma=1.25):
    a=np.asarray(Image.open(O+src).convert('RGB')).astype(np.float32)
    L=(a@np.array([0.3,0.59,0.11],np.float32))/255
    L=cv2.GaussianBlur(L,(0,0),sig*K); L=cv2.GaussianBlur(L,(0,0),sig*K*0.4)
    lo,hi=np.percentile(L,1),np.percentile(L,99.7); v=np.clip((L-lo)/(hi-lo),0,1)**gamma
    out=ramp(v,cols); out+=np.random.default_rng(5).normal(0,3.2,out.shape[:2])[...,None]      # film grain, not mottle
    Image.fromarray(out.clip(0,255).astype(np.uint8)).save(O+dst,quality=94)
man=[]
if __name__=="__main__":
  for rk,cols in RAMPS.items():
      for n in (1,2):
          heat(f'pr{n}.jpg',f'ht{n}-{rk}.jpg',cols)
          h=open(O+f'pr{n}.html').read().replace(f'pr{n}.jpg',f'ht{n}-{rk}.jpg')
          if n==1: h=h.replace('#F2ECDD','#F6F1E4')
          open(O+f'ht{n}-{rk}.html','w').write(h)
          w,hh=[int(x) for x in re.search(r'width="(\d+)" height="(\d+)"',h).groups()]; man.append([O+f'ht{n}-{rk}',w,hh])
  json.dump(man,open(O+'ht.json','w')); print('ok')
  # the gentler pass: less blur, a softer curve, so the orchid's form and the leaves read through the glow
  man2=[]
  for rk in ('jade','amber'):
      for n in (1,2):
          heat(f'pr{n}.jpg',f'hs{n}-{rk}.jpg',RAMPS[rk],sig=1.1,gamma=0.95)
          h=open(O+f'ht{n}-{rk}.html').read().replace(f'ht{n}-{rk}.jpg',f'hs{n}-{rk}.jpg'); open(O+f'hs{n}-{rk}.html','w').write(h)
          w,hh=[int(x) for x in re.search(r'width="(\d+)" height="(\d+)"',h).groups()]; man2.append([O+f'hs{n}-{rk}',w,hh])
  json.dump(man2,open(O+'hs.json','w')); print('ok2')
