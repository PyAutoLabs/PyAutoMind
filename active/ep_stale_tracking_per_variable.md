# Track EP staleness per (factor, variable), not per factor

Type: feature
Target: PyAutoFit
Repos:
- PyAutoFit
- autofit_workspace_test
Themes:
- graphical-ep
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: judge
Witness: the phase-2 campaign graph (N=2, `TruncatedGaussianPrior(10, 0.5, 0, 100)` on sigma, Laplace) names the sigma variable as stale in `ep_diagnostics.results` when its message never moves while the factor's other variables update
Review-minutes: 10
Unattended: needs-slicing
Epic: graphical-ep
Filed: 2026-09-07
Issued: 2026-09-07

Follow-up to `complete/2026/09/ep-full-revert-not-updated.md` (PyAutoFit#1574, finding 2 of the Codex review of
the phase-2 fixes). That fix makes a *fully* reverted projection count as skipped. It cannot name a
*partial* revert: on the campaign graph every hierarchical projection is `BAD_PROJECTION` with the
sigma variable reverted in each one (its message stays `[10.0, 0.7071]` bit-identical, the reported
E[sigma] never leaves the hyper-prior mean), while the factor's mean and per-dataset variables
update — so the factor is "updated" and no STALE FACTORS line appears, which is exactly the #1405
stale-scatter state the warning exists to catch.

Human decided 2026-09-07: the diagnostics lever (per-variable tracking) goes ahead now; the
moment-matching projection cure stays its own prompt.

## Scope

- `EPOptimiser.factor_step` / `_stale_factor_warnings`
  (`autofit/graphical/expectation_propagation/optimiser.py:399-430`): track which *variables* of
  each factor changed on each sweep (the per-variable `changed` mask the bug fix introduces in
  `MeanField.update_factor_mean_field`), and warn on any (factor, variable) pair that never
  changed once — "HierarchicalFactor: variable `sigma` never completed a single update".
- `ep_history.csv` gains a per-variable column or a `reverted_variables` field so the referee
  scripts (`autofit_workspace_test/scripts/graphical/analytic_gaussian_collapse.py`) can tally it.
- The STALE classification in `analytic_gaussian_collapse.py` should then read the per-variable
  flag rather than "no SUCCESS on the HierarchicalFactor".

A prototype tracker exists from the 2026-09-07 verification session (scratch only). Gated by the
campaign's EP-internals check-in like the moment-matching cure
(`ep_hierarchical_scatter_moment_matching.md`); the human decides whether the diagnostics or the
projection is the right lever.
