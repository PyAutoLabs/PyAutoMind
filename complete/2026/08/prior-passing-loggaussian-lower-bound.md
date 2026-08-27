- issue: none — investigated and closed without one
- completed: 2026-08-27
- pr: none; **no code change was required**
- summary: NULL RESULT. Spot-check owed by PyAutoFit#1527, which changed the
  prior-passing fallback for `LogGaussianPrior` and flagged PyAutoGalaxy /
  PyAutoLens as worth checking. Neither repo constructs a `LogGaussianPrior`
  anywhere, so there is no exposure. Filed and closed the same day.
- validation: grep over fresh shallow clones (PyAutoGalaxy `05e5d13`, PyAutoLens
  same date) across `*.py`, `*.yaml`, `*.yml`, `*.json` and every other tracked
  file type.

## What was checked, and what it found

PyAutoFit#1527 made `LogGaussianPrior` report `(0.0, inf)` instead of
`(-inf, inf)`. That is downstream-visible in exactly one place:
`AbstractPriorModel.mapper_from_prior_means` falls back to `prior.limits` when
the priors config has no `Limits` entry for a parameter
(`autofit/mapper/prior_model/abstract.py:1153`), then builds
`TruncatedGaussianPrior(mean, sigma, *limits)`. Before the fix that produced a
prior which samples negative values for a strictly positive parameter; after it,
a lower-bounded one — a correctness fix that nonetheless **changes the unit-cube
mapping** of the passed prior.

The only occurrence of the name in either repo is an API-docs autosummary entry:

- `pyautogalaxy/docs/api/modeling.rst:57`
- `pyautolens/docs/api/modeling.rst:56`

Zero hits in source, zero in any priors config. Configured prior families:

| repo | configured `type:` values |
|---|---|
| PyAutoGalaxy | Absolute 420, Relative 277, Uniform 268, Gaussian 238, TruncatedGaussian 96, LogUniform 93, Constant 42 |
| PyAutoLens | Absolute 123, Uniform 101, Relative 73, Gaussian 62, TruncatedGaussian 26, LogUniform 23 |

`Absolute` / `Relative` are width modifiers, not prior families.

## Why that is conclusive rather than suggestive

`LogGaussianPrior` is the **only** prior whose `limits` #1527 changed. `Uniform`,
`LogUniform` and `TruncatedGaussian` already reported their real bounds and were
measured byte-identical across the change; `Gaussian` still reports
`(-inf, inf)`. So the fallback cannot return a changed value for any prior either
repo actually uses. No inter-phase prior-passing result moves.

## When to re-run this

Only if either repo starts using `LogGaussianPrior`. At that point the parameter
either gets a `Limits` entry in the priors config (which wins over
`prior.limits`, so nothing changes) or lands on the now-correct lower-bounded
fallback — which is the desired behaviour, not a regression.

## Note on the record

A null result recorded explicitly is the deliverable here. The alternative — a
prompt quietly retired because "nothing was found" — leaves the next reader
unable to tell a completed check from an abandoned one.

## Original prompt

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

## Result 2026-08-27 — NULL RESULT, no exposure

Checked against fresh shallow clones of both repos
(PyAutoGalaxy `05e5d13`, PyAutoLens at the same date).

**Neither repo constructs a `LogGaussianPrior` anywhere.** The only occurrence of
the name in either tree is an autosummary listing in the API docs:

- `pyautogalaxy/docs/api/modeling.rst:57`
- `pyautolens/docs/api/modeling.rst:56`

Zero hits in source (`--include=*.py`) and zero in any priors config
(`*.yaml` / `*.yml` / `*.json`). The prior types actually configured are:

| repo | configured `type:` values |
|---|---|
| PyAutoGalaxy | Absolute 420, Relative 277, Uniform 268, Gaussian 238, TruncatedGaussian 96, LogUniform 93, Constant 42 |
| PyAutoLens | Absolute 123, Uniform 101, Relative 73, Gaussian 62, TruncatedGaussian 26, LogUniform 23 |

(`Absolute` / `Relative` are width modifiers, not prior families.)

`LogGaussianPrior` is the **only** prior whose `limits` PyAutoFit#1527 changed —
`Uniform`, `LogUniform` and `TruncatedGaussian` were already truthful and
`Gaussian` still reports `(-inf, inf)`. So the prior-passing fallback at
`autofit/mapper/prior_model/abstract.py:1153` cannot reach a changed value from
either repo, and there is no inter-phase prior-passing exposure to check.

**This task is done. Retire it.** The check is worth re-running only if either
repo starts using `LogGaussianPrior` — at which point the parameter would need a
`Limits` entry in the priors config, or it lands on the (now correct)
lower-bounded fallback.
