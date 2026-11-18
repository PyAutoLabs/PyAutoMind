# Cluster pixelized-source refinement: per-source masks via AnalysisFactor

Type: feature
Target: workspaces
Repos:
- workspaces
Themes:
- cluster
- pixelization
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: glance
Witness: `scripts/cluster/features/extended_source/` runs to completion under the smoke profile with one AnalysisImaging per source, each bound to its own mask; a source with no mask entry raises rather than falling back to a shared or whole-cluster mask; and one factor's log-likelihood is unchanged when another source's light profile is perturbed, proving per-factor evaluation does not cross sources.
Review-minutes: 3
Unattended: ready
Lane: any
Epic: cluster-strong-lensing
Phase: 10
Parent: draft/feature/autolens/source_cluster_arc.md
Filed: 2026-08-19 (backfilled from git)

# Cluster pixelized-source refinement: per-source masks via AnalysisFactor

Part of the Source & Cluster arc (phase 10 of 12), gated on phases 4 and 9. User
request (verbatim): "Ability to use parametric pixelized source reconstructions on
clusters after model is inferred, perhaps include a few extra mass components for
refining it. Requires us to deal with masking challenges, that is every source needs to
be paired to a mask. You could either give it one image for the whole cluster, which is
huge, and would end up fitting the wrong stuff. Instead, each source needs its own mask,
thus we need some sort of system to ensure that happens. Obvious API is to use
AnalysisFactor in a similar fashion to multi_dataset, e.g. one Analysis for each source,
and to use the same source naming API to only evaluate each source light profile for
each mask. This requires users to use a GUI to make custom masks, which is fine but
annoying."

Audit: the mechanism fully exists — the gap is purely the example/wiring layer.
- `af.AnalysisFactor(prior_model, analysis)` binds one Analysis (one masked dataset) to
  a shared prior_model; cluster start_here.py:419-434 already uses one factor per
  SOURCE (point datasets); multi_dataset/start_here.py:207-233,321-350 is the exact
  per-dataset-mask template; multi_dataset/features/imaging_and_point_source/modeling.py
  is the nearest precedent for mixing point positions + pixelized imaging under one
  mass model (galaxy-scale today).
- complete/2026/11/cluster-regime-narrative.md planned a features/extended_source/
  cluster follow-up (one A2744 arc, pixelized, cluster mass model as start). Its
  narrative half shipped (autolens_workspace#671); the extended-source example was
  handed to this phase (see "Deferred" below).

Work:
1. Example: `scripts/cluster/features/extended_source/` — post-inference refinement:
   fix (or narrow priors from) the inferred cluster mass model, add a few free local
   mass components near the refined arc, one AnalysisImaging per source with its own
   mask, one AnalysisPoint per remaining source, all in one FactorGraphModel.
2. Masking system: per-source mask pairing convention (source-name → mask file), GUI
   custom-mask flow documented (existing mask GUI), loud failure when a source lacks a
   mask (no silent guards).
3. Source-naming API: ensure per-factor model evaluation only computes that source's
   light for that mask (verify what FactorGraphModel already gives; only extend the
   library if evaluation actually crosses sources).
4. Decide and document: whole-cluster single mask explicitly rejected (fits the wrong
   stuff) — say so in prose.

<!-- formalised by the Intake (Conception) Agent on 2026-08-19 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/483da28c-8c96-4c83-ad87-a43448ca2164/scratchpad/source_cluster_phases/phase10_cluster_pixelized_analysisfactor.md -->

## Deferred — human ruling 2026-11-18

Cluster extended sources will not be developed for a while (human, /health session
2026-11-18, closing autolens_workspace#670). This prompt now owns the
`features/extended_source/` example and its `autolens_workspace_test` integration
script from cluster-regime-narrative. Its three open questions were never answered and
must be settled before planning:

1. **Data.** The bundled A2744 `data.fits` is a 0.3"/px hips2fits colour cutout with
   no noise map or PSF, unsuitable for a pixelized inversion. Use (a) HFF/JWST imaging
   of one A2744 arc (prep plus a committed dataset), (b) an extended arc simulated from
   the `cluster/simulator.py` mass model, or (c) both?
2. **Mass-model handoff.** Fix the cluster mass at the point-source fit and refit only
   the arc's local perturbers plus the source, or free the full mass model with priors
   from the point fit?
3. **Sequencing.** Wait for phase 9 (`cluster_source_science`) to land first?
