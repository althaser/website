import math
import random
import sys

from common import DEFS, STAR, base_css, hexc, mix, nebula, palette, ramp, rgb, save, stars, svg_open

random.seed(11)
T = 9.0
COLS, ROWS, CELL, GAP = 32, 18, 20, 2
GW, GH = COLS * CELL, ROWS * CELL
GX, GY = 600 - GW / 2, 330 - GH / 2
GROUPS = 12
STEPS = 5
NOISE = ["#22d3ee", "#49b6f6", "#6366f1", "#a855f7", "#e879f9", "#fb923c"]
BG = (11, 16, 35)



PCX, PCY, PR = 13.4, 9.6, 6.1
RA, RB, ROT = 10.6, 3.1, math.radians(-12)
STAR_CELLS = {(2, 2), (6, 15), (19, 1), (25, 14), (29, 16), (16, 16), (1, 9), (22, 4), (30, 11), (9, 1), (3, 13), (28, 9)}


def pixel(x, y):
    cx, cy = x + .5, y + .5
    dx, dy = cx - PCX, cy - PCY
    rx = dx * math.cos(ROT) + dy * math.sin(ROT)
    ry = -dx * math.sin(ROT) + dy * math.cos(ROT)
    e = (rx / RA) ** 2 + (ry / RB) ** 2
    ring = .5 < e < 1.0
    in_planet = dx * dx + dy * dy < PR * PR
    if ring and (ry > 0 or not in_planet):
        return mix(rgb("#fb923c"), rgb("#f472b6"), (rx + RA) / (2 * RA))
    if in_planet:
        light = 1 - ((dx * .8 + dy) / (2 * PR) + .5)
        return ramp(["#3b0764", "#6d28d9", "#6366f1", "#38bdf8", "#a5f3fc"], light)
    mdx, mdy = cx - 27.4, cy - 4.0
    if mdx * mdx + mdy * mdy < 2.9 ** 2 and (mdx + 1.2) ** 2 + (mdy + .8) ** 2 > 2.4 ** 2:
        return rgb("#fde68a")
    if (x, y) in STAR_CELLS:
        return rgb(STAR)
    return BG


img = [[pixel(x, y) for x in range(COLS)] for y in range(ROWS)]


def cell(x, y):
    return f"M{GX + x * CELL + GAP / 2:.0f} {GY + y * CELL + GAP / 2:.0f}h{CELL - GAP}v{CELL - GAP}h-{CELL - GAP}z"


