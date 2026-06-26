# `@PyAutoFit` `UniformPrior.logpdf` does not handle array inputs

Found during the priors/messages audit (see
`PyAutoPrompt/autofit/priors_and_messages_math_audit.md`, finding A7).

## Problem

`@PyAutoFit/autofit/mapper/prior/uniform.py:100-116`:

```python
def logpdf(self, x):
    # TODO: handle x as a numpy array
    if x == self.lower_limit:
        x += epsilon
    elif x == self.upper_limit:
        x -= epsilon
    return self.message.logpdf(x)
```

The `if x == self.lower_limit:` test is scalar-only. The `# TODO`
acknowledges the gap. Passing a numpy array raises
`ValueError: The truth value of an array with more than one element is
ambiguous`.

## Wider context — how `logpdf` is called

`Prior.logpdf` is the user-facing way to evaluate a prior's log density.
It's invoked from:

- Plotting / visualisation code that vectorises across a grid.
- Diagnostic notebooks comparing priors.
- Anywhere the user wants to ask "what is p(x) under this prior"
  without going through the full search machinery.

The internal NonLinearSearch / Fitness machinery uses
`log_prior_from_value` (which is correctly array-safe for the JAX path,
see `uniform.py:167-179`). So this bug doesn't break inference — it
breaks user-facing density evaluation. The fact that the `# TODO` has
sat there suggests the array path was never used in earnest.

The boundary epsilon-snap exists because `UniformNormalMessage.logpdf`
goes to `-inf` exactly at the limits (`phi_transform` is `Φ⁻¹`, and
`Φ⁻¹(0) = -inf`). The fix needs to preserve that behaviour for arrays.

## Python reproducer

```python
# Reproducer: uniform_logpdf_array_handling.py
import numpy as np
import autofit as af

prior = af.UniformPrior(lower_limit=0.0, upper_limit=1.0)

# Scalar works
print(f"scalar logpdf(0.5) = {prior.logpdf(0.5)}")

# Boundary scalar works (epsilon-snap path)
print(f"scalar logpdf(0.0) = {prior.logpdf(0.0)}  (lower edge)")

# Array breaks
try:
    print(prior.logpdf(np.array([0.2, 0.5, 0.7])))
except ValueError as e:
    print(f"ARRAY: ValueError as expected: {e}")

# Array including boundaries (what we'd want post-fix)
try:
    print(prior.logpdf(np.array([0.0, 0.5, 1.0])))
except ValueError as e:
    print(f"ARRAY w/ boundaries: ValueError as expected: {e}")
```

Expected (buggy) output: scalar calls succeed, array calls raise
`ValueError: The truth value of an array with more than one element is
ambiguous`.

## Proposed fix

Replace the scalar boundary-snap with a vectorised np.where (mirroring
the pattern already in `log_prior_from_value`):

```python
def logpdf(self, x):
    x = np.asarray(x)
    x = np.where(x == self.lower_limit, x + epsilon, x)
    x = np.where(x == self.upper_limit, x - epsilon, x)
    return self.message.logpdf(x)
```

Open question for the reviewer: do we want `logpdf` to return `-inf`
for x outside `[lower_limit, upper_limit]` (like `log_prior_from_value`
on the JAX path), or do we want to keep delegating unconditionally to
the message (which extrapolates via the `phi_transform`)? Current
scalar behaviour silently delegates — array behaviour should match
that, but the reviewer should confirm.

## What the agent picking this up should do

1. Read `@PyAutoFit/autofit/mapper/prior/uniform.py` end-to-end.
2. Read `@PyAutoFit/autofit/messages/composed_transform.py` to
   understand what the underlying `UniformNormalMessage.logpdf` does
   for out-of-support values — the fix must not change that behaviour
   accidentally.
3. Run the reproducer. Confirm scalar works and array raises.
4. Sketch the fix above in a scratch checkout (no commit). Re-run the
   reproducer to confirm array calls now succeed and match
   `scipy.stats.uniform.logpdf` over the support.
5. File the GitHub issue via `/create_issue priors/02_uniform_logpdf_array_handling.md`.
6. **In the issue body, ask the reviewer to weigh in on the
   out-of-support semantics question above.** Also ask whether the
   `epsilon = 1e-14` snap is still load-bearing or whether a clean
   `np.where(in_bounds, message.logpdf, -np.inf)` would be cleaner.
7. **Stop. Do not implement until the open question is resolved.**
