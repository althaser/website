import random
import sys

random.seed(3)
T = 10.0
NW, NH, NGAP = 210, 160, 30
NX = [600 - (4 * NW + 3 * NGAP) / 2 + i * (NW + NGAP) for i in range(4)]
NY = 300
CPX, CPY = 600, 130
ING = (600, 610)
SLOT, SGAP = 40, 18
APP = ["#22d3ee", "#8b5cf6", "#e879f9", "#fb923c"]
OK, BAD = "#4ade80", "#f43f5e"
FAIL = 2
F0, F1 = 40, 72


def slot(n, i):
    c, r = i % 3, i // 3
    x0 = NX[n] + (NW - (3 * SLOT + 2 * SGAP)) / 2
    return x0 + c * (SLOT + SGAP) + SLOT / 2, NY + 58 + r * (SLOT + SGAP) + SLOT / 2


o = []
w = o.append
css = [
    "@keyframes tw{0%,100%{opacity:.15}50%{opacity:.9}}",
    "@keyframes spin{to{transform:rotate(360deg)}}",
    "@keyframes hb{0%{transform:translateY(0);opacity:0}10%{opacity:1}80%{opacity:1}100%{transform:translateY(var(--d));opacity:0}}",
    "@keyframes tr{0%{transform:translate(0,0);opacity:0}10%{opacity:1}85%{opacity:1}100%{transform:translate(var(--x),var(--y));opacity:0}}",
    f"@keyframes down{{0%,{F0 - .5}%{{opacity:1}}{F0}%,{F1}%{{opacity:0}}{F1 + .5}%,100%{{opacity:1}}}}",
    f"@keyframes fail{{0%,{F0 - .5}%{{opacity:0}}{F0}%{{opacity:1}}{F0 + 3}%{{opacity:.55}}{F0 + 6}%{{opacity:1}}{F1 - 2}%{{opacity:1}}{F1}%,100%{{opacity:0}}}}",
    "@keyframes sch{0%,9%{opacity:.25}12%,28%{opacity:1}31%,44%{opacity:.25}47%,62%{opacity:1}65%,100%{opacity:.25}}",
    ".pod{transform-box:fill-box;transform-origin:center}",
    "@media (prefers-reduced-motion:reduce){*{animation:none!important}.mv{opacity:0}}",
]
pods = []
kf = []


def pod(n, i, color, states, name):
    """states: list of (pct, opacity, from_cp) ; from_cp True means positioned at control plane"""
    x, y = slot(n, i)
    dx, dy = CPX - x, CPY + 40 - y
    frames = []
    for p, op, at_cp in states:
        t = f"translate({dx:.0f}px,{dy:.0f}px) scale(.6)" if at_cp else "translate(0,0) scale(1)"
        frames.append(f"{p}%{{transform:{t};opacity:{op}}}")
    kf.append(f"@keyframes {name}{{{''.join(frames)}}}")
    pods.append(f'<g class="pod" style="animation:{name} {T}s cubic-bezier(.45,0,.3,1) infinite"><rect x="{x - SLOT / 2 + 2:.0f}" y="{y - SLOT / 2 + 2:.0f}" width="{SLOT - 4}" height="{SLOT - 4}" rx="9" fill="#0b1023" stroke="{color}" stroke-width="1.8"/><rect x="{x - 8:.0f}" y="{y - 8:.0f}" width="16" height="16" rx="4" fill="{color}" fill-opacity=".85"/></g>')


base = {0: [0, 1, 2], 1: [0, 1], 2: [0, 1, 2], 3: [0, 1]}
k = 0
for n, slots in base.items():
    for i in slots:
        c = APP[(n + i) % 4]
        if n == FAIL:
            st = [(0, 1, False), (F0, 1, False), (F0 + 3, 0, False), (88, 0, False), (94, 1, False), (100, 1, False)]
        else:
            st = [(0, 1, False), (100, 1, False)]
        pod(n, i, c, st, f"p{k}")
        k += 1

scale = {0: 3, 1: 2, 2: 3, 3: 2}
for n, i in scale.items():
    s0 = 11 + n * 4
    c = APP[(n + 2) % 4]
    if n == FAIL:
        st = [(0, 0, True), (s0, 0, True), (s0 + .5, 1, True), (s0 + 5, 1, False), (F0, 1, False), (F0 + 3, 0, False), (100, 0, False)]
    else:
        st = [(0, 0, True), (s0, 0, True), (s0 + .5, 1, True), (s0 + 5, 1, False), (86, 1, False), (90, 0, False), (100, 0, False)]
    pod(n, i, c, st, f"p{k}")
    k += 1

