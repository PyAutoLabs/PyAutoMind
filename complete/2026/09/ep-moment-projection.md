## ep-moment-projection
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1654
- completed: 2026-09-30
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1656
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace_test/pull/105

### What shipped
- **PyAutoFit#1656** (merge b13169e2c): `af.LaplaceOptimiser(projection="moments")` adds opt-in moment-matching by nested quadrature, ported from the `analytic_ep_minimal` referee. The outer step is a Gauss–Legendre rule over each scale variable on its support, windowed to the cavity mean ± 8σ, with up to 4 re-windowing passes. The inner step is a conditional Laplace, using value-based central differences and a Newton polish. The kwargs are `n_quadrature=64`, `quadrature_half_width=8.0`, `moment_max_size=4` and `moment_max_outer=2`. The default stays `"mode"`, and any factor the moments path does not apply to falls back to the mode path bit-for-bit. Also new:
  - `MeanField.from_weighted_nodes`
  - `_HierarchicalFactor.scale_variables`
  - the numpy-only module `autofit.graphical.laplace.moments`
  - `autofit/graphical/README.md` §3.2, §3.3 and §3.5
- Library tests: 13 new tests. Known moments match `scipy.integrate.quad` to 1e-9. On the tight toy (50, 50.5, 49.5), mode gives 0 SUCCESS (all BAD_PROJECTION) and moments gives 3/3 SUCCESS. The full suite passes: 2947 passed, 2 skipped.
- **autofit_workspace_test#105** (merge 8f6e19c):
  - `analytic_autofit.py` passes `projection` through and seeds the DynestyStatic joint fit (`SeededDynestyStatic`).
  - `analytic_gaussian.py` is un-parked from `no_run.yaml` and added to `smoke_tests.txt`.
  - `analytic_gaussian_collapse.py` has a per-seed 0.5·std_ref scatter check, which does not gate (4/5 seeds pass).
  - The docstrings and labels match the 2026-09-30 runs.
- Witness, `analytic_gaussian.py` on the moments path (PARITY 41/41):
  - Leg A: 18/18.
  - Leg B autofit EP sigma: 6.3401 ± 2.4609 against the closed form 6.5667 ± 2.8832 (a 0.079, b 0.146).
  - HierarchicalFactor SUCCESS=25.
  - The mode-path control gives 9.3722 ± 3.5663 (a 0.973 FAIL) and BAD_PROJECTION=19.
  - Smoke: 15/15 (177 s). `analytic_gaussian.py` takes 119–130 s against the 300 s cap.

### Deviations from the approved plan (recorded on PyAutoFit#1656)
1. The inner Hessian and polish gradient use value-based central differences, not gradient finite differences. At σ≈0.017 the forward-difference gradient cancelled catastrophically, the Hessian went indefinite, and every update ended BAD_PROJECTION or FAILURE.
2. Up to 4 re-windowing passes, not 2. Two passes left a 15% variance error on a tilted density 14x narrower than the cavity.
3. `_SCALE_ARGUMENT_NAMES` stays in `expectation_propagation/diagnostics.py`.
4. The scale support `(0, inf)` is applied by argument name.
5. `moments.py` is numpy-only. A module-level scipy import broke `test_lazy_transformed_support`.
6. The end-to-end test uses two toys, because the mode path succeeds on the first one.
- Design departure from the prompt: the prompt proposed Gauss–Hermite centred on the Hessian. That centring fails exactly when the tilted σ density has no interior mode, so the support-aware Gauss–Legendre rule from the referee was used instead.

### Follow-ups
- `draft/bug/autofit/ep_moments_loggaussian_transformed_scatter.md` has two items:
  1. `analytic_gaussian_priors.py` stays parked. Its loggaussian leg fails (43/48, log sigma 3.2832 against 1.8338) on two Jacobian inconsistencies: `_OuterAxis.to_physical` applies the Jacobian to a cavity that is already base-space, and `PriorFactor` evaluates a physical density against a base-space cavity. A scratch fix recovers 1.8161 ± 0.3716.
  2. The fallback for factors with 3 finite-limit outer variables, which exceed `moment_max_outer=2`. This is why collapse seed 0 misses the scatter check.
