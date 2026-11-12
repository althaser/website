import math
import random
import sys

from common import DEFS, H, base_css, nebula, palette, save, stars, svg_open

random.seed(11)
T = 6.0
L = 12
X0, X1 = 165, 1015
XS = [X0 + (X1 - X0) * i / (L - 1) for i in range(L)]
NS = [round(7 + 15 * math.sin(math.pi * i / (L - 1)) ** .8) for i in range(L)]
NS[-1] = 5
GAP = 24
ORANGE, AMBER = "#fb923c", "#fbbf24"
WIN = 2
DIGIT = ["#####", "....#", "...#.", "..#..", ".#...", ".#...", ".#..."]



def ys(n):
    top = H / 2 - (n - 1) * GAP / 2
    return [top + j * GAP for j in range(n)]


def fwd(i):
    return 4 + i * 40 / (L - 1)


def bwd(i):
    return 58 + (L - 1 - i) * 34 / (L - 1)


css = [
    "@keyframes fl{0%{transform:translateX(0);opacity:0}20%,80%{opacity:1}100%{transform:translateX(40px);opacity:0}}",
    "@keyframes px{0%,2%{opacity:.35}5%,40%{opacity:1}50%,100%{opacity:.35}}",
    "@keyframes ls{0%,47%{opacity:0}51%{opacity:1}55%{opacity:.6}58%{opacity:1}64%,100%{opacity:0}}",
    "@keyframes ok{0%,50%{opacity:0}54%,92%{opacity:1}96%,100%{opacity:0}}",
    ".bar{transform-box:fill-box;transform-origin:0 50%}",
    ".f{fill:#fff;stroke-width:3;stroke-opacity:.5}.b{fill:#fbbf24;stroke:#fb923c;stroke-width:3;stroke-opacity:.5}",
] + base_css()
for i in range(L):
    f, b = fwd(i), bwd(i)
    css.append(f"@keyframes nf{i}{{0%,{f - 1:.1f}%{{opacity:.3}}{f + 1:.1f}%{{opacity:1}}{f + 14:.1f}%,100%{{opacity:.3}}}}")
    css.append(f"@keyframes nb{i}{{0%,{b - 1:.1f}%{{opacity:0}}{b + 1:.1f}%{{opacity:1}}{b + 8:.1f}%,100%{{opacity:0}}}}")
for i in range(L - 1):
    a, b = fwd(i), fwd(i + 1)
    css.append(f"@keyframes pf{i}{{0%,{a:.1f}%{{transform:translate(0,0);opacity:0}}{a + .5:.1f}%{{opacity:1}}{b - .5:.1f}%{{opacity:1}}{b:.1f}%,100%{{transform:translate(var(--x),var(--y));opacity:0}}}}")
    a, b = bwd(i + 1), bwd(i)
    css.append(f"@keyframes pb{i}{{0%,{a:.1f}%{{transform:translate(0,0);opacity:0}}{a + .5:.1f}%{{opacity:1}}{b - .5:.1f}%{{opacity:1}}{b:.1f}%,100%{{transform:translate(var(--x),var(--y));opacity:0}}}}")
    css.append(f"@keyframes eb{i}{{0%,{a:.1f}%{{opacity:0}}{a + 2:.1f}%{{opacity:1}}{b + 6:.1f}%,100%{{opacity:0}}}}")
    css.append(f".f{i}{{stroke:{palette((i + .5) / (L - 1))};animation:pf{i} {T}s linear infinite}}.b{i}{{animation:pb{i} {T}s linear infinite}}")

o = [svg_open("Animated neural network training"), "<defs>", *DEFS,
     '<radialGradient id="ho"><stop offset="0" stop-color="#fb923c" stop-opacity=".55"/><stop offset="1" stop-color="#fb923c" stop-opacity="0"/></radialGradient>']
for i in range(L - 1):
    o.append(f'<linearGradient id="g{i}" gradientUnits="userSpaceOnUse" x1="{XS[i]:.0f}" x2="{XS[i + 1]:.0f}" y1="0" y2="0"><stop offset="0" stop-color="{palette(i / (L - 1))}"/><stop offset="1" stop-color="{palette((i + 1) / (L - 1))}"/></linearGradient>')
o.append("</defs>")
STYLE_AT = len(o)

o.append(nebula((440, 350), (770, 350), (330, 340), 260))
o.extend(stars(90))

# input image: a hand-written 7
PS = 10
gx, gy = 48, H / 2 - len(DIGIT) * PS / 2
o.append(f'<rect x="{gx - 8}" y="{gy - 8:.0f}" width="{5 * PS + 16}" height="{len(DIGIT) * PS + 16}" rx="8" fill="#0b1023" fill-opacity=".7" stroke="#22d3ee" stroke-opacity=".4"/>')
on, off = [], []
for r, line in enumerate(DIGIT):
    for c, ch in enumerate(line):
        (on if ch == "#" else off).append(f"M{gx + c * PS + 1} {gy + r * PS + 1:.0f}h{PS - 2}v{PS - 2}h-{PS - 2}z")
