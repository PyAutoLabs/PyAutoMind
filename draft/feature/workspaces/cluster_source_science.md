# Cluster source_science.py: robust magnification science at cluster scale (no meshes

Type: feature
Target: workspaces
Repos:
- workspaces
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
Phase: 9
Parent: draft/feature/autolens/source_cluster_arc.md
Filed: 2026-08-19 (backfilled from git)

# Cluster source_science.py: robust magnification science at cluster scale (no meshes yet)

Part of the Source & Cluster arc (phase 9 of 12), gated on phases 1, 3, 5-8. User
request (verbatim): "Make extra sure source_science.py cluster is robust, e.g. all
examples of magnifications above but no mesh support yet."

Audit finding: `scripts/cluster/` has NO source_science.py at all (only start_here,
modeling, simulator, plot, likelihood_function, csv_api, mass_parameterizations,
lenstool/). Cluster magnification today is just the PointSolver
magnification_threshold arg and the μ²-weighted source-plane χ² narrative in
likelihood_function.py:381-481.

Work — new `scripts/cluster/source_science.py` (point-source tier only; pixelized
cluster sources are phase 10):
1. Point μ at each multiple image per source, multi-plane (per-source plane_redshift —
   the #678 final-plane-default trap must be spelled out in prose).
2. Point μ at arbitrary (y,x) — the LEGGOS clump-centroid pattern.
3. Area magnification of an arc segment via the LEGGOS Eq. 6-7 pixel-inversion sum,
   with the critical curve as segmentation boundary (phase 3/6 machinery).
4. Errors on all of the above via posterior draws (phase 7 pattern, multi-plane).
5. Magnification maps + uncertainty maps per source plane (phase 8 plotting).
6. Robustness: run against the A2744 start_here fit and the simulated cluster;
   smoke-viable subset (cluster scripts are currently not smoke-able — keep the heavy
   draws behind the standard guard).
Mirror the group/source_science.py structure for the regime ladder; cite LEGGOS II,
Richard+17 (HFF magnification-map deliverables) and Atek+15 (magnification as source-
science tool) in the prose. Coordinates with
draft/docs/workspaces/cluster_regime_narrative.md (narrative alignment) — this phase
delivers the science example; that draft delivers the regime prose.

<!-- formalised by the Intake (Conception) Agent on 2026-08-19 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/483da28c-8c96-4c83-ad87-a43448ca2164/scratchpad/source_cluster_phases/phase09_cluster_source_science.md -->
