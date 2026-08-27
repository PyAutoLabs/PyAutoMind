# Should `TransformedMessage` carry its own support, rather than the prior?

Type: research
Target: graphical_ep
Repos:
- PyAutoFit
Difficulty: medium
Autonomy: human-required
Priority: low
Status: formalised
Filed: 2026-08-27

Follow-up owed by `complete/2026/08/loggaussian-prior-declares-own-support.md`
(PyAutoFit#1526 / #1527), which **rejected** this route and shadowed the limits
on the prior instead. This prompt is the open question, not a plan to reverse
that decision.

## Why #1527 did not do it

`LogGaussianPrior` reported `(-inf, inf)` because its `TransformedMessage`
defaults its limits to `±inf` and was never passed any. The obvious fix — pass
the real limits into the message — was rejected for two measured reasons:

1. **They do not survive the message lifecycle.** Limits set on the message are
   dropped by `with_base`, `copy`, `project` and `__call__`. A prior that
   declared its support that way would lose it on the first projection.
2. **It is a live EP behaviour change.** `MeanField.lower_limit`
   (`autofit/graphical/mean_field.py:259`) reads `m.lower_limit` off each
   message and hands it to `OptimisationState.valid` via
   `LaplaceOptimiser(check_limits=True)`
   (`autofit/graphical/laplace/optimiser.py:96-99`). Giving a `TransformedMessage`
   a real `(0, inf)` support would start rejecting EP/Laplace states that are
   accepted today — well outside a bug fix, and unmeasured.

So #1527 set `self.lower_limit = 0.0` on the prior instance and left
`message.lower_limit` at `±inf`. #1527 verified that choice keeps EP/Laplace
seeing exactly what it saw before.

## The question this leaves open

The organism now has **two notions of support that deliberately disagree**: the
prior says `(0, inf)`, its message says `(-inf, inf)`. That is a correct
resolution of a scope problem, not a correct end state — it is the same shape of
divergence as the `Prior.limits`-vs-`lower_limit` split that #1527 closed, one
layer down.

Worth answering, in this order:

1. **Is `check_limits=True` EP actually wrong today** for a model carrying a
   `LogGaussianPrior`? It accepts states with a negative value for a strictly
   positive parameter. Does that produce a bad fit, or does the factor's own
   `-inf` density reject it downstream anyway? Measure before designing.
2. If it is wrong, **which layer should own the support** — the message (fixing
   the lifecycle drops in `with_base` / `copy` / `project` / `__call__` first),
   or `MeanField.lower_limit` reading through to the prior?
3. What is the EP regression surface? Any change here re-keys nothing but can
   change which states `OptimisationState.valid` rejects, and therefore where a
   Laplace optimisation lands.

## Related

- `active/13_collapse_prior_and_message.md` — the standing task on the
  Prior/Message split this sits inside. Read it first; this may be a sub-question
  of it rather than its own task.
- `complete/2026/08/transformed-message-semantics-doc.md`.
