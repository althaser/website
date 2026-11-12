# SVG generators

Generators for the animated SVGs in the AI section. Each script writes the SVG to the path given as its only argument:

```sh
python3 tools/svg/kubernetes.py static/images/kubernetes.svg
```

The output is deterministic (fixed random seed), so regenerating without changes produces an identical file.
