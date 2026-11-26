# Interferometer fit arms, prepared not submitted

Type: research
Target: autolens_workspace
Repos:
- autolens_workspace
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft
Epic: interferometer-adapt-image-get-the-imaging-mesh
Phase: 2
Consequence: glance
Witness: each arm completes one dataset in `PYAUTO_TEST_MODE` locally, and the submit script's dry-run lists every dataset x arm without submitting.
Review-minutes: 5
Lane: wsl-data
Blocked-by: PyAutoArray#714
Filed: 2026-11-26

Add interferometer SLaM arms to `adapt_snr_cap` (`scripts/` and `hpc/`): the current clipped-model-image behaviour against each slice-1 candidate, using the imaging mesh weighting and AdaptSplit input. Run each arm on one dataset in test mode on the laptop. Do not submit to RAL and do not change the library or workspace defaults: the human picks the candidate and submits.

## Seam

Slice 2 of 2 of `draft/research/autoarray/interferometer_adapt_image_get_the_imaging_mesh.md` (epic `interferometer-adapt-image-get-the-imaging-mesh`): owns autolens_workspace; after slice 1 (Candidate interferometer S/N adapt images, offline); last; needs slice(s) 1 merged first. One unattended run; reviewed against its own witness; revertible on its own PR(s).
