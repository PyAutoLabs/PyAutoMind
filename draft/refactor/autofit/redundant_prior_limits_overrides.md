# Three `limits` overrides are now exact duplicates of `Prior.limits`

Type: refactor
Target: autofit
Repos:
- PyAutoFit
Difficulty: small
Autonomy: safe
Priority: low
Status: formalised
Filed: 2026-08-27

Follow-up owed by `complete/2026/08/loggaussian-prior-declares-own-support.md`
(PyAutoFit#1526 / #1527), which named it and deliberately left it out to keep
that PR narrow.

## The duplication

PyAutoFit#1527 changed `Prior.limits` (`autofit/mapper/prior/abstract.py:360-373`)
from a hardcoded `(float("-inf"), float("inf"))` to

```python
return (float(self.lower_limit), float(self.upper_limit))
```

Three subclasses override it with what is now the same thing:

| File | Line | Body |
|---|---|---|
| `autofit/mapper/prior/uniform.py` | 205 | `return self.lower_limit, self.upper_limit` |
| `autofit/mapper/prior/log_uniform.py` | 199 | `return self.lower_limit, self.upper_limit` |
| `autofit/mapper/prior/truncated_gaussian.py` | 122 | `return self.lower_limit, self.upper_limit` |

## The one difference, and it is not cosmetic

The base coerces with `float(...)`; the three overrides do not. So deleting them
changes the *type* of what `limits` returns for these priors — a bare attribute
(possibly a numpy scalar, or a JAX tracer under `jit`) becomes a Python `float`.

That is the whole risk of this task, and it is why it is not a pure deletion:

- `AbstractPriorModel.mapper_from_prior_means` feeds `limits` straight into
  `TruncatedGaussianPrior(mean, sigma, *limits)`
  (`autofit/mapper/prior_model/abstract.py:1147-1156`), so the constructed
  prior's limit types change with it.
- Anything under `jax.jit` that reaches `limits` on a traced value would go from
  passing the tracer through to raising `ConcretizationTypeError` at `float()`.

Check both before deleting. If the coercion turns out to be the problem rather
than the overrides, the right change may be the reverse — drop `float()` from
the base — in which case say so and stop.

## The fix

Delete the three overrides if and only if the type question above comes back
clean. Otherwise reconcile the base and the overrides on one convention and
document which.

## Verify

- `UniformPrior(0.0, 2.0).limits == (0.0, 2.0)`, and likewise for `LogUniform`
  and `TruncatedGaussian`, before and after — values *and* types.
- `test_autofit/mapper/prior/test_prior_properties.py` P6 (the reported-support
  property added by #1527) still passes for every prior family.
- A JAX-path fit that touches `limits` under `jit`, if one exists — if none
  does, say so rather than assuming the path is unreachable. #1477's process
  lesson applies: the 1790-test suite passed against an `LBFGS._fit` that raised
  `NameError` on every real call, because nothing executed it.
