# Within-shell weight concentration at 30D — merged

Merged 2026-11-25 under the human's `/prm`: [autofit_profiling#37](https://github.com/PyAutoLabs/autofit_profiling/pull/37), CI green, head an ancestor of origin/main.

## Delivered

- Fresh likelihood calls per unit ESS: 1.17 / 1.64 / 98.02 at 5D / 10D / 30D (seed 0); 109.73–156.04 for the three independent 30D runs (`experiments/nautilus_shell_efficiency/`).
- The top 1% of draws in each shell carry 94.85–95.61% of squared posterior weight.
- Perfect shell reallocation saves at most 0.0061% of calls; split-half chosen proportions cost 8.48–17.36% more. Keep native shell allocation; within-shell proposal quality is the next candidate.

## Original prompt

# Diagnose the loss of fresh-sample efficiency across dimensions

Type: research
Target: autofit_profiling
Repos:
- autofit_profiling
Epic: nautilus-fast-likelihoods
Consequence: judge
Autonomy: supervised
Lane: local-dev

## Original request

> continue

## Phase 0b plan

Measure fresh likelihood calls per effective sample on the completed direct 5D, 10D and 30D correlated Gaussian checkpoints. Use the seed-0 saved stream for the dimension comparison, the other seed-0 conditional streams as sensitivity checks and the three independent 30D explorations from PR #35 as distinct cases. Keep exploration calls separate.

For fixed shell volumes and observed within-shell likelihood moments, compare the observed shell allocations against the allocation maximizing predicted Kish ESS for a fixed number of fresh calls. Report the optimistic same-data saving and test the allocation derived from the first half of each shell on its second half. Reconcile native ESS, evidence, counts and shell statistics against the pinned phase receipts before drawing conclusions. Publish compact reproducible sufficient statistics with raw checkpoint hashes, assumptions and limitations. This is local archival research under the [profiling producer task](https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/autofit_profiling_bootstrap.md). Retain native bounds, update cadence and pool safety. No new sampler or domain campaign runs. Deliver a draft PR stacked on #35 and update the epic.

Issued: 2026-11-25
Issue: https://github.com/PyAutoLabs/autofit_profiling/issues/36

## Results

[Draft profiling PR #37](https://github.com/PyAutoLabs/autofit_profiling/pull/37), stacked on #35, accounts for all eight completed direct Gaussian cases in this comparison. The saved seed-0 runs used 1.17, 1.64 and 98.02 fresh likelihood calls per effective sample at 5D, 10D and 30D. At independently learned 30D bounds, seeds 1–3 used 124.85, 109.73 and 156.04 calls per ESS. The highest-weight 1% of fresh draws within each shell contributed 94.85–95.61% of the total squared posterior weight on those independent seeds.

With measured shell volumes and moments held fixed, the optimal continuous allocation could reduce calls by at most 0.0061% across all six 30D cases. Allocation chosen from the early half of each shell predicted 8.48–17.36% more calls on later rows. The latter is a fixed-volume sensitivity check. Both findings are local to the archived fixture. Native shell allocation stays in place. A candidate for the next bounded diagnostic is whether pre-likelihood geometry indicators predict where the high weights occur within a shell on held-out draws, before proposing an algorithm change.

Eight native ESS, evidence and count receipts reconciled; independent raw-row calculations reproduced the weighting and allocation results. All 111 tooling tests, Ruff and catalogue validation passed. Scoped Heart dev-ship readiness was green. [Full diagnostic, model assumptions and per-case numbers](https://github.com/PyAutoLabs/autofit_profiling/blob/540497fdb77e2987c63e36f7d26eb6890f5ec3f4/experiments/nautilus_shell_efficiency/README.md). Wider phase 0b remains open and Pulse promotion stays deferred.
