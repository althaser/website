import math
import random
import sys

from common import DEFS, FONT, MONO, PALETTE, STAR, base_css, mobile, nebula, num, palette, poly, stars, title, write_svg

random.seed(11)
T = 26.0
SCAN = .92
TMAX = 52.0
ZEROS = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062, 37.586178, 40.918719, 43.327073, 48.005151, 49.773832]
CYAN, ORANGE = PALETTE[0], PALETTE[-1]

SX0, SX1, SY0, SY1 = 92, 292, 620, 90
LX = (SX0 + SX1) / 2
ZOX, ZOY, ZS = 507, 365, 94
PX0, PX1, PY0, PY1, PXMAX, PYMAX = 877, 1117, 513, 228, 40, 42
BERN = [1 / 6, -1 / 30, 1 / 42, -1 / 30, 5 / 66, -691 / 2730, 7 / 6]


def zeta(s, n=30):
    """Riemann zeta via Euler-Maclaurin summation, accurate for |Im s| < 60."""
    total = sum(k ** -s for k in range(1, n)) + n ** (1 - s) / (s - 1) + n ** -s / 2
    fact, term = 2, s
    for k, b in enumerate(BERN, 1):
        total += b / fact * term * n ** (-s - 2 * k + 1)
        term *= (s + 2 * k - 1) * (s + 2 * k)
        fact *= (2 * k + 1) * (2 * k + 2)
    return total


def when(t):
    """Cycle time at which the scan reaches height t, as a negative delay."""
    return t / TMAX * SCAN * T - T


def pct(t):
    return t / TMAX * SCAN * 100


def sy(t):
    return SY0 - (SY0 - SY1) * t / TMAX


def zp(z):
    return ZOX + ZS * z.real, ZOY - ZS * z.imag


def px(x):
    return PX0 + (PX1 - PX0) * x / PXMAX


def py(v):
    return PY0 - (PY0 - PY1) * v / PYMAX


def psi_approx(x, k):
    """Explicit formula for Chebyshev's psi(x) using the first k pairs of zeros."""
    v = x - math.log(2 * math.pi) - .5 * math.log(1 - x ** -2)
    for g in ZEROS[:k]:
        rho = complex(.5, g)
        v -= 2 * (x ** rho / rho).real
    return v


def von_mangoldt(n):
    for p in range(2, n + 1):
        if n % p == 0:
            while n % p == 0:
                n //= p
            return math.log(p) if n == 1 else 0
    return 0


css = [
    f"@keyframes sc{{0%{{transform:translateY(0);opacity:1}}{SCAN * 100:.0f}%{{transform:translateY({SY1 - SY0}px);opacity:1}}{SCAN * 100 + 3:.0f}%,100%{{transform:translateY({SY1 - SY0}px);opacity:0}}}}",
    "@keyframes tr{0%{opacity:1}7%,100%{opacity:0}}",
    "@keyframes fl{0%{opacity:1}5%{opacity:.25}11%,100%{opacity:0}}",
    "@keyframes rp{0%{transform:scale(.2);opacity:.9}12%,100%{transform:scale(2.2);opacity:0}}",
    ".rp{transform-box:fill-box;transform-origin:center}",
    ".c{fill:none;stroke-linecap:round;stroke-linejoin:round}",
    f".t{{stroke-width:3;stroke-linecap:butt;animation:tr {T}s linear infinite}}",
    f".f{{animation:fl {T}s infinite}}",
    mobile(".ax{font-size:22px}.ct{font-size:24px}.zv{display:none}.ri{font-size:30px}"),
] + base_css()

