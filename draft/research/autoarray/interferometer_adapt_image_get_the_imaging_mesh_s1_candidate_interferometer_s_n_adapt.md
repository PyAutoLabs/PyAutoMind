# Candidate interferometer S/N adapt images, offline

Type: research
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft
Epic: interferometer-adapt-image-get-the-imaging-mesh
Phase: 1
Consequence: glance
Witness: `results/interferometer/index.html` and `results/interferometer/coverage.csv` exist with one row per dataset x candidate plus the imaging reference, and the script reruns from a clean shell.
Review-minutes: 5
Lane: wsl-data
Filed: 2026-11-26

In the science project `~/Science/Science/development/adapt_snr_cap`, add `scripts/interferometer_adapt.py`: on the @autolens_workspace simulated interferometer datasets (whose true source is known, so no fits are needed), build three candidate adapt images — the model source image divided by one image-plane noise level `sqrt(0.5 * sum |noise_map| ** 2)`; the same with a noise level per resolution element from the dirty beam; and the clipped flux model image with the `peak_share` weighting's two S/N numbers rescaled into flux units — then draw the Hilbert mesh each gives offline with the `peak_share` weighting of `scripts/mesh_weighting.py` and compare coverage (background share, mesh points per pixel by S/N band, points on compact clumps) with the imaging meshes of a similar source. No library or workspace edits; the human picks a candidate.

## Seam

Slice 1 of 2 of `draft/research/autoarray/interferometer_adapt_image_get_the_imaging_mesh.md` (epic `interferometer-adapt-image-get-the-imaging-mesh`): owns PyAutoGalaxy; first — nothing before it; before slice 2 (Interferometer fit arms, prepared not submitted). One unattended run; reviewed against its own witness; revertible on its own PR(s).
