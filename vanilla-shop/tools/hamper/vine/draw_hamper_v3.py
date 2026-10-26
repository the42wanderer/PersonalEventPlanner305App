# Christmas vine, v3: the v2 study (draw_hamper_v2.py, unchanged composition) with added elements for a richer,
# more finished lid: a tone-on-tone sparkle ground, a fine gold double-rule border the botanicals break across, a
# hairline cartouche round the centre lettering, star anise, pine cones, tied cinnamon quills and more stars.
#   python3 draw_hamper_v3.py [OUTDIR]
from pathlib import Path
import math, sys
OUT=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).parent
R='#701F2C'; D='#4F1724'; M='#8C3941'; G='#C9A76A'; I='#F1E4C9'
def p(d,fill='none',stroke=G,w=2):
 return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'
def group(body,t='',id=''):
 return f'<g'+(f' id="{id}"' if id else '')+f' transform="{t}">{body}</g>'
def place(body,x,y,a=0,s=1):return group(body,f'translate({x} {y}) rotate({a}) scale({s})')
def mirror(body):return group(body,'translate(1460 0) scale(-1 1)')

# Deliberate asymmetry within each botanical silhouette; reflection is used only
# for the finished pair of arrangements, not to invent each leaf or flower.
def leaf(kind=0,style='light'):
 contours=[
 'M0 0 C-20-13-37-34-38-61 C-40-99-5-123-6-157 C21-137 40-113 37-84 C33-45 8-27 0 0Z',
 'M0 0 C-22-9-53-37-54-62 C-57-92-30-115-33-143 C-8-127 16-96 8-65 C3-45-1-22 0 0Z',
 'M0 0 C-2-33 11-58 35-77 C58-94 74-103 82-127 C94-87 79-59 55-41 C34-25 18-19 0 0Z',
 'M0 0 C-19-19-27-49-18-76 C-8-101 15-124 15-148 C44-113 49-89 34-56 C21-28 3-22 0 0Z',
 'M0 0 C-15-12-34-24-39-47 C-45-75-34-85-37-104 C-5-89 13-72 10-47 C8-27-3-16 0 0Z'
 ]
 axes=[
 'M0-6 C6-44 15-95-6-148',
 'M-2-7 C-21-45-36-89-33-134',
 'M7-8 C35-37 65-72 79-115',
 'M2-8 C14-47 27-92 15-138',
 'M-1-7 C-17-40-30-70-35-96']
 veins=[[
 'M5-29 C-9-36-20-49-25-60','M9-48 C-7-56-20-72-24-84','M11-69 C-3-81-12-95-13-112',
 'M7-39 C18-49 26-61 30-74','M11-60 C22-72 28-88 28-100','M10-84 C19-97 21-111 16-124'],[
 'M-10-26 C-24-30-35-40-41-51','M-19-47 C-31-50-43-64-44-76','M-28-72 C-38-77-44-90-41-101',
 'M-15-37 C-7-48-2-59-2-69','M-24-61 C-16-72-13-86-16-98','M-31-87 C-24-98-25-111-29-120'],[
 'M21-24 C16-39 23-54 32-63','M37-43 C32-58 40-72 49-79','M54-65 C51-77 58-90 66-96',
 'M28-32 C42-32 55-39 65-50','M47-54 C62-53 73-65 78-76','M64-80 C75-81 79-88 82-97'],[
 'M8-29 C-3-39-10-51-10-62','M14-50 C1-64-2-76 2-87','M21-78 C10-90 9-103 12-116',
 'M11-39 C26-47 30-56 33-66','M18-62 C31-72 36-82 35-94','M23-88 C32-99 32-109 28-120'],[
 'M-10-28 C-23-29-31-40-31-49','M-20-49 C-31-54-34-67-33-77','M-15-38 C-5-46-2-57-5-66']]
 fill,edge,ink={'light':(I,I,R),'gold':(G,G,R),'dark':(R,G,G),'muted':(M,M,G)}[style]
 return p(contours[kind],fill,edge,1.6)+p(axes[kind],'none',ink,2)+''.join(p(v,'none',ink,1.15) for v in veins[kind])

