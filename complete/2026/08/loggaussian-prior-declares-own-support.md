- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1526 (closed by the PR's `Closes` line)
- completed: 2026-08-25
- pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1527 (MERGED, merge `34d6dff`, head `c3505d1`,
  +276/-34 over 6 files, label `pending-release`)
- summary: `LogGaussianPrior` now declares its own `(0, inf)` support instead of delegating a wrong
  `(-inf, inf)` to a `TransformedMessage` that was never given limits. `Prior` gains a general
  strictness contract (`lower_limit_strict` / `upper_limit_strict`) so a consumer can tell an
  *exclusive* bound from an inclusive one without a type switch, and `Prior.limits` is now derived
  from `lower_limit`/`upper_limit` rather than hardcoded — the actual root cause of the bug class.
  `ClipperPriorBox`'s `isinstance(prior, LogGaussianPrior)` workaround, its import and its
  workaround docstrings are retired. This is follow-up 3 owed by
  `complete/2026/08/prior-support-clipper.md` (PyAutoFit#1477).
- validation: full suite 2178 passed / 36 skipped (baseline on `main`: 2124 / 36).
- release: not performed; the merged PR sits in the pending-release queue.

> **RECORD WRITTEN LATE, 2026-08-27.** The code shipped 2026-08-25 but the Mind-side close-out
> never landed: that session's PyAutoMind branch (`claude/loggaussian-prior-support-buv5xe` @
> `5dfffb4c3`) was condemned the same day and archived to
> `archive/condemned/pyautomind-loggaussian-prior-support-buv5xe` (see `condemned.md`). The prompt
> was therefore still sitting in `draft/bug/autofit/`, rendering on the dashboard as pickable
> backlog, and a `/start_dev` run on 2026-08-27 rediscovered the work already merged. This record
> and the `draft/ → complete/` move are that close-out, reconstructed from PyAutoFit#1526/#1527 and
> from `main` itself. Nothing in PyAutoFit was changed to write it.

## What shipped

| File | Change |
|---|---|
| `autofit/mapper/prior/abstract.py` | `Prior.lower_limit_strict` / `upper_limit_strict` class attributes (both `False`); `Prior.limits` derived from `lower_limit`/`upper_limit` |
| `autofit/mapper/prior/log_gaussian.py` | `lower_limit_strict = True`; `__init__` sets `self.lower_limit = 0.0`, `self.upper_limit = inf` |
| `autofit/non_linear/clipper.py` | `_limits_from_model` reads the strictness flags; `isinstance` block, `LogGaussianPrior` import and workaround docstrings gone |
| `test_autofit/mapper/prior/test_log_gaussian.py` | +128: reported support, strictness, regression pins |
| `test_autofit/mapper/prior/test_prior_properties.py` | +80: property P6 over every prior family |
| `test_autofit/non_linear/test_clipper.py` | the test that **asserted the bug** rewritten |

## The design decision worth remembering: on the prior, never on the message

The prompt offered two routes — "pass the limits into the `TransformedMessage`, or override
`lower_limit`". Only the second is viable, and the reason is not stylistic:

- Limits set on the message are **dropped** by `with_base`, `copy`, `project` and `__call__`.
- They would change what `MeanField.lower_limit` and `LaplaceOptimiser(check_limits=True)` feed to
  `OptimisationState.valid` — a live EP/Laplace behaviour change, well outside a bug fix.

So `message.lower_limit` is deliberately left at `±inf` and the declaration is shadowed on the
prior instance. That is why the EP machinery sees exactly what it saw before.

The second half of the fix is the one that stops this recurring: **`Prior.limits` used to be a
hardcoded `(-inf, inf)`** for every prior that did not override it. Two notions of "support" that
can disagree by construction is the bug class; deriving one from the other closes it.

## The general test is the deliverable, not the fix

`test_prior_properties.py` P6 asserts, parametrised over **every** prior family, that

- `log_prior_from_value` is finite strictly inside the *reported* `limits`,
- `-inf` outside them, and
- `-inf` *at* a bound flagged strict, finite at one that is not.

It **fails on the parent commit for `LogGaussianPrior` alone** and passes for the other five
families — i.e. it is the general form of the bug, not a restatement of the fix. That check is what
would have caught this in #1477, and it is what will catch the next prior that misreports.

## Measured: 34 of 37 probes identical

Before/after over 37 behavioural probes against a running 3.12 install. The three that moved are
`lower_limit` under `copy`, `pickle` and `project` — the fix itself.

| Probe | Result |
|---|---|
| `Identifier(prior)` + full `description` | byte-identical — **no output directories re-key** |
| `Identifier(LBFGS(clipper=ClipperPriorBox()))` | byte-identical |
| `log_prior_from_value` at 11 points either side of `0` | pointwise identical |
| `value_for`, `unit_value_for` round-trip, `Model.vector_from_unit_vector` | identical over a 10-point unit grid |
| `ClipperPriorBox` bounds / projections / clipped-masks | identical, 3 clipper configs × 3 input vectors |
| `message.lower_limit` (what EP/Laplace read) | unchanged at `±inf` |
| `Gaussian` / `Uniform` / `LogUniform` / `TruncatedGaussian` limits | unchanged |

The identifier result is the one to note. The prompt flagged re-keying as the main hazard, citing
the clipper-identifier decision of 2026-08-18 (`complete/2026/08/clipper-in-search-identifier.md`),
which chose to re-key and orphan stored results. **This change did not have to make that trade**:
`__identifier_fields__ = ("mean", "sigma")` gates it, and the strictness flags are *class*
attributes, so they stay out of `__dict__` and out of the hash. Declaring a derived constant on a
prior is identifier-safe; adding an instance attribute inside `__identifier_fields__` would not be.

## The one thing that DID change downstream — prior passing

Where a model's config supplies no `Limits` entry for a LogGaussian parameter,
`AbstractPriorModel` falls back to `prior.limits`:

| | before | after |
|---|---|---|
| passed prior | `TruncatedGaussian(1.0, 0.5, -inf, inf)` | `TruncatedGaussian(1.0, 0.5, 0.0, inf)` |
| `value_for(0.001)` | **`-0.545`** | `0.0089` |
| `log_prior_from_value(-1.0)` | **`-8.0`** (finite) | `-inf` |

A strictly positive parameter was being passed a prior that samples negative values. The fix is a
correctness fix, but it **changes the unit-cube mapping of the passed prior** — inter-phase prior
passing in PyAutoGalaxy / PyAutoLens is worth a spot-check, and that spot-check was not done as
part of #1527.

## Follow-ups still open

1. **`OptimisationState.valid`'s truthiness guard** — `line_search.py:107-114` uses
   `if self.lower_limit and …`. Filed as
   `draft/refactor/autofit/optimisation_state_limit_guard_truthiness.md`.

   **#1527's own description of this one is wrong, and the correction is the useful part.** Its
   follow-up list calls the guard "falsy at `0.0`", implying the fix above silently disabled a
   limit check for exactly the prior it gave a `0.0` lower limit. It did not. `self.lower_limit`
   is a `VariableData` (`autofit/mapper/variable.py:309`, a `Dict` subclass) built by
   `MeanField.lower_limit` and passed only when `check_limits=True`; dict truthiness is
   non-emptiness, so the guard is `False` only for a model with no free variables, where the check
   is vacuous. There is no `0.0` for it to be falsy at. And the EP path reads `m.lower_limit` off
   the **message**, which this task deliberately left at `±inf` — so that code sees exactly what
   it saw before. What remains is a readability/robustness defect: the guard reads as a scalar
   test (which is how it entered the follow-up list as a bug) and is one type change away from
   being one.
2. **Three redundant `limits` overrides.** `UniformPrior`, `LogUniformPrior` and
   `TruncatedGaussianPrior` now duplicate the base implementation exactly — except that the base
   coerces with `float()` and they do not, so deletion is a type change, not a no-op. Filed as
   `draft/refactor/autofit/redundant_prior_limits_overrides.md`.
3. **Declaring limits on `TransformedMessage`.** Rejected here for the EP reasons above. The
   residue is that the prior and its message now deliberately disagree about the support. Filed as
   `draft/research/graphical_ep/transformed_message_declares_support.md`.
4. **Downstream prior-passing spot-check** in PyAutoGalaxy / PyAutoLens, per the section above.
   Filed as `draft/test/autogalaxy/prior_passing_loggaussian_lower_bound.md`.

All four were filed as prompts on 2026-08-27, alongside this record, and worked the
same day:

- **1 and 2 implemented together** on PyAutoFit `claude/loggaussian-prior-support-ngh59x`
  (`4c0f79b`, suite 2186/36 vs baseline 2178/36). No PR opened yet.
- **Doing 1 exposed a live bug neither #1527 nor the prompt saw.** `VariableData.any`
  reduced through `var_all`, so it meant "is there a variable whose elements are ALL
  True" rather than "is ANY element True". `OptimisationState.valid` asks
  `(parameters < lower_limit).any()` — so a parameter vector with *some* components
  outside their limits was reported **valid**, and `MeanField`'s `valid.any()`
  under-reported the same way. Fixed in the same commit. That, not the truthiness
  guard, is why the limits check under-enforced; it surfaced only because rewriting
  the guard needed a test and `OptimisationState.valid` had **no coverage at all** —
  the #1477 process lesson, third time it has paid out in this lineage.
- **3 partly answered.** EP's `check_limits` path genuinely does not enforce
  LogGaussian's support (it reads the message's `-inf`), but the message's own density
  returns a clean `-inf` at negative values — no `NaN` — so EP is not producing wrong
  results today. The check is redundant for this prior, not load-bearing. Measurements
  appended to the prompt; the design question stays open at lower priority.
