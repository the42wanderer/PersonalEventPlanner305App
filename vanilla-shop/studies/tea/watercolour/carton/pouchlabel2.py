# Kraft-pouch labels (70 x 110 mm, arched top, as now) in the Split system: cream top with the name, the painted
# block below; plus a mock-up on the brown kraft pouch.
import re
R='/home/user/PersonalEventPlanner305App/vanilla-shop'
O='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/teaart/fol2/'
F={'IS':R+'/fonts/instrument-serif-italic.ttf','AE':R+'/fonts/archivo-expanded-regular.ttf','G':R+'/fonts/geist-regular.ttf'}
css=''.join(f"@font-face{{font-family:{k};src:url(file://{v})}}" for k,v in F.items())
LOGO=re.search(r' d="([^"]+)"',open(R+'/brand/vanilla-shop-logo.svg').read()).group(1)
LS=open(R+'/brand/ceylon-tea-lion.svg').read(); LV=[float(v) for v in re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)',LS).groups()]; LD=re.search(r' d="([^"]+)"',LS).group(1)
W,H,s=70,110,8.5
outline=f'M0 {H}V{s}H5C12 1 {W-12} 1 {W-5} {s}H{W}V{H}Z'
def svg(art,ink,lines,under):
    gold='url(#g)'
    t=[f'<defs><clipPath id="c"><path d="{outline}"/></clipPath><linearGradient id="g" x1="0" y1="0" x2="1" y2="0.4"><stop offset="0" stop-color="#4A2C06"/><stop offset="0.3" stop-color="#8C5F1C"/><stop offset="0.5" stop-color="#5E3E0C"/><stop offset="0.75" stop-color="#9C7028"/><stop offset="1" stop-color="#4A2C06"/></linearGradient></defs>',
       f'<g clip-path="url(#c)"><image href="file://{O}{art}" x="-3" y="-3" width="76" height="116" preserveAspectRatio="none"/>',
       f'<path d="{LOGO}" fill="{ink}" fill-rule="evenodd" transform="translate({W/2-14:.2f} 9.2) scale({10/933:.5f})"/>',
       f'<path d="M{W/2} 9.6V{9.6+12*LV[1]/LV[0]:.2f}" stroke="{ink}" stroke-width="0.18" opacity="0.4"/>',
       f'<path d="{LD}" fill="{ink}" fill-rule="evenodd" transform="translate({W/2+3.5:.2f} 9.6) scale({11.5/LV[0]:.5f})"/>',
       f'<text x="{W/2}" y="27" font-family="AE" font-size="1.9" letter-spacing="0.5" fill="{ink}" text-anchor="middle">AUTHENTIC CEYLON · 100 G</text>']
    two=len(lines)==2; sz=13.5 if two else 10.5; y=38 if two else 36; step=11 if two else 8.4
    for l,col in lines:
        t.append(f'<text x="{W/2}" y="{y:.1f}" font-family="IS" font-size="{sz}" fill="{gold if col else ink}" text-anchor="middle">{l}</text>'); y+=step
    for i,l in enumerate(under): t.append(f'<text x="{W/2}" y="{y-step+6.5+i*3:.1f}" font-family="G" font-size="2.2" fill="{ink}" text-anchor="middle">{l}</text>')
    t.append('</g>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W*12}" height="{H*12}">'+''.join(t)+'</svg>'
for name,art,ink,lines,under in (('pouch-vanilla','label-vanilla.png','#3E5A3C',[('Vanilla',1),('Tea',0)],['Ceylon black tea with natural vanilla']),):
    open(O+name+'.html','w').write(f'<html><head><meta charset="utf-8"><style>{css}html,body{{margin:0;background:transparent}}</style></head><body>{svg(art,ink,lines,under)}</body></html>')
print('ok')
