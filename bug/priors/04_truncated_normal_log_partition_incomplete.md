# `@PyAutoFit` `TruncatedNormalMessage` pdf does not integrate to 1 via the generic interface

Type: bug
Target: priors
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

Found during the priors/messages audit (see
`PyAutoPrompt/autofit/priors_and_messages_math_audit.md`, finding A4).

## Problem

`@PyAutoFit/autofit/messages/truncated_normal.py:29-49`:

```python
def log_partition(self, xp=np) -> float:
    from scipy.stats import norm
    a = (self.lower_limit - self.mean) / self.sigma
    b = (self.upper_limit - self.mean) / self.sigma
    Z = norm.cdf(b) - norm.cdf(a)
    return xp.log(Z) if Z > 0 else -xp.inf
```

This returns only the truncation normaliser `log Z`. It does **not**
include the standard Gaussian log-partition `A_gauss(η) = -η₁²/(4η₂) - 0.5·log(-2η₂)`.

The class inherits `MessageInterface.logpdf` (no override), which
computes:

```
logpdf(x) = log_base_measure + η·T(x) - log_partition()
```

With:
- `log_base_measure = -0.5·log(2π)`  (`truncated_normal.py:51`)
- `η = [μ/σ², -1/(2σ²)]`  (`truncated_normal.py:163-192`)
- `T(x) = [x, x²]`  (`truncated_normal.py:218-236`)
- `log_partition = log Z`  ← missing the Gaussian piece

Expanding:
```
logpdf(x) = -0.5·log(2π) + μx/σ² - x²/(2σ²) - log Z
          = -0.5·log(2π) - (x-μ)²/(2σ²) + μ²/(2σ²) - log Z
```

The correct truncated-normal log pdf is:
```
log p(x) = -0.5·log(2π) - log σ - (x-μ)²/(2σ²) - log Z   for x in [a, b]
```

So the generic-interface logpdf is wrong by `+μ²/(2σ²) + log σ` (i.e.
missing `-log σ - μ²/(2σ²)`). Consequently `truncated_message.pdf(x)`
does not integrate to 1.

`NormalMessage.log_partition` *does* include the Gaussian piece
(`@PyAutoFit/autofit/messages/normal.py:49-63`), so the bug is
specifically in the truncated subclass.

## Wider context — why this matters and why it's latent

The class also provides direct paths that are correct:

- `_normal_gradient_hessian` (`truncated_normal.py:349-407`) computes
  `logpdf` directly with the `-log σ` and `-log Z` terms.
- `log_prior_from_value` (`truncated_normal.py:481-522`) computes the
  full normalised density.

So:

- **Sampling** (uses `value_for`) — correct.
- **Inference figure-of-merit** (uses `log_prior_from_value` via
  `Fitness._call`) — correct.
- **EP / variational machinery** that calls `.logpdf` via the generic
  interface — wrong.
- **User-facing `.pdf(x)`** — wrong (gives a density that integrates
  to `σ · exp(μ²/(2σ²))` over the full normal support).

The latency is because `TruncatedNormalMessage` is rarely fed through
the EP machinery in practice. But anyone calling `.pdf()` or `.factor()`
on it gets a silently wrong answer.

## Python reproducer

