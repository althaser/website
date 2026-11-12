import random
import sys

random.seed(7)
T = 6.0
SLOT = 96
CX = 600
XS = [CX + (i - 4.5) * SLOT for i in range(1, 9)]
X9 = CX + 4.5 * SLOT
X0 = CX - 5.5 * SLOT
ROW_Y = 600
LAYERS = [505, 425, 345, 265]
LCOL = ["#22d3ee", "#49b6f6", "#6366f1", "#a855f7"]
TOP = 245
BAR_BASE = 180
ORANGE = "#fb923c"

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
w(f'<g id="chip"><rect x="-34" y="-15" width="68" height="30" rx="7" fill="#0b1023" stroke="#22d3ee" stroke-width="1.5"/><path d="M-22 -4h30M-22 5h20" stroke="#67e8f9" stroke-opacity=".75" stroke-width="2.5" stroke-linecap="round"/></g>')
w(f'<g id="chipo"><rect x="-34" y="-15" width="68" height="30" rx="7" fill="#1c1020" stroke="{ORANGE}" stroke-width="1.8"/><path d="M-22 -4h30M-22 5h20" stroke="#fdba74" stroke-width="2.5" stroke-linecap="round"/></g>')
w("</defs>")


def pct(x):
    return f"{x:.1f}%"


css = []
css.append(".fb{transform-box:fill-box;transform-origin:50% 100%}")
css.append("@keyframes tw{0%,100%{opacity:.15}50%{opacity:.9}}")
css.append("@keyframes up{0%{transform:translateY(0);opacity:0}3%{opacity:1}36%{transform:translateY(-345px);opacity:1}40%,100%{transform:translateY(-345px);opacity:0}}")
for k, y in enumerate(LAYERS):
    p = 3 + (ROW_Y - 10 - y) / 345 * 33
    css.append(f"@keyframes n{k}{{0%,{pct(p - 2)}{{opacity:.35}}{pct(p)}{{opacity:1}}{pct(p + 14)},100%{{opacity:.35}}}}")
    css.append(f"@keyframes a{k}{{0%,{pct(p)}{{opacity:.3}}{pct(p + 3)}{{opacity:1}}{pct(p + 18)},100%{{opacity:.3}}}}")
css.append("@keyframes sm{0%,37%{transform:translate(0,0);opacity:0}38%{opacity:1}45%{transform:translate(-336px,-52px);opacity:1}47%,100%{transform:translate(-336px,-52px);opacity:0}}")
css.append("@keyframes bar{0%,44%{transform:scaleY(.12);opacity:.3}52%{transform:scaleY(1);opacity:1}86%{transform:scaleY(1);opacity:1}97%,100%{transform:scaleY(.12);opacity:.3}}")
css.append("@keyframes win{0%,50%{opacity:0}56%,74%{opacity:1}86%,100%{opacity:0}}")
css.append("@keyframes cur{0%{opacity:1}14%,82%{opacity:0}96%,100%{opacity:1}}")
css.append("@keyframes row{0%,80%{transform:translateX(0)}95%{transform:translateX(-96px)}95.01%,100%{transform:translateX(0)}}")
css.append("@keyframes s9{0%,79%{opacity:0}80%,95%{opacity:1}95.01%,100%{opacity:0}}")
css.append("@keyframes fly{0%,55%{transform:translate(VAR_A);opacity:0}57%{transform:translate(VAR_A);opacity:1}66%{transform:translate(68px,-380px);opacity:1}78%{transform:translate(0,0);opacity:1}80%{transform:translate(0,0);opacity:1}95%{transform:translate(-96px,0);opacity:0}100%{transform:translate(-96px,0);opacity:0}}")
css.append("@media (prefers-reduced-motion:reduce){*{animation:none!important}}")

# winner bar position
NB = 31
BX0 = CX - (NB - 1) * 15 / 2
WIN = 19
wx = BX0 + WIN * 15
css[-2] = css[-2].replace("VAR_A", f"{wx - X9:.0f}px,{BAR_BASE - 92 - ROW_Y:.0f}px")

w("<style>" + "".join(css) + "</style>")

# nebula
w('<ellipse cx="450" cy="380" rx="360" ry="250" fill="url(#nb1)"/><ellipse cx="780" cy="300" rx="340" ry="250" fill="url(#nb2)"/>')

