- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1533 (closed by the PR's `Closes` line)
- completed: 2026-08-27
- pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1534 (MERGED, merge `5c391fd`, head `1e3b1a0`,
  +90/-1 over 2 files, label `pending-release`)
- summary: `AbstractMessage.natural_logpdf` clamped a genuine `-inf` to `-1.8e308` because
  `nan_to_num` was called with `nan=-inf` but default `posinf`/`neginf`. Fixed by passing all
  three, so only `NaN` is replaced.
- validation: 2203 passed / 36 skipped; baseline measured on the branch point `6e2d8c8` with
  changes stashed, 2190 / 36. CI green on all four legs.
- release: not performed; merged PR sits in the pending-release queue.
- origin: the loose end noted in `complete/2026/08/optimisation-state-limit-guard-truthiness.md`
  and in PyAutoFit#1532's Shipped comment, filed and shipped the same day.

## The defect

`autofit/messages/interface.py:98`:

```python
return xp.nan_to_num(log_base + eta_t - log_partition, nan=-xp.inf)
```

`nan=-xp.inf` is deliberate — an out-of-support `NaN` is zero density. But `posinf`/`neginf` were
left at their defaults, and `np.nan_to_num` replaces `-inf` with `-sys.float_info.max`. So the call
did the **opposite of its intent for the inputs that already had the right answer**:

| value reaching the reduction | intended | actual |
|---|---|---|
| `NaN` | `-inf` | `-inf` |
| `-inf` | `-inf` | `-1.7976931348623157e+308` |

## What made it findable: the asymmetry is the proof

`LogGaussianPrior(0.4, 1.3)` on `main` @ `6e2d8c8`:

```
message.logpdf(-1.0) = -inf                       # log(-1) is NaN -> nan=-inf applies
message.logpdf( 0.0) = -1.7976931348623157e+308   # log(0) is -inf -> default neginf clamps
```

Two out-of-support points, two different answers, from one line. That asymmetry names the mechanism
without needing to read the reduction — and the clamped value being *exactly* `-sys.float_info.max`
confirms it, since that is `nan_to_num`'s documented default and nothing else in the stack produces
it. `UniformPrior` and `LogUniformPrior` return `-inf` correctly, so the bug is invisible unless the
expression reaches `-inf` rather than `NaN`.

## Why a finite value there is not cosmetic

`-1.8e308` is **finite**, and `isfinite` is the branch:

- `optax.apply_if_finite` — the mechanism `autofit/non_linear/clipper.py` exists to exploit. That
  module's opening docstring says a step leaving the box "makes the objective non-finite". For a
  `LogGaussianPrior` landing exactly on `0.0`, it did not.
- Two such terms summed overflow to `-inf`; one does not. So the behaviour depended on *how many*
  parameters were out of support — the kind of dependence that makes a bug look like a flake.

## Deliberately left alone

`TruncatedGaussianPrior`'s **message** returns finite `logpdf` well outside its limits (`-8.20` at
`-1.0` for a `(0, 3)` support). Separate looseness in `TruncatedNormalMessage`, not this clamp; the
prior-level `log_prior_from_value` is correct there, which is why the P6 property tests pass. The
new general-property test **excludes it with a comment saying why**, rather than quietly asserting
something weaker across all families so it would pass. Unfiled.

## Process note: three stale-API misreadings in one session

Worth recording because it cost more time than the fix did. GitHub's `pull_request` check endpoints
served stale data repeatedly, and I misread it three times:

1. On PyAutoFit#1532, `get_check_runs` reported two legs `in_progress` for ~50 minutes after they
   had finished in ~4. Reported as a stall; wrong.
2. On PyAutoMind#350, `get_check_runs` reported `total_count: 0` indefinitely. Reported as "no CI
   configured" and escalated to the human; the workflows had in fact run and passed.
3. On this PR, `list_workflow_jobs` showed one leg complete and two mid-`Run tests` — which I argued
   was *therefore* fresh and trustworthy, and used to diagnose a hang and name my own change as the
   likely cause. It was a stale snapshot caught mid-run; all three passed in under four minutes.

