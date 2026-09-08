# likelihood_breakdown/pixelization.py imports a module PyAutoArray split

Type: bug
Target: autolens_profiling
Repos:
- @autolens_profiling
Difficulty: easy
Autonomy: safe
Priority: normal
Status: formalised
Consequence: glance
Witness: `python scripts/imaging/likelihood_breakdown/pixelization.py --instrument hst` runs to completion on main and its EXPECTED_LOG_EVIDENCE pin is re-measured (dated comment) after the lp [4,2,2] change from #235.
Review-minutes: 2
Unattended: ready
Filed: 2026-09-08

Original request (verbatim, surfaced by the #235 implementation): "`likelihood_breakdown/pixelization.py` pin could not be re-measured. The cell raises at step 5 on `main` too — `from autoarray.inversion.mesh.mesh.rectangular_adapt_density import overlay_grid_from`, a module PyAutoArray split into `rectangular_bilinear_adapt_density` / `rectangular_rtu_adapt_density`. Pre-existing, unrelated to #235."

Context: the JAX rectangular breakdown cell is the only imaging cell that did not run under #235; its pin carries a comment saying it was not re-measured. Fix the import (pick the bilinear module, which is the default rectangular mesh), run the cell once for hst, re-pin, and confirm `build_readme.py --check` stays clean.