def orchid():
 # Narrow sepals occupy their own plane behind the two curled lateral petals.
 back=[
 ('M-4 1 C-26-34-22-66-12-95 C-3-123-3-144-10-165 C22-149 36-123 28-94 C21-67 6-32-4 1Z','M-3-12 C11-60 16-111-8-154'),
 ('M-8 4 C-45 18-58 53-76 77 C-92 101-115 109-132 111 C-98 125-70 111-47 88 C-29 68-17 39-8 4Z','M-17 25 C-47 74-78 105-121 112'),
 ('M7 1 C35 12 51 37 62 63 C73 90 87 104 108 113 C80 114 55 98 37 75 C19 51 10 28 7 1Z','M18 23 C44 65 68 94 99 109')]
 out=''
 for a,b in back:out+=p(a,I,I,2)+p(b,'none',R,1.5)
 # Asymmetrical, curved lateral petals with folded ends.
 a='M-4-11 C-28-39-52-57-81-61 C-107-65-119-75-125-94 C-128-64-119-43-94-30 C-66-15-31-20-4-11Z'
 b='M5-11 C37-43 67-62 97-59 C118-57 132-62 141-72 C134-47 115-29 90-26 C58-22 27-28 5-11Z'
 out+=p(a,I,I,1.8)+p(b,I,I,1.8)
 for d in [
 'M-11-15 C-48-33-88-31-115-69','M-25-24 C-53-42-82-39-107-65',
 'M-41-35 C-62-48-81-46-99-61','M13-15 C59-39 102-29 131-59',
 'M34-29 C70-48 102-40 122-55','M54-40 C80-53 98-49 113-55']:
  out+=p(d,'none',R,1.4)
 # Curved tubular lip widening into a ruffled mouth, not a scalloped blob.
 out+=p('M-13-9 C-31 2-29 23-25 40 C-24 53-32 62-43 70 C-38 69-33 72-31 78 C-24 74-19 76-16 82 C-9 78-2 81 1 86 C7 79 14 81 19 77 C26 82 30 77 33 72 C40 74 45 68 48 61 C32 56 24 44 23 30 C22 13 24 1 12-8 C5-14-5-15-13-9Z',I,I,1.5)
 out+=p('M-10 11 C-17 21-16 32-8 39 C-3 43 5 40 10 33 C15 25 10 14 4 11 C-2 8-6 8-10 11Z',R,'none',0)
 out+=p('M-21 47 C-13 60-15 67-19 72 M-12 53 C-7 64-6 72-7 77 M-2 54 C1 65 4 71 6 76 M9 51 C15 61 20 66 25 69 M18 44 C23 55 31 60 37 62','none',R,1.5)
 out+=p('M-5-12 C-12-4-11 8-4 17 C0 22 6 19 8 14 C11 6 5-8-5-12Z',G,R,1.5)
 return out

def pods():
 out=''
 for dx,dy,angle,length in [(0,0,-14,1),(15,3,-2,.92),(29,4,10,.83)]:
  body=p('M0 0 C-6 44-16 101-14 152 C-14 191-7 224 4 235 C10 241 15 240 15 236 C9 227 4 205 3 178 C0 116 5 58 6 10 C7 2 5-3 0 0Z',G,'none',0)
  body+=p('M2 10 C-5 65-10 124-8 164 C-7 193-3 217 5 229','none',R,1.6)
  out+=place(body,dx,dy,angle,length)
 return out

def berries():
 out=p('M0 0 C-4-25 3-47 5-74 M0-22 C-19-28-24-43-24-54 M1-38 C18-43 23-53 24-64 M4-58 C-5-66-8-78-7-88','none',G,1.6)
 for x,y,r in [(5,-80,6),(-24,-60,7),(25,-70,6),(-8,-94,5.2)]:
  out+=f'<circle cx="{x}" cy="{y}" r="{r}" fill="{G}"/>'
  out+=p(f'M{x-r*.36} {y-r*.36} q{r*.20} {-r*.28} {r*.42} {-r*.22}','none',R,1.2)
 return out

def fir():
 out=p('M0 0 C-3-34 3-73 8-116','none',G,1.5)
 # Evergreen needles drawn as small tapered shapes with systematic attachment.
 for k in range(8):
  y=-12-k*12; x=.0008*y*y; length=23-k*1.45
  out+=p(f'M{x} {y} C{x-8} {y-1} {x-length} {y-11} {x-length-2} {y-21} C{x-length+9} {y-13} {x-6} {y-9} {x} {y}Z',G,'none',0)
  out+=p(f'M{x+1} {y-4} C{x+12} {y-10} {x+length} {y-17} {x+length+1} {y-26} C{x+length-9} {y-19} {x+7} {y-13} {x+1} {y-4}Z',G,'none',0)
 return out


