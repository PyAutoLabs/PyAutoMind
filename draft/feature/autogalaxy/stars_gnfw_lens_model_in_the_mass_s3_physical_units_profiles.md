# Physical-units profiles

Type: feature
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
Autonomy: supervised
Priority: high
Status: draft
Epic: stars-gnfw-lens-model-in-the-mass
Phase: 3
Witness: unit tests show a Sérsic built from a stellar mass returns that total mass to 1e-8 and a gNFW built from M200 encloses M200 inside r200 to 1e-6, on NumPy and JAX.
Lane: any
Filed: 2026-11-25

A Sérsic normalised by physical stellar mass (or M/L) and a gNFW by M200, JAX-traceable, with the conversions also available as derived quantities (detail: the epic prompt's "Physical-units parameterisation" section).

## Seam

Slice 3 of 4 of `draft/feature/autogalaxy/stars_gnfw_lens_model_in_the_mass.md` (epic `stars-gnfw-lens-model-in-the-mass`): owns PyAutoGalaxy; after slice 2 (The mass-sheet frame); before slice 4 (Workspace example); needs slice(s) 1 merged first. One unattended run; reviewed against its own witness; revertible on its own PR(s).
