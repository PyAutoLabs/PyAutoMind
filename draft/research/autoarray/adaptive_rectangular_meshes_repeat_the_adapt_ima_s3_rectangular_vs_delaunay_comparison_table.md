# Rectangular vs Delaunay comparison table

Type: research
Target: autolens_workspace
Repos:
- autolens_workspace
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft
Epic: adaptive-rectangular-meshes-repeat-the-adapt-ima
Phase: 3
Consequence: judge
Witness: `results/compare_rectangular/index.html` renders every lens whose rectangular fits exist and lists the missing ones by name.
Review-minutes: 15
Lane: wsl-data
Filed: 2026-11-26

After the human's RAL runs of slice 2 are pulled, extend `scripts/compare.py` to put the rectangular arms next to the Delaunay arms on the same lenses: coverage numbers from slice 1, the `weight_power` / `weight_floor` each fit chose, mean squared normalized residual by data S/N, fraction above 3 sigma, lag-1 autocorrelation, with evidence as a secondary column. Show the comparison without a verdict.

## Seam

Slice 3 of 3 of `draft/research/autoarray/adaptive_rectangular_meshes_repeat_the_adapt_ima.md` (epic `adaptive-rectangular-meshes-repeat-the-adapt-ima`): owns autolens_workspace; after slice 2 (Rectangular fit arms, prepared not submitted); last; needs slice(s) 1, 2 merged first. One unattended run; reviewed against its own witness; revertible on its own PR(s).
