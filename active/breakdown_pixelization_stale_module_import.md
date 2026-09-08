# Post-#235 profiling follow-ups: stale pixelization import; Euclid preset lp bins [4,4,2]

Type: bug
Target: autolens_profiling
Repos:
- @autolens_profiling
Difficulty: easy
Autonomy: safe
Priority: normal
Status: formalised
Consequence: glance
Witness: `python scripts/imaging/likelihood_breakdown/pixelization.py --instrument hst` runs to completion on main and its EXPECTED_LOG_EVIDENCE pin is re-measured (dated comment) after the lp [4,2,2] change from #235; and `_production_config.py`'s Euclid vis_pix preset carries lp radial bins [4,4,2] (matching euclid_strong_lens_modeling_pipeline `util.py` after PR #56) with the four Euclid numba cell rows re-run and re-pinned.
Review-minutes: 2
Unattended: ready
Issued: 2026-09-08
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/237
Filed: 2026-09-08

Original request (verbatim, surfaced by the #235 implementation): "`likelihood_breakdown/pixelization.py` pin could not be re-measured. The cell raises at step 5 on `main` too — `from autoarray.inversion.mesh.mesh.rectangular_adapt_density import overlay_grid_from`, a module PyAutoArray split into `rectangular_bilinear_adapt_density` / `rectangular_rtu_adapt_density`. Pre-existing, unrelated to #235."

Context: the JAX rectangular breakdown cell is the only imaging cell that did not run under #235; its pin carries a comment saying it was not re-measured. Fix the import (pick the bilinear module, which is the default rectangular mesh), run the cell once for hst, re-pin, and confirm `build_readme.py --check` stays clean.

Second item (surfaced at /prm close-out of #235): PR euclid_strong_lens_modeling_pipeline#56 raised the production lp radial bins to `[4,4,2]` because sub-size 2 in the 0.1-0.3" annulus under-integrates a compact source by ~0.6 % (the old [4,2,1] magnification agreement was two under-integrations cancelling). The Euclid preset in `autolens_profiling/_production_config.py` still says `[4,2,2]` with provenance to `util.py`, so its "matches production" claim is stale. Update the preset (and the HST preset only if subhalo_validation adopts [4,4,2] too — check `/mnt/c/Users/Jammy/Science/subhalo_validation/scripts/imaging.py`), re-run the Euclid Delaunay + rectangular numba cells (breakdown + runtime), re-pin with dated comments, refresh `results/notes/production_representative_cells.md` and the README tables.

