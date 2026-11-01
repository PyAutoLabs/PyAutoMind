Likelihood lifecycle phase 6b: a gradient script for every designated likelihood and the gradient_p6 campaign generator.

- Merged: https://github.com/PyAutoLabs/autolens_profiling/pull/508 (`97cdc88`, 2026-11-01, human /prm; lint green on `4385ce6`, including the smoke import of every gradient_breakdown.py). Issue https://github.com/PyAutoLabs/autolens_profiling/issues/507 closed. Heart RED development override invoked by the human 2026-11-01.
- Human ruling 2026-11-01 (AskUserQuestion): a `--gradient` hook at each fused-likelihood construction site (not standalone builders), so the gradient is of exactly the likelihood the runtime row timed.
- Shipped: hooks at 12 sites (drivers galaxy_group, cluster, datacube, multi_dataset, interferometer standard; runtime scripts imaging delaunay/delaunay_nn/rectangular, interferometer/mge, weak, both point-source solved); `harness.run_gradient`; 19 `gradient_breakdown.py` wrappers (plus the 6a mge pilot); `scripts/misc/campaigns/gradient_p6.py` — 74 legs (46 JAX optimal, 25 JAX CPU secondary of numba-optimal, 3 held datacube A100) in 14 submits on 2026.10.25.1, every WALL-BASIS row unmeasured/probe-first at 4x the phase-2 runtime wall (>= 1200 s), check_submits OK; nothing submitted.
- Next: 6c — run the 14 submits with the human's go from a RAL-capable session (this cloud session cannot reach RAL); 6d — ingest gradient.json into results/, coverage + day-zero pages, hazards (>4x or FD fail) through intake, and a separate frozen Pulse label for stamped gradients (the day_zero snapshot is never rewritten).

## Original prompt

# Likelihood lifecycle phase 6b: gradient_breakdown.py for every likelihood + gradient_p6 campaign generator

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
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/507
Consequence: judge
Witness: every gradient cell (JAX Optimal + JAX CPU secondary of numba-optimal cells + held datacube A100) maps to a gradient_breakdown.py that runs its runtime construction with --gradient; gradient_p6.py writes batch-0/batch-1 submits that pass check_submits; CI smoke-imports every gradient_breakdown.py; no runtime row changes without --gradient
Review-minutes: 30
Unattended: never
Epic: likelihood-lifecycle
Phase: 6
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-11-01

## Request (human, 2026-11-01, verbatim)

"Prm make gradients also day zeros and the do 6b"

## Human rulings (AskUserQuestion, 2026-11-01)

- Heart RED: "Override + create issue" (development only; merge via /prm).
- Design: a `--gradient` hook at each fused-likelihood construction site (shared drivers + self-contained runtime scripts); each gradient_breakdown.py is a thin wrapper running its runtime script with --gradient.
- Gradients run fp64 on the 2026.10.25.1 environment so they can carry the day-zero stamp (ruling on #506).

## Branch

Same session branch as #506: built and committed locally, pushed as its own PR after #506 merges.