resched = [(0, 4), (1, 3), (1, 4), (3, 3)]
for j, (n, i) in enumerate(resched):
    s0 = 47 + j * 3.5
    c = APP[j % 4]
    st = [(0, 0, True), (s0, 0, True), (s0 + .5, 1, True), (s0 + 5, 1, False), (85 + j, 1, False), (89 + j, 0, False), (100, 0, False)]
    pod(n, i, c, st, f"p{k}")
    k += 1

w('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 700" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Animated Kubernetes cluster">')
w("<defs>")
w('<radialGradient id="nb1"><stop offset="0" stop-color="#4338ca" stop-opacity=".42"/><stop offset="1" stop-color="#4338ca" stop-opacity="0"/></radialGradient>')
w('<radialGradient id="nb2"><stop offset="0" stop-color="#a21caf" stop-opacity=".36"/><stop offset="1" stop-color="#a21caf" stop-opacity="0"/></radialGradient>')
w('<radialGradient id="hl"><stop offset="0" stop-color="#a5b4fc" stop-opacity=".5"/><stop offset="1" stop-color="#a5b4fc" stop-opacity="0"/></radialGradient>')
w('<radialGradient id="rd"><stop offset="0" stop-color="#f43f5e" stop-opacity=".35"/><stop offset="1" stop-color="#f43f5e" stop-opacity="0"/></radialGradient>')
w("</defs>")
w("<style>" + "".join(css + kf) + "</style>")

