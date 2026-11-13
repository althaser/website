import math
import random
import sys

from common import DEFS, MONO, base_css, mobile, nebula, num, pt, stars, title, write_svg

random.seed(9)
SX, SY = 800, 365
V = 26.0
TAIL = 760
# oblique view: the Sun moves along D, an orbit is drawn with the screen vectors U (up) and W (towards the viewer)
D = (1, -.05)
U = (0, -.92)
W = (-.55, .3)

# name, distance (AU), period (years), colour, size
PLANETS = [("Mercury", .39, .24, "#c9c1b6", 2.8), ("Venus", .72, .62, "#f2cf86", 4.2), ("Earth", 1, 1, "#4aa8ff", 4.5),
           ("Mars", 1.52, 1.88, "#ef6b45", 3.6), ("Jupiter", 5.2, 11.86, "#e3a76f", 8.5), ("Saturn", 9.58, 29.46, "#eedc9f", 7.5),
           ("Uranus", 19.2, 84, "#86e7ec", 6), ("Neptune", 30, 164.8, "#5b7cff", 6)]
DX, DY = D


def orbit(r, a):
    """Screen offset of a planet at angle a on its orbit, and whether it is on the near side of the Sun."""
    c, s = math.cos(a), math.sin(a)
    return r * (c * U[0] + s * W[0]), r * (c * U[1] + s * W[1]), s


css = [
    "@keyframes fl{to{transform:translate(var(--x),var(--y))}}",
    ".h{fill:none;stroke-linecap:round;stroke-linejoin:round}",
    mobile(".ax{font-size:22px}"),
] + base_css()
defs = ["<defs>", *DEFS,
        '<radialGradient id="sun"><stop offset="0" stop-color="#fff7d6"/><stop offset=".35" stop-color="#ffd166"/><stop offset=".7" stop-color="#fb923c" stop-opacity=".35"/><stop offset="1" stop-color="#fb923c" stop-opacity="0"/></radialGradient>',
        f'<linearGradient id="tf" gradientUnits="userSpaceOnUse" x1="{SX - TAIL * .95}" y1="0" x2="{SX - TAIL * .45}" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff"/></linearGradient>',
        '<mask id="tm" maskUnits="userSpaceOnUse" x="0" y="0" width="1200" height="700"><rect width="1200" height="700" fill="url(#tf)"/></mask>',
        "</defs>"]
o = [nebula((430, 360), (820, 350), (420, 330), 280)]
o.extend(stars(100))

# the Sun's own path through the galaxy
o.append(f'<line x1="{SX}" y1="{SY}" x2="{num(SX + DX * 300)}" y2="{num(SY + DY * 300)}" stroke="#ffd166" stroke-opacity=".3" stroke-dasharray="3 7"/>')

back, front, planets = [], [], []
for n, (name, au, years, col, size) in enumerate(PLANETS):
    r = 22 + 27 * math.sqrt(au)
    period = 4.2 * years ** .25
    w = 2 * math.pi / period
    ph = 2.4 * n
    pitch = V * period
    per_turn = 48
    dt = period / per_turn

    def at(tau):
        """Where the trail point left `tau` seconds ago sits at the start of the cycle."""
        ox, oy, d = orbit(r, ph - w * tau)
        return SX - DX * V * tau + ox, SY - DY * V * tau + oy, d

    taus = [k * dt for k in range(-per_turn, int((TAIL / V + period) / dt) + 2)]
    pts = [at(t) for t in taus]
    flow = f"--x:{num(-DX * pitch)}px;--y:{num(-DY * pitch)}px;animation:fl {period:.3f}s linear infinite"
    layers = {True: [], False: []}
    last = {True: None, False: None}
    # segments ahead of the planet at the start of the cycle appear as it passes them and stay for the rest of the cycle
    for k in range(len(taus) - 1):
        a, b = pts[k], pts[k + 1]
        side = (a[2] + b[2]) / 2 > 0
        if taus[k] < 0:
            f = -taus[k + 1] / period * 100
            css.append(f"@keyframes r{n}_{k}{{0%,{f:.2f}%{{opacity:0}}{f + .01:.2f}%,100%{{opacity:1}}}}")
            layers[side].append(f'<path class="mv" d="M{pt(a[0], a[1])}L{pt(b[0], b[1])}" style="animation:r{n}_{k} {period:.3f}s linear infinite"/>')
        elif last[side] == k - 1 and isinstance(layers[side][-1], list):
            layers[side][-1].append(b)
        else:
            layers[side].append([a, b])
        last[side] = k
    for side, dest, op in ((False, back, .35), (True, front, .8)):
        body = "".join(p if isinstance(p, str) else '<path d="M' + "L".join(pt(q[0], q[1]) for q in p) + '"/>' for p in layers[side])
        dest.append(f'<g class="h" stroke="{col}" stroke-width="{1.2 + size / 8:.2f}" stroke-opacity="{op}" style="{flow}">{body}</g>')

    # the planet itself, going round the Sun
    steps = 60
    frames, hide = [], []
    for i in range(steps + 1):
        ox, oy, d = orbit(r, ph + w * period * i / steps)
        frames.append(f"{100 * i / steps:.2f}%{{transform:translate({num(SX + ox)}px,{num(SY + oy)}px);opacity:{1 if d > 0 or math.hypot(ox, oy) > 26 else 0}}}")
    css.append(f"@keyframes p{n}{{{''.join(frames)}}}")
    ox, oy, _ = orbit(r, ph)
    ring = f'<ellipse rx="{size * 2.1:.1f}" ry="{size * .7:.1f}" transform="rotate(-18)" fill="none" stroke="{col}" stroke-opacity=".8" stroke-width="1.4"/>' if name == "Saturn" else ""
    planets.append(f'<g transform="translate({num(SX + ox)} {num(SY + oy)})" style="animation:p{n} {period:.3f}s linear infinite">'
                   f'<circle r="{size * 2.6:.1f}" fill="url(#hl)"/><circle r="{size}" fill="{col}"/>{ring}</g>')

o.append(f'<g mask="url(#tm)">{"".join(back)}</g>')
o.append(f'<line x1="{num(SX - DX * TAIL)}" y1="{num(SY - DY * TAIL)}" x2="{SX}" y2="{SY}" stroke="#ffd166" stroke-opacity=".55" stroke-width="2" mask="url(#tm)"/>')
o.append(f'<circle cx="{SX}" cy="{SY}" r="70" fill="url(#sun)"/><circle cx="{SX}" cy="{SY}" r="17" fill="#fff4cc"/>')
o.append(f'<g mask="url(#tm)">{"".join(front)}</g>')
o.extend(planets)

o.append(title(600, 66, "the Sun’s path through the galaxy"))
o.append(f'<text x="{num(SX + DX * 300)}" y="{num(SY + DY * 300 - 12)}" text-anchor="end" class="ax" {MONO} font-size="13" fill="#ffd166" fill-opacity=".8">≈ 230 km/s</text>')
gap = 1040 / len(PLANETS)
for n, (name, *_, col, size) in enumerate(PLANETS):
    cx = 80 + gap * (n + .5)
    o.append(f'<circle cx="{num(cx - 34)}" cy="642" r="4" fill="{col}"/>'
             f'<text x="{num(cx - 24)}" y="646" class="ax" {MONO} font-size="13" fill="{col}">{name}</text>')

write_svg(sys.argv[1], "Animated solar system moving through space, the planets tracing helices around the Sun's path", defs, css, o)
