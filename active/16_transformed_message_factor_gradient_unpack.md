# `@PyAutoFit` `TransformedMessage.factor_gradient` crashes on first call

Type: bug
Target: priors
Difficulty: small
Autonomy: supervised
Priority: normal
Status: issued 2026-08-19 as PyAutoFit#1501 — awaiting external verification
(fix-or-delete hangs off the #1498 contract decision); do not start dev
Issued: 2026-08-19 (backfilled from active.md `registered:`)

Same shape as census finding A1 (#1331-01): a code path that has never run
end-to-end, dead on arrival.

## The finding

`TransformedMessage.factor_gradient` (`composed_transform.py:360-378`, main @
`21288bb`) unpacks four values from `self._transform_det_jac(x)`:

```python
x, logd, logd_grad, jacs = self._transform_det_jac(x)
```

but `_transform_det_jac` (`composed_transform.py:281-289`) returns three:
`(x, logd, logd_jacs)` where `logd_jacs` is a list of
`(logd_grad, jac)` tuples. Any call raises
`ValueError: not enough values to unpack (expected 4, got 3)`.

Reproducer on main:

```python
import autofit as af
af.UniformPrior(0.0, 2.0).message.factor_gradient(1.3)
# ValueError: not enough values to unpack (expected 4, got 3)
```

Even past the unpack, the body is wrong for the actual return structure: the
`for jac in reversed(jacs): grad = grad * jac` loop and the final
`grad + logd_grad` assume flat lists that `_transform_det_jac` does not
produce.

## Exposure

Zero production callers in `autofit/` — the `factor_gradient` in
`graphical/laplace/line_search.py` is an unrelated
FactorApproximation-level interface, and the only `exp_factor` use is one
test. So this is dead code that crashes if ever exercised; no live search
or EP path is affected.

## The fix (two options, adjudicate with #1498)

1. Repair it to be the physical-density gradient companion of `factor`
   (value `base.logpdf(T(x)) + log_det`, gradient chain-ruled **plus** the
   `log_det` gradient) and add it to the #1497 property sweep so the
   gradient is checked against a numerical derivative of `factor`.
2. Delete it — if the #1498/#1500 adjudication lands a single-source
   `log_density` contract, a hand-rolled second gradient path is exactly
   the kind of duplicate this cleanup exists to remove.

Do not fix silently ahead of the #1498 contract decision; whichever
convention wins decides whether this method should exist at all.
