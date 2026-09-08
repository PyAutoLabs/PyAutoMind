# Reinstate a numba CPU interferometer curvature path — the extent-grid convolution, geometry-gated

Type: feature
Target: autoarray
Repos:
- PyAutoArray
- autolens_profiling
Themes:
- numba-cpu
- interferometer
- likelihood-profiling
Difficulty: large
Autonomy: supervised
Priority: high
Epic: numba-interferometer-revisit
Filed: 2026-09-07
Issued: 2026-09-08
Issue: https://github.com/PyAutoLabs/PyAutoArray/issues/543

Follow-up from `autolens_profiling#226` (phase 2 of `numba-interferometer-revisit`). The
verdict, the bake-off and the in-situ arms are in
`autolens_profiling/results/notes/numba_interferometer_verdict.md`.

## What

Add `autoarray/inversion/inversion/interferometer_numba/` mirroring the live
`imaging_numba/` package, with **one** kernel: the extent-grid direct convolution prototyped
as `direct_conv` in `autolens_profiling/scripts/misc/numba_interferometer/kernels.py`. For
each source column of `A`, convolve it over the `(Ny, Nx)` unmasked-extent rectangle with
contiguous `W~` preload rows, then project with `Aᵀ`. Cost `O(nnz·M + S·nnz)`.

**Do not reinstate the deleted kernel.** The recovered `O(N² P²)` pair loop beats a NumPy
`rfft2` convolution at only one of six measured cells; `direct_conv` beats it by 2.9-4.8× on
the real likelihood's `F` row.

## Measured (single thread, i9-10885H, autolens 2026.8.17.1)

In-situ `F: mapper×mapper` row, real likelihood, arms interleaved with `dgemm` controls:

| instrument | mesh | recovered kernel | `direct_conv` | JAX/FFT (jit-warm) | direct_conv vs JAX |
|---|---|---|---|---|---|
| sma | Delaunay 1500 | 0.2475 s | 0.0844 s | 0.5917 s | **7.01×** |
| sma | rect 32² | 0.3967 s | 0.0998 s | 0.4101 s | **4.11×** |
| alma | Delaunay 1500 | 4.0710 s | 1.2250 s | 2.4297 s | **1.98×** |
| alma | rect 32² | 7.0205 s | 1.4631 s | 1.6110 s | 1.10× |

Whole evaluation, with the jit-warm `F` substituted into the measured non-`F` cost:
2.43× (sma Delaunay), 2.76× (sma rect), 1.77× (alma Delaunay), 1.08× (alma rect) faster than
JAX-CPU.

## The gate this needs

The controlling variable is **non-zeros per source column**, `nnz/S = N_pix·P/S`. Measured
crossover against a NumPy `rfft2` convolution: **≈60 (Delaunay) to ≈77 (rectangular)**. Below
it the numba kernel wins (up to 5.93×); above it the FFT wins (by 1.6× at alma_high Delaunay,
3.7× at alma_high rectangular). So the path must be *selected*, not defaulted to — a
dispatch rule on `nnz/S` with the constant measured on the target machine, or an explicit
user setting with the rule documented.

## Scope

- `interferometer_numba/inversion_interferometer_numba_util.py` — the `direct_conv` kernel
  and its `prange` sibling (3.5× at sma, 4.6× at alma on 8 threads; see the pool caveat).
- `interferometer_numba/sparse.py` — `InversionInterferometerSparseNumba`, mirroring
  `imaging_numba/sparse.py`, dispatched from `inversion/factory.py`.
- The mapper must emit the CSR/CSC + extent-flat layout directly (as
  `_sparse_triplets_curvature_from` already emits COO), so the kernel does not marshal its
  own inputs per evaluation.
- Preconditions to raise on, not work around (the profiling pack already does): linear-
  function lists, multiple mappers, `over_sample_size != 1`, non-NumPy `xp`.
- Parity gate: `F`, `D`, reconstruction and log evidence against
  `InversionInterferometerSparse` at `rtol=1e-10` on `F` with `atol` scaled by `max|F|`,
  plus a control that a 1 % scale fails the pin.
- The real-space `W~` preload must be kept on the dataset: `InterferometerSparseOperator`
  currently stores only `Khat = fft2(preload)` and discards the array this kernel indexes.
