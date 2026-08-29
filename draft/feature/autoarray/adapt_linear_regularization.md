# `*Linear` Adapt regularization: squared-once sibling classes

Type: feature
Target: autoarray
Repos:
- @PyAutoArray
- @PyAutoGalaxy
- @PyAutoLens
Themes:
- pixelization
- inference
Difficulty: medium
Autonomy: supervised
Priority: high
Status: draft
Filed: 2026-08-29

## Original request (verbatim)

> do the 5 things above listed and make sure we have some SMC runs going soon

(Rung 2 of the overflow-flood fix wave — see the approved plan "Overflow-flood
fix wave + SMC on the A100", task A3.)

## Why

The `Adapt` family squares its coefficient **twice**, so the regularization
matrix scales as λ⁴:

1. `autoarray/inversion/regularization/adapt.py:45-47` —
   `adapt_regularization_weights_from` returns `(...)**2.0`;
2. `adapt.py:84` (and `regularization_util.py:257` / `:334` for the split
   family) squares the weights again.

`Constant` squares exactly once (`constant.py:44`). Both families carry the
identical `LogUniform(1e-6, 1e6)` prior, so under the same prior `Adapt`
explores a *fourth-power* smoothing range. Measured consequence (RAL pilot
341908_5, `slam_source_pix_nn`): the regularization matrix goes numerically
non-positive-definite from `c ≈ 1e4` (vs `c ≈ 1e6` for `Constant`), fp64
Cholesky returns finite garbage, and Nautilus accepted `log_l` up to 3e+303 —
a likelihood-overflow flood that made a 6-hour GPU run never terminate.

## Human decisions (binding)

- The existing `Adapt`, `AdaptSplit`, `AdaptSplitZeroth`, `MaternAdaptKernel`
  classes stay **byte-for-byte**: identifiers, stored outputs and aggregator
  reloads remain valid.
- Corrected **siblings** are added instead: `AdaptLinear`, `AdaptSplitLinear`,
  `AdaptSplitZerothLinear`, `MaternAdaptLinearKernel`. Distinct class paths give
  distinct `af.Model` identifiers for free.
- The **factor-2 scatter asymmetry** (`Adapt(inner=outer=c)` is exactly 2×
  `Constant(c)`, not equal to it) is **documented only** — filed separately as
  `draft/bug/autoarray/adapt_scatter_factor_two.md`.
- Making the linear classes the default is a separate, deferred, breaking
  decision — filed as `draft/feature/autoarray/adapt_linear_default_flip.md`.

## Scope

- `adapt.py`: `adapt_regularization_weights_from(..., power=2.0)` gains a
  `power` keyword; default 2.0 keeps the existing numerics untouched.
- New modules `adapt_linear.py`, `adapt_split_linear.py`,
  `adapt_split_zeroth_linear.py`, `matern_adapt_linear_kernel.py`, each a thin
  subclass overriding only `regularization_weights_from` to pass `power=1.0`.
- Exports through `autoarray/inversion/regularization/__init__.py` → `aa.reg`
  → `ag.reg` / `al.reg`.
- PyAutoGalaxy prior yamls (copies of the existing ones) + the PyAutoLens test
  config mirror.
- Tests: parity (`Linear(c)` == legacy(`sqrt(c)`)), unsquared weights,
  numpy/JAX parity for the split path, `af.Model` identifier divergence,
  one composition test each in PyAutoGalaxy and PyAutoLens.
- Docs: docstrings on both old and new classes, `docs/api/pixelization.rst`
  autosummary entries in PyAutoGalaxy and PyAutoLens.

## Migration

`c_new = c_old ** 2` — an `AdaptLinear` coefficient of `c` reproduces a legacy
`Adapt` coefficient of `sqrt(c)` exactly.
