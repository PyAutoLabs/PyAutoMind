## Outcome
PyAutoCTI's installation pages no longer tell people to run a bare `pip install arcticpy`, which on numpy 2 installs 2.6 and downgrades numpy. They now give one recipe that matches PyAutoHeart `install_arcticpy.sh`, `.readthedocs.yaml` and the pyproject note: GSL headers, `pip install --upgrade pip setuptools wheel`, `pip install "numpy>=2" "cython>=3" scipy matplotlib`, then `pip install "arcticpy @ git+https://github.com/jkeger/arctic@6f5153582aca00b7b0cc11ab04b2c58a7502400d" --no-build-isolation --no-deps`. Each page says this becomes `arcticpy==2.7` once it reaches PyPI.

- PyAutoLabs/PyAutoCTI#134 (merged 65b1e7d, 2026-11-26; closes PyAutoCTI#133): `docs/installation/{pip,conda,arctic,troubleshooting,overview}.rst`.
  - pip.rst / conda.rst: new arCTIc section with the recipe and an import check; says `import autocti` works without arcticpy (lazy import, `complete/2026/11/arcticpy-lazy-import.md`) and that clocking needs it.
  - arctic.rst: the reference page. Drops the false claim that `pip install autocti` installs arcticpy and the stale 2.1 `pip show` output; explains each flag; links the Heart script.
  - troubleshooting.rst: missing GSL, numpy downgraded, missing `setuptools.build_meta`, missing scipy/matplotlib. `arcticpy_no_gsl` kept only as a labelled last resort with a numpy-downgrade warning.
- Tier `glance`, merged in shift 2026-11-26-pm by an independent close-out session (Opus 5.5): witness held on head b709258 (recipe on every page; no page recommends a bare `pip install arcticpy`; `arcticpy_no_gsl` only under "Last resort"; docs-build green), public-names CLEAN, Heart PyAutoCTI dev-ship green, ci-verdict GREEN (unittest 3.12/3.13/nojax + docs-build; skipped job was the Heart feed refresh, not a test).

## Follow-ups
- When 2.7 reaches PyPI, `draft/maintenance/pyautoheart/arcticpy_pin_bump_after_upstream_release.md` now also lists `docs/installation/{pip,conda,arctic}.rst` among the PyAutoCTI lines to switch to `arcticpy==2.7`.

## Original prompt

# autocti docs: rewrite installation pages around the arcticpy recipe

Type: docs
Target: autocti
Repos:
- @PyAutoCTI
Themes:
- cti
- install
- docs
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: glance
Witness: `docs/installation/{pip,conda,arctic,troubleshooting}.rst` give one working recipe: install autocti, then arcticpy via the PyAutoHeart `install_arcticpy.sh` steps, or plain `pip install arcticpy==<pin>` once upstream ships wheels. No page says a bare `pip install arcticpy` works on numpy 2. `arcticpy_no_gsl` appears only as the documented fallback. The RTD build is green.
Review-minutes: 5
Unattended: ready
Lane: any
Epic: cti-upkeep
Phase: 2c
Unblocked: 2026-11-26 by the 2.7 git-source stopgap (complete/2026/11/arcticpy-27-git-source.md) — document the pinned-commit recipe (`pip install "arcticpy @ git+https://github.com/jkeger/arctic@6f5153582aca00b7b0cc11ab04b2c58a7502400d" --no-build-isolation --no-deps` after numpy>=2, cython>=3, GSL); the PyPI bump later switches it to `arcticpy==2.7`.

Follows the PyAutoBrain `skills/WRITING_STYLE.md` rules: human-first, a short
start, no jargon. If the lazy import (shipped 2026-11-05, complete/2026/11/arcticpy-lazy-import.md)
has shipped, say that `import autocti` works without arcticpy and that clocking
needs it.
