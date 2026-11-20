autolens_inference `hpc/sync submit` now passes allow-listed sbatch overrides (`--time`, `--no-requeue`, `--mem`, `--array`, `--dependency`) and `--env NAME=VALUE` (exported on RAL before sbatch; `SBATCH_*`/`SLURM_*`/`LD_*`/`PATH`… are refused), and logs every submit and cancel to `campaign/<name>/actions.log` on RAL in the AUTONOMY.md "Scheduler actions" format. Before, it took only a script name and `--dependency`, silently treated unknown flags as the script name, and logged nothing. A likelihood-lifecycle phase-4 timing resubmit (24 h limit, no requeue, XLA eigen flag) no longer needs a `PYAUTO_SKIP_SCHEDULER_GUARD` exception.

Witness (stub ssh/sbatch harness): `hpc/sync submit --cpu --campaign p4_validation --time 24:00:00 --no-requeue --env XLA_FLAGS=--xla_cpu_multi_thread_eigen=false submit_p4_validation_mge_hst_jax_cpu_dense` gives sbatch argv `["--time=24:00:00", "--no-requeue", "submit_p4_…"]` with XLA_FLAGS set, writes the actions.log line, and `scheduler_action_guard.check_command` ALLOWS the hpc/sync form while the old raw `ssh … sbatch` form is refused. `scripts/misc/test/test_hpc_sync_submit.py` 30 passed. Independent Opus review FINDINGS(3), fixed in ec96d96, then CLEAN. Heart GREEN at the door; CI GREEN at /prm.

Not checked: no real RAL submit yet; the job-side environment is inferred from sbatch's default `--export=ALL`, not observed. Decision taken (PR labelled `decision-taken`, merged by the human): the generator-side default `--no-requeue` and eigen flag in `validation_p4.py` are left for a follow-up.

Shipped in autolens_inference#72 (https://github.com/PyAutoLabs/autolens_inference/pull/72), merged 2026-11-20 by human /prm. Issue https://github.com/PyAutoLabs/autolens_inference/issues/71. Done by shift worker 2026-11-19-pm2 (98526c76); epic likelihood-lifecycle phase 4 tooling.

## Original prompt

# autolens_inference `hpc/sync submit` can't pass `--time`, `--no-requeue` or environment variables, so every timing resubmit needs a scheduler-guard exception

Type: feature
Target: autolens_inference
Repos:
- autolens_inference
Themes:
- hpc
- inference
Difficulty: small
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: judge
Witness: `hpc/sync submit` accepts sbatch overrides (at least `--time`, `--no-requeue`) and forwards named environment variables (e.g. `XLA_FLAGS`) to the remote sbatch. Each submit is logged the way the scheduler-actions policy expects. A phase-4-style resubmit (24 h limit, no requeue, XLA eigen flag) then goes through hpc/sync with no `PYAUTO_SKIP_SCHEDULER_GUARD` exception.
Review-minutes: 10
Unattended: ready
Verified: 2026-11-19 9f05aa9f (autolens_inference)
Lane: ral
Epic: likelihood-lifecycle
Phase: 4
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-11-09

## Finding

From 2026-11-05 to 11-09 a PreToolUse hook blocked raw `sbatch`: campaign jobs must go through `hpc/sync` so each action is logged. autolens_inference's `hpc/sync submit` (`submit()` in `hpc/sync`) takes only a script name and `--dependency`, and runs `sbatch` over ssh, so local environment variables never reach the job. The project also has no `hpc/sync act …` and no `campaign/<name>/actions.log`. Every phase-4 timing resubmit therefore needed a human-directed `PYAUTO_SKIP_SCHEDULER_GUARD=1` exception: 414362, 414392, and 414639–414641.

Three things were needed and couldn't be passed:
- `--time`: the generator's estimates missed by up to 4.5×; see complete/2026/11/validation-wall-estimates-miss-eval-count-and-sampler-floor.md (fixed 2026-11-16, autolens_inference#70).
- `--no-requeue`: a SLURM auto-requeue after NODE_FAIL silently resumed 414392, and a resumed Nautilus stage's wall is invalid.
- `XLA_FLAGS=--xla_cpu_multi_thread_eigen=false`: the jaxlib 0.11.2 JAX CPU deadlock workaround (Pulse decision xla-cpu-deadlock-eigen-workaround).

## Fix direction

- Extend `submit()` with pass-through sbatch flags (allow-listed: `--time`, `--no-requeue`, `--mem`, `--array`) and `--env NAME=VALUE`. Export the variables in the remote shell before `sbatch`, quoting safely.
- Consider making `--no-requeue` the default for `p4_validation`/timing submits. Consider generator-side support for the eigen flag in JAX CPU submit scripts, so it isn't an env var at all.
- Mirror whatever logging the scheduler-actions policy (AUTONOMY.md "Scheduler actions") expects, or adopt the profiling repo's `hpc/sync act` if it exists there.

## Original request (verbatim, 2026-11-09)

Filed at the end of the phase-4 chat when the human paused Pulse work ("assume we are not doing any more pulse work in this chat"), so that the gap doesn't live only in memory.

## Answers from the human
- Q4 (2026-11-18, ruling unattended, shift ready-2026-11-18): (a) make it ready: slice or size it so a shift can start it