- PyAutoFit#1656 is unreleased, so the release gate is still open: the workspace scripts need a PyAutoFit release that carries `projection="moments"`.
- The moments path costs about 16x the mode path per hierarchical projection (0.64 s against 0.04 s on the toy). That cost is why it is opt-in.

### Notes
- Supervised task. It was opened under the human-authorised Heart RED development override (issue, worktree, plan and PR-open only). Both PRs were merged by the human via /prm.
- Tier: `Consequence: glance`, so no shadow row.

## Original prompt

# EP: moment-matching projection for the hierarchical scatter (the cure the Laplace path cannot give)

Type: feature
Target: PyAutoFit
Repos:
- PyAutoFit
Themes:
- graphical-ep
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: issued — formalised — filed as the "cure" follow-on of phase 2; gated by the campaign's "JAX/gradient/Hessian EP internals" check-in (`draft/research/graphical_ep/ep_campaign.md`, Deferred) — adopt only if the human judges the scatter worth it
Consequence: glance
Witness: `analytic_gaussian.py` leg B `sigma` row and both `x_i` rows PASS at the autofit-EP tolerance (a 0.15 / b 0.25) with leg A unchanged (18/18); `analytic_gaussian_priors.py` truncated and gaussian scatter rows PASS; `analytic_gaussian_collapse.py` seeds 0-4 put the scatter within 0.5 std of the closed form; a two-variable factor with known tilted moments matches to 1e-6; both scripts are un-parked from `no_run.yaml`.
Review-minutes: 3
Unattended: ready
Epic: graphical-ep
Filed: 2026-09-02
Issued: 2026-09-30
Issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1654

## Why

