# Magnification errors via posterior draws, standalone in source_science

Type: feature
Target: PyAutoLens
Repos:
- PyAutoLens
Themes:
- cluster
- samplers
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: ready
Epic: cluster-strong-lensing
Phase: 7
Parent: draft/feature/autolens/source_cluster_arc.md
Filed: 2026-08-19 (backfilled from git)

# Magnification errors via posterior draws, standalone in source_science

Part of the Source & Cluster arc (phase 7 of 12), gated on phases 5-6. User request
(verbatim): "Errors via posterior draws to go with all of this. I think errors in
source_science.py is where were headed, with the results folder being the main
description of how to get any errors but a user doing source science should get errors
standalone from source science."

Science anchor — LEGGOS II: magnification uncertainties from ~300 models drawn from the
posterior; per-clump errors by evaluating μ at the same pixel across the ensemble;
report percentile confidence intervals; fractional uncertainty σ_μ/|μ_best| ~0.03-0.09.

Audit findings: NO source_science.py computes errors today — all magnification numbers
are single max-likelihood point estimates. Posterior-draw machinery exists only in
guides (scripts/guides/results/aggregator/{models,data_fitting}.py,
randomly_drawn_via_pdf). The only error-bearing magnification in the library is the
latent-variable path (autolens/analysis/latent.py:218 `magnification`) — but it is
light-profile-only (NaN for pixelized sources), a single global scalar, and disabled by
default (config/latent.yaml magnification: false).

Work (lean existing lever — reuse the samples-draw API, don't build new machinery):
1. Standalone worked pattern in every source_science.py (both tiers): draw N instances
   from result.samples, rebuild the tracer per draw, recompute the phase-5/6
   magnification quantities (point μ at positions, flux-ratio μ, area μ), report
   median + percentile intervals. Make N and runtime cost explicit prose.
2. Decide the latent story: extend the magnification latent to pixelized sources (or
   document clearly why not), and whether point-μ-at-position latents (per multiple
   image) are worth registering — latents give free posterior errors on every fit.
3. Cluster-ready: the draw loop must support per-source plane_redshift (multi-plane)
   for phase 9 to consume.
Output feeds the phase-8 uncertainty map (per-pixel σ_μ/μ over the draw ensemble).

<!-- formalised by the Intake (Conception) Agent on 2026-08-19 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/483da28c-8c96-4c83-ad87-a43448ca2164/scratchpad/source_cluster_phases/phase07_magnification_errors_posterior_draws.md -->
