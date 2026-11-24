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
Status: filed 2026-11-24

## Original request

> contonue

## Overview

The retained-array experiment in [PR #19](https://github.com/PyAutoLabs/autofit_profiling/pull/19) found that minimum-volume ellipsoid fits accounted for over 97% of the outer mixture constructor on the local CPU. A complete native serial sampler fit supplies the missing denominator. This is an off-board local diagnostic.

## Plan

1. Reuse the existing correlated Gaussian and native sampling/stopping configuration for the 10D seed-2 comparison. Keep 400 live points, four neural networks, batch 100, ESS target 10,000, native checkpoints, one numerical thread and serial training.
2. Run fresh processes in control–traced–traced–control order. Time constructor, sampling and posterior materialization as the whole native fit. In the traced fits time complete bound builds, neural training/prediction inside them, and minimum-volume enclosing ellipsoid calls inside the builds. Separate inclusive and exclusive measurements, and report control timing scatter. Compare exact local results across all runs and after reopening each checkpoint. The RAL result used a different stack and fit boundary.
3. Implement the harness and evidence in a new producer directory with no edits to PR #19. Use feature/nautilus-whole-fit-geometry from clean producer main and transfer the same chat's coding claim from #19, preserving that PR, its review status and worktree. Reuse the process supervisor. Limit the pilot to four local children, 180 seconds and 4096 MiB each, 720 seconds in aggregate. Stop on a cap or mismatch, retain partial receipts and report the outcome. Publish the issue, evidence and a draft producer PR. Merge stays human.

Effective level is supervised. Merge mode is human /prm.
