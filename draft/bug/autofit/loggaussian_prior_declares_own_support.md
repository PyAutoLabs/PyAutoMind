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
