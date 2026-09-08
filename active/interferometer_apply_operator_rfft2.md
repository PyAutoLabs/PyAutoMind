# `InterferometerSparseOperator.apply_operator` pads real input to complex — use `rfft2`/`irfft2`

Type: feature
Target: autoarray
Repos:
- PyAutoArray
Themes:
- interferometer
- jax-performance
- likelihood-profiling
Difficulty: small
Autonomy: supervised
Priority: high
Epic: numba-interferometer-revisit
Filed: 2026-09-07
Issued: 2026-09-08
Issue: https://github.com/PyAutoLabs/PyAutoArray/issues/538

Follow-up from `autolens_profiling#226` (phase 2 of `numba-interferometer-revisit`); the
numbers are in `autolens_profiling/results/notes/numba_interferometer_verdict.md` and
`results/breakdown/interferometer/bakeoff_v2026.8.17.1.json`.

## What

`autoarray/inversion/inversion/interferometer/inversion_interferometer_util.py`
(`InterferometerSparseOperator.apply_operator`, ~689-728) zero-pads a **real** batch to
`(2y, 2x)` and applies the operator with complex `jnp.fft.fft2` / `jnp.fft.ifft2`, taking
the real part at the end. `Khat = jnp.fft.fft2(nufft_precision_operator)` is likewise the
complex transform of a real array. Both halve-able: the real-transform pair
`rfft2` / `irfft2` computes the same result exactly (not approximately) with roughly half
the spectrum and half the butterflies.

## Measured saving (single thread, i9-10885H, autoarray 2026.8.17.1)

Same synthetic inputs, same batch size (128), scipy stack, so the comparison isolates the
transform:

| geometry (extent) | mesh | complex `fft2` | real `rfft2` | saving |
|---|---|---|---|---|
| sma (70²) | Delaunay S=1500 | 1.7479 s | 1.2660 s | 1.38× |
| alma (140²) | Delaunay S=1500 | 6.5003 s | 4.3951 s | 1.48× |
| alma_high (280²) | Delaunay S=1500 | 17.7362 s | 11.0346 s | 1.61× |
| sma (70²) | rect S=784 | 1.0124 s | 0.7361 s | 1.38× |
| alma (140²) | rect S=784 | 3.3786 s | 2.6557 s | 1.27× |
| alma_high (280²) | rect S=784 | 6.9360 s | 4.8414 s | 1.43× |

`rfft2` on the NumPy stack also beats the library's own JAX-CPU route by 1.10-1.30× at every
one of those cells, i.e. the transform change is worth more than the backend.

## Scope

- Change `from_nufft_precision_operator` to cache `Khat = jnp.fft.rfft2(...)` and
  `apply_operator` to `rfft2` → multiply → `irfft2(s=(2y, 2x))` → crop.
- The parity gate is the existing interferometer inversion tests plus an explicit pin of
  `curvature_matrix` before/after at `rtol=1e-10`; the change is exact, so a loosened
  tolerance would be hiding a bug.
- GPU: the saving should hold or improve (half the FFT work and half the intermediate
  memory); confirm on the A100 before merging rather than assuming it.
- Nothing else in the interferometer path changes — the algebra is untouched.
