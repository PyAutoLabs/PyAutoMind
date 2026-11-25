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
Gate: the library release carrying 5A–5E and the setup banner (the wiki pin and the API gate check released autolens); 5G (autolens_assistant#191) merged first.
Epic: likelihood-lifecycle
Phase: 5
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md

## Context

Split out of 5G (design call 3, human-approved 2026-11-25). The 5G survey found:
- `hpc/template.py` :15, :40-44, :172-175, :228-262 use `--use_cpu` → `use_jax=not use_cpu`;
- `hpc/batch_cpu/template` :22, :40, :95 and `hpc/batch_cpu/stage` :32, :79, :157 pass `--number_of_cores=$THREADS` and `JAX_PLATFORMS=cpu`;
- `wiki/core/operations/hpc.md` :25-72 and `hpc_infrastructure.md` :48-72 document the old two-regime table, including the stale claim that the sparse operator is CPU/numba-only and not applied on GPU.

The epic's 5H (science projects) makes the same `--use_cpu` → `--setup` change in the science repos, so keep the CLI contract identical across both.
