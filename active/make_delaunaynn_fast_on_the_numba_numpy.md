# Make DelaunayNN fast on the numba/NumPy path

Type: feature
Target: PyAutoArray
Repos:
- PyAutoArray
Difficulty: large
Autonomy: supervised
Priority: normal
Memory: wiki/galaxies/sources/massive-ellipticals.md; wiki/lensing/sources/dark-matter-substructure.md; reading-queue.md
Status: formalised
Issued: 2026-10-15
Consequence: glance
Witness: on the Aris interferometer setup (1405 vertices, use_jax=False) DelaunayNN steady log_likelihood_function time <= 2x Delaunay, with numba-vs-reference Sibson parity tests green
Review-minutes: 3
Unattended: ready

DelaunayNN is ~40x slower than Delaunay on the NumPy (`use_jax=False`) path because the
Sibson natural-neighbour interpolation is a pure-Python per-query loop. Make it fast with
a numba kernel so DelaunayNN costs about the same as Delaunay on CPU.

## Evidence (measured 2026-10-15, laptop, PyAutoArray ccddfba6)

Collaborator (Aris) SMA-scale interferometer data: 5,516,930 visibilities, 5,496 masked
pixels, sparse operator applied, AdaptSplit, `use_positive_only_solver=False`, threads
pinned to 1. Bare `analysis.log_likelihood_function` steady seconds per call:

| mesh       | 1405 vertices | 5526 vertices |
|------------|---------------|---------------|
| Delaunay   | 0.43 s        | 12.7 s        |
| DelaunayNN | 18.1 s        | 56 s          |

Profile: almost all DelaunayNN time is in `sibson_mappings_weights_from_tables` ->
`single()` (`autoarray/inversion/mesh/interpolator/sibson.py` ~L613-644), reached via
`scipy_delaunay_nn` -> `mappings_weights_for` (~11k calls per likelihood: data points +
split points). The NumPy branch is a Python list comprehension over queries; each
`_sibson_single_from_tables` call runs ~50-100 tiny NumPy ops (argsort, np.add.at,
broadcast_to, where, stack, pad...) for at most ~32 cavity triangles / ~96 contributions,
~1.5 ms per query. The JAX branch is vectorised (vmap + lax.map) and is not affected.

Scripts/logs: scratchpad `.../50c8c6cd-6ac2-47c2-9290-7ee73f9c4315/scratchpad/aris/step6`
and `PROGRESS2.md` (temporary; numbers are reproduced above).

## Fix

- Add an `@njit` (parallel=True / `prange` over queries) kernel for the NumPy path of
  `sibson_mappings_weights_from_tables`: cavity walk, Watson circumcircle contributions,
  compaction/dedup of vertex ids into fixed-size `max_neighbors` rows, normalisation.
- Reproduce every edge case of `_sibson_single_from_tables` exactly: outside-mesh
  fallback (`seed_simplex < 0`), on-vertex fallback, on-edge barycentric row, degenerate
  Watson circles and cavity/neighbour overflow -> NaN weights, plus the returned
  diagnostics (`cavity_sizes`, `overflow`, `degenerate`).
- Follow the existing numba conventions in `interpolator/delaunay.py` /
  `rectangular.py` (config `numba:` block, caching). JAX path untouched.

## Numba likelihood paths must use it (imaging + interferometer)

The faster interpolation alone is not enough: the numba likelihood paths must actually
take DelaunayNN mappers.

- Interferometer: `factory.py` routes a NumPy inversion to the numba `direct_conv`
  curvature path (`InversionInterferometerSparseNumba`) only when mean non-zeros per
  source column <= `interferometer_numba_nnz_per_source_max` (60, tuned on Delaunay).
  DelaunayNN stencils carry more neighbours per data point (up to
  `SIBSON_MAX_NEIGHBORS` = 32 vs 3), so DelaunayNN may fall through to the slower FFT
  route. Measure nnz/column for DelaunayNN on the Aris mask; confirm which route it takes;
  if it misses `direct_conv`, make it take it (or re-measure the crossover) — and check the
  kernel handles variable-size Sibson rows correctly.
- Imaging: do the same audit for the numba imaging likelihood path — confirm DelaunayNN
  mappers are routed to it and handled correctly, and time imaging Delaunay vs DelaunayNN.
- Report, for both datasets, which inversion class each mesh is routed to before/after.

## Acceptance

- Parity unit tests: numba kernel vs the current NumPy reference on random meshes and on
  constructed edge cases (query on vertex, on edge, outside hull, degenerate) — mappings
  and sizes identical, weights to ~1e-12.
- Re-time on the Aris setup: Sibson step from ~18 s to tens of ms; DelaunayNN per-call
  cost close to Delaunay (report both vertex counts).
- Imaging and interferometer numba paths are taken by DelaunayNN mappers (asserted in a test
  of the routing), with likelihood parity vs the FFT/reference route.
- Existing DelaunayNN tests and the workspace_test parity scripts still pass.

<!-- formalised by the Intake (Conception) Agent on 2026-10-15 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/aaade95e-3f22-4661-b77d-365d91380803/scratchpad/delaunay_nn_numba.md -->
