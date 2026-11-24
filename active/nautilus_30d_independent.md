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

## Bounded attempt results

[Draft profiling PR #33](https://github.com/PyAutoLabs/autofit_profiling/pull/33), stacked on #31, started three native 30D samplers in empty directories. All three learned distinct ellipsoid geometries, also distinct from seed 0. At the exploration boundary the signed log-evidence errors were −0.892372, −0.955682 and −0.888639. Each independently learned exploration substantially underestimated the analytic evidence at that point.

All three children hit their registered 2,400-second limit before fresh-only ESS 10,000. The terminal files were intact. Seed 1 was 0.42% above analytic evidence (ESS 8,147; 1,074,100 fresh samples), seed 2 was 1.76% below (ESS 9,904; 1,090,100 fresh samples), and seed 3 was 0.35% below (ESS 6,920; 936,500 fresh samples). All three terminal estimates agreed between direct HDF5 reconstruction and native reopening, with source hashes preserved. The sign is mixed at the observed sample sizes. The matched-ESS comparison remains open. [Per-seed report, receipts and checkpoint audit](https://github.com/PyAutoLabs/autofit_profiling/blob/06c9c887a9d487f8325d25554d780f856f5b4049/experiments/nautilus_30d_independent/README.md).

All 111 tooling tests, Ruff and the catalogue validator passed. The bounded attempt awaits draft-PR review. Retain all three raw checkpoints for a separately scoped continuation. Native bound cadence, wider phase 0b and deferred Pulse promotion remain as recorded.
