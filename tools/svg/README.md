# SVG generators

Generators for the animated SVGs in the Visuals section. `common.py` holds the shared pieces (SVG header and writer, background gradients, nebula, star field, colour helpers, fonts, path helpers, panel titles with their phone sizes and the reduced-motion rule); each other script draws one image and needs a matching tab in `data/visuals.yaml`, which `build.py` checks.

Regenerate every image, or check that the committed ones match their generators:

```sh
python3 tools/svg/build.py
python3 tools/svg/build.py --check
```

A single image can also be written directly:

```sh
python3 tools/svg/kubernetes.py static/images/kubernetes.svg
```

The output is deterministic (fixed random seed), so regenerating without changes produces identical files.
