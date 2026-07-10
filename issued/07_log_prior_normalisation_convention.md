# `@PyAutoFit` `log_prior_from_value` convention is inconsistent across priors

Type: bug
Target: priors
Difficulty: too-large
Autonomy: supervised
Priority: normal
Status: formalised

Found during the priors/messages audit (see
`PyAutoPrompt/autofit/priors_and_messages_math_audit.md`, finding A5).

## Problem

After the LogUniform sign-convention fix (`e95295b83`), every prior's
`log_prior_from_value` returns "density form" — but the choice of which
additive constants to drop is inconsistent:

| Prior / message | `log_prior_from_value(x)` returns | Dropped constants |
|---|---|---|
| `UniformPrior` | `0.0` | `-log(b - a)` |
| `LogUniformPrior` | `-log x` | `-log log(b/a)` |
| `NormalMessage` (used by `GaussianPrior` via `__getattr__`) | `-(x-μ)² / (2σ²)` | `-log σ - 0.5·log(2π)` |
| `LogGaussianPrior` | `-(log x - μ)²/(2σ²) - log x` | `-log σ - 0.5·log(2π)` |
| `TruncatedNormalMessage` | full normalised density including `-log σ`, `-0.5·log(2π)`, `-log Z` | **none** |

The TruncatedNormal is the odd one out — it returns the full normalised
density. Everything else drops at least one constant.

## Wider context — what this affects

For the existing inference machinery this is fine:

- **MCMC** (`Emcee`, `Zeus`) — only ratios of log-posterior matter,
  additive constants cancel.
- **MLE** (`LBFGS`, `BFGS`, `Drawer`) — minimises `-2 · figure_of_merit`,
  additive constants are dropped from the gradient.
- **Nested sampling** (`Dynesty`, `Nautilus`) — uses `prior_transform`,
  not `log_prior_from_value`, so this column is bypass-able.

So *posterior shape* and *MAP location* are correct under the current
inconsistency. But it's a foot-gun for:

1. **Marginal likelihood / Bayes-factor calculations** that try to read
   `log_likelihood + sum(log_priors)` as an actual log-evidence. The
   missing constants make cross-prior-family comparisons silently
   wrong.
2. **Anyone calling `prior.logpdf(x)` and expecting a proper density**.
   Some priors give a normalised density, some don't — depends on
   which class.
3. **Future contributors** following the existing pattern when adding
   a new prior. The current code teaches the wrong lesson (mix of
   conventions).

The recent fix-commit (`e95295b83`) deliberately picked "drop constants"
for the Gaussian-family fixes, on the grounds that the constants are
"a true constant in the prior, irrelevant to posterior shape". But it
didn't propagate that decision to TruncatedNormal, and didn't put the
convention in a docstring anyone could find.

## Python reproducer

```python
# Reproducer: log_prior_normalisation_convention.py
import numpy as np
from scipy.integrate import quad

import autofit as af
from autofit.messages.truncated_normal import TruncatedNormalMessage

def integrate_exp_log_prior(prior, lo, hi, **kwargs):
    """Numerically integrate exp(log_prior_from_value(x)) over [lo, hi]."""
    def f(x):
        return float(np.exp(prior.log_prior_from_value(float(x))))
    I, _ = quad(f, lo, hi, **kwargs)
    return I

# 1. Uniform
u = af.UniformPrior(lower_limit=0.0, upper_limit=2.0)
I_u = integrate_exp_log_prior(u, 0.0, 2.0)
print(f"Uniform(0, 2):       ∫ exp(log_prior) dx = {I_u:.4f}  (drops -log(b-a)=-log 2)")

# 2. LogUniform
lu = af.LogUniformPrior(lower_limit=0.1, upper_limit=10.0)
I_lu = integrate_exp_log_prior(lu, 0.1, 10.0)
print(f"LogUniform(0.1, 10): ∫ exp(log_prior) dx = {I_lu:.4f}  (drops -log log(b/a))")

# 3. Gaussian (delegated to NormalMessage via __getattr__)
g = af.GaussianPrior(mean=0.0, sigma=1.0)
I_g = integrate_exp_log_prior(g, -10.0, 10.0)
print(f"Gaussian(0, 1):      ∫ exp(log_prior) dx = {I_g:.4f}  (drops -log σ - 0.5·log 2π)")

# 4. LogGaussian
lg = af.LogGaussianPrior(mean=0.0, sigma=1.0)
I_lg = integrate_exp_log_prior(lg, 1e-6, 100.0)
print(f"LogGaussian(0, 1):   ∫ exp(log_prior) dx = {I_lg:.4f}  (drops -log σ - 0.5·log 2π)")

# 5. TruncatedNormal — the odd one out
tn_msg = TruncatedNormalMessage(mean=0.0, sigma=1.0, lower_limit=-2.0, upper_limit=2.0)
I_tn = integrate_exp_log_prior(tn_msg, -2.0, 2.0)
print(f"TruncatedNormal:     ∫ exp(log_prior) dx = {I_tn:.4f}  (full normalised pdf — ≈1.0)")

print()
print("Convention is inconsistent: TruncatedNormal returns a normalised pdf,")
print("everything else returns up-to-additive-constant.")
```

