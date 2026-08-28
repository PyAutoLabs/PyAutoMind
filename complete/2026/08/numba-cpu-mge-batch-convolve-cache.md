## numba-cpu-mge-batch-convolve-cache
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/496 (closed, completed)
- completed: 2026-08-27
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/497 (MERGED 86e2944a)
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/588 (MERGED d55f3ab3)
- epic: numba-cpu-likelihood — phase 1
- shipped: PyAutoArray — `Convolver.state_from` reuses the precomputed `ConvolverState` via new
  `ConvolverState.is_for_mask` (the old test compared the mask to the *kernel* shape, so
  `Imaging.psf_setup_state` was never reused and every convolution re-ran the mask resize + rfft2);
  `AbstractInversionImaging.linear_func_operated_mapping_matrix_dict` → `cached_property`
  (numba override reaches the parent via `.func` — autonerves `CachedProperty` has no `.fget`);
  linear-func × linear-func curvature blocks in `imaging/sparse.py` and `imaging_numba/sparse.py`
  noise-weight each matrix once and mirror the upper triangle (exact for any per-pixel noise map).
  PyAutoGalaxy — `LightProfileLinearObjFuncList.operated_mapping_matrix_override` numpy /
  `convolve_over_sample_size == 1` path stacks the profile + blurring images and makes one
  `convolved_mapping_matrix_via_real_space_np_from` call; JAX + oversampled branches keep the loop.
- measured: MGE-60 operated matrix on the `cpu_fast_modeling` route, memo disabled, fresh
  FitImaging per call — hst 1.11 s → 0.30 s (3.7×), euclid 0.68 s → 0.125 s (5.4×). Output
  bitwise identical; hst pin 27661.910133664103 unchanged; smoke autogalaxy/autolens/autolens_test
  0 new failures (3 pre-existing `ENV: jax` pin mismatches reproduce bit-identically on main).
- trap: the autolens_profiling `pixelization_numba` breakdown/runtime harness re-evaluates one
  fixed instance, so the cross-eval operated-matrix memo hits and the MGE step reads ~0.003-0.01 s
  on BOTH sides of any A/B (and contaminates `direct_log_likelihood_function_per_call`). Real
  modelling perturbs the MGE every evaluation → memo always misses. Follow-up filed:
  `draft/feature/autolens_profiling/numba_breakdown_harness_memo_blind.md`.
- trap: blurring-mask ordering — `convolved_mapping_matrix_via_real_space_np_from` ignores its
  `blurring_mask` arg and scatters on the state's mask-derived blurring mask; verified identical
  slim ordering (pure padding translation) to `mask.derive_mask.blurring_from(..., allow_padding=True)`
  across 20+ configurations; pinned by tests in both repos.
- gate: shipped over Heart RED `release validation FAILED (stage integrate)` (unrelated
  autolens_workspace_test `rectangular_mge{,_rtu}.py` pin drift) on explicit human authorisation.
- epic next: phase 2 kernel-CDF fast path (deferred behind the Delaunay fiducial); phase 3 numba
  `fnnls` positive-only solver restoration (PyAutoArray 8bb449a1) — NOT YET FILED.
- affected-repos:
  - PyAutoArray
  - PyAutoGalaxy

## Original prompt

# Numba CPU likelihood phase 1: batched MGE convolution + operated-matrix caching

Type: feature
Epic: numba-cpu-likelihood
Phase: 1
Target: autoarray
Repos:
- @PyAutoArray
- @PyAutoGalaxy
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Issued: 2026-08-27
Filed: 2026-08-20 (backfilled from git)

> Phase 1 of the CPU-likelihood speed restoration
> (autolens_profiling#151 profiling; user request 2026-08-20 recorded verbatim
> in the phase-2 prompt `numba_cpu_likelihood_kernel_cdf_fast_path.md`).
> Exact-identical wins on files disjoint from phase 2's kernel-CDF work.

## Context (from the 2026-08-20 profiling + source hunt)

On the numba CPU sparse-operator likelihood (`apply_sparse_operator_cpu()` +
`use_jax=False`, MGE-60 linear lens light + rectangular pixelization —
the `cpu_fast_modeling.py` production route):

1. The 60 MGE linear-Gaussian operated images cost ~19% of a euclid evaluation
   (0.42 s of 2.15 s; 0.87 s at hst): `AbstractLinearObjFuncList.
   operated_mapping_matrix_override`
   (`PyAutoGalaxy autogalaxy/profiles/light/linear/abstract.py:319-382`) loops
   the Gaussians and calls `psf.convolved_image_from` **60 separate times**,
   each re-padding to fft_shape and re-transforming the PSF. A batched exact
   equivalent already exists and handles the blurring region:
   `Convolver.convolved_mapping_matrix_via_real_space_np_from`
   (`PyAutoArray autoarray/operators/convolver.py:1437`) — one scipy FFT
   convolution amortized over all 60 columns.
   `AbstractLinearObjFuncList.mapping_matrix` (`linear/abstract.py:291`)
   already produces the stacked unblurred matrix; only the blurring-grid stack
   is missing.
2. `linear_func_operated_mapping_matrix_dict`
   (`PyAutoArray autoarray/inversion/inversion/imaging/abstract.py:184`) is an
   **uncached `@property`** rebuilt on every access; the numba sparse inversion
   accesses it ~5 times per evaluation (`imaging_numba/sparse.py:194,419,443,
   451,509`), including inside an O(60^2) loop that also repeats a
   `(N_pix, 60)` noise-map division per pair. Cache it (`cached_property`,
   consistent with the inversion's per-evaluation lifetime) and hoist the
   noise division out of the pair loop.

## Goal

- Batch the MGE/linear-func operated mapping matrix construction through the
  existing batched convolver call (numpy path; JAX path untouched).
- Cache `linear_func_operated_mapping_matrix_dict` and hoist repeated
  per-pair work in `imaging_numba/sparse.py`.
- **Likelihood values unchanged**: pinned euclid/hst log-likelihoods in
  autolens_profiling's `pixelization_numba` cells must pass (rtol 1e-6; expect
  bit-comparable), plus the existing unit suites in both repos.
- Re-run the autolens_profiling runtime + breakdown cells to record the gain
  (expect the "MGE operated mapping matrix" step 0.42 s -> ~0.05-0.1 s at
  euclid).
