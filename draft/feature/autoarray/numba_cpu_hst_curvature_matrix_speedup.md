# Numba CPU likelihood at HST resolution: speed up the curvature matrix F (the 78% step)

Type: feature
Epic: none (successor to numba-cpu-likelihood, COMPLETE 2026-08-28)
Target: autoarray
Repos:
- @PyAutoArray
- @autolens_profiling
Themes:
- numba-cpu
- pixelization
- profiling
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Filed: 2026-08-28

> Successor to epic `numba-cpu-likelihood` (`epics.md`; records `complete/2026/08/numba-cpu-*.md`).
> That epic took the numba CPU (`use_jax=False`, `apply_sparse_operator_cpu()`) likelihood from
> 21.3 s → 1.25 s per evaluation at HST resolution on the default `RectangularBilinearAdaptDensity`
> mesh and 4.5 → ~1.6 s on the Delaunay-1250 fiducial. What is left is one step.

## Where the time goes now (2026-08-28, `pixelization_numba.py` / `delaunay_numba.py` breakdowns, `OMP_NUM_THREADS=1`, `AUTOARRAY_NUMBA_OPERATED_MEMO=0`, PyAutoArray main 1f5c636e)

| step | hst rectangular (1.28 s) | euclid rectangular (0.36 s) | hst Delaunay-1250 (3.22 s) |
|---|---|---|---|
| **Curvature matrix F [numba sparse-op]** | **0.997 s (78%)** | **0.211 s (59%)** | **1.77 s (55%)** |
| MGE operated mapping matrix (60 funcs) | 0.189 s | 0.077 s | — |
| Reconstruction solve (warm-started NNLS) | 0.008 s | 0.008 s | 0.54 s (warm: ~0.07 s) |
| everything else | ≤ 0.03 s each | ≤ 0.02 s each | inversion build ~0.5 s |

F is the `curvature_matrix` of `InversionImagingSparseNumba`
(`autoarray/inversion/inversion/imaging_numba/sparse.py`, kernels in
`inversion_imaging_numba_util.py`): the mapper × PSF-precision-operator × mapper contraction over the
sparse-operator (w-tilde heritage) representation, plus the linear-func blocks (already noise-weighted
once and mirrored, phase 1). It is rebuilt every evaluation because the mapper changes with the mass
model — no cross-evaluation memo applies.

## Goal

Make F substantially cheaper on the numba CPU path at HST resolution (target: ≥ 2× on the F step,
i.e. an HST rectangular evaluation ≤ ~0.7 s; Delaunay similar), with the log-likelihood unchanged to
pinned tolerance (`delaunay_numba.py` / `pixelization_numba.py` pins; hst rectangular pin
27661.910133664103).

1. **Step 0 — decompose F itself.** The breakdown cells time `fit.inversion.curvature_matrix` as one
   step. Instrument the kernel(s) behind it (mapper-mapper block, mapper-linear-func blocks,
   linear-func-linear-func block, any dense fill / symmetrisation / noise weighting) and record the
   split at hst + euclid, rectangular (default) + Delaunay. Commit the re-baseline artifacts from the
   2026-08-28 re-profile too (`pixelization_numba_breakdown_{euclid,hst}` incl. the `_rtu` variants —
   numbers in `complete/2026/08/numba-cpu-kernel-cdf-fast-path.md`; regenerate, do not hand-copy).
2. **Pick the lever from the split**, not from doctrine. Candidates to evaluate, cheapest first:
   - the unique-mappings compression (`data_slim_to_pixelization_unique_from`) — is F's inner loop
     iterating over data pixels × PSF footprint × source pixels where a per-source-pixel / per-unique
     -mapping formulation would be smaller;
   - symmetry — compute the upper triangle only and mirror (the linear-func blocks already do);
   - `numba.prange` over the outer loop with the OMP thread count (the campaign runs one process per
     core under Nautilus, so gains must be measured with `OMP_NUM_THREADS=1` AND with the pool);
   - reuse across evaluations of whatever does NOT depend on the mapper (PSF-precision-operator
     products are already preloaded — verify nothing mapper-independent is recomputed);
   - the MGE operated-matrix term is second (0.19 s at hst) — the phase-1 batching left the
     per-evaluation convolution of the *varying* profiles; check whether it is FFT- or scatter-bound.
3. Ship behind exact parity (bit-level where the summation order is unchanged, pinned rtol 1e-6
   otherwise); `test_autoarray` green; smoke `autolens_workspace/scripts/imaging/features/pixelization/
   cpu_fast_modeling.py` on the smoke profile.
4. Measure before/after on the four cells above; record results + a note in `autolens_profiling`.

Out of scope: the JAX path; the RTU / kernel-CDF meshes (GPU-only by decision, 2026-08-28); the NNLS
solve (done — `nnls_warm_start_memo`).
