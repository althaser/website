import math
import random
import sys

from common import DEFS, FONT, MONO, STAR, base_css, curiosity, mobile, nebula, poly, stars, title, write_svg

random.seed(23)
SX, SY, SR = 170, 245, 52
EX, EY, ER = 760, 245, 118
DX, DY = 820, 300
X1 = 1150
STREAMS = 13
P = 2.6
CATCH = 7.0

# flavour oscillation strip
OX0, OX1, OY = 160, 1040, 560
OP = 9.0
FLAVOURS = [("e", "#22d3ee"), ("μ", "#a855f7"), ("τ", "#fb923c")]

css = [
    "@keyframes fly{0%{transform:translateX(0);opacity:0}6%,92%{opacity:1}100%{transform:translateX(var(--d));opacity:0}}",
    "@keyframes ring{0%,88%{transform:scale(.1);opacity:0}89%{opacity:1}100%{transform:scale(1.8);opacity:0}}",
    "@keyframes hit{0%,88%{opacity:0}89%{opacity:1}96%,100%{opacity:0}}",
    f"@keyframes ride{{to{{transform:translateX({OX1 - OX0}px)}}}}",
    ".rg{transform-box:fill-box;transform-origin:center}",
    mobile(".ax{font-size:22px}.fl{font-size:36px}.fs{font-size:26px}.fc{display:none}"),
] + base_css()
defs = ["<defs>", *DEFS,
        '<radialGradient id="sun"><stop offset="0" stop-color="#fff7d6"/><stop offset=".4" stop-color="#fde68a"/><stop offset=".75" stop-color="#fb923c" stop-opacity=".35"/><stop offset="1" stop-color="#fb923c" stop-opacity="0"/></radialGradient>',
        '<radialGradient id="ea" cx=".38" cy=".35"><stop offset="0" stop-color="#60a5fa"/><stop offset=".6" stop-color="#1e3a8a"/><stop offset="1" stop-color="#0b1023"/></radialGradient>']
o = [nebula((330, 300), (840, 330), (300, 340), 260)]
o.extend(stars(90))

# --- from the Sun, straight through the Earth -------------------------------------
o.append(title(600, 66, "from the sun, straight through the earth"))
o.append(f'<circle cx="{EX}" cy="{EY}" r="{ER}" fill="url(#ea)" stroke="#60a5fa" stroke-opacity=".5"/>'
         f'<circle cx="{EX}" cy="{EY}" r="{ER * .45:.0f}" fill="#fb923c" fill-opacity=".12"/>')
o.append(f'<text x="{EX}" y="{EY + ER + 28}" text-anchor="middle" class="ax" {MONO} font-size="13" fill="#93c5fd" fill-opacity=".8">Earth</text>')

ys = [SY + (i - (STREAMS - 1) / 2) * 16 for i in range(STREAMS)]
o.append(f'<path d="{"".join(f"M{SX + SR * .6:.0f} {y:.0f}H{X1}" for y in ys)}" stroke="#c7d2fe" stroke-opacity=".12"/>')
for y in ys:
    for k in range(3):
        x0 = SX + 30
        o.append(f'<circle class="mv" cx="{x0}" cy="{y:.0f}" r="1.8" fill="#e0e7ff" '
                 f'style="--d:{X1 - x0}px;animation:fly {P}s linear {-random.uniform(0, P):.2f}s infinite"/>')

o.append(f'<circle cx="{SX}" cy="{SY}" r="{SR * 2.1:.0f}" fill="url(#sun)"/><circle cx="{SX}" cy="{SY}" r="{SR * .55:.0f}" fill="#fff4cc"/>')
o.append(f'<text x="{SX}" y="{SY + SR + 52}" text-anchor="middle" class="ax" {MONO} font-size="13" fill="#fde68a" fill-opacity=".8">Sun</text>')

# a rare catch: one neutrino stops in the underground detector and leaves a ring of light
o.append(f'<rect x="{DX - 22}" y="{DY - 14}" width="44" height="28" rx="6" fill="#0b1023" fill-opacity=".85" stroke="#22d3ee" stroke-opacity=".7"/>')
o.append(f'<circle class="mv rg" cx="{DX}" cy="{DY}" r="16" fill="none" stroke="#67e8f9" stroke-width="1.6" style="animation:ring {CATCH}s ease-out infinite"/>'
         f'<circle class="mv" cx="{DX}" cy="{DY}" r="10" fill="url(#hl)" style="animation:hit {CATCH}s linear infinite"/>')
o.append(f'<text x="{DX + 30}" y="{DY + 5}" class="ax" {MONO} font-size="12" fill="#67e8f9" fill-opacity=".8">detector</text>')
o.append(f'<text x="{X1}" y="{SY + 140}" text-anchor="end" class="fc" {FONT} font-size="20" fill="#fde68a">65 billion</text>'
         f'<text x="{X1}" y="{SY + 160}" text-anchor="end" class="fc" {MONO} font-size="12" fill="{STAR}" fill-opacity=".6">per cm² every second</text>')

# --- flavour oscillation ----------------------------------------------------------
o.append(title(600, 470, "changing flavour on the way"))
waves = []
for i, (_, col) in enumerate(FLAVOURS):
    pts = [(x, OY - 34 * max(0, math.cos(2 * math.pi * ((x - OX0) / (OX1 - OX0) * 2 - i / 3)))) for x in range(OX0, OX1 + 1, 8)]
    waves.append(f'<path d="{poly(pts)}L{OX1} {OY}L{OX0} {OY}Z" fill="{col}" fill-opacity=".1"/>'
                 f'<path d="{poly(pts)}" fill="none" stroke="{col}" stroke-opacity=".85" stroke-width="2"/>')
o.extend(waves)
o.append(f'<line x1="{OX0}" y1="{OY}" x2="{OX1}" y2="{OY}" stroke="{STAR}" stroke-opacity=".25"/>')

# the travelling neutrino: three stacked colours cross-fading in step with the curves above
dots = []
for i, (_, col) in enumerate(FLAVOURS):
    frames = []
    for k in range(61):
        t = k / 60
        p = max(0, math.cos(2 * math.pi * (t * 2 - i / 3)))
        frames.append(f"{100 * t:.1f}%{{opacity:{p:.2f}}}")
    css.append(f"@keyframes fv{i}{{{''.join(frames)}}}")
    dots.append(f'<circle r="9" fill="{col}" style="animation:fv{i} {OP}s linear infinite"/>')
o.append(f'<g transform="translate({OX0} {OY})"><g class="mv" style="animation:ride {OP}s linear infinite">'
         f'<circle r="22" fill="url(#hl)"/>{"".join(dots)}</g></g>')
for n, (name, col) in enumerate(FLAVOURS):
    x = 600 + (n - 1) * 130
    o.append(f'<circle cx="{x - 30}" cy="{OY + 45}" r="6" fill="{col}"/>'
             f'<text x="{x - 18}" y="{OY + 52}" class="fl" {FONT} font-style="italic" font-size="22" fill="{col}">ν<tspan class="fs" font-size="15" dy="4">{name}</tspan></text>')

o.append(curiosity(600, 664, "Super-Kamiokande hides 50 000 tonnes of water 1 km underground to catch just a few a day"))

defs.append("</defs>")
write_svg(sys.argv[1], "Animated neutrinos streaming from the Sun straight through the Earth, and one neutrino changing flavour as it travels", defs, css, o)
