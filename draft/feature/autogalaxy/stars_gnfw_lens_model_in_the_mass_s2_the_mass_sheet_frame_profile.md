# The mass-sheet-frame profile

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
Witness: a unit test shows its deflections equal `(stars + gNFW deflections) / lambda_0 + (1 - 1/lambda_0) * (grid - centre)` to 1e-10 on NumPy and JAX, and the ring convergence of the transformed lens at `theta_ap` is zero to 1e-6 at `eps = 0`.
Lane: any
Filed: 2026-11-25

The stars + gNFW profile in the normalised frame, its λ₀ helper, the physical-unit attributes, and the positions penalty scaled by 1 / λ₀.

## Seam

Slice 2 of 3 of `draft/feature/autogalaxy/stars_gnfw_lens_model_in_the_mass.md` (epic `stars-gnfw-lens-model-in-the-mass`): owns PyAutoGalaxy, PyAutoLens; after slice 1 (Building blocks); before slice 3 (Workspace example); needs slice(s) 1 merged first. One unattended run; reviewed against its own witness; revertible on its own PR(s).
