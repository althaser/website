import math
import random
import sys

from common import DEFS, FONT, MONO, STAR, base_css, mobile, nebula, num, poly, stars, title, write_svg

random.seed(21)
CX, CY, R = 600, 392, 270
LY = R / 50000
SUN_R = 26000 * LY
SPIN = 240
PITCH = math.radians(17)
K = math.tan(PITCH)
R0 = .2 * R
BAR = math.radians(-30)
SUN_A = math.radians(90)
ARMS = 4


def arm_angle(i, r):
    """Arms trail a clockwise rotation, so they wind counter-clockwise outwards."""
    return BAR + i * 2 * math.pi / ARMS - math.log(r / R0) / K


def polar(r, a):
    return CX + r * math.cos(a), CY + r * math.sin(a)


def gauss(s):
    return random.gauss(0, s)


# name each arm by where it crosses the Sun's direction: just outside is Perseus, just inside is Sagittarius
def crossing(i):
    best = None
    for m in range(-3, 4):
        r = R0 * math.exp(K * (BAR + i * 2 * math.pi / ARMS + 2 * math.pi * m - SUN_A))
        if R0 <= r <= R * 1.05 and (best is None or abs(r - SUN_R) < abs(best - SUN_R)):
            best = r
    return best or 0


outer = min((i for i in range(ARMS) if crossing(i) > SUN_R), key=crossing)
inner = max((i for i in range(ARMS) if 0 < crossing(i) < SUN_R), key=crossing)
rest = [i for i in range(ARMS) if i not in (outer, inner)]
NAMES = {outer: "Perseus", inner: "Sagittarius", rest[0]: "Scutum–Centaurus", rest[1]: "Norma"}

css = [
    "@keyframes gr{to{transform:rotate(360deg)}}",
    "@keyframes ps{0%{transform:scale(.4);opacity:.9}100%{transform:scale(2.6);opacity:0}}",
    mobile(".ar{font-size:22px}.yh{font-size:30px}.ex{display:none}"),
] + base_css()
defs = ["<defs>", *DEFS,
        '<radialGradient id="dk"><stop offset="0" stop-color="#c7d2fe" stop-opacity=".22"/><stop offset=".55" stop-color="#6366f1" stop-opacity=".08"/><stop offset="1" stop-color="#6366f1" stop-opacity="0"/></radialGradient>',
        '<radialGradient id="bu"><stop offset="0" stop-color="#fff7d6"/><stop offset=".3" stop-color="#fde68a" stop-opacity=".8"/><stop offset=".7" stop-color="#fb923c" stop-opacity=".25"/><stop offset="1" stop-color="#fb923c" stop-opacity="0"/></radialGradient>',
        '<radialGradient id="eg" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fde68a" stop-opacity=".9"/><stop offset=".25" stop-color="#c7d2fe" stop-opacity=".45"/><stop offset="1" stop-color="#6366f1" stop-opacity="0"/></radialGradient>',
        "</defs>"]
o = [nebula((600, 392), (600, 392), (330, 300), 300)]
o.extend(stars(90))
o.append(title(600, 66, "the milky way"))

g = [f'<circle cx="{CX}" cy="{CY}" r="{R * 1.08:.0f}" fill="url(#dk)"/>']

# arms: a soft glow along each spiral, then its stars
for i in range(ARMS):
    curve = [polar(r, arm_angle(i, r)) for r in (R0 + (R - R0) * t / 120 for t in range(121))]
    for w, op in ((34, .05), (16, .08), (6, .14)):
        g.append(f'<path d="{poly(curve)}" fill="none" stroke="#a5b4fc" stroke-opacity="{op}" stroke-width="{w}" stroke-linecap="round"/>')
dots = []
for i in range(ARMS):
    for _ in range(330):
        r = R0 + (R - R0) * random.random() ** .8
        a = arm_angle(i, r)
        x, y = polar(r + gauss(4 + r * .04), a + gauss(.05))
        c = random.choice(["#e0e7ff", "#e0e7ff", "#c7d2fe", "#a5b4fc", "#f9a8d4"])
        dots.append(f'<circle cx="{num(x)}" cy="{num(y)}" r="{random.choice([.6, .8, 1, 1.3])}" fill="{c}" opacity="{random.uniform(.35, .95):.2f}"/>')
# the Orion spur, a short branch between Sagittarius and Perseus where the Sun sits
for _ in range(70):
    t = random.uniform(-1, 1)
    r = SUN_R + t * 26
    a = SUN_A - math.radians(9) * t + gauss(.03)
    x, y = polar(r + gauss(3), a)
    dots.append(f'<circle cx="{num(x)}" cy="{num(y)}" r="{random.choice([.6, .8, 1])}" fill="#e0e7ff" opacity="{random.uniform(.3, .8):.2f}"/>')
