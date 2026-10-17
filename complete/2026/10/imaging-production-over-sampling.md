Phase 1 of the PyAutoPulse `imaging` task `imaging_production_over_sampling` (issue
autolens_profiling#430). Merged 2026-10-17 as
https://github.com/PyAutoLabs/autolens_profiling/pull/431 (MERGED), workspace-only:

- `--over-sampling {flat1,production}` (default `flat1`, historic rows reproduce) for the four
  JAX Delaunay-family imaging cells (`delaunay` / `delaunay_nn` × `likelihood_runtime` /
  `likelihood_breakdown`); production presets resolved by `--instrument`: euclid
  `EUCLID_VIS_PIX`, hst `HST_SOURCE_PIX_2`, with file:line provenance in `_production_config.py`.
- Production rows record their over-sampling configuration and land under `os_production/`.
- CPU functional smoke only: 8/8 production runs exit 0; no rows recorded, no A100 jobs.

Only phase 1 shipped; later phases of the Pulse task (production rows, A100 timing) remain
with the Pulse task. Findings left open in the PR: the HST flat-1 `adapt_split` pin already
drifts on main (29155.000174 vs pinned 29140.296); the numba cells' production threshold reads
the S/N-capped adapt image, so it under-samples relative to production.

## Original prompt

# Imaging production over-sampling presets — phase 1 (workspace-only)

Type: feature
Target: autolens_profiling
Repos:
- autolens_profiling
Difficulty: medium
Autonomy: supervised
Priority: normal
Consequence: judge
Campaign: PyAutoPulse `imaging` / task `tasks/imaging_production_over_sampling.md`
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/430

## Request (verbatim, relayed by the architect session; human authorised 2026-10-17 "Yes launch 1 and 2 now")

Phase 1 as recorded: "workspace-only: --instrument euclid|hst presets for the JAX
Delaunay runtime/breakdown cells, keeping flat-1 selectable; CPU smoke only. A100
re-measure is a separate compute-authorized phase." Evidence/context:
PyAutoArray#606.

Goal: ONE bounded phase. Add `--instrument euclid|hst` presets (production
over-sampling settings as the task and PyAutoArray#606 define them) to the JAX
Delaunay runtime and breakdown cells, keep the current flat sub-size 1 selectable
and the default behaviour unchanged, and verify by CPU smoke (functional run, not
timing) that each preset executes and produces the catalogue-conformant JSON. No
measurements are recorded as campaign evidence in this phase; no A100 jobs.
