# Rectangular fit arms, prepared not submitted

Type: research
Target: autolens_workspace
Repos:
- autolens_workspace
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft
Epic: adaptive-rectangular-meshes-repeat-the-adapt-ima
Phase: 2
Consequence: glance
Witness: each new arm completes one lens in `PYAUTO_TEST_MODE` locally, and the submit script's dry-run lists 19 lenses x 3 arms without submitting.
Review-minutes: 5
Lane: wsl-data
Filed: 2026-11-26

Add rectangular-mesh arms (capped, uncapped, soft adapt image, `weight_power` / `weight_floor` free as in the workspace rectangular SLaM) to `scripts/slam.py` and the `hpc/` submit scripts of `adapt_snr_cap`, mirroring the existing Delaunay arms. Run each arm on one lens in test mode on the laptop. Do not submit to RAL: the human submits.

## Seam

Slice 2 of 3 of `draft/research/autoarray/adaptive_rectangular_meshes_repeat_the_adapt_ima.md` (epic `adaptive-rectangular-meshes-repeat-the-adapt-ima`): owns autolens_workspace; after slice 1 (Offline rectangular mesh coverage); before slice 3 (Rectangular vs Delaunay comparison table). One unattended run; reviewed against its own witness; revertible on its own PR(s).
