# slope_hierarchy_scale `--use_cpu` must not disable the JAX likelihood

Type: bug
Target: graphical_ep
Repos:
- slope_hierarchy_scale
Themes:
- graphical-ep
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: `hpc/sync push-submit cpu scripts/ep.py` (the CPU partition) runs the EP arm with a vectorised JAX likelihood on the CPU backend and no multiprocessing pool, and the first factor_step completes; `use_jax` is no longer derived from the partition flag.
Review-minutes: 10
Unattended: ready
Gates:
- https://github.com/PyAutoLabs/PyAutoFit/issues/1608

## Original request (verbatim, from PyAutoFit#1608 phase 2)

> Root cause of the path being taken at all: the run was submitted --use_cpu,
> and scripts/ep.py:58 reads 'use_jax = not use_cpu'. That flag conflates 'run
> on the CPU partition' with 'disable JAX', so choosing CPU silently disabled
> the vectorised likelihood and dropped the fit onto the multiprocessing path.
> JAX-on-CPU, which needs no pool, is unreachable through that flag.
>
> 2. Confirm EP drives a vectorised JAX likelihood end to end (the machinery
> exists: use_jax is threaded through make_factor_graph), so parallelism comes
> from vectorisation rather than processes.

## Context

Phase 2 of PyAutoFit#1608, split out because the defect is in the science
project's own script (`PyAutoLabs/slope_hierarchy_scale`, `scripts/ep.py`),
not in PyAutoFit. The ruling of 2026-09-09 says EP parallelism comes from a
vectorised JAX likelihood, never from a Python multiprocessing pool; after
PyAutoFit#1608 lands, an EP factor search built with `number_of_cores>1`
refuses loudly, so a `--use_cpu` submission that still derives
`use_jax = not use_cpu` will fail at its first factor step instead of hanging.

## Scope

1. Decouple the two meanings of `--use_cpu` in `scripts/ep.py`: the SLURM
   partition (cpu vs gpu) and the likelihood backend (JAX vs numpy). JAX on
   the CPU backend is the default for the CPU partition; a separate explicit
   flag (e.g. `--no_jax`) opts out.
2. Build every EP factor search with `number_of_cores=1` (the ruling), and
   pass `use_jax=True` through `make_factor_graph` to the analyses.
3. Confirm end to end on RAL (CPU partition) that the EP arm gets past its
   first `factor_step` with JAX vectorisation and no pool, and record the
   run in the Cortex task `tasks/slope_hierarchy_scale/n25_scale_up.md`.

<!-- filed by /start_dev on 2026-09-11 as the phase-2 split of PyAutoFit#1608 -->
