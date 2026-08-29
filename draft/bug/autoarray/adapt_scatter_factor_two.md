# NOTE: legacy `Adapt` scatters every edge twice — it is 2× `Constant`, not equal to it

Type: bug
Target: autoarray
Repos:
- @PyAutoArray
Themes:
- pixelization
Difficulty: small
Autonomy: supervised
Priority: low
Status: documented — NOT an open bug (fixed in the `*Power` classes, 2026-08-29)
Filed: 2026-08-29

## What this is

A **note**, not an open task. The asymmetry described below is real, is now
documented in the legacy docstrings, and is **fixed in the new `AdaptPower`
family** shipped by `feature/autoarray/adapt_linear_regularization.md`. The
legacy classes deliberately keep it so that stored identifiers, outputs and
aggregator reloads stay valid.

## The asymmetry

`autoarray/inversion/regularization/adapt.py::weighted_regularization_matrix_from`
scatters **both** ordered directions of every mesh edge:

```python
mat[I, I] += w_ij;  mat[J, J] += w_ij
mat[I, J] -= w_ij;  mat[J, I] -= w_ij
```

Because the neighbor list already contains each unordered edge `{i, j}` twice
(once in row `i`, once in row `j`), each edge lands **four** times. `Constant`
scatters each ordered pair once (`constant.py`: `diag = 1e-8 + c²·n_i`,
`mat[i, neighbors[i]] -= c²`).

Consequence: with uniform weights the legacy `Adapt` matrix is exactly
**twice** the `Constant` matrix of the same coefficient (up to the shared
`1e-8` diagonal floor). Verified on PyAutoArray `main`, 4-connected 3×3 mesh,
`inner = outer = 1`:

```
Adapt diag  [4.00000001 6.00000001 4.00000001 ...]
Const diag  [2.00000001 3.00000001 2.00000001 ...]
ratio       [2. 2. 2. ...]         # off-diagonals too: -2.0 vs -1.0
```

This contradicts the `Adapt` / `AdaptSplit` / `MaternAdaptKernel` docstrings,
which claimed the defaults `inner_coefficient == outer_coefficient == 1.0`
make the scheme "numerically identical to `Constant(coefficient=1.0)`". Those
docstrings were corrected on 2026-08-29.

The **split** family does not carry the asymmetry: `AdaptSplit` and
`ConstantSplit` share `regularization_util.pixel_splitted_regularization_matrix_from`,
so their only difference is the coefficient exponent.

## Why it is not being fixed in place

Changing `weighted_regularization_matrix_from` would halve the effective
regularization of every `Adapt` fit ever run, invalidating stored results and
the coefficient scale of every published/ledgered adaptive run. The corrected
construction lives in
`weighted_regularization_matrix_single_scatter_from` and is used only by the
new `AdaptPower` class, where `AdaptPower(inner=outer=c) == Constant(c)`
exactly (a test asserts it).

## If this ever becomes actionable

It folds into `draft/feature/autoarray/adapt_linear_default_flip.md` — the
deferred breaking decision to make the `*Power` classes the defaults.
