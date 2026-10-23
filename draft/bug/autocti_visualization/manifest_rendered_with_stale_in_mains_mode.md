# autocti_visualization manifest `rendered_with:` shows stale source-checkout versions in mains mode

Type: bug
Target: autocti_visualization
Repos:
- autocti_visualization
Difficulty: easy
Autonomy: supervised
Priority: low
Status: draft
Consequence: judge
Filed: 2026-10-23

Since autocti_visualization#8, `render.yml` renders from the library mains by
default (autocti is not on PyPI past 2024.11). `gallery/gallery_build.py` still
stamps `gallery/viz_manifest.yaml` `rendered_with:` (and the `GALLERY.md` header,
via `--version-string`'s default) from `<lib>.__version__`. From a source checkout
that is a stale stamp: after render 40032877406 (commit c4a9752, PyAutoCTI
main@2a91ff5) the manifest says `autocti: 2024.11.13.2`, `autoarray: 2026.8.17.1`,
`autofit: 2026.8.17.1`. PyAutoEyes reads this manifest, so the dashboard shows a
2024 autocti for October figures.

Fix: let the builder take the stack identity from the workflow (e.g. a
`--rendered-with` override or env var set by `render.yml` to `main@<sha>` per
library in mains mode), keeping `__version__` for PyPI mode. Check the PyAutoEyes
read contract (`gallery/viz_manifest.yaml` schema 1) accepts a non-version string
there, or extend it together with the organ. The lens/galaxy/fit siblings render
from PyPI and are unaffected.
