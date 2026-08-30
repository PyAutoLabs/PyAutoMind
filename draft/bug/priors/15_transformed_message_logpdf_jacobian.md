# `@PyAutoFit` `TransformedMessage.logpdf`/`pdf` omit the transform Jacobian

Type: bug
Target: priors
Themes:
- graphical-ep
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised — issue filed (PyAutoFit#1498); caller analysis complete
Consequence: judge
Review-minutes: 20
Unattended: ready
(2026-08-19, below), awaiting human adjudication of the contract choice
Filed: 2026-08-18 (backfilled from git)

Found 2026-08-18 while implementing the #1497 property sweep (prompt
`bug/priors/09`). Same failure *shape* as census finding A4 (#1331-04): a
generic-interface density path is silently wrong while the direct paths are
right.

## The finding

`TransformedMessage` inherits `MessageInterface.logpdf` (the natural-parameter
path). Its overrides forward `natural_parameters`, `calc_log_base_measure` and
`to_canonical_form` to the base message — `to_canonical_form` is
`@transform`-decorated, so the physical input is mapped to base coordinates —
but **no `log_det` change-of-variables term is ever added**. `logpdf(x)` at a
physical `x` therefore returns the *base-space* density at the mapped point,
not the physical density. `TransformedMessage.factor(x)` does it correctly
(`base.logpdf(transform(x)) + log_det`).

Reproduction on `main` @ `7d4d931` (exact numbers):

- `af.UniformPrior(0,1).message.logpdf(0.7)` = −1.05644 (physical density is
  1.0 → expect 0.0); `factor(0.7)` = 0.0 ✓
- `∫ exp(logpdf)` over [0,1] = **0.282095 = 1/(2√π)**, not 1.0;
  `∫ exp(factor)` = 1.000000 ✓
- `LogUniformPrior(0.01, 100)`: generic-path pdf integrates to **15.83**.

Every `TransformedMessage`-wrapped prior (Uniform, LogUniform, LogGaussian) is
affected. `NormalMessage` / `TruncatedNormalMessage` priors are not.
`value_for`, `cdf`, `log_prior_from_value` and `factor` are all verified
correct — sampling and MCMC/MLE log-priors are unaffected; the exposure is
anything treating `transformed_message.pdf()` as a physical density.

## Doc contradiction

The `composed_transform.py` module docstring (added by #1334) claims `logpdf`
accumulates the log-Jacobian. The code does not. Either the docstring states
the intended contract (then `logpdf` needs the `log_det` term) or `logpdf` is
deliberately base-space for EP message arithmetic (then the docstring and
`pdf()` are misleading and should say so).

## What adjudication needs

1. Inventory callers of `TransformedMessage.logpdf`/`pdf` vs `factor` —
   especially whether any EP projection / `log_norm` path evaluates `logpdf`
   on transformed messages at physical coordinates.
2. `logpdf_gradient` returns the base `log_likelihood` with a
   Jacobian-corrected *gradient* (value base-space, gradient physical) — a
   third convention to settle in the same pass.
3. Decide: add `log_det` to the generic path, or document base-space `logpdf`
   as the contract and fix the module docstring + `pdf()`.

The #1497 property tests assert the physical density via `factor` and cite
#1498 at the site (`physical_log_density` helper in
`test_autofit/mapper/prior/test_prior_properties.py`); tighten them to
`logpdf` once resolved.

## Caller analysis (2026-08-19, main @ `21288bb`)

The inventory #1498 adjudication point 1 asked for, run over the full
`autofit/` production tree (tests excluded). Verified numerically:
`UniformPrior(0,2)` gives `logpdf(1.3) = −0.993174` vs
`factor(1.3) = −0.693147 = log 0.5`; `∫exp(logpdf)` over the support is
`0.564190 = 2/(2√π)` while `∫exp(factor)` is `1.000000`.

**Callers expecting a physical density (exposed to the bug):**

- `Prior.logpdf` — the public prior API. `UniformPrior.logpdf`
  (`uniform.py:124`) calls `message.logpdf` explicitly, and its
  boundary-epsilon nudge operates in *physical* coordinates, so the method
  unambiguously intends physical semantics; every other prior reaches
  `message.logpdf` via `Prior.__getattr__`. Uniform / LogUniform /
  LogGaussian users are silently handed base-space values.
- `MessageInterface.pdf` (`interface.py:45`) — **zero production callers**
  anywhere in `autofit/`; public-API surface only.
- The non-linear search stack never touches message `logpdf` — sampling and
  MCMC/MLE go through `value_for` / `log_prior_from_value` / `factor`, all
  verified correct. Exposure is API-level, not search-level.

**EP-internal callers — all base-space, and mutually consistent:**

- `MeanField.logpdf` / `logpdf_gradient` (`mean_field.py:294,300`), reached
  from `FactorApproximation.__call__` / `func_gradient`
  (`mean_field.py:631-633,647`) by the Laplace optimiser; `MeanField` is
  itself a `Factor` wrapping `_logpdf`, so `projection(mode)` in the
  `from_mode_covariance` `log_norm` calibration (`mean_field.py:404`) and
  `AbstractMessage.__call__`/`factor_jacobian` (`abstract.py:392,398`) route
  the same way.
- This loop is *coherent*, not buggy: a likelihood factor is a density over
  data (measure-free in x), so `fval(x) + Σ log q_base(T(x))` is exactly the
  **base-space tilted log density** at `z = T(x)`. The Laplace mode it finds
  is the base-space tilted mode, and `from_mode` (`transform_jac` +
  `jac.quad`) projects mode and covariance into base space consistently.
  The missing `log_det` is the EP loop's working convention, and base-space
  Laplace is arguably the better-conditioned choice (unbounded support).

**The one genuine cross-convention seam — `PriorFactor`:**

- `PriorFactor` (`declarative/factor/prior.py:23,62`) wraps `prior.factor` —
  the *physical* density — as both its factor callable and its
  `log_likelihood_function`. Its tilted objective under the numerical
  optimiser is therefore
  `log π_base(T(x)) + log_det(x) + Σ log q_base(T(x))` — one x-dependent
  `log_det(x)` *more* than the coherent base-space tilted density (and one
  short of the coherent physical one). Because the #1337 seam strips the
  exact-update hooks (`graphical/README.md` roster row), declarative
  PriorFactors really do take this numerical path: prior-factor EP updates
  optimise a hybrid objective whose mode is neither the base-space nor the
  physical tilted mode.

**Correction to adjudication point 2:** `logpdf_gradient` is *not* a third
convention. Its analytic gradient equals the central-difference derivative
of `logpdf` exactly (−0.520142 both, at the probe point) — the jacobian
multiplication is just the chain rule for the base-space composition
`base.logpdf(T(x))`. So (`logpdf`, `logpdf_gradient`,
`numerical_logpdf_gradient_hessian`) form one self-consistent base-space
family and `factor` is the physical one: **two conventions, not three**.

**New finding:** `TransformedMessage.factor_gradient`
(`composed_transform.py:360-378`) crashes on first call — it unpacks four
values from `_transform_det_jac`, which returns three. Zero production
callers (the `line_search.py` `factor_gradient` is an unrelated
FactorApproximation-level interface). Filed as `bug/priors/16`.

**Recommendation (for the human + #1500 to ratify — not actioned):** the fix
is a two-sided contract repair, not a one-line `logpdf` patch:

1. *EP-internal:* declare base-space `logpdf` the message contract (fix the
   `composed_transform.py` module-docstring claim that `logpdf` accumulates
   the Jacobian) and make `PriorFactor` consume the base-space density
   (`message.logpdf`) instead of `prior.factor`, making the EP loop fully
   base-space coherent. This changes prior-factor updates (removes the
   spurious `log_det`) but preserves the deliberate-looking base-space
   Laplace everywhere else. Belongs with #1500 Q2/Q3.
2. *Public API:* `Prior.logpdf` and `pdf` promise a physical density and
   should route through `factor` (or be renamed/documented). Small,
   standalone, user-facing correctness fix.

The other coherent option — adding `log_det` to `logpdf` itself so
everything is physical — touches every EP path at once and shifts EP Laplace
modes to physical-space MAPs; that is a design change that should only be
taken inside the #1500 single-source-density decision.

## Sequencing

Adjudicate alongside the parked single-source-density design (census C1/C4,
prompts `bug/priors/12`+`13`) — this is a fourth density-convention divergence
of exactly the kind that design exists to eliminate. The 12+13 design issue
should cite PyAutoFit#1498 as fresh evidence.
