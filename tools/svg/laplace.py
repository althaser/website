import math
import random
import sys

from common import (DEFS, FONT, MONO, STAR, base, base_css, curiosity, mobile, nebula, num, poly, small, stars, subtitle,
                    title, write_svg)

random.seed(29)
T = 15.0
OMEGA = 2.4
# each state: damping sigma, where its poles are drawn (px from the Im axis), colour, label
STATES = [(.35, -130, "#4ade80", "decays · stable"), (0.0, 0, "#fbbf24", "rings forever"), (-.08, 110, "#f43f5e", "grows · unstable")]
N = len(STATES)
DRAW = .6

# signal panel
SX0, SX1, SY, AMP, BOX = 80, 540, 410, 95, 150
TMAX = 10.0
# s-plane panel
PCX, PCY, IM = 890, 410, 52


def f(sigma, t):
    return math.exp(-sigma * t) * math.cos(OMEGA * t)


def signal(sigma):
    """The curve itself; the panel clip cuts it where it grows out of the box."""
    return [(SX0 + (SX1 - SX0) * i / 250, SY - AMP * f(sigma, TMAX * i / 250)) for i in range(251)]


def window(k):
    a = 100 * k / N
    return a, a + 100 / N


css = [
    ".rv{transform-box:fill-box;transform-origin:0 50%}",
    mobile(".ax{font-size:22px}.st{font-size:28px}"),
] + base_css()
defs = ["<defs>", *DEFS,
        f'<clipPath id="sb"><rect x="{SX0 - 6}" y="{SY - BOX}" width="{SX1 - SX0 + 12}" height="{2 * BOX}"/></clipPath>',
        f'<linearGradient id="hp" x1="0" x2="1"><stop offset="0" stop-color="#4ade80" stop-opacity=".1"/><stop offset=".5" stop-color="#4ade80" stop-opacity=".02"/>'
        f'<stop offset=".5" stop-color="#f43f5e" stop-opacity=".02"/><stop offset="1" stop-color="#f43f5e" stop-opacity=".1"/></linearGradient>']
o = [nebula((330, 410), (890, 410), (300, 300), 270)]
o.extend(stars(80))

# --- the signal in time -----------------------------------------------------------
o.append(title((SX0 + SX1) / 2, 66, "a signal in time"))
o.append(subtitle((SX0 + SX1) / 2, 98, f"f(t) = e{small('−σt', up=True)}{base(' cos ωt', up=True)}"))
o.append(f'<line x1="{SX0}" y1="{SY}" x2="{SX1 + 10}" y2="{SY}" stroke="{STAR}" stroke-opacity=".3"/>'
         f'<line x1="{SX0}" y1="{SY - BOX}" x2="{SX0}" y2="{SY + BOX}" stroke="{STAR}" stroke-opacity=".3"/>'
         f'<text x="{SX1 + 18}" y="{SY + 5}" class="ax" {FONT} font-style="italic" font-size="17" fill="{STAR}" fill-opacity=".75">t</text>')

for k, (sigma, _, col, label) in enumerate(STATES):
    a, b = window(k)
    end = "100%" if k == N - 1 else f"{b:.2f}%,100%"  # the last state ends exactly at 100%
    d = a + (b - a) * DRAW
    pts = signal(sigma)
    vis = f"0%{{opacity:1}}{b - 3:.2f}%{{opacity:1}}{b:.2f}%,100%{{opacity:0}}" if k == 0 else \
        f"0%,{a:.2f}%{{opacity:0}}{a + .5:.2f}%,{b - 3:.2f}%{{opacity:1}}{end}{{opacity:0}}"
    css.append(f"@keyframes w{k}{{{vis}}}")
    hold = f"0%,{a:.2f}%" if k else "0%"
    css.append(f"@keyframes rv{k}{{{hold}{{transform:scaleX(0)}}{d:.2f}%,100%{{transform:scaleX(1)}}}}")
    defs.append(f'<mask id="m{k}" maskUnits="userSpaceOnUse" x="0" y="0" width="1200" height="700">'
                f'<rect class="rv" x="{SX0 - 6}" y="{SY - BOX}" width="{SX1 - SX0 + 12}" height="{2 * BOX}" fill="#fff" style="animation:rv{k} {T}s linear infinite"/></mask>')
    still = "" if k == 0 else ' opacity="0"'
    o.append(f'<g{still} style="animation:w{k} {T}s linear infinite"><g clip-path="url(#sb)" mask="url(#m{k})">'
             f'<path d="{poly(pts)}" fill="none" stroke="{col}" stroke-width="2.4" stroke-linejoin="round"/></g>'
             f'<text x="{(SX0 + SX1) / 2}" y="{SY + BOX + 40}" text-anchor="middle" class="st" {FONT} font-style="italic" font-size="20" fill="{col}">{label}</text></g>')
    # pen at the tip of the curve while it is being drawn
    # hidden until just before its own window; two keyframes at the same offset would let the second one leak back to 0%
    frames = [f"0%,{a - .01:.2f}%{{transform:translate({num(pts[0][0])}px,{num(pts[0][1])}px);opacity:0}}"] if k else []
    for i in range(41):
        x, y = pts[round(i * 250 / 40)]
        op = 1 if i < 40 and abs(y - SY) < BOX else 0
        frames.append(f"{a + (d - a) * i / 40:.2f}%{{transform:translate({num(x)}px,{num(y)}px);opacity:{op}}}")
    frames.append(f"100%{{transform:translate({num(pts[-1][0])}px,{num(pts[-1][1])}px);opacity:0}}")
    css.append(f"@keyframes pn{k}{{{''.join(frames)}}}")
    o.append(f'<g class="mv" style="animation:pn{k} {T}s linear infinite"><circle r="12" fill="url(#hl)"/><circle r="3.5" fill="#fff"/></g>')

