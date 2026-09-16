# Catalogue: convergence, potential and deflections FITS per lens, collected from finished fits with no refit

Type: feature
Target: euclid
Repos:
- euclid_strong_lens_modeling_pipeline
Themes:
- euclid
- catalogue
Difficulty: easy
Autonomy: supervised
Priority: high
Status: formalised
Issued: 2026-09-16
Consequence: judge
Review-minutes: 15
Unattended: ready
Related: draft/feature/euclid/catalogue_extension_coolest_mass_fits.md (epic euclid-dr1-prep phase 9 — this task delivers its mass-model FITS leg and its retroactive-update verdict; the COOLEST CSV and the magnification plane stay there)
Project: euclid_dr1 (science checkout /mnt/c/Users/Jammy/Science/euclid_dr1, ledger wiki/project/state.md)
Filed: 2026-09-16
Issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/80

User request (verbatim):

"""
For the project euclid_dr1, do this: Update catalogue with .fits convergence, potential, deflections, do a quick run but this should not require a rerun
of any lenses and not require us to worry about updating lens modeling results. But make sure this is the case. I think this should be sich that you can rebuild the catalogue and do all this work without running anything on RAL, but I guess the point is we need to be sure the catalogue generation itself can run on RAL and be updated (noting that when theres 15000 lenses we cant download the whole output folder)
"""

## What is already true (surveyed 2026-09-16)

- Every finished `initial_lens_model` search (both `vis_lp` and `vis_pix`) already writes
  `image/tracer.fits` into its result zip, with extensions `MASK`, `CONVERGENCE`, `POTENTIAL`,
  `DEFLECTIONS_Y`, `DEFLECTIONS_X` (`autolens/lens/plot/tracer_plots.py::fits_tracer`, on the
  mask's zoomed grid with a one-pixel buffer — 102×102 for the 100×100 sep1 cut-outs; ~432 KB
  per file). All 18 sep1 zips under `Science/euclid_dr1/output/` carry it.
- `al.agg.fits_tracer` (`FITSTracer` enum) + `af.AggregateFITS.extract_fits` already read those
  HDUs out of a result zip — the exact mechanism `catalogue/scripts/deblending.py` uses for
  `pre_psf.fits` / `model.fits`. So the products are a **collect**, not a recompute and not a
  refit: the aggregator opens the zips read-only (`unzip_temporary=True`).
- The catalogue already builds on the cluster: `hpc/batch_cpu/submit_build_inspection_bundle`
  runs `scripts/build_inspection_bundle.sh` beside the results, and `hpc/sync pull` pulls
  `inspect/`. Two gaps for a 15 000-lens sample: `hpc/sync pull` always pulls `output/` too
  (there is no way to pull only `inspect/`), and `hpc/sync submit` cannot pass `--export`
  overrides, while the bundle submit script defaults `PROJECT_PATH` to `euclid_dr1_prelim`.

## Deliverables

1. A new catalogue producer (stage between deblending and the CSVs) writing per lens
   `convergence.fits`, `potential.fits` and `deflections.fits` (Y and X HDUs) from the
   `initial_lens_model/vis_pix` result's `tracer.fits`, via `AggregateFITS` — idempotent,
   per-lens failure isolation, same CLI trio as the other producers.
2. Wired into `scripts/build_inspection_bundle.sh`, `catalogue/README.md` (bundle-file table,
   run order, the zoomed-grid note) and the submit script's comments.
3. RAL path made sample-agnostic: `hpc/sync submit`/`push-submit` forward extra sbatch
   arguments; the bundle submit script derives `PROJECT_PATH` from where it was submitted;
   `hpc/sync pull [dir...]` restricts the pull to the named roots so `inspect/` can be
   fetched without `output/`.
4. The quick run: the producer (and the whole bundle) run locally against the 18 sep1 zips in
   `Science/euclid_dr1/output/`, with a before/after checksum of every zip proving no result
   was modified and no search was invoked. Nine lenses get the three files; the incomplete
   `Tile102007299…` is skipped, not half-written.
5. Fast test for the producer's pure parts; `test_repo_invariants` still green.

## Acceptance

- 9/9 completed sep1 lenses carry the three FITS with the expected extension names and shapes;
  zip checksums identical before and after; no `force_pickle_overwrite`, no `sbatch`, no RAL run.
- `bash scripts/build_inspection_bundle.sh` on the local tree is a full pass with the new stage.
- `hpc/sync pull inspect` (dry run via `status`) transfers only `inspect/`.
- Size numbers written down: per-lens bytes for the three files and the 15 000-lens extrapolation.

## Plan (2026-09-16) — APPROVED, STARTED 2026-09-16

The human approved the plan on 2026-09-16 ("I approve but dont start now"). Full two-level plan is on the issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/80. No worktree, no branch, no source edits, nothing on RAL. Resume with `/start_workspace catalogue-mass-maps-fits`.

Started 2026-09-16 via `/start_workspace catalogue-mass-maps-fits`: worktree `~/Code/PyAutoLabs-wt/catalogue-mass-maps-fits`, branch `feature/catalogue-mass-maps-fits`.

Shipped 2026-09-16: PR https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/81 (3a200ee), awaiting merge via /prm.

PyAutoFit fix shipped 2026-09-16: https://github.com/PyAutoLabs/PyAutoFit/pull/1633; pipeline follow-up 13876cb on PR #81; library-first merge.
