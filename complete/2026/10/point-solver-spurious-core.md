# PointSolver: reject spurious candidates on r_core = 0 member cores (default on)

- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/800

Issue PyAutoLens#799 → PR #800 (merge `67e9f1ff3`, 2026-10-23). Epic `cluster-pointsolver-speed`; Pulse ledger PR PyAutoPulse#73 (`3aeeeae07`).

## What shipped
- `residual_threshold` on `PointSolver` / `AbstractSolver`, its `for_grid` / `for_limits_and_scale` constructors, the pytree round trip and `display_solver_from`. **Default 10.0** (human decision 2026-10-23: the problem is common on cluster models); `None` disables it.
- The solver drops candidates with |β(θ̂) − β| > k · `pixel_scale_precision`. This is a static-shape NaN mask in `_solve_array` after the magnification filter, inside the custom-JVP primal only. It costs one extra trace of the padded candidates per solve.

## Evidence (laptop CPU fp64, diagnostic)
Residuals are in units of the precision:

| Dataset | Worst true image | Smallest spurious point |
|---|---|---|
| viz cluster | 3.58 | 38.5 |
| `simple` | 2.21 | none |
| 1c/1d near-cusp | 1.075 | none |

- On the viz model, k = 10 removes only the 4 known core points (238 cases), and the 1c/1d rows are bit-identical.
- Mechanism: the host is a near-critical saddle at the members, so the core points have |μ| of 0.1–0.3 and the magnification filter cannot remove them.
- Rejected: a triangle-area consistency check, because true near-cusp candidates reach 1927 on it.
- Not tested: A2744. At precision 0.01 the cut (0.1″) is above the ~0.04″ core residuals.

## Validation
- Library: 952 passed, 1 xfailed.
- Workspace smoke: autolens 41 + 2 notebooks, workspace_test 37, euclid 9, HowToLens 50, all passed.
- 6 real-solve workspace_test point-source scripts passed.
- CI green on every leg.
- Heart YELLOW acknowledged (manifest drift; PyAutoLens release validation stale).

## Follow-ups
- Workspace validation check: `draft/feature/autolens_workspace/cluster_point_solver_validation_check.md`.
- workspace_test CI witness for the default-on filter (epic phase 2).
- Side issues: PyAutoGalaxy#658 (`draft/bug/autogalaxy/mass_sheet_deflections_fail_under_jax.md`), autolens_profiling#445 (`draft/bug/autolens_profiling/stale_auto_simulated_cluster_dataset.md`).

## Original prompt

# `@PyAutoLens` PointSolver: spurious candidates exactly on `r_core = 0` dPIE member cores

Type: feature
Target: autolens
Repos:
- PyAutoLens
- PyAutoArray
Difficulty: small
Autonomy: supervised
Priority: medium
Status: active
Consequence: judge
Epic: cluster-pointsolver-speed
Related: autolens_profiling#439 (PR #440), `results/notes/cluster_pointsolver_campaign.md`
Filed: 2026-10-23
Issued: 2026-10-23
Issue: https://github.com/PyAutoLabs/PyAutoLens/issues/799

## Why

On autolens_profiling#439's viz-model stress draws 9 and 16, at starting scales 1.0, 0.7, 0.5 and 0.3″, `PointSolver` returned a candidate exactly at an `r_core = 0` scaling dPIE member core (e.g. (15.0, 9.0008)) with a lens-equation residual of 0.04″ against a last-step tolerance of about 0.002″. The deflection is discontinuous at a zero-core dPIE/SIS centre, so the triangle containment test passes without a true root. The independent oracle rejects these; the production solver does not.

## Deliverables

1. Reproduce on a single SIS-like member with `r_core = 0` (unit test fixture, eager + JIT).
2. Investigate an optional final residual filter (|β(θ) − β| below the precision) or core-aware containment; preserve JIT/vmap/gradient behaviour and the existing eager/JIT parity tests.
3. Any default change is a human decision; add the regression to autolens_workspace_test per the epic's CI-witness contract (phase 2) once accepted.

## Out of scope

Starting-grid defaults (decided separately); cluster workspace scripts.