# --- its poles in the s-plane ---------------------------------------------------------
o.append(title(PCX, 66, "its poles in the s-plane"))
o.append(subtitle(PCX, 98, f"F(s) = ∫ f(t) e{small('−st', up=True)}{base(' dt', up=True)}"))
HW, HH = 200, 160
o.append(f'<rect x="{PCX - HW}" y="{PCY - HH}" width="{2 * HW}" height="{2 * HH}" rx="10" fill="url(#hp)"/>')
o.append(f'<line x1="{PCX - HW}" y1="{PCY}" x2="{PCX + HW}" y2="{PCY}" stroke="{STAR}" stroke-opacity=".3"/>'
         f'<line x1="{PCX}" y1="{PCY - HH}" x2="{PCX}" y2="{PCY + HH}" stroke="{STAR}" stroke-opacity=".3"/>'
         f'<text x="{PCX + HW - 4}" y="{PCY - 9}" text-anchor="end" class="ax" {FONT} font-style="italic" font-size="17" fill="{STAR}" fill-opacity=".75">Re</text>'
         f'<text x="{PCX + 9}" y="{PCY - HH + 16}" class="ax" {FONT} font-style="italic" font-size="17" fill="{STAR}" fill-opacity=".75">Im</text>')
o.append(f'<text x="{PCX - HW / 2}" y="{PCY + HH + 26}" text-anchor="middle" class="ax" {MONO} font-size="13" fill="#4ade80" fill-opacity=".8">stable</text>'
         f'<text x="{PCX + HW / 2}" y="{PCY + HH + 26}" text-anchor="middle" class="ax" {MONO} font-size="13" fill="#f43f5e" fill-opacity=".8">unstable</text>')

# the pair of poles slides between the three states, in step with the signal
xs = [px for _, px, _, _ in STATES]
pf = []
for k in range(N):
    a, b = window(k)
    pf.append(f"{a + (3 if k else 0):.2f}%,{b - 2:.2f}%{{transform:translateX({num(xs[k])}px)}}")
pf.append(f"100%{{transform:translateX({num(xs[0])}px)}}")
css.append(f"@keyframes pl{{{''.join(pf)}}}")
POLES = (PCY - OMEGA * IM, PCY + OMEGA * IM)
cross = "".join(f'<path d="M-9 {y - 9}l18 18M9 {y - 9}l-18 18" stroke="#fff" stroke-width="3" stroke-linecap="round"/>' for y in POLES)
glow = "".join(f'<circle cy="{y}" r="20" fill="url(#hl)"/>' for y in POLES)
o.append(f'<g transform="translate({PCX} 0)"><g transform="translate({num(xs[0])} 0)" style="animation:pl {T}s cubic-bezier(.5,0,.3,1) infinite">{glow}{cross}</g></g>')
for k, (_, _, col, _) in enumerate(STATES):
    a, b = window(k)
    end = "100%" if k == N - 1 else f"{b:.2f}%,100%"
    vis = f"0%{{opacity:1}}{b - 3:.2f}%{{opacity:1}}{b:.2f}%,100%{{opacity:0}}" if k == 0 else \
        f"0%,{a:.2f}%{{opacity:0}}{a + 3:.2f}%,{b - 3:.2f}%{{opacity:1}}{end}{{opacity:0}}"
    css.append(f"@keyframes c{k}{{{vis}}}")
    still = "" if k == 0 else ' opacity="0"'
    o.append(f'<g{still} style="animation:c{k} {T}s linear infinite">'
             + "".join(f'<circle cx="{num(PCX + xs[k])}" cy="{y}" r="15" fill="none" stroke="{col}" stroke-width="2"/>' for y in POLES)
             + "</g>")

o.append(curiosity(600, 672, "engineers check if a bridge, a circuit or an autopilot is stable just by where its poles sit"))

defs.append("</defs>")
write_svg(sys.argv[1], "Animated Laplace transform: a damped, steady and growing signal and its poles moving across the s-plane", defs, css, o)
