# `@PyAutoLens` PointSolver: replace post-hoc candidate filters with root refinement (research)

Type: research
Target: autolens
Repos:
- @PyAutoLens
Themes:
- cluster
- point-source
- jax
Difficulty: large
Autonomy: supervised
Priority: low
Status: formalised
Consequence: judge
Epic: cluster-pointsolver-speed
Related: PyAutoLens#799/#800 (record `complete/2026/10/point-solver-spurious-core.md`); doc guide `draft/docs/autolens_workspace/point_solver_guide.md`
Filed: 2026-10-23 (as a Newton-distance filter feature); re-scoped to research 2026-10-24

## Why

PyAutoLens#800 rejects candidates whose source-plane residual exceeds 10 × `pixel_scale_precision`. A sanity check on 2026-10-23 found three weaknesses. It drops true demagnified central images when `magnification_threshold=0.01`. Those images have |μ| of 0.013–0.016, so the default 0.1 drops them anyway, which is right for modelling because they are never observed. This only matters below a threshold of about 0.02. It is weak at coarse precision (0.005 to 0.01). And the triangle search finds only 38–43 of 324 true images near zero-core members, before any filter runs.

The follow-up proposal was to reject only when residual > 10×precision AND |A⁻¹r| > 4h. Two adversarial reviews on 2026-10-24 (Claude and Codex `gpt-6-astra`) recommended against it:

- **Steep cusps and point masses defeat the Newton distance.** At a PowerLaw centre with slope 2.3/2.6, |A⁻¹r| ≈ 1.9h/0.96h while the residual is 600–100000×precision. The AND rule would keep candidates that #800 removes, and only `magnification_threshold` would catch them. A point mass gives 0.33h.
- **Near-caustic true images reach |A⁻¹r| of 4.2h, 5.6h and 14.8h** (|μ| 3.5e3–1e5). Only the residual leg keeps them.
- **The 4h cut is fitted to the data.** The affine bound is h/√3, and h/precision varies between 1 and 2. In the evidence, "true" meant polishing converged within 3h, which is circular.

Each condition covers a failure the other has, so stacking tuned thresholds is the wrong direction.

## Questions

1. **Root refinement.** Take triangle candidates as seeds, run a damped or trust-region Newton step on a fixed iteration budget, accept on convergence (residual at round-off, final correction small), deduplicate, and return the refined positions. Does this remove spurious singular-centre points without any threshold on profile class? What does it change in returned positions, likelihoods and implicit-diff gradients? A worked example is the oracle in `autolens_profiling/scripts/cluster/image_plane/_oracle.py`.
2. **Singularity-aware subdivision.** Refine around singular profile centres (zero-core dPIE, point mass, steep power law) during the search. Does it fix both the spurious points and the near-member completeness gap (38–43/324)?
3. **Constraints.** JAX: static shapes, padded candidates, vmap, a custom-JVP primal. Cost per solve. Cusp triplets about 7e-4″ apart.

## Evidence to build first

- An independent root census (the oracle) over: zero-core dPIE, steep PL, point mass, NFW, cored profiles across a range of core size / h, fold and cusp crossings, grid translations, and multi-plane.
- Probes from the review session (scratchpad `probe/caustic.py`, `probe/pl_centre.py`, plus the earlier `residual_sanity/`) as starting points.

## Out of scope

Shipping any new default. Any outcome goes back to the human as a design decision.
