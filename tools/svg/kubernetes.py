import random
import sys

from common import DEFS, MONO, base_css, mobile, motion, nebula, stars, write_svg

random.seed(3)
T = 13.0
NW, NH, NGAP = 210, 160, 30
NX = [600 - (4 * NW + 3 * NGAP) / 2 + i * (NW + NGAP) for i in range(4)]
NY = 300
CPX, CPY = 600, 150
CPW, CPT, CPH = 460, 79, 112  # CPY is the middle of the body, below the 30 px header
ING = (600, 610)
SLOT, SGAP = 28, 22
APP = ["#22d3ee", "#8b5cf6", "#e879f9", "#fb923c"]
OK, BAD, WARN = "#4ade80", "#f43f5e", "#fbbf24"
CP_COLOUR = "#a5b4fc"  # control plane components share one colour, unlike the app colours of the pods
FAIL = 2

# timeline (% of the cycle)
SCALE = 8          # scale-up starts
F0 = 30            # node fails
RS = 35            # rescheduling starts
GONE0, GONE1 = 50, 57   # empty node leaves the cluster
JOIN0, JOIN1 = 70, 77   # new node joins
READY = 81         # new node ready
BAL = 84           # rebalance


def slot(n, i):
    """Pod slots in a 3x2 grid centred in the node's body, below its 30 px header."""
    c, r = i % 3, i // 3
    step = SLOT + SGAP
    return NX[n] + NW / 2 + (c - 1) * step, NY + (30 + NH) / 2 + (r - .5) * step


o = []
w = o.append
css = [
    "@keyframes spin{to{transform:rotate(360deg)}}",
    "@keyframes hf{0%{opacity:0}8%,85%{opacity:1}100%{opacity:0}}",
    "@keyframes tr{0%{transform:translate(0,0);opacity:0}10%{opacity:1}85%{opacity:1}100%{transform:translate(var(--x),var(--y));opacity:0}}",
    "@keyframes run{0%,100%{opacity:.85}50%{opacity:.45}}",
    f"@keyframes down{{0%,{F0 - .5}%{{opacity:1}}{F0}%,{READY}%{{opacity:0}}{READY + 1}%,100%{{opacity:1}}}}",
    f"@keyframes link{{0%,{GONE0}%{{opacity:1}}{GONE1}%,{JOIN0}%{{opacity:0}}{JOIN1}%,100%{{opacity:1}}}}",
    f"@keyframes node{{0%,{GONE0}%{{transform:translateY(0) scale(1);opacity:1}}{GONE1}%,{JOIN0}%{{transform:translateY(46px) scale(.88);opacity:0}}{JOIN1}%,100%{{transform:translateY(0) scale(1);opacity:1}}}}",
    f"@keyframes fail{{0%,{F0 - .5}%{{opacity:0}}{F0}%{{opacity:1}}{F0 + 2}%{{opacity:.55}}{F0 + 4}%{{opacity:1}}{GONE1}%{{opacity:1}}{GONE1 + .5}%,100%{{opacity:0}}}}",
    f"@keyframes join{{0%,{JOIN0}%{{opacity:0}}{JOIN0 + 1}%{{opacity:1}}{JOIN1 + 1}%{{opacity:.3}}{JOIN1 + 2}%{{opacity:1}}{READY - 1}%{{opacity:.3}}{READY}%,100%{{opacity:0}}}}",
    f"@keyframes sch{{0%,{SCALE - 1}%{{opacity:.25}}{SCALE + 1}%,{SCALE + 14}%{{opacity:1}}{SCALE + 16}%,{RS - 1}%{{opacity:.25}}{RS + 1}%,{RS + 14}%{{opacity:1}}{RS + 16}%,{BAL}%{{opacity:.25}}{BAL + 1}%,{BAL + 9}%{{opacity:1}}{BAL + 11}%,100%{{opacity:.25}}}}",
    ".pod,.nd{transform-box:fill-box;transform-origin:center}",
    mobile(".lb{font-size:24px}.ev{font-size:26px}.pd{display:none}"),
] + base_css()
pods = []
kf = []


def pod(n, i, color, states, name):
    """states: (pct, opacity, at_control_plane)"""
    x, y = slot(n, i)
    dx, dy = CPX - x, CPY - y
    frames = []
    for p, op, at_cp in states:
        t = f"translate({dx:.0f}px,{dy:.0f}px) scale(.6)" if at_cp else "translate(0,0) scale(1)"
        frames.append(f"{p}%{{transform:{t};opacity:{op}}}")
    kf.append(f"@keyframes {name}{{{''.join(frames)}}}")
    pods.append(f'<g class="pod" style="animation:{name} {T}s cubic-bezier(.45,0,.3,1) infinite"><rect x="{x - 14:.0f}" y="{y - 14:.0f}" width="28" height="28" rx="7" fill="#0b1023" stroke="{color}" stroke-width="1.8"/><rect x="{x - 6:.0f}" y="{y - 6:.0f}" width="12" height="12" rx="3" fill="{color}" style="animation:run {random.choice([1.6, 2, 2.4])}s {-random.uniform(0, 2):.2f}s infinite"/></g>')


