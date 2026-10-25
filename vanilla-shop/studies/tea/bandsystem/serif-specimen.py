# One sheet: "Vanilla Tea" in every candidate serif that is free for commercial use, on the white band, same size.
import os
S='/tmp/claude-0/-home-user-PersonalEventPlanner305App/0712b206-ea71-562e-9a83-45f8f096455f/scratchpad/'
A=S+'ff2/'; F=S+'ff/'; N=S+'newfonts/x/'; R='/home/user/PersonalEventPlanner305App/vanilla-shop/fonts/'
fz=lambda p,n:N+f'{p}/Fonts/OTF/{n}.otf'
C=[('Redaction Bold','OFL · MoMA PS1 commission',F+'redaction-700-normal.ttf'),('Redaction','OFL',F+'redaction-400-normal.ttf'),
   ('Playfair 2 SemiBold','OFL · the 2023 redraw, not Playfair Display',A+'playfair-600.ttf'),('Playfair 2','OFL',A+'playfair-400.ttf'),
   ('Fraunces SemiBold','OFL',A+'fraunces-600.ttf'),('Newsreader SemiBold','OFL · Production Type',A+'newsreader-600.ttf'),
   ('Libre Caslon Display','OFL',A+'libre-caslon-display-400.ttf'),('Bodoni Moda Medium','OFL',A+'bodoni-moda-500.ttf'),
   ('DM Serif Display','OFL',A+'dm-serif-display-400.ttf'),('Young Serif','OFL',A+'young-serif-400.ttf'),
   ('Bagnard','OFL · Use & Modify',A+'bagnard-400.ttf'),('Cormorant Bold','OFL',A+'cormorant-700.ttf'),
   ('Gambetta Semibold','Fontshare FFL',fz('gambetta/Gambetta_Complete','Gambetta-Semibold')),('Erode Semibold','Fontshare FFL',N+'erode/Erode_Complete/Fonts/OTF/Erode-Semibold.otf'),
   ('Sentient Medium','Fontshare FFL',N+'sentient/Sentient_Complete/Fonts/OTF/Sentient-Medium.otf'),('Boska Medium','Fontshare FFL',fz('boska/Boska_Complete','Boska-Medium')),
   ('Hedvig Letters Serif','OFL · Kanon',F+'hedvig-letters-serif-400-normal.ttf'),('Instrument Serif','OFL · current brand',A+'instrument-serif-400.ttf')]
C=[c for c in C if os.path.exists(c[2])]
css=''.join(f"@font-face{{font-family:f{i};src:url(file://{c[2]})}}" for i,c in enumerate(C))+f"@font-face{{font-family:lab;src:url(file://{F}uncut-sans-500-normal.ttf)}}"
tiles=''.join(f'''<div class=t><div class=n><span>{i+1:02d}</span> {c[0]} <em>{c[1]}</em></div>
<div class=v style="font-family:f{i}"><b>Vanilla</b> Tea</div><div class=c style="font-family:f{i}">VANILLA TEA</div></div>''' for i,c in enumerate(C))
html=f'''<html><head><meta charset=utf-8><style>{css}html,body{{margin:0;background:#E9E5DC}}
.g{{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;padding:24px;width:2350px}}
.t{{background:#F6F3EC;padding:22px 30px 26px;height:250px;box-sizing:border-box;border-top:16px solid #113C3A}}
.n{{font:500 20px lab;color:#4D6E6A;margin-bottom:16px}} .n span{{color:#113C3A}} .n em{{font-style:normal;opacity:.6;margin-left:8px}}
.v{{font-size:92px;line-height:1;color:#123B39;white-space:nowrap}} .v b{{font-weight:inherit;color:#A07A2C}}
.c{{font-size:40px;letter-spacing:.08em;color:#123B39;margin-top:16px}}</style></head><body><div class=g>{tiles}</div></body></html>'''
open(S+'teasoap/specimen.html','w').write(html); print(len(C))
