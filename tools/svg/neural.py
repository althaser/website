import math
import random
import sys
random.seed(11)
W,H=1200,700
L=12
X0,X1=130,1070
xs=[X0+(X1-X0)*i/(L-1) for i in range(L)]
pal=['#22d3ee','#60a5fa','#6366f1','#8b5cf6','#a855f7','#d946ef','#f472b6','#fb923c']
def hx(c): return tuple(int(c[i:i+2],16) for i in (1,3,5))
def col(t):
    t=max(0,min(1,t))*(len(pal)-1); i=min(int(t),len(pal)-2); f=t-i
    a,b=hx(pal[i]),hx(pal[i+1])
    return '#%02x%02x%02x'%tuple(round(a[k]+(b[k]-a[k])*f) for k in range(3))
ns=[round(7+15*math.sin(math.pi*i/(L-1))**0.8) for i in range(L)]; ns[-1]=5
gap=24
def ys(n): top=H/2-(n-1)*gap/2; return [top+j*gap for j in range(n)]
STEP=.32; BIG=12
def pc(t,P): return f'{100*t/P:.1f}%'
css=['.n,.q,.s,.d,.b{will-change:opacity,transform}']
for P in (2,4):
    css.append(f'@keyframes q{P}{{0%{{transform:translate(0,0);opacity:0}}{pc(.03,P)}{{opacity:1}}{pc(STEP,P)}{{transform:translate(var(--x),var(--y));opacity:1}}{pc(STEP+.05,P)},100%{{transform:translate(var(--x),var(--y));opacity:0}}}}')
    css.append(f'@keyframes f{P}{{0%{{opacity:1}}{pc(.45,P)}{{opacity:.35}}{pc(1.1,P)},100%{{opacity:.07}}}}')
css.append('@keyframes tw{0%,100%{opacity:.15}50%{opacity:.9}}')
css.append('@keyframes fl{0%{transform:translateX(0);opacity:0}20%,80%{opacity:1}100%{transform:translateX(90px);opacity:0}}')
css.append(f'@keyframes sw{{0%{{transform:translateX(-260px)}}100%{{transform:translateX({W+60}px)}}}}')
css.append('@media (prefers-reduced-motion:reduce){*{animation:none!important}.q{opacity:0}}')
o=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Animação de uma rede neuronal">','<defs>',
'<radialGradient id="bg" r="75%"><stop offset="0" stop-color="#151a3a"/><stop offset=".65" stop-color="#0a0e22"/><stop offset="1" stop-color="#05070f"/></radialGradient>',
'<radialGradient id="nb1"><stop offset="0" stop-color="#4338ca" stop-opacity=".45"/><stop offset="1" stop-color="#4338ca" stop-opacity="0"/></radialGradient>',
'<radialGradient id="nb2"><stop offset="0" stop-color="#a21caf" stop-opacity=".4"/><stop offset="1" stop-color="#a21caf" stop-opacity="0"/></radialGradient>',
'<radialGradient id="hl"><stop offset="0" stop-color="#fff" stop-opacity=".5"/><stop offset=".4" stop-color="#fff" stop-opacity=".15"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>',
'<linearGradient id="band" x1="0" x2="1"><stop offset="0" stop-color="#c7d2fe" stop-opacity="0"/><stop offset=".5" stop-color="#c7d2fe" stop-opacity=".06"/><stop offset="1" stop-color="#c7d2fe" stop-opacity="0"/></linearGradient>']
for i in range(L-1):
    o.append(f'<linearGradient id="g{i}" gradientUnits="userSpaceOnUse" x1="{xs[i]:.0f}" x2="{xs[i+1]:.0f}" y1="0" y2="0"><stop offset="0" stop-color="{col(i/(L-1))}"/><stop offset="1" stop-color="{col((i+1)/(L-1))}"/></linearGradient>')
o.append('</defs><style>'+''.join(css)+'</style>')
o.append('<ellipse cx="430" cy="350" rx="330" ry="260" fill="url(#nb1)"/><ellipse cx="780" cy="350" rx="340" ry="260" fill="url(#nb2)"/>')
# stars: static mostly, few twinkle
for k in range(90):
    x,y=random.uniform(0,W),random.uniform(0,H)
    anim=f' class="s" style="animation:tw {random.uniform(3,7):.1f}s {-random.uniform(0,7):.1f}s infinite"' if k<25 else f' opacity="{random.uniform(.15,.6):.2f}"'
    o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.choice([.7,1,1.3])}" fill="#e0e7ff"{anim}/>')
# connections: merged per transition & weight bucket
edges=[]
for i in range(L-1):
    A,B=ys(ns[i]),ys(ns[i+1])
    buckets={0:[],1:[],2:[]}
    for y1 in A:
        for b in sorted(range(len(B)),key=lambda b:abs(B[b]-y1)+random.uniform(0,140))[:5]:
            w=random.random()**2; bk=0 if w<.25 else (1 if w<.6 else 2)
            buckets[bk].append(f'M{xs[i]:.0f} {y1:.0f}L{xs[i+1]:.0f} {B[b]:.0f}')
            edges.append((i,y1,B[b],w))
    for bk,(sw,so) in zip((0,1,2),((.5,.1),(1,.22),(1.7,.38))):
        if buckets[bk]: o.append(f'<path d="{"".join(buckets[bk])}" stroke="url(#g{i})" stroke-width="{sw}" stroke-opacity="{so}" fill="none"/>')
o.append(f'<rect class="b" width="240" height="{H}" fill="url(#band)" style="animation:sw {(L-1)*STEP*2:.1f}s linear infinite"/>')
# pulses: moving dots (transform only)
cnt=0
for (i,y1,y2,w) in edges:
    if random.random()>.15+.55*w: continue
    cnt+=1; P=random.choice((2,2,4))
    dx,dy=xs[i+1]-xs[i],y2-y1
    c=col((i+.5)/(L-1))
    o.append(f'<circle class="q" cx="{xs[i]:.0f}" cy="{y1:.0f}" r="2.4" fill="#fff" stroke="{c}" stroke-opacity=".5" stroke-width="3" style="--x:{dx:.0f}px;--y:{dy:.0f}px;animation:q{P} {P}s linear {i*STEP-BIG:.2f}s infinite"/>')
# neurons
for i in range(L):
    c=col(i/(L-1))
    for y in ys(ns[i]):
        a=random.uniform(.35,1); P=random.choice((2,2,4))
        x=f'{xs[i]:.0f}'
        o.append(f'<circle cx="{x}" cy="{y:.0f}" r="5.5" fill="#0b1023" stroke="{c}" stroke-opacity=".6" stroke-width="1.2"/>')
        o.append(f'<g class="n" opacity="{a:.2f}" style="animation:f{P} {P}s {i*STEP-BIG:.2f}s infinite"><circle cx="{x}" cy="{y:.0f}" r="15" fill="url(#hl)"/><circle cx="{x}" cy="{y:.0f}" r="{3+2.5*a:.1f}" fill="{c}"/></g>')
# data in/out
for side,yl,x0,c in (('in',ys(ns[0]),X0-115,'#67e8f9'),('out',ys(ns[-1]),X1+22,'#fdba74')):
    for y in yl:
        for k in range(2):
            o.append(f'<rect class="d" x="{x0}" y="{y-2:.0f}" width="7" height="4" rx="1" fill="{c}" style="animation:fl 2s linear {-k-random.uniform(0,.4):.2f}s infinite"/>')
o.append('</svg>')
s='\n'.join(o)
open(sys.argv[1],'w').write(s)
