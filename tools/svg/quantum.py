import math
import random
import sys

from common import DEFS, PALETTE, STAR, base_css, nebula, palette, save, stars, svg_open

random.seed(4)
NQ = 8
WY = [140 + 60 * q for q in range(NQ)]
X0, X1 = 190, 900
TRAV, PER = 4.0, 2.0
V = (X1 - X0) / TRAV
HT = 16.0
P1 = [.15, .5, .85, .3, .65, .5, .9, .25]
COLS = [270, 350, 430, 510, 590, 670, 750, 830]
CYAN, ORANGE = PALETTE[0], PALETTE[-1]


def arrival(x):
    """Animation delay so an element flashes when the wave packet reaches x."""
    return (x - X0) / V - 12


css = [
    f"@keyframes mv{{0%{{transform:translateX(0);opacity:0}}6%,94%{{opacity:1}}100%{{transform:translateX({X1 - X0}px);opacity:0}}}}",
    "@keyframes fl{0%{opacity:1}25%{opacity:.25}60%,100%{opacity:.06}}",
    "@keyframes sp{to{transform:rotate(360deg)}}",
    "@keyframes rp{0%{transform:scale(.2);opacity:0}20%{opacity:.5}100%{transform:scale(1.6);opacity:0}}",
    "@keyframes bit{0%,49.9%{opacity:1}50%,100%{opacity:0}}",
    "@keyframes nd{0%{transform:rotate(-40deg)}10%{transform:rotate(32deg)}24%{transform:rotate(-12deg)}40%,100%{transform:rotate(-40deg)}}",
    ".hb{transform-box:fill-box;transform-origin:0 50%}",
    ".rp{transform-box:fill-box;transform-origin:center}",
] + base_css(None)

# wave packet with a gaussian envelope
pts = []
for k in range(61):
    x = k * 1.5 - 45
    pts.append(f"{x:.1f} {-9 * math.exp(-(x / 18) ** 2) * math.sin(x / 3.2):.1f}")
stops = "".join(f'<stop offset="{k / (len(PALETTE) - 1):.2f}" stop-color="{c}"/>' for k, c in enumerate(PALETTE))
defs = ["<defs>", *DEFS,
        f'<linearGradient id="wg" gradientUnits="userSpaceOnUse" x1="{X0}" x2="{X1}" y1="0" y2="0">{stops}</linearGradient>',
        f'<path id="pk" d="M{" L".join(pts)}" fill="none" stroke-width="2" stroke-linecap="round"/>',
        "</defs>"]

o = [nebula((430, 350), (790, 350), (340, 340), 270)]
o.extend(stars(90))

# interference ripples
for cx, c in ((440, "#818cf8"), (770, "#e879f9")):
    for k in range(4):
        o.append(f'<circle class="rp" cx="{cx}" cy="350" r="190" fill="none" stroke="{c}" stroke-width="1" style="animation:rp 8s linear {-k * 2}s infinite"/>')

# wires with travelling wave packets
for y in WY:
    o.append(f'<line x1="{X0 - 40}" y1="{y}" x2="{X1 + 40}" y2="{y}" stroke="url(#wg)" stroke-opacity=".45" stroke-width="1.3"/>')
for y in WY:
    for k in range(int(TRAV / PER)):
        o.append(f'<use href="#pk" x="{X0}" y="{y}" stroke="#fff" style="animation:mv {TRAV}s linear {-k * PER - 12:.2f}s infinite"/>')

# gates: CNOTs with entanglement arcs, plus single-qubit gates
gates = []
for gx in COLS:
    used = set()
    c = palette((gx - X0) / (X1 - X0))
    dl = arrival(gx)
    for _ in range(random.choice([0, 1, 1, 2])):
        if len(used) >= NQ - 2:
            continue
        a, b = random.sample([q for q in range(NQ) if q not in used], 2)
        if abs(a - b) > 4:
            continue
        used |= {a, b}
        y1, y2 = WY[a], WY[b]
        top, bot = min(y1, y2), max(y1, y2)
        off = 18 + 8 * abs(a - b)
        o.append(f'<line x1="{gx}" y1="{y1}" x2="{gx}" y2="{y2}" stroke="{c}" stroke-width="1.6" stroke-opacity=".7"/>')
        o.append(f'<circle cx="{gx}" cy="{y1}" r="5" fill="{c}"/>')
        o.append(f'<circle cx="{gx}" cy="{y2}" r="11" fill="#0b1023" stroke="{c}" stroke-width="1.6"/><path d="M{gx - 11} {y2}h22M{gx} {y2 - 11}v22" stroke="{c}" stroke-width="1.6"/>')
        o.append(f'<path d="M{gx} {top} C{gx + off} {top} {gx + off} {bot} {gx} {bot}" fill="none" stroke="#fff" stroke-width="2" stroke-opacity=".9" style="animation:fl {PER}s {dl:.2f}s infinite"/>')
        o.append(f'<path d="M{gx} {top} C{gx - off} {top} {gx - off} {bot} {gx} {bot}" fill="none" stroke="{c}" stroke-width="2" style="animation:fl {PER}s {dl:.2f}s infinite"/>')
        gates += [(gx, y1, dl), (gx, y2, dl)]
    for q in range(NQ):
        if q in used or random.random() < .35:
            continue
        y = WY[q]
        g = random.choice(["H", "H", "X", "Rz", "Ry", "√X", "T"])
        o.append(f'<rect x="{gx - 16}" y="{y - 16}" width="32" height="32" rx="7" fill="#0b1023" stroke="{c}" stroke-width="1.5"/>')
        o.append(f'<text x="{gx}" y="{y + 5}" text-anchor="middle" font-family="Segoe UI,Helvetica,Arial,sans-serif" font-size="{13 if len(g) > 1 else 15}" font-weight="600" fill="{c}">{g}</text>')
        gates.append((gx, y, dl))
