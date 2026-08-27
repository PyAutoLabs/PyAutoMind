Fixed `TransformedMessage.factor_gradient` (`autofit/messages/composed_transform.py`), which crashed on every call with `ValueError: not enough values to unpack (expected 4, got 3)` because it unpacked four values from `_transform_det_jac`, which returns `(x, logd, logd_jacs)`.

Shipped via community PR https://github.com/PyAutoLabs/PyAutoFit/pull/1502 (@trexfr-ops), merged 2026-08-27 as `ae37ea817`; closes https://github.com/PyAutoLabs/PyAutoFit/issues/1501.

- Unpack corrected; gradient chain-ruled as `grad = grad * jac + logd_grad` over `reversed(logd_jacs)`, i.e. back through the transforms in reverse application order, so `factor_gradient` is the true gradient of `factor` (physical density including the log-det term).
- Added `test_transformed_message_factor_gradient` (analytic vs numerical derivative of `factor`).
- Maintainer verification before merge: finite-difference agreement to ~1e-10 on 2-transform (logistic + linear shift on (0, 2)) and 3-transform (log-uniform) chains with a non-flat Normal base, and on a 2-vector message. The two-transform test case recommended by the 2026-08-27 adjudication was performed as a pre-merge check rather than added to the PR.
- Option 1 (repair) chosen; independent of #1498 since `factor` stays the physical density under every #1498 option. #1498 remains open.

## Original prompt

# `@PyAutoFit` `TransformedMessage.factor_gradient` crashes on first call

Type: bug
Target: priors
Difficulty: small
Autonomy: supervised
Priority: normal
Status: issued 2026-08-19 as PyAutoFit#1501 — community PR PyAutoFit#1502
(@trexfr-ops) fixes it and its CI is GREEN on head 1da31ed; adjudicated as
mergeable independent of #1498 (see "Adjudication 2026-08-27" below), decision
pending human
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

### Adjudication 2026-08-27

Adjudicated by the Bug Agent session of 2026-08-27: option 1 (repair) wins, and
it does not have to wait for #1498. `factor_gradient` is the gradient of
`factor`, and `factor` stays the physical density under every #1498 option, so
the method's contract is stable whichever convention lands — community PR
PyAutoFit#1502 (@trexfr-ops) is therefore mergeable independent of #1498, and
its diff was verified correct against finite differences. Its CI is GREEN on
head 1da31ed (the maintainer updated the branch with main; the first run was red
purely from a 46-commit-stale base). Recommended sequence: adjudicate #1498 as
option B (base-space message contract, public `Prior.logpdf` via `factor`), then
merge #1502 once it carries a two-transform test case (e.g. `UniformPrior(0, 2)`)
at a tighter tolerance. Merge/close stays human.
