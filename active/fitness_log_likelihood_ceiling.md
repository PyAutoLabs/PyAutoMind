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
