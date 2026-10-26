# every element on one sheet: engraved in wine on garnet, foil parts in champagne gold; 280 x 150 mm
import sys; sys.path.insert(0,'/home/user/PersonalEventPlanner305App/vanilla-shop/tools/hamper')
import forms as Fm, engrave as E
from shapely.ops import unary_union
pr=[]; fo=[]
p1=Fm.Pod((8,118),(128,128),bow=0.05); p2=Fm.Pod((14,134),(126,146),bow=0.035,flip=-1)
pr+= p1.engrave_negative()+p2.engrave_negative()
for l in (Fm.Leaf((10,30),-12,62,19,bow=0.06), Fm.Leaf((84,62),-150,48,15,bow=-0.07,flip=-1), Fm.Leaf((14,74),18,44,13.5,bow=0.08)):
    pr+= l.engrave()
f=Fm.BrandFlower((178,52),30,2.35); h,o=f.engrave_parts(); pr+=h; fo+=o
r=Fm.FoldRibbon([[(140,118),(166,104),(196,96),(226,96)], [(226,96),(244,110),(252,132)], [(252,132),(268,140),(278,136)]], 10)
fo+= r.engrave()
for (x,y),rad in (((248,40),4.2),((257,46),3.7),((246,50),3.4),((256,36),3.0)):
    b=E.Berry((x,y),rad); pr+= b.hatch()+b.contour()
P=E.to_path(unary_union(pr)); F=E.to_path(unary_union(fo))
grad=('<linearGradient id="f" x1="0" y1="0" x2="1" y2="0.5"><stop offset="0" stop-color="#A8884F"/><stop offset=".3" stop-color="#EBD9A9"/>'
      '<stop offset=".55" stop-color="#B9975D"/><stop offset=".8" stop-color="#F1E2BA"/><stop offset="1" stop-color="#A9874F"/></linearGradient>')
open(sys.argv[1],'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 150"><defs>{grad}</defs><rect width="280" height="150" fill="#751F2B"/>'
                            f'<path d="{P}" fill="#501923"/><path d="{F}" fill="url(#f)"/></svg>')
