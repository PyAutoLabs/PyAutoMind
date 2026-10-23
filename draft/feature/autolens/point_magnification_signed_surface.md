# Point magnification: signed per-image magnifications on the point fit/Result surface + multi-plane witness

Type: feature
Target: PyAutoLens
Repos:
- PyAutoLens
Themes:
- cluster
- point-source
Difficulty: medium
Autonomy: supervised
Priority: high
Status: draft
Consequence: judge
Review-minutes: 10
Unattended: ready
Epic: cluster-strong-lensing
Phase: 5a
Parent: draft/feature/autolens/point_magnification_api.md
Filed: 2026-10-23

## Original user request (verbatim, from the phase-5 parent)

> Ability to get Magnification at a point in source science scripts, important for clusters
> and then extend to multi plane for clusters. It is common for lens modeling codes to give
> the magnification at a point in the image plane. PyAutoLens may do that but its not
> documented clearly, and should be in all source_science.py examples and the point source
> package.

## Why this slice

Brain's Feature Agent (2026-10-23) classifies the phase-5 parent as `split-into-phases`
(declared large, derived too-large). Phase 5a is the library-only slice; phase 5b (the
workspace `source_science.py` documentation across both tiers, plus the multi-plane worked
example) follows once 5a is pending-release. One bounded phase at a time.

Current source (PyAutoLens `b273f9c7d`, 2026-10-22) confirms the parent's audit:

- `autolens/point/fit/abstract.py:111` `magnifications_at_positions` computes μ at every
  observed image position through `LensCalc.from_tracer(use_multi_plane, plane_j)` →
  `magnification_2d_via_hessian_from`, then returns `abs(magnifications)` (line 141).
  Parity is discarded before every consumer: `fluxes.py` (model fluxes, solved flux),
  `positions/source/separations.py:184` (magnification weighting, `μ**-2`), and
  `plot/source_plane_panel.py:271` (which applies `np.abs` again).
- `autolens/point/model/result.py` `ResultPoint` exposes only `grid` and
  `max_log_likelihood_fit`; no magnification accessor on the Result surface.
- `PointDataset` has no magnification attribute (observed positions, fluxes, noise only).
- The parent's fourth item (stale `Tracer.magnification_2d_from` claim in
  `cluster/likelihood_function.py`) is ALREADY GONE — no edit required; record this.

## Bounded phase-5a task (PyAutoLens only)

1. **Signed magnification funnel.** Split `magnifications_at_positions` into a signed
   base (`signed_magnifications_at_positions`, the raw Hessian value, parity preserved)
   and keep `magnifications_at_positions` returning `abs(...)` of it so every existing
   consumer (fluxes, magnification weighting, source-plane panel) is numerically unchanged.
   The parity decision for this phase: **signed magnification is exposed as a new accessor;
   the existing unsigned default is unchanged.** Document in the docstrings that parity
   (sign) is the physical image-parity observable and that flux/weighting consumers use
   |μ| by construction.
2. **Result surface.** Add `ResultPoint.magnifications_at_positions` and
   `ResultPoint.signed_magnifications_at_positions` (via `max_log_likelihood_fit`), so a
   user reads per-image μ and parity from a finished point-source fit without rebuilding
   the fit. Keep the Result pickle/aggregator surface unchanged otherwise.
3. **Multi-plane witness.** A test asserting that the point fit's magnification for a
   source at a given `plane_redshift` equals `LensCalc.from_tracer(tracer,
   use_multi_plane=True, plane_j=j).magnification_2d_via_hessian_from(positions)`
   directly, on a three-plane fixture (the parent's `#678` final-plane-default trap:
   the test must fail if `plane_j` silently resolves to the final plane).
4. **Parity witness.** A test on a simple SIE two-image (or four-image) fixture asserting
   that `signed_magnifications_at_positions` has the expected mixed signs and that
   `magnifications_at_positions == abs(signed)`; both NumPy and JAX (`use_jax=True`) paths.
5. Point-package docstring pass: `PointDataset`/fit module docstrings state where μ at a
   point lives (fit accessor; `LensCalc.magnification_2d_via_hessian_from` for arbitrary
   (y,x)) — docstrings only, no new dataset attribute (the dataset holds observations, not
   model quantities; deferred unless phase 5b finds a need).

Validation: focused `test_autolens/point/` (fit, fluxes, separations, result) and the
multi-plane solver tests; full PyAutoLens suite before ship; black. Workspace point-source
smoke (`autolens_workspace_test` point_source scripts) must be unchanged numerically.

Out of scope here: the eleven `source_science.py` scripts (phase 5b), posterior-draw
errors (phase 7), maps (phase 8), any forward PointSolver repair (transferred to
`cluster-pointsolver-speed`), optimisation/profiling/robustness work (separate issues).

## Solver boundary — inherited from the parent (approved 2026-10-01)

Magnification at supplied/observed coordinates proceeds independently of PointSolver
repairs. No example or test in this slice discovers image positions with a forward solve;
positions are supplied fixture inputs.
