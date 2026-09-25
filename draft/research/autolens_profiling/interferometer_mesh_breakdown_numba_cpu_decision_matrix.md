# Interferometer likelihood campaign 3/3: mesh breakdown on numba sparse CPU, and the CPU-vs-GPU "which likelihood when" decision matrix

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- interferometer
- numba-cpu
- likelihood-profiling
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Consequence: glance
Witness: `results/notes/interferometer_likelihood_decision_matrix_2026_09.md` has a CPU-vs-A100 row for Delaunay-1500 at sma, alma and alma_high with mask radii 2.0/3.5/5.0, and the numba breakdown JSON's `configuration.inversion_path` reads `InversionInterferometerSparseNumba` for the gated arm.
Review-minutes: 8
Unattended: needs-slicing
Lane: local-dev
Epic: interferometer-likelihood-campaign
Filed: 2026-09-25

Mirror of the imaging numba CPU campaign (#263-#282: HST Delaunay 932 -> 230 ms) for
the interferometer sparse path on CPU, through the **library dispatch**
(`inversion_interferometer_from`, `factory.py:162-320`), which since PyAutoArray #544/#545
routes to `InversionInterferometerSparseNumba` (`direct_conv`, O(nnz*M)) when
`xp is np`, one mapper, `sub_fraction == 1`, and mean nnz per source column <=
`Settings.interferometer_numba_nnz_per_source_max` (60.0), else to the FFT sparse path.

Supersedes `draft/research/autolens_profiling/interferometer_numba_library_dispatch_insitu.md`
(its step 0 landed as #239/#240; fold the crossover re-measurement in and retire the
draft on filing).

## What

- Breakdown cells `delaunay_numba.py` / `pixelization_numba.py` re-pointed at the library
  factory rather than the prototype pack (`scripts/misc/numba_interferometer/`), with the
  same production discipline as the imaging numba cells (#235: iid instance stream, 1
  thread pinned, memo off, dgemm/Cholesky controls, log-evidence pins with
  `pinned_expected`/`pinned_drift`). Setups as task 2/3: Hilbert 1500 + AdaptSplit and
  39x39 Constant(1.0), no lens light; plus an N sweep 1000/1500/2500/4000.
- Three CPU arms on identical inputs, driven by
  `Settings(interferometer_numba_nnz_per_source_max=...)`: numba `direct_conv`, JAX-CPU
  FFT sparse (`xp=jnp`), NumPy FFT sparse (`xp=np`, gate 0). Steps: triplets, D, F
  (kernel vs rfft2 blocks), regularisation, fnnls/PDIP solve, log-det (fnnls passive-set
  reuse), chi-squared. Instruments sma, alma, alma_high (the FFT cost is set by the mask
  extent, 140^2 / 280^2 / 560^2, not by N_vis).
- Re-measure the crossover in situ and decide whether 60.0 (Delaunay) / ~77
  (rectangular, #226) is the right packaged default; add the section to
  `results/notes/numba_interferometer_verdict.md` and, if it moves, file the
  PyAutoArray `general.yaml` retune prompt.
- Optimisation task list in `results/notes/interferometer_mesh_cpu_breakdown_2026_09.md`
  (ranked, step/bound/gain, one prompt per lever): the `prange` kernel variant and
  `NUMBA_NUM_THREADS` scaling; fnnls warm-start memo (imaging: no lever at N4000, check
  here); Cholesky reuse for the log-det; whether the `kernel_index_arrays` marshalling
  inside F is a fixed cost worth preloading; a numba route for the MGE+mesh combination
  (never routed to numba today).

## The decision matrix (epic deliverable)

Write `results/notes/interferometer_likelihood_decision_matrix_2026_09.md`, the user-facing
answer to "which interferometer likelihood do I use if I have a CPU and a GPU?". Axes:

- **Number of visibilities**: 190 (sma), ~1e5 (`autolens_workspace` sdp81, 108,384,
  real data), 1M, 5M, 25M. The sparse paths are N_vis-independent per evaluation but
  pay the one-off preload (type-1 NUFFT, 7.3 s alma / 22 s alma_high) and dirty image;
  the dense NUFFT path scales with N_vis; the DFT is capped at 1e4 vis by default.
- **Real-space mask size**: mask radius 2.0 / 3.5 / 5.0 arcsec at alma pixel scale, so
  M = 4*y*x spans ~1e4 to ~1e5 and the FFT vs direct_conv vs dense costs separate;
  report masked pixels and nnz per source column per row.
- **Source model**: MGE-20 (dense path, task 1/3), Delaunay 1500, rectangular 39x39.
- **Device x path**: CPU numba direct_conv, CPU FFT (NumPy / JAX), CPU dense NUFFT,
  A100 FFT sparse, A100 dense NUFFT (rows from tasks 1/3 and 2/3 plus this task).
- Per cell: ms per likelihood evaluation, one-off setup seconds, peak RAM/VRAM, and the
  log-evidence agreement between paths (0.5-nat bar).

Output a table plus a short rule set (e.g. "below X vis and Y masked pixels stay on
CPU numba; above M = ... the A100 FFT path wins by Z x; MGE at 1M+ vis needs the W~
route from task 1/3 lever 1 first"), and a `results/README.md` pointer so the matrix
is the entry point the next campaign builds on. Cross-check the Q1/Euclid-style
"time per fit" by multiplying by the Nautilus evaluation counts recorded in
`results/runtime/` comparison files.

## Done when

- Committed numba/FFT breakdown JSON+PNG rows at sma/alma/alma_high for both meshes
  through the library dispatch, README dashboards regenerated, lint green.
- The verdict note carries the in-situ crossover section and the gate default is
  confirmed or a retune prompt is filed.
- The decision-matrix note exists with every cell either filled or marked blocked with
  the reason (e.g. MGE at alma OOM), and is linked from `results/README.md`.

Consequence: glance
Witness: `results/notes/interferometer_likelihood_decision_matrix_2026_09.md` has a CPU-vs-A100 row for Delaunay-1500 at sma, alma and alma_high with mask radii 2.0/3.5/5.0, and the numba breakdown JSON's `configuration.inversion_path` reads `InversionInterferometerSparseNumba` for the gated arm.
Review-minutes: 8

<!-- formalised by the Intake (Conception) Agent on 2026-09-25 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/ab334050-3e04-48cf-8914-a1e38ba0a9e5/scratchpad/prompts/interferometer_mesh_breakdown_numba_cpu_decision_matrix.md -->
