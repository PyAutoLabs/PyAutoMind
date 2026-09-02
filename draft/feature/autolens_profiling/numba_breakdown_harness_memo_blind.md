# Numba breakdown harness: perturb the instance so the operated-matrix memo cannot hide a step

Type: feature
Target: autolens_profiling
Repos:
- @autolens_profiling
Themes:
- numba-cpu
- profiling
Difficulty: small
Autonomy: safe
Priority: medium
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
Filed: 2026-08-27

## Context (found while measuring PyAutoArray#496, 2026-08-27)

Was a member of the `numba-cpu-likelihood` epic, retired 2026-09-02 to
`complete/archive/epics/numba-cpu-likelihood.md`; it stands alone now.

`scripts/imaging/likelihood_breakdown/pixelization_numba.py` and the
`likelihood_runtime` sibling time `n_repeats=10` evaluations of one fixed
`instance`. Since the cross-evaluation memo in PyAutoArray
`imaging_numba/sparse.py` (sha256 of the pickled linear func), every repeat
after warm-up hits the memo, so "MGE operated mapping matrix (60 funcs)" reads
~0.003 s (euclid) / ~0.01 s (hst) — and `direct_log_likelihood_function_per_call`
is contaminated the same way. Batching the convolution (a 3.7-5.4x win on that
step, measured with `AUTOARRAY_NUMBA_OPERATED_MEMO=0`) showed A/B = 1.04 in the
harness. Real modelling perturbs the MGE parameters every evaluation, so the
memo never hits there.

## Goal

- Per repeat, perturb the instance (e.g. shift the lens-light Gaussian centres
  by 1e-3·k) OR set `AUTOARRAY_NUMBA_OPERATED_MEMO=0` for the numba cells, so
  the step is measured un-memoised; record which in the results JSON
  `configuration`.
- Keep the pinned log-likelihood check on the unperturbed instance.
- Re-baseline the `pixelization_numba` and `delaunay_numba` breakdown/runtime
  results (euclid + hst) and note the regime change in the results README.
