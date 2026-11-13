"""Regenerate every animated SVG of the Visuals section, or check that they are up to date.

    python3 tools/svg/build.py           # write static/images/<name>.svg for every generator
    python3 tools/svg/build.py --check   # exit 1 if any committed SVG differs from its generator
"""
import subprocess
import sys
import tempfile
import xml.dom.minidom
from pathlib import Path

HERE = Path(__file__).resolve().parent
IMAGES = HERE.parent.parent / "static" / "images"
VISUALS = HERE.parent.parent / "data" / "visuals.yaml"
SKIP = {"common", "build"}


def tabs_match(generators):
    """Every generator needs a tab in data/visuals.yaml and every tab a generator."""
    tabs = {line.removeprefix("- id:").strip() for line in VISUALS.read_text().splitlines() if line.startswith("- id:")}
    for name in sorted(generators - tabs):
        print(f"NOTAB {name}.py has no entry in {VISUALS.name}")
    for name in sorted(tabs - generators):
        print(f"NOGEN {VISUALS.name} lists {name} but there is no {name}.py")
    return tabs == generators


def main():
    check = "--check" in sys.argv[1:]
    stale = []
    if not tabs_match({p.stem for p in HERE.glob("*.py")} - SKIP):
        stale.append(VISUALS.name)
    for script in sorted(HERE.glob("*.py")):
        if script.stem in SKIP:
            continue
        target = IMAGES / f"{script.stem}.svg"
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / target.name
            subprocess.run([sys.executable, str(script), str(out)], check=True)
            fresh = out.read_bytes()
        try:
            xml.dom.minidom.parseString(fresh)
        except Exception as e:
            sys.exit(f"INVALID {target.name}: {e}")
        if check:
            ok = target.exists() and target.read_bytes() == fresh
            print(f"{'ok   ' if ok else 'STALE'} {target.name}")
            if not ok:
                stale.append(target.name)
        else:
            target.write_bytes(fresh)
            print(f"wrote {target.name} ({len(fresh) // 1024} KB)")
    if stale:
        sys.exit(1)


if __name__ == "__main__":
    main()
