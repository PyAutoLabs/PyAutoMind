# Interferometer log_evidence fails (LinAlgError / NaN) at large regularization coefficients the jitted search accepted

Type: bug
Target: PyAutoArray
Repos:
- PyAutoArray
- PyAutoGalaxy
Themes:
- interferometer
- inversion
- jax
Autonomy: supervised
Priority: medium
Status: draft
Filed: 2026-10-01
Difficulty: medium
Consequence: judge
Witness: on the `autolens_workspace` `datacube/sim_simple` channel 0 (190 visibilities, Delaunay + Constant regularization), a `FitInterferometer` with `regularization.coefficient = 9.7e5` returns a finite `log_evidence` in NumPy and eager JAX that agrees with the jitted/vmapped search-path value at rel 1e-8 — or the search path rejects (−inf / resample) the same point; the result's max-likelihood instance can always be re-evaluated with `FitInterferometer(...).log_evidence` without raising.
Review-minutes: 6
Unattended: ready
Source: streaming P5 workspace example (`modeling_array_free.py`, PyAutoLabs/PyAutoArray#600, 2026-10-01): the Nautilus search on the low-S/N 4-channel cube returned a max-likelihood point with coefficient ≈ 9.7e5; re-evaluating it with `FitInterferometer.log_evidence` raised `LinAlgError` (Cholesky of the regularization matrix in `_log_det_symmetric_from`) in NumPy and gave NaN in eager JAX, on BOTH the in-memory and the array-free dataset — i.e. pre-existing, not array-free specific. The jit/vmap search path scored that sample as finite.

## What

`_log_det_symmetric_from` (autoarray inversion, regularization log-det) Cholesky-fails for a huge `Constant` coefficient
(matrix scaled by ~1e6 → loss of positive-definiteness in float64 after the curvature add, or overflow in the log-det
path), while the search's jitted likelihood accepted the same point. Either the search is scoring samples whose evidence
cannot be reproduced (a silent NaN→finite path under jit/vmap, or a different log-det route), or the eager path is the one
that is wrong. Both branches must agree, and a non-finite evidence must be rejected by the search, not returned.

## Plan

1. Reproduce: the saved result under `output/interferometer/datacube/.../modeling_array_free` (or re-run the example) →
   `result.max_log_likelihood_instance`; evaluate `FitInterferometer(...).log_evidence` eagerly (NumPy, eager JAX, jitted)
   and compare with the search's recorded `log_likelihood` for that sample.
2. Find where the jitted path differs (`jnp.linalg.cholesky` NaN handling vs NumPy raise; `jax.scipy` log-det; `lax` guards).
3. Fix: one consistent, finite-or-rejected log-det (e.g. `cho_factor` with explicit NaN → −inf, and the same guard in the
   eager path), plus a regression test at coefficient 1e6 on `interferometer_7`.
