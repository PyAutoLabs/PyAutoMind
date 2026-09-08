# `InterferometerSparseOperator` has no NumPy path — a CPU user is forced through JAX

Type: feature
Target: autoarray
Repos:
- PyAutoArray
Themes:
- interferometer
- numpy-cpu
- likelihood-profiling
Difficulty: medium
Autonomy: supervised
Priority: medium
Epic: numba-interferometer-revisit
Filed: 2026-09-07
Issued: 2026-09-08
Issue: https://github.com/PyAutoLabs/PyAutoArray/issues/542

Follow-up from `autolens_profiling#226` (phase 2 of `numba-interferometer-revisit`);
numbers in `autolens_profiling/results/notes/numba_interferometer_verdict.md`.

## What

`InterferometerSparseOperator.apply_operator`, `curvature_matrix_diag_from` and
`curvature_matrix_off_diag_from`
(`autoarray/inversion/inversion/interferometer/inversion_interferometer_util.py`) all
`import jax.numpy` inside the method body. There is no `xp=np` branch: a user without a GPU
still runs the interferometer curvature through JAX, and `InversionInterferometerSparse`
inherits that whatever `xp` the fit was built with.

That is not only an unwanted dependency — it is slower. On identical inputs, a NumPy/scipy
`rfft2` convolution with a `scipy.sparse` projection (the NumPy-stack counterpart of the JAX
route's `segment_sum`) beats the library's JAX-CPU route at every geometry measured:

| geometry | mesh | JAX-CPU (`fft2`) | NumPy (`rfft2`) | saving |
|---|---|---|---|---|
| sma | Delaunay S=1500 | 1.5239 s | 1.2660 s | 1.20× |
| alma | Delaunay S=1500 | 5.5156 s | 4.3951 s | 1.26× |
| alma_high | Delaunay S=1500 | 12.9655 s | 11.0346 s | 1.18× |
| sma | rect S=784 | 0.8510 s | 0.7361 s | 1.16× |
| alma | rect S=784 | 2.9317 s | 2.6557 s | 1.10× |
| alma_high | rect S=784 | 6.2817 s | 4.8414 s | 1.30× |

(Some of that gap is the `rfft2` change filed separately as
`interferometer_apply_operator_rfft2.md`, which shipped on 2026-09-08 — PyAutoArray#540,
record `complete/2026/09/interferometer-apply-operator-rfft2.md`. The real-FFT-first
sequencing constraint is therefore already satisfied; measure this one against the
post-`rfft2` baseline, not the numbers in the table above.)

## Scope

- An `xp`-aware application path so `xp=np` uses `scipy.fft` and `scipy.sparse` and never
  imports JAX; the JAX branch stays exactly as it is.
- The reference implementation to port is
  `autolens_profiling/scripts/misc/numba_interferometer/kernels.py::curvature_fft_numpy`,
  which is pinned to the numba reference kernel at `rtol=1e-10` in that pack's
  `test_parity.py`.
- Parity gate: the NumPy and JAX branches must agree at `rtol=1e-10` on `F` with `atol`
  scaled by `max|F|`.
- Worth checking at the same time whether `apply_sparse_operator(use_jax=False)` should
  imply the NumPy application path (today it only affects how the preload is *built*, not
  how the operator is *applied*, which is a surprising split).
