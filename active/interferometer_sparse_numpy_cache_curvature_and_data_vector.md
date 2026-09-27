# Interferometer likelihood campaign: cache curvature_matrix / data_vector on the NumPy sparse interferometer inversions

Type: feature
Target: PyAutoArray
Repos:
- PyAutoArray
- autolens_profiling
Themes:
- interferometer
- pixelization
- numba
Difficulty: small
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: glance
Witness: On the NumPy path (`FitInterferometer(..., xp=np)`), one `figure_of_merit` of `InversionInterferometerSparse` and `InversionInterferometerSparseNumba` evaluates `curvature_matrix_diag` exactly once and `data_vector` exactly once (the `evaluations_per_figure_of_merit` counter in `scripts/misc/likelihood_breakdown/interferometer_pixelized_numpy.py` reads {curvature_matrix_diag: 1, data_vector: 1}, down from {2, 4}), the log evidence is bit-identical to before on the sma / alma rows, the JAX path (jit + vmap + grad) is unaffected, and the RAL CPU alma Delaunay numba full call drops from 2297 ms towards ~1.3 s.
Review-minutes: 10
Epic: interferometer-likelihood-campaign
Filed: 2026-09-27
Issued: 2026-09-27

Source: autolens_profiling#326 phase 1 (PR autolens_profiling#328), RAL CPU rows
`results/breakdown/interferometer/{,sma/,alma_high/}*_numba_hpc_ral_cpu_fp64.json`
(`arms.*.evaluations_per_figure_of_merit` and `arms.*.sub_rows`).

## Why

The library-dispatch breakdown counts property evaluations on one prior-median
`figure_of_merit`: on both NumPy sparse classes **F is built twice and D four
times**. They are plain `@property` on the sparse classes (PyAutoArray main 14d63360):

- `autoarray/inversion/inversion/interferometer/sparse.py:70-71` `data_vector` — `@property`
- `autoarray/inversion/inversion/interferometer/sparse.py:132-133` `curvature_matrix` — `@property`
- `autoarray/inversion/inversion/interferometer/sparse.py:190-191` `curvature_matrix_diag` — `@property`
- `autoarray/inversion/inversion/interferometer_numba/sparse.py:184-185` numba `curvature_matrix_diag` override — `@property`

Consumers: `curvature_reg_matrix` (`inversion/abstract.py:368-389`, itself a
`cached_property`) takes F once; `fast_chi_squared`
(`inversion/interferometer/abstract.py:162`, reads `self.curvature_matrix` at :181
and `self.data_vector` at :189) takes F a second time; `reconstruction`
(`inversion/abstract.py:660`, `self.data_vector` at :699/:724/:739/:755 depending on
branch) plus `fast_chi_squared` account for the four D evaluations.

Measured redundant cost (one extra F + three extra D) from the RAL CPU rows,
1 thread, median full call:

| row | arm | F alone | D alone | full call | redundant | share |
|---|---|---|---|---|---|---|
| sma Delaunay | numba | 76 ms | 8 ms | 357 ms | 101 ms | 28% |
| sma Delaunay | NumPy FFT | 625 ms | 9 ms | 1440 ms | 652 ms | 45% |
| alma Delaunay | numba | 913 ms | 36 ms | 2297 ms | 1021 ms | 44% |
| alma rect | numba | 1281 ms | 32 ms | 3164 ms | 1376 ms | 43% |
| alma rect | NumPy FFT | 2251 ms | 31 ms | 5140 ms | 2343 ms | 46% |
| alma_high Delaunay | numba | 13139 ms | 122 ms | 27284 ms | 13505 ms | 49% |
| alma_high rect | NumPy FFT | 8579 ms | 118 ms | 18244 ms | 8933 ms | 49% |

So roughly half of every alma / alma_high NumPy `figure_of_merit` is recomputation.
This changes the numba-vs-JAX-CPU comparison in the campaign decision matrix
(at alma_high numba 27.3 s vs JAX-CPU 8.3 s would become ~13.8 s).

## What

Make `curvature_matrix` (or `curvature_matrix_diag`) and `data_vector` on the
sparse interferometer inversions cache per instance on the NumPy path (the
`autonerves.cached_property` used elsewhere in these classes), checking the
e819fa12 (2025-11-05) property sweep's reason for removing such caches does not
apply (a new inversion is built per fit, so no invalidation is needed), and that
JAX tracing is unaffected. Re-run the RAL CPU numba rows as the after-measurement.
