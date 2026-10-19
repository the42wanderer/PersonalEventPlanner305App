# Hand-placed pods for No. 03. Each pod is a cubic Bezier centre line (four control points, mm on the 60 x 70 panel),
# a half-width, and a depth. Curled pods bend up at the end like a banana: the curl is in the control points, the
# thickness is kept to the end and the end is rounded, never pointed.
import numpy as np
def bez(P,n=120):
    P=np.array(P,float); t=np.linspace(0,1,n)[:,None]
    return (1-t)**3*P[0]+3*(1-t)**2*t*P[1]+3*(1-t)*t**2*P[2]+t**3*P[3]
def path(P):
    """one cubic (four points) or a chain of cubics (a list of four-point lists)"""
    if isinstance(P[0][0],(list,tuple)): return np.vstack([bez(seg,80)[(1 if i else 0):] for i,seg in enumerate(P)])
    return bez(P)
def outline(P,W,stalk=0.1):
    """closed outline: narrow at the stalk, full body, round cap at the end"""
    c=path(P); d=np.gradient(c,axis=0); d/=np.linalg.norm(d,axis=1,keepdims=True); nr=np.stack([-d[:,1],d[:,0]],1)
    t=np.linspace(0,1,len(c))
    w=np.where(t<stalk, 0.35+(W-0.35)*np.sin(np.pi/2*np.clip(t/stalk,0,1))**1.6, W*(1+0.05*np.sin(np.pi*t)))
    L=c+nr*w[:,None]; R=c-nr*w[:,None]
    a0=np.arctan2(nr[-1,1],nr[-1,0]); cap=[c[-1]+W*np.array([np.cos(a0-k),np.sin(a0-k)]) for k in np.linspace(0,np.pi,24)]
    return np.vstack([L,np.array(cap),R[::-1]]), c
TOP=(31,9)
X,Y=TOP
# (control points, half-width, depth 0 back .. 1 front). A short fan below the node, then the pods hang
# almost parallel; two of them, of different sizes, curl up at the end like a banana.
PODS=[
 ([(X,Y),(X-6,Y+5),(X-9,Y+22),(X-9.5,Y+50)],1.65,0.15),
 ([(X,Y),(X+6,Y+5),(X+9,Y+20),(X+9.8,Y+46)],1.65,0.2),
 ([(X,Y),(X-4.5,Y+6),(X-5.5,Y+30),(X-6,Y+56)],1.75,0.4),
 ([(X,Y),(X+4.2,Y+6),(X+5.4,Y+28),(X+5.8,Y+53)],1.75,0.5),
 # the big curl: hangs, then swings up and out to the left
 ([[(X,Y),(X-4,Y+6),(X-7,Y+26),(X-7.6,Y+44)],[(X-7.6,Y+44),(X-7.9,Y+51),(X-10.5,Y+55),(X-14.5,Y+51.5)]],1.7,0.6),
 ([(X,Y),(X-1.6,Y+6),(X-2,Y+30),(X-2.2,Y+59)],1.85,0.75),
 # a smaller curl, turning right
 ([[(X,Y),(X+2.2,Y+7),(X+3.4,Y+24),(X+3.7,Y+39)],[(X+3.7,Y+39),(X+3.9,Y+45),(X+5.6,Y+48.5),(X+8.6,Y+46.5)]],1.8,0.85),
 ([(X,Y),(X+1.2,Y+6),(X+1.6,Y+30),(X+1.8,Y+55)],1.85,1.0)]
