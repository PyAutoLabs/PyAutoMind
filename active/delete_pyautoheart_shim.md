# Delete the dead pyautoheart/ compatibility shim

Type: maintenance
Target: PyAutoHeart
Repos:
- PyAutoHeart
Difficulty: trivial
Autonomy: supervised
Priority: normal
Status: formalised

Filed 2026-07-16 from a repo census. Original request (verbatim): "PyAutoHeart,
heart and pyautoheart folders, feel duplicated / redudant and hsouldnt it be
autoheart if anything? i.e. do a quick census of PyAutoHeart" — census done in
session, user approved the deletion recommendation ("ok go").

## Why

`pyautoheart/` is a 6-line compatibility shim (`from heart import *`) created
by the PyAutoPulse→PyAutoHeart rename (#18, commit a2543d0) alongside the
`pulse/` / `pyautopulse/` wrappers. The Phase-2 retirement of the Pulse compat
surface (#28, commit a6f9083) deleted the pulse-era wrappers but missed this
one. Census confirmed **zero importers** of `pyautoheart` anywhere in the
workspace (PyAutoBrain mentions are repo-name routing strings, not imports),
and the package is never pip-installed (repo-local via `bin/pyauto-heart`).

## Scope

- Delete `PyAutoHeart/pyautoheart/` (single `__init__.py`).
- In `PyAutoHeart/pyproject.toml`, drop `"pyautoheart*"` from
  `[tool.setuptools.packages.find] include` (keep `name = "pyautoheart"` —
  that is the distribution name, not the import name).

Out of scope: renaming `heart/` → `autoheart` to match the org convention
(autofit/autoconf/autobuild). Heart is never installed into site-packages, so
the rename is cosmetic churn today; revisit only if Heart ever ships as a
package.

## Verify

- `grep -rn "import pyautoheart\|from pyautoheart" .` across the workspace → no hits.
- `pytest tests/ -q` in PyAutoHeart passes.
- `bin/pyauto-heart status` still runs.
