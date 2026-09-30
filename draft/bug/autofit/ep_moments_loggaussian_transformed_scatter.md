# EP moments projection drifts a log-space (LogGaussian / TransformedMessage) scatter to log sigma 3.28 against the closed form's 1.83

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
- autofit_workspace_test
Themes:
- graphical-ep
Difficulty: small
Autonomy: supervised
Priority: normal
Status: draft
Consequence: glance
Witness: the loggaussian family of `autofit_workspace_test/scripts/graphical/analytic_gaussian_priors.py` passes every autofit-EP row at a 0.15 / b 0.25 (log sigma row, mu, x_0..x_4, and the E[sigma] hard cap), so the script ends `PARITY: PASS (48/48)` and comes off `config/build/no_run.yaml`. Also a unit test in `test_autofit/graphical/functionality/test_moment_projection.py`: a two-variable factor N(x | 0, s) whose scale s carries a `LogGaussianPrior` / `TransformedMessage` cavity; E and Var of log s and of x from the moments projection match `scipy.integrate.quad` over log s to 1e-6.
Review-minutes: 3
Unattended: ready
Epic: graphical-ep
Filed: 2026-09-30
Parent: draft/feature/autofit/ep_hierarchical_scatter_moment_matching.md (PyAutoFit#1654, library PR #1656)

## What was seen

Phase 2 of ep-moment-projection ran `analytic_gaussian_priors.py` (seed 0, 2026-09-30) with
`af.LaplaceOptimiser(projection="moments")`. PyAutoFit was at 536049fa2, the same content as main
after #1656. The run ended `PARITY: FAIL (43/48)`, in 145 s:

    gaussian     16/16 PASS   sigma 6.3079 +/- 2.5678 vs 6.5667 +/- 2.8832 (a 0.090, b 0.109)
    truncated    16/16 PASS   sigma 6.3401 +/- 2.4609 (a 0.079, b 0.146)
    loggaussian  11/16        log sigma 3.2832 +/- 0.7413 vs 1.8338 +/- 0.3608 (a 4.017, b 1.054)
                              mu 50.5998 +/- 6.6196 (a 0.121, b 1.195); x_2 a 0.223; x_4 a 0.246
                              E[sigma] 35.09, outside [q05, q95] = [3.54, 11.59]
                              HierarchicalFactor SUCCESS=20; PriorFactor FAILURE=3 NO_CHANGE=12 SUCCESS=6
                              ep_diagnostics: STALE FACTORS: PriorFactor31
                              ("function is no longer finite, iter=1" on all three FAILUREs)

The referee on the same family, `analytic_ep_minimal.ep_leg_b(theta="log_sigma", projection="moments")`,
gives 1.8164 +/- 0.3716, which PASSes. The mode path (`projection="mode"`) on the same graph gives
1.5292 +/- 0.3929, also a miss but bounded. So the moments path makes the log-space family worse,
while it cures the gaussian and truncated families.

## Diagnosis (verified by monkeypatching in a scratch probe; PyAutoFit not edited)

There are two Jacobian inconsistencies. Both come from mixing the physical density and the
base-space (u = log sigma) density of a `TransformedMessage`.

1. **The moments path counts the Jacobian twice** (`autofit/graphical/laplace/moments.py:243-249`,
   `_OuterAxis.to_physical`, used at `:470-476` in `_integrate`).
   - Each outer node's log weight gets `log|dx/du|` (= u for the log transform). The assumption is
     that `FactorApproximation.__call__` returns a physical density.
   - It does not. `FactorApproximation.__call__` (`mean_field.py:778-782`) evaluates the cavity
     through `MeanField.logpdf` (`mean_field.py:288-294`), which calls
     `MessageInterface.logpdf` (`messages/interface.py:59`). For a `TransformedMessage` that is the
     base density at `_transform(x)`, **with no Jacobian**: only `.factor` adds `logd`
     (`composed_transform.py:370-385`).
   - Measured for `LogGaussianPrior(log 10, 0.5)` at sigma = 12: `message.logpdf` = -0.2923, which
     is N(log 12 | log 10, 0.5), the base density. `message.factor` = -2.7772, which is the physical
     log-normal.
   - So the quadrature integrates `tilted(u) * e^u`. Each hierarchical update then moves E[log sigma]
     up by about Var(log sigma), and the move compounds over the sweeps (1.83 → 3.28).
2. **The prior factor of a transformed prior is a physical density against a base-space cavity**
   (`declarative/factor/prior.py:23` → `Prior.factor` → `message.factor`,
   `mapper/prior/abstract.py:132-136`).
   - Against the u-measure cavity, the `logd` term tilts the prior site by e^{-u}, so the prior site
     is biased low by about Var(log sigma).
   - This runs on the mode path too: the PriorFactor is not an outer variable, because
     `_support_kwargs` is empty for a Normal base. It is a likely contributor to the mode path's 1.53.

Probe results (scratch `probe_loggauss_fix*.py`, seed 0, the same graph as the script):

    fix 1 only (to_physical returns log_j = 0)             log sigma 1.6912 +/- 0.3639 (a 0.395, b 0.008);
                                                           PriorFactor FAILUREs gone; every other row PASS
    fix 1 + fix 2 (TransformedMessage.factor := base logpdf)  log sigma 1.8161 +/- 0.3716 (a 0.049, b 0.030);
                                                           mu a 0.012 b 0.079; x_i a <= 0.012;
                                                           matches the minimal EP to 3e-4

## Proposed fix (not applied)

- In `moments.py` the tilted density is already a u-density for a transformed outer axis, so drop
  the `log|dx/du|` term. Two ways to do that:
  - `to_physical` returns `(x, 0.0)`.
  - Or, more robustly, compute log_j from how the cavity is evaluated: 0 when the message's `logpdf`
    is base-space.
- Update the module docstring's weight formula and README section 3.3 Eq. 9 to match.
- Make the EP prior site consistent with the u-measure messages. Either:
  - `PriorFactor` evaluates `prior.message.logpdf` (base density) inside EP, or
  - the tilted density is formed with `.factor` for both the factor and the cavity.

  `.factor` (the physical density, with the Jacobian) must stay what the joint/sampler fit of
  `global_prior_model` uses, because there the parameter is physical sigma. So the change belongs
  on the EP side, not in `TransformedMessage.factor`. Check that the #1498 fingerprint verdict in
  the priors script flips to "#1498 NOT reproduced".
- The witness includes the new unit test (quadrature reference in log s).

## Second item: bounded-support non-scale variables are promoted to outer variables

In `analytic_gaussian_collapse.py`, the drawn x_i, the parent mean and the parent scatter all carry
`TruncatedGaussianPrior(..., 0, 100)`. `moments.split_variables` (`moments.py:126-138`) makes
every variable with a finite limit an outer variable (`_has_bounded_support`, `:118-123`).

- Each `_HierarchicalFactor` therefore has 3 outer variables (mu, sigma, x_i). That is more than
  `moment_max_outer=2`, so every hierarchical update falls back to the mode path. An instrumented
  run counted 62 of 62 hierarchical calls with the reason "3 outer variables exceed
  moment_max_outer=2".
- With `moment_max_outer=3`:
  - At `n_quadrature=16`, 5 seeds took 25-40 s each, not the 4-5 s the fallback takes. Four seeds
    ended STALE, with the dataset factors in BAD_PROJECTION.
  - At `n_quadrature=32`, 2 seeds did not finish in 10 minutes.
- The mu and x_i truncations sit 50 std from their posteriors (mass outside [0, 100] < 1e-50). Only
  the scale needs quadrature.
- Proposed change: only `scale_variables` become outer variables. A finite limit alone should not
  promote a variable, or should promote it only when the cavity window
  (mean ± `quadrature_half_width`·std) reaches the limit. Keep the bounded variable inner, with its
  limit enforced by the conditional Laplace, as `prepare_state` already does.
- Witness for this item: the collapse script's "scatter within 0.5 std_ref" check becomes gating
  (`SCATTER_CHECK_GATES = True`) and passes 5/5. On 2026-09-30 it is 4/5: seed 0 has
  9.2913 +/- 3.53 against 6.5667 +/- 2.8832, |Δ|/std_ref 0.945. That miss is the mode-path result
  the fallback produces.
