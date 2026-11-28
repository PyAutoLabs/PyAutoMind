# Scalar vs native ellipsoid update in complete fits — merged

Merged 2026-11-25 under the human's `/prm`: [autofit_profiling#25](https://github.com/PyAutoLabs/autofit_profiling/pull/25), CI green, head an ancestor of origin/main.

## Delivered

- Four supervised complete fits compared the scalar weight-update candidate with native (`experiments/nautilus_weight_whole_fit/`).
- Timing was inconclusive under the pre-registered rule: 4.1% slower in native–candidate order, 15.2% faster in candidate–native order. The candidate stays experimental.
- All four fits matched the native posterior, log evidence, ESS, shell and evaluation counts; all 101 ellipsoid call shapes matched.

## Original prompt

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

## Result — 2026-11-24

[Draft producer PR #25](https://github.com/PyAutoLabs/autofit_profiling/pull/25) is stacked on #23. The candidate took 43.17 s against 41.48 s native in the first pair (4.1% slower) and 38.22 s against 45.08 s native in the reverse pair (15.2% faster). The registered pair-direction rule gives an inconclusive end-to-end timing result. Keep the scalar update experimental. All four cases matched the frozen native ordered posterior, log evidence, ESS, 12 shells and 23,500 likelihood calls, including on unmodified native checkpoint reopening. Every case made 101 solver calls with matching input shapes in order.

Four local fits completed within 174.7 s and the declared caps, with no failures or unrun cases. Implementation `b601d24`, report `b10c0b1`. All 111 tooling tests passed, Ruff and catalogue validation passed, and the scoped Heart development gate was green. [Measured pairs and validation](https://github.com/PyAutoLabs/autofit_profiling/blob/b10c0b142adeaf486109b30fe1052aabc6d0c898/experiments/nautilus_weight_whole_fit/README.md). Before pursuing a production change, a quieter paired multi-seed comparison would need to resolve total-fit and kernel time together. Link the owning domain task before executing a campaign. Wider phase 0b and the 30D evidence gate remain open. No new campaign was submitted.