ys = [sy(0), sy(TMAX)]
defs = ["<defs>", *DEFS,
        f'<linearGradient id="cl" gradientUnits="userSpaceOnUse" x1="0" x2="0" y1="{ys[0]}" y2="{ys[1]}">'
        + "".join(f'<stop offset="{k / (len(PALETTE) - 1):.2f}" stop-color="{c}"/>' for k, c in enumerate(PALETTE)) + "</linearGradient>",
        f'<linearGradient id="st" x1="0" x2="1"><stop offset="0" stop-color="#6366f1" stop-opacity=".05"/><stop offset=".5" stop-color="#8b5cf6" stop-opacity=".22"/><stop offset="1" stop-color="#6366f1" stop-opacity=".05"/></linearGradient>',
        f'<clipPath id="pc"><rect x="{PX0}" y="{PY1 - 10}" width="{PX1 - PX0 + 10}" height="{PY0 - PY1 + 10}"/></clipPath>',
        "</defs>"]

o = [nebula((392, 350), (832, 350), (380, 360), 270)]
o.extend(stars(90))

# critical strip 0 < Re(s) < 1 with the critical line and the first ten zeros on it
o.append(f'<rect x="{SX0}" y="{SY1 - 10}" width="{SX1 - SX0}" height="{SY0 - SY1 + 10}" fill="url(#st)" stroke="#818cf8" stroke-opacity=".35" stroke-dasharray="3 4"/>')
for t in range(10, 51, 10):
    o.append(f'<line x1="{SX0 - 6}" y1="{sy(t):.1f}" x2="{SX0}" y2="{sy(t):.1f}" stroke="{STAR}" stroke-opacity=".4"/>'
             f'<text x="{SX0 - 10}" y="{sy(t) + 4:.1f}" text-anchor="end" class="zv" {MONO} font-size="12" fill="{STAR}" fill-opacity=".5">{t}i</text>')
o.append(f'<line x1="{SX0 - 20}" y1="{SY0}" x2="{SX1 + 20}" y2="{SY0}" stroke="{STAR}" stroke-opacity=".35"/>')
for x, label in ((SX0, "0"), (LX, "½"), (SX1, "1")):
    o.append(f'<text x="{x}" y="{SY0 + 22}" text-anchor="middle" class="ax" {MONO} font-size="14" fill="{STAR}" fill-opacity=".7">{label}</text>')
o.append(f'<line x1="{LX}" y1="{SY0}" x2="{LX}" y2="{SY1 - 10}" stroke="url(#cl)" stroke-width="2"/>')
o.append(title(LX, SY1 - 24, "Re(s) = ½"))
o.append(f'<g class="mv" style="animation:sc {T}s linear infinite"><line x1="{SX0 - 4}" y1="{SY0}" x2="{SX1 + 4}" y2="{SY0}" stroke="#fff" stroke-opacity=".55"/>'
         f'<circle cx="{LX}" cy="{SY0}" r="16" fill="url(#hl)"/><circle cx="{LX}" cy="{SY0}" r="3.5" fill="#fff"/></g>')

# the curve t -> zeta(1/2 + it): a faint full trace, a comet trail and the moving point
o.append(f'<line x1="{ZOX - 1.75 * ZS:.0f}" y1="{ZOY}" x2="{ZOX + 3.8 * ZS:.0f}" y2="{ZOY}" stroke="{STAR}" stroke-opacity=".3"/>'
         f'<line x1="{ZOX}" y1="{ZOY - 2.6 * ZS:.0f}" x2="{ZOX}" y2="{ZOY + 2.6 * ZS:.0f}" stroke="{STAR}" stroke-opacity=".3"/>')
o.append(title(f"{ZOX + ZS:.0f}", SY1 - 24, "ζ(s) = ζ(½ + ti)"))
o.append(f'<text x="{ZOX + 3.8 * ZS - 4:.0f}" y="{ZOY - 9}" text-anchor="end" class="ri" {FONT} font-style="italic" font-size="17" fill="{STAR}" fill-opacity=".75">Re</text>'
         f'<text x="{ZOX + 9}" y="{ZOY - 2.6 * ZS + 14:.0f}" class="ri" {FONT} font-style="italic" font-size="17" fill="{STAR}" fill-opacity=".75">Im</text>')
