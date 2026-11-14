import math
import random
import sys

from common import DEFS, FONT, MONO, STAR, base_css, mobile, nebula, num, palette, poly, stars, subtitle, title, write_svg

random.seed(13)

# speed of light: Earth to Moon, in real time
EX, MX, LY = 150, 1050, 160
ER, MR = 34, 10
TRIP, PC = 1.28, 3.2

# wave: double slit
# the panels share a 70 px side margin with the plate on the right
WX0 = 70
SX, SY = 150, 480
BX, GAP, SLIT = 310, 64, 12
SCR = 590
LAM, PW = 20, 12.0
TOP, BOT = 330, 640
S1, S2 = SY - GAP / 2, SY + GAP / 2

# particle: photoelectric effect
PLX0, PLX1, PLY = 700, 1130, 600
PP = 6.0
WORK = .5

css = [
    "@keyframes rg{0%{transform:scale(.02);opacity:.9}100%{transform:scale(1);opacity:0}}",
    ".w{fill:none;stroke-width:1.6;transform-box:view-box}",
    mobile(".ax{font-size:24px}.cu{display:none}"),
] + base_css(shown=".st")
defs = ["<defs>", *DEFS,
        '<radialGradient id="ea" cx=".38" cy=".35"><stop offset="0" stop-color="#7dd3fc"/><stop offset=".55" stop-color="#2563eb"/><stop offset="1" stop-color="#1e1b4b"/></radialGradient>',
        '<radialGradient id="mo" cx=".38" cy=".35"><stop offset="0" stop-color="#f1f5f9"/><stop offset="1" stop-color="#64748b"/></radialGradient>',
        '<linearGradient id="pl" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#cbd5e1"/><stop offset="1" stop-color="#475569"/></linearGradient>',
        f'<linearGradient id="bm" gradientUnits="userSpaceOnUse" x1="-90" x2="0" y1="0" y2="0"><stop offset="0" stop-color="#fde68a" stop-opacity="0"/><stop offset="1" stop-color="#fff7d6"/></linearGradient>',
        f'<clipPath id="before"><rect x="{WX0}" y="{TOP}" width="{BX - WX0}" height="{BOT - TOP}"/></clipPath>',
        f'<linearGradient id="fv" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".18" stop-color="#fff"/><stop offset=".82" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>',
        f'<linearGradient id="fh" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".25" stop-color="#fff"/></linearGradient>',
        f'<mask id="mv" maskUnits="userSpaceOnUse" x="{WX0}" y="{TOP}" width="{SCR - WX0}" height="{BOT - TOP}"><rect x="{WX0}" y="{TOP}" width="{SCR - WX0}" height="{BOT - TOP}" fill="url(#fv)"/></mask>',
        f'<mask id="mh" maskUnits="userSpaceOnUse" x="{WX0}" y="{TOP}" width="{BX - WX0}" height="{BOT - TOP}"><rect x="{WX0}" y="{TOP}" width="{BX - WX0}" height="{BOT - TOP}" fill="url(#fh)"/></mask>',
        f'<clipPath id="after"><rect x="{BX + 2}" y="{TOP}" width="{SCR - BX - 2}" height="{BOT - TOP}"/></clipPath>',
        "</defs>"]
o = [nebula((370, 470), (900, 430), (300, 290), 220)]
o.extend(stars(80))

# --- speed of light ---------------------------------------------------------------
o.append(title(600, 66, "light: wave or particle"))
o.append(subtitle(600, 98, "c = 299 792 458 m/s"))
o.append(f'<line x1="{EX + ER}" y1="{LY}" x2="{MX - MR}" y2="{LY}" stroke="{STAR}" stroke-opacity=".18" stroke-dasharray="2 6"/>')
o.append(f'<circle cx="{EX}" cy="{LY}" r="{ER * 1.6:.0f}" fill="url(#hl)" opacity=".5"/><circle cx="{EX}" cy="{LY}" r="{ER}" fill="url(#ea)"/>')
o.append(f'<circle cx="{MX}" cy="{LY}" r="{MR}" fill="url(#mo)"/>')
for dx, dy, r in ((-3, -3, 2.2), (3, 2, 1.6), (-1, 4, 1.2)):
    o.append(f'<circle cx="{MX + dx}" cy="{LY + dy}" r="{r}" fill="#475569" fill-opacity=".5"/>')
