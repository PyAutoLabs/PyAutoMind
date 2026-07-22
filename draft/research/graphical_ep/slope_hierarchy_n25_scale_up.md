# slope_hierarchy: scale the hierarchical slope recovery to N=25–50

Type: research
Target: graphical_ep
Repos:
- slope_hierarchy
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

## Context

The `slope_hierarchy` science project (private, Jammy2211/slope_hierarchy#1,
external checkout `/mnt/c/Users/Jammy/Science/slope_hierarchy` — its own `main`,
no PyAutoLabs worktree) answered **all four of its goals** at N=5 and was wrapped
up on 2026-07-22. This is the *optional* scale-up that was left on the table, not
a blocker or an open defect.

Final N=5 parity (converged, `results/ep_history_n5_maxsteps12/`):

| parent | truth | draws | NUTS | EP (converged) |
|---|---|---|---|---|
| mean | 2.0 | 2.023 | 2.028 [2.000, 2.063] | 2.051 ± 0.0001 |
| sigma | 0.1 | 0.099 | 0.143 [0.117, 0.185] | 0.026 ± 0.00001 |

## The question

Does the picture hold at survey-relevant N? Specifically:

- Does **NUTS** stay the trustworthy method for the parent scatter as N grows —
  and does the scatter estimate tighten toward truth 0.1 the way more data should
  make it?
- Does **EP**'s ~4×-low scatter get *better* with N (more groups → more
  information in the parent factor) or *worse* (more per-group messages to
  over-shrink)? Either answer is publishable: the framing is **NUTS headline, EP
  cautionary**, and the EP arm is here to characterise the failure mode at scale,
  not to be rescued.
- Does the collapse basin documented in PyAutoFit#1405 show up more or less often
  at larger N?

## Mechanics (carried from the retired active.md entry — these are the traps)

1. Edit the simulator's `N` and re-simulate.
2. Submit with `submit_*` scripts using `--array` for the per-lens fits.
3. **`rm output/<sample>/*` before refits** — stale output silently resumes and
   you get the old answer back (`feedback_stale_test_mode_output_fakes_nonetype`
   is the same class of trap).
4. **Force-sync the truth files** to the cluster; a stale truth file makes the
   recovery scoring quietly wrong.
5. **Verify the RAL PyAutoFit mirror commit** before trusting a run — the HPC
   stack is a mirror of local `main` and drifts (`HPCPullPyAuto`; see
   `reference_ral_ssh_and_mirror_sync_traps`).
6. **`export JAX_ENABLE_X64=True` explicitly in the sbatch script** — it is
   ambient locally but *not* inherited by `sbatch`, and float32 silently ruins a
   gradient run (`reference_ral_sbatch_jax_x64_not_inherited`). Verify with
   `grep -c "truncated to dtype float32" *.err` == 0.
7. Repo is on **`autonerves`** (autoconf renamed; PRs #2/#3 landed 2026-07-18).

Cost note: RAL GPU contention has been severe (multi-day queues as of
2026-07-20). N=25–50 × per-lens fits is a large array job — check the queue
before committing to it, and consider the CPU `ral` partition for the EP arm
(finiteness, not throughput).

## Deliverable

An N=25–50 parity table in the same shape as the N=5 one, committed under
`results/`, plus an issue comment on slope_hierarchy#1. Feeds the write-up
(`slope_hierarchy_methods_writeup.md`).

<!-- filed 2026-07-22 when the slope-hierarchy task was wrapped up; all 4 goals
were answered at N=5, this is the optional scale-up. -->
