import math
import random
import sys

from common import DEFS, FONT, PALETTE, STAR, back, base_css, mobile, nebula, num, poly, stars, sub, title, write_svg

random.seed(7)
CYAN, ORANGE = PALETTE[0], PALETTE[-1]

# curved sheet: z = -A / sqrt(1 + (r/C)^2), seen from a camera raised by ELEV
CX, CY = 790, 300
L, STEP = 300, 30
A, C = 190, 46
ELEV = math.radians(30)
D = F = 1500
P = 9.0
R0 = 175
PHOTON, PH_GAP = 4.5, 2.5

# worldline panel
HX, HY = 225, 390
HR, SQ = 46, .34
PITCH = 320


def well(r):
    return -A / math.sqrt(1 + (r / C) ** 2)


def proj(x, y, z=None):
    if z is None:
        z = well(math.hypot(x, y))
    up = z * math.cos(ELEV) + y * math.sin(ELEV)
    fwd = y * math.cos(ELEV) - z * math.sin(ELEV)
    k = F / (D + fwd)
    return CX + x * k, CY - up * k, k


def frames(points, period, name, extra=""):
    n = len(points) - 1
    body = "".join(f"{100 * i / n:.2f}%{{transform:translate({num(x)}px,{num(y)}px)}}" for i, (x, y) in enumerate(points))
    return f"@keyframes {name}{{{body}}}" + extra


css = [
    "@keyframes tr{0%{opacity:1}24%,100%{opacity:0}}",
    "@keyframes gl{0%,100%{transform:scale(1);opacity:.9}50%{transform:scale(1.12);opacity:1}}",
    f"@keyframes hs{{to{{transform:translateY({PITCH}px)}}}}",
    ".c{fill:none;stroke-linecap:round;stroke-linejoin:round}",
    ".gl{transform-box:fill-box;transform-origin:center}",
    mobile(".ax{font-size:26px}"),
] + base_css()

defs = ["<defs>", *DEFS,
        f'<radialGradient id="gg" gradientUnits="userSpaceOnUse" cx="{CX}" cy="{proj(0, 0)[1]:.0f}" r="430">'
        f'<stop offset="0" stop-color="#e879f9" stop-opacity=".95"/><stop offset=".35" stop-color="#8b5cf6" stop-opacity=".6"/>'
        f'<stop offset=".7" stop-color="#22d3ee" stop-opacity=".28"/><stop offset="1" stop-color="#22d3ee" stop-opacity="0"/></radialGradient>',
        '<radialGradient id="sg"><stop offset="0" stop-color="#fff"/><stop offset=".25" stop-color="#fde68a"/><stop offset=".55" stop-color="#fb923c" stop-opacity=".55"/><stop offset="1" stop-color="#fb923c" stop-opacity="0"/></radialGradient>',
        '<radialGradient id="pg" cx=".35" cy=".35"><stop offset="0" stop-color="#a5f3fc"/><stop offset=".6" stop-color="#22d3ee"/><stop offset="1" stop-color="#0e7490"/></radialGradient>',
        f'<clipPath id="past"><rect x="0" y="{HY}" width="440" height="{HY + 260 - HY}"/></clipPath>',
        f'<clipPath id="futr"><rect x="0" y="110" width="440" height="{HY - 110}"/></clipPath>',
        '<radialGradient id="gf"><stop offset=".42" stop-color="#fff"/><stop offset=".9" stop-color="#000"/></radialGradient>',
        '<linearGradient id="vf" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#000"/><stop offset=".2" stop-color="#fff"/><stop offset=".8" stop-color="#fff"/><stop offset="1" stop-color="#000"/></linearGradient>',
        f'<mask id="gm" maskUnits="userSpaceOnUse" x="0" y="0" width="1200" height="700"><rect x="{CX - 420}" y="140" width="840" height="420" fill="url(#gf)"/></mask>',
        f'<mask id="cm" maskUnits="userSpaceOnUse" x="0" y="0" width="1200" height="700"><rect x="0" y="110" width="440" height="{HY + 250 - 110}" fill="url(#vf)"/></mask>',
        "</defs>"]

o = [nebula((350, 360), (820, 340), (340, 370), 290)]
o.extend(stars(90))

