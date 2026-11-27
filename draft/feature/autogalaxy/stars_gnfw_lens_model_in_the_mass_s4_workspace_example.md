# Workspace example

Type: feature
Target: autolens_workspace
Repos:
- autolens_workspace
Autonomy: supervised
Priority: high
Status: draft
Epic: stars-gnfw-lens-model-in-the-mass
Phase: 4
Witness: the example runs in smoke and recovers the input dark-matter fraction inside its 95% interval.
Lane: any
Filed: 2026-11-25

Simulate a stars + gNFW lens, fit it in the frame (the general frame around the aperture-normalised Sérsic and gNFW, `f_dm` shared by compound priors, the frame-unit shear and source priors), convert the result back to physical units (M*, M200).

The model shares `f_dm` through compound priors, so this slice also waits for the fix of `complete/2026/11/a-compound-prior-model-reloaded-from-model.md` (merged PyAutoFit#1810 on 2026-11-27, awaiting release); do not ship the project's `with_stable_prior_order` workaround. Model composition and the frame-unit priors: the epic prompt's "Assessment" section.

## Seam

Slice 4 of 4 of `draft/feature/autogalaxy/stars_gnfw_lens_model_in_the_mass.md` (epic `stars-gnfw-lens-model-in-the-mass`): owns autolens_workspace; after slice 3 (Physical-units profiles); last; needs slice(s) 2 merged first. One unattended run; reviewed against its own witness; revertible on its own PR(s).
