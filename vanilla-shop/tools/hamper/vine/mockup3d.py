# 3D previews of the hamper: the lid (top and sides from the rendered artwork) over the 1 in of base that shows below
# it, from above at a table (35 degrees) and nearly level, as on a shelf.
#   python3 mockup3d.py DIR   (DIR holds top.png, side-long.png, side-end.png rendered from the SVGs, bleed trimmed)
import sys
d = sys.argv[1].rstrip('/') + '/'
k = 2.2                                                   # px per mm
W, D, LD, B = 368.3 * k, 228.6 * k, 88.9 * k, 25.4 * k   # lid length, width, skirt depth, base showing
I = 3 * k                                                # base inset under the lid
def face(img, w, h, tr, extra=''):
    bg = f'url(file://{d}{img}) center/100% 100%' if img.endswith('.png') else img
    return (f'<div style="position:absolute;left:{-w/2}px;top:{-h/2}px;width:{w}px;height:{h}px;background:{bg};'
            f'transform:{tr};backface-visibility:hidden">{extra}</div>')
def shade(a): return f'<div style="position:absolute;inset:0;background:rgba(0,0,0,{a})"></div>'
def box(rx, ry):
    base = '#5E1823'
    bw, bd = W - 2 * I, D - 2 * I
    f = [  # base reveal, below the lid
        face(base, bw, B, f'translateY({LD/2 + B/2}px) translateZ({bd/2}px)', shade(0.10) + '<div style="height:30%;background:linear-gradient(rgba(0,0,0,.45),transparent)"></div>'),
        face(base, bd, B, f'translateY({LD/2 + B/2}px) rotateY(90deg) translateZ({bw/2}px)', shade(0.28) + '<div style="height:30%;background:linear-gradient(rgba(0,0,0,.45),transparent)"></div>'),
        face(base, bd, B, f'translateY({LD/2 + B/2}px) rotateY(-90deg) translateZ({bw/2}px)', shade(0.28)),
        face(base, bw, B, f'translateY({LD/2 + B/2}px) rotateY(180deg) translateZ({bd/2}px)', shade(0.2)),
        # the lid
        face('side-long.png', W, LD, f'translateZ({D/2}px)', shade(0.04)),
        face('side-end.png', D, LD, f'rotateY(90deg) translateZ({W/2}px)', shade(0.22)),
        face('side-end.png', D, LD, f'rotateY(-90deg) translateZ({W/2}px)', shade(0.22)),
        face('side-long.png', W, LD, f'rotateY(180deg) translateZ({D/2}px)', shade(0.1)),
        face('top.png', W, D, f'translateY({-LD/2}px) rotateX(90deg)', '<div style="position:absolute;inset:0;background:linear-gradient(115deg,rgba(255,240,220,.10),transparent 45%,rgba(0,0,0,.06))"></div>'),
    ]
    return (f'<div style="position:absolute;left:50%;top:52%;transform-style:preserve-3d;transform:rotateX({rx}deg) rotateY({ry}deg)">'
            + ''.join(f.replace('backface-visibility:hidden', 'backface-visibility:hidden;') for f in f) + '</div>')
for name, rx, ry in (('table', -34, -28), ('shelf', -7, -24)):
    html = ('<html><body style="margin:0"><div style="position:relative;width:1600px;height:1100px;overflow:hidden;'
            'background:radial-gradient(ellipse at 50% 30%,#EFE9DF,#D9D0C2);perspective:3200px">'
            '<div style="position:absolute;left:250px;right:250px;top:760px;height:260px;background:radial-gradient(closest-side,rgba(40,20,10,.35),transparent)"></div>'
            + box(rx, ry) + '</div></body></html>')
    open(d + f'3d-{name}.html', 'w').write(html)
print('ok')
