# `@PyAutoFit` `NormalMessage` silently accepts negative sigma; `TruncatedNormalMessage` rejects it

Found during the priors/messages audit (see
`PyAutoPrompt/autofit/priors_and_messages_math_audit.md`, finding A6).

## Problem

`@PyAutoFit/autofit/messages/normal.py:26-46` defines a helper
`assert_sigma_non_negative` with a JAX-aware branch:

```python
def assert_sigma_non_negative(sigma, xp=np):
    is_negative = sigma < 0
    if xp.__name__.startswith("jax"):
        import jax
        return jax.lax.cond(
            is_negative,
            lambda _: (_ for _ in ()).throw(ValueError("Sigma cannot be negative")),
            lambda _: None,
            operand=None,
        )
    else:
        if bool(is_negative):
            raise ValueError("Sigma cannot be negative")
```

Two problems:

1. The call site is commented out (`normal.py:103`):

   ```python
   # assert_sigma_non_negative(sigma, xp=xp)
   ```

   So negative sigma silently constructs a `NormalMessage` with a
   non-physical variance. Most downstream math (logpdf, gradient,
   `1/sigma²`) accidentally still gives a finite number — it's just
   wrong.

2. The JAX branch wouldn't behave as intended even if uncommented.
   `lambda _: (_ for _ in ()).throw(...)` creates a generator that
   throws when iterated, but `jax.lax.cond` doesn't iterate the lambda
   in trace mode — it traces both branches. Under `jit` the exception
   is suppressed/rewritten.

Meanwhile `TruncatedNormalMessage` *does* enforce this
(`@PyAutoFit/autofit/messages/truncated_normal.py:85-86`):

```python
if (np.array(sigma) < 0).any():
    raise exc.MessageException("Sigma cannot be negative")
```

So the two classes disagree on what counts as a valid input.

## Wider context — why the asymmetry matters

The inconsistency is load-bearing because `GaussianPrior` wraps
`NormalMessage` directly (not the truncated version), so anything that
produces a negative sigma upstream and feeds it into a `GaussianPrior`
goes undetected.

The audit identified two upstream sources that can produce negative
sigma:

- **`RelativeWidthModifier(value).__call__(mean)` → `value * mean`**
  (`@PyAutoFit/autofit/mapper/prior/width_modifier.py:78-81`). If
  `mean < 0`, the resulting sigma is negative. This is finding A9 in
  the audit and gets its own prompt (08).
- **Prior-passing `GaussianPrior.with_limits(lower, upper)` →
  `sigma = upper - lower`**. If a user inverts the limits or passes
  identical limits, the constructed prior has `sigma <= 0`. No check
  in either method.

So `NormalMessage` is the last line of defence. Fixing it here is the
high-leverage move because every other path eventually flows through
this constructor.

## Python reproducer

```python
# Reproducer: normal_message_sigma_negative_unchecked.py
import numpy as np
import autofit as af

from autofit.messages.normal import NormalMessage
from autofit.messages.truncated_normal import TruncatedNormalMessage

print("=== NormalMessage(0, sigma=-1) ===")
try:
    n = NormalMessage(mean=0.0, sigma=-1.0)
    print(f"  constructs silently: {n!r}")
    print(f"  variance = {n.variance}")   # = 1.0, deceptively finite
    print(f"  logpdf(0) = {n.logpdf(np.asarray(0.0))}")
except ValueError as e:
    print(f"  raised ValueError as expected: {e}")

print()
print("=== TruncatedNormalMessage(0, sigma=-1) ===")
try:
    t = TruncatedNormalMessage(mean=0.0, sigma=-1.0)
    print(f"  constructs silently: {t!r}")
except Exception as e:
    print(f"  raised {type(e).__name__}: {e}")

print()
print("=== GaussianPrior with collapsed limits ===")
try:
    p = af.GaussianPrior.with_limits(lower_limit=5.0, upper_limit=5.0)
    print(f"  constructs silently with sigma=0: {p!r}")
    print(f"  prior.value_for(0.5) = {p.value_for(0.5)}")
    # sigma=0 → degenerate, value_for collapses to mean
except Exception as e:
    print(f"  raised {type(e).__name__}: {e}")
```

Expected (buggy) output: `NormalMessage(0, -1)` constructs without
complaint and returns a finite `variance = 1.0`. `TruncatedNormalMessage(0, -1)`
raises `MessageException`. `GaussianPrior.with_limits(5, 5)` constructs
with sigma=0.

## Proposed fix

Two small changes, both straightforward:

1. **Enforce `sigma > 0` in `NormalMessage.__init__`** to match
   `TruncatedNormalMessage`. Either uncomment and fix the existing
   `assert_sigma_non_negative` helper, or just inline a NumPy check
   that doesn't try to be JAX-aware (the JAX path can defer to NaN
   propagation):

   ```python
   if (np.asarray(sigma) < 0).any():
       raise exc.MessageException("Sigma cannot be negative")
   ```

2. **Decide whether `sigma == 0` is also illegal.** A degenerate
   Gaussian has support {μ}, which breaks `logpdf`. Most users
   wouldn't construct it deliberately. Either:
   - reject (`sigma <= 0`), simpler and stricter, or
   - allow (`sigma < 0` rejected, `sigma == 0` permitted as a
     "point-mass-like" thing).

The audit recommends `sigma <= 0` → reject, but the reviewer should
confirm whether any current call site depends on `sigma == 0`
constructing.

## What the agent picking this up should do

1. Read `@PyAutoFit/autofit/messages/normal.py`,
   `@PyAutoFit/autofit/messages/truncated_normal.py:80-95`,
   `@PyAutoFit/autofit/mapper/prior/gaussian.py:69-96` (the
   `with_limits` upstream), and
   `@PyAutoFit/autofit/mapper/prior/width_modifier.py` (the other
   upstream that can produce negative sigma).
2. Run the reproducer. Confirm the three asymmetric outcomes.
3. Sketch the fix in a scratch checkout (no commit). Re-run. Confirm
   `NormalMessage(0, -1)` now raises.
4. Check whether any test in `@PyAutoFit/test_autofit` deliberately
   constructs `NormalMessage` with `sigma <= 0`. If yes, list those
   tests for the reviewer (they may be using degenerate priors for
   point-mass behaviour — and the fix would break them).
5. File the GitHub issue via `/create_issue priors/06_normal_message_sigma_negative_unchecked.md`.
6. **In the issue body, ask the reviewer to choose between
   `sigma < 0` rejected (allows `sigma == 0`) and `sigma <= 0`
   rejected. Note this prompt is the prerequisite for prompt 08
   (RelativeWidthModifier safety), which leans on this check.**
7. **Stop. Do not implement until the strict-vs-permissive question
   is settled.**
