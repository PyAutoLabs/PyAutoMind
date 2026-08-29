## harvest-0829-phase8b-final
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/194
- completed: 2026-08-29
- library-pr: autolens_profiling#195 (merged a305a49c -> main); alongside autolens_profiling#193 W6 tail submits (merged 24155feb -> main)
- what shipped: RAL harvest of 341978/341981/341987/341988 — 18 result JSONs; Phase 8B FINAL verdict on 39/39 arms = FALSIFIED 3/4 (F1, F3, F4), `preliminary: false`, F2 not falsified, F5 diagnostic max rel 1.06e-5, 23/39 best points |e|>1; W6 n_batch tail (MGE wall optimum n_batch=2000, 4.19 ms/eval, logZ drift -0.24 nat over the scan; delaunay leg LOST to cuFFT 25 GiB OOM reported as COMPLETED); Phase 6 NUTS probe (3.42 s/draw @ 4 lanes = 38.53 ms/eval in wall/rates.py; warm arm reaches basin but rhat 3.9 / 50% divergences -> H6.1 unsupported with MAP-sourced diagonal metric; cold arm timed out at 0:45 -> submit budget 2:00). Three DECISIONS.md entries, PROGRAMME rows + new W11, phase_08 RESULTS.md + 39-arm appendix, methods/nautilus.md rows, `activate.sh` SLURM exit-code guard (85 submits).
- validation: scorer reproduced the verdict byte-identically in the worktree; appendix re-derived from committed JSONs; lint CI green (ruff, format, build_readme --check, check_submits --check, pytest 256 passed).
- heart-ack: shipped + merged under human-authorised YELLOW ("1 yes", 2026-08-29) — reasons verbatim: "workspace validation not passing (0 failed, 1 timeout, cloud#33229145647: autolens_test scripts/multi_dataset/delaunay_mge.py)" and "release validation incomplete: no rehearsal for current source" — release-chain, other repos; this PR touches no library source.
- caveats: PyAutoFit stack SHA is unverifiable from artifacts (JSONs carry only `version: 2026.8.17.1`) — "library SHAs in the results schema" filed in W11; sacct COMPLETED is not evidence (341988) — guard added.
- human calls left open: delaunay n_batch tail redesign DECLINED 2026-08-29 ("doesn't sound worth it"); dense-metric NUTS probe from a Nautilus warm start APPROVED in principle, to be planned as a new task; slam_source_pix_nn refs 5,6 still HELD.

## Original prompt

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
