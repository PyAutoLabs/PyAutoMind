# Critical-curve oracle: find the regime where zero-contour beats marching squares for complex mass models

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
- PyAutoGalaxy
- PyAutoLens
Themes:
- critical-curves
- jax
- cluster
Difficulty: too-large
Autonomy: human-required
Priority: medium
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: never
Lane: ral
Campaign: critical-curves
Filed: 2026-11-09

Human request (verbatim, 2026-11-09): "I think the intake should be such that in the long term we create an oracle which for galaxy scale and cluster scale complex mass models computes all tangential and radial critical curves and works out if and how marching squares reduces in speed or accuracy compared to zero contour. I am confident we need to use zero contour for the hardest critical curve calculations but we dont know what regime to use it."

## Why

autolens_profiling#521 (PR #522) kept marching squares for modeling-run figures. Its corpus was phase-4 posterior draws of simple-to-moderate models, so it answers "which engine for today's figures". It does not answer the harder question. The human expects zero-contour to be **needed** for the hardest critical-curve calculations, and we do not yet know where that regime starts. #521 already showed both engines failing on the hard end, for different reasons:

- Marching squares misses small member-galaxy curves at cluster scale (0.25″ grid).
- Zero-contour's ±3″ seeds miss group and cluster curves.
- Zero-contour's 500 × 0.05″ path length cannot close a large far-plane curve.

## Goal: an oracle, then a regime map

1. **Oracle.** For galaxy-scale and cluster-scale complex mass models, compute *every* tangential and radial critical curve, plus its caustic, to a stated accuracy, independently of both engines being judged. Candidates to weigh during scoping: adaptive refinement of the eigenvalue sign field, dense sampling plus Newton polish (as in the cluster PointSolver oracle, `scripts/cluster/image_plane/_oracle.py`), and analytic controls (cored isothermal radii) for calibration. The oracle must prove completeness, i.e. no missed small components, on calibrated fixtures before it is trusted.
2. **Model corpus spanning difficulty:**
   - galaxy: power law + shear, multipoles, cored/radial-curve-heavy profiles, MGE/decomposed stellar + dark;
   - group: several dPIE members around a main lens;
   - cluster: many members, scaling relations, multiple source planes, substructure.
   Vary curve size, member count, separation and source redshift.
3. **Regime map.** For each model, score marching squares against grid resolution and field, and zero-contour against seed policy, step size and path length, with and without a warm compile cache. Measure accuracy (component completeness, two-pixel distance, closure) and cost. Output: the boundary where zero-contour becomes necessary or cheaper for a required accuracy, per scale. Cover both modeling-run figures and offline analysis (magnification maps, caustic-crossing calculations).
4. **Outcome.** A recommended engine-selection rule (e.g. by expected curve size, member count, required accuracy). Any library change ships as its own phase via start_dev, including the zero-contour prerequisites (`draft/refactor/autogalaxy/zero_contour_pytree_compile_cache.md`: compile cache, field-wide seeds, duplicate removal, fallback).

## Reuse

- Harness and corpus loaders: `scripts/lens/critical_curves/modeling_viz_feasibility*.py` (all-paths samples loader, cluster per-plane comparison).
- Phase-3a fixtures and geometry: `scripts/lens/critical_curves/dispatch.py`.
- Campaign wiki: `wiki/campaigns/lens/critical_curves/critical_curves.md`.

## Scoping first

Large. The first session scopes it with the human: oracle method and its own validation, corpus, compute, and how much runs on RAL GPU vs CPU. It is then phased before any measurement.

<!-- formalised by the Intake (Conception) Agent on 2026-11-09 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/b8d07835-3b05-4ec8-8d02-781e09e7a2b3/scratchpad/oracle.md -->