o = []
w = o.append
w(svg_open("Animated diffusion model generating an image"))
w("<defs>")
o.extend(DEFS)
w('<linearGradient id="band" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c7d2fe" stop-opacity="0"/><stop offset=".5" stop-color="#c7d2fe" stop-opacity=".22"/><stop offset="1" stop-color="#c7d2fe" stop-opacity="0"/></linearGradient>')
w('<linearGradient id="trk" x1="0" x2="1"><stop offset="0" stop-color="#e879f9"/><stop offset="1" stop-color="#22d3ee"/></linearGradient>')
w('<radialGradient id="sg"><stop offset="0" stop-color="#e0e7ff" stop-opacity=".6"/><stop offset="1" stop-color="#e0e7ff" stop-opacity="0"/></radialGradient>')
w('<radialGradient id="mg"><stop offset=".56" stop-color="#fde68a" stop-opacity="0"/><stop offset=".6" stop-color="#fde68a" stop-opacity=".22"/><stop offset="1" stop-color="#fde68a" stop-opacity="0"/></radialGradient>')
w('<radialGradient id="atm"><stop offset=".68" stop-color="#38bdf8" stop-opacity=".35"/><stop offset=".78" stop-color="#6366f1" stop-opacity=".15"/><stop offset="1" stop-color="#6366f1" stop-opacity="0"/></radialGradient>')
w('<linearGradient id="pg" x1=".18" y1=".1" x2=".82" y2=".95"><stop offset="0" stop-color="#a5f3fc"/><stop offset=".3" stop-color="#38bdf8"/><stop offset=".55" stop-color="#6366f1"/><stop offset=".8" stop-color="#6d28d9"/><stop offset="1" stop-color="#3b0764"/></linearGradient>')
w('<radialGradient id="sh" cx=".3" cy=".25" r=".9"><stop offset=".55" stop-color="#05070f" stop-opacity="0"/><stop offset="1" stop-color="#05070f" stop-opacity=".55"/></radialGradient>')
w(f'<linearGradient id="rg" gradientUnits="userSpaceOnUse" x1="{-RA * CELL:.0f}" x2="{RA * CELL:.0f}" y1="0" y2="0"><stop offset="0" stop-color="#fb923c"/><stop offset=".5" stop-color="#fda4af"/><stop offset="1" stop-color="#f472b6"/></linearGradient>')
w(f'<clipPath id="front"><rect x="{-RA * CELL - 2:.0f}" y="0" width="{2 * RA * CELL + 4:.0f}" height="{RB * CELL + 2:.0f}"/></clipPath>')
w(f'<clipPath id="pc"><circle cx="{GX + PCX * CELL:.1f}" cy="{GY + PCY * CELL:.1f}" r="{PR * CELL:.0f}"/></clipPath>')
w(f'<mask id="moon" maskUnits="userSpaceOnUse" x="0" y="0" width="1200" height="700"><circle cx="{GX + 27.4 * CELL:.0f}" cy="{GY + 4.0 * CELL:.0f}" r="{2.9 * CELL:.0f}" fill="#fff"/><circle cx="{GX + 26.2 * CELL:.0f}" cy="{GY + 3.2 * CELL:.0f}" r="{2.4 * CELL:.0f}" fill="#000"/></mask>')
w(f'<clipPath id="gc"><rect x="{GX}" y="{GY}" width="{GW}" height="{GH}" rx="10"/></clipPath>')
w("</defs>")

den0, den1, hold1, re1 = 10, 58, 80, 97
css = base_css(".nz")
for g in range(GROUPS):
    r = den0 + 4 + (den1 - den0 - 12) * (g + random.random() * .8) / GROUPS
    n = hold1 + (re1 - hold1 - 4) * random.random()
    css.append(f"@keyframes k{g}{{0%,{r:.1f}%{{opacity:1}}{r + 4:.1f}%,{n:.1f}%{{opacity:0}}{n + 3:.1f}%,100%{{opacity:1}}}}.k{g}{{animation:k{g} {T}s infinite}}")
css.append(f"@keyframes fk{{0%,49.9%{{opacity:1}}50%,100%{{opacity:0}}}}")
css.append(f"@keyframes sh{{0%,{den1 - 18}%{{opacity:0}}{den1 + 2}%,{re1}%{{opacity:1}}{re1 + .5}%,100%{{opacity:0}}}}")
css.append(f"@keyframes co{{0%,{den0 + 6}%{{opacity:0}}{den0 + 22}%,{re1}%{{opacity:1}}{re1 + .5}%,100%{{opacity:0}}}}")
sweeps = []
for s in range(STEPS):
    a = den0 + (den1 - den0) * s / STEPS
    b = a + (den1 - den0) / STEPS * .8
    sweeps.append(f"{a:.1f}%{{transform:translateY(0);opacity:0}}{a + .5:.1f}%{{opacity:1}}{b - .5:.1f}%{{opacity:1}}{b:.1f}%{{transform:translateY({GH + 60}px);opacity:0}}")
css.append("@keyframes sw{0%{transform:translateY(0);opacity:0}" + "".join(sweeps) + "100%{transform:translateY(0);opacity:0}}")
TW = GW
css.append(f"@keyframes dot{{0%,{den0}%{{transform:translateX(0)}}{den1}%,{hold1}%{{transform:translateX({TW}px)}}{re1}%,100%{{transform:translateX(0)}}}}")
for s in range(STEPS + 1):
    p = den0 + (den1 - den0) * s / STEPS
    css.append(f"@keyframes t{s}{{0%,{p - .5:.1f}%{{opacity:.25}}{p:.1f}%,{hold1}%{{opacity:1}}{re1 - (re1 - hold1) * s / STEPS:.1f}%,100%{{opacity:.25}}}}")
