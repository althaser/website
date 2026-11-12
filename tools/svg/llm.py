import random
import sys

random.seed(7)
STEP = 5.0
N = 4
T = STEP * N
SLOT = 96
CX = 600
X0 = CX - 4.5 * SLOT
XS = [CX + (i - 4.5) * SLOT for i in range(1, 9)]
X9 = CX + 4.5 * SLOT
ROW_Y = 600
LAYERS = [505, 425, 345, 265]
LCOL = ["#22d3ee", "#49b6f6", "#6366f1", "#a855f7"]
HEADS = ["#67e8f9", "#c4b5fd", "#fde68a"]
TOP = 245
BAR_BASE = 180
BAR_H = 92
ORANGE = "#fb923c"
NB = 31
BX0 = CX - (NB - 1) * 15 / 2
WINNERS = [19, 9, 24, 14]
TYPES = [("#22d3ee", 30, 20), ("#a78bfa", 18, 28), ("#f0abfc", 34, 12), ("#fdba74", 24, 24)]


def g(k, p):
    return (k + p / 100) / N * 100


def pct(x):
    return f"{x:.2f}%"


o = []
w = o.append
w('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 700" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Animated transformer language model">')
w("<defs>")
w('<radialGradient id="nb1"><stop offset="0" stop-color="#4338ca" stop-opacity=".42"/><stop offset="1" stop-color="#4338ca" stop-opacity="0"/></radialGradient>')
w('<radialGradient id="nb2"><stop offset="0" stop-color="#a21caf" stop-opacity=".36"/><stop offset="1" stop-color="#a21caf" stop-opacity="0"/></radialGradient>')
w('<radialGradient id="hl"><stop offset="0" stop-color="#fff" stop-opacity=".5"/><stop offset=".4" stop-color="#fff" stop-opacity=".15"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>')
w('<radialGradient id="ho"><stop offset="0" stop-color="#fb923c" stop-opacity=".55"/><stop offset="1" stop-color="#fb923c" stop-opacity="0"/></radialGradient>')
w('<linearGradient id="res" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#22d3ee"/><stop offset=".5" stop-color="#6366f1"/><stop offset="1" stop-color="#d946ef"/></linearGradient>')
for k, c in enumerate(LCOL):
    w(f'<linearGradient id="pl{k}" x1="0" x2="1"><stop offset="0" stop-color="{c}" stop-opacity="0"/><stop offset=".15" stop-color="{c}" stop-opacity=".10"/><stop offset=".85" stop-color="{c}" stop-opacity=".10"/><stop offset="1" stop-color="{c}" stop-opacity="0"/></linearGradient>')
w('<linearGradient id="fx" gradientUnits="userSpaceOnUse" x1="150" x2="1100" y1="0" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".1" stop-color="#fff"/><stop offset=".92" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>')
w('<mask id="rowFade" maskUnits="userSpaceOnUse" x="0" y="0" width="1200" height="700"><rect width="1200" height="700" fill="url(#fx)"/></mask>')
for t, (dot, l1, l2) in enumerate(TYPES):
    glyph = f'<path d="M-14 -4h{l1}M-14 5h{l2}" stroke-width="2.5" stroke-linecap="round"/><circle cx="-24" cy="0" r="3.5" fill="{dot}"/>'
    w(f'<g id="t{t}"><rect x="-34" y="-15" width="68" height="30" rx="7" fill="#0b1023" stroke="#22d3ee" stroke-width="1.5"/><g stroke="#67e8f9" stroke-opacity=".75">{glyph}</g></g>')
    w(f'<g id="o{t}"><rect x="-34" y="-15" width="68" height="30" rx="7" fill="#1c1020" stroke="{ORANGE}" stroke-width="1.8"/><g stroke="#fdba74">{glyph}</g></g>')
w("</defs>")

