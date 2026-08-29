## fitness-log-likelihood-ceiling
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1543
- completed: 2026-08-29
- library-pr: PyAutoFit#1545 (merged f71b91efe -> main)
- what shipped: `Fitness.call` third `xp.where` — finite |log_likelihood| above `general.test.log_likelihood_ceiling` (default 1e20; null/inf disables; read once in `__init__` as a static float, PyYAML "1e20"-string trap coerced) maps to `resample_figure_of_merit`; inside the jit/vmap region so numpy, `_jit`, `_vmap`, Nautilus n_batch and BlackJAXNUTS inherit it; `__setstate__` backfill for pre-change pickles. NSS closure lifted to module-level `nss_log_likelihood_from(model, analysis, log_likelihood_ceiling)` sharing the ceiling (`NSS_INVALID_LOG_LIKELIHOOD` sentinel). Packaged + test config mirrored.
- why: RAL 341908_5 (`slam_source_pix_nn`) accepted finite log_l up to 3e+303 from a non-PD Adapt regularization matrix — Nautilus poisoned, never terminated (see autolens_profiling issue #194 follow-ups).
- validation: 2337 passed / 3 skipped; new tests numpy (both signs, sentinel idempotence, config parsing) + jax jit/vmap (values inside float32 range so the magnitude guard, not isinf, fires) + NSS factory; CI 4/4 (3.12, 3.13, nojax, docs).
- heart-ack: shipped + merged under human-authorised YELLOW ("merge", 2026-08-29) — "workspace validation not passing (0 failed, 1 timeout, cloud#33229145647: autolens_test scripts/multi_dataset/delaunay_mge.py)"; "release validation incomplete: no rehearsal for current source". Unrelated to this change.
- skipped: /smoke_test (no workspace impact — ceiling ~15 orders above any real likelihood); workspace general.yaml files not given the key (KeyError → 1e20 default) — follow-up if the knob should be visible.

## Original prompt

# Fitness: reject implausibly large finite log-likelihoods

Type: bug
Target: PyAutoFit
Autonomy: human-required
Issued: 2026-08-29

## Problem

RAL pilot `341908_5` (`slam_source_pix_nn`, free `AdaptSplit` on `DelaunayNN`) was
ledgered as "0 Nautilus calls in 6 h / thrashes". The checkpoint shows it actually
made 90,000 calls, reached maxL 30,701 and was killed by a **likelihood-overflow
flood**: `Adapt*` regularization squares the coefficient twice (λ⁴), the
regularization matrix goes non-PD from c≈1e4 under `LogUniform(1e-6, 1e6)`, the
fp64 Cholesky returns *finite garbage* (log_l up to 3e+303), and PyAutoFit's
`Fitness` passes any finite value straight through. Nautilus accepted it as the
best point → `shell_log_l ≈ 1e56`, `f_live` never terminated.

`Fitness.call` guards NaN and inf, but nothing guards a finite value that is
physically impossible. A magnitude ceiling closes that hole for every search that
goes through `Fitness.call` (numpy, `_jit`, `_vmap`, Nautilus `n_batch`,
BlackJAXNUTS), and the same ceiling has to be applied in `af.NSS`, which bypasses
`Fitness.call` with its own inline JAX closure.

## Scope

- `autofit/non_linear/fitness.py` — a third `xp.where` after the isnan/isinf
  wheres mapping `|log_likelihood| > ceiling` to `resample_figure_of_merit`.
  Ceiling is a **static Python float** read once in `__init__` from
  `conf.instance["general"]["test"]["log_likelihood_ceiling"]` (default `1e20`;
  `null` / `inf` disables). Mirrored into the packaged `autofit/config/general.yaml`.
- `autofit/non_linear/search/nest/nss/search.py` — same ceiling in the NSS inline
  closure.
- Tests: `test_autofit/non_linear/test_fitness_assertions.py` (numpy + jax jit +
  vmap paths) and one NSS closure test.
- Docs: the gradient caveat paragraph in `fitness.py` notes the guard is
  value-only.
- Release notes: bug-fix entry (not breaking).

## Original request

> do the 5 things above listed and make sure we have some SMC runs going soon

(This is rung 1 of that five-rung wave: the PyAutoFit `Fitness` magnitude guard.)