```python
# Reproducer: truncated_normal_log_partition_incomplete.py
import numpy as np
from scipy.integrate import quad
from scipy.stats import truncnorm

from autofit.messages.truncated_normal import TruncatedNormalMessage

# Pick μ != 0 and σ != 1 so both missing terms (-log σ and -μ²/(2σ²))
# are visible. Bounds are wide so Z is close to 1 and we can see the
# generic-interface error as a clean ~σ·exp(μ²/(2σ²)) factor.
mean, sigma = 1.0, 2.0
lo, hi = -5.0, 5.0
msg = TruncatedNormalMessage(mean=mean, sigma=sigma, lower_limit=lo, upper_limit=hi)

# Path A: MessageInterface.logpdf (inherited, generic exponential family)
def pdf_via_interface(x):
    return float(np.exp(msg.logpdf(np.asarray(float(x)))))

# Path B: scipy.stats.truncnorm as ground truth
a, b = (lo - mean) / sigma, (hi - mean) / sigma
def pdf_correct(x):
    return float(truncnorm.pdf(x, a, b, loc=mean, scale=sigma))

# Path C: log_prior_from_value (the direct path, should be correct)
def pdf_via_log_prior(x):
    return float(np.exp(msg.log_prior_from_value(float(x))))

I_interface, _ = quad(pdf_via_interface, lo, hi)
I_correct, _ = quad(pdf_correct, lo, hi)
I_log_prior, _ = quad(pdf_via_log_prior, lo, hi)

print(f"∫ pdf dx via MessageInterface.logpdf (BUGGY): {I_interface:.4f}")
print(f"∫ pdf dx via log_prior_from_value (correct): {I_log_prior:.4f}")
print(f"∫ pdf dx via scipy.stats.truncnorm  (truth): {I_correct:.4f}")
print()
print(f"Expected ratio buggy / correct = σ · exp(μ²/(2σ²)) "
      f"= {sigma * np.exp(mean**2 / (2 * sigma**2)):.4f}")
print(f"Observed ratio                                 = "
      f"{I_interface / I_correct:.4f}")
```

Expected (buggy) output: `I_interface ≈ 2.27`, `I_log_prior ≈ 1.0`,
`I_correct ≈ 1.0`. The ratio matches `σ·exp(μ²/(2σ²)) = 2·exp(0.125)`.

## Proposed fix

Add the Gaussian log-partition to the truncation log-partition:

```python
def log_partition(self, xp=np) -> float:
    from scipy.stats import norm
    a = (self.lower_limit - self.mean) / self.sigma
    b = (self.upper_limit - self.mean) / self.sigma
    Z = norm.cdf(b) - norm.cdf(a)
    log_Z = xp.log(Z) if Z > 0 else -xp.inf

    # Same as NormalMessage.log_partition: -η₁²/(4η₂) - 0.5·log(-2η₂)
    eta1, eta2 = self.natural_parameters(xp=xp)
    A_gauss = -(eta1**2) / 4 / eta2 - xp.log(-2 * eta2) / 2

    return A_gauss + log_Z
```

Reviewer should also confirm whether `TruncatedNaturalNormal` (same
file, lines 569-) has the same bug — it inherits `log_partition` from
`TruncatedNormalMessage` so the fix should automatically propagate,
but it's worth a quick numerical check.

## What the agent picking this up should do

1. Read `@PyAutoFit/autofit/messages/truncated_normal.py` and
   `@PyAutoFit/autofit/messages/normal.py` (for the
   sister `log_partition` that *is* correct) and
   `@PyAutoFit/autofit/messages/interface.py:47-87` (the generic
   `logpdf` path that consumes `log_partition`).
2. Run the reproducer. Confirm the three integrals differ as predicted.
3. Sketch the fix in a scratch checkout (no commit). Re-run. Confirm
   `I_interface` now ≈ 1.0.
4. Repeat for `TruncatedNaturalNormal` to confirm the fix propagates.
5. File the GitHub issue via `/create_issue priors/04_truncated_normal_log_partition_incomplete.md`.
6. **In the issue body, ask a reviewer with exponential-family / EP
   background to verify the math. Note explicitly that this affects
   only the generic interface path; `log_prior_from_value` and
   sampling are unaffected.**
7. **Stop. Do not implement until the math is confirmed.**


## Fable verdict (2026-07-08, PyAutoFit main @ 0f26ff2d8; PyAutoFit#1330)

**Verdict: CONFIRMED, numerically exact — highest-priority math fix (severity: high for EP).**
Integral of pdf via the generic `MessageInterface.logpdf` = 2.2663, matching
the predicted error factor sigma*exp(mu^2/(2 sigma^2)) = 2.2663 to 4 d.p.;
`log_prior_from_value` and scipy truncnorm both = 1.0000. The generic
exponential-family path is precisely what `autofit/graphical` consumes, so
this is the first fix to land ahead of the EP statistics review (Phase 1 of
`research/graphical_ep/ep_framework_review.md`). Proposed fix (add the
Gaussian log-partition term) verified correct analytically.

<!-- formalised retroactively by the Intake (Conception) Agent on 2026-07-08 -->