- **4 done, null result** — `complete/2026/08/prior-passing-loggaussian-lower-bound.md`.
  Neither PyAutoGalaxy nor PyAutoLens constructs a `LogGaussianPrior`, so the
  prior-passing change has no downstream exposure.

## Repos / worktree

- PyAutoFit: `feature/loggaussian-prior-support` (merged, deletable).
- No worktree — the implementing session ran `web-github` against a direct clone.
- PyAutoMind: the implementing session's branch was condemned before its Mind state merged; this
  record was written on `claude/loggaussian-prior-support-ngh59x` two days later.

## The process lesson: a condemned Mind branch orphans the close-out silently

The code half of this task shipped cleanly and the Mind half vanished with the branch. Nothing
detected it: `dashboard.md` self-heals its *render*, and a prompt that shipped but was never
retired renders faithfully as pickable backlog — no workflow can tell the difference. The drift
surfaced only because `/start_dev` was pointed at the prompt again and the session checked the
tracker before filing a duplicate issue.

Two cheap habits fall out of that. **Check the issue tracker and the target repo's `main` before
filing** — start_dev's resume check reads `active.md`, which by construction cannot know about a
close-out that never merged. And when condemning a branch, **check whether it carried Mind state
that has no other home**; `condemned.md` recorded the branch faithfully, but "what was lost with
it" is not a field it has.

