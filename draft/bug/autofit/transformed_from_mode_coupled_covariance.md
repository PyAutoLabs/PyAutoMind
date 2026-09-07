# `TransformedMessage.from_mode` diagonalises an operator covariance before a coupled Jacobian

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Themes:
- graphical-ep
Difficulty: small
Autonomy: safe
Priority: medium
Status: formalised
Consequence: glance
Witness: `MultiLogitNormalMessage.from_mode(mode=[0.3, 0.4], covariance=...)` returns the same variances ([1.2222, 1.2431], the delta-method `diag(J Σ Jᵀ)`) for an ndarray, a `MatrixOperator` and a `DiagonalMatrix` input (operator forms currently [2.3611, 2.1875]); `test_autofit/messages` stays green with the new parametrised case; scalar-transform results bit-identical
Review-minutes: 4
Unattended: ready
Epic: graphical-ep
Filed: 2026-09-07

Finding 3 (P2) of the Codex review of the graphical-ep phase-2 fixes (review text verbatim in the
sibling `ep_laplace_deterministic_hessian.md`). Confirmed on `main` (f6a991504) on 2026-09-07.
Not a regression in the strict sense: pre-#1560 the operator path raised `ValueError`; #1560
turned a crash into a silently wrong answer. No live caller reaches it (see Impact), so P2 stands
but is defensive-path only.

## Reproduction (2026-09-07)

`MultiLogitNormalMessage`, mode `[0.3, 0.4]`, Σ = diag(0.02, 0.03), base-message variances:

| covariance input | variance |
|---|---|
| `np.diag([0.02, 0.03])` | [1.2222, 1.2431] |
| `MatrixOperator(np.diag(...))` | [2.3611, 2.1875] |
| `DiagonalMatrix([0.02, 0.03])` | [2.3611, 2.1875] |
| delta method `diag(J Σ Jᵀ)` | [1.2222, 1.2431] |

Mode `[0.2, 0.3]`, Σ = 0.01·I: matrix [0.5300, 0.3244] vs operator [0.7767, 0.5711] — the same
shape as the reviewer's [0.5700, 0.6089] vs [1.0233, 0.8956].

## Mechanism

`autofit/messages/composed_transform.py:446-457`: an operator covariance is reduced to
`covariance.diagonal()` *before* the Jacobian loop; `jac.quad(M)` (`LinearOperator.quad`,
`(M * self).T * self`) contracts a 1-D input as a vector (`J(Jᵀv)`), not as `diag(v)`. For
`MultinomialLogitTransform` the Jacobian is a coupled `ShermanMorrison` operator, so the
off-diagonal `J Σ Jᵀ` mass that belongs on the diagonal is lost. Scalar transforms (log, log10,
logistic) have diagonal Jacobians where both contractions coincide, which is why every campaign
test passes.

## Fix

For a `LinearOperator` covariance keep the dense matrix (`covariance.to_dense()`) through the
Jacobian loop when `self.transforms` is non-empty; take `.diagonal()` only in the no-transform
case. Keying on `is_diagonal` is wrong: `diag(v)` under a coupled J still needs the full matrix.
Verified by monkeypatch: all three input forms return [1.2222, 1.2431]; scalar-transform results
bit-identical.

Test: parametrise the operator-vs-array equivalence in
`test_autofit/messages/test_transformed_from_mode.py` (added by #1560, currently scalar-only) over
`MultiLogitNormalMessage` with a 2x2 Σ, asserting both forms equal the delta-method reference.

## Impact

`MeanField.from_mode_covariance` (`autofit/graphical/mean_field.py:397`) is the only in-library
caller and is fed dense ndarrays from `VariableOperator.blocks()` /
`VariableFullOperator.blocks()`, so the branch is defensive-only in the live EP/Laplace path.
`MultiLogitNormalMessage` has zero hits in any workspace.
