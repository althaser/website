import random

W, H = 1200, 700
STAR = "#e0e7ff"
PALETTE = ["#22d3ee", "#60a5fa", "#6366f1", "#8b5cf6", "#a855f7", "#d946ef", "#f472b6", "#fb923c"]


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def hexc(c):
    return "#%02x%02x%02x" % tuple(round(max(0, min(255, v))) for v in c)


def mix(a, b, t):
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))


def ramp(stops, t):
    t = max(0, min(1, t))
    seg = t * (len(stops) - 1)
    i = min(int(seg), len(stops) - 2)
    return mix(rgb(stops[i]), rgb(stops[i + 1]), seg - i)


def palette(t, stops=PALETTE):
    return hexc(ramp(stops, t))


def svg_open(label, x=0, y=0):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x} {y} {W} {H}" preserveAspectRatio="xMidYMid slice" role="img" aria-label="{label}">'


DEFS = [
    '<radialGradient id="nb1"><stop offset="0" stop-color="#4338ca" stop-opacity=".42"/><stop offset="1" stop-color="#4338ca" stop-opacity="0"/></radialGradient>',
    '<radialGradient id="nb2"><stop offset="0" stop-color="#a21caf" stop-opacity=".36"/><stop offset="1" stop-color="#a21caf" stop-opacity="0"/></radialGradient>',
    '<radialGradient id="hl"><stop offset="0" stop-color="#fff" stop-opacity=".5"/><stop offset=".4" stop-color="#fff" stop-opacity=".15"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>',
]


def base_css(hidden=".mv"):
    """Twinkle keyframes plus the reduced-motion rule; `hidden` lists elements to hide when motion is reduced."""
    extra = f"{hidden}{{opacity:0}}" if hidden else ""
    return [
        "@keyframes tw{0%,100%{opacity:.15}50%{opacity:.9}}",
        f"@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}{extra}}}",
    ]


def nebula(left=(450, 350), right=(770, 350), rx=(360, 340), ry=250):
    return (f'<ellipse cx="{left[0]}" cy="{left[1]}" rx="{rx[0]}" ry="{ry}" fill="url(#nb1)"/>'
            f'<ellipse cx="{right[0]}" cy="{right[1]}" rx="{rx[1]}" ry="{ry}" fill="url(#nb2)"/>')


def stars(count=80, avoid=None):
    """Star field; every fifth star twinkles. `avoid` is an (x0, y0, x1, y1) box kept clear."""
    out = []
    for i in range(count):
        x, y = random.randint(10, W - 10), random.randint(10, H - 10)
        if avoid and avoid[0] < x < avoid[2] and avoid[1] < y < avoid[3]:
            continue
        r = random.choice([.7, 1, 1, 1.3])
        if i % 5 == 0:
            out.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{STAR}" style="animation:tw {random.uniform(3.5, 7):.1f}s -{random.uniform(0, 7):.1f}s infinite"/>')
        else:
            out.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{STAR}" opacity="{random.uniform(.15, .55):.2f}"/>')
    return out


def save(path, parts):
    with open(path, "w") as f:
        f.write("\n".join(parts))
