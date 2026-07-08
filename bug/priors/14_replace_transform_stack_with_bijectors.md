# `@PyAutoFit` Refactor: replace hand-rolled `AbstractDensityTransform` with `tfp.bijectors` / `numpyro.distributions.transforms`

Type: bug
Target: priors
Difficulty: too-large
Autonomy: supervised
Priority: normal
Status: formalised

Found during the priors/messages audit (see
`PyAutoPrompt/autofit/priors_and_messages_math_audit.md`, finding C5).

> **Prerequisites:** Prompts 01-13 should at least be acked. This is
> the largest single change in the audit; it should not begin without
> the math bugs caught, the property tests in place, and a clear
> position on the class hierarchy from prompts 12/13.
>
> **Scope warning:** introduces an external dependency. Read carefully
> before opening the issue.

## Problem

`@PyAutoFit/autofit/messages/transform.py` defines
`AbstractDensityTransform` with a public API of:

- `transform(x)`
- `inv_transform(x)`
- `jacobian(x)`
- `log_det(x)`
- `log_det_grad(x)`
- `log_det_hess(x)`
- `transform_det(x)`
- `transform_jac(x)`
- `transform_det_jac(x)`
- `transform_func(...)`
- `transform_func_grad(...)`
- `transform_func_grad_hess(...)`

Plus a concrete set: `LinearTransform`, `LinearShiftTransform`,
`FunctionTransform`, `MultinomialLogitTransform`, and module-level
`exp_transform`, `log_transform`, `log_10_transform`,
`logistic_transform`, `phi_transform`.

This re-implements the public surface of
`tensorflow_probability.bijectors` and
`numpyro.distributions.transforms` — both of which:

- Are JAX-native (`tfp.experimental.substrates.jax.bijectors` and
  `numpyro.distributions` both have first-class JAX support).
- Are autograd-friendly (no need to hand-write `log_det_grad`).
- Have hundreds of contributor-years of correctness work on this
  exact math.
- Cover edge cases the current code does not (e.g. stable
  `log1mexp` for `sigmoid_grad`, masked Jacobians for the simplex).

## Wider context — what the current code costs

1. **Math correctness reimplemented from scratch.** The LogUniform
   sign bug, prompt 04 (truncated normal log_partition), and the
   asymmetric reversal convention in prompt 11 are all symptoms of
   hand-rolled transform composition.

2. **Numerical fragility.** `FunctionTransform.log_det_grad` uses
   `hs / gs` (`transform.py:228`) which loses precision when `gs` is
   small (e.g. boundary of `phi_transform`). `tfb.NormalCDF` uses
   stabilised `log_prob` internally.

3. **JAX dispatch is bolted on.** The current `xp=np` kwargs are a
   per-function decision; new transforms forget to thread `xp` and
   silently NumPy-fall-back. Bijector libraries handle this at the
   framework level.

4. **`numerical_jacobian` exists as a fallback.** The fact that the
   codebase carries a finite-difference Jacobian function
   (`transform.py:23-35`) for transforms that should have closed-form
   ones is a smell.

## Wider context — what migration would buy / cost

**Buy:**
- ~600 LoC of hand-rolled math deleted (`transform.py` +
  `composed_transform.py` core).
- Free JAX gradients via the chosen library's autodiff support.
- All five existing transforms have direct 1:1 equivalents:

  | autofit | tfp.bijectors | numpyro.distributions.transforms |
  |---|---|---|
  | `LinearShiftTransform(shift, scale)` | `tfb.Shift(shift) ∘ tfb.Scale(scale)` | `AffineTransform(shift, scale)` |
  | `exp_transform` | `tfb.Exp()` | `ExpTransform()` |
  | `log_transform` | `tfb.Log()` | `ExpTransform().inv` |
  | `log_10_transform` | `tfb.Log() / log(10)` (no direct equivalent — chain) | similar |
  | `logistic_transform` | `tfb.Sigmoid()` | `SigmoidTransform()` |
  | `phi_transform` | `tfb.NormalCDF()` | `NormalTransform()` (or composition) |
  | `MultinomialLogitTransform` | `tfb.SoftmaxCentered()` | `SoftmaxTransform()` |

