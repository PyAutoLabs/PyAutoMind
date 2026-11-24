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

Issued: 2026-11-24
Issue: https://github.com/PyAutoLabs/autofit_profiling/issues/26

## Gaussian-profile pairs

Both reversed-order pairs completed. The doubled interval shortened full fits by 34.7% and 25.5%, with 1,800 extra likelihood evaluations in each. First near-peak calls moved from 4,278 to 6,020 and from 4,043 to 5,608. Both pairs passed evidence and folded-posterior checks and exceeded the registered discovery limit. The two-mode controls are in progress.

## Completed comparison

[Draft profiling PR #27](https://github.com/PyAutoLabs/autofit_profiling/pull/27) reports eight local CPU fits in four counterbalanced pairs. Doubling the native interval from 200 to 400 shortened the full Gaussian-profile fits by 34.7% and 25.5% and the symmetric two-mode fits by 31.2% and 32.4%. Bound builds fell from 25–28 to 18–19. The candidate required 1,600–1,800 additional likelihood evaluations per fit.

All eight log-evidence errors were below 0.058 against quadrature (reference −57.45410). Both signs were recovered in every symmetric fit, with positive-mode mass 0.490–0.520. All folded posterior checks passed. Three of four pairs exceeded the 25% allowance on evaluations to a peak. Keep the native default. Transfer to lensing remains unmeasured. For the single-mode pairs, 7.6–11.7 ms of additional work per serial evaluation would absorb the observed time saving if sampling paths and other costs stayed fixed.

[Paired timings and reproduction](https://github.com/PyAutoLabs/autofit_profiling/blob/bfb33b7f4a2792bf467b16de640a58afe70e1e8c/experiments/nautilus_bound_cadence/README.md). All 111 tooling tests, Ruff and the Pulse catalogue check passed. The scoped Heart verdict was green with this producer deferred to PR checks. The draft PR awaits human review. Wider phase 0b and its 30D evidence gate remain open. Pulse promotion remains deferred.
