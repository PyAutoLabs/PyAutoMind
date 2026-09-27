# Retune the interferometer numba gate 60 → 70 (in-situ crossover, autolens_profiling#332)

Type: feature
Target: autoarray
Repos:
- PyAutoArray
- autolens_profiling
Themes:
- interferometer
- numba-cpu
- config
Difficulty: small
Autonomy: supervised
Priority: low
Status: draft
Consequence: glance
Witness: with `interferometer_numba_nnz_per_source_max: 70.0`, the factory routes to the faster arm at every measured RAL CPU cell of autolens_profiling#332 (sma / alma r2.0-6.0 / alma_high, both meshes) plus two new in-band cells (alma rect r4.6, nnz ≈ 70; alma Delaunay r5.4, nnz ≈ 66), each measured numba vs NumPy FFT on the #332 harness.
Review-minutes: 6
Lane: local-dev
Epic: interferometer-likelihood-campaign
Filed: 2026-09-27

## Context

The packaged gate is one number for both meshes: PyAutoArray `autoarray/config/general.yaml:21`
(`interferometer_numba_nnz_per_source_max: 60.0`), read at
`autoarray/inversion/inversion/factory.py:284` in `_use_interferometer_numba`. Its comment quotes
"~60 (Delaunay) and ~77 (rectangular)" from #226 (prototype pack, three fiducials).

The in-situ library-dispatch sweep in autolens_profiling#332
(`results/notes/interferometer_mesh_cpu_breakdown_2026_09.md`) measured the numba / NumPy FFT
full-call ratio across alma mask radii. It brackets the crossover at **nnz/col ≈ 66–67
(Delaunay: 55.6 → 0.886, 81.4 → 1.169)** and **≈ 72–73 (rect: 59.7 → 0.749, 82.7 → 1.225)**.

- **Gate 60.** Rect cells with nnz 60–72 run the FFT route, up to 1.33× slower than numba.
  Delaunay cells at 60–66 are up to 1.08× slower.
- **Gate 70.** The worst mis-route is ≤ 1.03× (Delaunay 66–70) and ≤ 1.07× (rect 70–72).
- Every *measured* cell routes correctly at both 60 and 70. The move rests on interpolation, so
  the witness adds measured in-band cells first.

## What

1. autolens_profiling: two RAL CPU rows on the #332 harness
   (`scripts/interferometer/likelihood_breakdown/{pixelization,delaunay}_numba.py --mask-radius`)
   at alma rect r4.6 and alma Delaunay r5.4. Confirm the predicted nnz/col and the ratio side.
2. PyAutoArray: set `general.yaml:21` to 70.0 and re-quote its comment to "in situ ≈ 66
   (Delaunay) / ≈ 72 (rectangular), autolens_profiling#332". Mention that the crossover drifts up
   with the extent (alma_high extrapolates to ≈ 80). Update the docstrings that quote 60 / 77:
   `inversion_interferometer_numba_util.py` `nnz_per_source_column_from` and
   `interferometer_numba/sparse.py` class docstring.
3. Any unit test pinning 60.0 as the default.

## Out of scope

A per-mesh or per-extent gate (the data does not yet justify a second number). GPU routing.