css.append(f"@keyframes hd{{0%,{den1 - 8}%{{opacity:0}}{den1 + 4}%,{re1}%{{opacity:1}}{re1 + .5}%,100%{{opacity:0}}}}")
css.append("@keyframes gl{0%,50%{opacity:0}62%,80%{opacity:1}95%,100%{opacity:0}}")
w("<style>" + "".join(css) + "</style>")

w(nebula((460, 330), (770, 320)))
o.extend(stars(70, (GX - 10, GY - 10, GX + GW + 10, GY + GH + 10)))

w(f'<rect x="{GX - 8}" y="{GY - 8}" width="{GW + 16}" height="{GH + 16}" rx="14" fill="#0b1023" fill-opacity=".55" stroke="#818cf8" stroke-opacity=".35"/>')
w(f'<ellipse cx="{600}" cy="{330}" rx="{GW * .55}" ry="{GH * .6}" fill="url(#nb1)" opacity="0" style="animation:gl {T}s infinite"/>')

w(f'<g clip-path="url(#gc)">')
# coarse (blurred) layer: 3x3 block averages
coarse = []
for by in range(0, ROWS, 2):
    for bx in range(0, COLS, 3):
        cells = [img[y][x] for y in range(by, min(by + 2, ROWS)) for x in range(bx, min(bx + 3, COLS))]
        avg = tuple(sum(c[i] for c in cells) / len(cells) for i in range(3))
        avg = mix(avg, BG, .15)
        coarse.append(f'<rect x="{GX + bx * CELL:.0f}" y="{GY + by * CELL:.0f}" width="{3 * CELL}" height="{2 * CELL}" fill="{hexc(avg)}"/>')
w(f'<g opacity="0" style="animation:co {T}s infinite">' + "".join(coarse) + "</g>")

# sharp layer, merged by colour
by_col = {}
for y in range(ROWS):
    for x in range(COLS):
        by_col.setdefault(hexc(img[y][x]), []).append(cell(x, y))
w(f'<g opacity="0" style="animation:sh {T}s infinite">' + "".join(f'<path d="{"".join(d)}" fill="{c}"/>' for c, d in by_col.items()) + "</g>")

# final high-definition vector layer
X, Y, R = GX + PCX * CELL, GY + PCY * CELL, PR * CELL
ra, rb = RA * CELL, RB * CELL
band = (f"M{-ra:.1f} 0a{ra:.1f} {rb:.1f} 0 1 0 {2 * ra:.1f} 0a{ra:.1f} {rb:.1f} 0 1 0 {-2 * ra:.1f} 0z"
        f"M{-ra * .707:.1f} 0a{ra * .707:.1f} {rb * .707:.1f} 0 1 0 {2 * ra * .707:.1f} 0a{ra * .707:.1f} {rb * .707:.1f} 0 1 0 {-2 * ra * .707:.1f} 0z")
ring_t = f'translate({X:.1f} {Y:.1f}) rotate({math.degrees(ROT):.0f})'
MX, MY, MR = GX + 27.4 * CELL, GY + 4.0 * CELL, 2.9 * CELL
hd = [f'<rect x="{GX}" y="{GY}" width="{GW}" height="{GH}" fill="{hexc(BG)}"/>']
for i in range(26):
    hd.append(f'<circle cx="{GX + random.uniform(8, GW - 8):.0f}" cy="{GY + random.uniform(8, GH - 8):.0f}" r="{random.choice([.6, .8, 1])}" fill="#e0e7ff" opacity="{random.uniform(.2, .6):.2f}"/>')
