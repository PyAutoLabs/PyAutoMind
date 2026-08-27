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
