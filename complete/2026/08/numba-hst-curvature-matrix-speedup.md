# The numba CPU curvature matrix F at HST: 3.3x on F, 2.6x on the evaluation — the dense mapper x linear-func block was a PSF *correlation* the batched FFT Convolver could already do

- **Issue:** PyAutoArray#505 (closed) · **PRs:** PyAutoArray#506 (`1b89404b`, head `d43e1aca`), autolens_profiling#189 (`b3fa632a`, head `e936aae7`) — merged 2026-08-28
- **Repos:** PyAutoArray (`inversion/inversion/imaging_numba/sparse.py`, `inversion_imaging_numba_util.py`, `operators/convolver.py`, two test modules), autolens_profiling (`scripts/imaging/likelihood_breakdown/`, `results/breakdown/imaging/`, `results/notes/`)
- **Epic:** successor to `numba-cpu-likelihood` (COMPLETE 2026-08-28). **Phase 1 of 2** — phase 2 is PyAutoArray#507 / `active/numba_cpu_hst_curvature_matrix_phase2.md`
- **Status: SHIPPED.** The issue's >=2x goal on F is met on both HST cells, with a 3.3x margin.

## The headline

F was 78% of a 1.28 s HST rectangular numba evaluation. Instrumenting its sub-blocks first — the checkpoint the plan insisted on — showed the cost was not where the prompt's candidate list said it was: the mapper x mapper block already exploited PSF symmetry, and **the mapper x linear-func block was the 0.86 s**. That block expanded the 60 MGE curvature weights onto the full native grid and ran a direct sliding-window correlation over `ny x nx x ky x kx x 60`, once per (mapper, linear func) pair, every evaluation.

A sliding-window correlation with the PSF is a convolution with the PSF reversed along both axes. PyAutoArray already owns a batched FFT `Convolver`; the block now runs through it once per linear func (new cached `Convolver.reversed_kernel`), leaving only the sparse scatter onto source pixels in numba.

Measured at `OMP_NUM_THREADS=1`, memo off, `n_repeats` 10, with the before column re-measured back-to-back with the after run (this host carries 20-30% session-to-session variance):

| cell | eval | F total | mapper x mapper | mapper x l-func |
|---|---|---|---|---|
| hst, rectangular bilinear | 1.562 -> **0.595** | 1.195 -> **0.359** | 0.295 -> 0.277 | 0.858 -> **0.054** |
| euclid, rectangular bilinear | 0.349 -> **0.249** | 0.256 -> **0.097** | 0.060 -> 0.065 | 0.182 -> **0.023** |
| hst, Delaunay-1250 | 1.367 -> **0.758** | 1.077 -> **0.184** | 0.122 -> 0.123 | 0.854 -> **0.052** |
| hst, rectangular RTU | (8.501) -> 7.479 | (1.250) -> **0.334** | (0.304) -> 0.249 | (0.929) -> **0.061** |

**~16x on the block, 3.3x on F, 2.6x on the whole HST evaluation.** RTU is parenthesised because it is GPU-only by the 2026-08-28 decision and was re-run once for currency rather than paired.

The second change is separate and bit-identical: the three blocks each rebuilt `operated_mapping_matrix / noise_map ** 2` and re-walked the mapping matrix, and a global re-mirror ran over an already-symmetric matrix with a fresh O(P^2) allocation. They are now per-block helpers over one shared weighted copy that fill both triangles directly (`np.array_equal` True on euclid and hst).

## Verification