# stars
for i in range(80):
    x, y = random.randint(10, 1190), random.randint(10, 690)
    r = random.choice([0.7, 1, 1, 1.3])
    if i % 5 == 0:
        w(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#e0e7ff" style="animation:tw {random.uniform(3.5, 7):.1f}s -{random.uniform(0, 7):.1f}s infinite"/>')
    else:
        w(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#e0e7ff" opacity="{random.uniform(.15, .55):.2f}"/>')

# layer planes with ghost sheets
for k, y in reversed(list(enumerate(LAYERS))):
    for g, (dx, dy, op) in enumerate([(26, -14, .35), (13, -7, .6)]):
        w(f'<rect x="{200 + dx}" y="{y - 22 + dy}" width="800" height="44" rx="12" fill="url(#pl{k})" opacity="{op}"/>')
    w(f'<rect x="200" y="{y - 22}" width="800" height="44" rx="12" fill="url(#pl{k})" stroke="{LCOL[k]}" stroke-opacity=".18"/>')

# residual streams
for x in XS:
    w(f'<line x1="{x}" y1="{ROW_Y - 16}" x2="{x}" y2="{TOP}" stroke="url(#res)" stroke-opacity=".22" stroke-width="1.2"/>')

# attention arcs per layer (from last token to previous tokens)
for k, y in enumerate(LAYERS):
    weights = [random.uniform(.05, .3) for _ in range(7)]
    focus = [6, 5, 1, 1][k]
    weights[focus] = 1.0
    if k >= 2:
        weights[4] = .55
    faint = []
    for a in range(1, 7):
        for b in range(a):
            if random.random() < .35:
                xa, xb = XS[a], XS[b]
                h = 10 + (xa - xb) * .06
                faint.append(f"M{xa:.0f} {y}Q{(xa + xb) / 2:.0f} {y - h:.0f} {xb:.0f} {y}")
    w(f'<path d="{"".join(faint)}" fill="none" stroke="{LCOL[k]}" stroke-opacity=".16" stroke-width="1"/>')
    parts = []
    for j, wt in enumerate(weights):
        x8, xj = XS[7], XS[j]
        h = 12 + (x8 - xj) * .075
        parts.append(f'<path d="M{x8:.0f} {y}Q{(x8 + xj) / 2:.0f} {y - h:.0f} {xj:.0f} {y}" fill="none" stroke="{LCOL[k] if wt < .9 else "#fde68a"}" stroke-opacity="{.35 + .65 * wt:.2f}" stroke-width="{1 + 3.2 * wt:.1f}"/>')
    w(f'<g style="animation:a{k} {T}s infinite">' + "".join(parts) + "</g>")

# layer nodes
for k, y in enumerate(LAYERS):
    for i, x in enumerate(XS):
        r = 6 if i < 7 else 7.5
        w(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#0b1023" stroke="{LCOL[k]}" stroke-width="1.4"/>')
    cores = "".join(f'<circle cx="{x}" cy="{y}" r="16" fill="url(#hl)"/><circle cx="{x}" cy="{y}" r="{3 if i < 7 else 4}" fill="{LCOL[k]}"/>' for i, x in enumerate(XS))
    w(f'<g style="animation:n{k} {T}s infinite" opacity=".35">{cores}</g>')

# pulses up the residual stream
for i, x in enumerate(XS):
    d = -i * 0.04
    w(f'<circle cx="{x}" cy="{ROW_Y - 18}" r="2.6" fill="#fff" opacity="0" style="animation:up {T}s linear {d:.2f}s infinite"/>')

# top: link to softmax
w(f'<path d="M{XS[7]:.0f} {TOP}Q{XS[7] - 40:.0f} {BAR_BASE + 20} {CX + 60} {BAR_BASE + 10}" fill="none" stroke="#e879f9" stroke-opacity=".2" stroke-width="1.2"/>')
w(f'<circle cx="{XS[7]:.0f}" cy="{TOP - 8}" r="3" fill="#f5d0fe" opacity="0" style="animation:sm {T}s ease-in-out infinite"/>')

# softmax bars
w(f'<line x1="{BX0 - 14:.0f}" y1="{BAR_BASE}" x2="{BX0 + (NB - 1) * 15 + 14:.0f}" y2="{BAR_BASE}" stroke="#c4b5fd" stroke-opacity=".25"/>')
for b in range(NB):
    x = BX0 + b * 15
    if b == WIN:
        h, col = 92, ORANGE
    else:
        h = random.choice([6, 8, 10, 12, 14, 18, 22, 28, 34, 44]) if abs(b - WIN) > 1 else 40
        col = ["#6366f1", "#8b5cf6", "#a855f7", "#c084fc", "#e879f9"][b * 5 // NB]
    w(f'<rect class="fb" x="{x - 4:.0f}" y="{BAR_BASE - h}" width="8" height="{h}" rx="2" fill="{col}" fill-opacity="{.95 if b == WIN else .7}" style="animation:bar {T}s ease-in-out infinite"/>')
w(f'<circle cx="{wx:.0f}" cy="{BAR_BASE - 100}" r="26" fill="url(#ho)" opacity="0" style="animation:win {T}s infinite"/>')

# autoregressive loop hint
w(f'<path d="M{wx + 30:.0f} {BAR_BASE - 92}C1130 {BAR_BASE - 92} 1130 {ROW_Y - 60} {X9:.0f} {ROW_Y - 24}" fill="none" stroke="{ORANGE}" stroke-opacity=".28" stroke-width="1.3" stroke-dasharray="5 7"/>')

# current-token highlight under slot 8
w(f'<circle cx="{XS[7]:.0f}" cy="{ROW_Y}" r="44" fill="url(#hl)" style="animation:cur {T}s infinite"/>')

# token row (slides one slot per cycle)
chips = "".join(f'<use href="#chip" x="{x:.0f}" y="{ROW_Y}"/>' for x in [X0] + XS)
w(f'<g mask="url(#rowFade)"><g style="animation:row {T}s cubic-bezier(.5,0,.3,1) infinite">{chips}<use href="#chip" x="{X9:.0f}" y="{ROW_Y}" opacity="0" style="animation:s9 {T}s infinite"/></g></g>')

# flying generated token
w(f'<g style="animation:fly {T}s cubic-bezier(.45,0,.35,1) infinite" opacity="0"><use href="#chipo" x="{X9:.0f}" y="{ROW_Y}"/></g>')

w("</svg>")
open(sys.argv[1], "w").write("\n".join(o))
