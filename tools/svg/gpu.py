import random
import sys

from common import DEFS, MONO, base_css, mobile, nebula, stars, subtitle, title, write_svg

random.seed(5)
W = 2.4
PX, PY, PW, PH = 170, 185, 860, 380
DX, DY, DW, DH = 380, 215, 440, 320
SMC, SMR = 6, 4
GAP = 9
L2H = 20
SMW = (DW - GAP * (SMC + 1)) / SMC
SMH = (DH - L2H - GAP * (SMR + 2)) / SMR
L2Y = DY + GAP + 2 * (SMH + GAP)
CORES = 4
COLS = ["#22d3ee", "#38bdf8", "#6366f1", "#8b5cf6", "#a855f7", "#e879f9"]
ORANGE = "#fb923c"
HBW, HBH = 112, 80
HBX = [PX + 30, PX + PW - 30 - HBW]
HBY = [DY + 16, DY + DH - 16 - HBH - 10]
OUT_C, OUT_R, OUT_S = 18, 3, 16
OUT_X, OUT_Y = 600 - OUT_C * OUT_S / 2, 60

defs = ["<defs>"]
defs.extend(DEFS)
defs.append('<linearGradient id="l2" x1="0" x2="1"><stop offset="0" stop-color="#22d3ee" stop-opacity=".25"/><stop offset=".5" stop-color="#a5b4fc" stop-opacity=".6"/><stop offset="1" stop-color="#e879f9" stop-opacity=".25"/></linearGradient>')
defs.append('<linearGradient id="shine" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#e0e7ff" stop-opacity=".09"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>')
defs.append('<linearGradient id="sub" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#111a3f"/><stop offset="1" stop-color="#0a0f26"/></linearGradient>')
defs.append(f'<clipPath id="l2c"><rect x="{DX + GAP + 4}" y="{L2Y:.1f}" width="{DW - 2 * GAP - 8}" height="{L2H}"/></clipPath>')
defs.append(f'<clipPath id="dc"><rect x="{DX}" y="{DY}" width="{DW}" height="{DH}" rx="10"/></clipPath>')
defs.append("</defs>")

css = [
    "@keyframes sm{0%,100%{opacity:.15}12%{opacity:1}45%{opacity:.3}}",
    "@keyframes c0{0%,100%{opacity:.3}50%{opacity:1}}",
    "@keyframes ws{0%,100%{opacity:.2}10%,30%{opacity:1}}",
    "@keyframes l2f{to{transform:translateX(24px)}}",
    "@keyframes mv{0%{transform:translate(0,0);opacity:0}12%{opacity:1}88%{opacity:1}100%{transform:translate(var(--x),var(--y));opacity:0}}",
    "@keyframes led{0%,100%{opacity:.25}50%{opacity:1}}",
    "@keyframes glow{0%,100%{opacity:.35}50%{opacity:.8}}",
    "@keyframes sh{0%{transform:translateX(-200px)}100%{transform:translateX(" + str(DW + 200) + "px)}}",
    f"@keyframes oc{{0%,4%{{opacity:.08}}10%,78%{{opacity:1}}92%,100%{{opacity:.08}}}}",
    mobile(".lb{font-size:22px}.sl{display:none}"),
] + base_css()
kf = []
o = []
w = o.append

w(nebula((460, 360), (770, 350), (400, 380), 270))
o.extend(stars(90, (PX - 20, OUT_Y - 20, PX + PW + 20, PY + PH + 90)))
BODY = len(o)

