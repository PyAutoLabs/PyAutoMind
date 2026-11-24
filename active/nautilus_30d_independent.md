# Test 30D evidence across independently learned Nautilus bounds

Type: research
Target: autofit_profiling
Repos:
- autofit_profiling
Epic: nautilus-fast-likelihoods
Consequence: judge
Autonomy: supervised
Lane: local-dev

## Original request

> ok continue phase 0b with independent 30D exploration seeds and see if the evidence still comes out low with separately learned bounds

## Plan

Start three fresh direct Nautilus 1.0.5 runs, exploration seeds 1, 2 and 3. Use the same pinned analytic 30D Gaussian, prior, four neural networks, native update cadence of 400, 400 live points, batch 100, f_live 0.01 and single-thread libraries as PR #31. Each starts with no checkpoint or learned bounds. Record exploration-inclusive evidence and an exploration-boundary witness, then sample only fresh points with each run's own continuing RNG. Require ESS ≥10,000 and ≥100 fresh points per shell. Pin and compare the learned outer ellipsoid centres and shapes across all three runs and the historical seed-0 checkpoint. Confirm each run preserves its own geometry through fresh sampling. Reopen each final native checkpoint and reconstruct evidence and ESS independently from stored likelihoods and shell volumes.

Report the signed log-evidence and relative evidence errors against the analytic answer for every seed, their descriptive spread, calls, moments and all failures. Judge whether the sign persists across the new explorations. Keep the conditional seed-0 repeats separate. No post hoc acceptance band, calibrated uncertainty claim or timing comparison. Local accuracy experiment, three concurrent single-process children at most, 2,400 seconds and 4 GiB sampled RSS per child; no retries or cluster compute. Link [the canonical profiling task](https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/autofit_profiling_bootstrap.md) and [conditional predecessor](https://github.com/PyAutoLabs/autofit_profiling/pull/31). Publish a stacked draft PR, update the implementation epic, leave merge to the human.

Issued: 2026-11-24
Issue: https://github.com/PyAutoLabs/autofit_profiling/issues/32

## Exploration completed

All three runs began empty. Their learned outer ellipsoid fingerprints differ from each other and from the historical seed-0 checkpoint. At the native exploration cutoff the signed log-evidence errors for seeds 1, 2 and 3 were −0.8924, −0.9557 and −0.8886. Fresh-only sampling is in progress for the registered endpoint.
