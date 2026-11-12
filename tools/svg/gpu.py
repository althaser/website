import random
import sys

random.seed(5)
W = 2.4
PX, PY, PW, PH = 330, 150, 540, 400
DX, DY, DW, DH = 360, 180, 480, 340
SMC, SMR = 6, 4
GAP = 10
L2H = 22
SMW = (DW - GAP * (SMC + 1)) / SMC
SMH = (DH - L2H - GAP * (SMR + 2)) / SMR
CORES = 4
COLS = ["#22d3ee", "#38bdf8", "#6366f1", "#8b5cf6", "#a855f7", "#e879f9"]
ORANGE = "#fb923c"

o = []
w = o.append
w('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -40 1200 700" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Animated GPU parallel computing">')
w("<defs>")
w('<radialGradient id="nb1"><stop offset="0" stop-color="#4338ca" stop-opacity=".42"/><stop offset="1" stop-color="#4338ca" stop-opacity="0"/></radialGradient>')
w('<radialGradient id="nb2"><stop offset="0" stop-color="#a21caf" stop-opacity=".36"/><stop offset="1" stop-color="#a21caf" stop-opacity="0"/></radialGradient>')
w('<radialGradient id="hl"><stop offset="0" stop-color="#fff" stop-opacity=".45"/><stop offset=".45" stop-color="#fff" stop-opacity=".12"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>')
w('<linearGradient id="l2" x1="0" x2="1"><stop offset="0" stop-color="#22d3ee" stop-opacity=".15"/><stop offset=".5" stop-color="#a5b4fc" stop-opacity=".55"/><stop offset="1" stop-color="#e879f9" stop-opacity=".15"/></linearGradient>')
w('<linearGradient id="hbm" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fdba74"/><stop offset="1" stop-color="#c2410c"/></linearGradient>')
w("</defs>")

css = [
    "@keyframes tw{0%,100%{opacity:.15}50%{opacity:.9}}",
    "@keyframes sm{0%,100%{opacity:.18}12%{opacity:1}40%{opacity:.35}}",
    "@keyframes c0{0%,100%{opacity:.25}50%{opacity:1}}",
    "@keyframes l2{0%,100%{opacity:.45}50%{opacity:1}}",
    "@keyframes dl{0%{transform:translateX(0);opacity:0}15%{opacity:1}85%{opacity:1}100%{transform:translateX(var(--d));opacity:0}}",
    "@keyframes out{0%{transform:translateY(0);opacity:0}20%{opacity:1}100%{transform:translateY(-110px);opacity:0}}",
    "@keyframes hb{0%,100%{opacity:.55}50%{opacity:1}}",
    "@keyframes glow{0%,100%{opacity:.35}50%{opacity:.8}}",
    "@media (prefers-reduced-motion:reduce){*{animation:none!important}.mv{opacity:0}}",
]
w("<style>" + "".join(css) + "</style>")

