# 3D mockup of the hamper (365 x 227 x 105 mm, lid about 40 mm deep) with the new candle box beside it.
O='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/hamper/'
RP='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/report/'
G={'green':('#1E3B2A','#16301F','#11251A'),'red':('#7A1C22','#621519','#4E1014')}
def box(L,W,H,top,side,front,s,extra=''):
    # an upright cuboid in px: L along x, W along z (depth), H up
    L,W,H=L*s,W*s,H*s
    f=lambda c,img: (f'background:{c};' if not img else f'background:url({img}) center/100% 100%;')
    return (f'<div style="position:absolute;transform-style:preserve-3d;{extra}">'
      f'<div style="position:absolute;left:{-L/2}px;top:{-W/2}px;width:{L}px;height:{W}px;{f(*top)}transform:translateY({-H}px) rotateX(90deg)"></div>'
      f'<div style="position:absolute;left:{-L/2}px;top:{-H}px;width:{L}px;height:{H}px;{f(*front)}transform:translateZ({W/2}px)"></div>'
      f'<div style="position:absolute;left:{-W/2}px;top:{-H}px;width:{W}px;height:{H}px;{f(*side)}transform:rotateY(90deg) translateZ({L/2}px)"></div></div>')
def hamper(c,s,x,y,ry):
    g,d,b=G[c]
    base=box(359,221,72,(g,None),(b,None),(d,None),s)
    lid=box(365,227,40,(None,f'file://{O}lid-{c}-mock.jpg'),(d,None),(g,None),s,f'transform:translateY({-70*s}px)')
    return f'<div style="position:absolute;left:{x}px;top:{y}px;transform-style:preserve-3d;transform:rotateX(-24deg) rotateY({ry}deg)">{base}{lid}</div>'
def candle(k,s,x,y,ry):
    fr=f'file://{RP}cd-{k}-front.jpg'; sd=f'file://{RP}cd-{k}-side.jpg'; tp=f'file://{RP}cd-{k}-top.jpg'
    return f'<div style="position:absolute;left:{x}px;top:{y}px;transform-style:preserve-3d;transform:rotateX(-24deg) rotateY({ry}deg)">{box(90,90,95,(None,tp),(None,sd),(None,fr),s)}</div>'
for c,k in (('green','velvet'),('red','harmony')):
    sc=(f'<div style="position:relative;width:1800px;height:1100px;background:linear-gradient(#ECE6DC,#DED6C9);overflow:hidden;perspective:3200px">'
        f'<div style="position:absolute;left:220px;right:220px;top:790px;height:150px;background:radial-gradient(closest-side,rgba(40,25,10,.28),transparent)"></div>'
        +hamper(c,s:=3.0,820,820,-26)+candle(k,3.0,1500,930,-30)+'</div>')
    open(O+f'mock-{c}.html','w').write(f'<html><head><meta charset="utf-8"><style>html,body{{margin:0}}</style></head><body>{sc}</body></html>')
print('ok')
