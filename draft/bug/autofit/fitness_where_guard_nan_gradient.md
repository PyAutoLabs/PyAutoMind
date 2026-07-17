# Fitness's NaN resample guard does not protect gradient consumers

Type: bug
Target: autofit
Repos:
- @PyAutoFit
Difficulty: medium
Autonomy: supervised
Priority: high
Status: draft

Found while localising the pixelized NaN (autolens_workspace_developer#104, phase 1
shipped via #105). Separate repo, separate fix — and arguably HIGHER leverage than
the autoarray fix it was found alongside, because it affects every `jax.grad`
consumer of EVERY likelihood, not just pixelized ones.

`Fitness.call` (`autofit/non_linear/fitness.py:239-240`) penalises a bad likelihood
with:

```python
log_likelihood = self._xp.where(self._xp.isnan(log_likelihood), self.resample_figure_of_merit, log_likelihood)
log_likelihood = self._xp.where(self._xp.isinf(log_likelihood), self.resample_figure_of_merit, log_likelihood)
```

This is the classic JAX `where`-guard gradient trap. It repairs the **value** —
confirmed empirically: the #104 probe's rejected draws report `loss = inf`, not
`nan`, so the guard fires and `resample_figure_of_merit=-inf` propagates through
`*= -2.0` to `+inf`. But reverse-mode AD evaluates BOTH branches of a `where` and
multiplies the unselected one by zero, so a NaN in the masked branch yields
`0 * NaN = NaN`: **the gradient is NaN regardless of the guard.**

So the guard's contract ("invalid models are resampled, never selected") holds for
sampler-style consumers that only read the value, and silently fails for every
gradient consumer — multi-start MAP, HMC/NUTS, MCLMC, SVGD. The value looks
handled; the gradient is poison.

This retroactively explains two #100/#101 observations that were mysterious at the
time: trajectories died with a NON-finite objective rather than a NaN one, and
`optax.apply_if_finite` LATCHED at the cliff instead of stepping past it
(unguarded runs died silently — the -39888 result in #100).

Task: apply the standard double-`where` ("safe-x") pattern so the masked branch is
never differentiated through a NaN — sanitise the input to the primal before the
select, not just the output:

```python
safe = xp.where(bad, <finite sentinel>, log_likelihood)
log_likelihood = xp.where(bad, self.resample_figure_of_merit, safe)
```

Verify with `jax.grad` at a point known to produce a NaN likelihood (the #104 probe
supplies two: seed-0 rejected draws 12 and 35 — see
`autolens_workspace_developer/searches_minimal/probe_nonfinite_pix.py`; note it
needs ~11 GiB, so an A100, not a laptop). The gradient must be finite (or a
deliberate zero), never NaN.

Decide explicitly what a resampled point's gradient SHOULD be — zero is the
defensible default (no information, don't move), but that is a judgment call with
science consequences for every gradient search, so it belongs in the plan rather
than being implied by whichever formulation is convenient.

Note the numpy path is unaffected: it catches `exc.FitException` and returns the
resample value directly (`fitness.py:232-236`); only the JAX branch reaches the
`where`. Unit tests stay numpy-only per repo policy, so the gradient assertion
belongs in a workspace_test JAX parity script, not `test_autofit/`.
