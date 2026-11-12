import math
import random
import sys
random.seed(9)
W,H=1200,700; P=4.0
pal=['#22d3ee','#60a5fa','#6366f1','#8b5cf6','#a855f7','#d946ef','#f472b6','#fb923c']
def pc(t): return f'{100*max(0,min(P,t))/P:.2f}%'
css=[
'@keyframes tw{0%,100%{opacity:.15}50%{opacity:.9}}',
'@keyframes sp{to{transform:rotate(360deg)}}',
'@keyframes wk{0%,100%{opacity:1}50%{opacity:.3}}',
'@keyframes gs{0%{transform:translate(0,0);opacity:0}5%{opacity:1}45%{transform:translate(var(--x),var(--y));opacity:1}50%,100%{transform:translate(var(--x),var(--y));opacity:0}}',
'@media (prefers-reduced-motion:reduce){*{animation:none!important}}']
o=[]
def kf(name,frames): css.append(f'@keyframes {name}{{{frames}}}')
# ---------- background
o.append('<ellipse cx="420" cy="260" rx="380" ry="230" fill="url(#nb1)"/><ellipse cx="800" cy="470" rx="380" ry="240" fill="url(#nb2)"/>')
for k in range(90):
    x,y=random.uniform(0,W),random.uniform(0,H)
    a=f' style="animation:tw {random.uniform(3,7):.1f}s {-random.uniform(0,7):.1f}s infinite"' if k<22 else f' opacity="{random.uniform(.15,.55):.2f}"'
    o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.choice([.7,1,1.3])}" fill="#e0e7ff"{a}/>')
# ---------- P2P mesh
nodes=[]
while len(nodes)<26:
    x,y=random.uniform(70,1130),random.uniform(45,265)
    if abs(x-600)<130 and y>215: continue
    if all(math.hypot(x-a,y-b)>88 for a,b in nodes): nodes.append((x,y))
edges=set()
for i,(x,y) in enumerate(nodes):
    near=sorted(range(len(nodes)),key=lambda j:math.hypot(nodes[j][0]-x,nodes[j][1]-y))[1:4]
    for j in near: edges.add(tuple(sorted((i,j))))
def ncol(x): 
    t=(x-100)/1000; return pal[min(3,int(t*4))]