Expected (buggy) output: the five integrals are all different. The
TruncatedNormal one is ≈ 1.0; the others are not.

## Proposed fix — needs a decision, not code

Two coherent options:

### Option A: drop constants everywhere (audit's first-pass recommendation)

Pros: matches existing Gaussian/LogGaussian/Uniform/LogUniform behaviour
(four out of five). Fastest path. Matches the *spirit* of the existing
fix commit. Lower runtime cost (no `log(Z)` for truncated normal in the
inference loop).

Cons: ` prior.logpdf` is no longer a proper density. Marginal-likelihood
calculations require a separate "log normaliser" hook per prior class.

Change required: `TruncatedNormalMessage.log_prior_from_value` drops the
constants — only return `-0.5·(x-μ)²/σ²` plus the in-bounds mask.

### Option B: keep full normalised density everywhere

Pros: `prior.logpdf(x)` is always a proper density, the value is
meaningful in isolation, evidence calculations are correct without
extra hooks. Matches `scipy.stats` convention.

Cons: bigger change (every prior is touched). Slight runtime cost in
the MCMC/MLE inner loop from computing constants that get cancelled
anyway. Need to ensure JAX paths are also normalised consistently.

### Decision criteria

The audit recommends asking the reviewer:

- Do any downstream consumers (workspace examples, `analysis` plotting,
  third-party code in `autoarray`/`autogalaxy`/`autolens`) read
  `prior.log_prior_from_value(x)` and treat it as a proper density?
- Is there appetite to expose a separate `prior.log_normaliser`
  property that returns the dropped constants on demand? This would
  let Option A coexist with evidence calculations.

Once chosen, the change is:

- Update every prior subclass to match the convention.
- Add a docstring on `Prior.log_prior_from_value` (the base class)
  stating the convention as a hard contract.
- Add a property-based test (see prompt 09) that asserts the convention
  on every subclass.

## What the agent picking this up should do

1. Read every prior's `log_prior_from_value` in
   `@PyAutoFit/autofit/mapper/prior/` and
   `@PyAutoFit/autofit/messages/`. Make a fresh version of the table
   above to confirm the audit's claims have not drifted.
2. Grep across `@PyAutoFit`, `@autofit_workspace`,
   `@PyAutoArray`, `@PyAutoGalaxy`, `@PyAutoLens` for callers of
   `log_prior_from_value` and `prior.logpdf` to identify downstream
   consumers. List each one in the issue body.
3. Run the reproducer. Confirm the five integrals differ.
4. File the GitHub issue via `/create_issue priors/07_log_prior_normalisation_convention.md`.
5. **In the issue body, frame the choice (Option A vs B) clearly and
   ask the reviewer to pick.** Provide the list of downstream callers
   so the reviewer can see which choice is least disruptive.
6. **Stop. This is a design decision, not a bug fix.** Implementation
   proceeds only after the reviewer signs off on the convention.


## Fable verdict (2026-07-08, PyAutoFit main @ 0f26ff2d8; PyAutoFit#1330)

**Verdict: CONFIRMED — design decision still open (Option A vs B).**
Integrals of exp(log_prior_from_value): Uniform(0,2) = 2.000,
LogUniform(0.1,10) = 4.605, Gaussian(0,1) = 2.507, LogGaussian(0,1) = 2.507,
TruncatedNormalMessage = 1.000 — four-vs-one inconsistency exactly as
audited. Current main's `NormalMessage.log_prior_from_value` docstring now
documents the drop-constants convention, strengthening Option A's claim to
be the de-facto standard. Recommend settling this inside Phase 2 of the EP
framework review (`research/graphical_ep/ep_framework_review.md`), whose
formal-equations documentation must state the convention either way.

<!-- formalised retroactively by the Intake (Conception) Agent on 2026-07-08 -->
