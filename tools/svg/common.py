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


FONT = 'font-family="Cambria Math,Georgia,Times New Roman,serif"'
MONO = 'font-family="Consolas,monospace"'


def num(v):
    return f"{v:.1f}".removesuffix(".0")


def pt(x, y):
    return f"{num(x)} {num(y)}"


def poly(points, close=False):
    """Path through (x, y) pairs or complex numbers."""
    xy = ((p.real, p.imag) if isinstance(p, complex) else p for p in points)
    return "M" + " ".join(pt(x, y) for x, y in xy) + ("Z" if close else "")


def motion(name, points):
    """Keyframes that carry an element through (x, y) pairs or complex numbers at an even pace."""
    xy = [(p.real, p.imag) if isinstance(p, complex) else p for p in points]
    n = len(xy) - 1
    body = "".join(f"{100 * i / n:.2f}%{{transform:translate({num(x)}px,{num(y)}px)}}" for i, (x, y) in enumerate(xy))
    return f"@keyframes {name}{{{body}}}"


def title(x, y, body):
    """Panel title, always lowercase; `body` may hold sub() spans."""
    if any(c.isupper() for c in body if c.isascii() and c.isalpha()) and "<" not in body:
        raise ValueError(f"titles are lowercase: {body!r}")
    return f'<text x="{x}" y="{y}" text-anchor="middle" class="ti" {FONT} font-size="25" fill="#ede9fe">{body}</text>'


def subtitle(x, y, body):
    """Smaller line under a title, usually the formula behind it; `body` may hold small() and base() spans."""
    return f'<text x="{x}" y="{y}" text-anchor="middle" class="sbt" {FONT} font-size="18" fill="#c4b5fd" fill-opacity=".85">{body}</text>'


def small(text, up=False):
    """Subscript (or superscript with up=True) inside a subtitle; follow it with base() to return to the baseline."""
    return f'<tspan class="sbs" font-size="12" dy="{-7 if up else 4}">{text}</tspan>'


def base(text, up=False):
    return f'<tspan dy="{7 if up else -4}">{text}</tspan>'


def sub(text, up=False):
    """Subscript (or superscript with up=True) inside a title; follow it with back() to return to the baseline."""
    return f'<tspan class="su" font-size="17" dy="{-10 if up else 6}">{text}</tspan>'


def back(text, up=False):
    return f'<tspan dy="{10 if up else -6}">{text}</tspan>'


def curiosity(x, y, text):
    """A one-line fact in small print; hidden on phones, where it would be too small to read."""
    return f'<text x="{x}" y="{y}" text-anchor="middle" class="cu" {MONO} font-size="13" fill="{STAR}" fill-opacity=".6">{text}</text>'


def mobile(rules=""):
    """Phone sizes: titles and subscripts are shared, `rules` adds the image's own."""
    return f"@media (max-width:520px){{.ti{{font-size:34px}}.su{{font-size:23px}}.sbt{{font-size:26px}}.sbs{{font-size:17px}}.cu{{display:none}}{rules}}}"


def svg_open(label, x=0, y=0):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x} {y} {W} {H}" preserveAspectRatio="xMidYMid slice" role="img" aria-label="{label}">'


DEFS = [
    '<radialGradient id="nb1"><stop offset="0" stop-color="#4338ca" stop-opacity=".42"/><stop offset="1" stop-color="#4338ca" stop-opacity="0"/></radialGradient>',
    '<radialGradient id="nb2"><stop offset="0" stop-color="#a21caf" stop-opacity=".36"/><stop offset="1" stop-color="#a21caf" stop-opacity="0"/></radialGradient>',
    '<radialGradient id="hl"><stop offset="0" stop-color="#fff" stop-opacity=".5"/><stop offset=".4" stop-color="#fff" stop-opacity=".15"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>',
]


def base_css(hidden=".mv", shown=None):
    """Twinkle keyframes plus the reduced-motion rule: `hidden` elements disappear and `shown` ones (a still stand-in) appear."""
    extra = f"{hidden}{{opacity:0}}" if hidden else ""
    still = [f"{shown}{{display:none}}"] if shown else []
    if shown:
        extra += f"{shown}{{display:inline}}"
    return [
        "@keyframes tw{0%,100%{opacity:.15}50%{opacity:.9}}",
        *still,
        f"@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}{extra}}}",
    ]


def nebula(left=(450, 350), right=(770, 350), rx=(360, 340), ry=250):
    """Two soft glows; each must fit inside the canvas, or its gradient is cut into a visible edge."""
    for (cx, cy), r in ((left, rx[0]), (right, rx[1])):
        if cx - r < 0 or cx + r > W or cy - ry < 0 or cy + ry > H:
            raise ValueError(f"nebula at ({cx}, {cy}) with radii ({r}, {ry}) leaves the {W}x{H} canvas")
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


def write_svg(path, label, defs, css, body, x=0, y=0):
    save(path, [svg_open(label, x, y), *defs, "<style>" + "".join(css) + "</style>", *body, "</svg>"])


def save(path, parts):
    with open(path, "w") as f:
        f.write("\n".join(parts))