# panel geometry
PX,PY,PW,PH=600,410,190,150
leaves=[(PX-70+k*20,PY+55) for k in range(8)]
lv2=[(PX-60+k*40,PY+20) for k in range(4)]
lv3=[(PX-40+k*80,PY-15) for k in range(2)]
root=(PX,PY-48)
T_LEAF=[0.5+k*0.22 for k in range(8)]; T2=2.35; T3=2.5; TR=2.65; TOFF=3.1
# validation lines (under mesh)
kf('val',f'0%,{pc(TR)}{{opacity:0}}{pc(TR+.1)}{{opacity:.9}}{pc(TOFF)}{{opacity:.5}}{pc(TOFF+.2)},100%{{opacity:0}}')
for (x,y) in nodes:
    o.append(f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{PX}" y2="{PY-PH/2}" stroke="#34d399" stroke-width="1" stroke-dasharray="3 5" style="animation:val {P}s infinite"/>')
for i,j in edges:
    (x1,y1),(x2,y2)=nodes[i],nodes[j]
    o.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="#6366f1" stroke-opacity=".35" stroke-width="1"/>')
# gossip packets
for i,j in edges:
    for (a,b) in ((i,j),(j,i)):
        if random.random()<.7:
            (x1,y1),(x2,y2)=nodes[a],nodes[b]; per=random.choice([2,3,4])
            o.append(f'<rect x="{x1-3:.0f}" y="{y1-3:.0f}" width="6" height="6" rx="1.5" fill="#67e8f9" style="--x:{x2-x1:.0f}px;--y:{y2-y1:.0f}px;animation:gs {per}s linear {-random.uniform(0,per):.2f}s infinite"/>')
# tx packets to leaves
for k,(lx,ly) in enumerate(leaves):
    sx,sy=nodes[sorted(range(len(nodes)),key=lambda j:abs(nodes[j][0]-lx)+random.uniform(0,300))[0]]
    t1=T_LEAF[k]; t0=t1-0.7
    kf(f'tx{k}',f'0%,{pc(t0)}{{transform:translate(0,0);opacity:0}}{pc(t0+.05)}{{opacity:1}}{pc(t1)}{{transform:translate({lx-sx:.0f}px,{ly-sy:.0f}px);opacity:1}}{pc(t1+.05)},100%{{transform:translate({lx-sx:.0f}px,{ly-sy:.0f}px);opacity:0}}')
    o.append(f'<g style="animation:tx{k} {P}s infinite cubic-bezier(.4,0,.6,1)"><circle cx="{sx:.0f}" cy="{sy:.0f}" r="9" fill="url(#hl)"/><rect x="{sx-4:.0f}" y="{sy-4:.0f}" width="8" height="8" rx="2" fill="#fde68a"/></g>')
for (x,y) in nodes:
    c=ncol(x)
    o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="20" fill="url(#hl)" opacity=".5"/>')
    o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="9" fill="#0b1023" stroke="{c}" stroke-width="2"/>')
    o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="3.5" fill="{c}" style="animation:wk {random.choice([.4,.5,.6,.7])}s {-random.uniform(0,1):.2f}s infinite"/>')
    sp=random.uniform(1.2,2.6)
    o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="14" fill="none" stroke="{c}" stroke-opacity=".75" stroke-width="1.6" stroke-dasharray="9 79" style="transform-origin:{x:.0f}px {y:.0f}px;animation:sp {sp:.1f}s linear {-random.uniform(0,sp):.2f}s infinite{" reverse" if random.random()<.5 else ""}"/>')
    o.append(f'<path d="M{x-5:.0f} {y-14:.0f}l3.5 3.5 6.5-7" fill="none" stroke="#34d399" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="animation:val {P}s infinite"/>')
# ---------- mining panel
o.append(f'<circle cx="{PX}" cy="{PY}" r="122" fill="none" stroke="#a855f7" stroke-opacity=".5" stroke-width="1.5" stroke-dasharray="2 9" style="transform-origin:{PX}px {PY}px;animation:sp 6s linear infinite"/>')
o.append(f'<circle cx="{PX}" cy="{PY}" r="134" fill="none" stroke="#d946ef" stroke-opacity=".3" stroke-width="1" stroke-dasharray="14 20" style="transform-origin:{PX}px {PY}px;animation:sp 9s linear infinite reverse"/>')
kf('pf',f'0%,{pc(TR)}{{opacity:0}}{pc(TR+.08)}{{opacity:1}}{pc(TOFF+.3)},100%{{opacity:0}}')
o.append(f'<rect x="{PX-PW/2-6}" y="{PY-PH/2-6}" width="{PW+12}" height="{PH+12}" rx="18" fill="none" stroke="#34d399" stroke-width="3" style="animation:pf {P}s infinite"/>')
o.append(f'<circle cx="{PX}" cy="{PY}" r="150" fill="url(#hlg)" style="animation:pf {P}s infinite"/>')
o.append(f'<rect x="{PX-PW/2}" y="{PY-PH/2}" width="{PW}" height="{PH}" rx="14" fill="#0b1023" fill-opacity=".85" stroke="#8b5cf6" stroke-width="1.6"/>')
def lit(name,t,x,y,r,c,shape='c'):
    kf(name,f'0%,{pc(t-.02)}{{opacity:.12}}{pc(t+.06)}{{opacity:1}}{pc(TOFF)}{{opacity:.9}}{pc(TOFF+.25)},100%{{opacity:.12}}')
    if shape=='c':
        o.append(f'<g style="animation:{name} {P}s infinite"><circle cx="{x}" cy="{y}" r="{r*2.4}" fill="url(#hl)"/><circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/></g>')
    else:
        o.append(f'<g style="animation:{name} {P}s infinite"><circle cx="{x}" cy="{y}" r="{r*2.4}" fill="url(#hl)"/><rect x="{x-r}" y="{y-r}" width="{2*r}" height="{2*r}" rx="2" fill="{c}"/></g>')
def edge(a,b,t,name):
    kf(name,f'0%,{pc(t-.02)}{{opacity:.15}}{pc(t+.06)}{{opacity:.9}}{pc(TOFF)}{{opacity:.8}}{pc(TOFF+.25)},100%{{opacity:.15}}')
    o.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="#c4b5fd" stroke-width="1.3" style="animation:{name} {P}s infinite"/>')
for k,l in enumerate(leaves): edge(l,lv2[k//2],T2,f'e1{k}')
for k,l in enumerate(lv2): edge(l,lv3[k//2],T3,f'e2{k}')
for k,l in enumerate(lv3): edge(l,root,TR,f'e3{k}')
for k,(x,y) in enumerate(leaves): lit(f'l{k}',T_LEAF[k],x,y,4.5,'#fde68a','r')
for k,(x,y) in enumerate(lv2): lit(f'm{k}',T2,x,y,4.5,'#a78bfa')
for k,(x,y) in enumerate(lv3): lit(f'n{k}',T3,x,y,5,'#e879f9')
lit('rt',TR,root[0],root[1],7,'#34d399')
# hash attempts flicker (above panel)
hashes=['0x9f3a…c41e','0x07bd…e902','0x5c1f…77ab','0xe24d…0b3c','0x3a90…f15d','0x81c2…6a07']
n=len(hashes); dur=0.6
for k,hh in enumerate(hashes):
    o.append(f'<text x="{PX}" y="{PY-PH/2-14}" text-anchor="middle" font-family="Consolas,monospace" font-size="13" fill="#a78bfa" style="animation:hs {dur}s steps(1) {-k*dur/n-0.03:.3f}s infinite">{hh}</text>')
css.append(f'@keyframes hs{{0%{{opacity:1}}{100/n:.2f}%,100%{{opacity:0}}}}')
kf('hm',f'0%,{pc(TR)}{{opacity:1}}{pc(TR+.01)},{pc(TOFF+.3)}{{opacity:0}}{pc(TOFF+.31)},100%{{opacity:1}}')
kf('hf',f'0%,{pc(TR)}{{opacity:0}}{pc(TR+.01)},{pc(TOFF+.3)}{{opacity:1}}{pc(TOFF+.31)},100%{{opacity:0}}')
# wrap flicker in group that hides when found
i0=[k for k,x in enumerate(o) if 'animation:hs' in x]
grp=['<g style="animation:hm %ss infinite">'%P]+[o[k] for k in i0]+['</g>']
for k in reversed(i0): o.pop(k)
o+=grp
o.append(f'<text x="{PX}" y="{PY-PH/2-14}" text-anchor="middle" font-family="Consolas,monospace" font-size="13" fill="#34d399" style="animation:hf {P}s infinite">0x0000…a7f3 ✓</text>')
# ---------- chain
CY=615; S=130; N=9; XEND=1012
def cube(cx,cy,s=34):
    h=s*0.5
    top=f'M{cx} {cy-s}L{cx+s} {cy-s+h}L{cx} {cy-s+2*h}L{cx-s} {cy-s+h}Z'
    left=f'M{cx-s} {cy-s+h}L{cx} {cy}L{cx} {cy+s}L{cx-s} {cy+h}Z'
    right=f'M{cx+s} {cy-s+h}L{cx} {cy}L{cx} {cy+s}L{cx+s} {cy+h}Z'
    g=[f'<path d="{left}" fill="#4c1d95" stroke="#c084fc" stroke-width="1"/>',
       f'<path d="{right}" fill="#701a75" stroke="#f0abfc" stroke-width="1"/>',
       f'<path d="{top}" fill="#a855f7" fill-opacity=".85" stroke="#f5d0fe" stroke-width="1"/>']
    for k in range(3):
        g.append(f'<path d="M{cx+6} {cy+6+k*7}l{18-k*4} -{9-k*2}" stroke="#fbcfe8" stroke-opacity=".7" stroke-width="1.5" stroke-linecap="round"/>')
    g.append(f'<path d="M{cx-26} {cy-1}l6 3M{cx-26} {cy+7}l12 6M{cx-26} {cy+15}l8 4" stroke="#ddd6fe" stroke-opacity=".6" stroke-width="1.5" stroke-linecap="round"/>')
    return ''.join(g)
def link(x1,x2,y):
    return (f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="#f472b6" stroke-width="2" stroke-opacity=".7"/>'
            f'<rect x="{(x1+x2)/2-11}" y="{y-6}" width="22" height="12" rx="6" fill="none" stroke="#fb923c" stroke-width="2"/>')
kf('ch',f'0%,{pc(3.55)}{{transform:translateX(0)}}100%{{transform:translateX(-{S}px)}}')
chain=[f'<g mask="url(#chainFade)"><g style="animation:ch {P}s infinite cubic-bezier(.5,0,.3,1)">']
for k in range(N):
    cx=XEND-(N-k)*S
    chain.append(link(cx+34,cx+S-34,CY+8))
    chain.append(cube(cx,CY))
chain.append('</g>')
o+=chain
# falling new block
dx,dy=XEND-PX,CY-PY
kf('nb',f'0%,{pc(TOFF-.05)}{{transform:translate(0,0) scale(.4);opacity:0}}{pc(TOFF+.05)}{{opacity:1}}{pc(3.55)}{{transform:translate({dx}px,{dy}px) scale(1);opacity:1}}100%{{transform:translate({dx-S}px,{dy}px) scale(1);opacity:1}}')
o.append(f'<g style="transform-origin:{PX}px {PY}px;animation:nb {P}s infinite cubic-bezier(.5,0,.3,1)"><circle cx="{PX}" cy="{PY}" r="60" fill="url(#hlg)"/>{cube(PX,PY)}</g></g>')
defs=['<defs>',
'<radialGradient id="bg" r="75%"><stop offset="0" stop-color="#151a3a"/><stop offset=".65" stop-color="#0a0e22"/><stop offset="1" stop-color="#05070f"/></radialGradient>',
'<radialGradient id="nb1"><stop offset="0" stop-color="#4338ca" stop-opacity=".45"/><stop offset="1" stop-color="#4338ca" stop-opacity="0"/></radialGradient>',
'<radialGradient id="nb2"><stop offset="0" stop-color="#a21caf" stop-opacity=".4"/><stop offset="1" stop-color="#a21caf" stop-opacity="0"/></radialGradient>',
'<radialGradient id="hl"><stop offset="0" stop-color="#fff" stop-opacity=".55"/><stop offset=".4" stop-color="#fff" stop-opacity=".15"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>',
'<radialGradient id="hlg"><stop offset="0" stop-color="#34d399" stop-opacity=".35"/><stop offset="1" stop-color="#34d399" stop-opacity="0"/></radialGradient>',
'<linearGradient id="fadeX" gradientUnits="userSpaceOnUse" x1="0" x2="1200" y1="0" y2="0"><stop offset=".138" stop-color="#fff" stop-opacity="0"/><stop offset=".228" stop-color="#fff"/><stop offset=".89" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient><mask id="chainFade" maskUnits="userSpaceOnUse" x="0" y="0" width="1200" height="700"><rect width="1200" height="700" fill="url(#fadeX)"/></mask>',
'</defs>']
s='\n'.join([f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Animação do processamento de uma blockchain">']+defs+['<style>'+''.join(css)+'</style>']+o+['</svg>'])
open(sys.argv[1],'w').write(s)
