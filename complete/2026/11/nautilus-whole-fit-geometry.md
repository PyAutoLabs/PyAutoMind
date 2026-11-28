# Ellipsoid fitting inside complete native Nautilus fits — merged

Merged 2026-11-25 under the human's `/prm`: [autofit_profiling#21](https://github.com/PyAutoLabs/autofit_profiling/pull/21), CI green, head an ancestor of origin/main.

## Delivered

- Timed the minimum-volume enclosing ellipsoid routine inside four complete native Nautilus fits (`experiments/nautilus_whole_fit_geometry/`).
- Both traced runs made 101 calls across eleven bound builds; the routine took 7.88 of 42.34 s and 7.37 of 38.63 s (18.6% and 19.1% of whole-fit time).
- All four fits matched calls, posterior hash, ESS, evidence and shell count; checkpoints reopened identically. Local timing, one seed, one target.

## Original prompt

# Measure ellipsoid fitting inside a complete native Nautilus fit

Type: research
Target: autofit_profiling
Repos:
- autofit_profiling
Epic: nautilus-fast-likelihoods
Phase: experimental 0b whole-fit geometry attribution
Difficulty: medium
Autonomy: supervised
Consequence: judge
Witness: Two complete traced fits match two same-seed controls on ordered posterior arrays, calls, ESS, evidence, shells, and reopened checkpoints. Report enclosing-ellipsoid time inside native bound builds divided by complete fit time, with tracing overhead and independent-seed limitations visible.
Lane: local-dev
Issued: 2026-11-24
Issue: https://github.com/PyAutoLabs/autofit_profiling/issues/20
Status: Pilot complete; draft PR #21 awaiting human review.

## Original request

> contonue

## Overview

The retained-array experiment in [PR #19](https://github.com/PyAutoLabs/autofit_profiling/pull/19) found that minimum-volume ellipsoid fits accounted for over 97% of the outer mixture constructor on the local CPU. A complete native serial sampler fit supplies the missing denominator. This is an off-board local diagnostic.

## Plan

1. Reuse the existing correlated Gaussian and native sampling/stopping configuration for the 10D seed-2 comparison. Keep 400 live points, four neural networks, batch 100, ESS target 10,000, native checkpoints, one numerical thread and serial training.
2. Run fresh processes in control–traced–traced–control order. Time constructor, sampling and posterior materialization as the whole native fit. In the traced fits time complete bound builds, neural training/prediction inside them, and minimum-volume enclosing ellipsoid calls inside the builds. Separate inclusive and exclusive measurements, and report control timing scatter. Compare exact local results across all runs and after reopening each checkpoint. The RAL result used a different stack and fit boundary.
3. Implement the harness and evidence in a new producer directory with no edits to PR #19. Use feature/nautilus-whole-fit-geometry from clean producer main and transfer the same chat's coding claim from #19, preserving that PR, its review status and worktree. Reuse the process supervisor. Limit the pilot to four local children, 180 seconds and 4096 MiB each, 720 seconds in aggregate. Stop on a cap or mismatch, retain partial receipts and report the outcome. Publish the issue, evidence and a draft producer PR. Merge stays human.

Effective level is supervised. Merge mode is human /prm.

## Result — 2026-11-24

[Draft PR #21](https://github.com/PyAutoLabs/autofit_profiling/pull/21) measures native minimum-volume ellipsoid fitting inside the complete 10D, seed-2 fit. The counter recorded 101 calls across eleven bound builds. Ellipsoid fitting took 7.88 / 42.34 s and 7.37 / 38.63 s (18.6% / 19.1% of the traced whole fits). Controls took 40.43 and 39.94 s. Each fit and its reopened checkpoint matched exactly on posterior, evidence, ESS and calls. All 23,500 evaluations were accounted for. The ordered posterior hash also matches the RAL reference. These are native-fit timings on one local CPU fixture. The 97% measured in PR #19 used only the outer mixture constructor as its denominator.

The four authorized local children finished in 166.6 s with no failures or unrun cases. The measured script is at `44c5325` and the report head is `d8709a7`. The 111 tooling tests, Ruff and the Pulse catalogue validator passed. The scoped Heart gate was green. Both PRs await human review. The next bounded CPU experiment can test a numerically equivalent change within the enclosing-ellipsoid routine on retained inputs before seeking a whole-fit speedup. Wider phase 0b and the 30D accuracy gate remain open. [Results and replay instructions](https://github.com/PyAutoLabs/autofit_profiling/blob/d8709a7d536a61f278a311b67ac99ea66f61702f/experiments/nautilus_whole_fit_geometry/README.md).
