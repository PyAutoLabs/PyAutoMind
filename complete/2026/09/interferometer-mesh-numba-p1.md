# interferometer-mesh-numba-p1 — mesh numba CPU breakdown via library dispatch (campaign 3/3, phase 1)

- Repo: autolens_profiling
- Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/326
- PR: https://github.com/PyAutoLabs/autolens_profiling/pull/328 (MERGED, merge `ea2711d9`, 2026-09-27; lint green)
- Epic: interferometer-likelihood-campaign (phase map `draft/research/autolens_profiling/interferometer_mesh_breakdown_numba_cpu_decision_matrix.md`)
- Workspace-only; no library PR, no pending-release. Heart YELLOW acked at ship (manifest drift + no rehearsal; none touch autolens_profiling).

## Shipped scope

- New NumPy/numba library-dispatch breakdown harness
  `scripts/misc/likelihood_breakdown/interferometer_pixelized_numpy.py` (times the library's own
  `InversionInterferometerSparseNumba` / `InversionInterferometerSparse(xp=np)` steps on the JAX
  harness's inputs); shared setup + `--mask-radius` on the JAX harness; thin numba cells
  (`delaunay_numba.py` / `pixelization_numba.py`).
- 8 RAL CPU submits `hpc/batch_cpu/submit_breakdown_interferometer_{delaunay,pixelization}_numba_ral_*`.
- RAL CPU fp64 rows for sma / alma / alma_high on both meshes plus the alma N sweep
  (`results/breakdown/interferometer/**`).

## Findings

- numba is 2-4x faster than NumPy FFT at sma and alma; it loses at alma_high (nnz/col 118-162),
  where JAX-CPU is fastest.
- Witness PASS: gated arm `configuration.inversion_path == InversionInterferometerSparseNumba`;
  numba vs FFT log-evidence <= 9.1e-13 nat; step sum / full call 0.996-1.006.
- Human decision 2026-09-27: keep the May-18 sma adapt image; pins re-set.

## Follow-ups

- Campaign phases 2 (in-situ crossover) and 3 (A100 mask-radius sweep) are now unblocked.
- `draft/feature/autoarray/interferometer_sparse_numpy_cache_curvature_and_data_vector.md`.
- RAL worktree `/mnt/ral/jnightin/autolens_profiling_wt/interferometer-mesh-numba-p1` left in place.

## Original prompt

# Interferometer likelihood campaign 3/3 — phase 1: library-dispatch numba CPU breakdown cells

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- interferometer
- numba-cpu
- likelihood-profiling
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: glance
Witness: the gated-arm breakdown JSON under `results/breakdown/interferometer/` records `configuration.inversion_path == "InversionInterferometerSparseNumba"`, its numba vs NumPy-FFT log-evidence differ by <= 0.5 nat (expect ~1e-8), and its step sum is within 10 % of the full library `FitInterferometer` call.
Review-minutes: 8
Lane: local-dev
Epic: interferometer-likelihood-campaign
Filed: 2026-09-27
Issued: 2026-09-27
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/326
Campaign: draft/research/autolens_profiling/interferometer_mesh_breakdown_numba_cpu_decision_matrix.md

Phase 1 of the campaign prompt above (retained in `draft/` as the campaign intent; its
campaign contract and #235 discipline govern). Plan approved by the human 2026-09-27.

## Context

`scripts/interferometer/likelihood_breakdown/delaunay_numba.py` / `pixelization_numba.py`
still time the prototype pack (`scripts/misc/numba_interferometer/inversion`), not the
library dispatch. Since PyAutoArray #544/#545, `inversion_interferometer_from`
(`autoarray/inversion/inversion/factory.py:166-321`) routes to
`InversionInterferometerSparseNumba` (`direct_conv`) when `xp is np`, one mapper,
`sub_fraction == 1` and mean nnz/col <= `Settings.interferometer_numba_nnz_per_source_max`
(`general.yaml:21` = 60.0), else to `InversionInterferometerSparse` (FFT). The shared harness
`scripts/misc/likelihood_breakdown/interferometer_pixelized.py` is JAX-only.

## What

1. New sibling harness `scripts/misc/likelihood_breakdown/interferometer_pixelized_numpy.py`
   reusing the JAX harness's dataset / mesh / adapt setup (shared code imported, not copied,
   where clean; the JAX harness's outputs stay bit-identical). Three arms on identical
   inputs selected through `Settings(interferometer_numba_nnz_per_source_max=...)`:
   - **numba** (gate forced to admit) — `InversionInterferometerSparseNumba`;
   - **NumPy FFT** (gate 0) — `InversionInterferometerSparse(xp=np)`;
   - **JAX-CPU FFT** — pointer / row from the existing JAX harness on identical inputs.
   The JSON records `configuration.inversion_path` and the cell asserts the path it asked for.
   Steps: triplets, D, F (numba kernel incl. `kernel_index_arrays` marshalling vs rfft2
   blocks), regularisation, fnnls solve, log-det (fnnls Cholesky reuse), chi-squared; full
   call via the library `FitInterferometer`; step-sum / full ratio; log-evidence pins
   (`pinned_expected` / `pinned_drift`); peak RSS; nnz per source column.
2. `--mask-radius` on both harnesses (default = preset 3.5; W~ preload cache filename keyed by
   radius; JSON name suffix `_r{radius}` only when non-default so r3.5 outputs keep names).
3. Re-point `delaunay_numba.py` / `pixelization_numba.py` at the new harness as thin CLI
   wrappers; `scripts/misc/numba_interferometer/` untouched.
4. RAL CPU submits `hpc/batch_cpu/submit_breakdown_interferometer_{delaunay,pixelization}_numba_ral_{sma,alma,alma_high}_fp64`
   plus an alma N sweep (Delaunay 1000/1500/2500/4000; rect 32²/39²/50²/64²), copying
   `hpc/batch_cpu/submit_breakdown_imaging_fixed_light_numba_delaunay_ral_hst_fp64`
   (`gpu` partition, no `--gres`, 4 CPUs, `NUMBA_NUM_THREADS=1`, BLAS pinned);
   `check_submits.py --check` green.

## Verification

- Local sma, both meshes, all arms: `inversion_path` asserts, numba vs FFT log-evidence
  <= 1e-6 nat, `FitInterferometer.figure_of_merit` reproduction, step sum / full in [0.9, 1.1],
  peak RSS logged.
- Repo lint as CI: ruff, ruff format --check, `build_readme.py --check`,
  `check_submits.py --check`, `pytest scripts/misc/test/`, smoke scripts (PYTHONPATH on the
  local library mains).
- RAL: jobs complete with 0 Tracebacks; JSON `source_revisions` match the library mains
  (check the RAL venv against dependency floors first — numba, nufftax).

## Out of scope

Crossover sweep and gate retune (phase 2), A100 mask-radius jobs (phase 3), the decision matrix
(phase 4), any library edit.
