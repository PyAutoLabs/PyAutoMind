# `jax.jit(jax.vmap(fn))` at B=50 returns wrong HST-scale inversion log likelihoods on an A100

Type: bug
Target: autoarray
Repos:
- PyAutoArray
- autolens_profiling
Themes:
- jax
- inversion
- hpc-gpu
Difficulty: medium
Autonomy: supervised
Priority: high
Status: draft — filed from certified-solver phase C1 (autolens_profiling#304), human-approved 2026-09-25
Epic: certified-positive-solver
Consequence: judge
Witness: A minimal script (no profiling harness) that builds the library imaging likelihood for the HST-scale fixed-light Delaunay N=1500 (or rectangular 39x39) pixelized source used in C1, evaluates B=50 lanes with `jax.jit(jax.vmap(fn))` and the same 50 lanes with per-lane `jax.jit(fn)`, and shows > 1 nat disagreement on the A100 80GB in fp64 (C1: 44-50/50 lanes). Then the same script records whether it reproduces (a) on CPU, (b) with `XLA_PYTHON_CLIENT_ALLOCATOR=platform`, (c) with `XLA_PYTHON_CLIENT_ALLOCATOR=cuda_malloc_async`, (d) with a smaller `XLA_PYTHON_CLIENT_MEM_FRACTION`, and whether the `bfc_allocator.cc:317` warning appears in each. The fix (or an XLA upstream report plus a library-side guard) is witnessed by the same script agreeing to <= 1e-6 relative on every finite lane at B=50.
Review-minutes: 15
Unattended: no
Filed: 2026-09-25

## Why this target

The fault is in a batched pixelized-inversion likelihood under XLA: the allocation that fails over
(18.31 GiB Delaunay / 18.56 GiB rectangular) is B x the 0.37 GiB PSF-convolved mapping cube, which
PyAutoArray's inversion builds. PyAutoArray owns that code path, so localisation starts there. It
may turn out to be an XLA/JAX bug under allocator pressure, in which case the deliverable is an
upstream report plus a library-side guard (for example a batch-size cap or chunked vmap). It is
not a solver question: every solver shows it (library PDIP, certified+PDIP, certified+none).

## The finding (autolens_profiling#304, phase C1, RAL array 350768)

- Device: NVIDIA A100 80GB PCIe, fp64, HST imaging, fixed lens light, dense inversion, border
  relocation on; Delaunay N=1500 and rectangular 39x39=1521; lanes replayed from real `af.Nautilus`
  proposal batches.
- At **B=50**, `jax.jit(jax.vmap(fn))` returns wrong log likelihoods on **44-50 of 50 lanes**, on
  both meshes, in all six B=50 tasks. Median error about 5200 nats (Delaunay) and 6000 nats
  (rectangular); relative error on individual lanes up to 9x (cross-composition 9.12 / 8.59
  relative, 2.07e5 / 2.13e5 nats worst).
- Example: Delaunay pix1, `call00015_lane00` (lane row 300), library PDIP: vmap **18700.6**, scalar
  `jit(fn)` **24758.5**, the capture's own Fitness evaluation **24758.5**. At B=16 and B=20 the same
  lane gives 24758.5 in both compositions.
- The values are not a permutation of other lanes' values (checked on the Delaunay PDIP task).
- **The C1 gate was blind to it:** the vmap arm and the independently compiled vmap library-PDIP
  reference agree with each other, so the own-composition 1e-9 pin passed most lanes. Only the
  ungated cross-composition column showed the fault.
- All six B=50 tasks, and only those, log XLA's
  `bfc_allocator.cc:317 ... ran out of memory trying to allocate 18.31 GiB` (18.56 GiB rectangular)
  `... The caller indicates that this is not a failure` warning, 10 times per task, peak use 58.8 GB.
  None of the 18 B <= 20 time tasks or the 4 rate tasks logs it or shows the fault. This is an exact
  correlation in one array, **not a demonstrated cause**.
- B=100 does not run at all (73.3 / 74.3 GiB single allocation, RESOURCE_EXHAUSTED) — a separate,
  honest OOM, not this bug.

## Evidence

- autolens_profiling commit `e38f645` (branch `feature/certified-solver-phase-c1-lane-rate`):
  JSONs `results/breakdown/imaging/*jitvmap50_captured_pix1*` (six tasks: 14-16 Delaunay, 26-28
  rectangular), per-lane `vmap.lane_construction.lane_rows`.
- Sidecar: `results/notes/certified_solver_phase_c1_job350768.json` (sacct rows, allocator
  excerpts, checksums).
- Note: `results/notes/certified_solver_phase_c1_lane_rate_2026_09.md`, Diagnosis 3.
- Library mains at replay: PyAutoArray `3de624b5`, PyAutoFit `dd9fbe0a`, PyAutoGalaxy `70a61e26`,
  PyAutoLens `86054bbc`, PyAutoNerves `1fa613aa`.

## Risk

Silent wrong likelihoods for any user batching >= 50 HST-scale pixelized lanes in one
`jit(vmap)` call on a GPU. Production Nautilus `n_batch=20` did not show it in C1, but nothing
currently prevents a larger batch, and nothing reports the failure — XLA says "not a failure".

## What

1. Reproduce with the minimal witness script on the A100 (RAL `gpu` partition); confirm scalar vs
   vmap disagreement and the allocator warning together.
2. Bisect the conditions: CPU; allocator modes (`platform`, `cuda_malloc_async`); preallocation
   off / smaller mem fraction; B between 20 and 50 (find the threshold); Delaunay vs rectangular;
   PDIP vs certified solve.
3. Localise inside the likelihood (mapping cube, curvature matrix, solve, log det) by comparing
   intermediate arrays between the two compositions on one lane.
4. Decide: library fix, library-side guard (cap or chunk the vmap batch), and/or upstream XLA
   report. Any C2 batched-guard work must keep a gated cross-composition check so this class of
   fault is visible.