# output matrix (C = A x B) filling above the chip
w(f'<rect x="{OUT_X - 10}" y="{OUT_Y - 10}" width="{OUT_C * OUT_S + 20}" height="{OUT_R * OUT_S + 20}" rx="8" fill="#0b1023" fill-opacity=".6" stroke="#818cf8" stroke-opacity=".35"/>')
cells = {}
for r in range(OUT_R):
    for c in range(OUT_C):
        col = COLS[min(5, c * 6 // OUT_C)]
        delay = (c * OUT_R + r) / (OUT_C * OUT_R) * 4.0
        cells.setdefault((col, round(delay, 1)), []).append(f"M{OUT_X + c * OUT_S + 2:.0f} {OUT_Y + r * OUT_S + 2:.0f}h{OUT_S - 4}v{OUT_S - 4}h-{OUT_S - 4}z")
for (col, d), paths in sorted(cells.items()):
    w(f'<path d="{"".join(paths)}" fill="{col}" style="animation:oc 4.8s {d - 4.8:.1f}s infinite"/>')

# package substrate, pins and PCIe edge
pins = []
for i in range(40):
    x = PX + 16 + i * (PW - 32) / 39
    pins.append(f"M{x:.1f} {PY - 7}v7")
for i in range(18):
    y = PY + 16 + i * (PH - 32) / 17
    pins.append(f"M{PX - 7} {y:.1f}h7M{PX + PW} {y:.1f}h7")
w(f'<path d="{"".join(pins)}" stroke="#a5b4fc" stroke-opacity=".3" stroke-width="2"/>')
w(f'<rect x="{PX}" y="{PY}" width="{PW}" height="{PH}" rx="20" fill="url(#sub)" stroke="#818cf8" stroke-opacity=".5" stroke-width="1.5"/>')
w(f'<rect x="{PX + 14}" y="{PY + 14}" width="{PW - 28}" height="{PH - 28}" rx="14" fill="none" stroke="#818cf8" stroke-opacity=".12"/>')
ex0, ex1 = 600 - 210, 600 + 210
fingers = "".join(f"M{ex0 + 8 + i * 14:.0f} {PY + PH + 6}v26" for i in range(30))
w(f'<rect x="{ex0}" y="{PY + PH}" width="{ex1 - ex0}" height="40" rx="6" fill="#0b1023" stroke="#818cf8" stroke-opacity=".4"/>')
w(f'<path d="{fingers}" stroke="#fbbf24" stroke-opacity=".45" stroke-width="4"/>')

# PCIe lanes into the die
lanes = []
for i in range(6):
    x = DX + 50 + i * (DW - 100) / 5
    lanes.append(f"M{x:.0f} {PY + PH + 4}V{DY + DH}")
    for k in range(2):
        w(f'<circle class="mv" cx="{x:.0f}" cy="{PY + PH + 4}" r="3" fill="#67e8f9" style="--x:0px;--y:{DY + DH - (PY + PH + 4)}px;animation:mv 1.1s linear {-random.uniform(0, 1.1):.2f}s infinite"/>')
w(f'<path d="{"".join(lanes)}" stroke="#22d3ee" stroke-opacity=".25" stroke-width="1.5"/>')

# die
w(f'<ellipse cx="{DX + DW / 2}" cy="{DY + DH / 2}" rx="{DW * .66}" ry="{DH * .66}" fill="url(#nb1)" style="animation:glow {W * 2}s infinite"/>')
w(f'<rect x="{DX - 6}" y="{DY - 6}" width="{DW + 12}" height="{DH + 12}" rx="14" fill="none" stroke="#a5b4fc" stroke-opacity=".18"/>')
w(f'<rect x="{DX}" y="{DY}" width="{DW}" height="{DH}" rx="10" fill="#0d1330" stroke="#a5b4fc" stroke-opacity=".6"/>')

# VRAM (HBM) stacks, drawn like the other panels: a dark rounded box with an orange outline, a name and its stacked layers
for side, hx in enumerate(HBX):
    for hy in HBY:
        layers = 4
        top = hy + 22
        lh = (HBH - 26) / layers
        w(f'<rect x="{hx}" y="{hy}" width="{HBW}" height="{HBH}" rx="10" fill="#0b1023" fill-opacity=".9" stroke="{ORANGE}" stroke-opacity=".75" stroke-width="1.4"/>')
        w(f'<text x="{hx + 12}" y="{hy + 15}" class="lb" {MONO} font-size="11" fill="#fed7aa" fill-opacity=".8">VRAM</text>')
        w(f'<path d="{"".join(f"M{hx + 8} {top + k * lh:.1f}h{HBW - 16}" for k in range(layers + 1))}" stroke="{ORANGE}" stroke-opacity=".25"/>')
        for k in range(layers):
            for j in range(5):
                w(f'<rect x="{hx + 14 + j * 18}" y="{top + k * lh + lh / 2 - 2:.1f}" width="9" height="4" rx="1.5" fill="{ORANGE}" style="animation:led {random.choice([.5, .7, .9])}s {-random.uniform(0, 1):.2f}s infinite"/>')
        # bus from stack to die edge then to L2 entry
        sx = hx + HBW if side == 0 else hx
        dx_edge = DX if side == 0 else DX + DW
        sy = hy + HBH / 2
        path = f"M{sx:.0f} {sy:.0f}H{(sx + dx_edge) / 2:.0f}V{L2Y + L2H / 2:.0f}H{dx_edge:.0f}"
        w(f'<path d="{path}" fill="none" stroke="{ORANGE}" stroke-opacity=".35" stroke-width="2.5" stroke-linejoin="round"/>')
        mx = (sx + dx_edge) / 2
        ly = L2Y + L2H / 2
        name = f"hb{side}{int(hy)}"
        seg = [abs(mx - sx), abs(ly - sy), abs(dx_edge - mx)]
        p1, p2 = seg[0] / sum(seg) * 100, (seg[0] + seg[1]) / sum(seg) * 100
        kf.append(f"@keyframes {name}{{0%{{transform:translate(0,0);opacity:0}}6%{{opacity:1}}{p1:.0f}%{{transform:translate({mx - sx:.0f}px,0)}}{p2:.0f}%{{transform:translate({mx - sx:.0f}px,{ly - sy:.0f}px)}}94%{{opacity:1}}100%{{transform:translate({dx_edge - sx:.0f}px,{ly - sy:.0f}px);opacity:0}}}}")
        for k in range(3):
            w(f'<circle class="mv" cx="{sx:.0f}" cy="{sy:.0f}" r="3.2" fill="{ORANGE}" style="animation:{name} 1.5s linear {-k * .5:.2f}s infinite"/>')

# inside the die
w('<g clip-path="url(#dc)">')
w(f'<rect x="{DX + GAP}" y="{L2Y:.1f}" width="{DW - 2 * GAP}" height="{L2H}" rx="5" fill="url(#l2)"/>')
w(f'<g clip-path="url(#l2c)"><path d="M{DX - 24} {L2Y + L2H / 2:.1f}H{DX + DW}" stroke="#fff" stroke-opacity=".7" stroke-width="3" stroke-dasharray="6 18" style="animation:l2f .6s linear infinite"/></g>')

for r in range(SMR):
    for c in range(SMC):
        x = DX + GAP + c * (SMW + GAP)
        y = DY + GAP + r * (SMH + GAP) + (L2H + GAP if r >= 2 else 0)
        col = COLS[c]
        delay = (c + r) * W / (SMC + SMR)
        w(f'<rect x="{x:.1f}" y="{y:.1f}" width="{SMW:.1f}" height="{SMH:.1f}" rx="6" fill="#0b1023" stroke="{col}" stroke-opacity=".6"/>')
        cw = (SMW - 12) / CORES
        ch = (SMH - 20) / CORES
        phases = {}
        for i in range(CORES):
            for j in range(CORES):
                phases.setdefault(random.randrange(4), []).append(f"M{x + 6 + i * cw + 1:.1f} {y + 14 + j * ch + 1:.1f}h{cw - 3:.1f}v{ch - 3:.1f}h-{cw - 3:.1f}z")
        inner = "".join(f'<path d="{"".join(d)}" fill="{col}" style="animation:c0 {random.choice([.45, .55, .65, .75])}s {-p * .15:.2f}s infinite"/>' for p, d in phases.items())
        sched = f'<rect x="{x + 6:.1f}" y="{y + 5:.1f}" width="{SMW - 12:.1f}" height="4" rx="2" fill="#fff" style="animation:ws {W}s {delay - W:.2f}s infinite"/>'
        w(f'<g style="animation:sm {W}s {delay - W:.2f}s infinite" opacity=".15"><rect x="{x + 3:.1f}" y="{y + 3:.1f}" width="{SMW - 6:.1f}" height="{SMH - 6:.1f}" rx="4" fill="url(#hl)"/>{inner}</g>{sched}')
        # L2 -> SM transfer
        if r in (1, 2):
            ty = L2Y if r == 1 else L2Y + L2H
            dy = (y + SMH - 4) - ty if r == 1 else (y + 4) - ty
            w(f'<circle class="mv" cx="{x + SMW / 2:.1f}" cy="{ty:.1f}" r="2.6" fill="#e0e7ff" style="--x:0px;--y:{dy:.0f}px;animation:mv .5s linear {-random.uniform(0, .5):.2f}s infinite"/>')

w(f'<rect x="{DX}" y="{DY}" width="160" height="{DH}" fill="url(#shine)" style="animation:sh 5s linear infinite"/>')
w("</g>")

# results streaming to the output matrix
for i in range(8):
    x = DX + 40 + i * (DW - 80) / 7
    tx = OUT_X + 20 + i * (OUT_C * OUT_S - 40) / 7
    col = COLS[min(5, i * 6 // 8)]
    w(f'<path d="M{x:.0f} {DY - 6}L{tx:.0f} {OUT_Y + OUT_R * OUT_S + 10}" fill="none" stroke="{col}" stroke-opacity=".22" stroke-width="1.4"/>')
    w(f'<circle class="mv" cx="{x:.0f}" cy="{DY - 6}" r="2.8" fill="{col}" style="--x:{tx - x:.0f}px;--y:{OUT_Y + OUT_R * OUT_S + 10 - (DY - 6):.0f}px;animation:mv .9s ease-in {-random.uniform(0, .9):.2f}s infinite"/>')

# labels
LB = f'{MONO} font-size="12" fill="#c7d2fe" fill-opacity=".7"'
o.append(f'<text x="{OUT_X - 18}" y="{OUT_Y + OUT_R * OUT_S / 2 + 4}" text-anchor="end" class="lb" {LB}>output</text>')
o.append(f'<text x="{PX + 24}" y="{PY + PH - 22}" class="sl" {LB}>GPU package</text>')
o.append(f'<g class="sl"><rect x="{DX + DW / 2 - 36}" y="{L2Y + 2:.1f}" width="72" height="{L2H - 4}" rx="4" fill="#0d1330"/>'
         f'<text x="{DX + DW / 2}" y="{L2Y + L2H / 2 + 4:.1f}" text-anchor="middle" {MONO} font-size="11" fill="#e0e7ff">L2 cache</text></g>')
o.append(f'<text x="{DX + 4}" y="{DY - 12}" class="sl" {LB}>streaming multiprocessors</text>')
o.append(f'<text x="{ex1 + 14}" y="{PY + PH + 25}" class="lb" {LB}>PCIe</text>')

# the drawing is laid out at 1:1 and then fitted below the title
ZOOM, TOP = .94, 120
Y0, Y1 = OUT_Y - 10, PY + PH + 40
o[BODY:] = [f'<g transform="translate(600 {TOP + ZOOM * (Y1 - Y0) / 2:.1f}) scale({ZOOM}) translate(-600 {-(Y0 + Y1) / 2:.1f})">', *o[BODY:], "</g>"]
o.append(title(600, 66, "thousands of cores in parallel"))
o.append(subtitle(600, 98, "an NVIDIA H100 has 16 896 cores working at the same time"))

write_svg(sys.argv[1], "Animated GPU parallel computing", defs, css + kf, o)
