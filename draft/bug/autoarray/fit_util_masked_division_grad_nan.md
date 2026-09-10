# fit_util: masked divisions NaN the gradient on the JAX path

Type: bug
Target: PyAutoArray
Repos:
- PyAutoArray
Difficulty: small
Autonomy: safe
Priority: medium
Status: formalised
Filed: 2026-09-10

Found by the ask-(3) pattern sweep of
`draft/bug/autoarray/mapper_adapt_zero_signal_jax_nan.md` (PyAutoArray#548), and
split out of it on the human's call rather than widening that PR into a second
module. Same bug class, different module, and on the face of it the more serious
of the two: this one sits on the likelihood-gradient path.

`autoarray/fit/fit_util.py` has three `xp.where(cond, <expr with a division>, …)`
sites where the `where` guards only the *selection* — the division is still
evaluated for every element, so a zero denominator puts a NaN in the discarded
branch. Forwards it is invisible; under `jax.grad` it propagates.

```
fit_util.py:251  chi_squared_map_with_mask_from
                 xp.where(mask == 0, xp.square(residual_map / noise_map), 0)
fit_util.py:452  residual_flux_fraction_map_from
                 xp.where(data != 0, residual_map / data, 0)
fit_util.py:474  residual_flux_fraction_map_with_mask_from
                 xp.where(mask == 0, residual_map / data, 0)
```

Reproduced for :251, the chi-squared map, with a masked-out pixel carrying zero
noise (the ordinary case — noise maps are commonly zeroed outside the mask):

```python
mask      = np.array([0, 0, 1])     # 0 == included
noise_map = np.array([1.0, 2.0, 0.0])
# forward : 2.0                     <- finite, so nothing catches it
# grad    : [ 2.,  1., nan]
```

:474 has a second problem on top of the shared one: it guards on the *mask*, not
on `data`, so a zero `data` value anywhere inside the unmasked region is a NaN
forwards, on both backends.

Ask: (1) pin each of the three with a `jax.grad` test asserting a finite
gradient, plus a forward test for the :474 unmasked-zero case; (2) fix with a
safe denominator — `denom = xp.where(cond, denom, 1.0)` then divide — the idiom
`mapper_util.adaptive_pixel_signals_from` now uses after #548, and that
`pixel_counts` in that same function used already; (3) decide whether :474
should guard on `data != 0` as well as the mask, or whether a zero data value in
the unmasked region should stay loud.

Note for whoever picks this up: #548's investigation showed the *forward* NumPy
and JAX results agreed at its site, and the same is true here — do not expect a
forward-value divergence to reproduce it. The gradient is the witness.
