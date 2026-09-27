# Interferometer likelihood campaign 3/3 — mesh numba CPU breakdown + CPU-vs-GPU decision matrix — phase map (phase 1 shipped; phases 2 & 3 unblocked)

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
Status: campaign map — phases issued one at a time
Consequence: glance
Witness: `results/notes/interferometer_likelihood_decision_matrix_2026_09.md` has a CPU-vs-A100 row for Delaunay-1500 at sma, alma and alma_high with mask radii 2.0/3.5/5.0, and the numba breakdown JSON's `configuration.inversion_path` reads `InversionInterferometerSparseNumba` for the gated arm.
Review-minutes: 8
Unattended: needs-slicing
Lane: local-dev
Epic: interferometer-likelihood-campaign
Filed: 2026-09-25
Updated: 2026-09-27

## Phase 1 shipped (2026-09-27)

- **Merged:** autolens_profiling#328 at `ea2711d9` (issue #326). Record
  `complete/2026/09/interferometer-mesh-numba-p1.md`.
- **Landed:** library-dispatch harness `scripts/misc/likelihood_breakdown/interferometer_pixelized_numpy.py`,
  `--mask-radius` on the JAX harness, thin numba cells, 8 RAL CPU submits, RAL CPU fp64 rows
  (sma / alma / alma_high, both meshes) + alma N sweep.
- **Headline:** numba 2-4x faster than NumPy FFT at sma / alma; loses at alma_high (nnz/col 118-162),
  where JAX-CPU is fastest. Witness PASS (`InversionInterferometerSparseNumba`; numba vs FFT
  <= 9.1e-13 nat; step sum 0.996-1.006). sma adapt image kept at the May-18 copy (human, 2026-09-27).
