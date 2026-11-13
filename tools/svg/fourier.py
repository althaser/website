import cmath
import math
import random
import sys

from common import DEFS, PALETTE, STAR, base_css, nebula, palette, save, stars, svg_open

random.seed(5)
FONT = 'font-family="Cambria Math,Georgia,Times New Roman,serif"'
MONO = 'font-family="Consolas,monospace"'
P = 14.0
KMAX = 20
EX, EY, SCALE = 360, 380, 1.9
SPX0, SPX1, SPY0, SPY1 = 760, 1130, 330, 140
THUMBS, TY, TS = (2, 5, 10, 2 * KMAX + 1), 515, .2

# a stylised pi, traced clockwise
SHAPE = [(-105, -80), (105, -80), (105, -56), (56, -56), (56, 60), (62, 82), (78, 84), (74, 100), (48, 100), (32, 84), (32, -56),
         (-34, -56), (-40, 30), (-52, 80), (-66, 100), (-88, 96), (-74, 74), (-62, 30), (-58, -56), (-105, -56)]


def num(v):
    return f"{v:.1f}".removesuffix(".0")


def poly(points, close=False):
    return "M" + " ".join(f"{num(p.real)} {num(p.imag)}" for p in points) + ("Z" if close else "")


def sample(shape, m):
    """Points spread evenly along the closed polygon."""
    pts = [complex(*p) * SCALE for p in shape]
    edges = list(zip(pts, pts[1:] + pts[:1]))
    total = sum(abs(b - a) for a, b in edges)
    out, acc, e = [], 0.0, 0
    for j in range(m):
        s = total * j / m
        while acc + abs(edges[e][1] - edges[e][0]) < s:
            acc += abs(edges[e][1] - edges[e][0])
            e += 1
        a, b = edges[e]
        out.append(a + (b - a) * (s - acc) / abs(b - a))
    return out


M = 1024
z = sample(SHAPE, M)
coef = {k: sum(z[j] * cmath.exp(-2j * math.pi * k * j / M) for j in range(M)) / M for k in range(-KMAX, KMAX + 1)}
order = sorted((k for k in coef if k), key=lambda k: -abs(coef[k]))


def series(t, terms):
    keep = [0] + order[:terms - 1]
    return sum(coef[k] * cmath.exp(2j * math.pi * k * t) for k in keep)


def color(k):
    return palette(abs(k) / KMAX)


css = [
    "@keyframes sp{to{transform:rotate(360deg)}}",
    "@keyframes tr{0%{opacity:1}100%{opacity:.1}}",
    ".c{fill:none;stroke-linecap:round;stroke-linejoin:round}",
    "@media (max-width:520px){.ti{font-size:30px}.su{font-size:20px}.ax{font-size:22px}}",
] + base_css()
defs = ["<defs>", *DEFS, "</defs>"]
o = [nebula((360, 380), (900, 340), (380, 360), 280)]
o.extend(stars(90))

# target shape, faint
o.append(f'<path class="c" transform="translate({EX} {EY})" d="{poly(z[::8], True)}" stroke="{STAR}" stroke-opacity=".12" stroke-width="10"/>')

# the tip's trail: every segment lights up as the tip passes and fades over one period
STEPS = 480
tip = [series(i / STEPS, 2 * KMAX + 1) + complex(EX, EY) for i in range(STEPS + 1)]
for i in range(0, STEPS, 2):
    c = palette(i / STEPS)
    o.append(f'<path class="c" d="{poly(tip[i:i + 3])}" stroke="{c}" stroke-width="2.6" stroke-linecap="butt" style="animation:tr {P}s linear {i / STEPS * P - P:.2f}s infinite"/>')

