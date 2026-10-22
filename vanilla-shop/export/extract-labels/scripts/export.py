# Print files: every label as a vector PDF page at its print size, with 3 mm bleed, crop marks and a slug line,
# plus a separate die-line page. The design is drawn at 226 x 70 mm; the provided template is 274 x 85 mm, so
# everything is scaled by 274/226 (same proportions).
import sys, json, numpy as np
from PIL import Image
import splitwrap as SW, neck as NK
from kit import css
T=SW.T
S=274/226                      # design mm -> print mm
B=3.0                          # bleed, print mm
M=16.0                         # page margin round the bleed, for crop marks and the slug
OUT=T+'print/'
import os; os.makedirs(OUT,exist_ok=True)
def padded_art(src,b_px,name):
    """the colour art reflected outwards on its left, top and bottom so it runs into the bleed"""
    a=np.asarray(Image.open(T+src).convert('RGB'))
    a=np.pad(a,((b_px,b_px),(b_px,0),(0,0)),mode='reflect'); Image.fromarray(a).save(T+name); return name
def wrap_svg(k,size):
    Z=SW.SIZE[size]; w,h=Z['W'],Z['H']; b=B/S                       # bleed in design mm
    SW.PROOF=False
    if size=='500': o=SW.wrap(k); src=f'wart-{k}.png'; aw=SW.CX
    else: SW.small_art(k,size); o=SW.wrap_small(k,size); src=f'wart-{k}-{size}.png'; aw=w/2
    bp=int(round(b*20)); art=padded_art(src,bp,f'bleed-{src}')
    o[0]=f'<rect x="{-b:.3f}" y="{-b:.3f}" width="{w+2*b:.3f}" height="{h+2*b:.3f}" fill="{SW.PAPER}"/>'
    o[1]=f'<image href="file://{T}{art}" x="{-b:.3f}" y="{-b:.3f}" width="{aw+b:.3f}" height="{h+2*b:.3f}" preserveAspectRatio="none"/>'
    return o,w,h
def seal_svg(k):
    b=B/S; s=NK.LOOK[k]
    # bleed for the shaped seal: the strip and the disc grown outwards by the bleed
    pre=[f'<path d="{NK.outline()}" fill="{s["ground"]}" stroke="{s["ground"]}" stroke-width="{2*b:.3f}" stroke-linejoin="miter" stroke-miterlimit="10"/>',
         f'<circle cx="{NK.cx}" cy="{NK.cy}" r="{NK.D/2+b:.3f}" fill="{SW.PAPER}"/>']
    o=pre+NK.seal(k)
    # shift so the seal's own bounding box starts at 0,0
    g=f'<g transform="translate({-NK.PAD} {-NK.PAD+(NK.D-NK.D)/2})">'+''.join(o)+'</g>'
    return [g],NK.L,NK.D
def dieline(kind,w,h):
    if kind=='seal':
        # one outer cut path: strip ends with their fishtails, joined by arcs over and under the disc
        import math
        r=NK.D/2; cx,cy=NK.cx,NK.cy; t,b=NK.t,NK.b; dx=math.sqrt(r*r-(cy-t)**2)
        d=(f'M{NK.x0} {t}H{cx-dx:.4f}A{r} {r} 0 0 1 {cx+dx:.4f} {t}H{NK.x1}L{NK.x1-NK.NOTCH} {cy}L{NK.x1} {b}'
           f'H{cx+dx:.4f}A{r} {r} 0 0 1 {cx-dx:.4f} {b}H{NK.x0}L{NK.x0+NK.NOTCH} {cy}Z')
        return (f'<g transform="translate({-NK.PAD} {-NK.PAD})" fill="none" stroke="#EC008C" stroke-width="{0.25/S:.3f}"><path d="{d}"/></g>')
    return f'<rect x="0" y="0" width="{w}" height="{h}" fill="none" stroke="#EC008C" stroke-width="{0.25/S:.3f}"/>'