# ---- v3 additions ----
def star_anise(seeds=True):
 """eight boat-shaped carpels round a small hub, each split open on a glossy seed"""
 out=''
 for k in range(8):
  a=k*45+(4 if k%2 else -3); L=1-(0.08 if k%3==1 else 0)
  c=p('M0-5 C8-10 10-27 4-41 C2-45-2-45-4-41 C-10-27-8-10 0-5Z',G,R,1.3)
  c+=p('M0-15 C3.5-21 3.5-29 0-35 C-3.5-29-3.5-21 0-15Z',R,'none',0)
  if seeds:c+=p('M0-18 C2-22 2-28 0-31 C-2-28-2-22 0-18Z',I,'none',0)
  out+=group(c,f'rotate({a}) scale({L})')
 out+=f'<circle r="5.5" fill="{G}" stroke="{R}" stroke-width="1.3"/>'
 return out

def pine_cone():
 """broad woody scales in staggered rows, each lower row lapping over the one above; a short stalk"""
 out=p('M0-50 C2-60 0-70 5-80','none',G,3.2)
 rows=[(-46,22,2),(-32,30,3),(-17,34,3),(-2,33,4),(13,30,3),(28,24,3),(42,17,2),(55,9,1)]
 for i,(y,half,n) in enumerate(rows):
  sw=2*half/n
  for j in range(n):
   x=-half+sw*(j+0.5)
   s_=sw*0.62; h=14+4*(1-abs(y)/60)
   sh=(f'M{x-s_:.1f} {y:.1f} C{x-s_*1.05:.1f} {y+h*0.6:.1f} {x-s_*0.45:.1f} {y+h*0.95:.1f} {x:.1f} {y+h:.1f} '
       f'C{x+s_*0.45:.1f} {y+h*0.95:.1f} {x+s_*1.05:.1f} {y+h*0.6:.1f} {x+s_:.1f} {y:.1f}Z')
   out+=p(sh,G,R,1.6)
   u=y+h*0.62; k=s_*0.32
   out+=p(f'M{x-k:.1f} {u:.1f} L{x:.1f} {u-k*0.7:.1f} L{x+k:.1f} {u:.1f} L{x:.1f} {u+k*0.7:.1f}Z',R,'none',0)   # the umbo
 return out

def cinnamon():
 """three rolled quills, tied with a fine ivory ribbon in a bow"""
 out=''
 for dy,ln,dx in [(-7,150,6),(7,142,0),(0,156,-4)]:
  q=p(f'M0 -6.5 H{ln} C{ln+3} -6.5 {ln+4.5} 6.5 {ln} 6.5 H0Z',G,R,1.3)
  q+=p(f'M14 -2.5 H{ln*0.46} M{ln*0.55} -2.5 H{ln-12} M24 2.5 H{ln*0.7}','none',R,1)
  q+=f'<ellipse cx="0" cy="0" rx="3.6" ry="6.5" fill="{I}" stroke="{R}" stroke-width="1.2"/>'
  q+=p('M0.4 0.3 C-1.6 0.3-1.6-3 0.6-3 C3-3 2.6 2.8-0.2 3.4','none',R,1)
  out+=group(q,f'translate({dx} {dy})')
 out+=p('M70-15 C72-5 72 5 70 16 L77 16 C79 5 79-5 77-15Z',I,R,1)
 out+=p('M74 16 C64 26 58 34 60 42 C66 38 70 30 74 18 C80 30 86 38 92 40 C92 32 86 24 74 16Z',I,R,1)
 out+=p('M73 18 C70 30 66 40 58 50 M75 18 C78 30 84 40 90 52','none',I,1.6)
 return out

def sparkle(x,y,r,col=G):
 return p(f'M{x} {y-r} C{x+r*.12} {y-r*.12} {x+r*.12} {y-r*.12} {x+r} {y} C{x+r*.12} {y+r*.12} {x+r*.12} {y+r*.12} {x} {y+r} '
          f'C{x-r*.12} {y+r*.12} {x-r*.12} {y+r*.12} {x-r} {y} C{x-r*.12} {y-r*.12} {x-r*.12} {y-r*.12} {x} {y-r}Z',col,'none',0)

left=[]
# Rich but quiet secondary silhouettes fill gaps behind the principal drawing.
for x,y,a,s,k in [(139,316,-35,1.0,1),(183,256,35,.83,0),(159,615,-35,1.0,1),(304,729,50,1.0,0),(470,807,-68,.9,0),(392,115,-40,.85,1),(585,90,-65,.74,0)]:
 left.append(place(leaf(k,'muted'),x,y,a,s))
