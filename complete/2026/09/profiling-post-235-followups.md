- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/237
- completed: 2026-09-08
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/238
- merged: autolens_profiling 242fe12 (PR #238)
- heart-ack: 2026-09-08 in-session, same reason set as #235 — "workspace validation not passing (5 failed, 2 timeout, cloud#34099198772 …)" and "release validation incomplete: no rehearsal for current source"; neither reason touches autolens_profiling

**Summary.** Both post-#235 profiling follow-ups shipped in one PR. The JAX rectangular breakdown cell's `overlay_grid_from` import was repointed to `rectangular_rtu_adapt_density` — the helper lives in the **RTU** module, which the bilinear mesh subclasses, not in the bilinear module the prompt guessed at — so `likelihood_breakdown/pixelization.py` runs to completion for `--instrument hst` and its `EXPECTED_LOG_EVIDENCE` pin is re-measured with a dated comment. Both Euclid presets in `_production_config.py` now carry lp radial bins `[4, 4, 2]`, matching `euclid_strong_lens_modeling_pipeline` `util.py` after pipeline#56, closing the stale "matches production" claim #235 left behind; the four Euclid numba cell rows (Delaunay + rectangular, breakdown + runtime) were re-run and re-pinned, and `results/notes/production_representative_cells.md` plus the README dashboards were regenerated.

**Witness.** Met: the pixelization cell runs and is re-pinned; the Euclid preset reads `[4, 4, 2]`. Smoke 12 of 12; `build_readme.py --check` clean; lint green.

**Traps / notes.**
- The PyAutoArray split put `overlay_grid_from` in the RTU module and left the bilinear mesh subclassing it. Picking the "default rectangular mesh" module, as the prompt suggested, would have failed the same way — read the split before repointing an import.
- The HST preset stays at `[4, 2, 2]`: `subhalo_validation` has not adopted `[4, 4, 2]`, so raising it here would have broken the provenance claim in the other direction.
- autolens_profiling README tables are generated — `build_readme.py --check` runs in lint, so re-pinned rows need the regenerated dashboards in the same PR.

**Follow-ups.** None filed. `subhalo_validation` needs the same middle-bin decision the Euclid pipeline took, but only if it computes flux latents; recorded on the `workspace-lp-sub-size-1-retire` record.

## Original prompt

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