w('<ellipse cx="470" cy="350" rx="380" ry="260" fill="url(#nb1)"/><ellipse cx="760" cy="340" rx="360" ry="260" fill="url(#nb2)"/>')
for i in range(80):
    x, y = random.randint(10, 1190), random.randint(10, 690)
    if PX - 150 < x < PX + PW + 150 and PY - 40 < y < PY + PH + 30:
        continue
    r = random.choice([.7, 1, 1, 1.3])
    if i % 5 == 0:
        w(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#e0e7ff" style="animation:tw {random.uniform(3.5, 7):.1f}s -{random.uniform(0, 7):.1f}s infinite"/>')
    else:
        w(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#e0e7ff" opacity="{random.uniform(.15, .55):.2f}"/>')

# package with pins
pins = []
for i in range(26):
    x = PX + 14 + i * (PW - 28) / 25
    pins.append(f"M{x:.1f} {PY - 8}v8M{x:.1f} {PY + PH}v8")
for i in range(19):
    y = PY + 14 + i * (PH - 28) / 18
    pins.append(f"M{PX - 8} {y:.1f}h8M{PX + PW} {y:.1f}h8")
w(f'<path d="{"".join(pins)}" stroke="#a5b4fc" stroke-opacity=".35" stroke-width="2"/>')
w(f'<rect x="{PX}" y="{PY}" width="{PW}" height="{PH}" rx="18" fill="#0b1023" fill-opacity=".85" stroke="#818cf8" stroke-opacity=".45" stroke-width="1.5"/>')
w(f'<ellipse cx="{DX + DW / 2}" cy="{DY + DH / 2}" rx="{DW * .62}" ry="{DH * .62}" fill="url(#nb1)" style="animation:glow {W * 2}s infinite"/>')
w(f'<rect x="{DX}" y="{DY}" width="{DW}" height="{DH}" rx="10" fill="#0d1330" stroke="#a5b4fc" stroke-opacity=".5"/>')

# HBM stacks and buses
stacks = []
buses = []
packets = []
for side in (-1, 1):
    sx = PX - 120 if side < 0 else PX + PW + 60
    for k, sy in enumerate((DY + 8, DY + DH / 2 + 12)):
        sh = DH / 2 - 20
        for layer in range(5):
            stacks.append(f'<rect x="{sx + layer * 2}" y="{sy + layer * (sh / 5):.1f}" width="56" height="{sh / 5 - 4:.1f}" rx="3" fill="url(#hbm)" fill-opacity="{.35 + layer * .1:.2f}" stroke="#fdba74" stroke-opacity=".5"/>')
        x0 = sx + 60 if side < 0 else sx - 4
        x1 = PX - 4 if side < 0 else PX + PW + 4
        x1d = DX if side < 0 else DX + DW
        for lane in range(4):
            y = sy + 16 + lane * (sh - 32) / 3
            buses.append(f"M{x0:.0f} {y:.0f}H{x1d:.0f}")
            d = (x1d - x0)
            for n in range(2):
                delay = -random.uniform(0, 1.6)
                packets.append(f'<rect class="mv" x="{x0 - 5:.0f}" y="{y - 3:.0f}" width="10" height="6" rx="2" fill="{ORANGE}" style="--d:{d:.0f}px;animation:dl 1.6s linear {delay:.2f}s infinite"/>')
w(f'<path d="{"".join(buses)}" stroke="{ORANGE}" stroke-opacity=".22" stroke-width="1.5"/>')
w(f'<g style="animation:hb {W}s infinite">' + "".join(stacks) + "</g>")
w("".join(packets))

# L2 cache strip
l2y = DY + GAP + 2 * (SMH + GAP)
w(f'<rect x="{DX + GAP}" y="{l2y:.1f}" width="{DW - 2 * GAP}" height="{L2H}" rx="5" fill="url(#l2)" style="animation:l2 {W / 2}s infinite"/>')
cells = "".join(f"M{DX + GAP + 6 + i * 12} {l2y + 5:.1f}h8v{L2H - 10}h-8z" for i in range(int((DW - 2 * GAP - 12) / 12)))
w(f'<path d="{cells}" fill="#e0e7ff" fill-opacity=".18"/>')

# streaming multiprocessors
for r in range(SMR):
    for c in range(SMC):
        x = DX + GAP + c * (SMW + GAP)
        y = DY + GAP + r * (SMH + GAP) + (L2H + GAP if r >= 2 else 0)
        col = COLS[c]
        delay = (c + r) * W / (SMC + SMR)
        w(f'<rect x="{x:.1f}" y="{y:.1f}" width="{SMW:.1f}" height="{SMH:.1f}" rx="6" fill="#0b1023" stroke="{col}" stroke-opacity=".55"/>')
        cw = (SMW - 14) / CORES
        ch = (SMH - 14) / CORES
        phases = {}
        for i in range(CORES):
            for j in range(CORES):
                phases.setdefault(random.randrange(4), []).append(f"M{x + 7 + i * cw + 1:.1f} {y + 7 + j * ch + 1:.1f}h{cw - 3:.1f}v{ch - 3:.1f}h-{cw - 3:.1f}z")
        inner = "".join(f'<path d="{"".join(d)}" fill="{col}" style="animation:c0 {random.choice([.5, .6, .7, .8])}s {-p * .15:.2f}s infinite"/>' for p, d in phases.items())
        w(f'<g style="animation:sm {W}s {delay - W:.2f}s infinite" opacity=".18"><rect x="{x + 3:.1f}" y="{y + 3:.1f}" width="{SMW - 6:.1f}" height="{SMH - 6:.1f}" rx="4" fill="url(#hl)"/>{inner}</g>')

# results leaving through the top
for i in range(12):
    x = DX + 30 + i * (DW - 60) / 11
    col = COLS[min(5, i // 2)]
    w(f'<g class="mv" style="animation:out 2.2s ease-out {-random.uniform(0, 2.2):.2f}s infinite"><rect x="{x - 6:.0f}" y="{PY - 22}" width="12" height="12" rx="2" fill="none" stroke="{col}" stroke-width="1.5"/><rect x="{x - 2:.0f}" y="{PY - 18}" width="4" height="4" fill="{col}"/></g>')

w("</svg>")
open(sys.argv[1], "w").write("\n".join(o))
