## Summary

Two regressions in multi-core `af.Nautilus` fits, both from PyAutoFit #1439 (2026-07-31, the Py3.14
fork-context pin that replaced `pool=<int>` with a `Pool` object), found while running the first
`subhalo_validation` SLaM job on RAL and fixed in PyAutoFit PR #1548 (`e6ff1e65`, merged 2026-08-30).

1. **Per-task pickling of the Fitness.** With a `Pool` object nautilus maps the bound `Fitness.call_wrap`
   directly, so multiprocessing pickled the whole analysis + dataset (PSF Convolver, 172 MB numba sparse
   operator, adapt images — 173.7 MB per task) into every task chunk; each worker unpickled a fresh dataset
   per likelihood call. Symptoms: worker memory +59.5 MB/call (8-core RAL jobs hit 96 GB → `OUT_OF_MEMORY`),
   per-call 1.7 s vs 0.25 s, only ~2.4 of 8 cores busy. Fix: build the fork pool with nautilus's
   `initialize_worker(fitness.call_wrap)` and hand nautilus `_LikelihoodWorkerPool`, whose `map` dispatches
   `likelihood_worker` (the pre-#1439 int-pool behaviour).
2. **Dead worker hangs the fit.** nautilus used the same pool for neural-bound training; a worker
   OOM-killed mid-`map` is replaced by `Pool` but its task never re-issued, so the fit idled for hours at
   ~0% CPU. Fix: `pool=(pool, None)` — bound training serial in the parent (4 small MLPs, negligible).

## Evidence

- RAL jobs 342005/6/7 (hung, `sstat` AveCPU ≈ 7 min / 2.6 h), 342020 (`OUT_OF_MEMORY` at 96 GB), py-spy
  dumps (main in `nautilus/neural.py:96 train → pool.map`; later a worker rebuilding `Convolver` via
  `psf.reversed_kernel` at minute 22 = fresh dataset per call).
- Local harness `subhalo_validation/scripts/scratch/memory_growth.py`: pickled-func map +59.5 MB/call/worker
  linear; initializer-global map flat (0.19 MB/call). NNLS warm-start memo exonerated (4 KB, capped).
- After the fix, RAL job 342027: memory flat 6–9 GB/task over 5 polls, ~6 cores busy.

## Tests

`test__multi_core_passes_serial_sampler_pool`, `test__likelihood_pool_does_not_pickle_fitness` (a
`__getstate__`-raising fitness maps correctly through the wrapper and raises through a plain pool);
`test_nautilus.py` 6 passed; `non_linear/search` 326 passed, 2 skipped; CI green 3.12 / 3.13 / nojax.

## Follow-ups filed

- `draft/refactor/autoarray/sparse_operator_int32_indexes.md` — shrink the 172 MB sparse-operator payload.
- (project) `Imaging.apply_over_sampling` drops the sparse operator — re-apply after adaptive over-sampling.

## Original prompt

# Nautilus: train neural bounds serially so a dead pool worker cannot hang the fit

Target: PyAutoFit
Type: bug
Autonomy: safe
Issued: 2026-08-29

## Original request (verbatim)

PyAutoFit: Nautilus multiprocessing — run neural-bound training serially in the parent (pass pool=(pool, None)) so a dead fork-pool worker cannot hang Pool.map during bound construction; keep likelihood evaluation parallel. Found on RAL 2026-08-29 in subhalo_validation job B (py-spy: main in nautilus/neural.py:96 train → pool.map, workers idle, _repopulate_pool replacement worker). Change is at autofit/non_linear/search/nest/nautilus/search.py ~L352 (`pool=pool`).

## Context

- `fit_multiprocessing` builds a fork-context `Pool(number_of_cores)` and passes it as `pool=pool`;
  nautilus (`sampler.py:281-295`) uses a single pool for both likelihood calls (`pool_l`) and
  sampler calculations (`pool_s`), including `NeuralNetworkEmulator.train` (`neural.py:96`),
  which maps `n_networks` (4) sklearn MLP fits over the pool.
- If a worker dies (per-job OOM on RAL, 8 workers × 1–2.8 GB) `multiprocessing.Pool` spawns a
  replacement but never re-issues the lost task, so `pool.map` blocks forever; observed on three
  jobs simultaneously (342005/6/7), each idle for hours at 0.7% CPU.
- nautilus accepts `pool=(pool_likelihood, pool_sampler)`; `None` for the second keeps bound
  training in the parent. Cost: 4 small MLPs on ≤ few hundred points, per bound — negligible
  next to likelihood evaluation.

## Acceptance

- `search.py` passes `pool=(pool, None)` when `number_of_cores > 1`; serial path unchanged.
- Unit test asserting the tuple is passed (mock sampler_cls) and that `number_of_cores<=1`
  still passes `pool=None`.
- Docstring/comment explains the dead-worker hang and why bound training stays serial.
