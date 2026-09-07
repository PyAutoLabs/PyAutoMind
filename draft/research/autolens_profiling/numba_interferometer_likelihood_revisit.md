# Revisit the numba CPU interferometer likelihood: recover the w-tilde pack, break it down, judge reinstatement

Type: research
Target: autolens_profiling
Repos:
- @autolens_profiling
- @PyAutoArray
Themes:
- numba-cpu
- interferometer
- likelihood-profiling
Difficulty: hard
Autonomy: supervised
Priority: high
Filed: 2026-09-07

## Original request (verbatim)

> We recently sped up the imaging numba likelihood function, which was a big win and got us x10ish speed up on the likelihood function on CPU. Approximately 6 months to a year ago, we removed the interferometer numba likelihood function in favour of the the JAX implementation, because it felt like CPU run times on JAX were pretty fast. However, given the success on the imaging numba work, I think its worth revisting this as there are still many users who do not have GPU access and anything which makes CPU run times as fast as possible will be appreciarted. Therefore, can you dig up the code in the Github history which contains the numba interferometry likeilhood function, I think in the past it was called "secret". Can you recover this into a standalne pack (for now), as part of autolens_profiling, and ultimately produce a likelihood_breakdown function for it which mirrors the imaging numba likelihood funciton. Can Can you then do some deep research on whether the way that code is implement was the best approach or if there is lots of numba speed up possible (like there was for imaging), noting that I think it algebraically may differ from what now is the JAX implementation in terms of linear algbera. Can you treat separating the work required on building the preload curvature matrix, which has its own dediciated sparsity approach for CPU but never got anywhere near as fast as it became on GPU. Ultimately, work out if numba CPU interferometer is worth reinstating in the code base, or if it does not compare to the JAX implementation. It could well be that imaging works so well because of how it exploits sparsity, and theres less of that low hanging fruit in interferometer, but I do also know the old code exploited a hell of a lot of sparsity itself.

## What the archaeology already established (2026-09-07, read-only)

- The "secret" modules (`interferometer_secret.py`, `inversion_util_secret.py`) were never
  tracked; PyAutoArray PR #161 `feature/unsecret_interferometer` (merged `d76904e8`,
  2025-03-19) published their bodies into
  `autoarray/inversion/inversion/interferometer/inversion_interferometer_util.py`.
- Best intact snapshot: PyAutoArray **`0b90c401`** (2025-12-17, "fast chi squared
  implemented"). Numba module deleted by `c9605b5b` (PR #201, merged 2025-12-21);
  `WTildeInterferometer` / `InversionInterferometerWTilde` deleted by `222ee046` (PR #204,
  merged 2026-02-03). Last copy of the split-out `inversion_interferometer_numba_util.py`
  is at `8dd049e7`.
- The linear algebra is **unchanged** between the numba path and today's JAX sparse
  operator: same preload `W~[dy,dx] = sum_k sigma_k^-2 cos(2 pi (dx u_k + dy v_k))`
  (`curvature_preload` then, `nufft_precision_operator` now), same `D = M^T Re(F^H W d)`,
  same `F = M^T W~ M`, same `fast_chi_squared`. What differs is the *application*:
  the numba kernel scatter-accumulates `F[s0,s1] += preload[dy,dx] w0 w1` over image-pixel
  pairs, cost O(N_pix^2 P^2) and independent of K; the JAX path applies the block-Toeplitz
  `W~` as a zero-padded FFT convolution batched over source columns, O(S N log N).
- Today's `InterferometerSparseOperator.curvature_matrix_*_from` methods import
  `jax.numpy` inside the method body: there is **no NumPy application path** for the
  sparse curvature matrix on main. "JAX CPU" is therefore the only CPU sparse route a
  no-GPU user has, and the recovered numba kernel is the only non-JAX comparator.
- Unlike imaging, `W~` for an interferometer has *no compact support* (uv coverage is
  sparse, so the real-space kernel is dense). The imaging numba win came from PSF-sized
  support; the interferometer kernel's "sparsity" is only the mapper's (P entries per
  image pixel), so the quadratic-in-N scaling is intrinsic to the scatter approach.

## Deliverables

1. **Standalone pack** under `autolens_profiling/scripts/misc/numba_interferometer/`
   (name at the plan's discretion): the recovered numba kernels (core five plus
   `sub_slim_indexes_for_pix_index`; drop the COSMA multiprocessing experiments),
   shimmed to today's `Mapper` / `Mask2D` / `AbstractInversionInterferometer` API, an
   `InversionInterferometerNumba` class, and a parity test that pins its `F`, `D`,
   reconstruction and `log_evidence` against `InversionInterferometerSparse` on the same
   dataset. The preload is shared: `nufft_precision_operator_from` returns the identical
   array, so the pack reuses `dataset.sparse_operator` for the preload and dirty image.
2. **`scripts/interferometer/likelihood_breakdown/delaunay_numba.py`** (and a rectangular
   sibling if cheap) mirroring `scripts/imaging/likelihood_breakdown/delaunay_numba.py`:
   same step accessors, residual-row convention, `_profile_cli` output, pinned log
   evidence, JSON+PNG under `results/breakdown/interferometer/`.
3. **Research note** (`results/notes/`): numba vs JAX-CPU per-step comparison on SMA and
   ALMA instruments; which of the imaging levers transfer (two-stage source-space
   accumulator, symmetric halving, hoisted row gathers, extent-index rows) and by how
   much; whether a NumPy/pocketfft FFT-convolution kernel driven from numba beats both;
   thread scaling under `OMP_NUM_THREADS=1` vs the pool run.
4. **Preload as its own line item**: time `nufft_precision_operator_via_np_from` vs the
   recovered numba preload vs the JAX one on CPU, and test the hypothesis that the preload
   is exactly an adjoint (type-1) NUFFT of the weights `1/sigma^2` onto the doubled
   `(2Ny, 2Nx)` offset grid, which would turn O(N K) cosines into O(K + N log N) via the
   existing transformer. Verify against the brute-force array at fp64.
5. **Verdict**: reinstate numba interferometer in PyAutoArray (as `interferometer_numba/`
   mirroring `imaging_numba/`), keep it as a profiling-only pack, or drop it, with the
   numbers that decide it.

## Constraints

- Read-only on PyAutoArray unless the verdict is "reinstate", which is a follow-up prompt.
- No JAX in the numba pack's hot path; `xp=np` throughout, `use_jax=False`.
- Verification discipline: parity pinned at `rtol=1e-6` before any lever is tried;
  paired B/A runs with a control row that must hold still.
