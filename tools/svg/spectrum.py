import math
import random
import sys

from common import DEFS, FONT, MONO, STAR, base_css, mobile, nebula, num, palette, poly, stars, title, write_svg

random.seed(17)
X0, X1 = 70, 1130
LMAX, LMIN = 4, -13
WY, AMP = 322, 24
AXY, FQY = 526, 458
V = 40.0
ZX0, ZX1, ZY = 300, 900, 184

# name, longest and shortest wavelength (log10 m), drawn wavelength (px), example
BANDS = [("radio", 4, 0, 120, "radio · TV"), ("microwave", 0, -3, 62, "Wi-Fi · ovens"), ("infrared", -3, -6.15, 32, "heat · remotes"),
         ("visible", -6.15, -6.4, 0, "our eyes"), ("ultraviolet", -6.4, -8, 16, "sunburn"), ("X-ray", -8, -11, 9, "medical scans"),
         ("gamma", -11, -13, 5, "nuclear decay")]
# frequency range of each band, matching its wavelength limits above
FREQ = {"radio": "30 kHz–300 MHz", "microwave": "300 MHz–300 GHz", "infrared": "300 GHz–430 THz", "visible": "430–750 THz",
        "ultraviolet": "750 THz–30 PHz", "X-ray": "30 PHz–30 EHz", "gamma": "> 30 EHz"}
RAINBOW = ["#ef4444", "#f97316", "#facc15", "#4ade80", "#22d3ee", "#3b82f6", "#8b5cf6"]


def x(log_l):
    return X0 + (LMAX - log_l) / (LMAX - LMIN) * (X1 - X0)


def colour(n):
    return palette(1 - n / (len(BANDS) - 1))


css = [
    "@keyframes wv{to{transform:translateX(var(--d))}}",
    ".c{fill:none;stroke-linecap:round;stroke-linejoin:round}",
    mobile(".ax{font-size:22px}.bn{font-size:26px}.ex{display:none}"),
] + base_css()
defs = ["<defs>", *DEFS,
        '<linearGradient id="rb" x1="0" x2="1">' + "".join(f'<stop offset="{i / (len(RAINBOW) - 1):.2f}" stop-color="{c}"/>' for i, c in enumerate(RAINBOW)) + "</linearGradient>",
        '<linearGradient id="fade" x1="0" x2="0" y1="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity=".25"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>']
o = [nebula((380, 380), (820, 360), (340, 340), 260)]
o.extend(stars(80))
o.append(title(600, 66, "the electromagnetic spectrum"))

# bands: each wave moves at the same speed (light speed) but with its own wavelength
for n, (name, a, b, lam, example) in enumerate(BANDS):
    xa, xb = x(a), x(b)
    c = colour(n)
    defs.append(f'<clipPath id="b{n}"><rect x="{num(xa)}" y="{WY - AMP - 6}" width="{num(xb - xa)}" height="{2 * AMP + 12}"/></clipPath>')
    if name == "visible":
        o.append(f'<rect x="{num(xa)}" y="{WY - AMP}" width="{num(xb - xa)}" height="{2 * AMP}" fill="url(#rb)"/>')
    else:
        o.append(f'<rect x="{num(xa)}" y="{WY - AMP - 6}" width="{num(xb - xa)}" height="{2 * AMP + 12}" fill="{c}" fill-opacity=".06"/>')
        pts = [(t / 4, WY - AMP * math.sin(2 * math.pi * t / 4 / lam)) for t in range(int((xb - xa + lam) * 4) + 1)]
        wave = poly((xa - lam + px, py) for px, py in pts)
        o.append(f'<g clip-path="url(#b{n})"><g style="--d:{lam}px;animation:wv {lam / V:.3f}s linear infinite">'
                 f'<path class="c" d="{wave}" stroke="{c}" stroke-width="2.2"/></g></g>')
    if n:
        o.append(f'<line x1="{num(xa)}" y1="{WY - AMP - 12}" x2="{num(xa)}" y2="{WY + AMP + 12}" stroke="{STAR}" stroke-opacity=".18"/>')
    if name == "visible":
        continue
    mid = (xa + xb) / 2
    o.append(f'<text x="{num(mid)}" y="{WY + AMP + 40}" text-anchor="middle" class="bn" {FONT} font-size="18" fill="{c}">{name}</text>')
    o.append(f'<text x="{num(mid)}" y="{WY + AMP + 60}" text-anchor="middle" class="ex" {MONO} font-size="12" fill="{STAR}" fill-opacity=".55">{example}</text>')
    o.append(f'<text x="{num(mid)}" y="{WY + AMP + 78}" text-anchor="middle" class="ex" {MONO} font-size="12" fill="{c}" fill-opacity=".85">{FREQ[name]}</text>')

