# EP Laplace: the projected "covariance" is not a Hessian, and a failed line search still projects and overwrites the message

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Themes:
- graphical-ep
Difficulty: medium
Autonomy: supervised
Priority: high
Status: issued — PyAutoFit#1561, worktree ep-laplace-hessian
Consequence: judge
Review-minutes: 20
Unattended: ready
Epic: graphical-ep
Filed: 2026-09-02
Issued: 2026-09-02
Issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1561

Two coupled defects (D2 + D3) found by the analytic Gaussian benchmark
(autofit_workspace_test#91). **This is the mechanism under the phase-2
scale-collapse prompt** `ep_scale_collapse_basin_cure_or_caveat.md` and under
PyAutoFit#1405: a wrong per-update variance (D2) that is written back even when the
optimiser did nothing (D3). Requires D1
(`ep_prior_id_zero_collides_with_factor_value.md`) first — with the D1 gradient
still broken every hierarchical update fails before these paths matter.

## Why

With the D1 gradient fixed, leg A (exactly Gaussian graph, Laplace should be
exact) still gives 17/40 hierarchical updates BAD_PROJECTION, and the `mu` std
depends on which random draw hits it: **3.76 (-8.5%)** with `refine_state`,
**4.26 (+3.7%)** with it disabled, reference 4.11. Before D1, D3 is what drove
mu's mean field to sigma 20.6 > prior sigma 10 while the optimiser reported
`Line search failed, iter=0` on all 90 updates.

## D2 — the Laplace covariance is the mean-field precision plus one random diagonal secant

- `make_posdef_hessian` (`autofit/graphical/laplace/optimiser.py:14-15`) seeds the
  Hessian with `MeanField.precision` of the `model_dist` — the factor's own old
  message included, **no factor curvature at all**. When the start is already the
  mode (gradient 0 -> NO_CHANGE) no quasi-Newton step ever touches it.
- `refine_state` (`optimiser.py:138-146`) then applies `diag_sr1_update`
  (`newton.py:60-76`) at `n_refine=3` random samples of `mean_field.sample()`.
  `state.update(...)` copies the *original* Hessian each time and
  `diag_sr1_update` writes `state1.hessian = Bk.diagonalupdate(...)` from that
  original, so the refinements **do not accumulate — only the last sample counts**.
  For the exact tilted precision `[[0.02, -0.01], [-0.01, 0.0125]]` the diagonal
  secant is indefinite in sign, so the projected variance routinely exceeds the
  cavity variance -> q*/cavity invalid -> BAD_PROJECTION (`mean_field.py:494-515`).
- Prior-id dependence: `MeanField.sample` draws `np.random` in dict order, and that
  order comes from `factor.all_variables` sets hashed by id
  (`EPMeanField.from_approx_dists`, `ep_mean_field.py:180-183`), so which variable
  consumes which draw changes with prior ids. Leg A with K throwaway priors
  created before the graph:

  K=0 (ids 0-5) mu 50.00 +/- 20.65 (D1), x_2 b 0.000; K=1 (ids 1-6) 50.8596 +/- 3.7599, b 0.018;
  K=3 (ids 3-8) 50.8596 +/- 4.0943, b 0.331; K=6 (ids 6-11) 50.8595 +/- 3.7466, b 0.004;
  K=1,3,6 with `refine_state` disabled: 50.8597 +/- 4.2627 identical to every digit, b 0.001.
  `n_refine=0` cannot be requested (`n_refine or self.n_refine`, `optimiser.py:140`).

## D3 — a failed line search still projects the start point as the mode

`optimise_approx` (`laplace/optimiser.py:130-135`) takes `max(state, next_state)`
— the *start* when the search failed — and projects it;
`update_factor_mean_field` (`mean_field.py:478-517`) never consults
`status.success`, so a FAILURE update replaces the message with
`N(old mean, secant variance) / cavity`. This is how mu's mean field drifted to
sigma 20.6 > prior 10 under D1. The exception branch at `:519-521` already returns
`last_dist` with `updated=False`; the failed-search branch should do the same.

## Minimal repro (after the D1 setup in the sibling prompt)

```python
np.random.seed(0)
proj, status = af.LaplaceOptimiser().optimise(fa)          # fa: the hierarchical FactorApproximation
_, st = proj.update_factor_mean_field(fa.cavity_dist, fa.factor_dist, status=status)
print(status.flag, "->", st.flag)   # NO_CHANGE (iter=0) -> BAD_PROJECTION
# q* sigma {mu: 11.559, x: 72.995} vs cavity (10, 20): the "Hessian" is the mean-field precision
# plus one random diagonal secant, never the tilted curvature
```

## Fix sketch

1. At the converged mode compute a real Hessian: finite-difference the (now
   correct, post-D1) gradient, or use the messages' analytic
   `_normal_gradient_hessian` plus the factor's numerical Hessian. Invert the full
   matrix and project the marginal variances.
2. Make `refine_state` accumulate across samples, or drop it once a real Hessian
   exists; allow `n_refine=0`.
3. Guard the projection: require `precision(q*) >= precision(cavity)` per variable
   *before* dividing, and flag otherwise (a real BAD_PROJECTION, not a secant
   artefact).
4. On `status.success == False` return `last_dist` with `updated=False`, mirroring
   the exception branch.

## Finding for the phase-2 "caveat" half — state it, do not re-derive it

The benchmark's minimal EP (`analytic_ep_minimal.py`) reproduces the scale
collapse **deterministically** under a mode-based (Laplace) projection on sigma:
the tilted density is proportional to 1/sigma at x_i = mu, so its mode sits at
the boundary and the projected message shrinks on every sweep. Moment matching in
the same script passes every cell. A Laplace projection of the *scatter* therefore
cannot be made exact; the fix above (real Hessian + precision guard) makes leg A
exact and stops the leg-B churn, but the cure for the scatter is **moment
matching or a log-sigma parameterisation**. That is the "caveat" deliverable of
`ep_scale_collapse_basin_cure_or_caveat.md`, and it is now writable from this
evidence.

## Acceptance

- Unit tests: (a) on a two-variable Gaussian factor with known tilted precision,
  the projected covariance equals the analytic inverse Hessian to 1e-8 and is
  independent of `np.random` state and of prior ids; (b) a forced line-search
  failure returns the unchanged `last_dist` with `updated=False` and the mean
  field is byte-identical before and after the update.
- `autofit_workspace_test/scripts/graphical/analytic_gaussian.py`, leg A,
  "closed form vs autofit EP": the `mu` cell PASS with std within tolerance of
  4.11 (currently 3.76 / 4.09 / 3.75 / 4.26 depending on K), and the result is
  identical to every digit across K = 1, 3, 6; `ep_history.csv` shows 0
  BAD_PROJECTION for the hierarchical factor on leg A.
- `analytic_gaussian.py` leg B `sigma` row and `analytic_gaussian_collapse.py`
  per-seed verdicts: report the after-numbers; PASS is *not* required here (the
  finding above says Laplace on sigma stays biased), but "documented collapse"
  must replace every "SILENT" verdict.

## Links

- autofit_workspace_test#91 — https://github.com/PyAutoLabs/autofit_workspace_test/issues/91
  - evidence comments: https://github.com/PyAutoLabs/autofit_workspace_test/issues/91#issuecomment-5512686880 and https://github.com/PyAutoLabs/autofit_workspace_test/issues/91#issuecomment-5513518379
- PyAutoFit#1405 (umbrella symptom) — https://github.com/PyAutoLabs/PyAutoFit/issues/1405;
  adjacent: #1332 F8/F10
- Campaign ledger: `draft/research/graphical_ep/ep_campaign.md` (phases 1-2)
- Phase 2 prompt: `draft/bug/autofit/ep_scale_collapse_basin_cure_or_caveat.md`
- Siblings (same dir): `ep_prior_id_zero_collides_with_factor_value.md` (done — `complete/2026/09/ep-prior-id-zero.md`, PyAutoFit#1558 merged 2026-09-02),
  `ep_message_support_and_transform_lost_in_projection.md` (done — `complete/2026/09/ep-message-support.md`, PyAutoFit#1560 merged 2026-09-02),
  `samples_errors_at_sigma_instance_prior_valued_model.md`
- Scripts: `autofit_workspace_test/scripts/graphical/analytic_{reference,ep_minimal,autofit,gaussian,gaussian_priors,gaussian_collapse}.py`
  on branch `feature/analytic-gaussian-benchmark`