def page(inner,w,h,slug,die=None):
    """one PDF page in print mm: the artwork (design units scaled by S) with bleed, crop marks and a slug"""
    pw,ph=w*S,h*S; PW,PH=max(pw+2*(B+M),150),ph+2*(B+M); x0,y0=(PW-pw)/2,B+M; b=B/S
    art=(f'<svg xmlns="http://www.w3.org/2000/svg" style="position:absolute;left:{x0-B}mm;top:{y0-B}mm" width="{pw+2*B}mm" height="{ph+2*B}mm" '
         f'viewBox="{-b:.4f} {-b:.4f} {w+2*b:.4f} {h+2*b:.4f}">'
         f'<defs><clipPath id="bl"><rect x="{-b}" y="{-b}" width="{w+2*b}" height="{h+2*b}"/></clipPath></defs>'
         f'<g clip-path="url(#bl)">{"".join(inner)}</g>{die or ""}</svg>')
    marks=''
    for (x,y) in ((x0,y0),(x0+pw,y0),(x0,y0+ph),(x0+pw,y0+ph)):
        dx=-1 if x==x0 else 1; dy=-1 if y==y0 else 1
        marks+=(f'<path d="M{x+dx*(B+1)} {y}H{x+dx*(B+8)}M{x} {y+dy*(B+1)}V{y+dy*(B+8)}" stroke="#000" stroke-width="0.12"/>')
    over=(f'<svg xmlns="http://www.w3.org/2000/svg" style="position:absolute;left:0;top:0" width="{PW}mm" height="{PH}mm" viewBox="0 0 {PW} {PH}">{marks}'
          +''.join(f'<text x="{x0-B}" y="{PH-M+B+5.5+i*3.0:.2f}" font-family="G" font-size="2.2" fill="#333">{ln}</text>' for i,ln in enumerate(slug.split(' · ',1)))+'</svg>')
    return PW,PH,f'<div class="p" style="width:{PW}mm;height:{PH}mm">{art}{over}</div>'
if __name__=='__main__':
    jobs=[]
    names={'01':'No01-Vanilla-Extract-with-alcohol','02':'No02-Vanilla-Extract-alcohol-free','03':'No03-Vanilla-Syrup'}
    for k in ('01','02','03'):
        for size in SW.PRICE[k]:
            inner,w,h=wrap_svg(k,size)
            tag='template size' if size=='500' else 'ESTIMATED size, scaled from the template: printer to adjust'
            slug=f'{names[k]} · {size} ml wrap · trim {w*S:.1f} × {h*S:.1f} mm · bleed 3 mm · {tag} · barcode {"from current label" if size=="500" else "PLACEHOLDER"}'
            jobs.append((f'{names[k]}_{size}ml',inner,w,h,slug,'rect'))
        inner,w,h=seal_svg(k)
        jobs.append((f'{names[k]}_neck-seal',inner,w,h,f'{names[k]} · neck seal (over the cap) · trim {w*S:.1f} × {h*S:.1f} mm on the original die shape · bleed 3 mm','seal'))
    manifest=[]
    for name,inner,w,h,slug,kind in jobs:
        for suffix,die in (('',None),('_CUTLINE',dieline(kind,w,h))):
            PW,PH,div=page([] if die else inner,w,h,slug+(' · CUT LINE ONLY (magenta), same position as the artwork file' if die else ''),die)
            html=(f'<html><head><style>{css}@page{{size:{PW}mm {PH}mm;margin:0}}html,body{{margin:0}}'
                  f'.p{{position:relative;overflow:hidden}}</style></head><body>{div}</body></html>')
            open(OUT+name+suffix+'.html','w').write(html); manifest.append([OUT+name+suffix,PW,PH])
    json.dump(manifest,open(OUT+'manifest.json','w'))
    print(len(manifest),'pages')
