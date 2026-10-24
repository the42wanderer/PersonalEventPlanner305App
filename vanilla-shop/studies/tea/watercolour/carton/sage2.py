# Vanilla Tea in Sage, art directed: one hero bloom and a small soft echo on a diagonal away from the name,
# a tall wash shaped round the bloom (deep sage only behind the petals), slim pods laid low as a base,
# and "two leaves and a bud" (the Ceylon plucking standard) climbing the corner onto the brew side.
import sys, os, shutil
sys.path.insert(0,'/home/user/PersonalEventPlanner305App/vanilla-shop/studies/extract/split')
sys.path.insert(0,'/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/teaart')
from comp import flower, mix
from split2 import flush, pod_pair, echo
from greens import pal, build, side_layers, C, ROOT
G3,G1,G2='#6E8C6A','#E2EADB','#B4C8AC'
p=pal(G3); p.update(pod_core='#5E3E26',pod_edge='#3A2414')   # pods a shade lighter: a base, not a headline
O=ROOT+'w-sage2/'; os.makedirs(O,exist_ok=True)
def cube():
    FW,SW=87.6,84.6; f=FW+3
    def art(cv):
        echo(cv,p,(f-15,21),30,0.8)
        pod_pair(cv,p,(f-82,86),-7,80,2.1)
        flush(cv,p,(f+4,96),-92,1.05)
        flush(cv,p,(f+36,98),-102,0.8)
        flower(cv,(f-21,61),40,1.7,p,blurs=(0.3,0.26,0.5))
    build(O,'cube',FW,SW,art,side_layers(FW,SW,G1,G2)+[
        ([C(70,55,28,38),C(40,82,34,8),C(73,19,15,11)],1.0,G1,0.7,0.4),
        ([C(71,59,19,25),C(88,74,10,14)],1.0,G2,0.65,0.1),
        ([C(73,57,11,13)],1.0,G3,0.6,-0.2)])
def long():
    FW,SW=175.9,85.1; f=FW+3
    def art(cv):
        echo(cv,p,(f-70,20),30,1.1)
        pod_pair(cv,p,(f-104,84),-6,100,2.6)
        flush(cv,p,(f+5,96),-92,1.3)
        flush(cv,p,(f+70,100),-100,1.0)
        flower(cv,(f-36,45),40,2.6,p,blurs=(0.3,0.26,0.5))
    build(O,'long',FW,SW,art,side_layers(FW,SW,G1,G2)+[
        ([C(138,46,42,44),C(110,80,46,9),C(106,19,18,12)],1.0,G1,0.7,0.4),
        ([C(140,46,30,30),C(176,72,12,16)],1.0,G2,0.65,0.1),
        ([C(142,44,17,18)],1.0,G3,0.6,-0.2)])
if __name__=='__main__':
    {'cube':cube,'long':long}[sys.argv[1]]()
    shutil.copy(ROOT+'bw2/paper.jpg',O+'paper.jpg'); shutil.copy(ROOT+'bw2/paper.jpg',O+'paper-lid.jpg'); print('ok',sys.argv[1])
