# `@PyAutoLens` PointSolver residual filter: add a Newton-distance condition (fix low-threshold central-image loss)

Type: feature
Target: autolens
Repos:
- @PyAutoLens
Themes:
- cluster
- point-source
- jax
Difficulty: small
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: judge
Epic: cluster-pointsolver-speed
Related: PyAutoLens#799/#800 (record `complete/2026/10/point-solver-spurious-core.md`)
Filed: 2026-10-23

## Why

PyAutoLens#800 made `residual_threshold=10.0` the default: reject a candidate when |β(θ̂) − β| > 10 × `pixel_scale_precision`. A read-only adversarial check (2026-10-23, scripts in the session scratchpad `residual_sanity/`) found:

- **False rejection.** With `magnification_threshold=0.01`, the demagnified central images of a small-core (0.02″), very elliptical `IsothermalCore` sit at 11.07× and 11.18× precision (σ_max of A ≈ 20–24). The default drops them: 2 distinct true images of 67 found. Others sit just under the cut (9.6×, 9.4×). The 11 workspace callers using 0.01 all have singular main lenses, so they are not exposed today.
- **Weak at coarse precision.** The spurious residual is fixed at about the member's Einstein radius b, so the cut only works while b > 10 × precision. At precision 0.005 (the Euclid pipeline's setting) the margin is 1.33×; at 0.01 the spurious point survives. One near-member spurious point (6×, |μ| 0.20) also survived on a fine 0.02″ grid.
- **Wrong docstring.** The #800 docstring says the linearised |A⁻¹r| would accept the core point. Measured, it is 1280h there (σ_min ≈ 0.033), so it rejects it strongly.
- **Rule comparison** on 219 candidates (209 true, 10 spurious), with h the final triangle edge:
  - Newton distance |A⁻¹r| separates cleanly: true ≤ 2.74h, spurious 23h–1670h.
  - The lost central images have |A⁻¹r| of 0.31–0.35h.
  - "residual > 10×precision **and** |A⁻¹r| > 4h" rejects 0/209 true candidates and removes the same 5 spurious ones as the current rule.
  - "|A⁻¹r| > 4h and residual > 1×precision" removes 10/10 spurious with 0 true rejected, but is untested at |μ| > ~350.
- `autolens_workspace_test/scripts/point_source/solver/error_audit.py` (threshold 0) already changes output under #800: the singular-centre candidate is dropped, so counts go 5/7 → 4/6.

## Deliverables

1. Add the Newton-distance condition. A comes from `LensCalc.hessian_from` (the components `magnification_2d_via_hessian_from` already uses), measured at the solved plane. h is the final triangle edge `scale / 2**(n_steps - 1)`, not `pixel_scale_precision`.
   - Keep it a static-shape NaN mask inside the custom-JVP primal: eager/JIT/vmap, gradients unchanged.
   - Decide, with evidence, between the AND-rule and the stronger variant. The stronger variant needs a high-|μ| (≥ 1000) near-caustic check before adoption.
2. Correct the docstring.
3. Regressions:
   - the low-threshold central-image case is kept;
   - the minimal-fixture spurious core point is still removed (and at precision 0.005, plus the 0.01 case if the stronger variant is chosen);
   - true images near a fold/cusp at high |μ| are kept.
4. Note the `error_audit.py` count change in the PR.
5. Any change to the threshold's meaning or default is a human decision at review.

## Out of scope

The triangle search's own completeness near zero-core members: it finds only 38–43 of 324 forward-built images within 0.03″ of a member, before any filter. File that separately if pursued.
