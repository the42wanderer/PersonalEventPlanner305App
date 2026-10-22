# Over-the-cap neck seal, on the original die shape: a fishtailed strip with a disc in the middle that sits on the cap.
# Measured from vanilla_labeels__final-01.pdf and drawn at the same scale as the 226 x 70 mm wraps (sheet x 226/274).
import sys; sys.path.insert(0,'../w')
from kit import width, logo, txt, caps, css
T='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/ext/d/'
SC=226/274
L,SH,D,NOTCH=120.1*SC,9.9*SC,22.6*SC,6.1*SC          # length, strip height, disc diameter, fishtail depth (mm)
PAD=2; W,H=L+2*PAD,D+2*PAD; cx,cy=W/2,H/2; x0,x1=PAD,PAD+L; t,b=cy-SH/2,cy+SH/2
PAPER='#F7EFDC'
LOOK={'01':dict(ground='#B83A24',dark='#4A120C',on='#FBE7D2'),
      '02':dict(ground='#C98A22',dark='#4A2C08',on='#3B2108'),
      '03':dict(ground='#2F5A33',dark='#16301C',on='#EAF2D6')}
def outline():
    return (f'M{x0} {t}H{x1}L{x1-NOTCH} {cy}L{x1} {b}H{x0}L{x0+NOTCH} {cy}Z')
def seal(k,die=False):
    s=LOOK[k]; o=[]
    o.append(f'<path d="{outline()}" fill="{s["ground"]}"/>')
    # fine rules just inside the strip's edges, following the fishtails
    i=0.75
    for yy in (t+i,b-i):
        o.append(f'<path d="M{x0+NOTCH*0.25} {yy}H{x1-NOTCH*0.25}" stroke="{s["on"]}" stroke-width="0.18" opacity="0.7"/>')
    # the claim on each arm; the left arm is turned over so both read from outside when the seal is folded over the cap
    msg='100% PURE NATURAL VANILLA'; sz=2.05; tr=0.22
    arm=(L-D)/2-NOTCH-1.5; wt=width(msg,'RW',sz,tr)
    if wt>arm: sz*=arm/wt; wt=arm
    ax=cx+D/2+(L/2-D/2-NOTCH)/2+0.4
    o.append(caps(msg,ax,cy+sz*0.36,sz,s['on'],'middle',tr))
    o.append(f'<g transform="rotate(180 {cx} {cy})">'+caps(msg,ax,cy+sz*0.36,sz,s['on'],'middle',tr)+'</g>')
    # the disc on the cap: cream, a ring in the product colour, the logo and the number
    r=D/2
    o+=[f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{PAPER}"/>',
        f'<circle cx="{cx}" cy="{cy}" r="{r-0.9}" fill="none" stroke="{s["ground"]}" stroke-width="0.25"/>',
        f'<circle cx="{cx}" cy="{cy}" r="{r-1.35}" fill="none" stroke="{s["ground"]}" stroke-width="0.12" stroke-dasharray="0.25 0.45"/>',
        logo(cx,cy-1.6,7.6,s['dark']), txt('No. '+k,cx,cy+5.3,2.6,s['ground'],'IS','middle')]
    if die:
        o.append(f'<path d="{outline()}" fill="none" stroke="#FF2BA6" stroke-width="0.15"/><circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#FF2BA6" stroke-width="0.15"/>')
    return o
def save(o,name):
    s_=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W*20:.0f}" height="{H*20:.0f}" viewBox="0 0 {W:.3f} {H:.3f}">'+''.join(o)+'</svg>'
    open(T+name+'.html','w').write(f'<html><head><style>{css}html,body{{margin:0;background:transparent}}</style></head><body>{s_}</body></html>')
if __name__=='__main__':
    for k in ('01','02','03'):
        save(seal(k),f'NK-{k}'); save(seal(k,True),f'NKD-{k}')
    print('ok', round(L,1),'x',round(D,1),'mm; strip',round(SH,1),'px',round(W*20),round(H*20))