o.append(f'<text x="{ZOX + ZS}" y="{ZOY + 21}" text-anchor="middle" class="ax" {MONO} font-size="13" fill="{STAR}" fill-opacity=".6">1</text>'
         f'<line x1="{ZOX + ZS}" y1="{ZOY - 4}" x2="{ZOX + ZS}" y2="{ZOY + 4}" stroke="{STAR}" stroke-opacity=".4"/>')
STEP, SUB = .05, 5
samples = [k * STEP for k in range(int(TMAX / STEP) + 1)]
pts = [zp(zeta(complex(.5, t))) for t in samples]
o.append(f'<path class="c" d="{poly(pts)}" stroke="{STAR}" stroke-opacity=".14" stroke-width="1.2"/>')
CHUNK = 10
for n, k in enumerate(range(0, len(pts) - 1, CHUNK)):
    end = min(k + CHUNK, len(pts) - 1)
    c = palette(samples[(k + end) // 2] / TMAX)
    a = min(pct(samples[end]), SCAN * 100 - .5)
    css.append(f"@keyframes c{n}{{0%,{a:.2f}%{{opacity:0}}{a + .4:.2f}%,{SCAN * 100:.0f}%{{opacity:1}}{SCAN * 100 + 3:.0f}%,100%{{opacity:0}}}}")
    defs.insert(-1, f'<path id="k{n}" d="{poly(pts[k:end + 1])}"/>')
    o.append(f'<g class="c" style="animation:c{n} {T}s linear infinite;stroke-linecap:butt" stroke="{c}"><use href="#k{n}" stroke-opacity=".18" stroke-width="6"/>'
             f'<use href="#k{n}" stroke-opacity=".8" stroke-width="1.8"/></g>')
o.append(f'<g style="animation:zo {T}s linear infinite">')
for k in range(SUB, len(pts), SUB):
    o.append(f'<path class="mv c t" d="{poly(pts[k - SUB:k + 1])}" stroke="{palette(samples[k] / TMAX)}" style="animation-delay:{when(samples[k - SUB]):.2f}s"/>')
o.append('</g>')
frames = [f"{pct(t):.2f}%{{transform:translate({num(x)}px,{num(y)}px)}}" for t, (x, y) in list(zip(samples, pts))[::4]]
frames.append(f"100%{{transform:translate({num(pts[-1][0])}px,{num(pts[-1][1])}px)}}")
css.append("@keyframes zp{" + "".join(frames) + "}")
css.append(f"@keyframes zo{{0%,{SCAN * 100:.0f}%{{opacity:1}}{SCAN * 100 + 3:.0f}%,100%{{opacity:0}}}}")
o.append(f'<g class="mv" style="animation:zo {T}s linear infinite"><g style="animation:zp {T}s linear infinite"><circle r="18" fill="url(#hl)"/><circle r="4" fill="#fff"/></g></g>')

# every zero flashes on the critical line and sends a ripple from the origin of the zeta plane
for j, g in enumerate(ZEROS):
    c = palette(g / TMAX)
    dl = when(g)
    o.append(f'<circle cx="{LX}" cy="{sy(g):.1f}" r="5" fill="#0b1023" stroke="{c}" stroke-width="2"/>')
    o.append(f'<circle cx="{LX}" cy="{sy(g):.1f}" r="26" fill="url(#hl)" class="mv f" style="animation-delay:{dl:.2f}s"/>')
    defs.insert(-1, f'<radialGradient id="g{j}"><stop offset="0" stop-color="{c}" stop-opacity=".7"/><stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient>')
    o.append(f'<ellipse cx="{PX0 + 52}" cy="{PY1 + 1}" rx="80" ry="26" fill="url(#g{j})" class="mv f" style="animation-delay:{dl:.2f}s"/>')
    o.append(f'<text x="{LX + 14}" y="{sy(g) + 4:.1f}" class="zv" {MONO} font-size="11" fill="{c}" fill-opacity=".8">{g:.2f}</text>')
    o.append(f'<circle class="rp" cx="{ZOX}" cy="{ZOY}" r="22" fill="none" stroke="{c}" stroke-width="1.6" opacity="0" style="animation:rp {T}s ease-out {dl:.2f}s infinite"/>')
o.append(f'<circle cx="{ZOX}" cy="{ZOY}" r="3" fill="#fff"/>')

# primes: Chebyshev psi(x) and the explicit formula sharpening as each zero is found
o.append(f'<line x1="{PX0}" y1="{PY0}" x2="{PX1 + 10}" y2="{PY0}" stroke="{STAR}" stroke-opacity=".35"/>'
         f'<line x1="{PX0}" y1="{PY0}" x2="{PX0}" y2="{PY1 - 10}" stroke="{STAR}" stroke-opacity=".35"/>')
o.append(f'<text x="{PX1 + 16}" y="{PY0 + 5}" class="ri" {FONT} font-style="italic" font-size="17" fill="{STAR}" fill-opacity=".75">x</text>'
         f'<text x="{PX0 - 8}" y="{PY1 + 2}" text-anchor="end" class="ri" {FONT} font-style="italic" font-size="17" fill="{STAR}" fill-opacity=".75">ψ</text>')
o.append(title((PX0 + PX1) / 2, PY1 - 44, "ψ(x) from the zeros"))
for x in range(10, PXMAX + 1, 10):
    o.append(f'<text x="{px(x):.1f}" y="{PY0 + 22}" text-anchor="middle" class="ax" {MONO} font-size="12" fill="{STAR}" fill-opacity=".5">{x}</text>')
for p in (n for n in range(2, PXMAX) if all(n % d for d in range(2, n))):
    o.append(f'<line x1="{px(p):.1f}" y1="{PY0}" x2="{px(p):.1f}" y2="{PY0 + 6}" stroke="{ORANGE}" stroke-opacity=".8" stroke-width="1.5"/>')
stair, v = [f"M{px(1):.1f} {py(0):.1f}"], 0
for n in range(2, PXMAX + 1):
    stair.append(f"H{px(n):.1f}")
    v += von_mangoldt(n)
    stair.append(f"V{py(v):.1f}")
o.append(f'<path d="{"".join(stair)}H{px(PXMAX):.1f}" fill="none" stroke="{STAR}" stroke-opacity=".45" stroke-width="1.4"/>')

bounds = [0, *ZEROS, TMAX]
xs = [math.exp(u * .02) for u in range(int(math.log(1.2) / .02), int(math.log(PXMAX) / .02) + 1)]
for k in range(len(ZEROS) + 1):
    a, b = pct(bounds[k]), pct(bounds[k + 1])
    fade = .6
    if k == 0:
        frames = f"0%{{opacity:1}}{b:.2f}%{{opacity:1}}{b + fade:.2f}%,{100 - fade:.2f}%{{opacity:0}}100%{{opacity:1}}"
    elif k == len(ZEROS):
        frames = f"0%,{a:.2f}%{{opacity:0}}{a + fade:.2f}%,{SCAN * 100:.0f}%{{opacity:1}}{SCAN * 100 + 3:.0f}%,100%{{opacity:0}}"
    else:
        frames = f"0%,{a:.2f}%{{opacity:0}}{a + fade:.2f}%,{b:.2f}%{{opacity:1}}{b + fade:.2f}%,100%{{opacity:0}}"
    css.append(f"@keyframes a{k}{{{frames}}}")
    c = palette(bounds[k] / TMAX) if k else CYAN
    d = poly((px(x), py(psi_approx(x, k))) for x in xs)
    o.append(f'<g class="mv" style="animation:a{k} {T}s linear infinite"><path class="c" d="{d}" stroke="{c}" stroke-width="2" clip-path="url(#pc)"/>'
             f'<text x="{PX0 + 8}" y="{PY1 + 6}" class="ct" {MONO} font-size="13" fill="{c}">{k} zero{"" if k == 1 else "s"}</text></g>')

write_svg(sys.argv[1], "Animated Riemann zeta zeros", defs, css, o)
