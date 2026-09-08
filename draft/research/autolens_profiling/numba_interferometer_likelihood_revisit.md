# Revisit the numba CPU interferometer likelihood — epic ledger

Type: research
Target: autolens_profiling
Repos:
- @autolens_profiling
- @PyAutoArray
Themes:
- numba-cpu
- interferometer
- likelihood-profiling
Difficulty: too-large
Autonomy: human-required
Priority: high
Status: epic ledger — phases route through /start_dev one at a time; this file is never issued itself
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Epic: numba-interferometer-revisit
Filed: 2026-09-07

## Original request (verbatim)

> We recently sped up the imaging numba likelihood function, which was a big win and got us x10ish speed up on the likelihood function on CPU. Approximately 6 months to a year ago, we removed the interferometer numba likelihood function in favour of the the JAX implementation, because it felt like CPU run times on JAX were pretty fast. However, given the success on the imaging numba work, I think its worth revisting this as there are still many users who do not have GPU access and anything which makes CPU run times as fast as possible will be appreciarted. Therefore, can you dig up the code in the Github history which contains the numba interferometry likeilhood function, I think in the past it was called "secret". Can you recover this into a standalne pack (for now), as part of autolens_profiling, and ultimately produce a likelihood_breakdown function for it which mirrors the imaging numba likelihood funciton. Can Can you then do some deep research on whether the way that code is implement was the best approach or if there is lots of numba speed up possible (like there was for imaging), noting that I think it algebraically may differ from what now is the JAX implementation in terms of linear algbera. Can you treat separating the work required on building the preload curvature matrix, which has its own dediciated sparsity approach for CPU but never got anywhere near as fast as it became on GPU. Ultimately, work out if numba CPU interferometer is worth reinstating in the code base, or if it does not compare to the JAX implementation. It could well be that imaging works so well because of how it exploits sparsity, and theres less of that low hanging fruit in interferometer, but I do also know the old code exploited a hell of a lot of sparsity itself.

## What the archaeology established (2026-09-07, read-only)

- The "secret" modules (`interferometer_secret.py`, `inversion_util_secret.py`) were never
  tracked; PyAutoArray PR #161 `feature/unsecret_interferometer` (merged `d76904e8`,
  2025-03-19) published their bodies into
  `autoarray/inversion/inversion/interferometer/inversion_interferometer_util.py`.
- Best intact snapshot: PyAutoArray **`0b90c401`** (2025-12-17). Numba module deleted by
  `c9605b5b` (PR #201, merged 2025-12-21); `WTildeInterferometer` /
  `InversionInterferometerWTilde` deleted by `222ee046` (PR #204, merged 2026-02-03). Last
  copy of the split-out `inversion_interferometer_numba_util.py` is `8dd049e7`.
- The linear algebra is **unchanged** between the numba path and today's JAX sparse
  operator: same preload `W~[dy,dx] = Σ_k σ_k⁻² cos(2π(dx·u_k + dy·v_k))`
  (`curvature_preload` then, `nufft_precision_operator` now), same `D = Mᵀ Re(Fᴴ W d)`,
  same `F = Mᵀ W~ M`, same `fast_chi_squared`. What differs is the *application*: the numba
  kernel scatter-accumulates `F[s0,s1] += preload[dy,dx] w0 w1` over image-pixel pairs,
  O(N_pix² P²) and independent of K; the JAX path applies the block-Toeplitz `W~` as a
  zero-padded FFT convolution batched over source columns, O(S·M log M).
- Today's `InterferometerSparseOperator.curvature_matrix_*_from` methods import `jax.numpy`
  inside the method body: there is **no NumPy application path** on main. "JAX CPU" is the
  only CPU sparse route a no-GPU user has.
- Unlike imaging, `W~` for an interferometer has *no compact support* (sparse uv coverage →
  dense real-space kernel). The imaging numba win came from PSF-sized support; the
  interferometer kernel's only sparsity is the mapper's (P entries per image pixel), so the
  quadratic-in-N scaling is intrinsic to the scatter approach.
- Design review (2026-09-07, synthetic single-thread bake-off, to be reproduced in phase 2):
  the winning numba form is a direct extent-grid convolution (0.11 s sma / 1.65 s alma vs
  0.36 / 7.6 s for the recovered scatter and 0.48 / 1.99 s for a NumPy `rfft2` path); FFT
  wins once a source column touches more than ~35–45 image pixels (alma_high and beyond);
  the library's complex `fft2` on real input is 1.6–2.2× slower than `rfft2` for everyone;
  the preload is exactly an adjoint type-1 NUFFT of the weights (100–500× cheaper to build).

## Phases

| # | Phase | Prompt | State (2026-09-07) |
|---|-------|--------|--------------------|
| 1 | Standalone pack + breakdown scripts mirroring the imaging numba ones | `complete/2026/09/numba-interferometer-pack.md` | **SHIPPED 2026-09-07** — autolens_profiling#223, PR #225 merged `99f4b533b52cda974f62c59e8b2995ccb941474b` |
| 2 | Synthetic bake-off, kernel levers, in-situ numba vs JAX-CPU, verdict note | `complete/2026/09/numba-interferometer-kernel-levers.md` | **SHIPPED 2026-09-07** — autolens_profiling#226, PR #228 merged `2ad7b8faee0813b159f4a1ed504fc1b072692cd1` |
| 3 | Preload as its own line item: builder timings + adjoint-NUFFT construction | `draft/research/autolens_profiling/interferometer_preload_cpu.md` | filed; after phase 1 |

Follow-ups filed from the phase-2 verdict (2026-09-07): draft/feature/autoarray/interferometer_apply_operator_rfft2.md, interferometer_numba_cpu_direct_conv.md, interferometer_sparse_operator_numpy_cpu_path.md.

PyAutoArray is read-only throughout; library changes the verdict justifies (reinstatement,
the `rfft2` change, the NUFFT preload) are filed as follow-up prompts via `/intake`.