# the curved spacetime sheet
SUB = 6
grid = []
for g in range(-L, L + 1, STEP):
    for line in ([(g, -L + i * STEP / SUB) for i in range(2 * L * SUB // STEP + 1)],
                 [(-L + i * STEP / SUB, g) for i in range(2 * L * SUB // STEP + 1)]):
        grid.append(f'<path d="{poly(proj(x, y)[:2] for x, y in line)}"/>')
o.append(f'<g class="c" mask="url(#gm)" stroke="url(#gg)" stroke-width="1.1">{"".join(grid)}</g>')

# orbit of the planet on the sheet, split so the star hides the far half
orbit = [proj(R0 * math.cos(a), R0 * math.sin(a))[:2] for a in (2 * math.pi * i / 240 for i in range(241))]
o.append(f'<path class="c" d="{poly(orbit[:121])}" stroke="{CYAN}" stroke-opacity=".5" stroke-dasharray="4 6"/>')

# light ray deflected by the mass, with the undeflected direction dashed
x, y, vx, vy = -L - 40.0, -95.0, 1.0, 0.0
ray = [(x, y)]
while -L - 40 <= x <= L + 60 and abs(y) <= L + 60:
    r2 = x * x + y * y
    acc = 6000 / (r2 + 900)
    vx -= acc * x / math.sqrt(r2) * .02
    vy -= acc * y / math.sqrt(r2) * .02
    s = math.hypot(vx, vy)
    vx, vy = vx / s, vy / s
    x, y = x + vx * 4, y + vy * 4
    ray.append((x, y))
ray = [p for p in ray if abs(p[0]) <= L and abs(p[1]) <= L]
rp = [proj(px, py)[:2] for px, py in ray]
straight = [proj(px, -95)[:2] for px in range(-L, L + 1, 5)]
o.append(f'<path class="c" d="{poly(straight)}" stroke="{STAR}" stroke-opacity=".35" stroke-dasharray="3 7" mask="url(#gm)"/>')
o.append(f'<path class="c" d="{poly(rp)}" stroke="#fde68a" stroke-opacity=".25" stroke-width="1.2" mask="url(#gm)"/>')
TOTAL = PHOTON + PH_GAP
seg = 4
for k in range(seg, len(rp), seg):
    dl = (k - seg) / (len(rp) - 1) * PHOTON - TOTAL
    o.append(f'<path class="c mv" d="{poly(rp[k - seg:k + 1])}" stroke="#fde68a" stroke-width="2.6" style="animation:tr {TOTAL}s linear {dl:.2f}s infinite"/>')
idx = [round(i * (len(rp) - 1) / 60) for i in range(61)]
scan = PHOTON / TOTAL * 100
body = "".join(f"{scan * i / 60:.2f}%{{transform:translate({num(rp[j][0])}px,{num(rp[j][1])}px)}}" for i, j in enumerate(idx))
css.append(f"@keyframes ph{{{body}100%{{transform:translate({num(rp[-1][0])}px,{num(rp[-1][1])}px)}}}}")
css.append(f"@keyframes po{{0%,{scan:.1f}%{{opacity:1}}{scan + 2:.1f}%,100%{{opacity:0}}}}")
o.append(f'<g class="mv" style="animation:po {TOTAL}s linear infinite"><g style="animation:ph {TOTAL}s linear infinite"><circle r="14" fill="url(#hl)"/><circle r="3.2" fill="#fff"/></g></g>')

# the star at the bottom of the well
sx, sy, _ = proj(0, 0)
o.append(f'<circle class="gl" cx="{num(sx)}" cy="{num(sy)}" r="62" fill="url(#sg)" style="animation:gl 4s ease-in-out infinite"/>')
o.append(f'<circle cx="{num(sx)}" cy="{num(sy)}" r="15" fill="#fff7ed"/>')
o.append(f'<path class="c" d="{poly(orbit[120:])}" stroke="{CYAN}" stroke-opacity=".5" stroke-dasharray="4 6"/>')

# planet: position and perspective size along the orbit
pts = []
for i in range(121):
    a = 2 * math.pi * i / 120
    px, py, k = proj(R0 * math.cos(a), R0 * math.sin(a))
    pts.append((px, py, k))
body = "".join(f"{100 * i / 120:.2f}%{{transform:translate({num(px)}px,{num(py)}px) scale({k:.3f})}}" for i, (px, py, k) in enumerate(pts))
css.append(f"@keyframes pl{{{body}}}")
o.append(f'<g transform="translate({num(pts[0][0])} {num(pts[0][1])}) scale({pts[0][2]:.3f})" style="animation:pl {P}s linear infinite"><circle r="22" fill="url(#hl)"/><circle r="9" fill="url(#pg)"/></g>')
o.append(title(CX, 66, f'G{sub("μν")}{back(" = 8πG T")}{sub("μν")}'))

# worldline: the same orbit drawn in (x, y, t) is a helix inside the light cone
def hp(phase, t):
    return HX + HR * math.cos(phase), HY - t + HR * SQ * -math.sin(phase)


o.append(title(HX, 66, "worldline"))
turns = range(-6, 6)
back = "".join(poly(hp(math.pi * (2 * n + i / 30), PITCH * (2 * n + i / 30) / 2) for i in range(31)) for n in turns)
front = "".join(poly(hp(math.pi * (2 * n + 1 + i / 30), PITCH * (2 * n + 1 + i / 30) / 2) for i in range(31)) for n in turns)


def helix(d, weight, opacity):
    return (f'<g clip-path="url(#futr)" mask="url(#cm)"><g style="animation:hs {P}s linear infinite"><path class="c" d="{d}" stroke="{CYAN}" stroke-opacity="{.35 * opacity:.2f}" stroke-width="{1.6 * weight:.1f}" stroke-dasharray="4 6"/></g></g>'
            f'<g clip-path="url(#past)" mask="url(#cm)"><g style="animation:hs {P}s linear infinite"><path class="c" d="{d}" stroke="url(#wl)" stroke-opacity="{opacity}" stroke-width="{2.4 * weight:.1f}"/></g></g>')


o.append(helix(back, .75, .6))
o.append(f'<rect x="{HX - HR}" y="110" width="{2 * HR}" height="{HY + 250 - 110}" fill="url(#cy)" mask="url(#cm)"/>')
o.append(f'<line x1="{HX}" y1="{HY + 250}" x2="{HX}" y2="110" stroke="{STAR}" stroke-opacity=".35"/>'
         f'<text x="{HX + 10}" y="120" class="ax" {FONT} font-style="italic" font-size="17" fill="{STAR}" fill-opacity=".8">t</text>')
o.append(f'<ellipse cx="{HX}" cy="{HY}" rx="{HR + 70}" ry="{(HR + 70) * SQ:.1f}" fill="#8b5cf6" fill-opacity=".1" stroke="#a78bfa" stroke-opacity=".5" stroke-dasharray="3 5"/>')
o.append(f'<text x="{HX - HR - 118}" y="{HY + 5}" class="ax" {FONT} font-style="italic" font-size="15" fill="#c4b5fd" fill-opacity=".85">now</text>')
o.append(helix(front, 1, 1))
defs.insert(-1, f'<linearGradient id="wl" gradientUnits="userSpaceOnUse" x1="0" x2="0" y1="{HY}" y2="{HY + 300}">'
            f'<stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="#8b5cf6" stop-opacity=".1"/></linearGradient>')
defs.insert(-1, f'<linearGradient id="cy"><stop offset="0" stop-color="{CYAN}" stop-opacity=".09"/><stop offset=".5" stop-color="{CYAN}" stop-opacity="0"/>'
            f'<stop offset="1" stop-color="{CYAN}" stop-opacity=".09"/></linearGradient>')

# light cone carried by the planet's present event
H = 112
cone = (f'<path class="c" d="M{-H} {-H}L0 0L{H} {-H}M{-H} {H}L0 0L{H} {H}" stroke="#fde68a" stroke-opacity=".45" stroke-width="1.2"/>'
        f'<ellipse cy="{-H}" rx="{H}" ry="{H * SQ:.1f}" fill="#fde68a" fill-opacity=".05" stroke="#fde68a" stroke-opacity=".4"/>'
        f'<ellipse cy="{H}" rx="{H}" ry="{H * SQ:.1f}" fill="none" stroke="#fde68a" stroke-opacity=".25" stroke-dasharray="3 5"/>')
now = [hp(2 * math.pi * i / 120, 0) for i in range(121)]
css.append(frames(now, P, "wn"))
labels = (f'<text x="{H + 10}" y="{-H + 5}" class="ax" {FONT} font-style="italic" font-size="15" fill="#fde68a" fill-opacity=".8">future</text>'
          f'<text x="{H + 10}" y="{H + 5}" class="ax" {FONT} font-style="italic" font-size="15" fill="#fde68a" fill-opacity=".6">past</text>')
o.append(f'<g transform="translate({num(now[0][0])} {num(now[0][1])})" style="animation:wn {P}s linear infinite">{cone}{labels}<circle r="16" fill="url(#hl)"/><circle r="5" fill="#a5f3fc"/></g>')

write_svg(sys.argv[1], "Animated curved spacetime", defs, css, o)
