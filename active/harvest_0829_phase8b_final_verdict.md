# Harvest 2026-08-29: Phase 8B FINAL verdict, W6 n_batch tail, Phase 6 NUTS probe

Type: feature
Epic: jax-inference-profiling
Target: autolens_profiling
Repos:
- @autolens_profiling
Themes:
- inference-programme
- profiling
- hpc
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Filed: 2026-08-29
Issued: 2026-08-29

## Original request (verbatim)

> Continue the JAX gradient epic which has A100s going on RAL and presumably lots have finished to update and check on

## Context

The RAL A100 queue drained on 2026-08-29. Four jobs landed and were surveyed and
harvested read-only into the session scratchpad (18 result JSONs + SLURM logs):

- **341978** — Phase 8B bijector A/B rerun, 15 arms, all real (3000 steps, walls
  1.8-4.1 h, stack 2026.8.17.1). With these the campaign reaches **39/39 arms**.
- **341987** — W6 Nautilus `n_batch` tail on `imaging/mge/hst`: n_batch 2000 and
  4000.
- **341988** — W6 Nautilus `n_batch` tail on `imaging/delaunay/hst` (512/1000):
  **no data** — a cuFFT batched plan wanted 25.31 GiB of scratch and the arm died
  with `JaxRuntimeError`, but the submit did not check the exit code, so SLURM
  recorded COMPLETED 0:0 and the failure was visible only in the `.err` file.
- **341981** — Phase 6 first `af.BlackJAXNUTS` probe: cold arm TIMEOUT inside
  warmup, warm arm completed.

Issues #162 / #163 / #187 are all closed, so none of these outcomes has an open
tracker.

## Goal

Land the harvest as repository record, in one PR:

- Commit the 18 result JSONs under `results/searches/...` and re-run
  `scripts/misc/searches/bijector_ab.py --stage score` in-repo so the committed
  `verdict_cpu_x86_64.json` is the 39-row, `preliminary: false` artifact.
- Write the FINAL Phase 8B verdict, the W6 tail reading and the Phase 6 probe
  result into `DECISIONS.md`, `PROGRAMME.md`,
  `phase_08_regularization/RESULTS.md` and `methods/nautilus.md`.
- Add the measured NUTS rate to `scripts/misc/wall/rates.py` and flip the NUTS
  probe submit's WALL-BASIS row from `unmeasured` to `rates`.
- Close the faked-pass channel: make a Python crash inside a `batch_gpu` job
  fail the SLURM job instead of exiting 0.

## Not in scope

- Resubmitting the delaunay `n_batch` tail (needs a chunked / smaller-batch
  redesign, not a resubmit).
- A second NUTS probe (dense metric from a Nautilus-sourced warm start).
- Merging PR#193.