**Cost:**
- New top-level dependency on either `tensorflow_probability` or
  `numpyro`. tfp is heavier (pulls TensorFlow if not using the JAX
  substrate); numpyro is lighter but requires JAX.
- Existing users who subclass `AbstractDensityTransform` (none in the
  audit's repo grep, but external users may) have their code break.
- `TransformedMessage` composition machinery needs rewriting to use
  the library's `Chain` / composition primitives.

## Python reproducer — exposition, not a bug

```python
# Reproducer: replace_transform_stack_with_bijectors.py
# Compare the current hand-rolled phi_transform against tfp / scipy
# equivalents for numerical stability near the boundary.

import numpy as np
from scipy.special import ndtri, ndtr
from autofit.messages.transform import phi_transform

xs = np.array([1e-10, 1e-6, 1e-3, 0.5, 1 - 1e-3, 1 - 1e-6, 1 - 1e-10])

print("Boundary stability test for inv_transform (ndtr) and log_det:")
print(f"{'x':>14} {'inv':>14} {'log_det':>14}")
for x in xs:
    inv = phi_transform.inv_transform(np.asarray(x))
    ld = phi_transform.log_det(np.asarray(x))
    print(f"{x:>14.6e} {float(inv):>14.6f} {float(ld):>14.6f}")
print()
print("With tfp.bijectors.NormalCDF or numpyro's equivalent, the")
print("log_det path would use a stabilised formula and not lose")
print("precision near the boundaries.")
```

The current code uses `epsilon = 1e-14` snapping in `ndtri` to dodge
boundary infinities. Bijector libraries handle this more cleanly
with explicit `log_prob` computations that don't require snapping.

## Proposed direction

Two-phase plan:

### Phase 1: parallel implementation

Add a `autofit/messages/transforms_bijector.py` (or similar) that
provides a `Bijector`-based version of each transform, alongside the
existing `AbstractDensityTransform`-based one. New `TransformedMessage`
instances can opt into the new path via a kwarg.

The five existing concrete transforms get bijector equivalents:

```python
# Sketch
from numpyro.distributions import transforms as t

phi_bijector = t.SigmoidTransform().inv ∘ ...  # see docs for exact form
log_bijector = t.ExpTransform().inv
linear_shift_bijector = t.AffineTransform(shift, scale)
# etc.
```

Property tests from prompt 09 run against both implementations to
verify equivalence.

### Phase 2: migration

Once the new path is solid, switch `UniformPrior` /
`LogUniformPrior` / `LogGaussianPrior` etc. to use the bijector
backend. Mark `AbstractDensityTransform` deprecated. Remove after
one release cycle.

## What the agent picking this up should do

1. Read `@PyAutoFit/autofit/messages/transform.py` and
   `@PyAutoFit/autofit/messages/composed_transform.py` end-to-end.
2. Grep `@PyAutoFit`, `@PyAutoArray`, `@PyAutoGalaxy`, `@PyAutoLens`,
   the workspaces for any external subclass of
   `AbstractDensityTransform`. List them (deprecation surface).
3. Choose between `tfp.experimental.substrates.jax.bijectors` and
   `numpyro.distributions.transforms`. Write a short comparison: which
   ships with PyAutoFit's existing JAX optional-extra, which has
   simpler dependencies, which has the better long-term Python
   support story.
4. Run the reproducer to confirm the existing transform stack has the
   boundary-stability character claimed.
5. File the GitHub issue via
   `/create_issue priors/14_replace_transform_stack_with_bijectors.md`.
6. **In the issue body, present the buy/cost analysis above and ask
   the reviewer for a go/no-go decision before any code is written.**
   The library choice (tfp vs numpyro) is itself a major call.
7. **Stop. No code until a green light.** This is the largest single
   piece of work in the audit; rushing it would regress everything
   prompts 01-13 fixed.

## Out-of-scope reminders

- This prompt is **not** the right place to revisit the `Prior` /
  `Message` split — that's prompt 13.
- This prompt is **not** the right place to add JAX-native priors
  end-to-end — that's already done in commit `2e3540771` (`feat:
  JAX-native priors`).
- This prompt is **not** about refactoring the EP machinery — only
  the transform stack underneath `TransformedMessage`.

<!-- formalised retroactively by the Intake (Conception) Agent on 2026-07-08 -->
