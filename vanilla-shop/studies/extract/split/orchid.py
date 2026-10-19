# A vanilla orchid drawn as vector: five narrow tepals in a loose star, a frilled trumpet lip, and cured pods.
import math
def _pt(cx,cy,a,r): return cx+r*math.cos(a), cy+r*math.sin(a)
def tepal(cx,cy,ang,L,w,bend=0.12):
    a=math.radians(ang); d=(math.cos(a),math.sin(a)); p=(-d[1],d[0])
    tip=(cx+d[0]*L+p[0]*L*bend*0.5, cy+d[1]*L+p[1]*L*bend*0.5)
    def q(t,s): return (cx+d[0]*L*t+p[0]*w*L*s+p[0]*L*bend*t*t*0.5, cy+d[1]*L*t+p[1]*w*L*s+p[1]*L*bend*t*t*0.5)
    b1=q(0.12,0.35); c1=q(0.38,1.0); c2=q(0.78,0.75); b2=q(0.12,-0.35); c3=q(0.38,-1.0); c4=q(0.78,-0.75)
    f=lambda P:f'{P[0]:.3f} {P[1]:.3f}'
    return f'M{f(b1)}C{f(c1)} {f(c2)} {f(tip)}C{f(c4)} {f(c3)} {f(b2)}Z'
# tepal angles (deg, 0 = right, clockwise in SVG), length factor, width, bend
TEPALS=[(-96,1.00,0.17,0.10),(-158,0.92,0.16,-0.14),(-22,0.94,0.16,0.14),(138,0.86,0.15,0.12),(44,0.88,0.15,-0.12)]
def flower(cx,cy,R):
    """returns dict of path strings: tepals, lip (frilled trumpet), throat"""
    tp=[tepal(cx,cy,a,R*l,w,b) for a,l,w,b in TEPALS]
    # lip: a trumpet running from the column down and forward, its mouth frilled and open to the viewer
    lx,ly=cx+R*0.06,cy+R*0.34; rx,ry=R*0.25,R*0.19; n=9; mouth=[]
    for i in range(n*10+1):
        t=2*math.pi*i/(n*10); k=1+0.09*math.sin(n*t)
        mouth.append((lx+rx*k*math.cos(t), ly+ry*k*math.sin(t)))
    lip='M'+'L'.join(f'{x:.3f} {y:.3f}' for x,y in mouth)+'Z'
    tube=(f'M{cx-R*0.09:.3f} {cy-R*0.02:.3f}Q{cx-R*0.16:.3f} {cy+R*0.18:.3f} {lx-rx*0.95:.3f} {ly-ry*0.2:.3f}'
          f'L{lx+rx*0.95:.3f} {ly-ry*0.2:.3f}Q{cx+R*0.22:.3f} {cy+R*0.14:.3f} {cx+R*0.09:.3f} {cy-R*0.02:.3f}Z')
    throat=f'M{lx-rx*0.55:.3f} {ly+ry*0.05:.3f}a{rx*0.55:.3f} {ry*0.5:.3f} 0 1 0 {rx*1.1:.3f} 0a{rx*0.55:.3f} {ry*0.5:.3f} 0 1 0 {-rx*1.1:.3f} 0Z'
    column=f'M{cx:.3f} {cy:.3f}Q{cx+R*0.03:.3f} {cy+R*0.12:.3f} {lx:.3f} {ly-ry*0.1:.3f}'
    lr=rx
    return dict(tepals=tp,tube=tube,lip=lip,throat=throat,column=column,lipc=(lx,ly,lr))
def pod(x0,y0,x1,y1,w,hook=1,sag=0.08):
    """a long slim cured pod from (x0,y0) to (x1,y1) with a curled hook at the far end"""
    dx,dy=x1-x0,y1-y0; L=math.hypot(dx,dy); ux,uy=dx/L,dy/L; px,py=-uy,ux
    m=lambda t,s:(x0+dx*t+px*(L*sag*math.sin(math.pi*t)+w*s), y0+dy*t+py*(L*sag*math.sin(math.pi*t)+w*s))
    f=lambda P:f'{P[0]:.3f} {P[1]:.3f}'
    a=m(0,0.15); b=m(0.5,0.55); c=m(0.97,0.25); d=m(0.97,-0.25); e=m(0.5,-0.55); g=m(0,-0.15)
    body=f'M{f(a)}Q{f(b)} {f(c)}L{f(d)}Q{f(e)} {f(g)}Z'
    # hook: a small curl past the tip
    tip=m(1.0,0); r=w*0.9*hook
    hx,hy=tip[0]+ux*r*0.6,tip[1]+uy*r*0.6
    curl=f'M{f(m(0.96,0))}Q{hx+ux*r:.3f} {hy+uy*r:.3f} {hx+px*r:.3f} {hy+py*r:.3f}Q{hx+px*r*1.2-ux*r*0.6:.3f} {hy+py*r*1.2-uy*r*0.6:.3f} {hx+px*r*0.5-ux*r*0.5:.3f} {hy+py*r*0.5-uy*r*0.5:.3f}'
    spine=f'M{f(m(0.04,0))}Q{f(m(0.5,0))} {f(m(0.95,0))}'
    return dict(body=body,curl=curl,spine=spine)