css = [
    ".fb{transform-box:fill-box;transform-origin:50% 100%}",
    "@keyframes tw{0%,100%{opacity:.15}50%{opacity:.9}}",
    "@keyframes up{0%{transform:translateY(0);opacity:0}3%{opacity:1}36%{transform:translateY(-345px);opacity:1}40%,100%{transform:translateY(-345px);opacity:0}}",
    "@keyframes sm{0%,37%{transform:translate(0,0);opacity:0}38%{opacity:1}45%{transform:translate(-336px,-52px);opacity:1}47%,100%{transform:translate(-336px,-52px);opacity:0}}",
    "@keyframes cur{0%{opacity:1}14%,82%{opacity:0}96%,100%{opacity:1}}",
    "@media (prefers-reduced-motion:reduce){*{animation:none!important}.mv{opacity:0}}",
]
for k, y in enumerate(LAYERS):
    p = 3 + (ROW_Y - 10 - y) / 345 * 33
    css.append(f"@keyframes n{k}{{0%,{p - 2:.1f}%{{opacity:.35}}{p:.1f}%{{opacity:1}}{p + 14:.1f}%,100%{{opacity:.35}}}}")
    for h in range(3):
        q = p + h * 1.5
        css.append(f"@keyframes a{k}{h}{{0%,{q:.1f}%{{opacity:.22}}{q + 2.5:.1f}%{{opacity:1}}{q + 16:.1f}%,100%{{opacity:.22}}}}")
    m = p + 6
    css.append(f"@keyframes m{k}{{0%,{m:.1f}%{{opacity:.25}}{m + 2:.1f}%{{opacity:1}}{m + 12:.1f}%,100%{{opacity:.25}}}}")

# per-step (global) keyframes
row = ["0%{transform:translateX(0)}"]
for k in range(N):
    row.append(f"{pct(g(k, 80))}{{transform:translateX({-k * SLOT}px)}}{pct(g(k, 95))}{{transform:translateX({-(k + 1) * SLOT}px)}}")
row.append(f"100%{{transform:translateX({-N * SLOT}px)}}")
css.append("@keyframes row{" + "".join(row) + "}")

