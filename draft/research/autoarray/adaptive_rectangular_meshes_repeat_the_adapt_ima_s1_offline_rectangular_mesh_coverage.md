# Offline rectangular mesh coverage

Type: research
Target: PyAutoArray
Repos:
- PyAutoArray
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft
Epic: adaptive-rectangular-meshes-repeat-the-adapt-ima
Phase: 1
Consequence: glance
Witness: `results/rectangular/index.html` and `results/rectangular/coverage.csv` exist with one row per lens x adapt-image variant x grid point for all 19 lenses, and `python scripts/rectangular_metrics.py` reruns from a clean shell.
Review-minutes: 5
Lane: wsl-data
Filed: 2026-11-26

In the science project `~/Science/Science/development/adapt_snr_cap`, add `scripts/rectangular_metrics.py`: for each of the 19 lenses, take the source adapt image the completed Delaunay arms already produced and build the RectangularAdaptImage and RectangularRTUAdaptImage / RTUAdaptDensity meshes of @PyAutoArray offline (no fits) over a grid of `weight_power` x `weight_floor`, for a capped, an uncapped and a soft-transformed (`regularization_image_from`) adapt image. Report source-plane pixel size across the source against the magnified image pixel, and pixels on the source against pixels on empty sky. No library or workspace edits; the human judges.

## Seam

Slice 1 of 3 of `draft/research/autoarray/adaptive_rectangular_meshes_repeat_the_adapt_ima.md` (epic `adaptive-rectangular-meshes-repeat-the-adapt-ima`): owns PyAutoArray; first — nothing before it; before slice 2 (Rectangular fit arms, prepared not submitted). One unattended run; reviewed against its own witness; revertible on its own PR(s).