# wavelength and frequency scales
o.append(f'<line x1="{X0}" y1="{AXY}" x2="{X1}" y2="{AXY}" stroke="{STAR}" stroke-opacity=".35"/>'
         f'<line x1="{X0}" y1="{FQY}" x2="{X1}" y2="{FQY}" stroke="{STAR}" stroke-opacity=".35"/>')
TICKS = [(3, "1 km", "300 kHz"), (0, "1 m", "300 MHz"), (-3, "1 mm", "300 GHz"), (-6, "1 µm", "300 THz"), (-9, "1 nm", "300 PHz"), (-12, "1 pm", "300 EHz")]
for lg, wl, fq in TICKS:
    tx = num(x(lg))
    o.append(f'<line x1="{tx}" y1="{AXY - 5}" x2="{tx}" y2="{AXY + 5}" stroke="{STAR}" stroke-opacity=".5"/>'
             f'<line x1="{tx}" y1="{FQY - 5}" x2="{tx}" y2="{FQY + 5}" stroke="{STAR}" stroke-opacity=".5"/>'
             f'<text x="{tx}" y="{AXY + 22}" text-anchor="middle" class="ax" {MONO} font-size="13" fill="#fde68a" fill-opacity=".85">{wl}</text>'
             f'<text x="{tx}" y="{FQY + 22}" text-anchor="middle" class="ax" {MONO} font-size="13" fill="#a5f3fc" fill-opacity=".85">{fq}</text>')
# the visible slice marked on both scales, just right of 1 µm
for y in (AXY, FQY):
    o.append(f'<rect x="{num(x(BANDS[3][1]))}" y="{y - 4}" width="{num(x(BANDS[3][2]) - x(BANDS[3][1]))}" height="8" rx="1" fill="url(#rb)"/>')
o.append(f'<text x="{X0}" y="{AXY - 12}" class="ax" {MONO} font-size="13" fill="#fde68a" fill-opacity=".6">wavelength</text>'
         f'<text x="{X0}" y="{FQY - 12}" class="ax" {MONO} font-size="13" fill="#a5f3fc" fill-opacity=".6">frequency</text>')

# the visible slice, magnified
va, vb = x(BANDS[3][1]), x(BANDS[3][2])
o.append(f'<path d="M{num(va)} {WY - AMP}L{ZX0} {ZY + 34}M{num(vb)} {WY - AMP}L{ZX1} {ZY + 34}" stroke="{STAR}" stroke-opacity=".25" stroke-dasharray="3 5"/>')
o.append(f'<path d="M{num(va)} {WY - AMP}L{num(vb)} {WY - AMP}L{ZX1} {ZY + 34}L{ZX0} {ZY + 34}Z" fill="url(#fade)" opacity=".35"/>')
o.append(f'<rect x="{ZX0}" y="{ZY - 30}" width="{ZX1 - ZX0}" height="60" rx="6" fill="url(#rb)"/>')
o.append(f'<text x="{(ZX0 + ZX1) / 2}" y="{ZY + 7}" text-anchor="middle" class="bn" {FONT} font-size="20" fill="#0b1023">visible light · {BANDS[3][4]}</text>')
chirp, phase, px = [], 0.0, ZX0
while px <= ZX1:
    lam = 70 - 30 * (px - ZX0) / (ZX1 - ZX0)
    chirp.append((px, ZY - 56 - 12 * math.sin(phase)))
    phase += 2 * math.pi * 2 / lam
    px += 2
o.append(f'<path class="c" d="{poly(chirp)}" stroke="url(#rb)" stroke-width="2"/>')
o.append(f'<text x="{(ZX0 + ZX1) / 2}" y="{ZY + 52}" text-anchor="middle" class="ax" {MONO} font-size="13" fill="{STAR}" fill-opacity=".75">{FREQ["visible"]}</text>')
# the zoom's own scale sits inside the bar, so it is not read against the axes below
o.append(f'<text x="{ZX0 + 12}" y="{ZY + 5}" class="ax" {MONO} font-size="13" font-weight="600" fill="#0b1023">700 nm</text>'
         f'<text x="{ZX1 - 12}" y="{ZY + 5}" text-anchor="end" class="ax" {MONO} font-size="13" font-weight="600" fill="#0b1023">400 nm</text>')

# energy direction
o.append(f'<text x="{X0}" y="628" class="ax" {MONO} font-size="13" fill="{STAR}" fill-opacity=".6">← longer waves · lower energy</text>'
         f'<text x="{X1}" y="628" text-anchor="end" class="ax" {MONO} font-size="13" fill="{STAR}" fill-opacity=".6">shorter waves · higher energy →</text>')

defs.append("</defs>")
write_svg(sys.argv[1], "Animated electromagnetic spectrum from radio waves to gamma rays, with wavelengths, frequencies and the visible colours", defs, css, o)
