# `AdaptPower` regularization: coefficient exponent as an input, factor-2 scatter fixed

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
Issued: 2026-08-29

## Original request (verbatim)

> do the 5 things above listed and make sure we have some SMC runs going soon

(Rung 2 of the overflow-flood fix wave — see the approved plan "Overflow-flood
fix wave + SMC on the A100", task A3, as amended 2026-08-29 by the human:
"maximal changes, power as an input".)

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

A second, independent asymmetry sits in the same builder: the non-split
`Adapt` matrix scatters every edge **twice** (both `(i,j)` and `(j,i)` from
each direction), so `Adapt(inner=outer=c)` is exactly `2 ×` `Constant(c)`,
contradicting its own docstring's "numerically identical to
`Constant(coefficient=1.0)`". Verified on main:
`Adapt` diag `4.00000001` vs `Constant` diag `2.00000001` on a 4-connected
3×3 mesh, ratio 2.0 on every entry. The split family does **not** carry this
(it shares `pixel_splitted_regularization_matrix_from` with `ConstantSplit`).

## Human decisions (binding)

- The existing `Adapt`, `AdaptSplit`, `AdaptSplitZeroth`, `MaternAdaptKernel`
  classes and their util functions stay **byte-for-byte**: identifiers, stored
  outputs and aggregator reloads remain valid.
- Corrected **siblings** are added instead: `AdaptPower`, `AdaptSplitPower`,
  `AdaptSplitZerothPower`, `MaternAdaptPowerKernel`. Distinct class paths give
  distinct `af.Model` identifiers for free.
- The new classes take **`power: float = 1.0`** as a constructor argument. The
  effective coefficient exponent is `2 · power`, so the default `power=1.0`
  gives the λ² convention shared with `Constant`, and `power=2.0` reproduces
  the legacy λ⁴ classes exactly. `power` is declared
  `type: Constant, value: 1.0` in the prior yamls so `af.Model` never samples
  it.
- The new classes **also fix the factor-2 scatter**: a new single-scatter
  matrix builder beside `weighted_regularization_matrix_from` (numpy + JAX)
  makes `AdaptPower(inner=outer=c)` equal `Constant(c)` exactly, and
  `AdaptSplitPower(inner=outer=c)` equal `ConstantSplit(c)` exactly.
- Making the power classes the default is a separate, deferred, breaking
  decision — filed as `draft/feature/autoarray/adapt_linear_default_flip.md`.

## Scope

- `adapt.py`: `adapt_regularization_weights_from(..., power=2.0)` gains a
  `power` keyword; default 2.0 keeps the existing numerics untouched. New
  `weighted_regularization_matrix_single_scatter_from` beside it (weighted
  graph Laplacian with edge weight `0.5·(w_i² + w_j²)` — PSD, symmetric,
  reduces to `Constant` exactly for uniform weights).
- New modules `adapt_power.py`, `adapt_split_power.py`,
  `adapt_split_zeroth_power.py`, `matern_adapt_power_kernel.py`.
- Exports through `autoarray/inversion/regularization/__init__.py` → `aa.reg`
  → `ag.reg` / `al.reg`.
- PyAutoGalaxy prior yamls (copies of the existing ones plus the constant
  `power`) + the PyAutoLens test config mirror.
- Tests: `AdaptPower(inner=outer=c) == Constant(c)`,
  `AdaptSplitPower(inner=outer=c) == ConstantSplit(c)`,
  `power=2.0` reproduces the legacy classes, weights are unsquared at
  `power=1.0`, numpy/JAX parity for both builders, `af.Model` identifier
  divergence, one composition test each in PyAutoGalaxy and PyAutoLens.
- Docs: docstrings on both old and new classes, `docs/api/pixelization.rst`
  autosummary entries in PyAutoGalaxy and PyAutoLens.

## Migration

`c_new = c_old ** 2` — an `AdaptPower` coefficient of `c` reproduces a legacy
`Adapt` coefficient of `sqrt(c)` (up to the factor-2 scatter, which the new
class also removes; `AdaptPower(power=2.0)` is the byte-exact legacy path).
