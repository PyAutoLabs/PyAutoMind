## likelihood-lifecycle-p6c-gradient-walls
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/509
- completed: 2026-11-02
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/510 (witness v2 FD step sweep, d7b70a3f)
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/511 (measured v2 walls, 1cdf84bf)
- Campaign: v1 RAL 413707–413722; FD step diagnostic 413781 (mechanisms A–E); v2 RAL 413791–413830, 72/74 witness-valid; 512 GB rerun RAL 413890: delaunay_nn/hst CPU valid (~338 GiB, grad/forward 4.09x); imaging/delaunay/ao CPU still running at close — its record, wall and the imaging RAL CPU memory value move to 6d (autolens_profiling#512).
- Side runs: RTU vs Bilinear (413867–413870) → wrong-gradient bug filed (draft/bug/autoarray/rectangular_fiducial_gradient_wrong_rtu_and_cpu_sparse.md, now active as rectangular-gradient-rtu-sparse); Delaunay/Hilbert probe 413876 → complete/2026/11/likelihood-lifecycle-p6-delaunay-hilbert-roughness.md (human accepted: intrinsic).
- Closed early by the human ("yes do 1 and 2", 2026-11-02) with the one slow leg moved to 6d. The worktree ~/Code/PyAutoLabs-wt/likelihood-lifecycle-p6c-gradient-walls is kept: task rectangular-gradient-rtu-sparse reads its autolens_profiling checkout as a witness harness.

## Original prompt

# Likelihood lifecycle phase 6c: run the gradient campaign on RAL (74 legs, 14 submits)

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- profiling
- jax-gradient
Difficulty: medium
Autonomy: supervised
Priority: high
Status: issued
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/509
Issued: 2026-11-01
Consequence: judge
Witness: every one of the 74 gradient legs has run (exit, wall vs --time recorded) and wrote a gradient.json that passes gradient_witness.py --check, or its failure (non-finite / FD fail / OOM) is recorded as a result; timeouts resubmitted with raised walls; gradient_p6.py carries measured-wall WALL-BASIS rows from output/p6_gradient_logs/walls.tsv
Review-minutes: 30
Unattended: never
Epic: likelihood-lifecycle
Phase: 6
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-11-01

## Context

- 6a autolens_profiling#506 (a319e83): gradient harness, gradient_witness.py, gradient records in build_catalogue — complete/2026/11/likelihood-lifecycle-p6a-gradient-harness.md.
- 6b autolens_profiling#508 (97cdc88): --gradient hooks, 20 gradient_breakdown.py, scripts/misc/campaigns/gradient_p6.py (74 legs: 46 JAX optimal, 25 JAX CPU secondary of numba-optimal, 3 held datacube A100; 14 submits hpc/batch_cpu/submit_campaign_p6_gradient_<source>_ral_cpu_fp64 and hpc/batch_gpu/submit_campaign_p6_gradient_<source>_a100_fp64; walls unmeasured/probe-first at 4x the phase-2 runtime wall, >= 1200 s) — complete/2026/11/likelihood-lifecycle-p6b-gradient-scripts.md.

## Plan (approved by the human 2026-11-01)

1. RAL prep: submit checkout /mnt/ral/jnightin/profiling/autolens_profiling_p2dg moved to origin/main (97cdc88); private libraries /mnt/ral/jnightin/profiling/PyAuto_2026.10.25.1 all at tag 2026.10.25.1 (verified); hpc/batch_{cpu,gpu}/{output,error} present.
2. Batch 0 (probe, human go given): submit_campaign_p6_gradient_weak_ral_cpu_fp64 (1 leg, partition ral); gradient_witness.py --check on its gradient.json.
3. Batch 1 (human go): weak A100 + point_source, cluster, multi_galaxy_group CPU and A100 (18 legs).
4. Batch 2 (human go): imaging, interferometer, multi_dataset_datacube CPU and A100 (52 legs).
5. Per batch: job ids in the epic ledger; per-leg report — exit, wall vs --time, FD status / max rel error, grad/forward, hazard. Timeouts: raise the cell's guess in gradient_p6.py (or measured-wall rows), re-render, resubmit only those legs. Non-finite / FD fail / vmap OOM are results, kept.
6. PR: measured-wall WALL-BASIS rows into gradient_p6.py; merge by human /prm only.

Next (separate task, 6d): ingest gradient.json into results/, catalogue / coverage / day-zero pages / dashboard, frozen Pulse label for stamped gradients, hazards through /intake.

## Rules

No compute without the human's go per batch; CPU jobs only on --partition=ral; never merge without the human's /prm.

## Request (human, 2026-11-01, verbatim excerpt)

"Likelihood-lifecycle epic, phase 6c: run the gradient campaign on RAL, then hand back for 6d. [...] 6c — DO (one /start_dev task; plan for my OK; ask me for the Heart RED override; ask my go per batch) [...] RULES: report where things stand after every step; never merge without my explicit /prm; no compute without my go; CPU jobs only on the ral partition."

Heart at start: STALE (exit 1, monitoring RED 45/100) — not RED, no override invoked.
