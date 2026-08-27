- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1531 (shared with its sibling; closed by the PR)
- completed: 2026-08-27
- pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1532 (MERGED, merge `6e2d8c8`, head `4c0f79b`,
  label `pending-release`)
- summary: Deleted the three `limits` overrides PyAutoFit#1527 made exact duplicates of
  `Prior.limits`, plus their now-unused `Tuple` imports — after measuring the one difference that
  made it not a pure deletion.
- validation: 2186 passed / 36 skipped (baseline 2178/36); CI green on all four legs.
- release: not performed; merged PR sits in the pending-release queue.
- sibling: shipped in the same PR as `optimisation-state-limit-guard-truthiness` — the substantive
  half of that PR, and the record worth reading.

## What was deleted

`UniformPrior` (`uniform.py:205`), `LogUniformPrior` (`log_uniform.py:199`) and
`TruncatedGaussianPrior` (`truncated_gaussian.py:122`) each carried

```python
@property
def limits(self) -> Tuple[float, float]:
    return self.lower_limit, self.upper_limit
```

which #1527 made redundant when it changed the base `Prior.limits` from a hardcoded
`(-inf, inf)` to `(float(self.lower_limit), float(self.upper_limit))`.

## The measurement that made this safe — and why it was not obvious

The base coerces with `float()`; the three overrides did not. So deleting them changes the *type* of
what `limits` returns, and that value is not inert — `AbstractPriorModel.mapper_from_prior_means`
feeds it straight into `TruncatedGaussianPrior(mean, sigma, *limits)`
(`prior_model/abstract.py:1153`). Two ways it could have bitten:

1. **A numpy scalar becoming a Python float** in a constructed passed-prior. Measured: all three
   priors already store Python `float`s (`UniformPrior.__init__` does `self.lower_limit =
   float(lower_limit)` itself), so `float()` is a no-op. Values **and** types identical across all
   five prior families, before and after.
2. **A JAX tracer hitting `float()` under `jit`** and raising `ConcretizationTypeError`. This looked
   like the real risk, because `UniformPrior.tree_flatten` returns `(lower_limit, upper_limit, id)`
   as pytree **children** — so under `jit` they genuinely are tracers.

Point 2 turned out to be moot, for a reason worth recording: **a prior cannot cross a `jit` boundary
as an argument at all today.** With `autofit.jax.enable_pytrees()` on, `jax.jit(f)(prior)` raises
inside `tree_unflatten` → `UniformPrior.__init__`, at `self.lower_limit = float(lower_limit)`, before
any `limits` access happens. Verified for both the override path and the base path — identical
failure, with and without this change. So `limits` is unreachable under `jit` either way.

That is a latent limitation in its own right (a class registered as a pytree node that cannot
actually survive the round-trip), and it is **not** fixed here. Noted, not filed.

## Why this shipped in a two-prompt PR

Against PyAutoMind's "one prompt = one task = one PR". Both prompts are the same cleanup left by
#1527, this half is three line deletions plus three import edits, and splitting would have put the
type measurement above in one PR and the deletions it licenses in another. Flagged in the PR body
and to the human before merge.

## Repos / worktree

- PyAutoFit: `claude/loggaussian-prior-support-ngh59x` (merged, deletable).
- No worktree — ran `web-github` against a direct clone.

## Original prompt

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
Issued: 2026-08-27

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