The reliable read is `list_workflow_jobs` **with per-step `completed_at` timestamps**, and the
tell is the timestamps themselves: a job showing `in_progress` whose sibling steps completed an hour
of wall-clock ago is a stale snapshot, not a hang. Compare the reported step start against the
elapsed real time before concluding anything.

## Repos / worktree

- PyAutoFit: `claude/loggaussian-prior-support-ngh59x` (merged, deletable).
- No worktree — `web-github` against a direct clone.

## Original prompt

# `natural_logpdf` clamps a genuine `-inf` to `-1.8e308`

Type: bug
Target: priors
Repos:
- PyAutoFit
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised
Filed: 2026-08-27
Issued: 2026-08-27

Loose end from PyAutoFit#1532 (`complete/2026/08/optimisation-state-limit-guard-truthiness.md`),
noted there and not filed at the time.

## The defect

`AbstractMessage.natural_logpdf` (`autofit/messages/interface.py:98`):

```python
return xp.nan_to_num(log_base + eta_t - log_partition, nan=-xp.inf)
```

It passes `nan=-xp.inf` — deliberate, mapping an out-of-support NaN to zero density —
but leaves `posinf`/`neginf` at their **defaults**. `np.nan_to_num`'s default replaces
`-inf` with `-1.7976931348623157e+308` (negative float max).

So the call does exactly the opposite of what it intends for half its inputs:

| expression value | intent | actual |
|---|---|---|
| `NaN` | `-inf` | `-inf` ✅ |
| `-inf` | `-inf` | **`-1.8e308`** ❌ |

A genuine zero-density point is turned into a *finite* number.

## Measured on `main` @ `6e2d8c8`

`LogGaussianPrior(0.4, 1.3)`:

| value | `message.logpdf` | `prior.log_prior_from_value` |
|---|---|---|
| `-1.0` | `-inf` | `-inf` |
| `0.0` | **`-1.7976931348623157e+308`** | `-inf` |

The asymmetry is the proof of mechanism: at `-1.0` the log transform gives `log(-1) = NaN`,
which `nan=-inf` correctly maps; at `0.0` it gives `log(0) = -inf`, which the default
`neginf` clamps. Confirmed equal to `-sys.float_info.max` exactly.

`UniformPrior` / `LogUniformPrior` return `-inf` correctly outside their boxes, so this is
not visible for every family — it needs an expression that reaches `-inf` rather than `NaN`.

## Why it matters

`-1.8e308` is **finite**, and a lot of this codebase branches on exactly that:

- `np.isfinite(logpdf)` is `True` at a point of zero density.
- `optax.apply_if_finite` — the mechanism `autofit/non_linear/clipper.py` is built around —
  would fire differently. That module's whole premise is that leaving the support makes the
  objective non-finite.
- Two such terms summed overflow to `-inf`, one does not, so the behaviour depends on how
  many parameters are out of support.

## The fix

Preserve the infinities and replace only `NaN`:

```python
return xp.nan_to_num(
    log_base + eta_t - log_partition, nan=-xp.inf, neginf=-xp.inf, posinf=xp.inf
)
```

## Verify

- `LogGaussianPrior(0.4, 1.3).message.logpdf(0.0) == -inf`.
- `logpdf` unchanged at in-support points, pinned against pre-change values across every
  prior family.
- `log_prior_from_value` unchanged everywhere — it was already correct and must stay so.
- The JAX path agrees with the NumPy path (`jnp.nan_to_num` takes the same keywords).

## Deliberately out of scope

`TruncatedGaussianPrior`'s **message** returns finite `logpdf` well outside its limits
(`-8.20` at `-1.0` for a `(0, 3)` support). That is a separate looseness in
`TruncatedNormalMessage`, not this clamp — the prior-level `log_prior_from_value` is correct
there, which is why the P6 property tests pass. File separately if it matters.
