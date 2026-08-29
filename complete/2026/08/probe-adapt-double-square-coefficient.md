# PROBE answered: `Adapt`'s 4th-power coefficient is real, undocumented, and now has a corrected sibling

**Answered 2026-08-29** while planning the overflow-flood fix wave
(plan "Overflow-flood fix wave + SMC on the A100", task A3;
PyAutoArray issue #511). This record retires the probe — no separate
implementation task remains for the question it asked.

## The four questions, answered

**1. Is the 4th-power dependence real? Reproduced?** Yes. Verified on
PyAutoArray `main`, 4-connected 3×3 mesh, `inner = outer = c`, direct calls to
`weighted_regularization_matrix_from` and `constant_regularization_matrix_from`:

| `c` | `Adapt` `M[0,0]` | `Constant` `M[0,0]` | ratio |
|-----|------------------|---------------------|-------|
| 1.0 | 4.00000001       | 2.00000001          | 2.0   |
| 2.0 | 64.0             | 8.0                 | 8.0   |
| 3.0 | 324.0            | 18.0                | 18.0  |

`Adapt` = `2 · c⁴ · n_i` on the diagonal, `Constant` = `c² · n_i`. The ratio is
`2 c²` — i.e. **two** separate discrepancies, not one.

**2. Is the double square intentional?** No evidence that it is. It is
consistent with the docstring of `adapt_regularization_weights_from` being
correct ("the weights **are** the effective regularization coefficient") and
`adapt.py:84` then squaring them a second time being the anomaly. No paper
reference in the git history motivates a λ⁴ dependence; Nightingale & Dye
(2015) and Suyu et al. (2006) describe adaptive *weights*, not a quartic
coefficient scale. Removing one square does make `Adapt` reduce to `Constant`
under uniform `pixel_signals` — the consistency check the probe proposed —
**once the second discrepancy below is also removed**.

**3. The second, previously unnoticed discrepancy: a factor-2 scatter.**
`weighted_regularization_matrix_from` scatters each mesh edge in **both**
directions (`mat[I,J] -= w` *and* `mat[J,I] -= w` for each ordered pair), and
the neighbour list already contains each unordered edge twice — so every edge
lands four times where `Constant` lands it twice. That is the residual factor
2 in the table above, and it is why the `Adapt` / `AdaptSplit` /
`MaternAdaptKernel` docstrings' claim that the defaults are "numerically
identical to `Constant(coefficient=1.0)`" was false. Those docstrings were
corrected on 2026-08-29. The **split** family does not carry it: `AdaptSplit`
and `ConstantSplit` share
`regularization_util.pixel_splitted_regularization_matrix_from`.

**4. The conditioning consequence is what actually bit.** RAL pilot 341908_5
(`slam_source_pix_nn`, free `AdaptSplit` on `DelaunayNN`) was ledgered as
"0 Nautilus calls in 6 h / thrashes". The checkpoint says otherwise: 90,000
calls, maxL 30,701, killed by a **likelihood-overflow flood**. Under
`LogUniform(1e-6, 1e6)` the λ⁴ scale drives the regularization matrix
non-positive-definite from `c ≈ 1e4` (vs `c ≈ 1e6` for `Constant`); fp64
Cholesky returns finite garbage (`log_l` up to 3e+303), PyAutoFit's `Fitness`
passes any finite value through, Nautilus accepts it as the best point, and
`f_live` never terminates.

## The resolution taken (human decision, 2026-08-29)

Not a fix in place — the c-scale of every adaptive fit ever run would change
silently, invalidating stored results and every ledgered coefficient. Instead:

- Legacy `Adapt`, `AdaptSplit`, `AdaptSplitZeroth`, `MaternAdaptKernel` and
  their util functions stay **byte-for-byte**.
- Corrected siblings ship alongside — `AdaptPower`, `AdaptSplitPower`,
  `AdaptSplitZerothPower`, `MaternAdaptPowerKernel` — each taking
  `power: float = 1.0` (effective coefficient exponent `2 · power`; `power=2.0`
  reproduces the legacy classes exactly), and each using a new single-scatter
  matrix builder so `AdaptPower(inner=outer=c)` equals `Constant(c)` **exactly**
  and `AdaptSplitPower(inner=outer=c)` equals `ConstantSplit(c)` exactly.
- Distinct class paths give distinct `af.Model` identifiers for free, so
  pre- and post-change results cannot silently mix.
- Migration for existing coefficients: `c_new = c_old ** 2`.

## Follow-ups filed

- `draft/bug/autoarray/adapt_scatter_factor_two.md` — the factor-2 scatter,
  recorded as a documented property of the legacy classes, **not** an open bug.
- `draft/feature/autoarray/adapt_linear_default_flip.md` — the deferred,
  breaking decision to make the `*Power` classes the defaults.

Implementation: PyAutoArray issue #511 /
`active/adapt_linear_regularization.md`.

## Original prompt

# PROBE: is Adapt's 4th-power coefficient dependence (double square) intentional?

Type: bug
Target: autoarray
Repos:
- @PyAutoArray
Themes:
- pixelization
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft
Filed: 2026-07-17 (backfilled from git)

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
