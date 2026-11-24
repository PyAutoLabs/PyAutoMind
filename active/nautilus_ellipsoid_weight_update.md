# Test the scalar weight update on retained Nautilus ellipsoid inputs

Type: research
Target: autofit_profiling
Repos:
- autofit_profiling
Epic: nautilus-fast-likelihoods
Phase: experimental phase 1 CPU kernel ablation
Difficulty: medium
Autonomy: supervised
Consequence: judge
Witness: Compare native and candidate calculations on all 57 ellipsoid calls triggered by eleven retained 10D outer bounds, including the lower-dimensional projections. Require identical input and output bytes for corresponding calls and matching reconstructed geometry. Publish every paired timing or the first failure.
Lane: local-dev
Issued: 2026-11-24
Issue: https://github.com/PyAutoLabs/autofit_profiling/issues/22

## Original request

> ok i approve continue

## Plan

[Whole-fit attribution](https://github.com/PyAutoLabs/autofit_profiling/pull/21) measured 18.6–19.1% of native fit wall time inside ellipsoid fitting. Measure one change on the existing [retained-input replay](https://github.com/PyAutoLabs/autofit_profiling/pull/19). After scaling all weights by the original factor, add the original increment only at the selected index. Keep every solver iteration, selected index, covariance calculation and neural bound convention intact.

1. Reuse PR #19's source and input validation on a stacked producer branch. Apply the one-line expression replacement to a temporary experimental copy of the pinned native module.
2. Compare corresponding point arrays and all returned centers and matrices byte-for-byte during preflight. Check the outer geometry, saved masks and exact membership, unchanged inputs and RNG. Stop on mismatch.
3. Run six paired forward/reverse blocks on the eleven inputs with balanced within-pair order, one numerical thread. Collect wall time and process CPU for the outer mixture constructor with the solver uninstrumented. Report all blocks, per-input timings and limitations. This local engineering trial starts no sampler, cluster job or campaign.
4. File the phase issue and draft producer PR, record the result in the epic and preserve the review branches for #19 and #21. Human merge.

Effective level is supervised. Merge mode is human /prm.

## Result — 2026-11-24

[Draft profiling PR #23](https://github.com/PyAutoLabs/autofit_profiling/pull/23), stacked on #19, changes only the solver weight update in an isolated replay. Native and candidate solver inputs and all three returned arrays matched bit-for-bit across 57 corresponding calls from 11 retained outer bounds. Every one of 132 timed outer constructions matched native geometry, membership and RNG state. Across six paired blocks, median wall and process CPU reductions were both 14.4%. Wall reductions ranged from 1.6% to 25.5%, with the smallest gains in the two slowest blocks. All blocks repeat one 10D seed-2 point set per bound on the shared laptop.

Producer implementation `9dfb165`, report `91e9ec1`. The 111 repository tooling tests, Ruff and the Pulse catalogue validator passed. The scoped Heart dev-ship gate was green. [Results and all six timing blocks](https://github.com/PyAutoLabs/autofit_profiling/blob/91e9ec1bec5078374ec7c5ef464c3224d9d4290a/experiments/nautilus_ellipsoid_weight_update/README.md). The next bounded gate is a native-versus-candidate whole-fit comparison on the #21 fixture, with exact posterior, evidence, ESS, call-count and checkpoint-reopen checks. Production adoption, wider phase 0b and the 30D evidence gate remain open.