o.append(f'<text x="{EX}" y="{LY + ER + 26}" text-anchor="middle" class="ax" {MONO} font-size="13" fill="#7dd3fc">Earth</text>')
o.append(f'<text x="{MX}" y="{LY + ER + 26}" text-anchor="middle" class="ax" {MONO} font-size="13" fill="#cbd5e1">Moon</text>')
o.append(f'<text x="{(EX + MX) / 2}" y="{LY + 30}" text-anchor="middle" class="ax" {MONO} font-size="13" fill="{STAR}" fill-opacity=".55">384 400 km</text>')
arrive = TRIP / PC * 100
dist = MX - MR - EX - ER
css.append(f"@keyframes cb{{0%{{transform:translateX(0);opacity:1}}{arrive:.1f}%{{transform:translateX({dist}px);opacity:1}}{arrive + 2:.1f}%,100%{{transform:translateX({dist}px);opacity:0}}}}")
css.append(f"@keyframes cf{{0%,{arrive - .5:.1f}%{{opacity:0}}{arrive + 1:.1f}%{{opacity:1}}{arrive + 30:.1f}%,100%{{opacity:0}}}}")
css.append(f"@keyframes ct{{0%,{arrive - .5:.1f}%{{opacity:0}}{arrive + 1:.1f}%,92%{{opacity:1}}97%,100%{{opacity:0}}}}")
o.append(f'<g transform="translate({EX + ER} {LY})"><g class="mv" style="animation:cb {PC}s linear infinite">'
         f'<line x1="-90" y1="0" x2="0" y2="0" stroke="url(#bm)" stroke-width="3" stroke-linecap="round"/><circle r="9" fill="url(#hl)"/><circle r="3" fill="#fff"/></g></g>')
o.append(f'<circle class="mv" cx="{MX}" cy="{LY}" r="26" fill="url(#hl)" style="animation:cf {PC}s linear infinite"/>')
o.append(f'<text class="mv ax" x="{MX}" y="{LY - 26}" text-anchor="middle" {MONO} font-size="14" fill="#fde68a" style="animation:ct {PC}s linear infinite">{TRIP} s</text>')

# --- wave: double slit ------------------------------------------------------------
o.append(title((SX + SCR) / 2, 280, "wave"))
o.append(subtitle((SX + SCR) / 2, 312, "double slit"))
rings = int(400 / LAM)


# every ring set grows at the same speed, so a crest leaves the source every PW / rings seconds
def ring_set(cx, cy, radius, clip, colour):
    n = math.ceil(radius / LAM)
    period = n * PW / rings
    out = [f'<g clip-path="url(#{clip})">']
    for i in range(n):
        out.append(f'<circle class="w mv" cx="{cx}" cy="{cy}" r="{radius}" stroke="{colour}" vector-effect="non-scaling-stroke" '
                   f'style="transform-origin:{cx}px {cy}px;animation:rg {period:.2f}s linear {-i * period / n:.2f}s infinite"/>')
    # still wavefronts, shown only when motion is reduced
    out.extend(f'<circle class="w st" cx="{cx}" cy="{cy}" r="{k * LAM}" stroke="{colour}" stroke-opacity="{.9 * (1 - k / (n + 1)):.2f}"/>' for k in range(1, n + 1))
    return out + ["</g>"]


o.append('<g mask="url(#mv)"><g mask="url(#mh)">')
o.extend(ring_set(SX, SY, BX - SX + 10, "before", "#22d3ee"))
o.append("</g>")
for sy in (S1, S2):
    o.extend(ring_set(BX, sy, SCR - BX + 40, "after", "#a78bfa"))
o.append("</g>")
o.append(f'<circle cx="{SX}" cy="{SY}" r="14" fill="url(#hl)"/><circle cx="{SX}" cy="{SY}" r="4" fill="#a5f3fc"/>')
bar = [(TOP, S1 - SLIT / 2), (S1 + SLIT / 2, S2 - SLIT / 2), (S2 + SLIT / 2, BOT)]
o.append(f'<path d="{"".join(f"M{BX} {a:.0f}V{b:.0f}" for a, b in bar)}" stroke="#c7d2fe" stroke-opacity=".8" stroke-width="4"/>')

# interference on the screen, with its intensity profile
L = SCR - BX
fr, prof = [], []
for k in range(0, int(BOT - TOP) + 1, 3):
    y = TOP + k
    r1, r2 = math.hypot(L, y - S1), math.hypot(L, y - S2)
    env = math.exp(-((y - SY) / 170) ** 2)
    inten = math.cos(math.pi * (r1 - r2) / LAM) ** 2 * env
    fr.append(f'<rect x="{SCR - 3}" y="{y - 1.5:.1f}" width="8" height="3" fill="{palette(.55 + .45 * inten)}" fill-opacity="{.08 + .92 * inten:.2f}"/>')
    prof.append((SCR + 12 + 30 * inten, y))
