## likelihood-lifecycle-r6c-assistant-hpc
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/195
- completed: 2026-11-26
- workspace-pr: https://github.com/PyAutoLabs/autolens_assistant/pull/196
- epic: likelihood-lifecycle (R6 phase C)

autolens_assistant HPC templates moved to the automatic compute setup, merged before the R6 release by human ruling (works on 2026.11.25.1: `setup=` passed explicitly).

- `hpc/template.py`, `hpc/batch_cpu/{template,stage}`, `hpc/batch_gpu/template`: `--setup <auto|cpu|gpu|setup_id>` (default auto) and `--number_of_cores <auto|int>` (default auto), the same contract as euclid_strong_lens_modeling_pipeline#142; `--use_cpu` is a deprecated alias for `--setup cpu`. `cpu`/`gpu` export `PYAUTO_SETUP` and resolve as `"auto"`.
- Kept pins (commented): `JAX_PLATFORMS=cpu` on CPU jobs; `BLAS_THREADS` default 1 driving OMP/MKL/OpenBLAS/`NUMBA_NUM_THREADS`, because `number_of_cores=auto` runs one numba worker per CPU (differs from the Euclid stage, which defaults to the allocated CPUs).
- `wiki/core/operations/hpc.md` rewritten via al_update_wiki from the real `setup_rules.yaml`, stale "sparse operator CPU/numba-only" claim removed, pinned to library main (Array e261e6d6, Galaxy 9c391639, Fit 67164d22); `hpc_infrastructure.md`, `skills/init-slam.md`, `scripts/AGENTS.md` aligned.
- Tests: new `test_hpc_template.py`, updated `test_hpc_sync.py` (59 pass). The 9 `test_forward_model_consistency.py` errors ("Reference requires autolens==2026.9.27.2") are pre-existing on main.

## Original prompt

# autolens_assistant HPC: `--use_cpu` → `--setup` in the hpc templates, and the wiki/core HPC pages rewritten for the automatic compute setup

Type: feature
Target: autolens_assistant
Repos:
- autolens_assistant
Themes:
- hpc-gpu
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: draft
Consequence: judge
Witness:
- `hpc/template.py` and `hpc/batch_cpu/{template,stage}` (and the batch_gpu equivalents) take `--setup <auto|setup_id>`, default `auto`, instead of `--use_cpu` / hand-set `use_jax`, and `--number_of_cores auto` by default.
- `JAX_PLATFORMS=cpu` and thread pins are kept only where they are still needed, with a comment saying why.
- `wiki/core/operations/hpc.md` and `wiki/core/operations/hpc_infrastructure.md` are rewritten via `al_update_wiki`, with `sources:` and `pinned_commit` at the released library version, to describe `setup="auto"` / `number_of_cores="auto"`. The stale "sparse operator is CPU/numba-only, never on GPU" claims are removed.
- `skills/init-slam.md`'s CLI contract matches.
- `make test` passes. A dry `hpc/sync plan` against the new templates works.
Review-minutes: 20
Unattended: no
Lane: any
Filed: 2026-11-25
Issued: 2026-11-26
Gate: lifted 2026-11-26 by the human — merges before the release (wording true on both releases; no R6-only arguments).
Epic: likelihood-lifecycle
Phase: 5
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md

## Context

Split out of 5G (design call 3, human-approved 2026-11-25). The 5G survey found:
- `hpc/template.py` :15, :40-44, :172-175, :228-262 use `--use_cpu` → `use_jax=not use_cpu`;
- `hpc/batch_cpu/template` :22, :40, :95 and `hpc/batch_cpu/stage` :32, :79, :157 pass `--number_of_cores=$THREADS` and `JAX_PLATFORMS=cpu`;
- `wiki/core/operations/hpc.md` :25-72 and `hpc_infrastructure.md` :48-72 document the old two-regime table, including the stale claim that the sparse operator is CPU/numba-only and not applied on GPU.

The epic's 5H (science projects) makes the same `--use_cpu` → `--setup` change in the science repos, so keep the CLI contract identical across both.
