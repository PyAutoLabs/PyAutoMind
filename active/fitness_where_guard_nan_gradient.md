# Pin the real contract of Fitness's NaN resample guard (value, never gradient)

Type: bug
Target: autofit
Repos:
- @PyAutoFit
- @autofit_workspace_test
- @autolens_workspace_developer
Difficulty: small
Autonomy: supervised
Priority: normal
Status: draft

Found while localising the pixelized NaN (autolens_workspace_developer#104,
shipped via #105).

`Fitness.call` (`autofit/non_linear/fitness.py:238-240`) penalises a bad
likelihood with:

```python
log_likelihood = self._xp.where(self._xp.isnan(log_likelihood), self.resample_figure_of_merit, log_likelihood)
log_likelihood = self._xp.where(self._xp.isinf(log_likelihood), self.resample_figure_of_merit, log_likelihood)
```

It repairs the **value** — confirmed empirically: #104's rejected draws report
`loss = inf`, not `nan`, so the guard fires. But under `jax.grad`, reverse-mode
AD differentiates the masked branch and multiplies by zero, so `0 * NaN = NaN`:
**the gradient is NaN regardless of the guard.** This retroactively explains two
#100/#101 mysteries — trajectories died with a non-finite objective rather than a
NaN one, and `optax.apply_if_finite` LATCHED at the cliff instead of stepping
past it (unguarded runs died silently — #100's -39888).

## What the investigation established (do not re-derive)

Three things were proved on CPU in seconds (~20 lines of JAX; **no A100 needed** —
an earlier draft of this prompt wrongly specified the #104 pixelized probe, which
needs ~11 GiB):

1. **The trap is narrower than "the guard never protects gradients".** It fires
   only when the masked branch's **derivative** is non-finite. `sqrt(x)` at x<0
   NaNs its derivative -> trap fires. `log(x)` at x<0 is NaN in value but its
   derivative `1/x` stays finite -> `0 * -1 = 0`, no trap. Cholesky on a non-PD
   matrix (#104's actual site) NaNs its derivative, so the trap fires there.

2. **An output-side double-`where` DOES NOT FIX IT.** Measured:

   ```
   current (fitness.py:239-240)     x=-1.0  value=inf  grad=nan
   output-side double-where         x=-1.0  value=inf  grad=nan   <-- still NaN
   input-side safe-x                x=-1.0  value=inf  grad=0.0   <-- works
   ```

   By the time `Fitness.call` receives `log_likelihood`, the NaN derivative is
   already on the tape. Sanitising the output cannot repair it. Only avoiding the
   *evaluation* of the likelihood at the bad input works — and that decision lives
   deep inside the likelihood (autoarray's cholesky), not in `Fitness.call`.

3. **Therefore `Fitness.call` is structurally incapable of fixing this.** The
   guard advertises protection it cannot provide to gradient consumers. The real
   fix belongs at each NaN source — for the pixelized case, that is
   `draft/bug/autoarray/reg_matrix_logdet_nonfinite_fix.md` (phase 2).

## Task: contract + test, NOT a code fix

Human decision 2026-07-17: pin the true contract; write no code fix here.

1. **PyAutoFit** — docstring on `Fitness.call` stating the guard's real contract:
   value-only; gradient-safety must be established at the NaN source; a
   downstream guard cannot repair a NaN-carrying tape. Note the
   masked-derivative condition (point 1 above). No behaviour change. Cross-ref
   autolens_workspace_developer#104.

2. **autofit_workspace_test** — new
   `scripts/jax_assertions/fitness_nan_gradient_contract.py`, mirroring the
   sibling `fitness_dispatch.py` (same `af.ex.Gaussian` + `Fitness` setup).
   Assert on a NaN-derivative likelihood: the **value** is guarded; `jax.grad`
   **is** NaN (pins the limitation so it cannot silently regress into a false
   promise); the output-side double-`where` does **not** fix it (the disproof, so
   nobody re-prescribes it); input-side safe-x **does**. Unit tests stay
   numpy-only per repo policy — this belongs here, not in `test_autofit/`.

3. **autolens_workspace_developer** — correct
   `searches_minimal/pix_nonfinite_findings.md`, which shipped in #105 carrying
   two errors from before this investigation: the over-strong "does not protect
   gradient consumers at all" claim, and the double-`where` remedy line (now
   disproved). Replace the "needs an A100" reproduction note for this specific
   bug with the CPU repro.

Explicitly **out of scope**: a search-level gradient sanitiser
(`where(isfinite(g), g, 0)`). It fabricates a zero gradient at invalid points, and
#101 already showed `optax.apply_if_finite` latches at the cliff; the principled
response to an invalid point is restart/resample, which
`draft/feature/autofit/multistart_resurrection_and_contrib_rules.md` covers.
