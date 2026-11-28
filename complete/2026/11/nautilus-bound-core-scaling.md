# Whole-fit CPU scaling during native Nautilus bound training — merged

Merged 2026-11-25 under the human's `/prm`: [autofit_profiling#41](https://github.com/PyAutoLabs/autofit_profiling/pull/41), CI green, head an ancestor of origin/main.

## Delivered

- Eighteen complete PyAutoFit fits compared native serial ensemble training with two and four in-process training workers (`experiments/nautilus_bound_core_scaling/`).
- All 12 threaded comparisons were slower: median increases 39% / 80% (Gaussian profile) and 41% / 105% (two-mode control) for 2 / 4 workers.
- Keep native serial training. Magnitudes are host-specific (shared WSL laptop, fixed core affinity).

## Original prompt

# Does parallel native ensemble training shorten complete Nautilus fits?

Type: research
Target: @autofit_profiling
Repos:
- autofit_profiling
Epic: nautilus-fast-likelihoods
Consequence: judge
Lane: local-dev

## Original request

> ok continue with the CPU bound construction test and see if using more cores speeds up the whole fit. Keep the native sampler settings.

## Approved experiment

Use the baseline arm of [the application-fit protocol](https://github.com/PyAutoLabs/autofit_profiling/pull/27), with the same Gaussian profile and two-mode signed-centre control, output, checkpointing, likelihood dispatch, neural ensemble, bound cadence and stopping settings. The earlier [spawn-based pool experiment](https://github.com/PyAutoLabs/autofit_profiling/issues/16) had unstable timings. Test ordered in-process threads at the existing optional neural training map only. Compare native serial to two and four training workers using the same four physical cores, one native math thread per worker, fixed PyAutoFit/PyAutoNerves revisions and fresh output directories. Keep proposed-point and likelihood hashes, native settings, calls, bounds, posterior and evidence equal for each seed.

Run sequentially with rotated arm order for seeds 1–3 in both fixtures. Include executor setup, dispatch and teardown in complete fit wall. Measure neural training, remaining bound geometry, concurrent training CPU and rest of fit. Report each paired ratio, medians by fixture, and numerical parity. Treat a worker count as a promising follow-up only if its median whole-fit improvement is at least 5% on both fixtures, every matched fit improves, and parity holds. Record negative or mixed results. Use the existing [Pulse producer task](https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/autofit_profiling_bootstrap.md). Local experiment only. Update the epic and open a draft PR for human review.

Issue: https://github.com/PyAutoLabs/autofit_profiling/issues/40

## Outcome

[Draft profiling PR #41](https://github.com/PyAutoLabs/autofit_profiling/pull/41) awaits human review. Both threaded arms were slower on every paired whole fit. Retain native serial training. [Timings and parity checks](https://github.com/PyAutoLabs/autofit_profiling/blob/27da441f6c5416c981858e70b5f9bfde62a8a637/experiments/nautilus_bound_core_scaling/README.md).