w('<ellipse cx="460" cy="360" rx="380" ry="260" fill="url(#nb1)"/><ellipse cx="770" cy="340" rx="360" ry="260" fill="url(#nb2)"/>')
for i in range(80):
    x, y = random.randint(10, 1190), random.randint(10, 690)
    if NX[0] - 10 < x < NX[3] + NW + 10 and NY - 10 < y < NY + NH + 10:
        continue
    r = random.choice([.7, 1, 1, 1.3])
    if i % 5 == 0:
        w(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#e0e7ff" style="animation:tw {random.uniform(3.5, 7):.1f}s -{random.uniform(0, 7):.1f}s infinite"/>')
    else:
        w(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#e0e7ff" opacity="{random.uniform(.15, .55):.2f}"/>')

# links control plane <-> nodes and ingress -> nodes
links = []
for n in range(4):
    cx = NX[n] + NW / 2
    links.append(f"M{CPX} {CPY + 42}C{CPX} {CPY + 110} {cx:.0f} {NY - 80} {cx:.0f} {NY}")
w(f'<path d="{"".join(links)}" fill="none" stroke="#a5b4fc" stroke-opacity=".3" stroke-width="1.4" stroke-dasharray="4 6"/>')
ing = []
for n in range(4):
    cx = NX[n] + NW / 2
    ing.append(f"M{ING[0]} {ING[1] - 22}C{ING[0]} {ING[1] - 60} {cx:.0f} {NY + NH + 40} {cx:.0f} {NY + NH}")
w(f'<path d="{"".join(ing)}" fill="none" stroke="#22d3ee" stroke-opacity=".25" stroke-width="1.4"/>')

# nodes
for n in range(4):
    x = NX[n]
    w(f'<rect x="{x + 14}" y="{NY - 10}" width="{NW}" height="{NH}" rx="14" fill="#6366f1" fill-opacity=".05" stroke="#818cf8" stroke-opacity=".15"/>')
    w(f'<rect x="{x}" y="{NY}" width="{NW}" height="{NH}" rx="14" fill="#0b1023" fill-opacity=".85" stroke="#818cf8" stroke-opacity=".55" stroke-width="1.4"/>')
    w(f'<path d="M{x + 14} {NY + 30}H{x + NW - 14}" stroke="#818cf8" stroke-opacity=".25"/>')
    w(f'<path d="M{x + 40} {NY + 15}h46M{x + 40} {NY + 15}" stroke="#c7d2fe" stroke-opacity=".5" stroke-width="3" stroke-linecap="round"/>')
    for i in range(6):
        sx, sy = slot(n, i)
        w(f'<rect x="{sx - SLOT / 2 + 2:.0f}" y="{sy - SLOT / 2 + 2:.0f}" width="{SLOT - 4}" height="{SLOT - 4}" rx="9" fill="none" stroke="#818cf8" stroke-opacity=".18" stroke-dasharray="3 4"/>')
    w(f'<circle cx="{x + 24}" cy="{NY + 15}" r="5" fill="{OK}"/>')
    if n == FAIL:
        w(f'<g opacity="0" style="animation:fail {T}s infinite"><ellipse cx="{x + NW / 2}" cy="{NY + NH / 2}" rx="{NW * .75}" ry="{NH * .8}" fill="url(#rd)"/><rect x="{x}" y="{NY}" width="{NW}" height="{NH}" rx="14" fill="none" stroke="{BAD}" stroke-width="2.2"/><circle cx="{x + 24}" cy="{NY + 15}" r="5" fill="{BAD}"/><path d="M{x + NW - 36} {NY + 9}l12 12M{x + NW - 24} {NY + 9}l-12 12" stroke="{BAD}" stroke-width="2.4" stroke-linecap="round"/></g>')

# pods
w("".join(pods))

# heartbeats node -> control plane and traffic ingress -> node
for n in range(4):
    cx = NX[n] + NW / 2
    hb = f'<circle class="mv" cx="{cx:.0f}" cy="{NY - 4}" r="3" fill="{OK}" style="--d:-30px;animation:hb 2s ease-out {-n * .5:.1f}s infinite"/>'
    tr = "".join(f'<circle class="mv" cx="{ING[0]}" cy="{ING[1] - 24}" r="2.6" fill="#67e8f9" style="--x:{cx - ING[0]:.0f}px;--y:{NY + NH + 4 - (ING[1] - 24):.0f}px;animation:tr 1.4s ease-in {-random.uniform(0, 1.4):.2f}s infinite"/>' for _ in range(3))
    if n == FAIL:
        w(f'<g style="animation:down {T}s infinite">{hb}{tr}</g>')
    else:
        w(hb + tr)

# control plane
w(f'<ellipse cx="{CPX}" cy="{CPY}" rx="190" ry="70" fill="url(#hl)" opacity=".25" style="animation:sch {T}s infinite"/>')
w(f'<rect x="{CPX - 150}" y="{CPY - 42}" width="300" height="84" rx="16" fill="#0b1023" fill-opacity=".9" stroke="#a5b4fc" stroke-opacity=".6" stroke-width="1.5"/>')
w(f'<g style="transform-origin:{CPX}px {CPY}px;animation:spin 8s linear infinite"><circle cx="{CPX}" cy="{CPY}" r="27" fill="none" stroke="#a5b4fc" stroke-opacity=".7" stroke-width="2" stroke-dasharray="10 7"/></g>')
w(f'<circle cx="{CPX}" cy="{CPY}" r="15" fill="#6366f1" fill-opacity=".85" stroke="#c7d2fe"/>')
for side in (-1, 1):
    for j in range(2):
        x = CPX + side * (62 + j * 46)
        c = ["#22d3ee", "#a855f7", "#e879f9", "#fb923c"][(side + 1) + j]
        w(f'<rect x="{x - 17}" y="{CPY - 17}" width="34" height="34" rx="8" fill="#0b1023" stroke="{c}" stroke-width="1.5"/><rect x="{x - 6}" y="{CPY - 6}" width="12" height="12" rx="3" fill="{c}" style="animation:sch {T}s infinite"/>')

# ingress
w(f'<rect x="{ING[0] - 110}" y="{ING[1] - 22}" width="220" height="44" rx="12" fill="#0b1023" fill-opacity=".9" stroke="#22d3ee" stroke-opacity=".6" stroke-width="1.5"/>')
w(f'<path d="M{ING[0] - 70} {ING[1]}h140M{ING[0] + 56} {ING[1] - 10}l14 10-14 10M{ING[0] - 56} {ING[1] - 10}l-14 10 14 10" fill="none" stroke="#67e8f9" stroke-opacity=".8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
for i in range(5):
    w(f'<circle class="mv" cx="{ING[0] - 220 + i * 6}" cy="{ING[1]}" r="2.4" fill="#67e8f9" style="--x:110px;--y:0px;animation:tr 1.2s linear {-i * .24:.2f}s infinite"/>')

w("</svg>")
open(sys.argv[1], "w").write("\n".join(o))
