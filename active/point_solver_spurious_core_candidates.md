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
