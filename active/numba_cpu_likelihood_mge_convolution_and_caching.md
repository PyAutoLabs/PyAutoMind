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
