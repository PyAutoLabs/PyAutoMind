- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1531 (closed by the PR's `Closes` line)
- completed: 2026-08-27
- pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1532 (MERGED, merge `6e2d8c8`, head `4c0f79b`,
  +167/-20 over 6 files, label `pending-release`)
- summary: `OptimisationState.valid`'s limits guards rewritten from truthiness to `is not None` —
  and, underneath that tidy-up, a **live bug** fixed: `VariableData.any` reduced through `var_all`,
  so the limits check accepted a parameter vector with *some* components out of bounds.
- validation: 2186 passed / 36 skipped (baseline 2178/36); CI green on all four legs.
- release: not performed; merged PR sits in the pending-release queue.
- sibling: shipped in the same PR as `redundant-prior-limits-overrides` — see that record.

## The correction this task was really about

The prompt was filed as `refactor` on the strength of a correction to **PyAutoFit#1527's own
follow-up list**, which described the guard as:

> `line_search.OptimisationState.valid` uses `if self.lower_limit and …`, which is falsy at `0.0`.

That is wrong, and believing it would have produced a bug report for a bug that does not exist.
`self.lower_limit` is not a scalar: it is a `VariableData` (`autofit/mapper/variable.py:309`, a
`Dict[Variable, np.ndarray]` subclass), built by `MeanField.lower_limit` and passed in by
`LaplaceOptimiser` only when `check_limits=True`. Dict truthiness is non-emptiness, so the guard was
`False` only for a model with **no free variables**, where the check is vacuous. There is no `0.0`
for it to be falsy at. And the EP path reads `m.lower_limit` off the **message**, which #1527
deliberately left at `±inf` — so that code saw exactly what it saw before that fix.

What remained was a readability and robustness defect: `if x` *reads* as a scalar test (which is how
it entered the follow-up list as a `0.0` bug) and was one type change away from being one — a scalar
would make `0.0` skip the check, a bare array would raise on the ambiguous truth value.

## The bug underneath it — the actual find

Writing a test for the rewritten guard is what exposed it. `VariableData.any`:

```python
def any(self) -> bool:
    return any(VariableData.var_all(self).values())   # var_all, not var_any
```

It reduced through **`var_all`**, so it meant *"is there a variable whose elements are ALL True"*
rather than *"is ANY element True"*. For `array([True, False])` it answered `False`.

`OptimisationState.valid` asks `(self.parameters < self.lower_limit).any()`. So a parameter vector
with **some** components outside their limits was reported **valid**, and only a variable violating
on **every** component was caught. `MeanField`'s `if valid.any()` (`mean_field.py:501`) under-reported
the same way, inside an EP update loop.

That, not the truthiness guard, is why the Laplace limits check under-enforced. Both fixes shipped
together, because the guard being tidied does not enforce anything without it.

Blast radius, enumerated rather than assumed: the library has six `.any()` call sites. Four
(`graphical/utils.py:539`, `multi_start_gradient/search.py:468`, `analysis/latent.py:274`, plus the
numpy paths) are on numpy arrays and are untouched. The only `VariableData` consumers are
`line_search.py` (×2) and `mean_field.py:501`, and all three want a real `any`.

## The process lesson, paying out a third time in this lineage

`OptimisationState.valid` and `VariableData.any` had **no test coverage at all**. The full 2178-test
suite would have stayed green through any change to either — and did stay green through the bug, for
however long it had been there.

This is the same lesson as `prior-support-clipper` (#1477), where a 1790-test suite passed against an
`LBFGS._fit` that raised `NameError` on every real call, and as `loggaussian-prior-declares-own-support`
(#1527), whose clipper test *asserted the bug as expected behaviour*. Three times in one lineage the
defect was in code nothing executed or nothing asserted about.

The new `test_autofit/graphical/test_optimisation_state_valid.py` (8 tests) is verified by inversion:
reverting `var_any` to `var_all` fails 3 of them, including both partial-violation cases.

## Repos / worktree

- PyAutoFit: `claude/loggaussian-prior-support-ngh59x` (merged, deletable).
- No worktree — ran `web-github` against a direct clone.

## Original prompt

# `OptimisationState.valid` guards on dict truthiness, not on "is a limit set"

Type: refactor
Target: autofit
Repos:
- PyAutoFit
Difficulty: small
Autonomy: safe
Priority: low
Status: formalised
Filed: 2026-08-27
Issued: 2026-08-27

Follow-up owed by `complete/2026/08/loggaussian-prior-declares-own-support.md`
(PyAutoFit#1526 / #1527), which listed it as an open item.

## Correction to the inherited claim — read this first

PyAutoFit#1527's own "Deliberately not done" list says:

> `line_search.OptimisationState.valid` uses `if self.lower_limit and …`, which
> is falsy at `0.0`.

**That characterisation is wrong, and the prompt would be a bug report if it were
right.** `self.lower_limit` is not a scalar. It is a `VariableData`
(`autofit/mapper/variable.py:309`, a `Dict[Variable, np.ndarray]` subclass),
built by `MeanField.lower_limit` (`autofit/graphical/mean_field.py:259`) and
passed in by `LaplaceOptimiser` only when `check_limits=True`
(`autofit/graphical/laplace/optimiser.py:96-99`). Dict truthiness is
non-emptiness, so the guard is `False` only for a model with **no free
variables**, where the check is vacuous anyway. There is no `0.0` for it to be
falsy at, and no prior — LogGaussian included — can make it one.

Worth stating explicitly: the EP/Laplace path reads `m.lower_limit` off the
**message**, and #1527 deliberately left `message.lower_limit` at `±inf`. So
this code sees exactly what it saw before that fix. Nothing about it changed.

## What is actually here

`autofit/graphical/laplace/line_search.py:107-114`:

```python
@property
def valid(self):
    if self.lower_limit and (self.parameters < self.lower_limit).any():
        return False

    if self.upper_limit and (self.parameters > self.upper_limit).any():
        return False

    return True
```

Both attributes default to `None` (`line_search.py:78-79`), so the *intent* of
the guard is plainly "was a limit supplied?" — and `if x` happens to express
that correctly today, by accident of `VariableData` being a dict. It is a
readability and robustness defect, not a live bug:

- It reads as a scalar test to anyone skimming it, which is exactly how it got
  written into #1527's follow-up list as a `0.0` bug.
- It is one type change away from being a real one. If `lower_limit` ever
  becomes an array, `if self.lower_limit` raises
  `ValueError: truth value of an array with more than one element is ambiguous`;
  if it becomes a scalar, the `0.0` bug #1527 described becomes real.

## The fix

Replace both guards with `is not None`, and add a short comment saying the
attributes are `VariableData` keyed by free variable, `None` when
`check_limits=False`.

## Verify

- `valid` returns the same answer for every case the suite already covers —
  this is behaviour-preserving by construction, since the only truthiness case
  that differs is the empty `VariableData`, where both comparison expressions
  are vacuously `False` and the property returns `True` either way.
- A `LaplaceOptimiser(check_limits=True)` EP run is unchanged.
- Confirm no other call site constructs `OptimisationState` with a scalar or
  bare-array `lower_limit` (`grep -rn "lower_limit" autofit/graphical/` had one
  producer at the time of filing, `optimiser.py:98`).

## Scope note

Do **not** widen this into "make EP read the prior's declared support instead of
the message's". That is the separate, deliberately-rejected question in
`draft/research/graphical_ep/transformed_message_declares_support.md`.

## Status 2026-08-27 — implemented, pushed, not yet PR'd

Both this and its sibling `redundant_prior_limits_overrides.md` were implemented
together on PyAutoFit branch `claude/loggaussian-prior-support-ngh59x`, commit
`4c0f79b` — one coherent change (the limits cleanup #1527 left behind) rather
than two PRs, which departs from "one prompt = one task = one PR" deliberately
and is worth splitting if a reviewer prefers.

Full suite **2186 passed / 36 skipped** (baseline 2178/36, +8 new tests).
No PR opened.

**A live bug turned up inside this work.** `VariableData.any` reduced through
`var_all`, so it answered "is there a variable whose elements are ALL True"
rather than "is ANY element True". `OptimisationState.valid` asks
`(parameters < lower_limit).any()`, so a parameter vector with *some* components
outside their limits was reported **valid** — only a variable violating on every
component was caught. `MeanField`'s `valid.any()` under-reported the same way.
Fixed in the same commit; the other four `.any()` call sites in the library are
numpy arrays and are untouched.

That bug, not the truthiness guard, is why the limits check under-enforced. This
prompt's own framing (a readability defect) was right about the guard and missed
the real one underneath it — found only because the guard rewrite needed a test
and `OptimisationState.valid` had **no test coverage at all**.
