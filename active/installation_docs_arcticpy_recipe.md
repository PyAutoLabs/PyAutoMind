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