left.append(p('M730 817 C554 861 346 809 236 692 C141 591 125 451 172 315 C218 181 315 105 455 100 C541 97 642 120 730 82','none',G,3.3))
left.append(p('M236 692 C225 611 236 564 259 528 M172 315 C110 300 89 256 87 221 M224 212 C257 189 267 155 265 126 M455 100 C430 76 402 62 371 65 M360 778 C348 821 321 846 286 853','none',G,2))

for x,y,a,s in [(151,410,-55,.95),(204,237,48,.88),(313,750,-67,.94),(439,811,77,.89),(530,108,-69,.83),(109,537,-34,.75)]:left.append(place(fir(),x,y,a,s))
placements=[
 (174,312,-68,.85,1,'light'),(195,267,15,.82,2,'dark'),(238,205,-39,.78,0,'gold'),
 (278,159,52,.65,2,'light'),(349,120,-60,.70,1,'dark'),(415,102,66,.63,2,'light'),
 (495,104,-53,.67,0,'gold'),(555,106,64,.61,2,'dark'),(612,104,-54,.52,1,'light'),
 (658,96,54,.48,2,'gold'),(151,386,-72,.75,3,'gold'),(144,449,-71,.78,1,'dark'),
 (155,548,-88,.75,0,'light'),(186,624,-65,.77,1,'dark'),(235,691,-81,.82,0,'gold'),
 (291,740,13,.85,3,'light'),(349,776,-74,.75,0,'dark'),(425,810,80,.77,2,'light'),
 (493,831,-52,.64,1,'gold'),(554,837,73,.62,2,'dark'),(612,832,-64,.55,0,'light'),
 (660,825,67,.46,2,'gold'),(87,221,20,.65,4,'light'),(265,126,-35,.56,1,'light'),
 (371,65,-65,.55,4,'gold'),(286,853,-68,.51,4,'light')]
for x,y,a,s,k,st in placements:left.append(place(leaf(k,st),x,y,a,s))
for x,y,a,s in [(106,591,-35,.80),(293,735,37,.75),(329,144,-18,.70),(570,121,70,.62)]:left.append(place(berries(),x,y,a,s))
left.append(place(pods(),252,520,-14,.80))
# Two orchids at differing scales, each attached to the main vine.
left.append(p('M152 451 C180 444 206 437 236 434 M282 157 C302 166 317 179 328 195','none',G,2.3))
left.append(place(orchid(),238,435,-9,.91))
left.append(place(orchid(),326,198,23,.49))

# Ribbon winds behind a lower stem then visibly folds over it.
left.append(p('M243 686 C274 677 307 700 319 729 C328 753 344 764 374 758 L376 785 C336 801 309 778 298 753 C287 726 266 711 243 716Z',R,G,1.7))
left.append(p('M243 686 C259 721 291 742 332 741 C385 741 430 711 472 718 C494 721 511 732 518 749 C492 736 472 741 450 753 C395 785 324 784 280 754 C256 737 242 712 243 686Z',G,'none',0))
left.append(p('M264 721 C309 768 371 765 426 742 M296 747 C338 769 385 761 421 749','none',R,1.4))
left.append(p('M472 718 C482 738 476 760 457 781 C446 794 446 809 453 820 L430 809 L412 823 C414 801 426 787 441 773 C463 753 474 734 472 718Z',G,R,1.5))

# v3: the spices and cones, set into the frame's open pockets (mirrored with the rest)
left.insert(0,place(cinnamon(),56,806,-24,.8))
left.insert(0,place(pine_cone(),204,796,30,1.0))
left.append(place(star_anise(),96,92,12,.92))
left.append(place(star_anise(),402,872,-8,.62))
left.append(place(star_anise(False),60,686,20,.5))
# v3: stars of several sizes in the open band between the frame and the centre
left.append(''.join(sparkle(x,y,r) for x,y,r in [(408,232,13),(560,190,7),(372,610,9),(512,680,6),(620,640,4),(470,300,4),(338,360,5),(650,232,4)]))
left.append(''.join(f'<circle cx="{x}" cy="{y}" r="2" fill="{G}"/>' for x,y in [(452,262),(596,214),(398,662),(560,700),(355,300),(610,600)]))
left=''.join(left)

# Balanced central seasonal ornament integrates the upper vine ends.
star=p('M730 54 L736 72 L754 78 L736 84 L730 104 L724 84 L706 78 L724 72Z',G,'none',0)
star+=p('M730 61 V96 M713 78 H747','none',R,1.1)
# A restrained, hanging faceted ornament completes the lower frame.
orn=p('M730 800 V822 M721 829 H739 V838 H721Z','none',G,1.6)
orn+=p('M730 838 C703 850 704 868 730 880 C756 868 757 850 730 838Z',G,'none',0)
orn+=p('M730 843 C717 855 717 865 730 875 C743 865 743 855 730 843Z M710 859 H750','none',R,1.3)

