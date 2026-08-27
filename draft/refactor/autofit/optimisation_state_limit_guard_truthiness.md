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