## Original prompt

# `LogGaussianPrior` misreports its own support as `(-inf, inf)`

Type: bug
Target: autofit
Repos:
- PyAutoFit
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised
Filed: 2026-08-16 (backfilled from git)
Issued: 2026-08-25

Filed 2026-08-16. Follow-up 3 owed by the prior-support `Clipper`
(`complete/2026/08/prior-support-clipper.md`, PyAutoFit#1477), which worked
around it rather than fixing it.

## The defect

`LogGaussianPrior`'s support is `(0, inf)` — `log_prior_from_value` returns
`-inf` for `value <= 0`. But its `TransformedMessage` defaults its limits to
`±inf` and is never passed any, so the prior **reports** `(-inf, inf)`.

Every other prior answers `lower_limit` / `upper_limit` truthfully via
`Prior.__getattr__` delegating to the message, which is why the `Clipper` needs
no type switch anywhere else. This one prior is the exception, and it is the
kind of exception that is invisible until something trusts the answer.

## Why it matters now

`ClipperPriorBox` **declares the real support in the clipper** rather than on
the prior — deliberately, to avoid touching a shared class late in that task,
and recorded as a follow-up rather than left silent. That special case is
correct but misplaced: any future consumer of `lower_limit` gets the wrong
answer unless it also knows to special-case this prior.

The general hazard: a bound of `-inf` on a strictly positive parameter means a
consumer will not guard `0`, and `log(0)` / a division by it is the failure that
follows.

## The fix

Declare the support on `LogGaussianPrior` itself — pass the limits into the
`TransformedMessage`, or override `lower_limit` — then retire the clipper's
special case and its accompanying comment.

## The care needed — why this is `supervised` and not `safe`

Changing what a prior reports as its support is not local:

- **The nested samplers work in unit-cube coordinates** and map through the
  prior. Confirm a limits change does not alter that mapping, or every stored
  nested-sampling result shifts.
- **`log_prior_from_value` must not change behaviour.** It is already correct;
  only the *reported* limits are wrong. If the fix changes the density anywhere,
  it has gone too far.
- **Check the identifier.** If `lower_limit` feeds the search identifier, a
  change re-keys existing output directories and orphans stored results — the
  same class of concern as the clipper identifier decision, which chose to
  re-key and orphan rather than special-case (2026-08-18; record
  `complete/2026/08/clipper-in-search-identifier.md`).

## Verify

- `LogGaussianPrior(...).lower_limit == 0.0` (or whatever exclusive convention
  is chosen — state it).
- `log_prior_from_value` is unchanged across a range of values either side of
  zero, asserted against the pre-change values.
- `ClipperPriorBox.bounds_from_model` returns the same bounds for a model
  containing a `LogGaussianPrior` **after** the clipper's special case is
  removed as it did before — that equivalence is the whole point of the change.
- A nested-sampler unit-cube round-trip through the prior is unchanged.

<!-- Grounding: recorded as trap 3 and follow-up 3 in
     complete/2026/08/prior-support-clipper.md, measured against a running
     install during PyAutoFit#1477. -->