# epicycles: nested frames, each turning relative to its parent so the absolute speed is k turns per period
c0 = coef[0]
chain = f'<g transform="translate({num(EX + c0.real)} {num(EY + c0.imag)})">'
close = "</g>"
prev_k, prev_arg = 0, 0.0
for k in order:
    r, arg = abs(coef[k]), cmath.phase(coef[k])
    dk = k - prev_k
    spin = f"animation:sp {P / abs(dk):.3f}s linear infinite" + (";animation-direction:reverse" if dk < 0 else "")
    chain += (f'<g transform="rotate({math.degrees(arg - prev_arg):.2f})"><g style="{spin}">'
              f'<circle r="{num(r)}" fill="none" stroke="{color(k)}" stroke-opacity=".35"/>'
              f'<line x2="{num(r)}" stroke="{color(k)}" stroke-opacity=".8" stroke-width="1.2"/><g transform="translate({num(r)} 0)">')
    close += "</g></g></g>"
    prev_k, prev_arg = k, arg
chain += '<circle r="12" fill="url(#hl)"/><circle r="3.5" fill="#fff"/>' + close
o.append(chain)
o.append(f'<text x="{EX}" y="66" text-anchor="middle" class="ti" {FONT} font-size="19" fill="#ede9fe">f(t) = Σ c<tspan class="su" font-size="13" dy="5">k</tspan>'
         f'<tspan dy="-5"> e</tspan><tspan class="su" font-size="13" dy="-8">2πikt</tspan></text>')

# spectrum: |c_k| for every frequency, coloured like its circle
o.append(f'<text x="{(SPX0 + SPX1) / 2}" y="66" text-anchor="middle" class="ti" {FONT} font-size="19" fill="#ede9fe">|c<tspan class="su" font-size="13" dy="5">k</tspan><tspan dy="-5">|  spectrum</tspan></text>')
o.append(f'<line x1="{SPX0 - 10}" y1="{SPY0}" x2="{SPX1 + 10}" y2="{SPY0}" stroke="{STAR}" stroke-opacity=".35"/>')
peak = max(abs(coef[k]) for k in order)
bw = (SPX1 - SPX0) / (2 * KMAX + 1)
for k in range(-KMAX, KMAX + 1):
    if not k:
        continue
    h = (SPY0 - SPY1) * (abs(coef[k]) / peak) ** .6
    x = SPX0 + (k + KMAX) * bw
    o.append(f'<rect x="{num(x + 1)}" y="{num(SPY0 - h)}" width="{num(bw - 2)}" height="{num(h)}" rx="1.5" fill="{color(k)}" fill-opacity=".85"/>')
for k in (-KMAX, -10, 0, 10, KMAX):
    o.append(f'<text x="{num(SPX0 + (k + KMAX + .5) * bw)}" y="{SPY0 + 20}" text-anchor="middle" class="ax" {MONO} font-size="12" fill="{STAR}" fill-opacity=".55">{k}</text>')

# reconstructions with only the strongest few terms
o.append(f'<text x="{(SPX0 + SPX1) / 2}" y="{TY - 70}" text-anchor="middle" class="ti" {FONT} font-size="19" fill="#ede9fe">number of terms</text>')
gap = (SPX1 - SPX0) / len(THUMBS)
for n, terms in enumerate(THUMBS):
    cx = SPX0 + gap * (n + .5)
    shape = [series(i / 240, terms) * TS + complex(cx, TY) for i in range(241)]
    c = palette(n / (len(THUMBS) - 1))
    o.append(f'<path class="c" d="{poly(shape)}" stroke="{c}" stroke-width="1.6"/>')
    body = "".join(f"{100 * i / 60:.2f}%{{transform:translate({num(shape[i * 4].real)}px,{num(shape[i * 4].imag)}px)}}" for i in range(61))
    css.append(f"@keyframes m{n}{{{body}}}")
    o.append(f'<g class="mv" style="animation:m{n} {P}s linear infinite"><circle r="7" fill="url(#hl)"/><circle r="2.2" fill="#fff"/></g>')
    o.append(f'<text x="{num(cx)}" y="{TY + 55}" text-anchor="middle" class="ax" {MONO} font-size="12" fill="{c}">{terms}</text>')

save(sys.argv[1], [svg_open("Animated Fourier series drawing with epicycles"), *defs, "<style>" + "".join(css) + "</style>", *o, "</svg>"])