- `test_autoarray` **1296 passed** (1290 before, 6 new). The new tests assert the FFT path against the retained dense kernel with **asymmetric non-square PSFs**, so a missing axis reversal fails rather than passing by symmetry.
- F agrees with the sliding-window result to **3e-18 relative** (the FFT is not bit-identical to the direct sum, as expected).
- All **3 pinned log-likelihoods PASSED**: hst bilinear 27661.91013366411, hst RTU 27180.70471569685, hst Delaunay 29090.527210448134. euclid (no pin) measured 6213.306873885871, unchanged to every recorded digit.
- **The pool run is the one that mattered.** A single-thread win only counts if it survives Nautilus's one-process-per-core pool, where a library quietly spinning up its own threads shows as a regression. `cpu_fast_modeling.py` on an 8-core host, canonical `main` vs the branch via `PYTHONPATH` (`autoarray.__file__` asserted both ways), 60-component linear MGE bulge so the FFT'd block is non-empty: pool of 8 0.1919 -> **0.1747** s/eval, serial 0.4845 -> **0.4489** s/eval. The parallel speed-up ratio is **flat** across the change (2.52x -> 2.57x) — that ratio, not the wall-clock, is what drops on hidden threads. Consistent with the code: `Convolver`'s FFT path uses `np.fft.rfft2` with no `workers=`, and `scipy.fft` appears only as `next_fast_len`.

## Traps recorded

- **Instrument before optimising: the prompt's candidate list was half stale.** Two of the three named levers were already applied (the mapper block's PSF symmetry) or would have bought ~2% (the mirror pass). The 0.86 s was in the one block the prompt described as secondary. The step-0 checkpoint is what caught it.
- **A sliding window over a PSF is a correlation, not a convolution.** Routing it through the FFT `Convolver` unreversed gives a wrong-but-plausible F — the pinned likelihood moves, but a symmetric test PSF hides it entirely. The parity test uses an asymmetric non-square kernel for exactly this reason.
- **Threading is not a lever on this path, and never was.** Nautilus samples with Python `multiprocessing`, one process per core; `prange` or an FFT thread pool would oversubscribe N procs x N threads. Every measurement here is `OMP_NUM_THREADS=1` plus one real pool run, and the pool run is the evidence, not the single-thread number.
- **Re-measure the before column back-to-back.** This host drifts 20-30% between sessions, so the committed `*_v2026.8.17.1` artifacts could not serve as the "before" — they also pre-dated PyAutoArray#462 and still showed an 18.8 s sparse-triplets step. Artifacts were regenerated, never hand-copied.
- **The removed symbol has two innocent namesakes.** `inversion_imaging_numba.curvature_matrix_mirrored_from` is gone; the identically-named `inversion_util` and `inversion_imaging_util` functions are untouched and still serve the interferometer and non-numba imaging paths. The only downstream workspace reference is to the untouched non-numba namespace.

## What phase 1 leaves

F is no longer the dominant term at HST resolution. On hst bilinear the largest remaining steps are the mapper x mapper sparse-operator block (0.277 s) and the MGE operated mapping matrix (~0.224 s). PR#506's body says no phase-2 prompt was filed because the goal was met; phase 2 was subsequently filed anyway on those two residuals, as **PyAutoArray#507**, and starts from this record's numbers.

## Heart RED at merge — human override

Merged over the pre-existing Heart **RED score 45** (`pyauto-heart readiness`, ts `2026-08-28T15:02:11Z`): `red_reasons: "release validation FAILED (stage integrate)"`. Human authorisation 2026-08-28, verbatim: *"prm and then kick off phase 2, I authorize the heart RED thing"* — scoped to this task only; release stays human. The RED is pre-existing on `main` and unrelated: the failing scripts (`autofit scripts/plot/nautilus_plotter.py`, `autolens_test .../jax_likelihood/rectangular_mge{,_rtu}.py`, timeout `.../multi_dataset/jax_likelihood/delaunay.py`) all live in other repos and all sit on the **JAX** likelihood path or in `autofit`; this diff touches only the **numba** imaging-inversion path plus an additive-only `convolver.py`.

CI was green on every run and every matrix leg before each merge: PyAutoArray `Tests [pull_request]` — `unittest (3.12)`, `unittest (3.13)`, `unittest-nojax`; autolens_profiling `lint [pull_request]`.

## Original prompt

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
Status: active
Filed: 2026-08-28
Issued: 2026-08-28

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
