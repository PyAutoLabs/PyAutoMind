# Measure the scalar ellipsoid update in complete native fits

Type: research
Target: autofit_profiling
Repos:
- autofit_profiling
Epic: nautilus-fast-likelihoods
Phase: experimental phase 1 whole-fit ablation
Difficulty: medium
Autonomy: supervised
Consequence: judge
Witness: Compare two counterbalanced local native/candidate fit pairs on the frozen 10D seed-2 fixture. Require exact ordered posterior, evidence, ESS, calls, shells and native checkpoint reopening for each case. Show every time, pair direction and failed or missing case.
Lane: local-dev
Issued: 2026-11-24
Issue: https://github.com/PyAutoLabs/autofit_profiling/issues/24

## Original request

> ok continue

## Plan

[PR #23](https://github.com/PyAutoLabs/autofit_profiling/pull/23) measured a 14.4% median reduction in outer-bound reconstruction time. Test its exact candidate on the [PR #21](https://github.com/PyAutoLabs/autofit_profiling/pull/21) whole-fit fixture. Only the native solver's weight update changes.

1. Create a new producer branch stacked on #23. Preserve the three existing review PRs and transfer this chat's coding claim. Reuse the pinned candidate loader and pinned #21 control-mode fit routine. Verify both source identities before sampling.
2. Run native, candidate, candidate and native as fresh local processes at one native thread, seed 2, dimension 10, 400 live points, four neural networks, native checkpoints, batch 100 and target ESS 10,000. Count solver invocations symmetrically. Use the same pinned local libraries and constructor-through-posterior timing boundary as #21. Retain the four checkpoints and verify them with unmodified native code.
3. Use 180 seconds and 4096 MiB per child, and 720 seconds aggregate. Stop on the first failure, cap or parity mismatch. Compare each case against the frozen native result. Report both ordered pair effects; opposite signs mean inconclusive. A two-pair, one-seed observation cannot establish a production default.
4. Publish the harness and compact receipt through a draft profiling PR and update the epic. Preserve raw results in scratch. The pilot is local and off-board, with production adoption and merge left to human review.

Effective level is supervised. Merge mode is human /prm.
