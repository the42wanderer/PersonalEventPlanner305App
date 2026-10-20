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
    w=np.where(t<stalk, 0.35+(W-0.35)*np.sin(np.pi/2*np.clip(t/stalk,0,1))**1.6, W*(1+0.06*np.sin(np.pi*t)))
    # a banana's end: the last stretch narrows into a small blunt nub
    w=np.where(t>0.86, w*(1-0.62*np.clip((t-0.86)/0.14,0,1)**1.3), w)
    L=c+nr*w[:,None]; R=c-nr*w[:,None]
    we=w[-1]; a0=np.arctan2(nr[-1,1],nr[-1,0]); cap=[c[-1]+we*np.array([np.cos(a0-k),np.sin(a0-k)]) for k in np.linspace(0,np.pi,24)]
    return np.vstack([L,np.array(cap),R[::-1]]), c
TOP=(25,9)
X,Y=TOP
def crescent(spread,ang,L,bow,lift=0.0,flip=False):
    """a pod hanging from the node, slanted ang degrees to the right of vertical, bowed into a gentle crescent
    (bow mm to the lower left of its chord), its last part easing up and right like a banana's end"""
    a=np.radians(ang); d=np.array([np.sin(a),np.cos(a)]); n=np.array([-d[1],d[0]])   # n points lower-left
    S=np.array([X+spread*0.3,Y]); E=S+d*L+np.array([(-1 if flip else 1)*lift*0.6,-lift])
    P1=S+np.array([spread*1.9,L*0.22])
    P2=S+d*L*0.72-n*(-bow)
    return [tuple(S),tuple(P1),tuple(P2),tuple(E)]
# (control points, half-width, depth 0 back .. 1 front)
PODS=[
 (crescent(-4.2, 4,44,3.0,1.0),1.7,0.15),
 (crescent( 4.0,34,42,3.0,1.8),1.7,0.22),
 (crescent(-2.6,11,54,3.4,1.4),1.8,0.45),
 (crescent( 2.6,27,51,3.4,2.0),1.8,0.55),
 (crescent(-1.0,16,58,3.8,1.8),1.9,0.7),
 (crescent( 1.4,23,48,3.4,2.4),1.85,0.85),
 (crescent( 0.2,19,55,3.6,2.0),1.9,1.0),
 # two that curve the other way, sweeping down-left behind the bunch; the right-leaning beans cross over them
 (crescent(-2.0,-9,50,-3.4,1.6,True),1.75,0.1),
 (crescent(3.6,-7,57,-3.2,1.4,True),1.8,0.32)]

def slices(P,W,stalk=0.1,n=40):
    """the pod cut across into n slices (polygons) with each slice's position t along the pod, for fading focus"""
    poly,c=outline(P,W,stalk); m=len(c)
    L=poly[:m]; R=poly[m+24:][::-1]
    out=[]
    for i in range(n):
        a=int(i*(m-1)/n); b=int((i+1)*(m-1)/n)+1
        quad=np.vstack([L[a:b+1],R[a:b+1][::-1]]); out.append((quad,(i+0.5)/n))
    out.append((poly[m-1:m+25],1.0))      # the round end
    return out