def fly(t0):
    return [(0, 0, True), (t0, 0, True), (t0 + .5, 1, True), (t0 + 4, 1, False)]


base = {0: [0, 1, 2], 1: [0, 1], 2: [0, 1, 2], 3: [0, 1]}
k = 0
for n, slots in base.items():
    for j, i in enumerate(slots):
        c = APP[(n + i) % 4]
        if n == FAIL:
            t0 = BAL + 2 + j * 2.5
            st = [(0, 1, False), (F0, 1, False), (F0 + 2, 0, False), (F0 + 2.1, 0, True), (t0, 0, True), (t0 + .5, 1, True), (t0 + 4, 1, False), (100, 1, False)]
        else:
            st = [(0, 1, False), (100, 1, False)]
        pod(n, i, c, st, f"p{k}")
        k += 1

for n, i in {0: 3, 1: 2, 2: 3, 3: 2}.items():
    t0 = SCALE + 1 + n * 3.2
    c = APP[(n + 2) % 4]
    if n == FAIL:
        st = fly(t0) + [(F0, 1, False), (F0 + 2, 0, False), (100, 0, False)]
    else:
        st = fly(t0) + [(BAL + 1, 1, False), (BAL + 4, 0, False), (100, 0, False)]
    pod(n, i, c, st, f"p{k}")
    k += 1

for j, (n, i) in enumerate([(0, 4), (1, 3), (1, 4), (3, 3)]):
    t0 = RS + 1 + j * 3
    st = fly(t0) + [(BAL + 2 + j, 1, False), (BAL + 5 + j, 0, False), (100, 0, False)]
    pod(n, i, APP[j % 4], st, f"p{k}")
    k += 1

defs = ["<defs>", *DEFS,
        '<radialGradient id="cpg"><stop offset="0" stop-color="#a5b4fc" stop-opacity=".5"/><stop offset="1" stop-color="#a5b4fc" stop-opacity="0"/></radialGradient>',
        '<radialGradient id="rd"><stop offset="0" stop-color="#f43f5e" stop-opacity=".35"/><stop offset="1" stop-color="#f43f5e" stop-opacity="0"/></radialGradient>',
        '<radialGradient id="jn"><stop offset="0" stop-color="#fbbf24" stop-opacity=".28"/><stop offset="1" stop-color="#fbbf24" stop-opacity="0"/></radialGradient>',
        "</defs>"]

w(nebula((460, 360), (770, 340), (380, 360), 260))
o.extend(stars(80, (NX[0] - 10, NY - 10, NX[3] + NW + 10, NY + NH + 60)))


def cp_link(n):
    cx = NX[n] + NW / 2
    return f"M{CPX} {CPT + CPH}C{CPX} {CPY + 110} {cx:.0f} {NY - 80} {cx:.0f} {NY}"


def ing_link(n):
    cx = NX[n] + NW / 2
    return f"M{ING[0]} {ING[1] - 22}C{ING[0]} {ING[1] - 60} {cx:.0f} {NY + NH + 40} {cx:.0f} {NY + NH}"


others = [n for n in range(4) if n != FAIL]
w(f'<path d="{"".join(cp_link(n) for n in others)}" fill="none" stroke="#a5b4fc" stroke-opacity=".3" stroke-width="1.4" stroke-dasharray="4 6"/>')
w(f'<path d="{"".join(ing_link(n) for n in others)}" fill="none" stroke="#22d3ee" stroke-opacity=".25" stroke-width="1.4"/>')
w(f'<g style="animation:link {T}s infinite"><path d="{cp_link(FAIL)}" fill="none" stroke="#a5b4fc" stroke-opacity=".3" stroke-width="1.4" stroke-dasharray="4 6"/><path d="{ing_link(FAIL)}" fill="none" stroke="#22d3ee" stroke-opacity=".25" stroke-width="1.4"/></g>')

