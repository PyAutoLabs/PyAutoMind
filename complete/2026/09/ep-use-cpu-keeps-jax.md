`scripts/ep.py` in the `slope_hierarchy_scale` science project derived `use_jax = not
use_cpu`, so `--use_cpu` meant both "run on the CPU partition" and "disable the
vectorised JAX likelihood". The 2026-09-08 CPU EP arm (job 342351_0) therefore ran the
numpy likelihood through a 10-worker multiprocessing pool, two forked workers segfaulted
and the parent hung 27 h; commit `6cea522` (2026-09-09) worked around it in the submit
script only. Phase 2 of PyAutoFit#1608, whose PR #1610 makes an EP factor search refuse
`number_of_cores > 1`.

`--use_cpu` is now a partition marker only: the likelihood stays the vectorised JAX one
on whatever backend `JAX_PLATFORMS` selects (the submit scripts pin cpu), and `--no_jax`
is the explicit opt-out. The EP Nautilus search is built with `number_of_cores=1` by
construction and `--number_of_cores` is removed — a stray flag fails at argparse rather
than being silently ignored. A one-line partition / likelihood / backend report prints at
start. `hpc/batch_cpu/submit_ep` passes `--use_cpu` again, drops `--number_of_cores=1`
and reads `MAX_STEPS` (default 12) so a short witness run ends cleanly; its comment block
carries the 342351_0 and 342410 history. `graphical.py`, `one_by_one.py`,
`hpc/template.py` and `util.py` keep `use_jax = not use_cpu` for the per-lens / NUTS arms
(their GPU submits never pass the flag) — noted, not changed.

**Shipped**

| repo | PR | merge commit |
|---|---|---|
| slope_hierarchy_scale | #4 | `174a9e1` |

**Evidence.** Local witness in the task worktree (2 lenses, 1 EP step,
`JAX_PLATFORMS=cpu JAX_ENABLE_X64=True … --use_cpu --total_datasets=2 --max_steps=1`):
exit 0 in 792 s; log shows `partition=cpu (--use_cpu) likelihood=JAX vectorised
jax_backend=cpu`, `Starting non-linear search with JAX (CPU: cpu)` and `Running search
with JAX vectorization` once per factor, zero matches for `Pool` /
`fit_multiprocessing` / `SearchException` / `Traceback`; `results/ep_sample_n25_seed42.json`
written. `--help` lists `--use_cpu` and `--no_jax` with no `--number_of_cores`;
`--number_of_cores=4` → argparse error rc 2; `py_compile` and `bash -n` pass. The repo
has no CI; merged on this evidence by the human's `/prm`. The worktree's gitignored
`dataset/<sample>/*.fits` had to be symlinked from the live clone for the local run
(only `info.json` / `truth.json` are tracked).

**Finding recorded on the way.** Job 342410 (2026-09-09, the submit-script workaround)
already took the JAX-on-CPU path with no pool: 76 factor searches (~3 EP steps of 25) in
~11 h, then `LLVM compilation error: Cannot allocate memory` / `LLVM ERROR: Unable to
allocate section memory!` at the 64 GB SBATCH limit — one fresh vmapped-likelihood jit
per factor search. Nothing had recorded it. Cortex ledger: 342410 marked done/failed,
Now refreshed. Filed as `draft/bug/autofit/ep_re_jit_compiles_the_vmapped_likelihood.md`
(PyAutoFit, gated on slope_hierarchy_scale#3).

**RAL witness (the prompt's scope 3).** The human chose a short run: after the merge the
live clone was fast-forwarded, `hpc/sync push` synced the code, the stale
`output/sample_n25_seed42/ep` on RAL was parked as `ep_dead_342410`, and
`sbatch --export=ALL,MAX_STEPS=2 submit_ep` submitted **job 343299** (the sync CLI's
`push-submit` does not forward environment variables, so `MAX_STEPS` was passed through
sbatch directly). Recorded under the Cortex ledger's `## Runs`; the first-factor-step
evidence is read at the next `/cortex` check-in — the session ended at the submit, not on
a timer. The RAL PyAutoFit mirror carries PyAutoFit#1610 (`650cb8833`).

**Gates.** Heart STALE at ship (release validation incomplete: no rehearsal for current
source); nothing in `slope_hierarchy_scale` is in the release chain. Not frozen at merge.
Fable 5.1 CLI session; implementation delegated to one Opus subagent.

## Original prompt

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
Issued: 2026-09-15
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