Phase 2 of the EP campaign (record
`complete/2026/09/ep-scale-collapse-basin-cure-or-caveat.md`) fixed the *mechanism* of the
parent-scale collapse (PyAutoFit#1558 gradients, #1560 message support,
#1561 Hessian at the mode + skip-not-write) and shipped the caveat
(`autofit/graphical/README.md` §3.5): the collapse configuration now
RECOVERS on 5/5 referee seeds. But the scatter itself is still not
*estimated* by EP — a hierarchical factor's tilted density in σ is
∝ 1/σ at xᵢ = μ, its mode sits on the boundary, and the fixed Laplace
path correctly refuses to write a Gaussian there. The scatter therefore
stays near its prior with an honest width (referee seed 0: 9.37 ± 3.57
vs exact 6.57 ± 2.88; `|Δmean|/std` 0.97), and the two per-dataset
means most affected by it miss at a ≈ 0.19.

The closed-form benchmark's minimal EP shows the cure: **moment
matching** of the same Gaussian site (E and Var of the tilted
distribution by quadrature) recovers the exact posterior on every seed
with a ≤ 0.08 / b ≤ 0.15 on the scatter row
(`autofit_workspace_test/scripts/graphical/analytic_ep_minimal.py`,
`projection="moments"`).

## What

A moment-matching projection option for `_HierarchicalFactor` updates
(and, if cheap, for any factor with ≤ ~4 free variables):

- `LaplaceOptimiser(projection="mode"|"moments")` or a sibling optimiser
  `MomentOptimiser`: at the Laplace mode, evaluate the tilted density on
  a tensor-product Gauss–Hermite grid (or adaptive quadrature over the
  scatter's support) and match E[T(x)] per variable, exactly the
  `AbstractMessage.project` contract of README §3.3 (Eq. 8) but with
  quadrature weights instead of sampler weights.
- Respect supports (post-#1560 `_support_kwargs`) so a truncated σ is
  integrated on (0, upper).
- Fall back to the mode projection above a parameter-count threshold.

## Acceptance

- `analytic_gaussian.py` leg B `sigma` row PASS at the autofit-EP
  tolerance (a 0.15 / b 0.25) and both `x_i` rows that miss today PASS;
  `analytic_gaussian_priors.py` truncated and gaussian families PASS on
  their scatter rows; leg A unchanged (18/18).
- `analytic_gaussian_collapse.py` seeds 0–4: scatter within 0.5 std of
  the closed form (was 0.7–1.0 std under the mode projection).
- Unit test: a two-variable factor with known tilted moments matches to
  1e-6; determinism across seeds and variable ids as in
  `test_laplace_hessian.py`.
- Un-park `analytic_gaussian.py` / `analytic_gaussian_priors.py` in
  `autofit_workspace_test/config/build/no_run.yaml` and curate
  `analytic_gaussian.py` into `smoke_tests.txt` (their `__Status__`
  paragraphs name this prompt).

## Links

- Campaign ledger: `draft/research/graphical_ep/ep_campaign.md` (phase 2, Findings)
- Mechanism records: `complete/2026/09/ep-prior-id-zero.md`, `ep-message-support.md`, `ep-laplace-hessian.md`
- PyAutoFit#1405 (umbrella), #1561 (Hessian), autofit_workspace_test#91 (referee)
- README caveat: `PyAutoFit/autofit/graphical/README.md` §3.5

## 2026-09-24 — slope_hierarchy_scale 343299: hierarchical factor 0/50 SUCCESS at N=25

RAL job 343299 (PyAutoCortex `projects/slope_hierarchy_scale.md`) completed
2026-09-16 02:03 BST: wall 5h20m, `MAX_STEPS=2`, 25 lenses, JAX-on-CPU, no
pool. It logged 50 "jit compiling vectorized" lines — one compile per factor
search (2 steps x 25), confirming `draft/refactor/autofit/ep_analysis_level_compile_cache.md`.
Every dataset factor reached SUCCESS (2/2 each). **The hierarchical factor
never did:** `HierarchicalFactor0` has 50 rows = 27 `BAD_PROJECTION` + 23
`FAILURE`, zero SUCCESS (`PriorFactor239` and `PriorFactor263` also stale),
and the library's own STALE FACTORS warning fired. The parent recovery printed
exactly the prior: mean 2.0000 ± 0.7071, sigma 0.5000 ± 0.3536 (priors
TG(2,1) / TG(0.5,0.5); truth sigma 0.1).

Under the Laplace optimiser's semantics `BAD_PROJECTION` = the Hessian at the
mode is not finite or not negative-definite (the scale parameter is driven to
a limit) and `FAILURE` = the line search failed and the mean field was handed
back unchanged. This is the Laplace-on-scatter caveat
(`PyAutoFit/autofit/graphical/README.md` §3.5, `analytic_gaussian` leg B) at
100 % on the lensing model: per-lens slope widths of 0.002-0.05 are far
tighter than the scatter prior, so the tilted density in sigma sits at the
boundary. The EP arm of campaign phase 3 therefore cannot estimate the slope
scatter with the Laplace projection; this prompt is now the blocking decision
for it (human call, `Autonomy: supervised`). EP output (local):
`output/sample_n25_seed42/ep/expectation_propagation/a7ec60f07f4261afcb98b2adef484199/`
(`ep_history.csv`, `ep_diagnostics.results`).

Cross-reference — `draft/bug/autofit/ep_factors_end_the_run_with_zero.md`:
that bug records a `HierarchicalFactor1` ending with only `BAD_PROJECTION` and
never a SUCCESS on 6/200 leg-B seeds of the analytic toy (seeds 29, 71, 106,
152, 178, 193). The same shape now reproduces at 100 % on a real lensing model
(every hierarchical update over 2 steps x 25 factors), so it is no longer a
rare-seed edge case: whether a zero-SUCCESS hierarchical factor is legitimate
(the bug's open question) and whether moment matching removes it should be
judged together.