# nodes
for n in range(4):
    x = NX[n]
    parts = [
        f'<rect x="{x}" y="{NY}" width="{NW}" height="{NH}" rx="14" fill="#0b1023" fill-opacity=".85" stroke="#818cf8" stroke-opacity=".55" stroke-width="1.4"/>',
        f'<path d="M{x + 14} {NY + 30}H{x + NW - 14}" stroke="#818cf8" stroke-opacity=".18"/>',
        f'<text x="{x + 38}" y="{NY + 20}" class="lb" {MONO} font-size="13" fill="#c7d2fe" fill-opacity=".75">node {n + 1}</text>',
    ]
    for i in range(6):
        sx, sy = slot(n, i)
        parts.append(f'<rect x="{sx - 14:.0f}" y="{sy - 14:.0f}" width="28" height="28" rx="7" fill="none" stroke="#818cf8" stroke-opacity=".18" stroke-dasharray="3 4"/>')
    parts.append(f'<circle cx="{x + 24}" cy="{NY + 15}" r="9" fill="url(#hl)"/><circle cx="{x + 24}" cy="{NY + 15}" r="3.5" fill="{OK}"/>')
    if n == FAIL:
        parts.append(f'<g opacity="0" style="animation:fail {T}s infinite"><ellipse cx="{x + NW / 2}" cy="{NY + NH / 2}" rx="{NW * .75}" ry="{NH * .8}" fill="url(#rd)"/><rect x="{x}" y="{NY}" width="{NW}" height="{NH}" rx="14" fill="none" stroke="{BAD}" stroke-width="1.6"/><circle cx="{x + 24}" cy="{NY + 15}" r="5" fill="{BAD}"/><path d="M{x + NW - 36} {NY + 9}l12 12M{x + NW - 24} {NY + 9}l-12 12" stroke="{BAD}" stroke-width="1.8" stroke-linecap="round"/>'
                     f'<text x="{x + NW / 2}" y="{NY + NH + 24}" text-anchor="middle" class="ev" {MONO} font-size="14" font-weight="600" fill="{BAD}">node down</text></g>')
        parts.append(f'<g opacity="0" style="animation:join {T}s infinite"><ellipse cx="{x + NW / 2}" cy="{NY + NH / 2}" rx="{NW * .75}" ry="{NH * .8}" fill="url(#jn)"/><rect x="{x}" y="{NY}" width="{NW}" height="{NH}" rx="14" fill="none" stroke="{WARN}" stroke-width="1.4" stroke-dasharray="8 6"/><circle cx="{x + 24}" cy="{NY + 15}" r="5" fill="{WARN}"/>'
                     f'<text x="{x + NW / 2}" y="{NY + NH + 24}" text-anchor="middle" class="ev" {MONO} font-size="14" font-weight="600" fill="{WARN}">node up</text></g>')
        w(f'<g class="nd" style="animation:node {T}s cubic-bezier(.5,0,.3,1) infinite">' + "".join(parts) + "</g>")
    else:
        w("".join(parts))

w("".join(pods))

# heartbeats node -> control plane and traffic ingress -> node
for n in range(4):
    cx = NX[n] + NW / 2
    # heartbeat: the node's kubelet reports to the api server, travelling up its dashed link
    p0, p1, p2, p3 = (cx, NY), (cx, NY - 80), (CPX, CPY + 110), (CPX, CPT + CPH)
    path = [tuple((1 - t) ** 3 * p0[i] + 3 * (1 - t) ** 2 * t * p1[i] + 3 * (1 - t) * t * t * p2[i] + t ** 3 * p3[i] for i in (0, 1))
            for t in (k / 24 for k in range(25))]
    css.append(motion(f"hm{n}", path))
    hb = (f'<g class="mv" style="animation:hf 2.6s linear {-n * .65:.2f}s infinite"><circle r="3" fill="{OK}" '
          f'style="animation:hm{n} 2.6s linear {-n * .65:.2f}s infinite"/></g>')
    tr = "".join(f'<circle class="mv" cx="{ING[0]}" cy="{ING[1] - 24}" r="2.6" fill="#67e8f9" style="--x:{cx - ING[0]:.0f}px;--y:{NY + NH + 4 - (ING[1] - 24):.0f}px;animation:tr 1.4s ease-in {-random.uniform(0, 1.4):.2f}s infinite"/>' for _ in range(3))
    if n == FAIL:
        w(f'<g style="animation:down {T}s infinite">{hb}{tr}</g>')
    else:
        w(hb + tr)

