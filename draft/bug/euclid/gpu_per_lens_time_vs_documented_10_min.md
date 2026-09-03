# GPU route takes 1 h 14 min to 1 h 44 min per lens with the committed config, not the documented ~10 min

Type: bug
Target: euclid
Repos:
- euclid_strong_lens_modeling_pipeline
Themes:
- euclid
- jax
- hpc
Difficulty: medium
Autonomy: safe
Priority: medium
Status: formalised
Consequence: judge
Review-minutes: 10
Unattended: ready
Epic: euclid-dr1-prep
Parent: draft/feature/euclid/euclid_dr1_prep_epic.md
Filed: 2026-09-03
Updated: 2026-09-03

Found during the RAL acceptance runs of Mind phase 4 of the euclid-dr1-prep epic
(`euclid_strong_lens_modeling_pipeline#49`), which measured both submission routes
end to end for the first time from the pipeline repo's own scripts.

**Re-scoped 2026-09-03.** The prompt originally carried two candidate causes. The
second — the sparse-operator drift on the JAX path — has since been fixed inside
PR #50 and measured, and it is **not** the cause. That leg is closed below; what
remains open is the gap itself.

## The finding

The repository documents `scripts/initial_lens_model.py` as fitting a lens in
"around 10 minutes on a GPU, around 20 minutes on an 8-core CPU"
(`README.md`, `start_here.py`). Measured on RAL on 2026-09-03, on the committed
example lens `q1_walsmley/102018665_NEG570040238507752998`, with the committed
`config/`:

| Route | Allocation | `vis_lp` | `vis_pix` | Total |
|---|---|---|---|---|
| GPU (`hpc/batch_gpu/submit_initial_lens_model`, job 342248_0) | A100 80GB PCIe (`euclid-ral-gpu-2`), 1 core | 30.2 min | 42.4 min | 1 h 14 min |
| GPU, re-run after the sparse-operator fix (job 342264_0) | A100 80GB PCIe (`euclid-ral-gpu-1`), 1 core | 37.7 min | 63.8 min | 1 h 44 min |
| Two-stage CPU (`hpc/batch_cpu/submit_initial_lens_model_two_stage`, job 342244_0) | 8 cores, 8 pool workers | 25.5 min | 2 h 51 min | 3 h 17 min |

All three jobs COMPLETED, and both GPU jobs' fail-fast guard printed
`JAX backend: gpu`, so these are real GPU runs rather than the CPU-fallback case
that the same phase's MIG-mode incident produced. The GPU figure is roughly 7x the
documented one, and the CPU figure roughly 10x.

The documented figures come from the DR1 science runs, which used their own
`config/` tree, so they are not necessarily wrong — but nothing in the repository
says so, and a new user following `hpc/README.md` gets the measured numbers.
Phase 4 has already replaced the route-table figures with the measured ones and
attributed the ~10 min claim in `README.md` / `start_here.py` to the science-run
configuration; this prompt is about closing the gap rather than describing it.

## Closed: the sparse-operator drift is not the cause

`scripts/initial_lens_model.py` applied `dataset.apply_sparse_operator()` on the
JAX path in an `else:` branch the science tree's copy does not have
(`/mnt/c/Users/Jammy/Science/euclid/scripts/initial_lens_model.py:210-211`), and
`scripts/full_model.py:611` applied it unconditionally. Both were fixed in
`d32d58e` on `feature/euclid-cpu-two-stage-route`: the operator is the CPU route's
Numba tool, applied only under `--use_cpu`, and under JAX the pixelized inversion
runs on the plain dataset. `full_model.py` has no `use_cpu` at all and every one of
its searches sets `use_jax=True`, so the call was removed outright there.

The GPU route was then re-run on the same lens with the same config (job 342264_0,
the second row above). It got **slower**, and almost all of that is the node:

- `vis_lp` never touched the operator in either run and took exactly 15
  quick-update blocks in both, so it measures the node alone: 2.01 min per block
  against 2.51, a **25% slower node** on the re-run.
- `vis_pix` went from 3.26 to 4.55 min per block, a factor of 1.40. Net of the 1.25
  node factor, about **1.12** is left — one run against one run on a shared
  cluster, i.e. inside the noise.
- Quick-update cost is unchanged (13.8 s against 13.2 s mean over 13 and 14
  updates), so the visualisation cadence is not the difference either.

So `d32d58e` is a correctness fix — the JAX path now matches the science tree — and
not a performance fix. PyAutoLens is not implicated, and `Repos:` stays as it is.

## What is left: where the other ~7x lives

1. **The science configuration.** `hpc/README.md` "Config for large runs" already
   names three `config/general.yaml` keys the DR1 runs set differently:
   `output.samples_to_csv: false`, `hpc.hpc_mode: true` (no GUI visualisation or
   screen logging) and `numba.cache: false`. The committed config runs a quick
   update roughly every 2.5 min at about 14 s each, so visualisation overhead alone
   is only about 10% — not a 7x gap. Whatever else the science tree's `config/`
   changed has not been diffed against the committed tree, and **that diff is the
   first thing to do here**. The sampler settings matter most: `vis_lp` runs
   `n_live=750` with a large batch and `vis_pix` `n_live=300`, and a science tree
   running smaller values would finish in a fraction of the likelihood evaluations
   with no per-call speed-up at all.

2. **Per-sample work outside the sampler.** JIT compilation on the first likelihood
   call, latent-variable computation, and the visualisation written at each quick
   update are all per-lens costs that the science runs may have had switched off or
   amortised across a sample. `hpc.hpc_mode: true` covers part of this; the rest is
   unmeasured.

3. **The claim may not be for this lens or this model.** The ~10 min figure predates
   the public repo and is not tied in writing to a dataset, a mask radius or a
   model. A brighter or smaller-mask lens, or a run that stopped at `vis_lp`, would
   plausibly hit it. Establishing what the number was actually measured on may
   settle the whole prompt.

## Acceptance

- The ~10 min per-lens GPU figure is either reproduced (naming the exact `config/`
  changes that get there, which then belong in `hpc/README.md`'s "Config for large
  runs" list) or retired from `README.md` and `start_here.py` in favour of a
  measured number.
- `hpc/README.md`'s route table carries whatever the final numbers are.
- If the answer turns out to be the sampler settings, `hpc/README.md` says which
  ones and what they cost in posterior quality, so a user picking the fast route
  knows what they are trading away.
