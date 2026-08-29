# Nautilus: train neural bounds serially so a dead pool worker cannot hang the fit

Target: PyAutoFit
Type: bug
Autonomy: safe

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
