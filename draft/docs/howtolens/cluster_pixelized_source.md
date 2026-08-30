# HowToLens cluster tutorial: show a pixelized source + fix the

Type: docs
Target: HowToLens
Repos:
- PyAutoLens
- autolens_workspace
- howtolens
Themes:
- cluster
- pixelization
- notebooks
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Epic: cluster-strong-lensing
Phase: 12
Parent: draft/feature/autolens/source_cluster_arc.md
Filed: 2026-08-19 (backfilled from git)

# HowToLens cluster tutorial: show a pixelized source + fix the stale cross-reference

Part of the Source & Cluster arc (phase 12 of 12), gated on phase 10. User request
(verbatim): "HowToLens Cluster should show pixelized source."

Audit: `HowToLens/scripts/chapter_4_scaling_up_lensing/tutorial_5_cluster_scale.py` is
point-source only, and its lines 181-184 claim extended-source cluster modeling "does
exist in PyAutoLens as a specialised follow-up analysis — see the autolens_workspace
cluster examples" — **that cross-reference is stale today** (no such example exists
until phase 10 lands). If any HowToLens release ships before phase 10, fix the stale
claim first as a one-line docs patch.

Work (after phase 10): extend tutorial 5 (or add a follow-up section) showing the
per-source-masked pixelized reconstruction of one cluster arc, teaching the
regime-ladder point — clusters default to point-source constraints, extended
reconstruction is the specialised follow-up — and forward-reference the cluster
source_science.py magnification story (phase 9). Tutorial prose is Opus-tier work per
the model-split convention.

<!-- formalised by the Intake (Conception) Agent on 2026-08-19 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/483da28c-8c96-4c83-ad87-a43448ca2164/scratchpad/source_cluster_phases/phase12_howtolens_cluster_pixelized.md -->