- **Next:** Phases 2 and 3 are unblocked and can be issued in parallel. Follow-up filed:
  `draft/feature/autoarray/interferometer_sparse_numpy_cache_curvature_and_data_vector.md` — library half
  shipped 2026-09-27 (`complete/2026/09/interferometer-sparse-cache.md`, PyAutoArray#582).

## Campaign contract

Task 3/3 of `interferometer-likelihood-campaign` (1/3 MGE and 2/3 mesh-on-A100, PR #324, are
shipped). The Feature Agent sized it large; the human approved a four-phase split on
2026-09-27. At start-dev issue ONLY the next bounded phase (one issue + one PR each, all in
autolens_profiling), retaining this prompt in `draft/` as the campaign intent until every
phase is resolved. Phases 2 and 3 can run in parallel once Phase 1 lands `--mask-radius`.
The #235 imaging numba discipline governs every CPU row: 1 thread pinned
(`NUMBA_NUM_THREADS=1`, BLAS=1), memo off, iid instance stream, log-evidence pins
(`pinned_expected` / `pinned_drift`), step sum vs the full library call, quiet RAL CPU
(`gpu` partition, no `--gres`) as the timing reference — the laptop fails the ABBA gate.

## Survey (2026-09-27)

- `scripts/interferometer/likelihood_breakdown/delaunay_numba.py` / `pixelization_numba.py`
  still import the prototype pack (`scripts/misc/numba_interferometer/inversion`), not the
  factory; the shared harness `scripts/misc/likelihood_breakdown/interferometer_pixelized.py`
  is JAX-only (`xp=jnp`, asserts `InversionInterferometerSparse`).
- Gate: PyAutoArray `autoarray/inversion/inversion/factory.py:242-321`
  `_use_interferometer_numba` (xp is np, one mapper, sub_fraction == 1, mean nnz/col <=
  `interferometer_numba_nnz_per_source_max`, `config/general.yaml:21` = 60.0). The task-2/3
  setups (AdaptSplit Delaunay, edge-zeroed rect, `over_sample_size_pixelization=1`) pass it;
  nnz/col decides. The NumPy path solves with fnnls and reuses its Cholesky for the log-det.
- Predicted Delaunay nnz/col: sma r3.5 7.7, alma r2.0 ~10, alma r3.5 30.8, alma r5.0 ~63,
  alma_high r3.5 123 — alma r5.0 straddles the 60 gate: the natural crossover probe.
- All task-2/3 A100 rows are at mask r3.5, so the witness's r2.0 / r5.0 GPU rows need new jobs.
- No `results/runtime/` file records Nautilus evaluation counts — the original time-per-fit
  cross-check has no source as written (decision below).
- sdp81 (108,384 vis) is local in `autolens_workspace/dataset/interferometer/sdp81/` but has no
  instrument preset / real-space mask.
- No interferometer `hpc/batch_cpu/` submit scripts exist; template
  `hpc/batch_cpu/submit_breakdown_imaging_fixed_light_numba_delaunay_ral_hst_fp64`.

## Decision (human-approved default, 2026-09-27)

Time-per-fit: take Nautilus evaluation counts from already-completed fits' search output
(`samples_summary` / `search.summary` total evaluations — e.g. the Q1 example lens GPU fit and
`autolens_inference/output/`), cite each source, and label the column "indicative". No new
Nautilus runs in this campaign.

## Phases

### Phase 1 — library-dispatch CPU cells (CPU only) — SHIPPED 2026-09-27

Record `complete/2026/09/interferometer-mesh-numba-p1.md` (task `interferometer-mesh-numba-p1`, autolens_profiling#326, PR #328 merge `ea2711d9`).
- New sibling harness `scripts/misc/likelihood_breakdown/interferometer_pixelized_numpy.py`
  reusing the JAX harness's dataset / mesh / adapt setup, timing the library's own
  `InversionInterferometerSparseNumba` / `InversionInterferometerSparse(xp=np)` steps
  (triplets, D, F incl. `kernel_index_arrays` marshalling, regularisation, fnnls, log-det,
  chi-squared). Three arms on identical inputs via
  `Settings(interferometer_numba_nnz_per_source_max=...)`: numba (gate forced to admit),
  NumPy FFT (gate 0), JAX-CPU FFT (existing harness). JSON records
  `configuration.inversion_path`; the cell asserts the path it asked for.
- Re-point `delaunay_numba.py` / `pixelization_numba.py` at the new harness (thin CLI
  wrappers); the prototype pack stays untouched.
- `--mask-radius` on both harnesses (preset default 3.5; W~ preload cache keyed by radius).
- RAL `hpc/batch_cpu/submit_breakdown_interferometer_{delaunay,pixelization}_numba_ral_*`
  for sma / alma / alma_high at r3.5 plus the alma N sweep (1000/1500/2500/4000).
- Witness: gated-arm JSON `configuration.inversion_path == "InversionInterferometerSparseNumba"`,
  numba vs FFT log-evidence <= 0.5 nat (expect ~1e-8), step sum within 10 % of the full call.

### Phase 2 — in-situ crossover + CPU lever list (CPU only)

- Sweep numba vs NumPy FFT across alma r2.0 / 3.5 / 5.0 and alma_high r3.5 for both meshes
  (nnz/col ~10 -> 123); re-derive rect nnz in situ (the #226 rect values do not reproduce as
  4·M/1521).
- New section in `results/notes/numba_interferometer_verdict.md`; confirm 60 / ~77 or file the
  PyAutoArray `general.yaml` retune prompt.
- `results/notes/interferometer_mesh_cpu_breakdown_2026_09.md`: ranked levers (prange +
  `NUMBA_NUM_THREADS` scaling, fnnls warm-start memo, Cholesky reuse, `kernel_index_arrays`
  preload, MGE+mesh numba route), one draft prompt per worthwhile lever.
- Witness: measured crossover bracketed by two measured points per mesh.
- Fold-in candidate: `draft/research/autolens_profiling/interferometer_sparse_cache_after_measurement.md` (harness cached_property counter fix + RAL CPU numba re-run of sma/alma/alma_high on PyAutoArray main ≥ e281abf3) — phase 2 re-runs these rows anyway.

### Phase 3 — A100 mask-radius sweep (new RAL GPU jobs)

- Delaunay-1500 fp64 at r2.0 and r5.0 for sma / alma / alma_high (6 jobs; rect optional +6)
  via the existing `hpc/batch_gpu/submit_breakdown_interferometer_*` with `--mask-radius`.
- Witness: `results/breakdown/interferometer/<inst>/delaunay_hpc_a100_fp64_r{2.0,5.0}.json`
  with non-null steps.

### Phase 4 — the decision matrix (epic deliverable)

- `results/notes/interferometer_likelihood_decision_matrix_2026_09.md`: N_vis (190 / 1e5 sdp81
  / 1M / 5M / 25M) x mask radius x source (MGE-20, Delaunay-1500, rect 39²) x device/path;
  ms/eval, one-off setup s, peak RAM/VRAM, log-evidence agreement; every cell filled or marked
  blocked with the reason (e.g. CPU alma_high MGE W~ empty, A100 library dense OOM >= alma); a
  short rule set; `results/README.md` pointer.
- sdp81 row: add an sdp81 preset + mask to `instruments/interferometer.py`; one CPU + one small
  A100 job.
- Time-per-fit column per the decision above.
- Witness: the campaign witness (CPU-vs-A100 Delaunay-1500 rows at sma / alma / alma_high x
  r2.0 / 3.5 / 5.0).

## Original prompt

_Filed 2026-09-25 by the Intake Agent; preserved verbatim below the header._

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
