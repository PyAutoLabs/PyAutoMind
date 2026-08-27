# Spot-check downstream prior passing after `LogGaussianPrior` gained a `0.0` lower limit

Type: test
Target: autogalaxy
Repos:
- PyAutoGalaxy
- PyAutoLens
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised
Filed: 2026-08-27

Follow-up owed by `complete/2026/08/loggaussian-prior-declares-own-support.md`
(PyAutoFit#1526 / #1527). That PR named the spot-check and **did not do it**.

## The change that reaches downstream

PyAutoFit#1527 is behaviour-preserving everywhere except one path, which it
measured and flagged. `AbstractPriorModel.mapper_from_prior_means` falls back to
`prior.limits` when the priors config supplies no `Limits` entry for a parameter
(`autofit/mapper/prior_model/abstract.py:1147-1156`), then constructs
`TruncatedGaussianPrior(mean, sigma, *limits)`.

For a LogGaussian parameter with no config `Limits` entry:

| | before #1527 | after #1527 |
|---|---|---|
| passed prior | `TruncatedGaussian(1.0, 0.5, -inf, inf)` | `TruncatedGaussian(1.0, 0.5, 0.0, inf)` |
| `value_for(0.001)` | **`-0.545`** | `0.0089` |
| `log_prior_from_value(-1.0)` | **`-8.0`** (finite) | `-inf` |

The old behaviour was a strictly positive parameter being passed a prior that
samples negative values, so this is a correctness fix. But it **changes the
unit-cube mapping of the passed prior**, and a changed unit-cube mapping is a
changed inter-phase result.

Note what is *not* at risk, so the check stays scoped: identifiers are
byte-identical (`__identifier_fields__ = ("mean", "sigma")` gates them), the
density is pointwise identical, and the direct (non-passed) unit-cube mapping is
identical over a 10-point grid. #1527 measured all three. Only **prior passing**
moved.

## What to check

1. **Does any PyAutoGalaxy / PyAutoLens model actually use `LogGaussianPrior`?**
   Grep the config trees (`config/priors/**`) and the pipeline/search-chaining
   code. If the answer is no, the task is done — record that and retire it. Do
   not skip this step; it is most of the value here.
2. If yes, **does the priors config supply a `Limits` entry** for those
   parameters? A config `Limits` entry wins over `prior.limits`, so a configured
   parameter is unaffected. Only the unconfigured ones changed.
3. For any parameter that reaches the fallback, confirm the new lower-bounded
   passed prior is what the science wants — it should be, since the parameter is
   strictly positive, but confirm rather than assume.

## Verify

- An inter-phase prior-passing run (a search-chaining example touching a
  LogGaussian parameter) completes and produces a passed prior whose
  `lower_limit` is `0.0`, with no negative draws.
- State explicitly in the completion record which repos, configs and parameters
  were checked, and whether any were affected — a null result here is the useful
  answer and should be recorded as one, not left implicit.

## Environment note

Neither repo was attached when this prompt was filed; the grounding above is from
PyAutoFit `main` and from PyAutoFit#1527's measurements. Attach PyAutoGalaxy and
PyAutoLens before starting.
