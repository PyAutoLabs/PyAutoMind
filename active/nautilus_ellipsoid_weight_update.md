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
