# matplotlib 3.11 breaks corner plotting (arviz-plots incompatibility) — cap it

Type: bug
Target: PyAutoConf
Difficulty: small
Autonomy: safe
Priority: high
Status: formalised

Discovered 2026-07-10 during the markdown-renderings rollout. matplotlib is
**unpinned** in every library requirements.txt (PyAutoConf/PyAutoFit/PyAutoArray/
PyAutoGalaxy/PyAutoLens), so a fresh `pip install` today resolves matplotlib
**3.11.0** (released recently). matplotlib 3.11 removed `matplotlib.style.core`,
which `arviz-plots` 1.0.0 imports at module load
(`arviz_plots/__init__.py: mplstyle.core.USER_LIBRARY_PATHS.append(...)`).
`corner` → `arviz` → `arviz_plots`, so **any script calling
`aplt.corner_cornerpy(...)` crashes at import** with
`AttributeError: module 'matplotlib.style' has no attribute 'core'`.

This hit every workspace `modeling.py` (corner posterior plot) and would hit any
user on matplotlib>=3.11 + arviz-plots<=1.0.0. Locally worked around by pinning
`matplotlib==3.10.9` in the shared venv (a concurrent session had bumped it to
3.11.0 at 11:41, silently breaking corner across all active sessions).

Fix: add a matplotlib upper cap (`matplotlib<3.11`) to the requirements where
the plotting stack is declared — OR bump the arviz-plots floor to a version
compatible with matplotlib 3.11 if one exists (check upstream). Verify: fresh
venv install + run a modeling script's `corner_cornerpy` cell. Decide the right
home for the cap (PyAutoConf owns the config/deps handshake; the plotting deps
may live in PyAutoFit). See [[markdown-example-renderings]].
