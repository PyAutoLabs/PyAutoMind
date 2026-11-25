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
