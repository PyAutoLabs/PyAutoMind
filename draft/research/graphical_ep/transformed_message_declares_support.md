# Should `TransformedMessage` carry its own support, rather than the prior?

Type: research
Target: graphical_ep
Repos:
- PyAutoFit
Themes:
- graphical-ep
Difficulty: medium
Autonomy: human-required
Priority: low
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: never
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

## Measured 2026-08-27 — question 1 is answered: EP is NOT wrong today

Run against a live 3.12 install on PyAutoFit `main`. The two layers do disagree,
exactly as described above:

```
prior.lower_limit    = 0.0     (declared by #1527)
prior.limits         = (0.0, inf)
message.lower_limit  = -inf    (deliberately left)
MeanField.lower_limit -> {LogGaussianPrior: -inf}   # what OptimisationState gets
```

So `OptimisationState.valid` does **not** enforce LogGaussian's support: with
`params = -1.0`, `(params < MeanField.lower_limit).any()` is `False` and `valid`
returns `True`, for a value whose prior density is `-inf`.

**But the message's own density already rejects it, cleanly:**

| value | `message.logpdf` | `prior.log_prior_from_value` |
|---|---|---|
| `-1.0` | `-inf` | `-inf` |
| `-1e-9` | `-inf` | `-inf` |
| `0.0` | `-1.798e308` | `-inf` |
| `1e-9` | `-133.19` | `-111.29` |
| `1.0` | `-1.229` | `-0.047` |

No `NaN` — which was the failure mode worth fearing, since a `log` of a negative
value could have produced one and poisoned the EP objective silently. It does
not. The limits check is **redundant for this prior, not load-bearing**, and EP
is not producing wrong results today because of the divergence.

### What that does to this task

It drops the priority. There is no live incorrectness to fix, so this stays what
the title says — a design question about which layer should own the support —
and not a bug. Two things are still worth someone's attention:

- ~~**`message.logpdf(0.0)` is `-1.798e308`, not `-inf`**~~ — **FIXED 2026-08-27**,
  PyAutoFit#1534 (record `complete/2026/08/natural-logpdf-clamps-neginf.md`). It
  was not harmless: `natural_logpdf` called `nan_to_num` with `nan=-inf` but
  default `neginf`, so a genuine `-inf` was clamped to negative float max — and
  `isfinite` is what `optax.apply_if_finite` and `non_linear/clipper.py` branch
  on. `message.logpdf(0.0)` is now `-inf`, matching the prior.

  **This changes the measurements above.** The table's `0.0` row read
  `-1.798e308` when it was taken; on `main` from `5c391fd` it reads `-inf`. The
  conclusion is unaffected — EP was already protected by the message returning a
  clean `-inf` at *negative* values, which is the row that mattered — but re-run
  the probe rather than trusting the printed `0.0` entry.
- The redundancy is now *documented* rather than latent, which was most of the
  hazard. Whoever picks this up starts from the table above.

Remaining open: questions 2 and 3 (which layer should own it; the EP regression
surface). Question 1 is closed.
