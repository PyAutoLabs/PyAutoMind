# Adapt-density mapper: a zero-signal adapt image is NaN on the JAX path and finite on NumPy

Type: bug
Target: PyAutoArray
Repos:
- PyAutoArray
- autolens_workspace_test
Difficulty: small
Autonomy: safe
Priority: medium
Status: formalised
Filed: 2026-09-06

Found during the phase-6 rebuild of the ci-timing-fast-tests epic
(autolens_workspace_test#293 / #294). In
`scripts/interferometer/jax_likelihood/rectangular.py` an adapt image was built
from the *unlensed* true source profile evaluated on the image-plane grid — a
compact blob sitting where the Einstein ring is not, so under
`RectangularRTUAdaptDensity` almost every source pixel receives zero adapt
signal. The NumPy path returns a finite likelihood with a warning; the JAX path
returns NaN, and `fitness._vmap` collapses to the `resample_figure_of_merit`:

```
NumPy fit.log_likelihood: -3154.8962799401297
  .../autoarray/inversion/mappers/mapper_util.py:84: RuntimeWarning: invalid value
  encountered in divide
    pixel_signals = xp.where(max_sig > 0, pixel_signals / max_sig, pixel_signals)
JAX(no jit) fit.log_likelihood: nan
raw vmap: [-1.e+99]
```

`xp.where(max_sig > 0, pixel_signals / max_sig, pixel_signals)` guards the
*selection* but still evaluates the division; NumPy's 0/0 warning is discarded
by the selection while on the JAX path the NaN propagates into the likelihood
(the usual `where`-inside-`grad`/NaN-propagation pattern; a safe denominator
`xp.where(max_sig > 0, max_sig, 1.0)` is the standard fix). The workspace script
was corrected to adapt to the *lensed* true image (the right object anyway), so
nothing is red — but the two backends disagree on the same input, which is the
class of divergence the `_test` repos exist to catch.

Ask: (1) reproduce with a unit test on `mapper_util` where `max_sig == 0` for
some source pixels, both backends; (2) fix the division so both paths agree
(finite, and identical); (3) check the same `where(cond, a / b, a)` pattern
elsewhere in `autoarray.inversion` (grep for `/ max_` and `xp.where(` around
divisions).
