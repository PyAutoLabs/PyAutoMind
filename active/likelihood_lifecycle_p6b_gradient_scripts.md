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
