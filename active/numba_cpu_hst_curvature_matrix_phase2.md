# Numba CPU likelihood at HST resolution, phase 2: the mapper×mapper block and the MGE operated matrix

Type: feature
Epic: none (successor to `numba_cpu_hst_curvature_matrix_speedup`, PyAutoArray#505)
Target: autoarray
Repos:
- @PyAutoArray
- @PyAutoGalaxy
- @autolens_profiling
Themes:
- numba-cpu
- pixelization
- profiling
Difficulty: large
Autonomy: supervised
Priority: high
Status: active
Filed: 2026-08-28
Issued: 2026-08-28
Blocked-by: PyAutoArray#505

## Original request

> yeah do that phase 2

(in reply to: "What's left for a phase 2, if you want one: mapper×mapper (0.28 s) and the MGE
operated matrix (0.22 s) now lead at HST.")

## Context

PyAutoArray#505 (branch `feature/numba-hst-curvature-matrix-speedup`, shipping 2026-08-28) routed
the mapper × linear-func block of the curvature matrix F through the batched FFT `Convolver`
(`Convolver.reversed_kernel`), taking F 1.20 → 0.36 s and the HST rectangular numba evaluation
1.56 → 0.60 s (`OMP_NUM_THREADS=1`, `AUTOARRAY_NUMBA_OPERATED_MEMO=0`, paired same-session
measurements; note in `autolens_profiling/results/notes/numba_curvature_matrix_f_split.md`).

Post-#505 HST rectangular split (0.60 s/eval):

| step | s | share |
|---|---|---|
| F: mapper×mapper [numba sparse-op / w-tilde contraction] | 0.277 | 46% |
| MGE operated mapping matrix (60 funcs, per-eval convolution of varying profiles) | ~0.22 | ~37% |
| F: mapper×linear-func [FFT conv + scatter] | 0.054 | 9% |
| everything else | ≤ 0.02 each | |

Delaunay-1250: mapper×mapper 0.123 s of 0.76 s; F is no longer dominant there — the inversion build
(~0.5 s) is, which is out of scope here.

## Plan findings (2026-08-28)

Two read-through findings changed the task's shape at planning time. First, the **MGE half of the
cost lives in PyAutoGalaxy, not PyAutoArray**: the #505 `Convolver` batching is already applied in
`LightProfileLinearObjFuncList.operated_mapping_matrix_override` (the 60 Gaussians are stacked into
one convolution) and scipy already skips the length-60 axis, so the bulk of the ~0.22 s is the 120
per-profile image evaluations, all of which recompute an identical transform and eccentric-radius
grid because the MGE basis shares `centre`/`ell_comps` and varies only in `sigma` — hence
`@PyAutoGalaxy` added to Repos above. Second, **two of the four mapper×mapper candidate levers are
dead on arrival**: upper-triangle symmetry is already exploited (the sparse preload stores
`ip1 >= ip0` and the kernel folds `A + Aᵀ`) and unique-mappings compression is already what the
kernel iterates over. The live lever is a **two-stage reformulation** — a per-data-pixel dense
source-space accumulator followed by contiguous AXPYs.

## Goal

Take the HST rectangular numba evaluation from ~0.60 s to ≤ ~0.35 s with the log-likelihood
unchanged to pinned tolerance (pins: hst rectangular 27661.910133664103, hst-rtu
27180.704715696862, hst-delaunay 29090.52721044813; rtol 1e-6 where summation order changes,
bit-identical otherwise).

1. **Decompose first, as in #505.** Instrument the mapper×mapper kernel
   (`inversion_imaging_numba_util.py`, sparse-op diag + off-diag kernels) and the MGE operated
   mapping matrix step in the `autolens_profiling` breakdown harness; record the split at hst +
   euclid rectangular and hst Delaunay-1250. Checkpoint: the split picks the lever.
2. **mapper×mapper candidates**, cheapest first: unique-mappings compression (is the inner loop over
   data pixels × PSF footprint × source pixels where a per-unique-mapping formulation is smaller);
   upper-triangle-only + mirror; whether the preloaded PSF-precision products are fully exploited
   (nothing mapper-independent recomputed per evaluation); `prange` measured both at
   `OMP_NUM_THREADS=1` and under the Nautilus pool.
3. **MGE operated matrix candidates**: determine FFT- vs scatter-bound; batch the varying profiles
   through the same `Convolver` path as #505 if the per-func convolution is the cost; check whether
   any profile subset is invariant across evaluations for a given model (memo, already
   `AUTOARRAY_NUMBA_OPERATED_MEMO`).
4. Ship behind parity tests; `test_autoarray` green; smoke
   `autolens_workspace/scripts/imaging/features/pixelization/cpu_fast_modeling.py`; paired
   before/after on the four breakdown cells + one Nautilus pool run; note in `autolens_profiling`.

Out of scope: the JAX path; RTU / kernel-CDF meshes (GPU-only by decision); the Delaunay inversion
build; the NNLS solve.
