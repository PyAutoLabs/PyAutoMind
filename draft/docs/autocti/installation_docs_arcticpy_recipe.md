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
Blocked-by: draft/maintenance/pyautoheart/arcticpy_pin_bump_after_upstream_release.md (the recipe text depends on whether upstream ships wheels)

Follows the PyAutoBrain `skills/WRITING_STYLE.md` rules: human-first, a short
start, no jargon. If the lazy import (shipped 2026-11-05, complete/2026/11/arcticpy-lazy-import.md)
has shipped, say that `import autocti` works without arcticpy and that clocking
needs it.