o.append("".join(fr))
o.append(f'<path d="{poly(prof)}" fill="none" stroke="#f0abfc" stroke-opacity=".8" stroke-width="1.4"/>')
o.append(f'<line x1="{SCR + 12}" y1="{TOP}" x2="{SCR + 12}" y2="{BOT}" stroke="{STAR}" stroke-opacity=".2"/>')

# --- particle: photoelectric effect -----------------------------------------------
o.append(title(915, 280, "particle"))
o.append(subtitle(915, 312, "E = hf"))
o.append(f'<rect x="{PLX0}" y="{PLY}" width="{PLX1 - PLX0}" height="22" rx="3" fill="url(#pl)" fill-opacity=".85"/>')
o.append(f'<text x="{(PLX0 + PLX1) / 2}" y="{PLY + 15}" text-anchor="middle" {MONO} font-size="12" fill="#1e293b">metal</text>')
hits = 6
for n in range(hits):
    violet = n % 2 == 0
    col, wl = ("#a78bfa", 7) if violet else ("#f87171", 15)
    hx = PLX0 + 60 + (PLX1 - PLX0 - 120) * ((n * 3) % hits + .5) / hits
    sx, sy = hx - 120, PLY - 250
    ang = math.atan2(PLY - sy, hx - sx)
    length = math.hypot(hx - sx, PLY - sy)
    squiggle = poly((-36 + t, 5 * math.sin(2 * math.pi * t / wl)) for t in range(0, 37, 1))
    b = 34
    css.append(f"@keyframes ph{n}{{0%{{transform:translate({sx}px,{sy}px) rotate({math.degrees(ang):.1f}deg);opacity:0}}"
               f"4%{{opacity:1}}{b - 1}%{{opacity:1}}{b}%{{transform:translate({num(hx)}px,{PLY}px) rotate({math.degrees(ang):.1f}deg);opacity:0}}"
               f"100%{{transform:translate({num(hx)}px,{PLY}px) rotate({math.degrees(ang):.1f}deg);opacity:0}}}}")
    delay = -n * PP / hits
    o.append(f'<g class="mv" style="animation:ph{n} {PP}s linear {delay:.2f}s infinite"><path d="{squiggle}" fill="none" stroke="{col}" stroke-width="2" stroke-linecap="round"/>'
             f'<circle r="8" fill="url(#hl)"/><circle r="2.6" fill="{col}"/></g>')
    css.append(f"@keyframes fx{n}{{0%,{b - 1}%{{opacity:0}}{b}%{{opacity:1}}{b + 10}%,100%{{opacity:0}}}}")
    o.append(f'<circle class="mv" cx="{num(hx)}" cy="{PLY}" r="16" fill="url(#hl)" style="animation:fx{n} {PP}s linear {delay:.2f}s infinite"/>')
    if violet:
        ex, ey = hx + 90, PLY - 230
        css.append(f"@keyframes el{n}{{0%,{b}%{{transform:translate({num(hx)}px,{PLY - 4}px);opacity:0}}{b + 1}%{{opacity:1}}{b + 34}%{{opacity:1}}"
                   f"{b + 40}%{{transform:translate({num(ex)}px,{ey}px);opacity:0}}100%{{transform:translate({num(ex)}px,{ey}px);opacity:0}}}}")
        o.append(f'<g class="mv" style="animation:el{n} {PP}s cubic-bezier(.2,.7,.4,1) {delay:.2f}s infinite"><circle r="10" fill="url(#hl)"/><circle r="4" fill="#fde68a"/>'
                 f'<text x="8" y="-8" {FONT} font-size="15" font-style="italic" fill="#fde68a">e⁻</text></g>')
o.append(f'<text x="{PLX0}" y="{PLY + 46}" class="ax" {MONO} font-size="13" fill="#a78bfa">high f → e⁻ ejected</text>'
         f'<text x="{PLX0}" y="{PLY + 72}" class="ax" {MONO} font-size="13" fill="#f87171">low f → none</text>')

o.append(f'<text x="600" y="238" text-anchor="middle" class="cu" {MONO} font-size="13" fill="{STAR}" fill-opacity=".6">'
         f'even one photon at a time builds up the stripes: each is a particle, and still a wave</text>')

write_svg(sys.argv[1], "Animated light: its speed from the Earth to the Moon, a double slit wave pattern and photons ejecting electrons", defs, css, o)