w('<ellipse cx="450" cy="380" rx="360" ry="250" fill="url(#nb1)"/><ellipse cx="780" cy="300" rx="340" ry="250" fill="url(#nb2)"/>')
for i in range(80):
    x, y = random.randint(10, 1190), random.randint(10, 690)
    r = random.choice([0.7, 1, 1, 1.3])
    if i % 5 == 0:
        w(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#e0e7ff" style="animation:tw {random.uniform(3.5, 7):.1f}s -{random.uniform(0, 7):.1f}s infinite"/>')
    else:
        w(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#e0e7ff" opacity="{random.uniform(.15, .55):.2f}"/>')

# layer planes with ghost sheets
for k, y in reversed(list(enumerate(LAYERS))):
    for dx, dy, op in [(26, -14, .35), (13, -7, .6)]:
        w(f'<rect x="{200 + dx}" y="{y - 22 + dy}" width="800" height="44" rx="12" fill="url(#pl{k})" opacity="{op}"/>')
    w(f'<rect x="200" y="{y - 22}" width="800" height="44" rx="12" fill="url(#pl{k})" stroke="{LCOL[k]}" stroke-opacity=".18"/>')

# MLP (feed-forward) block for each layer, left side
for k, y in enumerate(LAYERS):
    c = LCOL[k]
    xs3, xs6 = 118, 150
    ins = [y - 12, y, y + 12]
    mids = [y - 25 + j * 10 for j in range(6)]
    lines = "".join(f"M{xs3} {a}L{xs6} {b}M{xs6} {b}L182 {a}" for a in ins for b in mids)
    w(f'<path d="{lines}" stroke="{c}" stroke-opacity=".18" stroke-width=".8"/>')
    dots = "".join(f'<circle cx="{xs3}" cy="{a}" r="2.6" fill="{c}"/><circle cx="182" cy="{a}" r="2.6" fill="{c}"/>' for a in ins)
    dots += "".join(f'<circle cx="{xs6}" cy="{b}" r="2.6" fill="{c}"/>' for b in mids)
    w(f'<g opacity=".25" style="animation:m{k} {STEP}s infinite">{dots}<circle cx="{xs6}" cy="{y}" r="30" fill="url(#hl)" opacity=".5"/></g>')
    w(f'<path d="M188 {y}H{XS[0] - 10:.0f}" stroke="{c}" stroke-opacity=".25" stroke-dasharray="2 4"/>')

# residual streams
for x in XS:
    w(f'<line x1="{x}" y1="{ROW_Y - 16}" x2="{x}" y2="{TOP}" stroke="url(#res)" stroke-opacity=".22" stroke-width="1.2"/>')

# multi-head attention from the last token
for k, y in enumerate(LAYERS):
    for h in range(3):
        weights = [random.uniform(.03, .25) for _ in range(7)]
        weights[[6, 5, 3, 1][(k + h) % 4]] = 1.0
        weights[random.randrange(7)] = max(weights[random.randrange(7)], .5)
        parts = []
        for j, wt in enumerate(weights):
            x8, xj = XS[7], XS[j]
            hgt = (10 + (x8 - xj) * .06) * (.75 + .3 * h)
            parts.append(f'<path d="M{x8:.0f} {y}Q{(x8 + xj) / 2:.0f} {y - hgt:.0f} {xj:.0f} {y}" fill="none" stroke="{HEADS[h]}" stroke-opacity="{.25 + .75 * wt:.2f}" stroke-width="{.8 + 2.6 * wt:.1f}"/>')
        w(f'<g style="animation:a{k}{h} {STEP}s infinite" opacity=".22">' + "".join(parts) + "</g>")

# layer nodes
for k, y in enumerate(LAYERS):
    for i, x in enumerate(XS):
        w(f'<circle cx="{x}" cy="{y}" r="{6 if i < 7 else 7.5}" fill="#0b1023" stroke="{LCOL[k]}" stroke-width="1.4"/>')
    cores = "".join(f'<circle cx="{x}" cy="{y}" r="16" fill="url(#hl)"/><circle cx="{x}" cy="{y}" r="{3 if i < 7 else 4}" fill="{LCOL[k]}"/>' for i, x in enumerate(XS))
    w(f'<g style="animation:n{k} {STEP}s infinite" opacity=".35">{cores}</g>')

for i, x in enumerate(XS):
    w(f'<circle class="mv" cx="{x}" cy="{ROW_Y - 18}" r="2.6" fill="#fff" opacity="0" style="animation:up {STEP}s linear {-i * 0.04:.2f}s infinite"/>')

# link to softmax
w(f'<path d="M{XS[7]:.0f} {TOP}Q{XS[7] - 40:.0f} {BAR_BASE + 20} {CX + 60} {BAR_BASE + 10}" fill="none" stroke="#e879f9" stroke-opacity=".2" stroke-width="1.2"/>')
w(f'<circle class="mv" cx="{XS[7]:.0f}" cy="{TOP - 8}" r="3" fill="#f5d0fe" opacity="0" style="animation:sm {STEP}s ease-in-out infinite"/>')

# softmax: a different distribution and winner for every step
w(f'<line x1="{BX0 - 14:.0f}" y1="{BAR_BASE}" x2="{BX0 + (NB - 1) * 15 + 14:.0f}" y2="{BAR_BASE}" stroke="#c4b5fd" stroke-opacity=".25"/>')
for b in range(NB):
    x = BX0 + b * 15
    frames = ["0%{transform:scaleY(.12);opacity:.3}"]
    for k in range(N):
        if b == WINNERS[k]:
            s = 1.0
        elif abs(b - WINNERS[k]) == 1:
            s = random.uniform(.3, .45)
        else:
            s = random.choice([.06, .08, .1, .13, .16, .2, .24, .3, .36])
        frames.append(f"{pct(g(k, 44))}{{transform:scaleY(.12);opacity:.3}}{pct(g(k, 52))}{{transform:scaleY({s});opacity:1}}{pct(g(k, 86))}{{transform:scaleY({s});opacity:1}}{pct(g(k, 97))}{{transform:scaleY(.12);opacity:.3}}")
    frames.append("100%{transform:scaleY(.12);opacity:.3}")
    css.append(f"@keyframes b{b}{{{''.join(frames)}}}")
    col = ["#6366f1", "#8b5cf6", "#a855f7", "#c084fc", "#e879f9"][b * 5 // NB]
    w(f'<rect class="fb" x="{x - 4:.0f}" y="{BAR_BASE - BAR_H}" width="8" height="{BAR_H}" rx="2" fill="{col}" fill-opacity=".7" style="animation:b{b} {T}s ease-in-out infinite"/>')

for k, wb in enumerate(WINNERS):
    x = BX0 + wb * 15
    css.append(f"@keyframes w{k}{{0%,{pct(g(k, 50))}{{opacity:0}}{pct(g(k, 54))},{pct(g(k, 80))}{{opacity:1}}{pct(g(k, 88))},100%{{opacity:0}}}}")
    w(f'<g opacity="0" style="animation:w{k} {T}s infinite"><circle cx="{x:.0f}" cy="{BAR_BASE - BAR_H - 8}" r="26" fill="url(#ho)"/><rect x="{x - 4:.0f}" y="{BAR_BASE - BAR_H}" width="8" height="{BAR_H}" rx="2" fill="{ORANGE}"/></g>')

# autoregressive loop hint
w(f'<path d="M{CX + 250:.0f} {BAR_BASE - 60}C1110 {BAR_BASE - 60} 1110 {ROW_Y - 60} {X9:.0f} {ROW_Y - 24}" fill="none" stroke="{ORANGE}" stroke-opacity=".28" stroke-width="1.3" stroke-dasharray="5 7"/>')
w(f'<circle cx="{XS[7]:.0f}" cy="{ROW_Y}" r="44" fill="url(#hl)" style="animation:cur {STEP}s infinite"/>')

# token row: types repeat every N slots, so the row loops seamlessly after N generated tokens
chips = [f'<use href="#t{j % N}" x="{X0 + j * SLOT:.0f}" y="{ROW_Y}"/>' for j in range(9)]
for k in range(N):
    j = 9 + k
    css.append(f"@keyframes s{k}{{0%,{pct(g(k, 80) - .01)}{{opacity:0}}{pct(g(k, 80))},100%{{opacity:1}}}}")
    chips.append(f'<use href="#t{j % N}" x="{X0 + j * SLOT:.0f}" y="{ROW_Y}" opacity="0" style="animation:s{k} {T}s infinite"/>')
w(f'<g mask="url(#rowFade)"><g style="animation:row {T}s cubic-bezier(.5,0,.3,1) infinite">{"".join(chips)}</g></g>')

# generated tokens flying from the winning bar to the end of the sequence
for k, wb in enumerate(WINNERS):
    wx = BX0 + wb * 15
    ax, ay = wx - X9, BAR_BASE - BAR_H - 14 - ROW_Y
    css.append(
        f"@keyframes f{k}{{0%,{pct(g(k, 55))}{{transform:translate({ax:.0f}px,{ay:.0f}px);opacity:0}}"
        f"{pct(g(k, 57))}{{transform:translate({ax:.0f}px,{ay:.0f}px);opacity:1}}"
        f"{pct(g(k, 67))}{{transform:translate(40px,-330px);opacity:1}}"
        f"{pct(g(k, 79))}{{transform:translate(0,0);opacity:1}}"
        f"{pct(g(k, 81))}{{transform:translate(0,0);opacity:0}}100%{{transform:translate(0,0);opacity:0}}}}"
    )
    w(f'<g opacity="0" style="animation:f{k} {T}s cubic-bezier(.45,0,.35,1) infinite"><use href="#o{(9 + k) % N}" x="{X9:.0f}" y="{ROW_Y}"/></g>')

o.insert(o.index("</defs>") + 1, "<style>" + "".join(css) + "</style>")
w("</svg>")
open(sys.argv[1], "w").write("\n".join(o))
