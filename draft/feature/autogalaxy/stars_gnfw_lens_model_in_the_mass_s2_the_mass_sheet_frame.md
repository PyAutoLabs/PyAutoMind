# The mass-sheet frame

Type: feature
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
- PyAutoLens
Autonomy: supervised
Priority: high
Status: draft
Epic: stars-gnfw-lens-model-in-the-mass
Phase: 2
Witness: a unit test shows the frame's deflections for stars + gNFW equal `(stars + gNFW deflections) / lambda_0 + (1 - 1/lambda_0) * (grid - centre)` to 1e-10 on NumPy and JAX, the ring convergence of the transformed lens at `theta_ap` is zero to 1e-6 at zero mass offset, and, if the separate form is chosen, the same identity holds for a power law.
Lane: any
Filed: 2026-11-25

First the assessment in the epic prompt's "Assess first" section (a separate, general rescaling object against the composite profile), written into the plan; then the chosen form, its λ₀ helper, the physical-unit attributes, and the positions penalty scaled by 1 / λ₀.

## Seam

Slice 2 of 4 of `draft/feature/autogalaxy/stars_gnfw_lens_model_in_the_mass.md` (epic `stars-gnfw-lens-model-in-the-mass`): owns PyAutoGalaxy, PyAutoLens; after slice 1 (Building blocks); before slice 3 (Physical-units profiles); needs slice(s) 1 merged first. One unattended run; reviewed against its own witness; revertible on its own PR(s).