# the disc between the arms
for _ in range(380):
    r = R * min(1.05, random.expovariate(3.2))
    a = random.uniform(0, 2 * math.pi)
    x, y = polar(r, a)
    dots.append(f'<circle cx="{num(x)}" cy="{num(y)}" r=".7" fill="#e0e7ff" opacity="{random.uniform(.15, .45):.2f}"/>')
g.append("".join(dots))

# central bar and bulge
g.append(f'<ellipse cx="{CX}" cy="{CY}" rx="{R0 * 1.15:.0f}" ry="{R0 * .38:.0f}" transform="rotate({math.degrees(BAR):.0f} {CX} {CY})" fill="url(#bu)" opacity=".9"/>')
g.append(f'<circle cx="{CX}" cy="{CY}" r="{R0 * .75:.0f}" fill="url(#bu)"/>')


def upright(x, y, body):
    """Content that travels with the galaxy but stays level, by turning back as fast as the galaxy turns."""
    return (f'<g transform="translate({num(x)} {num(y)})"><g style="animation:gr {SPIN}s linear infinite reverse">{body}</g></g>')


for i, name in NAMES.items():
    r = R * .9
    x, y = polar(r + 22, arm_angle(i, r))
    g.append(upright(x, y, f'<text text-anchor="middle" class="ar" {FONT} font-style="italic" font-size="14" fill="#c7d2fe" fill-opacity=".85">{name}</text>'))

sx, sy = polar(SUN_R, SUN_A)
g.append(upright(sx, sy, '<circle class="mv" r="9" fill="none" stroke="#fde68a" stroke-width="1.5" style="animation:ps 2.4s ease-out infinite"/>'
                         '<circle r="9" fill="url(#hl)"/><circle r="3.6" fill="#fde68a"/>'
                         f'<text x="14" y="5" class="yh" {FONT} font-size="17" fill="#fde68a">you are here</text>'))

o.append(f'<circle cx="{CX}" cy="{CY}" r="{SUN_R:.0f}" fill="none" stroke="#fde68a" stroke-opacity=".22" stroke-dasharray="2 6"/>')
o.append(f'<g style="transform-origin:{CX}px {CY}px;animation:gr {SPIN}s linear infinite">{"".join(g)}</g>')

# the supermassive black hole at the very centre
o.append(f'<circle cx="{CX}" cy="{CY}" r="5" fill="#05070f" stroke="#fde68a" stroke-opacity=".9" stroke-width="1.4"/>')
o.append(f'<text x="{CX}" y="{CY + 34}" text-anchor="middle" class="ar" {FONT} font-style="italic" font-size="15" fill="#fff7d6" '
         f'stroke="#1e1033" stroke-opacity=".75" stroke-width="3" paint-order="stroke">Sagittarius A*</text>')

# side view: a thin disc with a central bulge, and where the Sun sits in it
VX, VY, VW = 170, 380, 120
o.append(f'<text x="{VX}" y="{VY - 44}" text-anchor="middle" class="ar" {FONT} font-style="italic" font-size="15" fill="#c7d2fe">side view</text>')
o.append(f'<ellipse cx="{VX}" cy="{VY}" rx="{VW}" ry="5" fill="url(#eg)"/><ellipse cx="{VX}" cy="{VY}" rx="20" ry="13" fill="url(#bu)"/>')
o.append(f'<circle cx="{VX + VW * 26 / 50:.0f}" cy="{VY}" r="3.2" fill="#fde68a"/>'
         f'<line x1="{VX + VW * 26 / 50:.0f}" y1="{VY - 6}" x2="{VX + VW * 26 / 50:.0f}" y2="{VY - 22}" stroke="#fde68a" stroke-opacity=".7"/>')

# three facts
facts = [("100 000", "light-years across"), ("26 000", "light-years from the centre"), ("230 million", "years for one orbit"), ("≈ 20", "orbits since the Sun was born"),
         ("100–400 billion", "stars"), ("4.5 billion", "years until it merges with Andromeda")]
for n, (big, small) in enumerate(facts):
    y = 150 + n * 82
    o.append(f'<text x="1030" y="{y}" text-anchor="middle" class="ex" {FONT} font-size="24" fill="#fde68a">{big}</text>'
             f'<text x="1030" y="{y + 22}" text-anchor="middle" class="ex" {MONO} font-size="12" fill="{STAR}" fill-opacity=".6">{small}</text>')

write_svg(sys.argv[1], "Animated Milky Way seen from above, with its spiral arms, central bar and the Sun's position", defs, css, o)
