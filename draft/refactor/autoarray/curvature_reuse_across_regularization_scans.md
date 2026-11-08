# Reuse the mapper curvature matrix across regularization-only refits

Type: refactor
Target: autoarray
Repos:
- PyAutoArray
- HowToLens
- HowToGalaxy
Themes:
- ci-smoke
- performance
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft
Consequence: judge
Route: profiling (the cost is inside the inversion, not a CI lever)
Filed: 2026-11-08

## Why (measured)

Four HowTo scripts are the top of Heart's smoke-script ranking (board 2026-11-08T11:40Z):

| Script | slowest leg | share of leg |
|---|---|---|
| HowToLens chapter_3_pixelizations/tutorial_6_adaptive_reconstruction.py | 67.7s | 25% |
| HowToGalaxy chapter_3_pixelizations/tutorial_4_adaptive_reconstruction.py | 61.9s | 29% |
| HowToLens chapter_3_pixelizations/tutorial_5_fit_problems.py | 60.3s | 22% |
| HowToGalaxy chapter_3_pixelizations/tutorial_3_fit_problems.py | 56.5s | 26% |

These scripts were added in the 2026-11-04 chapter-3 rewrite. They are new coverage
and caused the HowToLens/HowToGalaxy gate step change; they are not a regression.

Local reproduction (py3.12, libraries from main, the smoke profile plus the scripts'
own `ENV: full_datasets`): HowToLens tutorial_6 takes 98s under cProfile and 88–92s
without it. Split:

- **Curvature matrix: about 62s.** `Inversion._curvature_matrix_mapper_diag` → `SparseOperator.curvature_matrix_diag_from`
  runs 118 times at about 0.52s per call, including about 14s of JAX compilation (132
  backend compiles: the eager `lax.fori_loop` closes over a new `body` on every call, so
  nothing is reused, and each compile is about 0.1s, which is under JAX's persistent-cache
  minimum, so the CI JAX cache does not help).
- Plots: about 10s (14 × `subplot_fit`).
- The remainder: Delaunay mapping and regularization.

The script performs about 114 inversions by design: 13-point logspace coefficient scans
for each mesh, a 5×5 adaptive-coefficient grid, and weight-power and weight-floor
trials. In the coefficient scans **the mesh, mapper and data are fixed and only the
regularization changes**, so the curvature matrix F = AᵀWA is recomputed identically
13 or 25 times.

Ruled out:
- the numba cache (cold and warm are equal for this script);
- the sparse operator versus the dense mapping route (removing
  `apply_sparse_operator()` gives 96s against 98s);
- dropping `full_datasets` (the tutorial declares it deliberately, and dropping it would
  change what the lesson's evidence comparison demonstrates).

## Proposed approach (for /profiling → start_dev)

1. In PyAutoArray, let an inversion take a preloaded curvature matrix or mapper
   triplets when the mapper is unchanged. The docstring of `_curvature_matrix_mapper_diag`
   already notes "separate ... to enable preloading". Expose it through an existing
   preload or adapt mechanism, not a new user-facing argument, unless /profiling prefers one.
2. Separately: hoist `curvature_matrix_diag_from`'s `body` into a module-level function
   jitted on static (S_pad, B, M), so repeated same-shape calls stop retracing and
   recompiling. That is about 14s per tutorial, and it also benefits users' own scans.
3. Use it in the tutorials only if it stays idiomatic. The user-facing script must not
   gain smoke-only code.

Acceptance:
- log evidences identical to the 7th significant figure. The current run prints
  Overlay 15907.596 / Hilbert 16432.066 / best 16687.2655, which can serve as a witness;
- the HowToLens tutorial_6 local time is re-measured cold and warm before and after;
- no assertion or tolerance changes.