# control plane
w(f'<ellipse cx="{CPX}" cy="{CPY}" rx="190" ry="70" fill="url(#cpg)" opacity=".25" style="animation:sch {T}s infinite"/>')
# control plane: drawn like a node, wider, with its name in the header
w(f'<rect x="{CPX - CPW / 2}" y="{CPT}" width="{CPW}" height="{CPH}" rx="14" fill="#0b1023" fill-opacity=".9" stroke="#a5b4fc" stroke-opacity=".6" stroke-width="1.4"/>')
w(f'<path d="M{CPX - CPW / 2 + 14} {CPT + 30}H{CPX + CPW / 2 - 14}" stroke="#818cf8" stroke-opacity=".18"/>')
w(f'<circle cx="{CPX - CPW / 2 + 24}" cy="{CPT + 15}" r="9" fill="url(#hl)"/><circle cx="{CPX - CPW / 2 + 24}" cy="{CPT + 15}" r="3.5" fill="{OK}"/>'
  f'<text x="{CPX - CPW / 2 + 38}" y="{CPT + 20}" class="lb" {MONO} font-size="13" fill="#c7d2fe" fill-opacity=".75">control plane</text>')
w(f'<g style="transform-origin:{CPX}px {CPY}px;animation:spin 8s linear infinite"><circle cx="{CPX}" cy="{CPY}" r="27" fill="none" stroke="#a5b4fc" stroke-opacity=".6" stroke-width="1.3" stroke-dasharray="10 7"/></g>')
w(f'<circle cx="{CPX}" cy="{CPY}" r="15" fill="#6366f1" fill-opacity=".85" stroke="#c7d2fe"/>')
for side in (-1, 1):
    for j in range(2):
        x = CPX + side * (85 + j * 90)
        c = CP_COLOUR
        w(f'<rect x="{x - 14}" y="{CPY - 14}" width="28" height="28" rx="7" fill="#0b1023" stroke="{c}" stroke-width="1.5"/><rect x="{x - 5}" y="{CPY - 5}" width="10" height="10" rx="3" fill="{c}" style="animation:sch {T}s infinite"/>')
# what each piece of the control plane is
CP_PARTS = [(CPX - 175, "etcd"), (CPX - 85, "scheduler"), (CPX, "api server"), (CPX + 85, "controllers"), (CPX + 175, "cloud ctrl")]
w("".join(f'<text x="{x}" y="{CPY + 36}" text-anchor="middle" class="pd" {MONO} font-size="11" fill="#c7d2fe" fill-opacity=".65">{name}</text>' for x, name in CP_PARTS))

# labels
WL = (NX[0] - 18, NY - 44, NX[3] + NW + 18, NY + NH + 40)
w(f'<rect x="{WL[0]}" y="{WL[1]}" width="{WL[2] - WL[0]}" height="{WL[3] - WL[1]}" rx="20" fill="none" stroke="#818cf8" stroke-opacity=".28" stroke-dasharray="4 6"/>')
w(f'<text x="{WL[0] + 16}" y="{WL[1] - 10}" class="lb" {MONO} font-size="13" fill="#c7d2fe" fill-opacity=".75">workload · worker nodes</text>')
w(f'<text x="{NX[0] + NW - 14}" y="{NY + 20}" text-anchor="end" class="pd" {MONO} font-size="13" fill="#c7d2fe" fill-opacity=".5">pods</text>')

# ingress
w(f'<rect x="{ING[0] - 110}" y="{ING[1] - 22}" width="220" height="44" rx="12" fill="#0b1023" fill-opacity=".9" stroke="#22d3ee" stroke-opacity=".6" stroke-width="1.5"/>')
w(f'<text x="{ING[0]}" y="{ING[1] + 5}" text-anchor="middle" class="lb" {MONO} font-size="14" fill="#67e8f9" fill-opacity=".9">ingress</text>')
for i in range(5):
    w(f'<circle class="mv" cx="{ING[0] - 240 + i * 6}" cy="{ING[1]}" r="2.4" fill="#67e8f9" style="--x:130px;--y:0px;animation:tr 1.2s linear {-i * .24:.2f}s infinite"/>')

# users on the internet, where the traffic comes from
GX = ING[0] - 280
w(f'<circle cx="{GX}" cy="{ING[1]}" r="30" fill="url(#hl)"/>'
  f'<g fill="none" stroke="#67e8f9" stroke-opacity=".85" stroke-width="1.4"><circle cx="{GX}" cy="{ING[1]}" r="18"/>'
  f'<ellipse cx="{GX}" cy="{ING[1]}" rx="8" ry="18"/><path d="M{GX - 18} {ING[1]}h36M{GX - 15} {ING[1] - 9}h30M{GX - 15} {ING[1] + 9}h30"/></g>')
w(f'<text x="{GX}" y="{ING[1] + 40}" text-anchor="middle" class="lb" {MONO} font-size="13" fill="#67e8f9" fill-opacity=".75">users</text>')

write_svg(sys.argv[1], "Animated Kubernetes cluster", defs, css + kf, o)
