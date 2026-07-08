# `@PyAutoFit` `GammaMessage.from_mode` produces a Gamma that matches neither the requested mode nor variance

Type: bug
Target: priors
Difficulty: too-large
Autonomy: supervised
Priority: normal
Status: formalised

Found during the priors/messages audit (see
`PyAutoPrompt/autofit/priors_and_messages_math_audit.md`, finding A3).

## Problem

`@PyAutoFit/autofit/messages/gamma.py:75-81`:

```python
@classmethod
def from_mode(cls, mode, covariance, **kwargs):
    m, V = cls._get_mean_variance(mode, covariance)
    alpha = 1 + m ** 2 * V   # m=mode, V=variance → units: variance²
    beta  = alpha / m
    return cls(alpha, beta, **kwargs)
```

The Gamma distribution with rate parameterisation has:

- `mode = (α - 1) / β`  (for α ≥ 1)
- `variance = α / β²`

The formula `alpha = 1 + m² * V` does not satisfy either equation. It
is also dimensionally wrong: `m²` has units of (variance), `V` is
variance, so `m² * V` has units of variance². `α` is dimensionless.

The "1 +" suggests someone intended `α = 1 + m²/V` (the mean-matching
closed form that holds when mean ≈ mode for large α), but the operator
is wrong.

## Wider context — how `from_mode` is used

`from_mode` is the standard way to construct a message from a point
estimate. Sister methods:

- `NormalMessage.from_mode` (`@PyAutoFit/autofit/messages/normal.py:296-327`)
  — for a Gaussian, mode == mean, so `from_mode(m, V)` just constructs
  `NormalMessage(mode, sqrt(V))`. Correct.
- `TruncatedNormalMessage.from_mode` — same pattern, correct.

For asymmetric distributions like Gamma, mode != mean, so "from_mode"
has to solve a system. The expected invariants the reviewer should
confirm:

- **Interpretation A** (match mode + variance exactly): solve
  `mode = (α-1)/β` and `var = α/β²` jointly → quadratic in α.
- **Interpretation B** (match mean to mode, match variance): use
  `mean = α/β = m` and `var = α/β² = V` → `α = m²/V`, `β = m/V`. The
  resulting Gamma has mean=m, var=V, and mode = m - V/m (only equals m
  when V → 0).
- **Interpretation C** (current code's apparent intent — buggy):
  `α = 1 + m²/V` (close to Interpretation B but with the "+1" shift
  used in some texts to keep α ≥ 1).

The audit doc proposes the current line should be `α = 1 + m²/V`, but
the reviewer should confirm whether the call sites expect mean-matching
or mode-matching behaviour. Search for callers of `GammaMessage.from_mode`
to find out — the audit found none in the test suite, which is itself
a finding.

## Python reproducer

```python
# Reproducer: gamma_from_mode_wrong_formula.py
import numpy as np

from autofit.messages.gamma import GammaMessage

np.random.seed(0)

target_mode, target_var = 2.0, 1.0

print(f"Target: mode = {target_mode}, var = {target_var}")
print()

g = GammaMessage.from_mode(target_mode, target_var)
print(f"Constructed: alpha = {g.alpha:.4f}, beta = {g.beta:.4f}")

# What the resulting Gamma actually has:
analytic_mean = g.alpha / g.beta
analytic_var = g.alpha / g.beta ** 2
analytic_mode = (g.alpha - 1) / g.beta if g.alpha >= 1 else 0.0
print(f"Resulting analytic mean = {analytic_mean:.4f}")
print(f"Resulting analytic var  = {analytic_var:.4f}")
print(f"Resulting analytic mode = {analytic_mode:.4f}")
print()

# Sample-based sanity check
samples = np.random.gamma(g.alpha, scale=1 / g.beta, size=200_000)
print(f"Sampled mean = {samples.mean():.4f}")
print(f"Sampled var  = {samples.var():.4f}")
print()

# Compare to the two plausible intended formulas
def gamma_from_mode_intended_match_mean(m, V):
    """Interpretation B: mean=mode, var=V."""
    alpha = m ** 2 / V
    beta = m / V
    return alpha, beta

def gamma_from_mode_audit_proposed(m, V):
    """Audit's proposed fix: alpha = 1 + m^2/V."""
    alpha = 1 + m ** 2 / V
    beta = alpha / m
    return alpha, beta

aB, bB = gamma_from_mode_intended_match_mean(target_mode, target_var)
print(f"If we'd used alpha=m²/V (match mean):     "
      f"alpha={aB:.4f}, beta={bB:.4f}, "
      f"mean={aB/bB:.4f}, var={aB/bB**2:.4f}, "
      f"mode={(aB-1)/bB:.4f}")

aC, bC = gamma_from_mode_audit_proposed(target_mode, target_var)
print(f"If we'd used alpha=1+m²/V (audit's guess): "
      f"alpha={aC:.4f}, beta={bC:.4f}, "
      f"mean={aC/bC:.4f}, var={aC/bC**2:.4f}, "
      f"mode={(aC-1)/bC:.4f}")
```

Expected (buggy) output: the constructed Gamma's mean / var / mode do
not match the requested target. The two intended formulas land much
closer (in different ways).

## Proposed fix

**Needs design input.** The audit's first-pass guess is
`alpha = 1 + m**2 / V`, but the reviewer should confirm which invariant
`from_mode` is meant to maintain. Possible fixes, in order of likelihood:

1. `alpha = 1 + m**2 / V; beta = alpha / m`  — matches the intent
   suggested by the literal `"1 +"` in the current code.
2. `alpha = m**2 / V; beta = m / V`  — mean-matching (sister classes
   `NormalMessage.from_mode` are mean-matching, so this is consistent
   with the family).
3. Solve the quadratic to match mode + var exactly — only worth doing
   if a caller actually depends on the mode being preserved.

## What the agent picking this up should do

1. Read `@PyAutoFit/autofit/messages/gamma.py` and
   `@PyAutoFit/autofit/messages/normal.py:296-327` (sister
   `from_mode`) end-to-end.
2. Grep for `GammaMessage.from_mode` and `Gamma.*from_mode` across
   `@PyAutoFit` and the workspaces — list every call site so the
   reviewer can see what invariant callers depend on.
3. Run the reproducer. Confirm the three formulas produce three
   different Gammas.
4. File the GitHub issue via `/create_issue priors/03_gamma_from_mode_wrong_formula.md`.
5. **In the issue body, ask the reviewer to pick between options 1 / 2
   / 3 above based on what `from_mode` is supposed to mean for this
   family.** This is a math + API design call, not a mechanical fix.
6. **Stop. Do not implement until the reviewer specifies the desired
   invariant.**

<!-- formalised retroactively by the Intake (Conception) Agent on 2026-07-08 -->
