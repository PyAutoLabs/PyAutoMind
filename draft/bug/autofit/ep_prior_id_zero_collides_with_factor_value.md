# EP: the first prior of a process (id 0) collides with the `FactorValue` sentinel, corrupting every multi-variable factor gradient

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Themes:
- graphical-ep
Difficulty: small
Autonomy: safe
Priority: high
Status: formalised
Consequence: glance
Witness: on a graph whose first prior has id 0, `FactorApproximation.func_gradient` matches central finite differences of `FactorApproximation.__call__` to 1e-6 on every variable; `analytic_gaussian.py` leg A `mu` cell moves from 50.0000 +/- 20.6457 (FAIL) to 50.8596 +/- 3.76 (ref 50.8595 +/- 4.11)
Review-minutes: 5
Unattended: ready
Epic: graphical-ep
Filed: 2026-09-02

Found by the analytic Gaussian benchmark (autofit_workspace_test#91, phase (b)).
Sibling of `ep_laplace_covariance_and_failed_update_projection.md` (D2/D3) — D1 is
the reason leg A never moves at all; D2/D3 are what remains once it is fixed.

## Why

Leg A of the benchmark (exactly Gaussian hierarchical graph, sigma fixed, Laplace
should be exact) reproduces with the benchmark wiring: **mu 50.0000 +/- 20.6457**
against the closed form 50.8595 +/- 4.11. `ep_history.csv` for the hierarchical
factor: BAD_PROJECTION=54 / FAILURE=36, no SUCCESS. All 90 hierarchical updates
end `Line search failed, iter=0` or BAD_PROJECTION; mu never leaves its start, and
its mean field ends *wider* than its prior (sigma 20.6 > prior 10).

The gradient of every multi-variable factor is wrong whenever the process's first
prior has id 0. Measured at (mu=48, x=55): `state.gradient = (0.0214, -0.0139)`;
central finite differences of the same `FactorApproximation.__call__` give
`(0.0900, -0.0825)`. The factor Jacobian alone is correct (+0.07 / -0.07).
One-variable factors are unaffected (dataset_0: -4.55987 vs FD -4.55987), which is
why the analysis factors converge and only the hierarchical factor stalls.

## Root cause (deepest frame last)

1. `FactorApproximation.func_gradient`, `autofit/graphical/mean_field.py:652` —
   `grad = fjac.grad(grad_cavity)` passes the cavity gradient (keyed by the
   factor's input priors) into the Jacobian's VJP.
2. `AbstractJacobian.grad`, `autofit/graphical/factor_graphs/jacobians.py:97-99` —
   `seed = VariableData({FactorValue: 1.0}); seed.update(values)`: the input-keyed
   entries land in the VJP seed dict, which is keyed by `FactorValue`.
3. `FactorValue` is a class-as-Variable (`autofit/mapper/variable.py:142-149`)
   whose `Variable.__init__` gives it `id == 0`, `hash == 0` (`variable.py:99-100`).
4. `Prior.__eq__` (`autofit/mapper/prior/abstract.py:249-253`) compares
   `self.id == other.id` with no type check; `Prior.__hash__` is `hash(self.id)`
   (`:258-259`). So `GaussianPrior(id=0) == FactorValue` is `True`.

Net effect: the seed's `FactorValue` slot is overwritten by prior-0's cavity
gradient (0.02), the factor Jacobian is scaled by it, and prior-0's own gradient
entry is added onto the `FactorValue` key and discarded.

Control test: patching `func_gradient` to `fjac.grad() + grad_cavity` gives
mu 50.8596 +/- 3.76, all x_i means to a ~ 0.000 — bit-identical to the untouched
library when one throwaway prior is created first (so id 0 is never a graph prior).

## Minimal repro

```python
import numpy as np, autofit as af
from autofit.mapper.variable import FactorValue, VariableData
mu = af.GaussianPrior(50, 10)                      # FIRST prior of the process -> id 0
print(mu.id, FactorValue.id, mu == FactorValue, hash(mu) == hash(FactorValue))   # 0 0 True True
d = VariableData({FactorValue: 1.0}); d.update({mu: 0.02}); print(dict(d))       # {FactorValue: 0.02}
class Level:
    def __init__(self, x): self.x = x
class A(af.Analysis):
    def log_likelihood_function(self, i): return -0.5 * (51.0 - i.x) ** 2 / 0.5 ** 2
m = af.Model(Level); m.x = af.GaussianPrior(50, 20)
hf = af.HierarchicalFactor(af.GaussianPrior, mean=mu, sigma=10.0); hf.add_drawn_variable(m.x)
fg = af.FactorGraphModel(af.AnalysisFactor(m, A()), hf)
hfac = [f for f in fg.graph.factors if f.name.startswith("Hierarchical")][0]
fa = fg.mean_field_approximation().factor_approximation(hfac)
vals = {mu: np.float64(48.0), m.x: np.float64(55.0)}
_, g = fa.func_gradient(vals); eps = 1e-5
fd = lambda v: float(fa({**vals, v: vals[v] + eps}) - fa({**vals, v: vals[v] - eps})) / (2 * eps)
print({v.name: round(float(g[v]), 5) for v in vals}, {v.name: round(fd(v), 5) for v in vals})
# {'gaussianprior_0': 0.0214, 'gaussianprior_1': -0.0139}  vs FD {'gaussianprior_0': 0.09, 'gaussianprior_1': -0.0825}
```

## Fix sketch

- Give `FactorValue` an id that cannot collide with a prior: negative, or an
  `object()`-based identity; and/or make `Prior.__eq__` / `Variable.__hash__`
  type-aware so a `Prior` never compares equal to a non-`Prior` variable.
- Independently, `AbstractJacobian.grad` should not merge the free-variable cavity
  gradient into the VJP seed — only deterministic-variable cotangents belong
  there. Add the free-variable terms afterwards (the control-test form
  `fjac.grad() + grad_cavity`), which is also what makes the fix robust to any
  future id collision.

## Acceptance

- Unit test: build a graph whose first prior has id 0 (fresh process, or reset
  the id counter) and a two-variable factor; assert `func_gradient` against
  central finite differences on every variable to 1e-6, and assert
  `GaussianPrior(...) != FactorValue`.
- `autofit_workspace_test/scripts/graphical/analytic_gaussian.py`, leg A,
  "closed form vs autofit EP" column: the `mu` cell turns PASS (was
  50.0000 +/- 20.6457 FAIL); every `x_i` mean lands at a ~ 0.000. (The `mu` std
  is still ~8% low until D2 lands — see the sibling prompt; do not loosen the
  tolerance.)
- `ep_history.csv` for leg A: the hierarchical factor records SUCCESS updates
  instead of 54 BAD_PROJECTION / 36 FAILURE.

## Links

- autofit_workspace_test#91 — https://github.com/PyAutoLabs/autofit_workspace_test/issues/91
  - evidence comments: https://github.com/PyAutoLabs/autofit_workspace_test/issues/91#issuecomment-5512686880 and https://github.com/PyAutoLabs/autofit_workspace_test/issues/91#issuecomment-5513518379
- PyAutoFit#1405 (umbrella symptom) — https://github.com/PyAutoLabs/PyAutoFit/issues/1405
- Campaign ledger: `draft/research/graphical_ep/ep_campaign.md` (phase 1)
- Siblings: `draft/bug/autofit/ep_laplace_covariance_and_failed_update_projection.md`,
  `draft/bug/autofit/ep_message_support_and_transform_lost_in_projection.md`,
  `draft/bug/autofit/samples_errors_at_sigma_instance_prior_valued_model.md`,
  `draft/bug/autofit/ep_scale_collapse_basin_cure_or_caveat.md` (phase 2)
- Scripts: `autofit_workspace_test/scripts/graphical/analytic_{reference,ep_minimal,autofit,gaussian,gaussian_priors,gaussian_collapse}.py`
  on branch `feature/analytic-gaussian-benchmark`
