# Shared drawing kit for the wrap labels (mm units, 226 x 70).
import re
from PIL import ImageFont
R='/home/user/PersonalEventPlanner305App/vanilla-shop'; CF='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/candlefonts'
T='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/ext/w/'
W,H,CX=226,70,113
FONTS={'GMono':R+'/fonts/geist-mono.ttf','G':R+'/fonts/geist-regular.ttf','GM':R+'/fonts/geist-medium.ttf','GB':R+'/fonts/geist-bold.ttf','IS':R+'/fonts/instrument-serif-italic.ttf','RW':R+'/fonts/archivo-expanded-regular.ttf','RR':CF+'/roc-regular.otf','RB':CF+'/roc-bold.otf','RWM':R+'/fonts/archivo-expanded-medium.ttf'}
css=''.join(f"@font-face{{font-family:{k};src:url(file://{v})}}" for k,v in FONTS.items())
_m={}
def width(t,f,sz,tr=0):
    if f not in _m: _m[f]=ImageFont.truetype(FONTS[f],1000)
    return _m[f].getlength(t)/1000*sz + tr*sz*max(len(t)-1,0)
logoD=re.search(r' d="([^"]+)"',open(R+'/brand/vanilla-shop-logo.svg').read()).group(1)
def logo(cx,cy,lw,c): s=lw/933; return f'<path d="{logoD}" fill="{c}" fill-rule="evenodd" transform="translate({cx-lw/2:.2f} {cy-963*s/2:.2f}) scale({s:.5f})"/>'
def esc(t): return t.replace('&','&amp;')
def txt(t,x,y,sz,c,f='G',a='start',tr=0,op=1):
    return f'<text x="{x:.2f}" y="{y:.2f}" font-family="{f}" font-size="{sz}" letter-spacing="{sz*tr:.3f}" fill="{c}" text-anchor="{a}" opacity="{op}" xml:space="preserve">{esc(t)}</text>'
def caps(t,x,y,sz,c,a='start',tr=0.28,op=1,f='RW'): return txt(t,x,y,sz,c,f,a,tr,op)
def rule(x1,y1,x2,y2,c,w=0.2,op=0.55): return f'<path d="M{x1:.2f} {y1:.2f}L{x2:.2f} {y2:.2f}" stroke="{c}" stroke-width="{w}" opacity="{op}" fill="none"/>'
def para(t,x,y,w,sz,lead,c,f='G'):
    words=t.split(); lines=[]; cur=''
    for wd in words:
        tryl=(cur+' '+wd).strip()
        if width(tryl,f,sz)<=w: cur=tryl
        else: lines.append(cur); cur=wd
    lines.append(cur)
    return [txt(l,x,y+i*lead,sz,c,f) for i,l in enumerate(lines)], y+(len(lines)-1)*lead
def img(href,x,y,w,h,extra=''): return f'<image href="file://{T}{href}" x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" preserveAspectRatio="none" {extra}/>'
# EAN-13 at a given module width (mm)
LC=['0001101','0011001','0010011','0111101','0100011','0110001','0101111','0111011','0110111','0001011']
GC=['0100111','0110011','0011011','0100001','0011101','0111001','0000101','0010001','0001001','0010111']
RC=['1110010','1100110','1101100','1000010','1011100','1001110','1010000','1000100','1001000','1110100']
PAR=['LLLLLL','LLGLGG','LLGGLG','LLGGGL','LGLLGG','LGGLLG','LGGGLL','LGLGLG','LGLGGL','LGGLGL']
def ean13(code,x,y,m=0.264,h=12,c='#111'):
    d=[int(v) for v in code]; assert (10-sum(v*(3 if i%2 else 1) for i,v in enumerate(d[:12]))%10)%10==d[12]
    bits='101'+''.join((LC if p=='L' else GC)[v] for p,v in zip(PAR[d[0]],d[1:7]))+'01010'+''.join(RC[v] for v in d[7:])+'101'
    guards={0,1,2,45,46,47,48,49,92,93,94}; o=[f'<rect x="{x-1.2:.2f}" y="{y-1:.2f}" width="{95*m+2.4+1.5:.2f}" height="{h+4.6:.2f}" fill="#FFFFFF"/>']
    path=''
    for i,b in enumerate(bits):
        if b=='1': hh=h+(1.6 if i in guards else 0); path+=f'M{x+i*m:.3f} {y:.2f}h{m:.3f}v{hh:.2f}h{-m:.3f}z'
    o.append(f'<path d="{path}" fill="{c}"/>')
    sz=2.0; o+= [txt(code[0],x-0.9,y+h+2.0,sz,c,'G','middle'), txt(code[1:7],x+(3+21)*m,y+h+2.0,sz,c,'G','middle',0.12), txt(code[7:],x+(50+21)*m,y+h+2.0,sz,c,'G','middle',0.12)]
    return o, 95*m
def svg(o,name,w=W,h=H):
    s=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w*20}" height="{h*20}" viewBox="0 0 {w} {h}">'+''.join(o)+'</svg>'
    open(T+name+'.html','w').write(f'<html><head><style>{css}html,body{{margin:0;background:transparent}}</style></head><body>{s}</body></html>')
    open(T+name+'.svg','w').write(s)
