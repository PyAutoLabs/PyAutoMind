# Magnification at a point: surface the existing API in source_science

Type: feature
Target: PyAutoLens
Repos:
- PyAutoLens
Themes:
- cluster
- point-source
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: ready
Epic: cluster-strong-lensing
Phase: 5
Parent: draft/feature/autolens/source_cluster_arc.md
Filed: 2026-08-19 (backfilled from git)

# Magnification at a point: surface the existing API in source_science + point package, extend to multi-plane

Part of the Source & Cluster arc (phase 5 of 12). User request (verbatim): "Ability to
get Magnification at a point in source science scripts, important for clusters and then
extend to multi plane for clusters. It is common for lens modeling codes to give the
magnification at a point in the image plane. PyAutoLens may do that but its not
documented clearly, and should be in all source_science.py examples and the point source
package."

Audit answer: PyAutoLens DOES do it, in three places, none documented in source_science:
- `LensCalc.magnification_2d_via_hessian_from(grid, xp)` (lens_calc.py:624) — arbitrary
  (y,x) points, ArrayIrregular, JAX-viable; multi-plane via
  `LensCalc.from_tracer(..., use_multi_plane=True, plane_j=j)`.
- `magnifications_at_positions` on the point fit (point/fit/abstract.py:111) — per-image,
  multi-plane aware. But it applies `abs()` (:140) — **parity/sign is discarded at every
  consumer** in the stack; decide whether to expose signed magnification (parity is
  physical: image parities are standard cluster-lensing observables).
- The only closed-form profile magnification is dPIE
  (dual_pseudo_isothermal_mass.py:446,779).

Science anchor (LEGGOS II, arXiv:2606.20804): point magnification for a clump is the
magnification-map value at the pixel containing the clump centroid; per-clump errors
come from evaluating the same pixel across posterior-draw models (phase 7 handles the
draws; this phase makes the point evaluation a first-class documented call).

Work:
1. Document magnification-at-a-point in every source_science.py (both tiers) with a
   worked example: μ at chosen (y,x), μ at the positions of each multiple image.
2. Point package: expose per-image magnifications on the point Result/dataset surface
   (today magnification exists only on the fit; the dataset has no magnification
   attribute), and document the parity decision.
3. Multi-plane: worked example for cluster use — μ at a point for a source at given
   plane_redshift (per-source LensCalc plane_j); note the #678 trap (final-plane
   default).
4. Fix the stale doc claim `Tracer.magnification_2d_from` in
   cluster/likelihood_function.py:387 (no such method — calls route through LensCalc).

<!-- formalised by the Intake (Conception) Agent on 2026-08-19 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/483da28c-8c96-4c83-ad87-a43448ca2164/scratchpad/source_cluster_phases/phase05_point_magnification_api.md -->
