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
Witness: unit tests show, on NumPy and JAX, for the frame around stars + gNFW and around an elliptical power law: a grid traces to `centre + (source-plane grid of the physical lens - centre) / lambda_0` to 1e-10; the mean convergence inside `theta_ap` is `1 + eps` and the ring convergence at `theta_ap` is zero at `eps = 0`, both to 1e-6; a circular power law gives `lambda_0 = (slope - 1) / 2` to 1e-6; changing the power law's `einstein_radius` leaves the frame's deflections unchanged to 1e-10; and `PositionsLH` gives the same penalty for a frame lens as for its physical lens (the physical view, with the shear times `lambda_0`).
Lane: any
Filed: 2026-11-25

The general `MassSheetFrame` of the epic prompt's "Assessment" section (settled 2026-11-26: a profile wrapping a list of mass profiles; the composite is not built), its λ₀ and `mass_scale`, the physical view and attributes, and the positions penalty scaled by 1 / λ₀.

The design question is closed: do not reassess it. Read the epic prompt's "Assessment" section first; it gives the algebra, where the object lives, what was checked numerically and what goes with the frame. The sketch it was checked with is `~/Science/Science/scratch/mass_sheet_frame_assessment/general_frame_check.py` (a sketch, not library code).

## Seam

Slice 2 of 4 of `draft/feature/autogalaxy/stars_gnfw_lens_model_in_the_mass.md` (epic `stars-gnfw-lens-model-in-the-mass`): owns PyAutoGalaxy, PyAutoLens; after slice 1 (Building blocks); before slice 3 (Physical-units profiles); needs slice(s) 1 merged first. One unattended run; reviewed against its own witness; revertible on its own PR(s).
