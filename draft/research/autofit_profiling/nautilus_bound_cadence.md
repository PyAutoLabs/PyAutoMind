# Compare Nautilus bound-update intervals on complete PyAutoFit fits

Type: research
Target: autofit_profiling
Repos:
- autofit_profiling
Epic: nautilus-fast-likelihoods
Difficulty: medium
Autonomy: supervised
Consequence: judge
Lane: local-dev

## Original request

> ok continue

## Plan and decision

Run a local paired comparison of the native default and `n_update=400` at 200 live points. Keep four neural networks, a single sampler process, output and the same data, priors and stopping settings in both arms. Use the existing 100-pixel gaussian_x1 PyAutoFit application. Add a mode-recovery control with a symmetric signed centre whose absolute value enters the same profile. The two signs have equal mass and the same marginal evidence as the original prior. Use seeds 1 and 2 for each fixture, reverse the arm order across seeds and balance the first arm across fixtures. Eight fresh fits in total. Retain results and failures. Cap a fit at 300 s, with no blind retries of measured cases.

Record complete search.fit wall, actual sampler interval, bound builds, training and geometry time, evaluations, first evaluation reaching within 1 log-likelihood unit of the fixed best fit in each mode, posterior summaries, ESS and evidence. Use the fixed-data maximum and an independent numerical evidence calculation to check both arms. Require each run to reach every expected peak, absolute log evidence error at most 0.5, at least 0.35 and at most 0.65 posterior mass per mode in the symmetric control, and paired folded marginal means within 0.3 baseline posterior standard deviations. Flag a candidate taking over 25% more calls to any peak. Call a pilot win only if all four wall-time pairs improve and all science and discovery gates pass. No default change follows from a two-seed pilot.

Use the existing [Pulse producer task](https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/autofit_profiling_bootstrap.md) and the [epic research decision](https://github.com/PyAutoLabs/PyAutoMind/blob/main/complete/2026/11/nautilus_workload_transfer.md). Local off-board engineering evidence only. Publish the reproducible harness and compact measurements in a draft profiling PR and update Mind. Human review owns merge.
