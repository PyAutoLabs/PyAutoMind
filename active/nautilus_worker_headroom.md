# Bound the whole-fit gain available from scheduling two CPU workers

Type: research
Target: autofit_profiling
Repos:
- autofit_profiling
Epic: nautilus-fast-likelihoods
Consequence: judge
Autonomy: supervised
Lane: local-dev

## Original request

> ok keep the native default and continue to the next task in the Nautilus epic, its good we are mapping out possible speed ups

## Approved scope

Keep native bound cadence. Reuse every included two-worker traced case in the merged phase 0a manifest, covering direct Nautilus and PyAutoFit under fixed, parameter-correlated and random synthetic cost. Verify each compressed trace hash and reconcile all batch members. Pin the archive identity and report missing cases. Reuse the canonical [Pulse producer task](https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/autofit_profiling_bootstrap.md). This local offline analysis is groundwork for worker utilisation. Wider 0b and its dimension diagnostics remain open.

For each intact logical batch compare the observed submit-to-collection interval with a perfect two-worker lower bound, holding per-proposal service times fixed. Quantify idle capacity, the largest possible wall saving as a fraction of complete traced fit wall and the ceiling from eliminating the whole map. Model native contiguous chunks and one-proposal chunks under the same ordered queue and zero scheduling overhead. Keep serial parent work and the final batch barrier intact. Treat simulated changes as predictions. Use both the committed examples and the full retained archive. If even the optimistic scheduling ceiling stays below 5% of full fit wall in every measured case, deprioritise changing the production scheduler for this regime. Otherwise identify which fixture justifies an actual paired run. Publish the replay and measurements in a draft PR and update the epic.

Issued: 2026-11-24
Issue: https://github.com/PyAutoLabs/autofit_profiling/issues/28

## Result

[Draft profiling PR #29](https://github.com/PyAutoLabs/autofit_profiling/pull/29) replays all 14 selected two-worker phase 0a traces with fixed, correlated and random costs. All 35,600 proposals in 356 complete batches matched the native counts and archived service totals. Although workers were occupied for 29.7–72.6% of the map intervals, those intervals used only 0.65–1.44% of traced full-fit wall. With measured service times fixed, an ideal scheduler with free dispatch and collection could recover at most 0.39–0.51% of full wall across the cases. Zero-overhead simulation of single-proposal chunks predicts 0.003–0.033% savings over native chunks of 13.

Deprioritise scheduler changes on this cheap 5D fixture. All cases fall below the 5% gate. A costlier target needs its own measured map share before reopening this lead. This archival analysis does not advance asynchronous adaptation or complete phase 2. Keep native cadence. The next unresolved correctness gate is phase 0b's 30D fresh-sample evidence check. Pulse promotion remains deferred. [Replay, decision and per-fit evidence](https://github.com/PyAutoLabs/autofit_profiling/blob/0a34a82f998f46ce4322f449edc27378dd59a325/experiments/nautilus_worker_headroom/README.md). All 111 tooling tests, Ruff and the catalogue validator passed. The PR awaits human review.