for gx, y, dl in gates:
    o.append(f'<circle cx="{gx}" cy="{y}" r="30" fill="url(#hl)" style="animation:fl {PER}s {dl:.2f}s infinite"/>')

# Bloch spheres starting in |0>
for y in WY:
    cx = 105
    ang = math.radians(random.uniform(25, 70))
    ex, ey = cx + 18 * math.sin(ang), y - 18 * math.cos(ang)
    sp = random.uniform(2.5, 6) * random.choice([1, -1])
    direction = ";animation-direction:reverse" if sp < 0 else ""
    o.append(f'<circle cx="{cx}" cy="{y}" r="20" fill="#0b1023" stroke="{CYAN}" stroke-opacity=".7" stroke-width="1.2"/>')
    o.append(f'<ellipse cx="{cx}" cy="{y}" rx="20" ry="6" fill="none" stroke="{CYAN}" stroke-opacity=".35"/>')
    o.append(f'<line x1="{cx}" y1="{y - 20}" x2="{cx}" y2="{y + 20}" stroke="{CYAN}" stroke-opacity=".2"/>')
    o.append(f'<g style="transform-origin:{cx}px {y}px;animation:sp {abs(sp):.1f}s linear infinite{direction}"><line x1="{cx}" y1="{y}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="#fff" stroke-width="1.6"/><circle cx="{ex:.1f}" cy="{ey:.1f}" r="3" fill="{CYAN}"/></g>')
    o.append(f'<circle cx="{cx}" cy="{y}" r="2" fill="#fff"/>')
    o.append(f'<text x="{cx - 34}" y="{y + 5}" text-anchor="end" font-family="Consolas,monospace" font-size="14" fill="#67e8f9" fill-opacity=".85">|0</text><path d="M{cx - 33} {y - 7}l4 7-4 7" fill="none" stroke="#67e8f9" stroke-opacity=".85" stroke-width="1.3" stroke-linejoin="round"/>')

# measurement: the needle swings on collapse, one bit per shot, and a histogram of shots
mx = X1 + 50
for q, y in enumerate(WY):
    dl = arrival(mx)
    o.append(f'<rect x="{mx - 18}" y="{y - 15}" width="36" height="30" rx="6" fill="#0b1023" stroke="{ORANGE}" stroke-width="1.4"/>')
    o.append(f'<path d="M{mx - 11} {y + 6} A11 11 0 0 1 {mx + 11} {y + 6}" fill="none" stroke="{ORANGE}" stroke-width="1.4"/>')
    o.append(f'<line x1="{mx}" y1="{y + 6}" x2="{mx}" y2="{y - 7}" stroke="{ORANGE}" stroke-width="1.6" stroke-linecap="round" style="transform-origin:{mx}px {y + 6}px;animation:nd {PER}s {dl:.2f}s infinite"/>')
    o.append(f'<circle cx="{mx}" cy="{y}" r="22" fill="url(#hl)" style="animation:fl {PER}s {dl:.2f}s infinite"/>')
    bx = mx + 34
    p = random.choice([PER * 2, PER * 3, PER * 4])
    d = dl - random.randrange(4) * PER
    o.append(f'<text x="{bx}" y="{y + 5}" text-anchor="middle" font-family="Consolas,monospace" font-size="14" fill="{ORANGE}" style="animation:bit {p}s steps(1) {d:.2f}s infinite">1</text>'
             f'<text x="{bx}" y="{y + 5}" text-anchor="middle" font-family="Consolas,monospace" font-size="14" fill="#67e8f9" style="animation:bit {p}s steps(1) {d - p / 2:.2f}s infinite">0</text>')
    hx0, hw = bx + 18, 110
    shots = int(HT / PER)
    ones = 0
    frames = ["0%{transform:scaleX(.5)}"]
    for k in range(1, shots + 1):
        ones += random.random() < P1[q]
        est = (ones + 1) / (k + 2) * .5 + P1[q] * .5 * k / shots
        frames.append(f"{k / shots * 94:.1f}%{{transform:scaleX({est:.3f})}}")
    frames.append(f"97%{{transform:scaleX({P1[q]})}}100%{{transform:scaleX(.5)}}")
    css.append(f'@keyframes h{q}{{{"".join(frames)}}}')
    o.append(f'<rect x="{hx0}" y="{y - 6}" width="{hw}" height="12" rx="3" fill="{CYAN}" fill-opacity=".55"/>')
    o.append(f'<rect class="hb" x="{hx0}" y="{y - 6}" width="{hw}" height="12" rx="3" fill="{ORANGE}" style="animation:h{q} {HT}s ease-in-out infinite"/>')
    o.append(f'<line x1="{hx0 + hw / 2}" y1="{y - 9}" x2="{hx0 + hw / 2}" y2="{y + 9}" stroke="{STAR}" stroke-opacity=".35" stroke-dasharray="2 2"/>')

save(sys.argv[1], [svg_open("Animated quantum circuit", x=-17), *defs, "<style>" + "".join(css) + "</style>", *o, "</svg>"])
