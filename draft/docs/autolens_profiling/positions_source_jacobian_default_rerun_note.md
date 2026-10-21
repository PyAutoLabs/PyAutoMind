# Note in autolens_profiling that plain source-plane lane values predate the jacobian default

Type: docs
Target: autolens_profiling
Repos:
- autolens_profiling
Difficulty: small
Autonomy: supervised
Priority: low
Filed: 2026-10-21
Status: formalised
Consequence: glance

@autolens_profiling

## Context

PyAutoLens#792 (issue #791, record `complete/2026/10/positions-source-jacobian-default.md`) changed the `al.FitPositionsSource` default from `"magnification"` to `"jacobian"`. It also made the `"magnification"` normalisation model-independent: Σ log((2π)²σ⁴).

This scope was deferred from that task because autolens_profiling was claimed by `cluster-pointsolver-robust-settings`.

## Scope

- In `wiki/campaigns/point_source_source_plane.md` and `results/notes/point_source_source_plane_campaign.md`, add a dated note. It should say that the plain-lane `al.FitPositionsSource` timings and logL values were recorded under the old scalar default.
- Check the eager-parity rtol checks in `point_source_source/source_plane/*.py` and `cluster/source_plane/likelihood_breakdown.py`. They compare against eager values, so they should still pass. Re-pin any absolute literal.
- Decide whether a rerun is needed. Timing should be essentially unchanged, because both weightings need the Jacobian.
