# EP messages lose their truncation limits on every natural-parameter operation, and `TransformedMessage.from_mode` skips the Jacobian for scalars

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Themes:
- graphical-ep
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 15
Unattended: ready
Epic: graphical-ep
Filed: 2026-09-02

Two message-layer defects (D4 + D5) found by the analytic Gaussian benchmark
(autofit_workspace_test#91, `analytic_gaussian_priors.py`). Both make the
non-Gaussian prior families of an EP graph wrong from the very first sweep,
independently of the optimiser defects in the sibling prompts.

## D4 — truncation limits are dropped by every natural-parameter operation

**Why.** Leg B with `TruncatedGaussianPrior(10, 5, 0, 100)` on the scatter: autofit
EP gives **sigma 3.7348 +/- 0.7527** vs closed form **6.5667 +/- 2.8832**
(q05/q50/q95 2.980/5.981/12.154); the returned `TruncatedNormalMessage` has limits
`(-inf, inf)`. In other process histories the same leg collapses fully to
sigma ~ 1e-4. #1405 records the untruncated-message symptom without a cause.

**Root cause.** `AbstractMessage.__pow__` (`autofit/messages/abstract.py:225-234`)
and `_multiply` / `_divide` -> `from_natural_parameters` (`abstract.py:173-178`)
rebuild the message as `cls_(*invert_natural_parameters(eta))`;
`TruncatedNormalMessage.invert_natural_parameters` (`truncated_normal.py:210`)
returns only `(mean, sigma)`, so the limits revert to `(-inf, inf)`. The loss
happens at the very first step — `message_dict`'s
`prior.message ** (1 / (count - 1))` (`declarative/abstract.py:82-94`) — so the
whole leg-B mean field is untruncated from the start. Downstream,
`OptimisationState.valid` sees `lower_limit = -inf`, so sigma < 0 is only caught by
the `-inf` branch in `hierarchical.py:312-324`, and `from_mode_covariance`
(`mean_field.py:393-399`) forwards the already-lost limits.

## D5 — `TransformedMessage.from_mode` skips the Jacobian for scalar variables

**Why.** `LogGaussianPrior(log 10, 0.5)` leg: autofit log sigma **2.3026 +/- 0.4564**
— exactly its start — vs closed form **1.8338 +/- 0.3608** (minimal EP
1.8164 +/- 0.3716). BAD_PROJECTION on all 150 updates; log sigma never moves. Not
the #1498 fingerprint: the no-Jacobian reference 1.9692 +/- 0.3752 is not matched
either, and `af.LogGaussianPrior.factor` carries the Jacobian correctly.

**Root cause.** `composed_transform.py:406-407`:
`if covariance.shape != (): covariance = jac.quad(covariance)`.
`MeanField.from_mode_covariance` passes `covar.get(v)`, a 0-d `DiagonalMatrix`
(`VariableFullOperator.__getitem__`, `variable_operator.py:305-308`) whose
`.shape == ()`, so the **physical** variance of sigma (25.0) is written as the
**log-space** variance (should be 0.25). Every projection then has
var(q*) >> var(cavity) -> BAD_PROJECTION.

## Minimal repro

```python
import numpy as np, autofit as af
from autofit.mapper.operator import DiagonalMatrix
print(af.TruncatedGaussianPrior(10, 5, 0, 100).message ** 0.2)   # ... lower_limit = -inf, upper_limit = inf
m = af.LogGaussianPrior(mean=np.log(10.0), sigma=0.5).message      # physical var 25.0, log-space var 0.25
print(m.from_mode(np.asarray(10.0), DiagonalMatrix(np.asarray(m.variance))).base_message)  # sigma = 5.0 (should be 0.5)
```

## Fix sketch

- D4: carry `lower_limit` / `upper_limit` through `from_natural_parameters`,
  `__pow__` and `update_invalid` — they are `_support`, not natural parameters —
  and assert equal supports when multiplying / dividing two truncated messages.
  Note the open design question in
  `draft/research/graphical_ep/transformed_message_declares_support.md`
  (#1527 shadowed the limits on the prior because they did not survive
  `with_base` / `copy` / `project` / `__call__`); this prompt fixes the
  message-level loss, which is the prerequisite for either answer there.
- D5: test `np.ndim(covariance)` / `.size` rather than `.shape != ()`, or always
  apply `jac.quad` for scalar `LinearOperator`s.

## Acceptance

- Unit tests: (a) `TruncatedNormalMessage(10, 5, 0, 100) ** 0.2`, `* other`,
  `/ other` and `from_natural_parameters` all keep `(0, 100)`; multiplying two
  messages with different supports raises. (b) `TransformedMessage.from_mode`
  with a 0-d `DiagonalMatrix` covariance applies the Jacobian: log-space sigma
  0.5 from physical variance 25.0 at mode 10, identical to the 1-d path.
- `autofit_workspace_test/scripts/graphical/analytic_gaussian_priors.py`:
  `truncated` family — the returned message reports limits `(0, 100)` and the
  `mu` row PASS (mu std currently 69% low); `loggaussian` family — the
  `log_sigma` row moves off its start (2.3026 +/- 0.4564) and PASS against
  1.8338 +/- 0.3608 within the autofit-EP tolerance (a 0.15, b 0.25);
  `ep_history.csv` no longer shows BAD_PROJECTION on all 150 updates.
- `analytic_gaussian.py` leg B `sigma` row: report the after-number; the
  remaining bias is the Laplace-on-sigma finding recorded in
  `ep_laplace_covariance_and_failed_update_projection.md`, not this prompt.

## Links

- autofit_workspace_test#91 — https://github.com/PyAutoLabs/autofit_workspace_test/issues/91
  - evidence comments: https://github.com/PyAutoLabs/autofit_workspace_test/issues/91#issuecomment-5512686880 and https://github.com/PyAutoLabs/autofit_workspace_test/issues/91#issuecomment-5513518379
- PyAutoFit#1405 (umbrella; records the untruncated-message symptom) — https://github.com/PyAutoLabs/PyAutoFit/issues/1405;
  not covered by #1332 F1-F10, #1338, #1498, #1500, #1527
- Campaign ledger: `draft/research/graphical_ep/ep_campaign.md` (phase 1)
- Related research: `draft/research/graphical_ep/transformed_message_declares_support.md`
- Siblings: `complete/2026/09/ep-prior-id-zero.md` (D1 shipped 2026-09-02, PyAutoFit#1558),
  `draft/bug/autofit/ep_laplace_covariance_and_failed_update_projection.md`,
  `draft/bug/autofit/samples_errors_at_sigma_instance_prior_valued_model.md`,
  `draft/bug/autofit/ep_scale_collapse_basin_cure_or_caveat.md` (phase 2)
- Scripts: `autofit_workspace_test/scripts/graphical/analytic_{reference,ep_minimal,autofit,gaussian,gaussian_priors,gaussian_collapse}.py`
  on branch `feature/analytic-gaussian-benchmark`
