# Interferometer fixed-mapper searches: reuse the W~ curvature matrix across likelihood calls via `preloads.curvature_matrix`

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
- PyAutoLens
- PyAutoArray
Themes:
- interferometer
- pixelization
- likelihood-profiling
- jax-gpu
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft
Consequence: judge
Witness: A note section lists which production interferometer search stages (SLaM source-pix and any regularization-only stage) have a mapper that is constant across the search, each with a code citation. `results/breakdown/interferometer/{alma,jvla}` gains a fixed-mapper row: library call with `preloads.curvature_matrix` injected vs without. The two agree on the figure of merit to ≤ 1e-9 nats, and the row gives the measured saving against the F row (36–42 % alma, 91–92 % jvla).
Review-minutes: 12
Unattended: needs-slicing
Lane: local-dev
Epic: interferometer-likelihood-campaign
Filed: 2026-09-27

Follow-up to autolens_profiling#320, lever 3
(`results/notes/interferometer_mesh_a100_breakdown_2026_09.md`, "Ranked levers" §3).

## Why

On the A100 the sparse-path pixelized interferometer likelihood spends 36–42 % (alma), 66–73 %
(alma_high) and 91–92 % (jvla) of the call building F = Aᵀ W~ A. At jvla Delaunay-1500 that is
510 of 563 ms.

- `InversionInterferometerSparse.curvature_matrix` already returns an injected
  `preloads.curvature_matrix` untouched (PyAutoArray
  `inversion/inversion/interferometer/sparse.py:162-163`).
- The datacube case is shipped: `AnalysisInterferometer(shared_preloads=True)` builds F once
  per evaluation and shares it across channels via `shared_state_from` (PyAutoLens
  `interferometer/model/analysis.py:185-227`). That amortises F across channels **within** one
  call.
- Nothing reuses F **across** calls. When the mass is fixed and the image mesh is fixed, the
  mapper (and so A, F and D) is constant for the whole search, and only H, the solve and the
  log-dets change.
- Bound: skipping F takes jvla Delaunay from 563 ms to ~53 ms and alma from 49.5 ms to
  ~32 ms. This is a bound, not a measurement.

## What

1. **Census (read-only).** Which production interferometer stages have a constant mapper?
   Check the SLaM source-pix stages with mass fixed from source_lp, regularization-only
   searches, and the adapt-image / Hilbert image-mesh dependence (does the image mesh change
   between calls in those stages?). Cite file:line for each. If no production stage qualifies,
   stop here and record it.
2. **Measure (harness-injected).** For each qualifying configuration, run the alma and jvla
   Delaunay / rect cells (`scripts/interferometer/likelihood_breakdown/{delaunay,pixelization}.py`)
   with F built once and passed as `aa.PreloadsInterferometer(curvature_matrix=F)` through
   `fit_from(instance, preloads=...)`. Report per-call time vs the library row, the ≤ 1e-9 nats
   figure-of-merit match, and `jit(vmap)` behaviour. A closed-over F constant must not bloat the
   compiled program; record its size.
3. **Design sketch only.** An opt-in on `AnalysisInterferometer` (e.g. cache F keyed on the
   mapper identity, or a stage-level `fixed_mapper=True`) that reuses the `shared_preloads`
   plumbing. The invariance contract must be explicit: the user or pipeline asserts the mapper
   is fixed. Any library change is a separate prompt.

## Not in scope

Datacube channel sharing (already shipped). Mixed mapper + MGE inversions: the MGE columns
change with the lens light, although the mapper-mapper block could still be reused; note it
if the census finds it.