for (sx, sy) in sorted(STAR_CELLS):
    cx, cy = GX + (sx + .5) * CELL, GY + (sy + .5) * CELL
    hd.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="9" fill="url(#sg)"/><path d="M{cx:.0f} {cy - 6:.0f}L{cx + 1.4:.1f} {cy - 1.4:.1f}L{cx + 6:.0f} {cy:.0f}L{cx + 1.4:.1f} {cy + 1.4:.1f}L{cx:.0f} {cy + 6:.0f}L{cx - 1.4:.1f} {cy + 1.4:.1f}L{cx - 6:.0f} {cy:.0f}L{cx - 1.4:.1f} {cy - 1.4:.1f}Z" fill="#e0e7ff"/>')
hd.append(f'<circle cx="{MX:.0f}" cy="{MY:.0f}" r="{MR * 1.7:.0f}" fill="url(#mg)"/><circle cx="{MX:.0f}" cy="{MY:.0f}" r="{MR:.0f}" fill="#fde68a" mask="url(#moon)"/>')
hd.append(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="{R * 1.35:.0f}" fill="url(#atm)"/>')
hd.append(f'<g transform="{ring_t}"><path d="{band}" fill="url(#rg)" fill-rule="evenodd" opacity=".9"/></g>')
hd.append(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="{R:.0f}" fill="url(#pg)"/>')
hd.append(f'<g clip-path="url(#pc)" fill="none" stroke="#e0f2fe" stroke-opacity=".08" stroke-width="6"><path d="M{X - R:.0f} {Y - R * .35:.0f}Q{X:.0f} {Y - R * .2:.0f} {X + R:.0f} {Y - R * .45:.0f}M{X - R:.0f} {Y + R * .1:.0f}Q{X:.0f} {Y + R * .25:.0f} {X + R:.0f} {Y:.0f}M{X - R:.0f} {Y + R * .5:.0f}Q{X:.0f} {Y + R * .65:.0f} {X + R:.0f} {Y + R * .4:.0f}"/></g>')
hd.append(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="{R:.0f}" fill="url(#sh)"/>')
hd.append(f'<g transform="{ring_t}"><path d="{band}" fill="url(#rg)" fill-rule="evenodd" clip-path="url(#front)"/></g>')
w(f'<g style="animation:hd {T}s infinite">' + "".join(hd) + "</g>")

# noise layers, merged by (group, colour)
groups = [[random.randrange(GROUPS) for _ in range(COLS)] for _ in range(ROWS)]
for layer in range(2):
    paths = {}
    for y in range(ROWS):
        for x in range(COLS):
            c = random.choice(NOISE)
            paths.setdefault((groups[y][x], c), []).append(cell(x, y))
    inner = "".join(f'<path class="k{g}" d="{"".join(d)}" fill="{c}" fill-opacity="{random.uniform(.55, .9):.2f}"/>' for (g, c), d in sorted(paths.items()))
    style = f' style="animation:fk .36s steps(1) infinite"' if layer else ""
    w(f'<g class="nz"{style}>{inner}</g>')

w(f'<rect x="{GX}" y="{GY - 60}" width="{GW}" height="60" fill="url(#band)" opacity="0" style="animation:sw {T}s linear infinite"/>')
w("</g>")

# timestep track under the grid
ty = GY + GH + 48
w(f'<line x1="{GX}" y1="{ty}" x2="{GX + GW}" y2="{ty}" stroke="url(#trk)" stroke-opacity=".35" stroke-width="2"/>')
for s in range(STEPS + 1):
    x = GX + GW * s / STEPS
    w(f'<circle cx="{x:.0f}" cy="{ty}" r="5" fill="#0b1023" stroke="{palette(s / STEPS, ["#e879f9", "#a855f7", "#6366f1", "#22d3ee"])}" stroke-width="1.5" style="animation:t{s} {T}s infinite"/>')
w(f'<g style="animation:dot {T}s cubic-bezier(.45,0,.35,1) infinite"><circle cx="{GX}" cy="{ty}" r="14" fill="#fff" fill-opacity=".12"/><circle cx="{GX}" cy="{ty}" r="5" fill="#fff"/></g>')

w("</svg>")
save(sys.argv[1], o)
