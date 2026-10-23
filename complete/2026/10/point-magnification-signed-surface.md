Source & Cluster arc phase 5a (epic `cluster-strong-lensing`). PyAutoLens#798 merged as
`f791ac77d` on 2026-10-23, closing issue #797.

Shipped: `AbstractFitPoint.signed_magnifications_at_positions` (Hessian magnification at each
observed image position, sign = image parity); `magnifications_at_positions` is now exactly
`abs()` of it so flux fitting, magnification weighting and the source-plane panel are
numerically unchanged. `ResultPoint.signed_magnifications_at_positions` /
`magnifications_at_positions` read from the max-likelihood `FitPointDataset`'s first present
component fit (positions → flux → time delays; an unpaired dataset raises `AttributeError`).
Docstrings in the point fit module and `PointDataset` state where magnification at a point
lives and point to `LensCalc.magnification_2d_via_hessian_from` for arbitrary (y,x).

Tests: parity witness (SIE, supplied positions, NumPy and JAX, mixed signs), multi-plane
witness (three planes, point source in the middle plane; equals `LensCalc.from_tracer(...,
plane_j=1)` and differs from the final-plane value), `ResultPoint` accessor tests. No forward
PointSolver call anywhere (solver boundary approved 2026-10-01).

Evidence: full `pytest test_autolens` 941 passed / 1 xfailed; focused point tests 308 / 1
xfailed; black clean on changed files; autolens_workspace_test smoke 37/37 against the branch;
CI docs + unittest 3.12/3.13/nojax green. Heart YELLOW at ship (manifest drift 1 mismatch; no
release rehearsal), acknowledged by the human, who authorized /prm on green.

The parent prompt's stale `Tracer.magnification_2d_from` claim was already gone from source.
Workspace documentation is phase 5b: `draft/docs/autolens_workspace/point_magnification_workspace_docs.md`
(source_science.py both tiers, guides/lens_calc.py, guides/advanced/multi_plane.py cross-ref,
point_source/fit.py), launched under `--auto` per human direction 2026-10-23.


## Original prompt

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
Status: active
Issued: 2026-10-23
Consequence: judge
Review-minutes: 10
Unattended: ready
Epic: cluster-strong-lensing
Phase: 5a
Parent: draft/feature/autolens/point_magnification_api.md
Issue: https://github.com/PyAutoLabs/PyAutoLens/issues/797
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

Out of scope here, owned by phase 5b (human direction 2026-10-23: users must find this in
autolens_workspace): the eleven `source_science.py` scripts, plus a guide pass in
`guides/lens_calc.py` (mu at arbitrary (y,x) via the Hessian), `guides/advanced/multi_plane.py`
(per-source `plane_j`) and the point-source results surface in `guides/results/`; also (phase 5b), posterior-draw
errors (phase 7), maps (phase 8), any forward PointSolver repair (transferred to
`cluster-pointsolver-speed`), optimisation/profiling/robustness work (separate issues).

## Solver boundary — inherited from the parent (approved 2026-10-01)

Magnification at supplied/observed coordinates proceeds independently of PointSolver
repairs. No example or test in this slice discovers image positions with a forward solve;
positions are supplied fixture inputs.
