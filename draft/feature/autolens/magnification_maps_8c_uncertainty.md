# Magnification maps 8c: LEGGOS Fig-4 fractional magnification uncertainty map

Type: feature
Target: autolens_workspace
Repos:
- autolens_workspace
- PyAutoGalaxy
Themes:
- visualization
- cluster
Epic: cluster-strong-lensing
Phase: 8c
Parent: draft/feature/autolens/magnification_maps_visualization.md
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: no
Filed: 2026-11-02

## Context

Slice of phase 8. Per image pixel sigma_mu/|mu_best| over the phase-7b posterior draws (each draw → 8a mu map), with
the best-fit constant-mu contours overlaid, as LEGGOS II Fig. 4. Library helper only if the draw loop proves reusable.
Workspace: source_science scripts (start with imaging). Witness: map renders from 100 draws on imaging simple.