def ground_pattern():
 out=''
 for j,y in enumerate(range(24,908,46)):
  for x in range(24+(23 if j%2 else 0),1460,46):
   out+=sparkle(x,y,4.2,'#7A2834') if (x//46+j)%2==0 else f'<circle cx="{x}" cy="{y}" r="1.4" fill="#7A2834"/>'
 return out
def border():
 o,i=26,36; out=''
 for d,w in ((o,1.8),(i,0.9)):
  out+=f'<rect x="{d}" y="{d}" width="{1460-2*d}" height="{908-2*d}" fill="none" stroke="{G}" stroke-width="{w}"/>'
 for cx,cy in ((31,31),(1429,31),(31,877),(1429,877)):
  out+=f'<circle cx="{cx}" cy="{cy}" r="9" fill="{R}"/>'+sparkle(cx,cy,9)+f'<circle cx="{cx}" cy="{cy}" r="1.6" fill="{R}"/>'
 for cx,cy,a in ((730,26,0),(730,882,0)):
  out+=f'<rect x="{cx-24}" y="{cy-6}" width="48" height="12" fill="{R}"/>'+sparkle(cx-14,cy,4)+sparkle(cx+14,cy,4)+f'<circle cx="{cx}" cy="{cy}" r="2.2" fill="{G}"/>'
 return out
def cartouche():
 out=''
 for rx,ry,w in ((262,196,1.4),(252,186,0.8)):
  out+=f'<ellipse cx="730" cy="436" rx="{rx}" ry="{ry}" fill="none" stroke="{G}" stroke-width="{w}"/>'
 for x,y in ((730,240),(730,632),(468,436),(992,436)):
  out+=f'<circle cx="{x}" cy="{y}" r="9" fill="{R}"/>'+sparkle(x,y,8)
 return out

base=f'''<svg xmlns="http://www.w3.org/2000/svg" width="365mm" height="227mm" viewBox="0 0 1460 908">
<title>The Vanilla Shop — Christmas vine, v3</title>
<desc>Original editable vector artwork, revised from the first sparse study. Custom botanical curves, filled leaves, attached evergreen sprays, redesigned orchid lips and ribbon overlaps. Nominal lid size only; no bleed or manufacturing dieline.</desc>
<g id="background">{p('M0 0H1460V908H0Z',R,'none',0)}</g>
<g id="ground-pattern">{ground_pattern()}</g>
<g id="border">{border()}</g>
<g id="cartouche">{cartouche()}</g>
<g id="botanical-frame">{group(left,id='left-botanical')}{group(mirror(left),id='right-botanical')}</g>
<g id="seasonal-ornaments">{star}{orn}</g>
'''
(OUT/'christmas-vine-v3-artwork.svg').write_text(base+'</svg>')
import base64
FONTS=Path(__file__).resolve().parents[3]/'fonts'
def face(fam,file,style='normal',weight=400):
 b=base64.b64encode((FONTS/file).read_bytes()).decode()
 return f"@font-face{{font-family:'{fam}';font-style:{style};font-weight:{weight};src:url(data:font/ttf;base64,{b})}}"
# Brand type: Instrument Serif Italic for the name, Archivo Expanded Light for the tracked capitals (both OFL, in fonts/).
# The faces are embedded so the SVG renders anywhere; in Illustrator install the two fonts and the text stays live.
css=face('Instrument Serif','instrument-serif-italic.ttf','italic')+face('Archivo Expanded','archivo-expanded-light.ttf','normal',300)
types=f'''<defs><style>{css}</style></defs>
<g id="editable-type" fill="{I}" text-anchor="middle">
<text x="730" y="320" font-family="Archivo Expanded" font-weight="300" font-size="14" letter-spacing="6">THE VANILLA SHOP</text>
<text x="730" y="446" font-family="Instrument Serif" font-style="italic" font-size="112">Christmas</text>
<text x="730" y="500" font-family="Archivo Expanded" font-weight="300" font-size="13" letter-spacing="8">COLLECTION</text>
</g>
<g id="centre-flourish">{p('M683 545 C705 550 720 554 730 545 C740 554 755 550 777 545','none',G,1.7)}{p('M730 539 L735 545 L730 551 L725 545Z',G,'none',0)}</g>'''
(OUT/'christmas-vine-v3-typeset.svg').write_text(base+types+'</svg>')
print('V3 created.')
