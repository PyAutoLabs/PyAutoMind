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
