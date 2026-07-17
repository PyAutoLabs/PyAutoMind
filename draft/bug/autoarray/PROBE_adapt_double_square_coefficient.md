# PROBE: is Adapt's 4th-power coefficient dependence (double square) intentional?

Type: bug
Target: autoarray
Repos:
- @PyAutoArray
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft

**This is a review/probe request, not an implementation task — the answer could
be "intentional, document it" or "bug, fix it", and the two have very different
blast radii. Do not change code until the question is answered.**

Found during the reg-logdet investigation (autolens_workspace_developer#104
follow-up); the conditioning consequence was independently confirmed by a second
reviewer.

## The observation

`Adapt`'s regularization coefficient enters the regularization matrix at the
**fourth power**, because it is squared twice:

1. `autoarray/inversion/regularization/adapt.py:45-47`,
   `adapt_regularization_weights_from`:
   ```python
   return (inner_coefficient * pixel_signals
           + outer_coefficient * (1.0 - pixel_signals)) ** 2.0
   ```
2. `autoarray/inversion/regularization/adapt.py:84`,
   `weighted_regularization_matrix_from`:
   ```python
   reg_w = regularization_weights ** 2
   ```

By contrast `Constant` squares its coefficient exactly **once**
(`constant.py:44`, `regularization_coefficient = coefficient * coefficient`).

## Why it might be a bug

- Both schemes carry the **identical** prior
  `LogUniform(1e-6, 1e6)` on their coefficients
  (`autogalaxy_workspace/config/priors/regularization/{adapt,constant}.yaml`).
  A 4th-power vs 2nd-power dependence under identical priors means the priors
  encode very different effective-smoothing distributions — undocumented.
- `adapt_regularization_weights_from`'s own docstring says the weights "define
  the **effective regularization coefficient** of every mesh parameter". If the
  returned weights ARE the effective coefficient, then squaring them again in the
  matrix builder (`adapt.py:84`) is the anomaly — `Constant` treats its
  coefficient as entering the matrix squared once, and consistency would want
  `Adapt` to do the same.
- The measured conditioning consequence (verified on the real functions,
  30x30 4-connected mesh, `inner=outer=c`, `pixel_signals=0.5`): `Adapt` reaches
  a numerically non-positive-definite regularization matrix (Cholesky RAISES /
  JAX NaNs) from `c ~ 1e4`, where `Constant` survives to `c ~ 1e6` on the same
  mesh — a ~100x fragility gap that is entirely explained by the extra square.

## Why it might be intentional

- Adaptive regularization deliberately gives high- and low-signal pixels
  different effective smoothing; the extra nonlinearity in the coefficient may be
  a deliberate modelling choice with literature backing (Nightingale & Dye 2015,
  arXiv:1708.07377; Suyu et al. 2006). Check the papers before assuming.
- The `regularization_weights` are plotted / user-facing; changing what they
  represent is itself a visible change, not a free refactor.

## Questions to answer

1. Reproduce the 4th-power dependence and the ~100x conditioning gap on clean
   main (numbers above are reproducible in seconds on CPU).
2. Is the double square intentional? Trace the git history / any paper reference
   for `adapt.py:47` and `:84`. Does removing one square make `Adapt` reduce to
   `Constant` when `pixel_signals` is uniform (a good consistency check)?
3. If it is a bug: removing the extra square changes the **c-scale of every
   adaptive fit** and the meaning of the existing `LogUniform(1e-6, 1e6)` prior —
   so the fix must come WITH a prior-rescale and is science-visible in inference.
   What migration and parity evidence would be required?
4. If it is intentional: it must be documented (in the docstring and ideally the
   prior config comment), and the reg-logdet conditioning analysis should note
   that `Adapt`'s fragility threshold is `c ~ 1e4`, not `Constant`'s `c ~ 1e6`.

## Context

This surfaced while deciding whether to touch `log_det_regularization_matrix_term`
(the reg-logdet non-finite issue). Its resolution could change the c-scale at
which the conditioning collapse bites, so it is worth settling — but it is an
**independent** question and must not be bundled into the log-det change.
