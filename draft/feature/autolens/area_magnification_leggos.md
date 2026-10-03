# Area magnification (LEGGOS-style): per-pixel inversion sum as primary

Type: feature
Target: PyAutoLens
Repos:
- PyAutoLens
- autolens_workspace
- autolens_assistant
Themes:
- cluster
- point-source
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Epic: cluster-strong-lensing
Phase: 6
Parent: draft/feature/autolens/source_cluster_arc.md
Filed: 2026-08-19 (backfilled from git)

# Area magnification (LEGGOS-style): per-pixel inversion sum as primary; ShapeSolver rehabilitate-or-retire

Part of the Source & Cluster arc (phase 6 of the original arc), gated on phases
3 (critical curves/segmentation) and 5 (point magnification API). User request (verbatim): "Ability to get areas only Magnification as extension to
source science scripts. Look at LEGGOS paper for description of equations but basically
area extension to the above, seems like standard calculation in cluster lensing. We have
the ShapeSolver in the source code, but long time since used and tested and may not be
JAX support yet. This requires reviewing the ShapeSolver and working out if its good for
area magnification or we should use different approach. Remember also that area can link
to source size."

Science anchor — LEGGOS II (arXiv:2606.20804) Eq. 6-7, the standard cluster calculation:
  μ_arc = A_img / A_src,  with  A_src = Σ_i A_pix,i / μ_i
i.e. sum image-plane pixel areas over the arc mask, and invert the LOCAL point
magnification per pixel to get the source-plane area. Segmentation uses the critical
curve as the natural boundary between images (phase 3 dependency). This needs ONLY the
point-magnification map (phase 5) — no forward shape solving.

Historical ShapeSolver audit (2026-08-19; transferred scope, re-audit current code): effectively unmaintained. One method
(find_magnification = kept-triangle image area / source shape.area), only test commented
out since ~2024-09, `use_jax=True` silently ignored (find_magnification hardcodes xp=np,
never consults self._xp), the JAX triangle `area` cannot survive jax.jit (__len__
returns a traced count_nonzero), no per-image split, no magnification-threshold filter,
no error estimate; image area over-covers by up to one triangle edge per boundary with
no convergence check. Sole consumer: one unused demo in workspace point_source/fit.py.

Work:
1. Implement the LEGGOS per-pixel-inversion area magnification as the primary API: given
   an image-plane mask/segment (or arc pixels), compute μ_area with the μ-map from
   LensCalc (JAX-viable, multi-plane aware). Add to source_science.py examples.
2. Validate the primary pixel-inversion area against independently known simulated
   arc/source areas with resolution/convergence and segmentation controls. A
   forward ShapeSolver comparison can be added when independently validated; it
   is not a prerequisite for this primary API.
3. Keep multi-plane/source-redshift and signed/absolute magnification decisions
   explicit, with bounded numerical regressions in autolens_workspace_test/CI.
4. Ingest LEGGOS II into autolens_assistant wiki/literature (bibkey, source entry,
   magnification-methodology claims) so future cluster work cites it.

<!-- formalised by the Intake (Conception) Agent on 2026-08-19 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/483da28c-8c96-4c83-ad87-a43448ca2164/scratchpad/source_cluster_phases/phase06_area_magnification_leggos.md -->

## Scope separation — approved 2026-10-01

Forward ShapeSolver rehabilitation-or-retirement is owned by
`https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/cluster_pointsolver_speed.md`. That includes
current-code audit, xp/JIT behavior, per-image splitting, finite-source area
convergence/accuracy, flux-path implications and independent cross-validation.
The historical audit above is retained as context, not a current API verdict.
Do not remove or repair ShapeSolver as a side effect of this primary area task.
No blanket PointSolver-health gate applies to supplied image-plane arc pixels.