o.append(f'<path d="{"".join(off)}" fill="#22d3ee" fill-opacity=".08"/>')
o.append(f'<path d="{"".join(on)}" fill="#67e8f9" style="animation:px {T}s infinite"/>')
for y in ys(NS[0]):
    for k in range(2):
        o.append(f'<rect class="mv" x="{gx + 5 * PS + 14}" y="{y - 2:.0f}" width="7" height="4" rx="1" fill="#67e8f9" style="animation:fl 1.6s linear {-k * .8 - random.uniform(0, .4):.2f}s infinite"/>')

# connections (static, merged by weight) and backprop flashes (merged per transition)
edges = []
for i in range(L - 1):
    A, B = ys(NS[i]), ys(NS[i + 1])
    buckets = {0: [], 1: [], 2: []}
    for y1 in A:
        for b in sorted(range(len(B)), key=lambda b: abs(B[b] - y1) + random.uniform(0, 140))[:5]:
            wgt = random.random() ** 2
            bk = 0 if wgt < .25 else (1 if wgt < .6 else 2)
            buckets[bk].append(f"M{XS[i]:.0f} {y1:.0f}L{XS[i + 1]:.0f} {B[b]:.0f}")
            edges.append((i, y1, B[b], wgt))
    for bk, (sw, so) in zip((0, 1, 2), ((.5, .1), (1, .22), (1.7, .38))):
        if buckets[bk]:
            o.append(f'<path d="{"".join(buckets[bk])}" stroke="url(#g{i})" stroke-width="{sw}" stroke-opacity="{so}" fill="none"/>')
    grad = [f"M{XS[i]:.0f} {y1:.0f}L{XS[i + 1]:.0f} {y2:.0f}" for (j, y1, y2, wgt) in edges if j == i and wgt > .3]
    o.append(f'<path d="{"".join(grad)}" stroke="{AMBER}" stroke-width="1.4" stroke-opacity=".55" fill="none" opacity="0" style="animation:eb{i} {T}s infinite"/>')

# forward (white) and backward (orange) pulses
for (i, y1, y2, wgt) in edges:
    dx, dy = XS[i + 1] - XS[i], y2 - y1
    if random.random() < .2 + .5 * wgt:
        o.append(f'<circle class="mv f f{i}" cx="{XS[i]:.0f}" cy="{y1:.0f}" r="2.4" style="--x:{dx:.0f}px;--y:{dy:.0f}px"/>')
    if random.random() < .1 + .4 * wgt:
        o.append(f'<circle class="mv b b{i}" cx="{XS[i + 1]:.0f}" cy="{y2:.0f}" r="2.2" style="--x:{-dx:.0f}px;--y:{-dy:.0f}px"/>')

# neurons: forward glow plus an orange ring when the gradient passes
for i in range(L):
    c = palette(i / (L - 1))
    rings, cores, outs = [], [], []
    for y in ys(NS[i]):
        a = random.uniform(.35, 1)
        o.append(f'<circle cx="{XS[i]:.0f}" cy="{y:.0f}" r="5.5" fill="#0b1023" stroke="{c}" stroke-opacity=".6" stroke-width="1.2"/>')
        cores.append(f'<circle cx="{XS[i]:.0f}" cy="{y:.0f}" r="15" fill="url(#hl)" opacity="{a:.2f}"/><circle cx="{XS[i]:.0f}" cy="{y:.0f}" r="{3 + 2.5 * a:.1f}" fill="{c}"/>')
        rings.append(f'<circle cx="{XS[i]:.0f}" cy="{y:.0f}" r="8.5" fill="none" stroke="{ORANGE}" stroke-width="1.6"/>')
    o.append(f'<g opacity=".3" style="animation:nf{i} {T}s infinite">{"".join(cores)}</g>')
    o.append(f'<g opacity="0" style="animation:nb{i} {T}s infinite">{"".join(rings)}</g>')

# output probabilities with the correct class marked
bx = X1 + 26
probs = [.12, .08, 1.0, .18, .06]
for j, y in enumerate(ys(NS[-1])):
    p = probs[j]
    css.append(f"@keyframes pr{j}{{0%,{fwd(L - 1):.1f}%{{transform:scaleX(.04);opacity:.4}}{fwd(L - 1) + 6:.1f}%,92%{{transform:scaleX({p});opacity:1}}97%,100%{{transform:scaleX(.04);opacity:.4}}}}")
    fill = ORANGE if j == WIN else "#a78bfa"
    o.append(f'<rect x="{bx}" y="{y - 5:.0f}" width="90" height="10" rx="3" fill="#a78bfa" fill-opacity=".1"/>')
    o.append(f'<rect class="bar" x="{bx}" y="{y - 5:.0f}" width="90" height="10" rx="3" fill="{fill}" style="animation:pr{j} {T}s ease-out infinite"/>')
wy = ys(NS[-1])[WIN]
o.append(f'<path d="M{bx + 100} {wy:.0f}l5 5 9-11" fill="none" stroke="#4ade80" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" opacity="0" style="animation:ok {T}s infinite"/>')
o.append(f'<circle cx="{X1:.0f}" cy="{H / 2:.0f}" r="70" fill="url(#ho)" opacity="0" style="animation:ls {T}s infinite"/>')

o.insert(STYLE_AT, "<style>" + "".join(css) + "</style>")
o.append("</svg>")
save(sys.argv[1], o)
