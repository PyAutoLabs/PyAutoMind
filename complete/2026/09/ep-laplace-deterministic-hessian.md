- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1570 (closed completed 2026-09-07)
- completed: 2026-09-07
- library-pr: PyAutoFit https://github.com/PyAutoLabs/PyAutoFit/pull/1573 (head `d5acab35`, merge `470a89cf`)
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1573
- classification: bug, P1 (PyAutoFit) — epic `graphical-ep`; bundle `ep-phase2-review` (Codex review of the phase-2 fixes, finding 1). No workspace PR.
- ci: `Tests [pull_request]` unittest 3.12 / 3.13 / nojax green, `Docs [pull_request]` green; CLEAN.
- heart-ack: YELLOW "workspace validation not passing" (organism-scope, cloud#34099198772); nothing in this diff is in the release chain.

- summary: the fd branch of `LaplaceOptimiser.optimise_approx` (default since #1562) wrote only the free-variable Hessian; `det_hessian` kept the cavity precision, so deterministic variables were projected unchanged with `success=True` — z = 2x with initial q(z) = N(0, 10) returned Var(z) = 100 (quasi path and truth 0.8). New `make_deterministic_hessian`: central-difference Jacobian of `deterministic_values` on the shared `fd_steps`, precision = diag(J Σ Jᵀ)⁻¹ (diagonal only — rank-deficient when n_det > n_free; `from_mode` reads marginals); zero-row outputs keep cavity curvature.
- verdict: test `test__deterministic_variance_follows_the_free_variable[fd|quasi]` fails on fd without the fix; graphical 267 pass; workspace `ep_deterministic.py` PASS, `analytic_gaussian_collapse.py` RECOVER 5/5 with σ/μ unchanged from the phase-2 record. The campaign referee has no `factor_out`, which is why every gate missed this (memory `feedback_ep_referee_blind_to_deterministic_variables`).
- worktree: shared bundle worktree `~/Code/PyAutoLabs-wt/ep-phase2-review` removed at the bundle's close-out.

## Original prompt

# Laplace fd-Hessian path leaves deterministic variables at their cavity covariance

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
Witness: `z = 2x` EP graph (prior N(0,1), likelihood N(0,0.5) on x, initial q(z) = N(0,10)) returns Var(x) ≈ 0.2 and Var(z) ≈ 0.8 on `hessian="fd"` (currently 100.0) and `hessian="quasi"`; new test in `test_autofit/graphical/functionality/test_laplace_hessian.py`; `test_autofit/graphical` stays 265+ green; `autofit_workspace_test/scripts/graphical/ep_deterministic.py` PASS
Review-minutes: 6
Unattended: ready
Epic: graphical-ep
Filed: 2026-09-07
Issued: 2026-09-07

Finding 1 (P1) of the Codex review of the graphical-ep phase-2 fixes (PyAutoFit#1558, #1560,
#1562; record `complete/2026/09/ep-scale-collapse-basin-cure-or-caveat.md`). Reproduced exactly on
`main` (f6a991504) on 2026-09-07. Siblings from the same review:
`ep_full_revert_not_updated.md`, `transformed_from_mode_coupled_covariance.md`.

## Original review (verbatim)

> Phase 2 review: three code findings, across the merged fixes #1558, #1560 and #1562.
>
> 1. P1 — Incorrect uncertainties for deterministic variables (#1562). The new Hessian path
>    updates the free-variable covariance but leaves deterministic outputs using their old
>    estimate. For z = 2x, the correct variances are Var(x)=0.2, Var(z)=0.8; the new default
>    returns Var(z)=1.0 with success. The previous quasi-Newton path returns 0.8.
> 2. P2 — Fully rejected updates can suppress the stale warning (#1562). The new tracking trusts
>    status.updated, but existing projection logic sets it true after restoring every invalid
>    parameter. A reproduced full EP run returned its unchanged starting distribution with no
>    STALE warning.
> 3. P2 — Coupled transformations receive incorrect covariance (#1560). Converting operator
>    covariance into a diagonal vector breaks MultiLogitNormalMessage. Equivalent matrix/operator
>    inputs return variances [0.5700, 0.6089] versus [1.0233, 0.8956]. The campaign's scalar
>    transformations pass, so its tests miss this.
>
> The phase-1 reporting error also carries into phase 2's README: the minimal Laplace example
> demonstrates rejected updates, not numerical scatter collapse.
>
> Validation: 239 focused tests passed. The original phase-2 script reproduced RECOVER 5/5 on the
> exact PR snapshots. That confirms the recorded interval checks; the completion record correctly
> acknowledges that reliable scatter estimation remains unfinished. No defects found in #1558 or
> workspace #93.

## Reproduction (2026-09-07)

`Factor(2*x, x, factor_out=z)`, prior N(0,1) x likelihood N(0,0.5) on x, EP with
`LaplaceOptimiser`:

| path | Var(x) | Var(z) | status |
|---|---|---|---|
| `hessian="fd"` (new default) | 0.1996 | 1.0000 (initial q(z) untouched; 100.0 with q(z)=N(0,10)) | SUCCESS |
| `hessian="quasi"` (pre-#1562) | 0.1996 | 0.8000 | SUCCESS |
| truth | 0.2 | 0.8 | |

Both paths report success, so EP records the factor as updated: a silent wrong uncertainty. The
fd path exits the ascent at iteration 0 when the mean-field mean is already the mode, so not even
the in-loop secant update fires.

## Mechanism

`autofit/graphical/laplace/optimiser.py:219-248` (`LaplaceOptimiser.optimise_approx`): the fd
branch writes only `next_state.hessian` (free-variable curvature) and returns. `det_hessian` keeps
the cavity precision `prepare_state` built (lines 138-140). The only code that refreshes it,
`newton.quasi_deterministic_update` (`laplace/newton.py:104-119`), is reached from the line search
and from `refine_state`, which #1562 moved to the `else` branch. `OptimisationState.inv_hessian_blocks`
(`laplace/line_search.py:241-246`) then merges the stale `det_hessian.inv()` into the projection.

## Fix

In the fd branch, after `next_state.hessian = hessian`, when `next_state.det_hessian` is set,
refresh it with a new `make_deterministic_hessian(state, hessian, mean_field)`: central-difference
the factor's `FactorValue.deterministic_values` w.r.t. the free parameters (same step rule as
`make_mode_hessian`) to get J, then write `VariableFullOperator.from_diagonal(1 / diag(J Σ Jᵀ))`
with Σ = `hessian.inv()`. Diagonal only: `J Σ Jᵀ` is rank-deficient when n_det > n_free (the
regression tests with 50 outputs / 3 params fail on a full block), and `MeanField.from_mode`
consumes marginals. Outputs with a zero J row keep their cavity curvature. A verified prototype
(265/265 `test_autofit/graphical` pass, `ep_deterministic.py` PASS) exists; port it, do not
redesign.

Test: `z = 2x` as above, assert Var(x) ≈ 0.2 and Var(z) ≈ 0.8 (rtol 1e-2) for both `fd` and
`quasi`. No existing test asserts a deterministic variable's variance
(`regression/test_linear_regression.py` checks a, b only; `ep_deterministic.py` only asserts
`z_variance < z_prior_variance` under a dominating exact likelihood). The campaign referee
(`analytic_gaussian_collapse.py`) has no `factor_out`, so it could not see this.
