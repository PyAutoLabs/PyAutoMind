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

## Status 2026-08-27 — implemented, pushed, not yet PR'd

Both this and its sibling `redundant_prior_limits_overrides.md` were implemented
together on PyAutoFit branch `claude/loggaussian-prior-support-ngh59x`, commit
`4c0f79b` — one coherent change (the limits cleanup #1527 left behind) rather
than two PRs, which departs from "one prompt = one task = one PR" deliberately
and is worth splitting if a reviewer prefers.

Full suite **2186 passed / 36 skipped** (baseline 2178/36, +8 new tests).
No PR opened.

**A live bug turned up inside this work.** `VariableData.any` reduced through
`var_all`, so it answered "is there a variable whose elements are ALL True"
rather than "is ANY element True". `OptimisationState.valid` asks
`(parameters < lower_limit).any()`, so a parameter vector with *some* components
outside their limits was reported **valid** — only a variable violating on every
component was caught. `MeanField`'s `valid.any()` under-reported the same way.
Fixed in the same commit; the other four `.any()` call sites in the library are
numpy arrays and are untouched.

That bug, not the truthiness guard, is why the limits check under-enforced. This
prompt's own framing (a readability defect) was right about the guard and missed
the real one underneath it — found only because the guard rewrite needed a test
and `OptimisationState.valid` had **no test coverage at all**.
